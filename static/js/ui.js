// ---------- Tema (toggle com sol/lua) ----------
function applyThemeFromStorageOrSystem() {
  const saved = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isDark = saved ? saved === 'dark' : prefersDark;
  document.documentElement.classList.toggle('dark', isDark);
  updateThemeToggleUI(isDark);
  return isDark;
}

function updateThemeToggleUI(isDark) {
  const toggle = document.getElementById('themeToggle');
  const knob = document.getElementById('themeKnob');
  const sun = document.getElementById('iconSun');
  const moon = document.getElementById('iconMoon');
  if (!toggle || !knob || !sun || !moon) return;

  toggle.setAttribute('aria-checked', String(isDark));

  // move o knob (dark -> direita)
  knob.style.transform = isDark ? 'translateX(24px)' : 'translateX(0)';

  // opacidade dos ícones
  sun.style.opacity = isDark ? '0.4' : '1';
  moon.style.opacity = isDark ? '1' : '0.4';
}

document.addEventListener('DOMContentLoaded', () => {
  // aplica tema inicial e estado visual do toggle
  let isDark = applyThemeFromStorageOrSystem();

  // clique no toggle
  const btn = document.getElementById('themeToggle');
  if (btn) {
    btn.addEventListener('click', () => {
      isDark = !document.documentElement.classList.contains('dark'); // vai alternar
      document.documentElement.classList.toggle('dark');
      localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
      updateThemeToggleUI(document.documentElement.classList.contains('dark'));
    });
  }

  // ---------- Autofocus fallback ----------
  const auto = document.querySelector('[data-autofocus]');
  if (auto && document.activeElement !== auto) {
    auto.focus({ preventScroll: true });
    if (typeof auto.select === 'function') auto.select();
  }

  // ---------- Renderizar toasts das mensagens flash ----------
  (function renderFlashed() {
    const holder = document.getElementById('flashed-messages');
    holder?.querySelectorAll('div[data-message]').forEach((n) => {
      showToast(n.dataset.message || '', n.dataset.category || 'info');
    });
  })();
});

// ---------- Toast helper ----------
function showToast(msg, type = 'info') {
  const wrap = ensureToastWrap();
  const colors =
    {
      success: { bg: 'bg-emerald-50 dark:bg-emerald-900/30', text: 'text-emerald-800 dark:text-emerald-200', brd: 'border-emerald-200 dark:border-emerald-700' },
      danger:  { bg: 'bg-rose-50 dark:bg-rose-900/30',       text: 'text-rose-800 dark:text-rose-200',       brd: 'border-rose-200 dark:border-rose-700' },
      warning: { bg: 'bg-amber-50 dark:bg-amber-900/30',     text: 'text-amber-800 dark:text-amber-200',     brd: 'border-amber-200 dark:border-amber-700' },
      info:    { bg: 'bg-sky-50 dark:bg-sky-900/30',         text: 'text-sky-800 dark:text-sky-200',         brd: 'border-sky-200 dark:border-sky-700' },
    }[type] || { bg: 'bg-slate-50 dark:bg-slate-800', text: 'text-slate-800 dark:text-slate-100', brd: 'border-slate-200 dark:border-slate-700' };

  const el = document.createElement('div');
  el.className = `toast ${colors.bg} ${colors.text} ${colors.brd}`;
  el.setAttribute('role', 'status');
  el.setAttribute('aria-live', 'polite');

  const span = document.createElement('span');
  span.className = 'text-sm';
  span.textContent = msg;
  el.appendChild(span);

  const wrapLimit = 4;
  while (wrap.children.length >= wrapLimit) wrap.firstChild?.remove();

  wrap.appendChild(el);

  setTimeout(() => {
    el.style.transition = 'opacity .2s ease';
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 220);
  }, 3500);
}

function ensureToastWrap() {
  let wrap = document.getElementById('toastWrap');
  if (!wrap) {
    wrap = document.createElement('div');
    wrap.id = 'toastWrap';
    wrap.className = 'toast-wrap';
    document.body.appendChild(wrap);
  }
  return wrap;
}
