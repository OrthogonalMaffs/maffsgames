/* MaffsStageExit: one shared way out of a stage game mid-play (STAGE-EXIT, 28 Oct 2026).
 *
 * The stage games hid "← Back to Games" while a question was on screen (body.playing), so the only
 * ways out were ten questions or the browser's Back button. Include this file and stage-exit.css and
 * the page gets, with no other change:
 *   - on a question: a "← Stages" button and a "← Back to Games" link at the two ends of the game's HUD row
 *     (no extra height: a phone's fold has only a few pixels spare);
 *   - on the worked example (no HUD): the same two controls in one header row.
 *
 * Needs from the page: the standard `a.back-link`, a `.hud` row inside `#game`, `.screen.active` toggled by its
 * show(), and the "All stages" button the results screen already has (#menuBtn, or #againBtn). The button clicks
 * that button, so leaving runs the page's own path to the picker: no new route to keep in step.
 * Leaving is not finishing: nothing here fires game_completed, submits to a board or records a score.
 * Any pending "Next →" control is cleared first, so its fallback timer cannot advance a stage that was left.
 *
 * Label: <script src="stage-exit.js" data-label="← Rounds"> (default "← Stages").
 */
(function () {
  'use strict';
  var script = document.currentScript;
  var label = (script && script.getAttribute('data-label')) || '← Stages';

  function leave() {
    if (window.MaffsNext) {
      var wraps = document.querySelectorAll('.maffs-next-wrap');
      for (var i = 0; i < wraps.length; i++) MaffsNext.clear(wraps[i].parentNode);
    }
    var go = document.getElementById('menuBtn') || document.getElementById('againBtn');
    if (go) go.click();
  }

  function button(id) {
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'stage-exit-stages';
    btn.id = id;
    btn.textContent = label;
    btn.addEventListener('click', leave);
    return btn;
  }

  function build() {
    var link = document.querySelector('a.back-link');
    if (!link || document.querySelector('.stage-exit-row')) return;
    var row = document.createElement('div');
    row.className = 'stage-exit-row';
    link.parentNode.insertBefore(row, link);
    row.appendChild(button('stageExitBtn'));
    row.appendChild(link);
    var hud = document.querySelector('#game .hud');
    if (hud) {
      var home = document.createElement('a');
      home.className = 'stage-exit-home';
      home.href = link.getAttribute('href');
      home.textContent = link.textContent;
      hud.insertBefore(button('stageExitHudBtn'), hud.firstChild);
      hud.appendChild(home);
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build);
  else build();
  window.MaffsStageExit = { leave: leave };
})();
