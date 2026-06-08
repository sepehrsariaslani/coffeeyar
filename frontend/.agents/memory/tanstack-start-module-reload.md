---
name: TanStack Start module reload on dev server restart
description: After dev server restarts (e.g. file change), browser gets stale SSR HTML with old module URLs; React bundle fails to load and ALL buttons become non-interactive.
---

## The Rule
After any code change that causes the Vite dev server to restart, the browser preview may have stale HTML pointing to old module URLs. React's client bundle fails to fetch, hydration never happens, and all interactive elements (buttons, links) stop responding — even though the page looks visually normal.

**Why:** TanStack Start uses virtual Vite entry modules (`virtual:tanstack-start-client-entry`). On server restart, the URL hash changes. Old SSR HTML still references the previous hash → 404 → React never hydrates.

**Fix applied:** Added an inline `unhandledrejection` listener in `__root.tsx` `RootShell` that detects "dynamically imported module" failures and auto-reloads the page (with 8-second cooldown via `sessionStorage` to prevent infinite loops).

**User-facing workaround (before fix):** Manually refresh the preview pane after any code change.
