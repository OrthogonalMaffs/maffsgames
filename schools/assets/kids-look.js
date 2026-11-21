/* The child look's link fragment: one rule for every page that reads it (contract CLASS-PAGE, Jon 21 Nov 2026;
   canon §7.5.9).

   A game with a child look (Sums in Disguise, Some Thingies) opens in it from #kids, and greets a class from
   #kids/<Name>. The class page, /class/#<Name>, reads a bare name. The name lives only in the link: this file never
   stores it, sends it or writes it as HTML. Until CLASS-PAGE each game carried its own copy of the rule; now:

     MaffsKids.read(hash)               { kids, name } from a game's fragment: "#kids" or "#kids/<Name>" (any case for
                                        "kids") is the child look; name is the <Name> part when it passes the name rule,
                                        else null. Anything else is the grown-up look, name null. hash defaults to
                                        location.hash; pages pass their own, so each reads location.hash once.
     MaffsKids.read(hash, {bare: true}) { kids: false, name } from the class page's fragment, "#<Name>".
     MaffsKids.greeting(template, name) the template's {name} filled in; a name that already ends with "class" is not
                                        given a second "Class" ("Welcome, {name} Class!").
     MaffsKids.gameHash(name)           "#kids/<Name>" (encoded) for a valid name, else "#kids": a game link's fragment.
     MaffsKids.classHash(name)          "#<Name>" (encoded) for a valid name, else "": the class page's fragment.

   The name rule: decodeURIComponent, then trimmed; letters (any script), spaces, hyphens and apostrophes (' and ’)
   only, 1 to 20 characters, at least one letter. A fragment that does not decode gives no name.
   scripts/test-kids-look.py holds this file to the rule. No dependencies. */
(function () {
  'use strict';
  function valid(nm) {
    return typeof nm === 'string' && /^[\p{L}' ’-]{1,20}$/u.test(nm) && /\p{L}/u.test(nm);
  }
  function read(hash, opts) {
    var out = { kids: false, name: null };
    try {
      var frag = String((hash === undefined ? window.location.hash : hash) || '').replace(/^#/, '');
      if (opts && opts.bare) {
        if (frag) {
          var bare = decodeURIComponent(frag).trim();
          if (valid(bare)) out.name = bare;
        }
        return out;
      }
      var low = frag.toLowerCase();
      if (low === 'kids') out.kids = true;
      else if (low.indexOf('kids/') === 0) {
        out.kids = true;
        var nm = decodeURIComponent(frag.slice(5)).trim();
        if (valid(nm)) out.name = nm;
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
  function gameHash(name) { return valid(name) ? '#kids/' + encodeURIComponent(name) : '#kids'; }
  function classHash(name) { return valid(name) ? '#' + encodeURIComponent(name) : ''; }
  window.MaffsKids = { read: read, greeting: greeting, gameHash: gameHash, classHash: classHash };
})();
