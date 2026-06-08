---
name: Vue 3 migration
description: Full migration from TanStack Start (React + SSR) to Vue 3 SPA. Key decisions and gotchas.
---

## Stack
- Vue 3 + Vite + Vue Router 4 (SPA, no SSR) + Pinia + Tailwind CSS v4 + lucide-vue-next
- Node 22, npm, port 5000
- `@vitejs/plugin-vue` in vite.config.ts

## Critical file layout
- `index.html` — entry HTML, `<div id="app">`, `lang="fa" dir="rtl"`, loads `src/main.ts`
- `src/main.ts` — createApp + Pinia + router
- `src/router/index.ts` — all routes (export named `router`)
- `src/stores/` — cart.ts, account.ts, templates.ts (Pinia)
- `src/views/` — page components
- `src/views/admin/` — admin pages (AdminLayout wraps via `<RouterView>`)
- `src/components/site/` — TheHeader, TheFooter, TheLayout, MobileBottomNav, FlavorTriangle
- `src/lib/data.ts` — unchanged static data (products, posts, customers, formatPrice)
- `src/lib/utils.ts` — only `toFa()` (digits → Persian)
- `src/assets/` — product-1..4.jpg, hero-coffee.jpg, about.jpg

## RTL setup
- `html { direction: rtl }` in styles.css + `<html lang="fa" dir="rtl">` in index.html

## Tailwind v4
- `src/styles.css` uses `@import "tailwindcss" source(none)` + `@source "../src"`
- Custom tokens: `--maroon`, `--maroon-foreground` defined in CSS

## Gotcha: old router.tsx conflict
- If `src/router.tsx` (old TanStack file) exists alongside `src/router/index.ts`,
  Vite resolves `import "./router"` to the `.tsx` file, not the directory.
- Fix: delete `src/router.tsx` (and all other TanStack files: src/routes/, src/start.ts, src/server.ts, src/routeTree.gen.ts) then restart workflow to clear module cache.

**Why:** Vite's module resolution prefers explicit `.tsx` extension over directory `index.ts`.

**How to apply:** Always restart the workflow after deleting conflicting old files — Vite caches module graph in memory.
