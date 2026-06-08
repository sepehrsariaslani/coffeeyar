const BASE = "/api";

function getToken() {
  return localStorage.getItem("navar_token_v1") || "";
}

function setToken(t) {
  if (t) localStorage.setItem("navar_token_v1", t);
  else localStorage.removeItem("navar_token_v1");
}

async function req(method, path, body = null, auth = false) {
  const headers = { "Content-Type": "application/json" };
  const token = getToken();
  if (auth || token) {
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }
  const opts = { method, headers };
  if (body !== null) opts.body = JSON.stringify(body);
  const res = await fetch(`${BASE}${path}`, opts);
  if (!res.ok) {
    let msg = `خطا: ${res.status}`;
    try {
      const err = await res.json();
      msg = err.detail || err.message || msg;
    } catch {}
    throw new Error(msg);
  }
  return res.json();
}

const get = (path) => req("GET", path);
const post = (path, body) => req("POST", path, body);
const put = (path, body) => req("PUT", path, body);
const patch = (path, body) => req("PATCH", path, body);
const del = (path) => req("DELETE", path);

export const api = {
  setToken,
  getToken,

  // Auth
  auth: {
    register: (data) => post("/auth/register", data).then((r) => { setToken(r.token); return r; }),
    login: (data) => post("/auth/login", data).then((r) => { setToken(r.token); return r; }),
    logout: () => { setToken(null); },
    me: () => get("/auth/me"),
    updateMe: (data) => req("PUT", "/auth/me", data),
  },

  // Addresses
  addresses: {
    list: () => get("/addresses"),
    create: (data) => post("/addresses", data),
    remove: (id) => del(`/addresses/${id}`),
  },

  // Categories
  categories: {
    list: () => get("/categories"),
  },

  // Products
  products: {
    list: (params = {}) => {
      const q = new URLSearchParams();
      if (params.category_slug) q.set("category_slug", params.category_slug);
      if (params.featured) q.set("featured", "true");
      if (params.in_stock) q.set("in_stock", "true");
      if (params.sort) q.set("sort", params.sort);
      if (params.page) q.set("page", params.page);
      if (params.page_size) q.set("page_size", params.page_size);
      return get(`/products?${q}`);
    },
    get: (slug) => get(`/products/${slug}`),
    faqs: (slug) => get(`/products/${slug}/faqs`),
  },

  // Reviews
  reviews: {
    list: (product_id) => get(`/reviews/${product_id}`),
    create: (data) => post("/reviews", data),
  },

  // Wishlist
  wishlist: {
    list: () => get("/wishlist"),
    ids: () => get("/wishlist/ids"),
    toggle: (product_id) => post(`/wishlist/${product_id}`),
  },

  // Coupons
  coupons: {
    validate: (code, order_total) => post("/coupons/validate", { code, order_total }),
  },

  // Orders
  orders: {
    create: (data) => post("/orders", data),
    list: () => get("/orders"),
    get: (ref) => get(`/orders/${ref}`),
  },

  // Returns
  returns: {
    create: (data) => post("/returns", data),
    list: () => get("/returns"),
  },

  // FAQ
  faq: {
    list: () => get("/faq"),
  },

  // Blog
  blog: {
    list: (page = 1, page_size = 12) => get(`/blog?page=${page}&page_size=${page_size}`),
    get: (slug) => get(`/blog/${slug}`),
  },

  // Content / Policies
  content: {
    get: () => get("/content"),
  },
  policies: {
    get: () => get("/policies"),
  },
  productGlobalFaqs: {
    get: () => get("/product-global-faqs"),
  },

  // Site
  site: {
    settings: () => get("/site-settings"),
    navigation: () => get("/navigation"),
  },

  // Admin
  admin: {
    dashboard: () => get("/admin/dashboard"),

    products: {
      list: () => get("/admin/products"),
      create: (data) => post("/admin/products", data),
      update: (id, data) => put(`/admin/products/${id}`, data),
      remove: (id) => del(`/admin/products/${id}`),
    },

    categories: {
      list: () => get("/admin/categories"),
      create: (data) => post("/admin/categories", data),
      update: (id, data) => put(`/admin/categories/${id}`, data),
      remove: (id) => del(`/admin/categories/${id}`),
    },

    orders: {
      list: () => get("/admin/orders"),
      updateStatus: (id, data) => put(`/admin/orders/${id}/status`, data),
    },

    customers: {
      list: () => get("/admin/customers"),
    },

    blog: {
      list: () => get("/admin/blog"),
      create: (data) => post("/admin/blog", data),
      update: (id, data) => put(`/admin/blog/${id}`, data),
      remove: (id) => del(`/admin/blog/${id}`),
    },

    faq: {
      list: () => get("/admin/faq"),
      create: (data) => post("/admin/faq", data),
      update: (id, data) => put(`/admin/faq/${id}`, data),
      remove: (id) => del(`/admin/faq/${id}`),
    },

    coupons: {
      list: () => get("/admin/coupons"),
      create: (data) => post("/admin/coupons", data),
      remove: (id) => del(`/admin/coupons/${id}`),
      toggle: (id) => patch(`/admin/coupons/${id}/toggle`),
    },

    navigation: {
      list: () => get("/admin/navigation"),
      create: (data) => post("/admin/navigation", data),
      update: (id, data) => put(`/admin/navigation/${id}`, data),
      remove: (id) => del(`/admin/navigation/${id}`),
    },

    settings: {
      update: (data) => put("/admin/site-settings", data),
    },

    returns: {
      list: () => get("/admin/returns"),
      updateStatus: (id, data) => put(`/admin/returns/${id}/status`, data),
    },

    content: {
      get: () => get("/admin/content"),
      update: (data) => put("/admin/content", data),
    },

    policies: {
      get: () => get("/admin/policies"),
      update: (data) => put("/admin/policies", data),
    },

    groups: {
      get: () => get("/admin/groups"),
      update: (data) => put("/admin/groups", data),
    },

    templates: {
      get: () => get("/admin/templates"),
      update: (data) => put("/admin/templates", data),
    },

    profiles: {
      get: () => get("/admin/profiles"),
      update: (data) => put("/admin/profiles", data),
    },

    productFaqs: {
      get: () => get("/admin/product-faqs"),
      update: (data) => put("/admin/product-faqs", data),
    },

    theme: {
      get: () => get("/admin/theme"),
      update: (data) => put("/admin/theme", data),
    },
  },
};
