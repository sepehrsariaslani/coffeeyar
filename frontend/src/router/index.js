import { createRouter, createWebHistory } from "vue-router";
import { useLayoutStore, applyDesignTheme } from "@/stores/layout.js";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: () => import("@/views/HomeView.vue") },
    { path: "/products", component: () => import("@/views/ProductsView.vue") },
    { path: "/products/:id", component: () => import("@/views/ProductDetailView.vue") },
    { path: "/cart", component: () => import("@/views/CartView.vue") },
    { path: "/checkout", component: () => import("@/views/CheckoutView.vue") },
    { path: "/payment", component: () => import("@/views/PaymentView.vue") },
    { path: "/order-success", component: () => import("@/views/OrderSuccessView.vue") },
    { path: "/auth", component: () => import("@/views/AuthView.vue") },
    { path: "/wishlist", component: () => import("@/views/WishlistView.vue") },
    { path: "/about", component: () => import("@/views/AboutView.vue") },
    { path: "/contact", component: () => import("@/views/ContactView.vue") },
    { path: "/faq", component: () => import("@/views/FaqView.vue") },
    { path: "/blog", component: () => import("@/views/BlogView.vue") },
    { path: "/blog/:slug", component: () => import("@/views/BlogPostView.vue") },
    { path: "/account", component: () => import("@/views/AccountView.vue") },
    { path: "/tracking", component: () => import("@/views/TrackingView.vue") },
    { path: "/appearance", component: () => import("@/views/AppearanceView.vue") },
    { path: "/policies", component: () => import("@/views/PoliciesView.vue") },
    {
      path: "/admin",
      component: () => import("@/views/admin/AdminLayout.vue"),
      children: [
        { path: "", component: () => import("@/views/admin/AdminDashboard.vue") },
        { path: "products", component: () => import("@/views/admin/AdminProducts.vue") },
        { path: "groups", component: () => import("@/views/admin/AdminGroups.vue") },
        { path: "templates", component: () => import("@/views/admin/AdminTemplates.vue") },
        { path: "profiles", component: () => import("@/views/admin/AdminProfiles.vue") },
        { path: "categories", component: () => import("@/views/admin/AdminCategories.vue") },
        { path: "orders", component: () => import("@/views/admin/AdminOrders.vue") },
        { path: "returns", component: () => import("@/views/admin/AdminReturns.vue") },
        { path: "customers", component: () => import("@/views/admin/AdminCustomers.vue") },
        { path: "posts", component: () => import("@/views/admin/AdminPosts.vue") },
        { path: "content", component: () => import("@/views/admin/AdminContent.vue") },
        { path: "faq", component: () => import("@/views/admin/AdminFaq.vue") },
        { path: "product-faqs", component: () => import("@/views/admin/AdminProductFaqs.vue") },
        { path: "site-settings", component: () => import("@/views/admin/AdminSiteSettings.vue") },
        { path: "appearance", component: () => import("@/views/admin/AdminAppearance.vue") },
        { path: "settings", redirect: "/admin/appearance" },
        { path: "coupons", component: () => import("@/views/admin/AdminCoupons.vue") },
        { path: "invoice", component: () => import("@/views/admin/AdminInvoice.vue") },
        { path: "policies", component: () => import("@/views/admin/AdminPolicies.vue") },
      ],
    },
    { path: "/:pathMatch(.*)*", component: () => import("@/views/NotFoundView.vue") },
  ],
  scrollBehavior() {
    return { top: 0 };
  },
});

// Apply per-page design theme on navigation
router.afterEach((to) => {
  if (to.path.startsWith("/admin")) return;
  try {
    const layoutStore = useLayoutStore();
    const effective = layoutStore.getEffectiveDesign(to.path);
    applyDesignTheme(effective);
  } catch {}
});

export { router };
