/* MaffsProgress — device-local named progress, keyed by 3-letter initials.
 *
 * WHY THIS EXISTS
 * ---------------
 * The resit fluency strand (times tables first, then FDP, fractions, number bonds,
 * standard form) keeps a student's progress between visits: a grid that fills in as
 * facts are earned. Several students share one classroom machine, so progress is
 * named, by the same 3-letter initials the leaderboard uses. Built once here, so the
 * next resit game imports it rather than hand-rolling its own copy (Six Sevens, Bruv
 * contract, 30 Sep 2026).
 *
 * WHAT IT GUARANTEES
 * ------------------
 *   - Nothing leaves the device. localStorage only; no server call of any kind.
 *   - Initials are validated by MaffsInitials (schools/assets/firebase-leaderboard.js,
 *     defined at the top of that file with no dependency on the Firebase SDK), so a
 *     grid name obeys exactly the rules and the blocked list the leaderboard obeys.
 *     This module never references Firebase and works when the SDK fails to load.
 *     If MaffsInitials itself is missing, validate() refuses every name (fail closed).
 *   - Every storage read and write is wrapped in try/catch. A browser that blocks or
 *     wipes storage makes available() false and save() return false; the game must
 *     then run session-only and must never claim the grid will be kept.
 *
 * STORAGE
 * -------
 *   key:   mfg_progress_v1::<slug>::<INITIALS>
 *   value: {"v":1,"updated":<ms>,"summary":{...},"data":{...}}
 *   `data` is the game's own state; `summary` is what the start screen lists
 *   (e.g. {gold: 34}). The module never interprets either.
 *
 * USAGE
 * -----
 *   <script src="../../schools/assets/firebase-leaderboard.js"></script>  (MaffsInitials)
 *   <script src="../../schools/assets/progress.js"></script>
 *
 *   MaffsProgress.available()                      -> bool
 *   MaffsProgress.validate(raw)                    -> {ok, initials, reason}
 *   MaffsProgress.list(slug)                       -> [{initials, updated, summary}], newest first
 *   MaffsProgress.load(slug, initials)             -> data object, or null
 *   MaffsProgress.save(slug, initials, data, summary) -> bool (false = not kept)
 *   MaffsProgress.remove(slug, initials)           -> bool
 */
(function () {
  'use strict';

  var PREFIX = 'mfg_progress_v1::';
  var PROBE = 'mfg_progress_v1_probe';

  function key(slug, initials) {
    return PREFIX + slug + '::' + initials;
  }

  function store() {
    try { return window.localStorage || null; } catch (e) { return null; }
  }

  function available() {
    var s = store();
    if (!s) return false;
    try {
      s.setItem(PROBE, '1');
      var ok = s.getItem(PROBE) === '1';
      s.removeItem(PROBE);
      return ok;
    } catch (e) {
      return false;
    }
  }

  function validate(raw) {
    var MI = window.MaffsInitials;
    if (!MI || typeof MI.normaliseInitials !== 'function' || typeof MI.isBlocked !== 'function') {
      return { ok: false, initials: '', reason: 'Names cannot be checked on this page, so none can be saved.' };
    }
    var ini = MI.normaliseInitials(raw);
    if (ini.length !== 3) {
      return { ok: false, initials: ini, reason: 'Use exactly three letters.' };
    }
    if (MI.isBlocked(ini)) {
      return { ok: false, initials: ini, reason: 'Those initials are not allowed.' };
    }
    return { ok: true, initials: ini, reason: '' };
  }

  function list(slug) {
    var s = store();
    var out = [];
    if (!s) return out;
    var pre = PREFIX + slug + '::';
    try {
      for (var i = 0; i < s.length; i++) {
        var k = s.key(i);
        if (!k || k.indexOf(pre) !== 0) continue;
        var ini = k.slice(pre.length);
        var rec = null;
        try { rec = JSON.parse(s.getItem(k)); } catch (e) { rec = null; }
        if (!rec || rec.v !== 1 || !validate(ini).ok) continue;
        out.push({ initials: ini, updated: rec.updated || 0, summary: rec.summary || {} });
      }
    } catch (e) {
      return [];
    }
    out.sort(function (a, b) { return b.updated - a.updated; });
    return out;
  }

  function load(slug, initials) {
    var s = store();
    if (!s || !validate(initials).ok) return null;
    try {
      var rec = JSON.parse(s.getItem(key(slug, initials)));
      if (!rec || rec.v !== 1 || typeof rec.data !== 'object' || rec.data === null) return null;
      return rec.data;
    } catch (e) {
      return null;
    }
  }

  function save(slug, initials, data, summary) {
    var s = store();
    if (!s || !validate(initials).ok) return false;
    try {
      var k = key(slug, initials);
      s.setItem(k, JSON.stringify({ v: 1, updated: Date.now(), summary: summary || {}, data: data }));
      // A write can "succeed" and still not be kept (some private modes); read it back.
      return s.getItem(k) !== null;
    } catch (e) {
      return false;
    }
  }

  function remove(slug, initials) {
    var s = store();
    if (!s) return false;
    try {
      s.removeItem(key(slug, initials));
      return s.getItem(key(slug, initials)) === null;
    } catch (e) {
      return false;
    }
  }

  window.MaffsProgress = {
    available: available,
    validate: validate,
    list: list,
    load: load,
    save: save,
    remove: remove,
    PREFIX: PREFIX
  };
})();
