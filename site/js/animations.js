// sticky header: hidden over the hero's own in-card nav, slides in once scrolled past it
const stickyHeader = document.querySelector('[data-sticky-header]');
const heroNav = document.querySelector('.hero_nav');

if (stickyHeader && heroNav) {
  const toggleSticky = () => {
    const heroNavBottom = heroNav.getBoundingClientRect().bottom;
    stickyHeader.classList.toggle('is-visible', heroNavBottom < 0);
  };

  toggleSticky();
  window.addEventListener('scroll', toggleSticky, { passive: true });
}

if (typeof gsap !== 'undefined') {
  gsap.registerPlugin(ScrollTrigger);

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.querySelectorAll('[data-reveal]').forEach((el, i) => {
    if (reduceMotion) return;

    gsap.set(el, { opacity: 0, y: 20 });

    gsap.to(el, {
      opacity: 1,
      y: 0,
      duration: 0.5,
      ease: 'power2.out',
      delay: i * 0.08,
      scrollTrigger: {
        trigger: el,
        start: 'top 85%',
        once: true,
      },
    });
  });
}
