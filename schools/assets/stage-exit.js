/* MaffsStageExit: one shared way out of a game mid-play, back to the game's own start (STAGE-EXIT, 28 Oct 2026;
 * options CORE-PAPER-EXIT, 17 Nov 2026).
 *
 * The stage games hid their "← Games" link while a question was on screen (body.playing), so the only
 * ways out were ten questions or the browser's Back button. Include this file and stage-exit.css and
 * the page gets, with no other change:
 *   - on a question: a "← Stages" button and a "← Games" link at the two ends of the game's HUD row
 *     (no extra height: a phone's fold has only a few pixels spare);
 *   - on the worked example (no HUD): the same two controls in one header row.
 *
 * Needs from the page, with no options: the standard `a.back-link`, a `.hud` row inside `#game`, `.screen.active`
 * toggled by its show(), and the "All stages" button the results screen already has (#menuBtn, or #againBtn). The
 * button clicks that button, so leaving runs the page's own path to the picker: no new route to keep in step.
 * Leaving is not finishing: nothing here fires game_completed, submits to a board or records a score.
 * Any pending "Next →" control is cleared first, so its fallback timer cannot advance a stage that was left.
 *
 * Options, each an attribute on the script tag; leaving one out keeps the behaviour above:
 *   data-label="← Rounds"        the button's label (default "← Stages").
 *   data-home-label="..."        the home link's label (default "← Games"). build() sets the page's own back link to it
 *                                before the HUD copy is made, so the row and the HUD read the same. The full "← Back to
 *                                Games" wrapped at 320px in Aa mode and ran onto the next element (STAGE-EXIT-LABEL, Jon,
 *                                7 Nov 2026); games without this file keep it.
 *   data-game="#gameScreen"      the in-play screen (default "#game"): its `.hud`, if it has one, gets the two controls.
 *                                With no `.hud` inside it, the header row holds them instead, in the place the back link
 *                                already takes (no extra height): the button shows while that screen is `.active`, the
 *                                home link on every screen. The row sits outside that screen, so the shell gives it a
 *                                MaffsLock fresh window each time the screen becomes active (the page's own screen()
 *                                covers only its screen).
 *   data-leave="exitPaper"       the name of a global function that takes the page back to its own start (default: click
 *                                #menuBtn or #againBtn). It must record nothing.
 *   data-confirm="second-tap"    leaving takes two taps: the first turns the button into "Tap again to exit" for 3 s, a
 *                                second tap within those 3 s leaves, and otherwise the label comes back (Jon, 17 Nov 2026:
 *                                no pop-up dialog). Default: one tap leaves.
 */
(function () {
  'use strict';
  var script = document.currentScript;
  function opt(name) { return script && script.getAttribute(name); }
  var label = opt('data-label') || '← Stages';
  var homeLabel = opt('data-home-label') || '← Games';
  var gameSel = opt('data-game') || '#game';
  var leaveName = opt('data-leave');
  var secondTap = opt('data-confirm') === 'second-tap';
  var ARMED_LABEL = 'Tap again to exit';
  var ARMED_MS = 3000;
  var buttons = [];
  var armedTimer = null;

  function disarm() {
    if (armedTimer) { clearTimeout(armedTimer); armedTimer = null; }
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].textContent = label;
      buttons[i].classList.remove('stage-exit-armed');
    }
  }

  function leave() {
    disarm();
    if (window.MaffsNext) {
      var wraps = document.querySelectorAll('.maffs-next-wrap');
      for (var i = 0; i < wraps.length; i++) MaffsNext.clear(wraps[i].parentNode);
    }
    if (leaveName) {
      if (typeof window[leaveName] === 'function') window[leaveName]();
      return;
    }
    var go = document.getElementById('menuBtn') || document.getElementById('againBtn');
    if (go) go.click();
  }

  function tap(e) {
    if (!secondTap) { leave(); return; }
    var btn = e.currentTarget;
    if (armedTimer) { leave(); return; }
    btn.textContent = ARMED_LABEL;
    btn.classList.add('stage-exit-armed');
    armedTimer = setTimeout(disarm, ARMED_MS);   // the shell's own clock: no game timer may cancel the revert
  }

  function button(id) {
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'stage-exit-stages';
    btn.id = id;
    btn.textContent = label;
    if (secondTap) btn.setAttribute('aria-live', 'polite');   // the label change is read out
    btn.addEventListener('click', tap);
    buttons.push(btn);
    return btn;
  }

  function build() {
    var link = document.querySelector('a.back-link');
    if (!link || document.querySelector('.stage-exit-row')) return;
    link.textContent = homeLabel;
    var row = document.createElement('div');
    row.className = 'stage-exit-row';
    link.parentNode.insertBefore(row, link);
    row.appendChild(button('stageExitBtn'));
    row.appendChild(link);
    var game = document.querySelector(gameSel);
    var hud = game && game.querySelector('.hud');
    if (hud) {
      var home = document.createElement('a');
      home.className = 'stage-exit-home';
      home.href = link.getAttribute('href');
      home.textContent = link.textContent;
      hud.insertBefore(button('stageExitHudBtn'), hud.firstChild);
      hud.appendChild(home);
    } else if (game) {
      row.classList.add('stage-exit-inline');
      game.classList.add('stage-exit-play');
      // The button appears with that screen, but outside it: the page's MaffsLock.screen() covers its screen, never
      // this row. So when the screen becomes active the row gets the same fresh window (canon §7.6.0), and a
      // double-click's second click (Play again, Begin) cannot land on it. Leaving the screen by any route disarms.
      var wasActive = game.classList.contains('active');
      if (window.MutationObserver) {
        new MutationObserver(function () {
          var on = game.classList.contains('active');
          if (on && !wasActive && window.MaffsLock) MaffsLock.fresh(row);
          if (!on) disarm();
          wasActive = on;
        }).observe(game, { attributes: true, attributeFilter: ['class'] });
      }
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build);
  else build();
  window.MaffsStageExit = { leave: leave };
})();
