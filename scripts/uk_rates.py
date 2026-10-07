#!/usr/bin/env python3
# ci-line: B4 | UK rates module (unit tests against the gov.uk 2025/26 figures) | --selftest
"""UK income tax, employee NI and student loans for the teaching year: the one copy in code (canon §7.1.4).

    python scripts/uk_rates.py --selftest

Every verifier that checks a tax or NI figure imports this module, as the statistics verifiers
import stats_common.py; none restates a rate. Until 3 Oct 2026 each game and verifier carried its
own copy, so core-maths-paper1 kept the pre-January-2024 12% employee NI rate with nothing to catch it.

Teaching year 2025/26 (Jon, 3 Oct 2026): exam papers are set before the tax year they are sat in,
so the June 2027 series most likely uses 2025/26 figures. THE APRIL RULE (Jon, 3 Oct 2026): each
April, advance the teaching year by one (2025/26 -> 2026/27 in April 2027), in one PR that changes
TEACHING_YEAR, REVIEW_BY and the figures here, canon §7.1.4's table, and every game check-tax-year.py
registers. Jon has a yearly 1 April calendar reminder; check-tax-year.py enforces it: it warns from
REVIEW_WARN_FROM and fails after REVIEW_BY until the year is advanced. England, Wales and Northern
Ireland; never Scottish rates.

Sources (gov.uk):
  https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2025-to-2026  (tax, NI, student loans)
  https://www.gov.uk/income-tax-rates/income-over-100000
  https://www.gov.uk/repaying-your-student-loan/what-you-pay  (rates; its thresholds are the CURRENT year's)

Money is exact: every function takes and returns fractions.Fraction (or int), never a float.
"""
import datetime
import sys
from fractions import Fraction as F

TEACHING_YEAR = "2025/26"
# The April rule: advance TEACHING_YEAR (and these two dates, by a year) each April.
REVIEW_WARN_FROM = datetime.date(2027, 4, 1)
REVIEW_BY = datetime.date(2027, 4, 30)

PERSONAL_ALLOWANCE = 12570
PA_TAPER_FROM = 100000          # the allowance falls £1 for every £2 above this
BASIC_RATE_BAND = 37700         # on TAXABLE income
HIGHER_RATE_LIMIT = 125140      # on taxable income; also where the allowance reaches zero
BASIC_RATE = F(20, 100)
HIGHER_RATE = F(40, 100)
ADDITIONAL_RATE = F(45, 100)

NI_PRIMARY_THRESHOLD = 12570    # employee Class 1, a year
NI_UPPER_EARNINGS_LIMIT = 50270
NI_MAIN_RATE = F(8, 100)
NI_UPPER_RATE = F(2, 100)

# Student loans, England and Wales (employers 2025 to 2026, "Student loan and postgraduate loan
# recovery"): yearly thresholds; 9% above the threshold on Plans 1, 2 and 4, 6% on a Postgraduate Loan.
# Plan 5 has no 2025/26 threshold: its repayments began in April 2026.
STUDENT_LOAN_THRESHOLDS = {"plan1": 26065, "plan2": 28470, "plan4": 32745, "postgraduate": 21000}
STUDENT_LOAN_RATES = {"plan1": F(9, 100), "plan2": F(9, 100), "plan4": F(9, 100),
                      "postgraduate": F(6, 100)}

SOURCES = [
    "https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2025-to-2026",
    "https://www.gov.uk/income-tax-rates/income-over-100000",
    "https://www.gov.uk/repaying-your-student-loan/what-you-pay",
]


def personal_allowance(gross):
    """The allowance after the taper (whole pounds, as HMRC applies it)."""
    return max(0, PERSONAL_ALLOWANCE - max(0, int(gross) - PA_TAPER_FROM) // 2)


def taxable_income(gross):
    return max(0, gross - personal_allowance(gross))


def income_tax(gross):
    t = taxable_income(gross)
    return (min(t, BASIC_RATE_BAND) * BASIC_RATE
            + max(0, min(t, HIGHER_RATE_LIMIT) - BASIC_RATE_BAND) * HIGHER_RATE
            + max(0, t - HIGHER_RATE_LIMIT) * ADDITIONAL_RATE)


def employee_ni(gross):
    """Annual employee Class 1 NI on an annual salary (no weekly/monthly period effects)."""
    return (max(0, min(gross, NI_UPPER_EARNINGS_LIMIT) - NI_PRIMARY_THRESHOLD) * NI_MAIN_RATE
            + max(0, gross - NI_UPPER_EARNINGS_LIMIT) * NI_UPPER_RATE)


def take_home(gross):
    return gross - income_tax(gross) - employee_ni(gross)


def student_loan(gross, plan):
    """Yearly repayment on a yearly salary (no pay-period effects). plan: plan1/plan2/plan4/postgraduate."""
    return max(0, gross - STUDENT_LOAN_THRESHOLDS[plan]) * STUDENT_LOAN_RATES[plan]


def review_status(today):
    """'ok', 'warn' (from 1 April: advance the teaching year) or 'fail' (after REVIEW_BY)."""
    if today > REVIEW_BY:
        return "fail"
    return "warn" if today >= REVIEW_WARN_FROM else "ok"


def percent(rate):
    """F(8, 100) -> '8' (the figure a stem prints before %)."""
    v = rate * 100
    return str(v.numerator) if v.denominator == 1 else str(float(v))


def selftest():
    # hand-worked from the gov.uk figures above
    assert personal_allowance(31070) == 12570
    assert income_tax(31070) == 3700                              # 20% of 18,500
    assert employee_ni(22000) == F(75440, 100)                    # 8% of 9,430
    assert employee_ni(19770) == 576 and income_tax(19770) == 1440
    assert take_home(19770) == 17754
    assert personal_allowance(110000) == 7570                     # 10,000 over: -5,000
    assert personal_allowance(125140) == 0 and personal_allowance(125139) == 1
    assert income_tax(50270) == 7540                              # top of the basic band
    # 60,000: taxable 47,430 -> 37,700 at 20% + 9,730 at 40% = 7,540 + 3,892
    assert income_tax(60000) == 11432
    # 130,000: no allowance; 37,700 at 20% + 87,440 at 40% + 4,860 at 45%
    assert income_tax(130000) == 7540 + 34976 + F(4860 * 45, 100)
    assert employee_ni(60000) == F(301600, 100) + F(19460, 100)   # 8% of 37,700 + 2% of 9,730
    assert employee_ni(12570) == 0 and employee_ni(10000) == 0
    assert percent(NI_MAIN_RATE) == "8" and percent(BASIC_RATE) == "20"
    assert student_loan(30000, "plan2") == F(13770, 100)              # 9% of 1,530
    assert student_loan(28000, "plan2") == 0                          # below the 2025/26 threshold
    assert student_loan(25000, "postgraduate") == 240                 # 6% of 4,000
    assert student_loan(30000, "plan1") == F(35415, 100)              # 9% of 3,935
    assert review_status(datetime.date(2027, 3, 31)) == "ok"
    assert review_status(datetime.date(2027, 4, 1)) == "warn"
    assert review_status(datetime.date(2027, 4, 30)) == "warn"
    assert review_status(datetime.date(2027, 5, 1)) == "fail"
    print("uk_rates selftest: PASS (teaching year %s)" % TEACHING_YEAR)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        print(__doc__)
