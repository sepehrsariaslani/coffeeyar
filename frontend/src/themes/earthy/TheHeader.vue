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
  <header class="ea-header">
    <div class="ea-header__inner">
      <RouterLink to="/" class="ea-logo">
        <span class="ea-logo__leaf">🌿</span> {{ '' }}نـوار<span class="ea-logo__dot">.</span>
      </RouterLink>
      <nav class="ea-nav hidden md:flex">
        <RouterLink v-for="l in links" :key="l.to" :to="l.to"
          :class="['ea-nav__link', isActive(l) ? 'ea-nav__link--active' : '']">
          {{ l.label }}
        </RouterLink>
      </nav>
      <div class="ea-actions">
        <button @click="searchOpen = true" class="ea-icon"><Search class="h-4 w-4" /></button>
        <RouterLink to="/wishlist" class="ea-icon relative">
          <Heart class="h-4 w-4" :class="wishlistStore.count > 0 ? 'fill-green-700 text-green-700' : ''" />
          <span v-if="wishlistStore.count > 0" class="ea-badge">{{ toFa(wishlistStore.count) }}</span>
        </RouterLink>
        <RouterLink to="/cart" class="ea-cart">
          <ShoppingBag class="h-4 w-4" />
          <span v-if="cartStore.count > 0">{{ toFa(cartStore.count) }}</span>
          <span v-else class="hidden md:inline">سبد</span>
        </RouterLink>
        <template v-if="authStore.isLoggedIn">
          <RouterLink to="/account" class="ea-icon"><User class="h-4 w-4" /></RouterLink>
          <button @click="authStore.logout()" class="ea-icon hidden md:flex"><LogOut class="h-4 w-4" /></button>
        </template>
        <RouterLink v-else to="/auth" class="hidden md:block text-xs text-stone-500 hover:text-green-800 transition-colors">ورود</RouterLink>
        <button class="ea-icon md:hidden" @click="open = !open">
          <X v-if="open" class="h-5 w-5" /><Menu v-else class="h-5 w-5" />
        </button>
      </div>
    </div>
    <div v-if="open" class="ea-mobile-menu">
      <RouterLink v-for="l in links" :key="l.to" :to="l.to" @click="open = false" class="ea-mobile-link">{{ l.label }}</RouterLink>
      <RouterLink v-if="!authStore.isLoggedIn" to="/auth" @click="open = false" class="ea-mobile-link ea-mobile-link--cta">ورود / ثبت‌نام</RouterLink>
    </div>
  </header>
  <SearchModal v-if="searchOpen" @close="searchOpen = false" />
</template>

<style scoped>
.ea-header { position: sticky; top: 0; z-index: 50; background-color: #F5F0E8; border-bottom: 1.5px solid #D6CBB8; }
.ea-header__inner { max-width: 1280px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; padding: 0 1.5rem; height: 4rem; }
.ea-logo { font-size: 1.1rem; font-weight: 600; text-decoration: none; color: #2d2416; display: flex; align-items: center; gap: 0.4rem; letter-spacing: -0.01em; }
.ea-logo__dot { color: #4a7c59; }
.ea-logo__leaf { font-size: 1rem; }
.ea-nav { align-items: center; gap: 0.1rem; }
.ea-nav__link { padding: 0.4rem 1rem; border-radius: 9999px; font-size: 0.82rem; text-decoration: none; color: #6b5b45; transition: all 0.2s; }
.ea-nav__link:hover { background: #EDE5D6; color: #2d2416; }
.ea-nav__link--active { background: #4a7c59; color: #fff; font-weight: 500; }
.ea-actions { display: flex; align-items: center; gap: 0.4rem; }
.ea-icon { display: flex; align-items: center; justify-content: center; width: 34px; height: 34px; border-radius: 50%; background: #EDE5D6; border: 1.5px solid #D6CBB8; color: #6b5b45; cursor: pointer; text-decoration: none; transition: all 0.2s; position: relative; }
.ea-icon:hover { background: #E0D5C0; color: #2d2416; }
.ea-badge { position: absolute; top: -3px; left: -3px; background: #4a7c59; color: white; font-size: 0.6rem; min-width: 15px; height: 15px; border-radius: 9999px; display: flex; align-items: center; justify-content: center; padding: 0 2px; font-weight: 700; }
.ea-cart { display: flex; align-items: center; gap: 0.4rem; padding: 0.4rem 0.9rem; border-radius: 9999px; background: #4a7c59; color: #fff; font-size: 0.78rem; font-weight: 600; text-decoration: none; transition: opacity 0.2s; box-shadow: 0 2px 8px rgba(74,124,89,0.3); }
.ea-cart:hover { opacity: 0.88; }
.ea-mobile-menu { background: #F5F0E8; border-top: 1.5px solid #D6CBB8; padding: 0.75rem 1.5rem; display: flex; flex-direction: column; gap: 0.1rem; }
.ea-mobile-link { padding: 0.65rem 0.75rem; border-radius: 0.6rem; font-size: 0.9rem; text-decoration: none; color: #6b5b45; transition: background 0.15s; }
.ea-mobile-link:hover { background: #EDE5D6; }
.ea-mobile-link--cta { color: #4a7c59; font-weight: 600; }
</style>
