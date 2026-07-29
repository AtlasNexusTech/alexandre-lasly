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

function pulseWhileVisible(element, keyframes, options, restingState) {
  inView(
    element,
    () => {
      const controls = animate(element, keyframes, options);
      return () => {
        controls.stop();
        animate(element, restingState, { duration: 0.12 });
      };
    },
    { amount: 0.2 },
  );
}

function animateGradientText() {
  document.querySelectorAll('.animated-gradient-text').forEach((element, index) => {
    inView(
      element,
      () => {
        const controls = animate(
          element,
          { backgroundPosition: ['0% 50%', '100% 50%', '0% 50%'] },
          {
            duration: 7.2,
            repeat: Infinity,
            delay: index * 0.35,
            ease: 'linear',
          },
        );
        return () => {
          controls.stop();
          animate(element, { backgroundPosition: '0% 50%' }, { duration: 0.15 });
        };
      },
      { amount: 0.25 },
    );
  });
}

function addPulseMotion() {
  const statusDot = document.querySelector('.status-dot');
  if (statusDot) {
    pulseWhileVisible(
      statusDot,
      {
        scale: [1, 1.14, 1],
        boxShadow: [
          '0 0 0 4px rgba(21, 190, 83, 0.18)',
          '0 0 0 10px rgba(21, 190, 83, 0)',
          '0 0 0 4px rgba(21, 190, 83, 0.18)',
        ],
      },
      { duration: 2.2, repeat: Infinity, ease: 'easeOut' },
      { scale: 1, boxShadow: '0 0 0 5px rgba(21, 190, 83, 0.14)' },
    );
  }

  document.querySelectorAll('.button').forEach((button, index) => {
    const ring = document.createElement('span');
    ring.className = 'button-pulse-ring';
    ring.setAttribute('aria-hidden', 'true');
    button.prepend(ring);
    pulseWhileVisible(
      ring,
      { opacity: [0, 0.52, 0], scale: [1, 1.025, 1.13] },
      {
        duration: 2.5,
        repeat: Infinity,
        repeatDelay: 0.25,
        delay: index * 0.22,
        ease: [0.22, 1, 0.36, 1],
      },
      { opacity: 0, scale: 1 },
    );
  });

  document.querySelectorAll('.timeline-dot').forEach((dot, index) => {
    pulseWhileVisible(
      dot,
      {
        scale: [1, 1.18, 1],
        boxShadow: [
          '0 0 0 1px rgba(83, 58, 253, 0.38)',
          '0 0 0 9px rgba(83, 58, 253, 0)',
          '0 0 0 1px rgba(83, 58, 253, 0.38)',
        ],
      },
      {
        duration: 2.15,
        repeat: Infinity,
        repeatDelay: 0.35,
        delay: index * 0.17,
        ease: 'easeOut',
      },
      { scale: 1, boxShadow: '0 0 0 1px rgba(83, 58, 253, 0.38)' },
    );
  });
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
  animateGradientText();
  addPulseMotion();
  addHoverMotion();
}

initMotion();
