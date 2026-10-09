/**
 * MaffsInitials — the initials rules, shared.
 *
 * Defined FIRST, in its own scope, with no reference to the Firebase SDK, so it
 * exists even when the SDK fails to load ("firebase is not defined"). Device-local
 * features that name things by initials (schools/assets/progress.js) use it without
 * needing Firebase; the leaderboard pop-up below uses the same two functions, so
 * there is one copy of the rule. Exported 30 Sep 2026 (Six Sevens, Bruv contract);
 * the pop-up's behaviour is unchanged.
 *
 *   MaffsInitials.normaliseInitials(raw) -> letters A-Z only, upper-cased
 *   MaffsInitials.isBlocked(str)         -> true if it is a blocked 3-letter combo
 */
(function() {
  'use strict';

  // Blocked 3-letter combos (profanity filter)
  var BLOCKED = [
    'ASS','FUK','FUC','FCK','CNT','COK','DIK','DIX','FAG','GAY','JEW','KKK',
    'NAZ','NIG','NIP','POO','SEX','SHT','SLT','TIT','WTF','FKU','CUM','VAG',
    'WNK','NOB','KNB','BUM','ARS','COC','DIC','FFS','GIT','HOE','JAP','JIZ',
    'KYS','NUT','ORG','PIS','RAP','STD','SUK','SUC','TOE','TOD','WOG','WOP'
  ];

  function normaliseInitials(raw) {
    return String(raw == null ? '' : raw).replace(/[^A-Za-z]/g, '').toUpperCase();
  }

  function isBlocked(str) {
    var up = str.toUpperCase().replace(/[^A-Z]/g, '');
    for (var i = 0; i < BLOCKED.length; i++) {
      if (up === BLOCKED[i]) return true;
    }
    return false;
  }

  window.MaffsInitials = { isBlocked: isBlocked, normaliseInitials: normaliseInitials };
})();

/**
 * MaffsGames Firebase Leaderboard
 * Anonymous score submission with optional 3-letter initials
 * No personal data collected beyond freely-given initials
 *
 * Load Firebase CDN compat scripts BEFORE this file:
 *   <script src="https://www.gstatic.com/firebasejs/10.8.0/firebase-app-compat.js"></script>
 *   <script src="https://www.gstatic.com/firebasejs/10.8.0/firebase-database-compat.js"></script>
 *   <script src="../../schools/assets/firebase-leaderboard.js"></script>
 */

(function() {
  'use strict';

  // Firebase config
  var firebaseConfig = {
    apiKey: "AIzaSyCvLgIk8hdHaX7nL0aZ3p_Q8zNlRuKX18g",
    authDomain: "maffsgames-c1c9f.firebaseapp.com",
    databaseURL: "https://maffsgames-c1c9f-default-rtdb.europe-west1.firebasedatabase.app",
    projectId: "maffsgames-c1c9f",
    storageBucket: "maffsgames-c1c9f.firebasestorage.app",
    messagingSenderId: "571041014777",
    appId: "1:571041014777:web:d69dea42eec94aeca75328"
  };

  // Slug → human-readable name
  var GAME_NAMES = {
    'split-it':'Split It','sequence-solver':'Sequence Solver','estimation-golf':'Estimation Golf',
    'estimation-engine':'Estimation Engine','factor-race':'Factor Race','prime-factorisation':'Prime Sprint',
    'prime-or-composite':'Prime or Composite','percentage-flip':'Percentage Flip',
    'fraction-equivalence':'Fraction Snap','equatle':'Equatle','52dle':'52-dle',
    'constructions-lab':'Constructions Lab','word-problem-decoder':'Word Problem Decoder',
    'equation-builder':'Equation Builder','spot-the-error':'Spot the Error','truth-buster':'Truth Buster',
    'spot-the-muppet':'Spot the Muppet','terrible-advice':'Terrible Advice',
    'wrong-on-the-internet':'Wrong on the Internet','maths-court':'Maths Court',
    'expected-damage':'Expected Damage','gradient-hunter':'Gradient Hunter',
    'negative-number-line':'Negative Number Line','think-of-a-number':'Think of a Number',
    'formula-plug-in':'Formula Plug-In','decimal-detective':'Decimal Detective',
    'four-quadrant-explorer':'Four Quadrant Explorer','like-terms-collector':'Like Terms Collector',
    'probability-pioneer':'Probability Pioneer','shape-shifter':'Shape Shifter','new-shapes':'New Shapes',
    'index-laws':'Index Laws','quadratic-factoriser':'Quadratic Factoriser','trig-wars':'Trig Wars',
    'trig-worms':'Trig Worms','modular-battle':'Modular Battle','surd-simplifier':'Surd Simplifier',
    'proportion-blaster':'Proportion Blaster','trig-identity-duel':'Trig Identity Duel',
    'standard-form-blitz':'Standard Form Blitz','simultaneous-solver':'Simultaneous Solver',
    'circle-theorem-spotter':'Circle Theorem Spotter','probability-paradox':'Probability Paradox',
    'angle-ace':'Angle Ace','coordinate-geometry-dash':'Coordinate Geometry Dash',
    'graph-transformer':'Graph Transformer','formula-unlocked':'Formula Unlocked',
    'bearing-blitz':'Bearing Blitz','scale-factor-scaling':'Scale Factor Scaling',
    'unit-converter':'Unit Converter','formula-forge':'Formula Forge',
    'correlation-or-coincidence':'Correlation or Coincidence','chart-interrogator':'Chart Interrogator',
    'component-crusher':'Component Crusher','expectation-station':'Expectation Station',
    'better-value':'Better Value','core-maths-paper1':'Core Maths Paper 1',
    'core-maths-paper2a':'Core Maths Paper 2A','core-maths-paper2b':'Core Maths Paper 2B',
    'core-maths-paper2c':'Core Maths Paper 2C','tax-theft':'Tax Theft','stat-attack':'Stat Attack',
    'growth-and-decay':'Growth and Decay','graph-sketcher':'Graph Sketcher',
    'glorious-gantt':'Glorious Gantt','test-the-claim':'Test the Claim',
    'differentiation-duel':'Differentiation Duel','integration-duel':'Integration Duel',
    'suvat':'SUVAT Selector','curling-friction':'Curling Friction','force-resolver':'Force Resolver',
    'moments-master':'Moments Master','log-laws':'Log Laws','binomial-blaster':'Binomial Blaster',
    'partial-fractions-duel':'Partial Fractions Duel','proof-builder':'Proof Builder',
    'normal-navigator':'Normal Navigator','fermi-lab':'Fermi Lab','dimension-checker':'Dimension Checker',
    'regression-rumble':'Regression Rumble','factor-theorem':'Factor Theorem',
    'complex-converter':'Complex Converter','matrix-crunch':'Matrix Crunch',
    'characteristic-quest':'Characteristic Quest','eigenvalue-extractor':'Eigenvalue Extractor',
    'eigenvector-engine':'Eigenvector Engine','seven-bridges':'Seven Bridges',
    'higher-power':'Higher Power','given-that':'Given That','screening-room':'Screening Room',
    'prisoners-dilemma':"Prisoner's Dilemma",'boolean-blitz':'Boolean Blitz',
    'core-maths-paper1':'Core Maths Paper 1','core-maths-paper2a':'Core Maths Paper 2A',
    'core-maths-paper2b':'Core Maths Paper 2B','core-maths-paper2c':'Core Maths Paper 2C',
    'factor-theorem':'Factor Theorem','truth-will-set-you-free':'The Truth Will Set You Free',
    'six-sevens-bruv':'Six Sevens, Bruv','free-daily-pizza':'Free Daily Pizza'
  };

  // ── Naming a level: levelLabel() is the single source ──────────────────
  // Every level key any game submits, old and new, is named here or matched by
  // a pattern below. scripts/check-leaderboard-coverage.js loads this file and
  // FAILS on any submitted level levelLabel() cannot name, so a new key cannot
  // reach the ticker as raw text. 'all' is named '' on purpose: a game with no
  // levels shows no level.
  var LEVEL_NAMES = {
    'ks3':'KS3','gcse':'GCSE','alevel':'A-Level','alevel2':'A-Level Year 2',
    'further':'Further','level3':'Level 3 (Engineering)','level4':'Level 4','l4':'Level 4',
    'core':'Core Maths','year6':'Year 6','all':'',
    'q20':'20 questions','q40':'40 questions',
    'practice-q20':'Practice · 20','practice-q40':'Practice · 40',
    'higher':'GCSE Higher','formula':'Quadratic formula',
    // Simultaneous Solver: one board per Foundation stage (Jon, 6 Oct 2026).
    'foundation-s1':'Foundation · Stage 1','foundation-s2':'Foundation · Stage 2',
    'foundation-s3':'Foundation · Stage 3','foundation-s4':'Foundation · Stage 4',
    'foundation-s5':'Foundation · Stage 5'
  };

  // Keys that are not a fixed list. A pattern cannot be inverted, which is one
  // reason the legacy lookup below is frozen rather than extended.
  var MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var LEVEL_NAME_PATTERNS = [
    // Free Daily Pizza: one board per UK day (Jon, 30 Sep 2026).
    // Each namer returns the label, or null if the match is not a real key.
    [/^daily-(\d{4})-(\d{2})-(\d{2})$/, function(m) {
      var mon = MONTHS[parseInt(m[2], 10) - 1], day = parseInt(m[3], 10);
      return (mon && day >= 1 && day <= 31) ? 'Daily pizza ' + day + ' ' + mon : null;
    }],
    // Free Daily Pizza single-stage practice: score history and personal best only,
    // never a board (Jon, 30 Sep 2026). 'stage-s1-q20' -> 'Stage 1 · 20'.
    [/^stage-s(\d+)-q(\d+)$/, function(m) {
      return 'Stage ' + parseInt(m[1], 10) + ' · ' + parseInt(m[2], 10);
    }]
  ];

  // The display name for a level key, or null if nothing names it.
  function levelLabel(level) {
    if (LEVEL_NAMES.hasOwnProperty(level)) return LEVEL_NAMES[level];
    for (var i = 0; i < LEVEL_NAME_PATTERNS.length; i++) {
      var m = LEVEL_NAME_PATTERNS[i][0].exec(String(level));
      if (m) return LEVEL_NAME_PATTERNS[i][1](m);
    }
    return null;
  }

  // ── LEGACY, FROZEN: label → key, for old ticker entries only ───────────
  // Used only to read recent_scores entries written before `levelKey` existed
  // (28 Sep 2026), which carry the label and not the key. NEVER EXTEND IT, and
  // never build it from LEVEL_NAMES. It must keep answering exactly as it did
  // for the entries already stored: adding l4:'Level 4' would re-key every old
  // "Level 4" entry to 'l4', and a pattern cannot be inverted at all. The table
  // is as it stood when levelKey was added; its nine labels are distinct. A key
  // it did not name was stored as its own label, and levelKeyFromLabel()
  // returns such a label unchanged.
  var LEVEL_LABELS = {
    'ks3':'KS3','gcse':'GCSE','alevel':'A-Level','further':'Further',
    'level3':'Level 3 (Engineering)','level4':'Level 4','core':'Core Maths','year6':'Year 6','all':''
  };
  var LABEL_TO_LEVEL = {};
  (function() {
    for (var k in LEVEL_LABELS) {
      if (LEVEL_LABELS.hasOwnProperty(k)) LABEL_TO_LEVEL[LEVEL_LABELS[k]] = k;
    }
  })();

  // Legacy entries only (see above). An unmatched label was a raw key stored as
  // its own label, e.g. chart-interrogator's 'l4', so it is returned as-is.
  function levelKeyFromLabel(label) {
    if (LABEL_TO_LEVEL.hasOwnProperty(label)) return LABEL_TO_LEVEL[label];
    return label;
  }

  // Games whose leaderboard score is lower-is-better. Single copy — also
  // used by leaderboards/index.html (moved here 28 Sep 2026, was duplicated).
  var LOWER_IS_BETTER = { 'estimation-golf': true };

  // Games where the leaderboard node mixes incompatible scoring systems
  // under one key (pre-existing data issue, flagged to Jon, not fixed here).
  // Single copy — also used by leaderboards/index.html.
  var MIXED_UNRELIABLE = { 'higher-power': true };

  // Eligibility is completion, not a question count. Every game calls
  // submitScore() at its own natural end — pool exhausted, out of lives,
  // timer up, puzzle won or lost — so reaching the call IS the qualification.
  // A fixed "at least 10 questions" gate used to sit here and silently
  // rejected every run of any game whose unit is not ten-plus questions
  // (8-question Prime Sprint, 9-hole Estimation Golf, 6-guess Equatle,
  // 4-scenario Gantt ...): thirteen games could not rank at all, or not at
  // their default or shortest setting.

  // Every score that is not written says why, instead of vanishing.
  function reject(reason, gameSlug, level) {
    console.warn('MaffsLeaderboard: score not submitted — ' + reason +
      ' [game: ' + (GAME_NAMES[gameSlug] || gameSlug) + ', slug: ' + gameSlug +
      ', level: ' + level + ']');
    return { percentile: null, tier: null, totalPlayers: 0 };
  }

  // Certificate thresholds
  var GOLD_THRESHOLD = 0.05;   // top 5%
  var SILVER_THRESHOLD = 0.10; // top 10%

  // Initials rules live in MaffsInitials, defined at the top of this file.
  var isBlocked = window.MaffsInitials.isBlocked;
  var normaliseInitials = window.MaffsInitials.normaliseInitials;

  // Initialise Firebase (once only)
  var app = null;
  var db = null;

  function init() {
    if (app) return;
    if (typeof firebase === 'undefined' || !firebase.initializeApp) {
      console.warn('MaffsLeaderboard: Firebase SDK not loaded');
      return;
    }
    try {
      app = firebase.initializeApp(firebaseConfig);
      db = firebase.database();
    } catch (e) {
      if (e.code === 'app/duplicate-app') {
        app = firebase.app();
        db = firebase.database();
      } else {
        console.warn('MaffsLeaderboard: Firebase init failed', e);
      }
    }
  }

  /**
   * Show arcade-style initials overlay
   * Returns a Promise that resolves with the 3-letter string or '' if skipped
   */
  function askInitials(score) {
    return new Promise(function(resolve) {
      // Remove any existing overlay
      var existing = document.getElementById('mfg-initials-overlay');
      if (existing) existing.remove();

      var overlay = document.createElement('div');
      overlay.id = 'mfg-initials-overlay';
      overlay.innerHTML =
        '<div class="mfg-ini-box">' +
          '<div class="mfg-ini-title">ENTER YOUR INITIALS</div>' +
          '<div class="mfg-ini-score">Score: ' + score + '</div>' +
          '<div class="mfg-ini-inputs">' +
            '<input type="text" maxlength="1" class="mfg-ini-char" data-idx="0" autocomplete="off" autocapitalize="characters">' +
            '<input type="text" maxlength="1" class="mfg-ini-char" data-idx="1" autocomplete="off" autocapitalize="characters">' +
            '<input type="text" maxlength="1" class="mfg-ini-char" data-idx="2" autocomplete="off" autocapitalize="characters">' +
          '</div>' +
          '<div class="mfg-ini-error" style="display:none"></div>' +
          '<div class="mfg-ini-buttons">' +
            '<button class="mfg-ini-submit" disabled>Submit</button>' +
            '<button class="mfg-ini-skip">Skip</button>' +
          '</div>' +
        '</div>';

      // Inject styles if not already present
      if (!document.getElementById('mfg-ini-styles')) {
        var style = document.createElement('style');
        style.id = 'mfg-ini-styles';
        style.textContent =
          '#mfg-initials-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.7);' +
          'display:flex;align-items:center;justify-content:center;z-index:10000;font-family:"Outfit",system-ui,sans-serif}' +
          '.mfg-ini-box{background:#1a2744;border:2px solid #FFD700;border-radius:16px;padding:32px 40px;text-align:center;' +
          'box-shadow:0 0 40px rgba(255,215,0,0.2);max-width:340px;width:90%}' +
          '.mfg-ini-title{color:#FFD700;font-size:18px;font-weight:700;letter-spacing:2px;margin-bottom:8px}' +
          '.mfg-ini-score{color:rgba(255,255,255,0.6);font-size:14px;margin-bottom:24px}' +
          '.mfg-ini-inputs{display:flex;gap:12px;justify-content:center;margin-bottom:16px}' +
          '.mfg-ini-char{width:52px;height:60px;background:#0f1a2e;border:2px solid #FFD700;border-radius:8px;' +
          'color:#FFD700;font-size:28px;font-weight:700;text-align:center;text-transform:uppercase;' +
          'font-family:"JetBrains Mono","Outfit",monospace;outline:none;caret-color:#FFD700}' +
          '.mfg-ini-char:focus{border-color:#fff;box-shadow:0 0 12px rgba(255,215,0,0.4)}' +
          '.mfg-ini-error{color:#ef4444;font-size:12px;margin-bottom:12px}' +
          '.mfg-ini-buttons{display:flex;gap:12px;justify-content:center}' +
          '.mfg-ini-submit{background:#FFD700;color:#1a2744;border:none;border-radius:8px;padding:10px 24px;' +
          'font-size:14px;font-weight:700;cursor:pointer;font-family:inherit}' +
          '.mfg-ini-submit:disabled{opacity:0.3;cursor:default}' +
          '.mfg-ini-submit:not(:disabled):hover{background:#ffe44d}' +
          '.mfg-ini-skip{background:transparent;color:rgba(255,255,255,0.5);border:1px solid rgba(255,255,255,0.2);' +
          'border-radius:8px;padding:10px 24px;font-size:14px;cursor:pointer;font-family:inherit}' +
          '.mfg-ini-skip:hover{color:rgba(255,255,255,0.8);border-color:rgba(255,255,255,0.4)}';
        document.head.appendChild(style);
      }

      document.body.appendChild(overlay);

      // Keys typed into the overlay act on the overlay only (contract OVERLAY-KEYS, 9 Oct 2026). Games bind
      // shortcuts on document or window (all in the bubbling phase, none in capture), so a letter typed as
      // an initial also reached them: prisoners-dilemma restarted a finished game and lost the score.
      // 1. The overlay stops every key event that bubbles out of it, after its inputs' own handlers have run
      //    (Enter still submits, Backspace still steps back).
      // 2. While it is open, a capture-phase guard on window stops keys aimed anywhere else (focus left on
      //    the page by a tap on the backdrop), and it stays up through the keyup of a key held when the
      //    overlay closes, so the Enter that submits never reaches the game either.
      var KEY_EVENTS = ['keydown', 'keypress', 'keyup'];
      var held = 0, guardOn = true;
      function contain(e) { e.stopPropagation(); }
      function guard(e) {
        if (e.type === 'keydown' && !e.repeat) held++;
        if (e.type === 'keyup' && held > 0) held--;
        if (!overlay.isConnected || !overlay.contains(e.target)) e.stopPropagation();
        if (!overlay.isConnected && held === 0) unguard();
      }
      function unguard() {
        if (!guardOn) return;
        guardOn = false;
        KEY_EVENTS.forEach(function(t) { window.removeEventListener(t, guard, true); });
      }
      KEY_EVENTS.forEach(function(t) {
        overlay.addEventListener(t, contain);
        window.addEventListener(t, guard, true);
      });

      var inputs = overlay.querySelectorAll('.mfg-ini-char');
      var submitBtn = overlay.querySelector('.mfg-ini-submit');
      var skipBtn = overlay.querySelector('.mfg-ini-skip');
      var errorEl = overlay.querySelector('.mfg-ini-error');

      // Focus first input
      setTimeout(function() { inputs[0].focus(); }, 50);

      function getInitials() {
        return (inputs[0].value + inputs[1].value + inputs[2].value).toUpperCase();
      }

      function checkReady() {
        var ini = getInitials();
        submitBtn.disabled = ini.length < 3;
      }

      // Auto-advance on input, letters only
      for (var i = 0; i < inputs.length; i++) {
        (function(idx) {
          inputs[idx].addEventListener('input', function() {
            this.value = normaliseInitials(this.value).slice(0, 1);
            if (this.value && idx < 2) inputs[idx + 1].focus();
            checkReady();
            errorEl.style.display = 'none';
          });
          inputs[idx].addEventListener('keydown', function(e) {
            if (e.key === 'Backspace' && !this.value && idx > 0) {
              inputs[idx - 1].focus();
              inputs[idx - 1].value = '';
              checkReady();
            }
            if (e.key === 'Enter') {
              e.preventDefault();
              if (!submitBtn.disabled) submitBtn.click();
            }
          });
        })(i);
      }

      function cleanup() {
        overlay.remove();
        if (held === 0) unguard();
        else setTimeout(unguard, 1000);   // a held key's keyup normally ends the guard first
      }

      submitBtn.addEventListener('click', function() {
        var ini = getInitials();
        if (ini.length < 3) return;
        if (isBlocked(ini)) {
          errorEl.textContent = 'Those initials are not allowed.';
          errorEl.style.display = 'block';
          inputs[0].value = ''; inputs[1].value = ''; inputs[2].value = '';
          inputs[0].focus();
          submitBtn.disabled = true;
          return;
        }
        // Save for next time
        try { localStorage.setItem('mfg_initials', ini); } catch(e) {}
        cleanup();
        resolve(ini);
      });

      skipBtn.addEventListener('click', function() {
        cleanup();
        resolve('');
      });

      // Pre-fill from localStorage if available
      try {
        var saved = localStorage.getItem('mfg_initials');
        if (saved && saved.length === 3) {
          inputs[0].value = saved[0];
          inputs[1].value = saved[1];
          inputs[2].value = saved[2];
          checkReady();
        }
      } catch(e) {}
    });
  }

  /**
   * Submit a score to the leaderboard
   * Shows initials overlay, then submits to Firebase
   *
   * @param {string} gameSlug - e.g. 'differentiation-duel'
   * @param {string} level - e.g. 'gcse', 'alevel', 'year6'
   * @param {number} score - the score achieved
   * @param {number} questionsAnswered - accepted for existing callers; not used for eligibility
   * @returns {Promise<{percentile: number|null, tier: string|null, totalPlayers: number}>}
   */
  function submitScore(gameSlug, level, score, questionsAnswered) {
    init();
    if (!db) {
      return Promise.resolve(reject('Firebase SDK not loaded or failed to initialise', gameSlug, level));
    }

    var key = (gameSlug + '_' + level).replace(/-/g, '_');
    var ref = db.ref('leaderboards/' + key);

    var gameName = GAME_NAMES[gameSlug] || gameSlug;
    // levelLabel() names every key a game submits (the coverage check enforces
    // it); the raw key is only a last resort, never the normal path.
    var label = levelLabel(level);
    if (label === null) label = level;

    // Ask for initials first, then submit
    return askInitials(score).then(function(initials) {

      // ── Production only ──────────────────────────────────────────────
      // A game finished on a local server posted to the live leaderboard
      // and the front-page ticker; Skip still submits, just without
      // initials. Every write below (the leaderboard push and the
      // recent_scores push) is reached only through this point, so the
      // overlay still runs locally and nothing is written.
      var host = location.hostname;
      if (host !== 'maffsgames.co.uk' && host !== 'www.maffsgames.co.uk') {
        return reject('not the production host (' + host + ')', gameSlug, level);
      }

      // Stamped when the score is written, not when the initials overlay
      // opened: the database rules (firebase/database.rules.json) refuse a
      // timestamp more than 60 s from the server's clock, and a player can
      // sit on the overlay for longer than that.
      var now = Date.now();

      var leaderboardEntry = {
        score: score,
        timestamp: now
      };
      if (initials) leaderboardEntry.initials = initials;

      return ref.push(leaderboardEntry).then(function() {
        return ref.once('value');
      }).then(function(snapshot) {
        var data = snapshot.val();
        if (!data) return { percentile: null, tier: null, totalPlayers: 0 };

        var allScores = [];
        var keys = Object.keys(data);
        for (var i = 0; i < keys.length; i++) {
          if (data[keys[i]] && typeof data[keys[i]].score === 'number') {
            allScores.push(data[keys[i]].score);
          }
        }

        var percentile = calculatePercentile(score, allScores);
        var tier = getTier(percentile);

        // Push to recent_scores feed (fire-and-forget). highScore/weeklyBest/best
        // used to be computed here and frozen into the entry — removed 28 Sep 2026,
        // see docs/canon.md §9: the ticker now derives them live via standing().
        var recentRef = db.ref('recent_scores');
        var entry = {
          game: gameName,
          slug: gameSlug,
          level: label,
          levelKey: level,
          score: score,
          timestamp: now
        };
        if (initials) entry.initials = initials;
        // No client-side prune. It deleted the oldest entries beyond 50, which
        // needed the open delete permission the database rules now refuse. The
        // ticker reads only the latest 20 (orderByChild('timestamp').limitToLast(20),
        // served by the rules' .indexOn), so the feed's length does not matter to
        // it; docs/firebase-rules-deploy.md has the occasional manual prune.
        recentRef.push(entry).catch(function() {});

        return { percentile: percentile, tier: tier, totalPlayers: allScores.length };
      });

    }).catch(function(error) {
      return reject('write failed: ' + (error && error.message ? error.message : error), gameSlug, level);
    });
  }

  /**
   * Calculate what percentile a score is in
   * Returns 0.05 if score is better than 95% of scores (top 5%)
   */
  function calculatePercentile(score, allScores) {
    if (!allScores.length) return null;
    var scoresBelow = 0;
    for (var i = 0; i < allScores.length; i++) {
      if (allScores[i] < score) scoresBelow++;
    }
    return 1 - (scoresBelow / allScores.length);
  }

  /**
   * Determine certificate tier from percentile
   */
  function getTier(percentile) {
    if (percentile === null) return null;
    if (percentile <= GOLD_THRESHOLD) return 'gold';
    if (percentile <= SILVER_THRESHOLD) return 'silver';
    return null;
  }

  /**
   * Format percentile for display
   */
  function formatPercentile(percentile) {
    if (percentile === null) return null;
    var pct = Math.ceil(percentile * 100);
    return 'top ' + pct + '%';
  }

  /**
   * Live standing for a game+level, read from leaderboards/{slug}_{level}
   * at call time — never stored. This is the single place "best" and
   * "weekly best" are computed, so the portal ticker and the leaderboards
   * hub can't disagree, and neither can go stale the way recent_scores'
   * old highScore/weeklyBest/best flags did (frozen at submission time).
   * Cached per game+level for the page's lifetime.
   *
   * @param {string} gameSlug
   * @param {string} levelKey - e.g. 'gcse', 'alevel', 'year6'
   * @returns {Promise<{allTimeBest: number|null, weekBest: number|null, direction: 'higher'|'lower', rankable: boolean}>}
   */
  var standingCache = {};
  function standing(gameSlug, levelKey) {
    var direction = LOWER_IS_BETTER[gameSlug] ? 'lower' : 'higher';
    var rankable = !MIXED_UNRELIABLE[gameSlug];
    var cacheKey = gameSlug + '_' + levelKey;

    if (standingCache[cacheKey]) return standingCache[cacheKey];

    if (!rankable) {
      var held = Promise.resolve({ allTimeBest: null, weekBest: null, direction: direction, rankable: false });
      standingCache[cacheKey] = held;
      return held;
    }

    init();
    if (!db) {
      // Not cached — retry later once the SDK has loaded.
      return Promise.resolve({ allTimeBest: null, weekBest: null, direction: direction, rankable: true });
    }

    var key = (gameSlug + '_' + levelKey).replace(/-/g, '_');
    var promise = db.ref('leaderboards/' + key).once('value').then(function(snapshot) {
      var data = snapshot.val();
      var allTimeBest = null, weekBest = null;
      if (data) {
        var weekAgo = Date.now() - 604800000;
        var keys = Object.keys(data);
        for (var i = 0; i < keys.length; i++) {
          var e = data[keys[i]];
          if (!e || typeof e.score !== 'number') continue;
          if (allTimeBest === null || (direction === 'lower' ? e.score < allTimeBest : e.score > allTimeBest)) {
            allTimeBest = e.score;
          }
          if (e.timestamp >= weekAgo &&
              (weekBest === null || (direction === 'lower' ? e.score < weekBest : e.score > weekBest))) {
            weekBest = e.score;
          }
        }
      }
      return { allTimeBest: allTimeBest, weekBest: weekBest, direction: direction, rankable: true };
    }).catch(function() {
      return { allTimeBest: null, weekBest: null, direction: direction, rankable: true };
    });

    standingCache[cacheKey] = promise;
    return promise;
  }

  // Export
  /**
   * Read paths for pages (contract SCORES-OFFLINE, 9 Oct 2026). No page calls the SDK itself: on a network
   * that blocks it (common on college networks) these say so instead of throwing, so nothing else on the
   * page stops.
   *   available()            -> true when the database can be reached through the SDK
   *   readBoard(slug, level) -> Promise of the board's entries (an array; [] when it cannot be read)
   *   watchRecent(n, cb)     -> cb(scores, newest first) on every change to the n latest recent_scores;
   *                             returns false, and never calls cb, without the SDK
   */
  function available() {
    init();
    return !!db;
  }

  function readBoard(gameSlug, level) {
    init();
    if (!db) return Promise.resolve([]);
    var key = (gameSlug + '_' + level).replace(/-/g, '_');
    return db.ref('leaderboards/' + key).once('value').then(function(snap) {
      var data = snap.val() || {};
      return Object.keys(data).map(function(k) { return data[k]; })
        .filter(function(e) { return e && typeof e.score === 'number'; });
    }).catch(function() { return []; });
  }

  function watchRecent(n, cb) {
    init();
    if (!db) return false;
    db.ref('recent_scores').orderByChild('timestamp').limitToLast(n).on('value', function(snapshot) {
      var scores = [];
      snapshot.forEach(function(child) { scores.push(child.val()); });
      scores.reverse();
      cb(scores);
    });
    return true;
  }

  window.MaffsLeaderboard = {
    available: available,
    readBoard: readBoard,
    watchRecent: watchRecent,
    submitScore: submitScore,
    formatPercentile: formatPercentile,
    standing: standing,
    levelLabel: levelLabel,
    levelKeyFromLabel: levelKeyFromLabel,
    LOWER_IS_BETTER: LOWER_IS_BETTER,
    MIXED_UNRELIABLE: MIXED_UNRELIABLE,
    GOLD_THRESHOLD: GOLD_THRESHOLD,
    SILVER_THRESHOLD: SILVER_THRESHOLD
  };

})();
