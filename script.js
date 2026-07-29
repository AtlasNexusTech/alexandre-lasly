document.documentElement.classList.add('js');

const themeButton = document.querySelector('[data-theme-toggle]');
const menuButton = document.querySelector('[data-menu-toggle]');
const navLinks = document.querySelector('[data-nav-links]');
const themeIcon = document.querySelector('[data-theme-icon]');

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  if (themeIcon) {
    themeIcon.innerHTML = theme === 'dark'
      ? '<circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.93 4.93l1.42 1.42M17.65 17.65l1.42 1.42M2 12h2M20 12h2M4.93 19.07l1.42-1.42M17.65 6.35l1.42-1.42"></path>'
      : '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79Z"></path>';
  }
  if (themeButton) {
    const labels = document.documentElement.lang === 'en'
      ? { dark: 'Use light theme', light: 'Use dark theme' }
      : { dark: 'Utiliser le thème clair', light: 'Utiliser le thème sombre' };
    themeButton.setAttribute('aria-label', labels[theme]);
    themeButton.title = labels[theme];
  }
}

const savedTheme = localStorage.getItem('alexandre-lasly-theme');
const preferredTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
applyTheme(savedTheme || preferredTheme);

themeButton?.addEventListener('click', () => {
  const nextTheme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  localStorage.setItem('alexandre-lasly-theme', nextTheme);
  applyTheme(nextTheme);
});

menuButton?.addEventListener('click', () => {
  const isOpen = navLinks.classList.toggle('is-open');
  menuButton.setAttribute('aria-expanded', String(isOpen));
});

navLinks?.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('is-open');
    menuButton?.setAttribute('aria-expanded', 'false');
  });
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && navLinks?.classList.contains('is-open')) {
    navLinks.classList.remove('is-open');
    menuButton?.setAttribute('aria-expanded', 'false');
    menuButton?.focus();
  }
});

const contactButton = document.querySelector('[data-contact-reveal]');
const contactPanel = document.querySelector('[data-contact-panel]');
const contactLabel = document.querySelector('[data-contact-label]');
const decodeContact = (points) => String.fromCodePoint(...points);

contactButton?.addEventListener('click', () => {
  const isVisible = contactPanel.classList.toggle('is-visible');
  contactButton.setAttribute('aria-expanded', String(isVisible));
  if (contactLabel) {
    const english = document.documentElement.lang === 'en';
    contactLabel.textContent = isVisible
      ? (english ? 'Hide my contact details' : 'Masquer mes coordonnées')
      : (english ? 'Reveal my contact details' : 'Afficher mes coordonnées');
  }
  if (!isVisible || contactPanel.childElementCount) return;

  const email = decodeContact([108,97,115,108,121,97,108,101,120,97,110,100,114,101,64,103,109,97,105,108,46,99,111,109]);
  const phone = decodeContact([43,51,51,55,53,48,53,48,52,53,57,53]);
  const english = document.documentElement.lang === 'en';
  const displayPhone = english
    ? `${phone.slice(0, 3)} ${phone.slice(3, 4)} ${phone.slice(4, 6)} ${phone.slice(6, 8)} ${phone.slice(8, 10)} ${phone.slice(10, 12)}`
    : `0${phone.slice(3, 4)} ${phone.slice(4, 6)} ${phone.slice(6, 8)} ${phone.slice(8, 10)} ${phone.slice(10, 12)}`;
  const entries = [
    [english ? 'Email' : 'E-mail', email, `mailto:${email}`],
    [english ? 'Phone' : 'Téléphone', displayPhone, `tel:${phone}`],
  ];
  entries.forEach(([label, value, href]) => {
    const row = document.createElement('div');
    row.className = 'contact-line';
    const caption = document.createElement('span');
    caption.textContent = label;
    const link = document.createElement('a');
    link.textContent = value;
    link.href = href;
    row.append(caption, link);
    contactPanel.append(row);
  });
});

const revealItems = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add('is-visible'));
}
