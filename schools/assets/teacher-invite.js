/* The teacher feedback line (canon §4, shared components; contract 4 Oct 2026).

   One line of small text on a game's results screen, after its last control
   row, inviting a teacher who has used the game with a class to say how it
   went (Jon, 5 Oct 2026: the results screen is where a game ends in a lesson
   and where the teacher looks at how it went; only a game with no end keeps
   it on its start screen: constructions-lab, trig-wars). It links to the feedback
   form with the type set to "classroom" and the game already chosen, and opens
   in a new tab so a game in progress is never lost.

   Each game page loads this file and makes ONE call, pointing at an empty
   element placed where the line belongs:

       <p id="teacherInvite"></p>
       <script>MaffsInvite.mount(document.getElementById('teacherInvite'), 'slug');</script>

   A game whose results are BUILT by script (innerHTML), or which has more than
   one end state, keeps the mount point inside a hidden end container and, each
   time it shows an end state, moves the one line in after its controls:

       MaffsInvite.place(resultsEl);           // appended
       MaffsInvite.place(parentEl, beforeEl);  // or before a given child

   The line is moved, never copied, so a page always has exactly one.

   The slug is the game's directory name. A null slug links to the form with no
   game chosen (/leaderboards/). The line inherits the page's text colour and
   font; it adds no theme tokens and no opacity (at 0.75, four games' already
   muted text fell below 4.5:1 contrast). A page whose inherited
   colour does not read on its background sets an existing colour on the mount
   point (Estimation Golf, /leaderboards/). Placement rule (Jon, 4 Oct 2026):
   never between an answer input and its keypad, and visible without changing
   tabs.

   scripts/check-teacher-invite.py holds every game to the mount, its slug and
   the wording below. Nothing is recorded or sent. */
(function () {
  var TEXT = "Using this with a class? I'd love to hear how it went. — Jon";

  function style() {
    if (document.getElementById('teacherInviteStyle')) return;
    var s = document.createElement('style');
    s.id = 'teacherInviteStyle';
    s.textContent =
      '.teacher-invite a{color:inherit;font:inherit;text-decoration:underline;text-underline-offset:2px}';
    (document.head || document.documentElement).appendChild(s);
  }

  var mounted = null;

  function mount(target, slug) {
    if (!target) return null;
    mounted = target;
    style();
    var a = document.createElement('a');
    a.href = '/feedback/?type=classroom' + (slug ? '&game=' + encodeURIComponent(slug) : '');
    a.target = '_blank';
    a.rel = 'noopener';
    a.textContent = TEXT;
    target.classList.add('teacher-invite');
    // Inline, so a game's own rules for p (often by id) cannot resize or hide it.
    var st = target.style;
    st.display = 'block'; st.margin = '12px auto 0'; st.padding = '0'; st.maxWidth = '100%';
    st.fontSize = '0.8rem'; st.lineHeight = '1.4'; st.textAlign = 'center';
    target.textContent = '';
    target.appendChild(a);
    return target;
  }

  // Move the mounted line into an end container the game has just shown or
  // rebuilt. The element survives its old container's innerHTML being replaced.
  function place(parent, before) {
    if (!mounted || !parent) return null;
    parent.insertBefore(mounted, before || null);
    return mounted;
  }

  window.MaffsInvite = { mount: mount, place: place, TEXT: TEXT };
})();
