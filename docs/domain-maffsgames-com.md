# maffsgames.com — 301 alias, set up 24 Sep 2026

`maffsgames.com` was bought on 24 Sep 2026 and now **301-redirects to `maffsgames.co.uk`**.
It serves no content of its own and never should.

## The decision: .co.uk stays canonical

`.com` redirects to `.co.uk`, not the other way round. The reasons, in order of weight:

- **117 canonical tags, 110 sitemap URLs and `robots.txt` all hardcode `https://maffsgames.co.uk`.**
  Flipping the canonical domain is a repo-wide sweep of exactly the shape that killed
  `chart-interrogator` (`96381d74`) and `modular-battle` (`76514c70`). Not worth it.
- **GitHub Pages serves one custom domain per repo.** `CNAME` holds `maffsgames.co.uk`. Both
  domains cannot be served from this repo regardless.
- **Analytics.** GA4 is a single property (`G-992JLHLP2D`) with the snippet inlined on 118 pages
  and `storage: 'none'`. If both domains served the same HTML there would be two hostnames in one
  property and, being cookieless, **no way to dedupe a visitor** — sessions split and page_views
  roughly double, unrecoverably after the fact.
- The audience is UK schools and FE colleges, where `.co.uk` is a trust signal, not a downgrade.

**Why a 301 solves the analytics problem completely:** the redirect is issued at Cloudflare's edge
before any origin fetch, so no page from this repo is ever returned on a `.com` URL and the gtag
snippet never executes with a `.com` hostname. No cross-domain measurement config, no referral
exclusion, and no change to `analytics.js` or the 118 inline snippets was needed. **Nothing in this
repo changed for any of this.**

## How it is wired

Registrar is **IONOS** for both domains. Only `.com` was moved to Cloudflare; `.co.uk` keeps IONOS
nameservers because they also carry the live `contact@maffsgames.co.uk` mailbox.

- `maffsgames.com` nameservers -> `simone.ns.cloudflare.com`, `steven.ns.cloudflare.com`
- Cloudflare zone `maffsgames.com`, **Free plan**, total cost **GBP 0**

DNS records in the Cloudflare zone — all three, nothing else:

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| A | `maffsgames.com` | `192.0.2.1` | **Proxied** |
| A | `www` | `192.0.2.1` | **Proxied** |
| TXT | `maffsgames.com` | `v=spf1 -all` | DNS only |

`192.0.2.1` is reserved TEST-NET-1 — Cloudflare's documented placeholder for a redirect-only zone.
Nothing is ever fetched from it. **Both A records must stay Proxied: Redirect Rules only run on
proxied traffic.** If either goes grey-cloud the domain times out instead of redirecting.

`v=spf1 -all` states that no host may send mail as `maffsgames.com`. The IONOS MX, DKIM, DMARC,
autodiscover and `_domainconnect` records were all deleted — `.com` has no mailbox. If one is ever
wanted, **Cloudflare Email Routing** is free and writes its own MX.

Redirect Rule, in the `maffsgames.com` zone (Rules -> Overview -> Redirect Rules), built from the
"Redirect to a different domain" template:

- **If:** All incoming requests
- **Then:** Dynamic redirect, `concat("https://maffsgames.co.uk", http.request.uri.path)`
- **Status:** 301, **Preserve query string: on**

`http.request.uri.path` pairs with the checkbox. Using `http.request.uri` (which already contains
the query) *with* the checkbox would append the query twice.

## Certificates — both free, neither needs attention

| Domain | Certificate | Issued by |
|--------|-------------|-----------|
| `maffsgames.co.uk` | Let's Encrypt, auto-renewing | GitHub Pages |
| `maffsgames.com` | Let's Encrypt, auto-renewing, covers apex + `*.maffsgames.com` | Cloudflare Universal SSL |

**IONOS will claim `maffsgames.com` "does not yet have SSL and will be marked as insecure", with an
Activate link. It is wrong** — IONOS cannot see a certificate it does not serve. Do not buy an IONOS
SSL product for either domain. The one offered for `.co.uk` is "use with my own server", which
GitHub Pages gives you no way to install. Both certs above are free and automatic.

## Verified 24 Sep 2026, after deployment

    https://maffsgames.com/                      301 -> https://maffsgames.co.uk/
    https://www.maffsgames.com/                  301 -> https://maffsgames.co.uk/
    http://maffsgames.com/                       301 -> https://maffsgames.co.uk/
    /games/matrix-crunch/                        301 -> path preserved, 1 hop to 200
    /games/suvat/?level=4&mode=test              301 -> query string preserved exactly
    maffsgames.co.uk                             200 from 185.199.108.153 (unchanged)
    www.maffsgames.co.uk                         301 -> apex (unchanged)

The `.com` 301 response body is Cloudflare's bare stub: no `<script>`, no `gtag`, no
`G-992JLHLP2D`. Confirmed by grep against the live response.

## Rollback reference — IONOS records as they were before the move

Only needed if `maffsgames.com` is ever pointed back at IONOS.

    A     @                217.160.0.211                        (IONOS parking)
    AAAA  @                2001:8d8:100f:f000::200              (IONOS parking)
    MX    @                10 mx00.ionos.co.uk / 10 mx01.ionos.co.uk
    TXT   @                v=spf1 include:_spf-eu.ionos.com ~all
    TXT   _dep_ws_mutex    e2c924d844ad2495...
    CNAME _domainconnect   _domainconnect.ionos.com
    CNAME _dmarc           dmarc.ionos.co.uk
    CNAME s1-ionos._domainkey   s1.dkim.ionos.com
    CNAME s2-ionos._domainkey   s2.dkim.ionos.com
    CNAME autodiscover     adsredir.ionos.info
    NS    ns1106.ui-dns.de / ns1039.ui-dns.biz / ns1067.ui-dns.org / ns1023.ui-dns.com

`maffsgames.co.uk` was not touched. For reference its live config is four GitHub Pages A records
(`185.199.108-111.153`), `www` CNAME to `orthogonalmaffs.github.io`, IONOS MX, and the IONOS SPF.

## Not done, deliberately

- **`sitemap.xml` and Search Console were left alone.** The 301 tells Google to consolidate onto
  `.co.uk`. `.com` must never appear in the sitemap.
- **No hostname guard added to the gtag snippet.** It is 118 inline copies, and with the edge
  redirect in place it buys nothing here. The parked to-do item about non-production hosts is a
  separate concern.
