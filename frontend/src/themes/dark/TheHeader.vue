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
  <header class="dk-header">
    <div class="dk-header__top-accent" />
    <div class="dk-header__inner">
      <RouterLink to="/" class="dk-logo">نـوار<span class="dk-logo__dot">.</span></RouterLink>
      <nav class="dk-nav hidden md:flex">
        <RouterLink v-for="l in links" :key="l.to" :to="l.to"
          :class="['dk-nav__link', isActive(l) ? 'dk-nav__link--active' : '']">
          {{ l.label }}
        </RouterLink>
      </nav>
      <div class="dk-actions">
        <button @click="searchOpen = true" class="dk-icon">
          <Search class="h-4.5 w-4.5" />
        </button>
        <RouterLink to="/wishlist" class="dk-icon relative">
          <Heart class="h-4.5 w-4.5" :class="wishlistStore.count > 0 ? 'fill-amber-400 text-amber-400' : ''" />
          <span v-if="wishlistStore.count > 0" class="dk-badge">{{ toFa(wishlistStore.count) }}</span>
        </RouterLink>
        <RouterLink to="/cart" class="dk-cart">
          <ShoppingBag class="h-4.5 w-4.5" />
          <span v-if="cartStore.count > 0">{{ toFa(cartStore.count) }}</span>
          <span v-else class="hidden md:inline">سبد</span>
        </RouterLink>
        <template v-if="authStore.isLoggedIn">
          <RouterLink to="/account" class="dk-icon"><User class="h-4.5 w-4.5" /></RouterLink>
          <button @click="authStore.logout()" class="dk-icon hidden md:flex"><LogOut class="h-4 w-4" /></button>
        </template>
        <RouterLink v-else to="/auth" class="hidden md:block text-xs text-white/50 hover:text-white transition-colors">ورود</RouterLink>
        <button class="dk-icon md:hidden" @click="open = !open">
          <X v-if="open" class="h-5 w-5" /><Menu v-else class="h-5 w-5" />
        </button>
      </div>
    </div>
    <div v-if="open" class="dk-mobile-menu">
      <RouterLink v-for="l in links" :key="l.to" :to="l.to" @click="open = false" class="dk-mobile-link">{{ l.label }}</RouterLink>
      <RouterLink v-if="!authStore.isLoggedIn" to="/auth" @click="open = false" class="dk-mobile-link dk-mobile-link--cta">ورود / ثبت‌نام</RouterLink>
    </div>
  </header>
  <SearchModal v-if="searchOpen" @close="searchOpen = false" />
</template>

<style scoped>
.dk-header { position: sticky; top: 0; z-index: 50; background-color: #111; border-bottom: 1px solid rgba(255,255,255,0.07); }
.dk-header__top-accent { height: 2px; background: linear-gradient(to left, #C9923F, #e6a84a, #C9923F); }
.dk-header__inner { max-width: 1280px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; padding: 0 1.5rem; height: 3.75rem; }
.dk-logo { font-size: 1.15rem; font-weight: 500; text-decoration: none; color: rgba(255,255,255,0.9); letter-spacing: -0.01em; }
.dk-logo__dot { color: #C9923F; }
.dk-nav { align-items: center; gap: 0.15rem; }
.dk-nav__link { padding: 0.35rem 0.85rem; font-size: 0.82rem; text-decoration: none; color: rgba(255,255,255,0.5); transition: all 0.2s; border-radius: 0.4rem; }
.dk-nav__link:hover { color: rgba(255,255,255,0.85); background: rgba(255,255,255,0.05); }
.dk-nav__link--active { color: #C9923F; font-weight: 500; }
.dk-actions { display: flex; align-items: center; gap: 0.35rem; }
.dk-icon { display: flex; align-items: center; justify-content: center; width: 34px; height: 34px; border-radius: 50%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.10); color: rgba(255,255,255,0.55); cursor: pointer; text-decoration: none; transition: all 0.2s; position: relative; }
.dk-icon:hover { background: rgba(255,255,255,0.09); color: rgba(255,255,255,0.9); }
.dk-badge { position: absolute; top: -3px; left: -3px; background: #C9923F; color: #111; font-size: 0.6rem; min-width: 15px; height: 15px; border-radius: 9999px; display: flex; align-items: center; justify-content: center; padding: 0 2px; font-weight: 700; }
.dk-cart { display: flex; align-items: center; gap: 0.4rem; padding: 0.4rem 0.9rem; border-radius: 9999px; background: #C9923F; color: #0d0d0d; font-size: 0.78rem; font-weight: 700; text-decoration: none; transition: opacity 0.2s; }
.dk-cart:hover { opacity: 0.88; }
.dk-mobile-menu { background: #111; border-top: 1px solid rgba(255,255,255,0.07); padding: 0.75rem 1.5rem; display: flex; flex-direction: column; gap: 0.1rem; }
.dk-mobile-link { padding: 0.65rem 0; font-size: 0.9rem; text-decoration: none; color: rgba(255,255,255,0.55); border-bottom: 1px solid rgba(255,255,255,0.05); transition: color 0.15s; }
.dk-mobile-link:hover { color: rgba(255,255,255,0.9); }
.dk-mobile-link--cta { color: #C9923F; border-bottom: none; }
</style>
