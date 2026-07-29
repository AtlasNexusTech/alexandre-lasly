import { animate, inView, scroll, stagger } from 'motion';

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const supportsHover = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

function markAnimated(elements) {
  elements.forEach((element) => element.classList.add('motion-animated'));
}

function animateHero() {
  const heroCopy = document.querySelector('.hero-grid > .reveal');
  const heroCard = document.querySelector('.hero-card');
  const copyItems = heroCopy
    ? [...heroCopy.querySelectorAll('.eyebrow, h1, .hero-lead, .actions')]
    : [];

  markAnimated(copyItems);
  if (copyItems.length) {
    animate(
      copyItems,
      { opacity: [0.55, 1], y: [22, 0] },
      {
        delay: stagger(0.085),
        duration: 0.72,
        ease: [0.22, 1, 0.36, 1],
      },
    );
  }

  if (heroCard) {
    heroCard.classList.add('motion-animated');
    animate(
      heroCard,
      { opacity: [0.68, 1], x: [30, 0], scale: [0.975, 1] },
      { type: 'spring', stiffness: 118, damping: 18, delay: 0.16 },
    );
  }
}

function animateReadingProgress() {
  const progress = document.createElement('div');
  progress.className = 'motion-progress';
  progress.setAttribute('aria-hidden', 'true');
  document.body.prepend(progress);

  const progressAnimation = animate(
    progress,
    { scaleX: [0, 1] },
    { ease: 'linear' },
  );
  scroll(progressAnimation);
}

function animateSections() {
  const revealItems = [...document.querySelectorAll('.reveal')]
    .filter((element) => !element.closest('.hero'));

  revealItems.forEach((element) => {
    inView(
      element,
      () => {
        if (element.dataset.motionEntered === 'true') return;
        element.dataset.motionEntered = 'true';
        element.classList.add('motion-animated');
        const isTimelineItem = element.classList.contains('timeline-item');
        animate(
          element,
          {
            opacity: [0.62, 1],
            x: isTimelineItem ? [-18, 0] : [0, 0],
            y: isTimelineItem ? [0, 0] : [24, 0],
          },
          { duration: 0.68, ease: [0.22, 1, 0.36, 1] },
        );
      },
      { amount: 0.14, margin: '0px 0px -7% 0px' },
    );
  });

  const metrics = document.querySelectorAll('.metric');
  if (metrics.length) {
    inView(
      '.metrics',
      () => {
        animate(
          metrics,
          { opacity: [0.7, 1], y: [16, 0] },
          { delay: stagger(0.07), duration: 0.55, ease: [0.22, 1, 0.36, 1] },
        );
      },
      { amount: 0.35 },
    );
  }
}

function addHoverMotion() {
  if (!supportsHover) return;

  const cards = document.querySelectorAll(
    '.expertise-card, .education-card, .interest, .hero-card',
  );
  cards.forEach((card) => {
    card.addEventListener('pointerenter', () => {
      animate(
        card,
        { y: -5, scale: 1.012 },
        { type: 'spring', stiffness: 320, damping: 24 },
      );
    });
    card.addEventListener('pointerleave', () => {
      animate(
        card,
        { y: 0, scale: 1 },
        { type: 'spring', stiffness: 300, damping: 25 },
      );
    });
  });

  document.querySelectorAll('.button').forEach((button) => {
    button.addEventListener('pointerenter', () => {
      animate(button, { scale: 1.018 }, { duration: 0.18 });
      const arrow = button.querySelector('.arrow');
      if (arrow) animate(arrow, { x: [0, 5, 0] }, { duration: 0.5 });
    });
    button.addEventListener('pointerleave', () => {
      animate(button, { scale: 1 }, { duration: 0.18 });
    });
  });

  const portrait = document.querySelector('.profile-portrait');
  const image = portrait?.querySelector('img');
  if (portrait && image) {
    portrait.addEventListener('pointermove', (event) => {
      const bounds = portrait.getBoundingClientRect();
      const x = ((event.clientX - bounds.left) / bounds.width - 0.5) * 7;
      const y = ((event.clientY - bounds.top) / bounds.height - 0.5) * 7;
      animate(image, { x, y, scale: 1.035 }, { duration: 0.3 });
    });
    portrait.addEventListener('pointerleave', () => {
      animate(
        image,
        { x: 0, y: 0, scale: 1 },
        { type: 'spring', stiffness: 220, damping: 24 },
      );
    });
  }
}

function initMotion() {
  if (reduceMotion) {
    document.documentElement.dataset.motion = 'reduced';
    return;
  }

  document.documentElement.dataset.motion = 'active';
  animateReadingProgress();
  animateHero();
  animateSections();
  addHoverMotion();
}

initMotion();
