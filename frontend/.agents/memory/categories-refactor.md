---
name: Generic 2-level category system refactor
description: All product categorization moved from hardcoded coffee/accessory model to a generic 2-level category tree.
---

## Rule
Products use `categoryId` (root) + `subCategoryId` (child) + `attrs: {}` (dynamic key-value map). No `type`, `roast`, `origin`, `groupId`, `category` legacy fields in new code.

**Why:** User wanted a fully generic product catalog that works for any type of goods — not just coffee/accessories.

## How to apply
- Category attributes defined per root category in `useCategoriesStore` (key `navar_categories_v2`)
- `selectedRootCat.value?.attributes` drives dynamic form fields in AdminProducts drawer
- `categoriesStore.roots` drives filter tabs in ProductsView and AdminProducts filter bar
- `categoriesStore.children(catId)` drives sub-category dropdowns everywhere
- `getRootFor(id)` returns the root category for either a root or child ID

## Key files
- `src/stores/categories.js` — 2-level store, methods: roots, children, getById, getRootFor, add, update, remove, reorder
- `src/views/admin/AdminProducts.vue` — uses categoriesStore, emptyProduct (no type distinction), generic drawer form
- `src/views/admin/AdminCategories.vue` — tree accordion editor with attribute editor
- `src/views/ProductsView.vue` — category tabs driven by store roots, dynamic filters
- `src/components/SearchModal.vue` — uses categoriesStore.getById for display
- `src/lib/data.js` — all 11 products have categoryId/subCategoryId/attrs; legacy fields kept for ProductDetailView backward compat
