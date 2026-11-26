/* The child look's link fragment: the one copy of its rule (contract CLASS-PAGE, Jon 21 Nov 2026; canon §7.5).

   A game with a child look reads its look from the link: "#kids" is the child look, and "#kids/<name>" is the child
   look greeting a class ("Welcome, <name> Class!"). Until CLASS-PAGE the rule was copied into each game (Sums in
   Disguise, Some Thingies); the class page (/class/) would have made a third copy, so it lives here, used by the games,
   the class page and site-nav.js's way back to the class page.

     MaffsKids.read(hash)             { kids, name }: "#kids" (any case) gives { kids: true, name: null }; "#kids/<name>"
                                      gives { kids: true, name } when the name keeps the rule below, else name null;
                                      anything else { kids: false, name: null }.
     MaffsKids.read(hash, 'bare')     the class page's own fragment: as above, and also "#<name>" alone is the class
                                      name (the documented example is #Example). An invalid name gives name null.
     MaffsKids.greeting(template, name)   the template with {name} filled in; a name that already ends with "class" is
                                      not given a second "Class" ("Example Class" -> "Welcome, Example Class!").
     MaffsKids.gameLink(name)         the fragment a game link carries: "#kids/<name>" (encoded), or "#kids" with no name.
     MaffsKids.classLink(name)        the fragment back to the class page: "#<name>" (encoded), or "" with no name.

   The name rule: decodeURIComponent, trimmed, 1 to 20 characters, only letters, spaces, hyphens and apostrophes (' and
   ’), at least one letter. A malformed escape gives no name.

   The caller passes its own location.hash, read once. The fragment and the name stay in the page: nothing here stores
   or sends anything (no storage, no network, no cookie), and the only global is MaffsKids. scripts/test-kids-look.py
   holds the rule and that promise. */
(function () {
  'use strict';
  var NAME = /^[\p{L}' ’-]{1,20}$/u, LETTER = /\p{L}/u;

  function nameOf(raw) {
    var nm = decodeURIComponent(raw).trim();   // a malformed escape throws: read()'s catch gives no name
    return NAME.test(nm) && LETTER.test(nm) ? nm : null;
  }

  function read(hash, mode) {
    var out = { kids: false, name: null };
    try {
      var frag = String(hash || '').replace(/^#/, '');
      var low = frag.toLowerCase();
      if (low === 'kids') out.kids = true;
      else if (low.indexOf('kids/') === 0) {
        out.kids = true;
        out.name = nameOf(frag.slice(5));
      } else if (mode === 'bare' && frag) {
        out.kids = true;
        out.name = nameOf(frag);
      }
    } catch (e) { out.name = null; }
    return out;
  }

  function greeting(template, name) {
    var g = String(template).replace('{name}', name);
    // A name that already ends with "class" is not given a second "Class".
    if (/class$/i.test(name)) g = g.replace(/(class)\s+class\b/i, '$1');
    return g;
  }

  function gameLink(name) { return name ? '#kids/' + encodeURIComponent(name) : '#kids'; }
  function classLink(name) { return name ? '#' + encodeURIComponent(name) : ''; }

  window.MaffsKids = Object.freeze({ read: read, greeting: greeting, gameLink: gameLink, classLink: classLink });
})();
