# Print Lab Wraps — Site Architecture

Brand source: `Print_Lab_Wraps_Brand_Guidelines.pdf` (extracted, not invented).

## 0. Brand Tokens (extracted)

**Colors**
| Token | Hex | Role |
|---|---|---|
| `--color-red` | `#EE1E27` | Primary brand / CTA / accent |
| `--color-charcoal` | `#373737` | Secondary surfaces, muted text on white |
| `--color-white` | `#FFFFFF` | Base background, text on black |
| `--color-black` | `#000000` | Base background, text on white |

No additional colors exist in the guide — all states (hover, disabled, success/error) must be derived from these four via tint/shade/opacity, not invented hues. Suggested derived utilities (documented, not new brand colors): `red-hover` = `#C5181F` (darken 12%), `black-soft` = `#0D0D0D` (section separation on pure black), `white-muted` = `rgba(255,255,255,.7)` (body copy on black).

**Typography — Montserrat (single typeface, four weights)**
| Weight | Use |
|---|---|
| Black/ExtraBold (800–900) | H1, hero headline, section headlines |
| Bold/Semibold (600–700) | H2–H3, subheadings, card titles |
| Medium (500) | Nav links, buttons, labels, eyebrow text |
| Regular (400) | Body copy, paragraphs |

Brand logo lockup uses an italic/slanted custom mark with a star motif — this aggressive, motorsport-inspired angle is the brand's signature gesture. It should echo subtly in UI (slight skew on tags/badges, angled section dividers, diagonal image masks) without distorting body type, which must stay perfectly legible.

**Brand personality (derived from visual system):** bold, motorsport/industrial, high-contrast black-red-white, confident, no pastels, no gradients beyond subtle black fades — aligns directly with the brief's "industrial, premium, confident" mandate.

**Logo usage:** horizontal lockup provided in 6 variants (full-color on white/black/charcoal, plus reversed). Rule: maintain clear space ≥ height of the star icon on all sides; never place on busy photography without a solid or 60%+ black scrim behind it; never recolor the mark itself.

---

## 1. Page Hierarchy (sitemap)

```
/ (Home)
/services (hub)
  /services/commercial-vehicle-wraps
  /services/vehicle-wraps
  /services/signage-prints
  /services/buildings-facilities
  /services/other-offerings
/our-work                      (CMS portfolio list + filters)
  /our-work/[project-slug]     (CMS template — case study)
/about
/careers                       (CMS job list)
  /careers/[job-slug]          (CMS template — job detail)
/contact
/faq
/leave-a-review                (external link or embedded widget — footer target)
/terms-of-use
/privacy-policy
/404
```

Service subpages share one symmetric template (`template-service`) with CMS-swappable content blocks — not five hand-built pages. This is critical for maintenance and consistency.

---

## 2. CMS Architecture (Webflow Collections)

| Collection | Key Fields | Referenced By |
|---|---|---|
| **Services** | Name, Slug, Hero Headline, Hero Subheadline, Carousel Images (multi-ref → Project Images), Body Block 1 (image+rich text), Body Block 2 (image+rich text), Gallery Images (multi-ref), FAQ Category (ref), Meta Title, Meta Description, OG Image | Services hub, Homepage service cards, Nav, Footer |
| **Projects** | Name, Slug, Category (ref → Project Categories), Cover Image, Before Image, After Image, Gallery (multi-ref → Project Images), Vehicle/Client Type, Summary, Body (rich text), Featured (bool), Date | Our Work page, Homepage portfolio preview, Service pages (filtered gallery) |
| **Project Categories** | Name, Slug, Icon | Our Work filters, Service-to-category mapping |
| **Project Images** | Image, Alt Text, Project (ref) | Projects, Service galleries |
| **Services Offered** (sub-list per service, e.g. "Commercial Vehicles We Wrap") | Name, Icon, Service (ref) | Service page Block 3 three-column list |
| **FAQs** | Question, Answer (rich text), Category (ref), Order | FAQ page, FAQ Preview (home), Service page FAQ banner (filtered by category) |
| **Testimonials/Reviews** | Author, Company, Rating, Quote, Source (Google/Facebook/etc), Avatar, Date, Featured (bool) | Homepage trust section, Service pages, Our Work |
| **Job Openings** | Title, Slug, Department, Location, Type (FT/PT), Summary, Responsibilities (rich text), Requirements (rich text), Benefits (rich text), Apply Link/Form, Active (bool) | Careers list, Job detail template, related-jobs (filter by Department) |
| **Team Members** | Name, Role, Photo, Bio (short), Order | About page |

Static (non-CMS) content: Home, About, Contact, FAQ wrapper, Terms, Privacy, 404 — these reference CMS data but aren't items themselves.

---

## 3. Class Architecture (Client-First, Webflow)

**Global skeleton (every page):**
```
page-wrapper
  main-wrapper
    section-[name]                 e.g. section-hero, section-services-overview
      padding-global
        container-large | container-medium | container-small
          padding-section-large | -medium | -small
            [content: grid/flex layouts]
```

**Container scale**
- `container-large` — max-width 90rem (full-bleed galleries, hero)
- `container-medium` — max-width 75rem (default page content)
- `container-small` — max-width 48rem (forms, FAQ, body-copy-heavy blocks)

**Section padding scale (vertical rhythm, fluid)**
- `padding-section-large` → `clamp(5rem, 9vw, 9rem)`
- `padding-section-medium` → `clamp(3.5rem, 6vw, 6rem)`
- `padding-section-small` → `clamp(2rem, 4vw, 3.5rem)`

**Layout primitives**
- `grid-2-col`, `grid-3-col`, `grid-4-col` (+ `_tablet`, `_mobile` data-driven via Webflow breakpoints, not extra classes)
- `flex-horizontal`, `flex-vertical`, `flex-center`, `flex-space-between`
- Utility: `u-text-center`, `u-hide-mobile`, `u-hide-desktop`, `u-gap-row-small/medium/large`

**Typography classes (Montserrat scale, fluid via clamp)**
```
heading-style-h1   clamp(2.5rem, 5vw, 4.5rem)   weight 800/900
heading-style-h2   clamp(2rem, 3.5vw, 3rem)     weight 700
heading-style-h3   clamp(1.5rem, 2.5vw, 2rem)   weight 700
heading-style-h4   clamp(1.25rem, 2vw, 1.5rem)  weight 600
text-size-large    clamp(1.125rem, 1.5vw, 1.25rem) weight 400
text-size-regular  1rem                          weight 400
text-size-small    0.875rem                      weight 500 (eyebrow/labels)
text-style-nav     1rem weight 500
```

**Component classes (BEM-flavored Client-First, no combo bloat)**
```
button, button.is-secondary, button.is-on-dark
badge-tag (slight -3deg skew, echoes logo angle)
card-service, card-project, card-faq, card-testimonial, card-job
nav_component, nav_link, nav_dropdown
footer_component, footer_column
trust-bar_component, trust-bar_stat
process-step_component (the 4-step "We Make This Easy" block — built once, reused on Home + every service page)
gallery-marquee_component (infinite horizontal loop, Block 6 pattern)
carousel-3up_component (center-large / side-small rotating carousel, Block 1 pattern)
faq-accordion_component
cta-banner_component (image bg + centered content, reused for FAQ CTA + Final CTA)
```

Rule: one component class + at most one state modifier (`.is-active`, `.is-open`, `.is-on-dark`). No nested combo chains.

---

## 4. Component System (built once, reused everywhere)

1. **Sticky Header** — logo, nav links, Call button (tel: link, icon), Estimate button (primary, red), hamburger (mobile).
2. **Process Component** ("We Make This Easy") — 4-step, numbered, icon + label; used on Home Section 6 and every service page Block 5.
3. **Carousel-3up** — center-large/side-small infinite rotation (GSAP); used on Commercial Vehicle Wraps Block 1, reusable for any service hero needing it.
4. **Gallery Marquee** — 3-row infinite horizontal CMS-driven loop; reused across all service pages' galleries.
5. **CTA Banner** — bg image + centered heading/sub/button; reused for FAQ CTA and Final CTA, content swapped via instance.
6. **FAQ Accordion** — single source, used on FAQ page (full, searchable) and FAQ Preview (home, top 4–5 items, filtered).
7. **Card set** — service card, project card, testimonial card, job card — consistent padding/radius/hover treatment.
8. **Footer** — one global symbol across all pages.
9. **Trust Bar** — stat counters (years, projects, satisfaction %) — Home Section 4, reusable on About.
10. **Form component** — single styled form shell (input, label, error state, submit) reused for Estimate, Contact, Careers application — only fields differ.

---

## 5. Responsive Strategy

- Mobile-first builds; base styles target ~375px, scale up via breakpoints (478 / 768 / 992 / 1280 / 1440+).
- Fluid type/spacing via `clamp()` everywhere listed above — no fixed px breakpoints jumps for type.
- Containers in `%`/`rem`, never fixed px widths.
- Images: responsive `srcset`, native lazy-load, fixed aspect-ratio boxes to prevent layout shift.
- Touch targets ≥ 44×44px; header Call/Estimate buttons full-width stacked on mobile, inline on desktop.
- Carousel-3up and gallery-marquee degrade to single-column swipeable card list under 768px (no 3-up math on narrow viewports).
- Nav collapses to hamburger ≤ 991px; Call button stays visible in mobile header at all times (persistent conversion path).

---

## 6. SEO Strategy

- One `H1` per page (page name/primary keyword), strict H2→H6 nesting under it.
- Meta Title/Description fields on every static page + every CMS item (Service, Project, Job).
- Local SEO: NAP (Name/Address/Phone) schema (`LocalBusiness`) site-wide via footer + Contact page; service-specific pages add `Service` schema; Job pages add `JobPosting` schema; Our Work case studies can add `ImageObject`/`CreativeWork`.
- Open Graph + Twitter Card tags templated per page type, image falls back to brand default if CMS field empty.
- Keyword strategy: service pages target "[service] + [city/region]" long-tail; homepage targets primary category term; Our Work/case studies target vehicle-type + wrap-type combos for long-tail image/portfolio search.
- Internal linking: every service page links to related services, Our Work filtered by category, and the global Process + FAQ + CTA components — no orphan pages.
- All images: descriptive alt text (CMS field mandatory, not filename).
- Sitemap.xml + robots.txt at launch; canonical tags on all CMS templates.

---

## 7. Animation Strategy (restrained, premium)

Tools: GSAP (core), Lenis (smooth scroll), ScrollTrigger for reveals, Barba.js only if page-transition fidelity is worth the complexity (optional — default OFF unless requested).

- **Reveals:** fade-up 16–24px, 400–500ms, ease `power2.out`, staggered 60–80ms per item in a grid/list. Triggered once, no re-animate on scroll-back.
- **Hero:** subtle parallax on bg image/video (max 10–15% travel), headline fades in first, CTA buttons stagger in after.
- **Carousel-3up:** GSAP timeline-driven infinite rotation, eased, pause on hover/touch.
- **Gallery marquee:** CSS/GSAP continuous transform loop, three rows alternating direction, pause on hover.
- **Microinteractions:** button fill/scale-1.02 on hover (150–200ms), card lift (shadow + 4px translateY) on hover, accordion height auto-animate (250ms).
- **Respect `prefers-reduced-motion`:** disable parallax/marquee autoplay, keep only opacity fades.
- Explicitly avoid: page-load spinners/intros, scroll-jacking, animated counters that re-trigger, anything over 600ms.

---

## 8. Conversion Strategy

- **Persistent dual CTA** in header (Call — tel: link, one tap; Estimate — anchors to form/page) on every page, every breakpoint.
- Every section authored to answer: *Why trust you / why contact / why choose / why now* — explicit content checklist per section before copywriting (see Section design phase).
- **Above-the-fold conversion:** hero always carries both CTAs + a trust indicator line (years in business / projects completed / rating) — no scrolling required to act.
- **Social proof placement:** testimonials in homepage trust section + sprinkled on service pages near bottom-of-funnel CTAs (after gallery, before FAQ banner).
- **Portfolio as conversion tool:** Our Work preview on homepage links deep into filtered category — reduces friction for visitors who already know what they want wrapped.
- **FAQ as objection handling:** preview block + per-service filtered FAQ CTA banner removes hesitation right before the final ask.
- **Forms:** short by default (name/phone/email/service-needed), validated inline, spam-protected (honeypot + reCAPTCHA), success state confirms next step ("we'll call within X hours").
- **Exit-intent:** reserved only for Services/Our Work pages (desktop) offering the Estimate form — not used on mobile (no true hover/exit signal) and not stacked with anything else on screen.

---

*Next step: review/adjust this architecture, then move section-by-section starting with the Homepage Hero.*
