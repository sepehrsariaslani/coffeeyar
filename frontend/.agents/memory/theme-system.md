---
name: Theme system
description: Site-wide appearance customization architecture for نوار — deep themes, component variants, all managed from admin panel.
---

## Architecture

All customization state lives in `src/stores/layout.js` (Pinia), persisted to localStorage under key `navar_layout_v3`.

### Themes (9 options: minimal / bento / modern / dark / earthy / scandinavian / swiss / glass)
- Applied as a class on `<html>` element via `applyDesignTheme()`
- **minimal**: sharp 0px radius, no shadows, warm off-white, default
- **modern**: 12px card radius, 8px btn radius, blue accent, diagonal hero clip-path via CSS `.hero::after`, drop shadows
- **dark**: adds `dark` class, 2px radius, warm glow shadows
- **earthy**: 6px radius, organic wave on hero bottom via `.hero::after`
- **glass** (`theme-glass`): 18px radius, `body` gets gradient background-image, cards get `backdrop-filter: blur(20px)`, headers get frosted glass
- Deep UI tokens set per theme: `--ui-card-radius`, `--ui-btn-radius`, `--ui-card-shadow`, `--ui-glass-blur`
- Theme overrides in `src/styles.css` using `html.theme-* .card` selectors (required because cards use scoped CSS)

### Component variants (all in layoutStore, saved to localStorage)
- **heroVariant** (1–3): 1=overlay, 2=split, 3=diagonal — HeroSection.vue, used in HomeView.vue
- **footerVariant** (1–3): 1=classic 4-col, 2=centered minimal, 3=dark full — TheFooter.vue
- **cardVariant** (standard/compact/horizontal): ProductCard.vue reads from store (or overrideable via prop)

### Accent color (6 options)
- Applied as class `accent-*` on `<html>` via `applyAccentColor()`

### Header variant (4 options: 1–4)
- `layoutStore.headerVariant` consumed by TheHeader.vue

### Button style (3 options: sharp/rounded/pill)
- Applied as class `ui-rounded` or `ui-pill` on `<html>`

### Component theme inheritance
- `layoutStore.componentThemes` stores optional global theme overrides for layout, header, footer, hero, section header, featured grid, and product card.
- `pageComponentThemes` stores final per-page component overrides. Resolvers use page component → global component → page theme → global theme precedence.
- All design-aware resolvers use `layoutStore`, not `themeStore.themeClass`. The color store owns color tokens only and must not remove design classes.
- Resolver wrappers expose `data-design-theme` scopes so a modern/bento/scandinavian/swiss component can be styled independently on a page using another design.

## Entry points
- Admin: `/admin/appearance` → `AdminAppearance.vue` — full control including header/footer/hero/card variants
- Customer-facing: `src/components/site/ThemeSwitcher.vue` — palette icon in TheHeader.vue (all 4 variants); lets public users switch design theme, accent color, and button shape; persists via same layoutStore/localStorage

**Why:** Deep theme identity (shapes, blurs, shadows) requires per-component CSS overrides, not just color variables. Using `html.theme-X .component` selectors in global CSS to override scoped styles. Glass effect needs actual CSS `backdrop-filter` which can't be a CSS variable value.

**How to apply:** When adding a new themed component, add `html.theme-X .new-component { ... }` overrides in `src/styles.css` for each non-default theme.
