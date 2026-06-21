# Coffeeyar (Peakjoy) - Complete Project Index
# ============================================

## 📍 Basic Info
- **App Name:** coffeeyar
- **Site:** peakjoy.ir
- **App Path:** `/home/sepehr/den-v16-docker/apps/coffeeyar/`
- **Site Path (host):** `/home/sepehr/den-v16-docker/sites/peakjoy.ir/`
- **Site Path (docker):** `/home/frappe/frappe-bench/sites/peakjoy.ir/`
- **Docker Containers:** `den-v16-backend` (app), `den-v16-db` (MariaDB)
- **DB Root Password:** 7C7uWH2ds7
- **DB Name:** _11254399d006b45b
- **DB User:** _11254399d006b45b
- **DB Password:** TzawH22ZjKmElYOY

## 🛠️ Tech Stack
- **Backend:** Frappe v16 (Python 3.14)
- **Frontend:** Vue 3.5 + Vite 7 + TailwindCSS 4 + Pinia + Vue Router 4
- **Auth:** JWT via api_router (token in localStorage `navar_token_v1`) + Frappe Session
- **Payment:** Zarinpal (Sandbox)
- **Font:** Vazirmatn (CDN), RTL
- **Themes:** 9 design themes (minimal/bento/modern/dark/earthy/scandinavian/swiss/glass)

## 🏗️ Project Structure
```
coffeeyar/
├── __init__.py          ← MUST have __path__ override (see Gotchas)
├── pyproject.toml
├── README.md
├── frontend/            ← Vue 3 SPA
│   ├── src/
│   │   ├── main.js      ← Entry (Pinia, Router, tryFrappeSession)
│   │   ├── App.vue      ← Root (RouterView)
│   │   ├── router/index.js  ← 27 routes + admin guard
│   │   ├── lib/api.js   ← API client (BASE=/_api, Bearer token)
│   │   ├── lib/utils.js ← toFa() number converter
│   │   ├── stores/      ← 18+ Pinia stores
│   │   ├── views/       ← 27 views
│   │   ├── components/  ← Shared components
│   │   ├── themes/      ← 4 theme variants (default/dark/earthy/glass)
│   │   └── styles.css
│   ├── package.json
│   └── vite.config.ts
└── coffeeyar/           ← Frappe app
    ├── __init__.py
    ├── hooks.py         ← App config, routes, before_request, page_renderer
    ├── api.py           ← Core logic + before_request_api + ApiRenderer
    ├── api_router.py    ← All /_api/* routes (1618 lines)
    ├── variant.py       ← Variant CRUD (362 lines)
    ├── install.py       ← Seed data
    ├── patches.txt
    ├── patches/         ← DB migration patches
    ├── www/
    │   ├── coffee.html  ← SPA shell (Jinja2)
    │   ├── coffee.py    ← Page context (boot data)
    │   ├── api_handler.html
    │   └── api_handler.py
    ├── coffeeyar/
    │   └── doctype/     ← 32 DocTypes
    ├── public/
    │   └── frontend/    ← Built assets
    ├── config/
    ├── templates/
    └── modules.txt
```

## 📦 32 DocTypes
**Products (11):** Product, Product Variant, Product Attribute, Product Attribute Option, Product Attribute Value, Product Category, Product Group Setting, Product Template Setting, Product Review, Product FAQ, Product Global FAQ Setting
**Orders (5):** Order, Order Item, Coupon, Return Request, Return Request Item
**Customers (4):** Customer Profile, Customer Address, Customer Wallet, Wallet Transaction
**Content (6):** Blog Post, FAQ, Page Content, Site Page, Site Policy, Navigation Link
**Settings (6):** Store Settings, Theme Config, Taste Profile Setting, User Notification, Contact Message

## 🛣️ 27 Frontend Routes
**Public (19):** /, /products, /products/:id, /cart, /checkout, /payment, /order-success, /auth, /link, /wishlist, /about, /contact, /faq, /blog, /blog/:slug, /account, /tracking, /appearance, /policies
**Admin (18):** /admin/login, /admin (dashboard, products, groups, templates, profiles, categories, orders, returns, customers, posts, content, faq, product-faqs, site-settings, appearance, coupons, settings, policies)
**Catch-all:** /* → NotFoundView

## 🔌 API Endpoints (all /_api/*)
Auth: register, login, me, updateMe
Products: list, get, faqs | Categories: list | Attributes: list
Orders: create, list, get | Reviews: list, create
Wishlist: list, ids, toggle | Coupons: validate
Returns: create, list | Wallet: get, charge, spend
Addresses: list, create, delete | Notifications: list, markRead, markAllRead, remove
FAQ: list | Blog: list, get
Content/Policies/ProductGlobalFaqs/Theme/SiteSettings/Navigation: GET
Contact: POST | Upload: POST (admin)
Admin: dashboard, products CRUD, categories CRUD, orders+status, customers, blog CRUD, faq CRUD, coupons CRUD+toggle, navigation CRUD, site-settings, returns+status, messages, content, policies, groups, templates, profiles, product-faqs, theme

## 🔐 Auth System
- **JWT Token:** Stored in localStorage as `navar_token_v1`
- **Session:** Stored in localStorage as `navar_session_v1`
- **Token Generation:** `secrets.token_urlsafe(32)`, cached in Frappe cache with 30-day expiry
- **Token Resolution:** 1) Custom API token from header, 2) Frappe session cookie
- **Admin Check:** `System Manager` role required

## 🎨 Design System (layout.js)
- 9 design themes, 4 header variants, 3 footer variants, 3 hero variants, 3 card variants
- 3 button styles (sharp/rounded/pill), 6 accent colors (default/blue/teal/amber/purple/rose)
- Per-page design override via pageDesigns
- Theme config stored in `Theme Config` doctype (theme_json, layout_json)

## 💰 Payment Flow
1. `POST /_api/orders` → Create order (status: "Pending Payment")
2. `POST /_api/payment/start` → Get Zarinpal payment URL
3. User pays on Zarinpal
4. Zarinpal redirects to `/payment/callback?order_id=...&Authority=...&Status=OK`
5. `POST /_api/payment/verify` → Verify payment with Zarinpal

## 🌐 Website Routing (hooks.py)
```
home_page = "coffee"
website_route_rules = [
    {from_route: "/_api/<path>", to_route: "api_handler"},
    {from_route: "/desk", to_route: "desk"},
    {from_route: "/login", to_route: "login"},
    {from_route: "/", to_route: "coffee"},
    {from_route: "/<path>", to_route: "coffee"},  ← SPA catch-all
]
before_request = ["coffeeyar.api.before_request_api"]
page_renderer = ["coffeeyar.api.ApiRenderer"]
```

## ⚠️ Critical Gotchas
1. **`__init__.py` path fix:** `/apps/coffeeyar/__init__.py` MUST contain:
   ```python
   import os
   __path__ = [os.path.join(os.path.dirname(__file__), 'coffeeyar')]
   ```
   Without this, Python can't find `coffeeyar.hooks` because the app has nested package structure.

2. **MySQL password reset after DB container restart:**
   ```bash
   docker exec den-v16-db mysql -u root -p'7C7uWH2ds7' -e "CREATE USER IF NOT EXISTS '_11254399d006b45b'@'%' IDENTIFIED BY 'TzawH22ZjKmElYOY'; GRANT ALL PRIVILEGES ON _11254399d006b45b.* TO '_11254399d006b45b'@'%'; FLUSH PRIVILEGES;"
   ```

3. **Static assets guard:** `coffee.py` blocks /assets/, /_, /files/, /private/ paths

4. **CSRF:** Use `getCookie('csrf_token')` with `credentials: 'same-origin'`

5. **Admin routes:** Require `System Manager` role

6. **Build output:** `npm run build` in `frontend/` → `coffeeyar/public/frontend/`

7. **data.js deleted** — all data comes from Frappe API now

8. **backend/ deleted** — FastAPI standalone was removed, not needed

## 🔄 Build & Deploy
```bash
# Build frontend
cd /home/sepehr/den-v16-docker/apps/coffeeyar/frontend
npm run build

# Copy to Docker (if not volume-mounted)
docker cp ../coffeeyar/public/frontend/index.html den-v16-backend:/home/frappe/frappe-bench/apps/coffeeyar/coffeeyar/public/frontend/index.html

# Clear cache
docker exec -u frappe den-v16-backend bash -c "cd /home/frappe/frappe-bench && bench --site peakjoy.ir clear-cache"
```

## 🐛 Debugging
```bash
# Check site from inside container
docker exec den-v16-backend bash -c "curl -s -H 'Host: peakjoy.ir' http://localhost:8000/coffee"

# Check logs
docker exec den-v16-backend bash -c "tail -50 /home/frappe/frappe-bench/logs/frappe.log"

# Check installed apps
docker exec -u frappe den-v16-backend bash -c "cd /home/frappe/frappe-bench && bench --site peakjoy.ir list-apps"

# Console
docker exec -u frappe den-v16-backend bash -c "cd /home/frappe/frappe-bench && bench --site peakjoy.ir console"
```
