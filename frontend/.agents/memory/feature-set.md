---
name: Feature set
description: All major storefront features implemented and key conventions used across the navar project.
---

# Implemented features

- **Auth** (`src/stores/auth.js`, `/auth`): localStorage-based users array + session. hashSimple() for password. No real backend.
- **Reviews** (`src/stores/reviews.js`): keyed by productId in localStorage. Default mock reviews exist for ethiopia/colombia/kenya. Star rating UI with hover state.
- **SEO** (`src/composables/useSeo.js`): watchEffect + DOM manipulation (no @vueuse/head). Accepts refs, computed, or plain values.
- **Search** (`src/components/SearchModal.vue`): Ctrl+K shortcut, searches products + posts, min 2 chars. Triggered from TheHeader.vue via `searchOpen` ref.
- **Payment** (`src/views/PaymentView.vue`): standalone page outside TheLayout, blue bank-style UI. Checkout redirects to /payment?amount=X&ref=Y. COD also goes to payment page (amount=0&cod=1).
- **Coupon** (`src/stores/coupons.js`, `/admin/coupons`): full Pinia store with type/minOrder/maxUses/expiry. CheckoutView reads from store.
- **Homepage groups** (HomeView): reads from useGroupsStore. Shows emoji icon based on g.type field. Links to /products.
- **Blog section on homepage** (HomeView): shows 3 most recent posts from `posts` in data.js before the manifesto section.
- **Theme system (split)**:
  - **Design Theme** (`src/stores/layout.js`, `layoutStore.themeName`): 5 named themes (minimal/modern/dark/earthy/glass). Applies CSS class to `<html>`. Changes component shapes/styles. Persisted in `navar_layout_v3`.
  - **Color Theme** (`src/stores/theme.js`, `themeStore.theme`): OKLCH sliders for accent + bg. Applies CSS custom properties. Persisted in `navar_theme_v1`.
  - **Per-page design** (`layoutStore.pageDesigns`): map of path → design theme key (null = use global). Applied in `router/index.js` afterEach hook via `applyDesignTheme()`.
  - **postMessage live preview**: admin sends `navar-design-preview` (design class) and `navar-theme-preview` (colors) to the iframe. Listeners in `layout.js` and `theme.js`.
- **Admin panel (reorganized)**:
  - Grouped sidebar with collapsible sections: محصولات, سفارش‌ها, محتوا, بازاریابی, تنظیمات.
  - `/admin/settings` redirects to `/admin/appearance`.
  - Unified `/admin/appearance` page with 4 tabs: تم طراحی, تم رنگی, کامپوننت‌ها, صفحات.
  - Sticky live preview iframe (desktop + mobile) on the right panel.

# Key conventions
- useSeo() must be called at top of setup (before async), it uses watchEffect internally.
- PaymentView has no TheLayout wrapper — it's intentionally a full-page bank UI.
- Auth store logout() is called directly from TheHeader; no navigation guard needed.
- THEMES is exported as alias for DESIGN_THEMES in layout.js for backward compatibility.
