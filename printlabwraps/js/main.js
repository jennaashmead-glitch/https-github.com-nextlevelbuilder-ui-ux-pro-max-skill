/* ============================================================
   PRINT LAB WRAPS — Main JS
   Smooth scroll, reveal animations, accordion, carousel,
   mobile menu, sticky header, before/after slider
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ── Sticky Header ── */
  const header = document.querySelector('.site-header');
  if (header) {
    const onScroll = () => {
      header.classList.toggle('scrolled', window.scrollY > 20);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ── Mobile Menu ── */
  const hamburger = document.querySelector('.hamburger');
  const mobileMenu = document.querySelector('.mobile-menu');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      const open = hamburger.classList.toggle('open');
      mobileMenu.classList.toggle('open', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
    mobileMenu.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        hamburger.classList.remove('open');
        mobileMenu.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }

  /* ── Intersection Observer Reveal ── */
  const revealEls = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');
  if (revealEls.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e, i) => {
        if (e.isIntersecting) {
          const delay = e.target.dataset.delay || i * 80;
          setTimeout(() => e.target.classList.add('visible'), Number(delay));
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach(el => io.observe(el));
  }

  /* ── Stagger children ── */
  document.querySelectorAll('[data-stagger]').forEach(parent => {
    const children = parent.children;
    Array.from(children).forEach((child, i) => {
      child.classList.add('reveal');
      child.dataset.delay = i * 100;
    });
  });

  /* ── Accordion ── */
  document.querySelectorAll('.accordion-trigger').forEach(trigger => {
    trigger.addEventListener('click', () => {
      const item = trigger.closest('.accordion-item');
      const isOpen = item.classList.contains('open');
      // close all in same group
      const group = item.closest('[data-accordion]');
      if (group) {
        group.querySelectorAll('.accordion-item.open').forEach(el => el.classList.remove('open'));
      }
      if (!isOpen) item.classList.add('open');
    });
  });

  /* ── FAQ Search ── */
  const faqSearch = document.getElementById('faq-search');
  if (faqSearch) {
    faqSearch.addEventListener('input', () => {
      const q = faqSearch.value.toLowerCase();
      document.querySelectorAll('.accordion-item').forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(q) ? '' : 'none';
      });
    });
  }

  /* ── Portfolio Filter ── */
  const filterBtns = document.querySelectorAll('.filter-btn');
  const portfolioItems = document.querySelectorAll('[data-category]');
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const cat = btn.dataset.filter;
      portfolioItems.forEach(item => {
        if (cat === 'all' || item.dataset.category === cat) {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
      });
    });
  });

  /* ── Simple Carousel ── */
  const carousels = document.querySelectorAll('.vehicle-carousel');
  carousels.forEach(carousel => {
    const slides = carousel.querySelectorAll('.carousel-slide');
    const dots   = carousel.querySelectorAll('.dot');
    let current  = Math.floor(slides.length / 2);

    const go = (idx) => {
      slides.forEach((s, i) => s.classList.toggle('active', i === idx));
      dots.forEach((d, i) => d.classList.toggle('active', i === idx));
      current = idx;
    };

    carousel.querySelector('.carousel-prev')?.addEventListener('click', () => {
      go((current - 1 + slides.length) % slides.length);
    });
    carousel.querySelector('.carousel-next')?.addEventListener('click', () => {
      go((current + 1) % slides.length);
    });
    dots.forEach((d, i) => d.addEventListener('click', () => go(i)));
    go(current);

    // Auto-rotate
    let timer = setInterval(() => go((current + 1) % slides.length), 4000);
    carousel.addEventListener('mouseenter', () => clearInterval(timer));
    carousel.addEventListener('mouseleave', () => {
      timer = setInterval(() => go((current + 1) % slides.length), 4000);
    });
  });

  /* ── Before/After Slider ── */
  document.querySelectorAll('.ba-wrapper').forEach(wrapper => {
    const handle = wrapper.querySelector('.ba-handle');
    const after  = wrapper.querySelector('.ba-after');
    if (!handle || !after) return;

    let dragging = false;
    const move = (x) => {
      const rect  = wrapper.getBoundingClientRect();
      const pct   = Math.min(Math.max((x - rect.left) / rect.width * 100, 0), 100);
      handle.style.left = pct + '%';
      after.style.clipPath = `inset(0 ${100 - pct}% 0 0)`;
    };

    handle.addEventListener('mousedown',  () => dragging = true);
    handle.addEventListener('touchstart', () => dragging = true, { passive: true });
    window.addEventListener('mouseup',    () => dragging = false);
    window.addEventListener('touchend',   () => dragging = false);
    window.addEventListener('mousemove',  e => { if (dragging) move(e.clientX); });
    window.addEventListener('touchmove',  e => { if (dragging) move(e.touches[0].clientX); }, { passive: true });
  });

  /* ── Counter Animation ── */
  const counters = document.querySelectorAll('[data-count]');
  if (counters.length) {
    const countIO = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        const el = e.target;
        const target = parseInt(el.dataset.count);
        const suffix = el.dataset.suffix || '';
        const dur = 2000;
        const step = target / (dur / 16);
        let current = 0;
        const tick = () => {
          current = Math.min(current + step, target);
          el.textContent = Math.floor(current).toLocaleString() + suffix;
          if (current < target) requestAnimationFrame(tick);
        };
        tick();
        countIO.unobserve(el);
      });
    }, { threshold: 0.5 });
    counters.forEach(c => countIO.observe(c));
  }

  /* ── Active nav link ── */
  const page = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link, .mobile-nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && page.includes(href.replace('../pages/', '').replace('.html', ''))) {
      link.classList.add('active');
    }
  });

  /* ── Smooth scroll for anchors ── */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* ── Phone click tracking ── */
  document.querySelectorAll('a[href^="tel:"]').forEach(a => {
    a.addEventListener('click', () => {
      if (typeof gtag === 'function') gtag('event', 'phone_click', { event_category: 'conversion' });
    });
  });

});
