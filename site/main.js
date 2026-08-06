/* Fahad Hussain — portfolio behaviour.
   No dependencies. Everything degrades to a fully readable page
   with JS off: reveal styles are gated behind the .js class. */

(function () {
  'use strict';

  var root = document.documentElement;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');

  // Gate reveal styling on JS so content can never be stranded invisible.
  root.classList.add('js');

  /* ── Theme ─────────────────────────────────────────────── */
  var toggle = document.getElementById('theme-toggle');

  function apply(theme) {
    root.setAttribute('data-theme', theme);
    // Keeps native scrollbars and form controls in the right mode.
    root.style.colorScheme = theme;
    syncToggle();
  }

  function syncToggle() {
    var dark = root.getAttribute('data-theme') === 'dark';
    toggle.setAttribute('aria-pressed', String(dark));
    toggle.querySelector('.visually-hidden').textContent =
      dark ? 'Switch to light mode' : 'Switch to dark mode';
  }

  toggle.addEventListener('click', function () {
    var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    apply(next);
    try { localStorage.setItem('theme', next); } catch (e) {}
  });
  syncToggle();

  // Follow the OS only while the user has made no explicit choice.
  var scheme = window.matchMedia('(prefers-color-scheme: dark)');
  var onScheme = function (e) {
    var stored = null;
    try { stored = localStorage.getItem('theme'); } catch (err) {}
    if (stored) return;
    apply(e.matches ? 'dark' : 'light');
  };
  if (scheme.addEventListener) scheme.addEventListener('change', onScheme);
  else if (scheme.addListener) scheme.addListener(onScheme);

  /* ── Sticky bar hairline ───────────────────────────────── */
  var topbar = document.querySelector('.topbar');
  var ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      topbar.classList.toggle('topbar--stuck', window.scrollY > 8);
      ticking = false;
    });
  }, { passive: true });

  /* ── Scroll reveals ────────────────────────────────────── */
  var reveals = document.querySelectorAll('.reveal');

  if (reduced.matches || !('IntersectionObserver' in window)) {
    // Show everything immediately; no motion, no observer.
    for (var i = 0; i < reveals.length; i++) reveals[i].classList.add('is-in');
  } else {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        // Stagger only within a batch, and cap it so a long
        // batch never leaves the last item waiting.
        var delay = Math.min(entry.target.dataset.i * 60, 240);
        entry.target.style.transitionDelay = delay + 'ms';
        entry.target.classList.add('is-in');
        observer.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });

    Array.prototype.forEach.call(reveals, function (el, i) {
      el.dataset.i = i % 5;
      observer.observe(el);
    });
  }

  /* ── Hero readout count-up ─────────────────────────────── */
  /* The page's single orchestrated load moment: the stat rail
     settles into place the way an instrument panel would. */
  var nums = document.querySelectorAll('.num');

  if (!reduced.matches) {
    Array.prototype.forEach.call(nums, function (el, i) {
      var target = parseInt(el.dataset.count, 10);
      if (isNaN(target)) return;
      var start = null;
      var dur = 900;
      var delay = 260 + i * 90;

      el.textContent = '0';

      setTimeout(function () {
        requestAnimationFrame(function step(now) {
          if (start === null) start = now;
          var p = Math.min((now - start) / dur, 1);
          // easeOutExpo — fast settle, no bounce.
          var eased = p === 1 ? 1 : 1 - Math.pow(2, -10 * p);
          el.textContent = Math.round(eased * target);
          if (p < 1) requestAnimationFrame(step);
          else el.textContent = target;
        });
      }, delay);
    });
  }
})();
