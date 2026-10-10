/* Escape-room difficulty (contract ESCAPE-DIFFICULTY, 10 Oct 2026; Jon's scheme, 9 Oct 2026).

   Every lock carries `grade: N`, the GCSE grade (1-9) at which its skill is typically secure. A room's
   rating is its HARDEST lock's band:

     ★   Warm-up    grades 1-3
     ★★  Core       grades 4-5
     ★★★ Challenge  grades 6-9

   This file is the one place the bands live in the browser: engine.js (the start screen) and
   teacher.js (the teacher page) both call MaffsEscapeRating.rating(ROOM). The hub and front-page cards
   are static HTML, so scripts/check-escape-rooms.py derives the same rating from room.js (same bands)
   and fails if any card's data-stars disagrees or any lock has no grade. "Suits a top set" is for
   ★★★ teacher pages only, never a card or a student-facing screen. */
(function () {
  'use strict';
  var BANDS = [
    { stars: 1, name: 'Warm-up', grades: '1–3', top: 3 },
    { stars: 2, name: 'Core', grades: '4–5', top: 5 },
    { stars: 3, name: 'Challenge', grades: '6–9', top: 9 }
  ];

  // {stars, name, grades} for a room, or null when a lock has no grade (a room still in build).
  function rating(room) {
    var max = 0;
    for (var i = 0; i < room.locks.length; i++) {
      var g = room.locks[i].grade;
      if (typeof g !== 'number' || g < 1 || g > 9) return null;
      if (g > max) max = g;
    }
    for (var b = 0; b < BANDS.length; b++) {
      if (max <= BANDS[b].top) return { stars: BANDS[b].stars, name: BANDS[b].name, grades: BANDS[b].grades };
    }
    return null;
  }

  // The visible label with its text equivalent: the stars are hidden from screen readers, which read
  // "Difficulty: 2 of 3, Core, grades 4–5" instead. The star count, not colour, carries the rating.
  function html(r) {
    if (!r) return '';
    var stars = new Array(r.stars + 1).join('★');
    return '<span class="rating" data-stars="' + r.stars + '">' +
      '<span aria-hidden="true">' + stars + ' ' + r.name + ' &middot; grades ' + r.grades + '</span>' +
      '<span class="sr-only">Difficulty: ' + r.stars + ' of 3, ' + r.name + ', grades ' + r.grades + '</span>' +
      '</span>';
  }

  window.MaffsEscapeRating = { rating: rating, html: html, BANDS: BANDS };
})();
