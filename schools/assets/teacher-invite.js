/* The teacher feedback line (canon §4, shared components; contract 4 Oct 2026).

   One line of small text under a game's Start control, inviting a teacher who
   has used the game with a class to say how it went. It links to the feedback
   form with the type set to "classroom" and the game already chosen, and opens
   in a new tab so a game in progress is never lost.

   Each game page loads this file and makes ONE call, pointing at an empty
   element placed where the line belongs:

       <p id="teacherInvite"></p>
       <script>MaffsInvite.mount(document.getElementById('teacherInvite'), 'slug');</script>

   The slug is the game's directory name. A null slug links to the form with no
   game chosen (/leaderboards/). The line inherits the page's text colour and
   font; it adds no theme tokens and no opacity (at 0.75, four games' already
   muted start-screen text fell below 4.5:1 contrast). A page whose inherited
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

  function mount(target, slug) {
    if (!target) return null;
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

  window.MaffsInvite = { mount: mount, TEXT: TEXT };
})();
