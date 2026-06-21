<script setup>
import { ref, computed } from "vue";
import { useRoute, RouterLink } from "vue-router";
import { Menu, X, ShoppingBag, Search, Heart, User, LogOut } from "lucide-vue-next";
import { useCartStore } from "@/stores/cart.js";
import { useAuthStore } from "@/stores/auth.js";
import { useWishlistStore } from "@/stores/wishlist.js";
import { toFa } from "@/lib/utils.js";
import SearchModal from "@/components/SearchModal.vue";
import { onMounted, onUnmounted } from "vue";

const route = useRoute();
const cartStore = useCartStore();
const authStore = useAuthStore();
const wishlistStore = useWishlistStore();
const open = ref(false);
const searchOpen = ref(false);

function onSearchKey(e) {
  if ((e.ctrlKey || e.metaKey) && e.key === "k") { e.preventDefault(); searchOpen.value = true; }
}
onMounted(() => window.addEventListener("keydown", onSearchKey));
onUnmounted(() => window.removeEventListener("keydown", onSearchKey));

const links = [
  { to: "/", label: "خانه", exact: true },
  { to: "/products", label: "محصولات" },
  { to: "/about", label: "درباره ما" },
  { to: "/blog", label: "بلاگ" },
  { to: "/faq", label: "سوالات" },
  { to: "/contact", label: "تماس" },
];
function isActive(link) {
  if (link.exact) return route.path === link.to;
  return route.path.startsWith(link.to);
}
</script>

<template>
  <header class="gl-header">
    <div class="gl-header__bar">
      <RouterLink to="/" class="gl-logo">
        نـوار<span class="gl-logo__dot">.</span>
      </RouterLink>

      <nav class="gl-nav hidden md:flex">
        <RouterLink
          v-for="l in links" :key="l.to" :to="l.to"
          :class="['gl-nav__link', isActive(l) ? 'gl-nav__link--active' : '']"
        >{{ l.label }}</RouterLink>
      </nav>

      <div class="gl-actions">
        <button @click="searchOpen = true" class="gl-icon-btn">
          <Search class="h-4 w-4" />
        </button>
        <RouterLink to="/wishlist" class="gl-icon-btn relative">
          <Heart class="h-4 w-4" :class="wishlistStore.count > 0 ? 'fill-violet-600 text-violet-600' : ''" />
          <span v-if="wishlistStore.count > 0" class="gl-badge">{{ toFa(wishlistStore.count) }}</span>
        </RouterLink>
        <RouterLink to="/cart" class="gl-cart-btn">
          <ShoppingBag class="h-4 w-4" />
          <span v-if="cartStore.count > 0">{{ toFa(cartStore.count) }}</span>
          <span v-else class="hidden md:inline">سبد</span>
        </RouterLink>
        <template v-if="authStore.isLoggedIn">
          <RouterLink to="/account" class="gl-icon-btn"><User class="h-4 w-4" /></RouterLink>
          <button @click="authStore.logout()" class="gl-icon-btn hidden md:flex"><LogOut class="h-4 w-4" /></button>
        </template>
        <RouterLink v-else to="/auth" class="hidden md:block text-xs text-slate-600 hover:text-violet-700 transition-colors">ورود</RouterLink>
        <button class="gl-icon-btn md:hidden" @click="open = !open">
          <X v-if="open" class="h-5 w-5" /><Menu v-else class="h-5 w-5" />
        </button>
      </div>
    </div>

    <!-- Mobile menu -->
    <div v-if="open" class="gl-mobile-menu">
      <RouterLink v-for="l in links" :key="l.to" :to="l.to" @click="open = false" class="gl-mobile-link">{{ l.label }}</RouterLink>
      <RouterLink v-if="!authStore.isLoggedIn" to="/auth" @click="open = false" class="gl-mobile-link text-violet-700">ورود / ثبت‌نام</RouterLink>
    </div>
  </header>

  <SearchModal v-if="searchOpen" @close="searchOpen = false" />
</template>

<style scoped>
.gl-header {
  position: sticky;
  top: 0;
  z-index: 50;
  padding: 0.65rem 1.25rem;
}
.gl-header__bar {
  max-width: 1280px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.25rem;
  height: 3.25rem;
  background: rgba(255, 255, 255, 0.48);
  backdrop-filter: blur(28px) saturate(200%);
  -webkit-backdrop-filter: blur(28px) saturate(200%);
  border: 1px solid rgba(255, 255, 255, 0.65);
  border-radius: 1rem;
  box-shadow:
    inset 0 1.5px 0 rgba(255,255,255,0.75),
    0 8px 32px rgba(100, 60, 220, 0.12),
    0 2px 8px rgba(0,0,0,0.06);
}
.gl-logo {
  font-size: 1.1rem;
  font-weight: 600;
  text-decoration: none;
  color: #18103a;
  letter-spacing: -0.01em;
}
.gl-logo__dot { color: oklch(0.46 0.22 278); }
.gl-nav { align-items: center; gap: 0.15rem; }
.gl-nav__link {
  padding: 0.35rem 0.85rem;
  border-radius: 0.6rem;
  font-size: 0.82rem;
  text-decoration: none;
  color: rgba(20,10,60,0.6);
  transition: all 0.2s;
}
.gl-nav__link:hover { background: rgba(255,255,255,0.55); color: #18103a; }
.gl-nav__link--active {
  background: rgba(255,255,255,0.65);
  color: oklch(0.38 0.20 278);
  font-weight: 600;
}
.gl-actions { display: flex; align-items: center; gap: 0.4rem; }
.gl-icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px; height: 32px;
  border-radius: 50%;
  background: rgba(255,255,255,0.5);
  border: 1px solid rgba(255,255,255,0.7);
  color: rgba(20,10,60,0.65);
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s;
  position: relative;
}
.gl-icon-btn:hover {
  background: rgba(255,255,255,0.75);
  color: oklch(0.38 0.20 278);
}
.gl-badge {
  position: absolute;
  top: -4px; left: -4px;
  background: oklch(0.46 0.22 278);
  color: white;
  font-size: 0.6rem;
  min-width: 16px; height: 16px;
  border-radius: 9999px;
  display: flex; align-items: center; justify-content: center;
  padding: 0 3px;
}
.gl-cart-btn {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.4rem 0.9rem;
  border-radius: 9999px;
  background: oklch(0.46 0.22 278);
  color: white;
  font-size: 0.78rem;
  font-weight: 500;
  text-decoration: none;
  transition: opacity 0.2s;
  box-shadow: 0 2px 12px rgba(100,60,220,0.35);
}
.gl-cart-btn:hover { opacity: 0.88; }
.gl-mobile-menu {
  max-width: 1280px;
  margin: 0.5rem auto 0;
  background: rgba(255,255,255,0.55);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255,255,255,0.65);
  border-radius: 1rem;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}
.gl-mobile-link {
  padding: 0.6rem 1rem;
  border-radius: 0.6rem;
  font-size: 0.9rem;
  text-decoration: none;
  color: rgba(20,10,60,0.7);
  transition: background 0.15s;
}
.gl-mobile-link:hover { background: rgba(255,255,255,0.6); }
</style>
