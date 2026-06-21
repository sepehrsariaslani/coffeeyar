<script setup>
import { ref, computed } from "vue";
import { useRoute, RouterLink } from "vue-router";
import { Menu, X, ShoppingBag, Search, User, LogOut, Heart, Bell, Wallet } from "lucide-vue-next";
import { useCartStore } from "@/stores/cart.js";
import { useAuthStore } from "@/stores/auth.js";
import { useWishlistStore } from "@/stores/wishlist.js";
import { useNotificationsStore } from "@/stores/notifications.js";
import { useWalletStore } from "@/stores/wallet.js";
import { useLayoutStore } from "@/stores/layout.js";
import { toFa } from "@/lib/utils.js";
import SearchModal from "@/components/SearchModal.vue";
import { onMounted, onUnmounted } from "vue";

const route = useRoute();
const cartStore = useCartStore();
const authStore = useAuthStore();
const wishlistStore = useWishlistStore();
const notifStore = useNotificationsStore();
const walletStore = useWalletStore();
const layoutStore = useLayoutStore();

const open = ref(false);
const searchOpen = ref(false);
const notifOpen = ref(false);

function toggleNotif() { notifOpen.value = !notifOpen.value; }
function closeNotif() { notifOpen.value = false; }

const recentNotifs = computed(() => notifStore.items.slice(0, 5));
const v = computed(() => layoutStore.headerVariant);

const NOTIF_ICON = {
  wallet: "💰", refund: "💸", return: "↩️", success: "✅", info: "ℹ️", order: "📦",
};

function onSearchKey(e) {
  if ((e.ctrlKey || e.metaKey) && e.key === "k") { e.preventDefault(); searchOpen.value = true; }
}
function onClickOutside(e) {
  if (notifOpen.value && !e.target.closest(".notif-panel") && !e.target.closest(".notif-trigger")) {
    notifOpen.value = false;
  }
}
onMounted(() => { window.addEventListener("keydown", onSearchKey); window.addEventListener("click", onClickOutside); });
onUnmounted(() => { window.removeEventListener("keydown", onSearchKey); window.removeEventListener("click", onClickOutside); });

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
  <!-- ── Variant 1: Classic ──────────────────────────────────── -->
  <header v-if="v === 1" class="sticky top-0 z-50 border-b border-maroon/20 bg-background/85 backdrop-blur-md">
    <div class="h-0.5 w-full bg-maroon" />
    <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
      <RouterLink to="/" class="text-lg font-medium tracking-tight">
        نـوار <span class="text-maroon">.</span>
      </RouterLink>
      <nav class="hidden items-center gap-8 md:flex">
        <RouterLink v-for="l in links" :key="l.to" :to="l.to"
          :class="['relative text-sm transition-colors hover:text-maroon', isActive(l) ? 'text-foreground' : 'text-muted-foreground']">
          {{ l.label }}
          <span v-if="isActive(l)" class="absolute -bottom-[22px] left-0 right-0 h-px bg-maroon" />
        </RouterLink>
      </nav>
      <div class="flex items-center gap-3">
        <button @click="searchOpen = true" class="hidden md:flex items-center gap-2 border border-border px-3 py-1.5 text-xs text-muted-foreground hover:border-maroon hover:text-maroon transition-colors">
          <Search class="h-3.5 w-3.5" /> جستجو <span class="text-[10px] opacity-50">Ctrl+K</span>
        </button>
        <button @click="searchOpen = true" class="md:hidden text-muted-foreground hover:text-maroon"><Search class="h-5 w-5" /></button>
        <RouterLink to="/wishlist" class="relative text-muted-foreground hover:text-maroon transition-colors">
          <Heart class="h-5 w-5" :class="wishlistStore.count > 0 ? 'fill-maroon text-maroon' : ''" />
          <span v-if="wishlistStore.count > 0" class="absolute -top-2 -left-2 flex h-4 min-w-4 items-center justify-center rounded-full bg-maroon px-0.5 text-[9px] text-white">{{ toFa(wishlistStore.count) }}</span>
        </RouterLink>
        <RouterLink to="/cart" class="relative inline-flex items-center gap-2 text-sm text-foreground hover:text-maroon">
          <ShoppingBag class="h-5 w-5" />
          <span v-if="cartStore.count > 0" class="absolute -top-2 -left-2 flex h-5 min-w-5 items-center justify-center rounded-full bg-maroon px-1 text-[10px] text-maroon-foreground">{{ toFa(cartStore.count) }}</span>
        </RouterLink>
        <div v-if="authStore.isLoggedIn" class="relative hidden md:block">
          <button class="notif-trigger relative text-muted-foreground hover:text-maroon" @click.stop="toggleNotif">
            <Bell class="h-5 w-5" />
            <span v-if="notifStore.unreadCount > 0" class="absolute -top-2 -left-2 flex h-4 min-w-4 items-center justify-center rounded-full bg-maroon px-0.5 text-[9px] text-white">{{ toFa(notifStore.unreadCount) }}</span>
          </button>
          <div v-if="notifOpen" class="notif-panel absolute left-0 top-8 z-50 w-80 border border-border bg-background shadow-lg">
            <div class="flex items-center justify-between border-b border-border px-4 py-3">
              <span class="text-sm font-medium">اعلان‌ها</span>
              <button v-if="notifStore.items.length" type="button" class="text-[11px] text-muted-foreground hover:text-maroon" @click="notifStore.markAllRead()">همه خوانده شد</button>
            </div>
            <div v-if="notifStore.items.length === 0" class="px-4 py-6 text-center text-xs text-muted-foreground">اعلانی وجود ندارد</div>
            <div v-else>
              <div v-for="n in recentNotifs" :key="n.id" class="flex gap-3 border-b border-border px-4 py-3 cursor-pointer" :class="n.read ? 'bg-background' : 'bg-maroon/5'" @click="notifStore.markRead(n.id)">
                <span class="shrink-0 text-base">{{ NOTIF_ICON[n.type] || 'ℹ️' }}</span>
                <div class="min-w-0 flex-1">
                  <div class="text-xs font-medium line-clamp-1">{{ n.title }}</div>
                  <div v-if="n.body" class="mt-0.5 text-[11px] text-muted-foreground line-clamp-2">{{ n.body }}</div>
                  <div class="mt-1 text-[10px] text-muted-foreground">{{ n.date }}</div>
                </div>
              </div>
            </div>
            <RouterLink to="/account" class="block px-4 py-2.5 text-center text-xs text-maroon hover:bg-muted/30" @click="closeNotif">مشاهده همه</RouterLink>
          </div>
        </div>
        <template v-if="authStore.isLoggedIn">
          <div class="hidden md:flex items-center gap-2">
            <RouterLink to="/account" class="flex items-center gap-1.5 text-xs text-muted-foreground hover:text-maroon"><User class="h-4 w-4" />{{ authStore.user?.name?.split(' ')[0] }}</RouterLink>
            <button @click="authStore.logout()" class="text-muted-foreground hover:text-maroon"><LogOut class="h-4 w-4" /></button>
          </div>
        </template>
        <RouterLink v-else to="/auth" class="hidden text-xs text-muted-foreground hover:text-maroon md:block">ورود</RouterLink>
        <button class="md:hidden" @click="open = !open"><X v-if="open" class="h-5 w-5" /><Menu v-else class="h-5 w-5" /></button>
      </div>
    </div>
    <div v-if="open" class="border-t border-border bg-background md:hidden">
      <nav class="flex flex-col px-6 py-4">
        <RouterLink v-for="l in links" :key="l.to" :to="l.to" @click="open = false" class="py-3 text-sm text-muted-foreground hover:text-maroon">{{ l.label }}</RouterLink>
        <template v-if="authStore.isLoggedIn">
          <RouterLink to="/account" @click="open = false" class="py-3 text-sm text-maroon">حساب من</RouterLink>
          <button @click="authStore.logout(); open = false" class="py-3 text-sm text-right text-muted-foreground hover:text-maroon">خروج</button>
        </template>
        <RouterLink v-else to="/auth" @click="open = false" class="py-3 text-sm text-maroon">ورود / ثبت‌نام</RouterLink>
      </nav>
    </div>
  </header>

  <!-- ── Variant 2: Two-Row ──────────────────────────────────── -->
  <header v-else-if="v === 2" class="sticky top-0 z-50 border-b border-border bg-background/90 backdrop-blur-md">
    <div class="mx-auto flex h-14 max-w-7xl items-center justify-between px-6">
      <div class="flex items-center gap-3">
        <button @click="searchOpen = true" class="text-muted-foreground hover:text-maroon transition-colors"><Search class="h-5 w-5" /></button>
        <RouterLink to="/wishlist" class="relative text-muted-foreground hover:text-maroon transition-colors">
          <Heart class="h-5 w-5" :class="wishlistStore.count > 0 ? 'fill-maroon text-maroon' : ''" />
          <span v-if="wishlistStore.count > 0" class="absolute -top-1.5 -left-1.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-maroon px-0.5 text-[9px] text-white">{{ toFa(wishlistStore.count) }}</span>
        </RouterLink>
      </div>
      <RouterLink to="/" class="absolute right-1/2 translate-x-1/2 text-xl font-medium tracking-tight">
        نـوار<span class="text-maroon">.</span>
      </RouterLink>
      <div class="flex items-center gap-3">
        <RouterLink to="/cart" class="relative text-muted-foreground hover:text-maroon transition-colors">
          <ShoppingBag class="h-5 w-5" />
          <span v-if="cartStore.count > 0" class="absolute -top-1.5 -left-1.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-maroon px-0.5 text-[9px] text-maroon-foreground">{{ toFa(cartStore.count) }}</span>
        </RouterLink>
        <RouterLink v-if="authStore.isLoggedIn" to="/account" class="text-muted-foreground hover:text-maroon"><User class="h-5 w-5" /></RouterLink>
        <RouterLink v-else to="/auth" class="text-xs text-muted-foreground hover:text-maroon">ورود</RouterLink>
        <button class="md:hidden" @click="open = !open"><X v-if="open" class="h-5 w-5" /><Menu v-else class="h-5 w-5" /></button>
      </div>
    </div>
    <div class="hidden border-t border-border md:block">
      <nav class="mx-auto flex max-w-7xl items-center justify-center gap-8 py-2.5">
        <RouterLink v-for="l in links" :key="l.to" :to="l.to"
          :class="['text-xs transition-colors uppercase tracking-widest', isActive(l) ? 'text-maroon' : 'text-muted-foreground hover:text-foreground']">
          {{ l.label }}
        </RouterLink>
      </nav>
    </div>
    <div v-if="open" class="border-t border-border bg-background md:hidden">
      <nav class="flex flex-col px-6 py-4">
        <RouterLink v-for="l in links" :key="l.to" :to="l.to" @click="open = false" class="py-3 text-sm text-muted-foreground hover:text-maroon">{{ l.label }}</RouterLink>
        <RouterLink v-if="!authStore.isLoggedIn" to="/auth" @click="open = false" class="py-3 text-sm text-maroon">ورود / ثبت‌نام</RouterLink>
      </nav>
    </div>
  </header>

  <!-- ── Variant 3: Pill Nav ──────────────────────────────────── -->
  <header v-else-if="v === 3" class="sticky top-0 z-50 bg-background/80 backdrop-blur-lg">
    <div class="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
      <RouterLink to="/" class="text-lg font-medium">نـوار<span class="text-maroon">.</span></RouterLink>
      <nav class="hidden items-center gap-1 md:flex bg-muted/60 rounded-full px-2 py-1.5 border border-border">
        <RouterLink v-for="l in links" :key="l.to" :to="l.to"
          :class="['px-4 py-1.5 text-xs rounded-full transition-all', isActive(l) ? 'bg-maroon text-white' : 'text-muted-foreground hover:bg-background hover:text-foreground']">
          {{ l.label }}
        </RouterLink>
      </nav>
      <div class="flex items-center gap-3">
        <button @click="searchOpen = true" class="flex h-9 w-9 items-center justify-center rounded-full border border-border bg-background text-muted-foreground hover:border-maroon hover:text-maroon transition-colors">
          <Search class="h-4 w-4" />
        </button>
        <RouterLink to="/wishlist" class="relative flex h-9 w-9 items-center justify-center rounded-full border border-border bg-background text-muted-foreground hover:border-maroon hover:text-maroon transition-colors">
          <Heart class="h-4 w-4" :class="wishlistStore.count > 0 ? 'fill-maroon text-maroon' : ''" />
          <span v-if="wishlistStore.count > 0" class="absolute -top-1 -left-1 flex h-4 min-w-4 items-center justify-center rounded-full bg-maroon text-[9px] text-white">{{ toFa(wishlistStore.count) }}</span>
        </RouterLink>
        <RouterLink to="/cart" class="relative flex h-9 items-center gap-2 rounded-full bg-maroon px-4 text-xs text-white hover:opacity-90 transition-opacity">
          <ShoppingBag class="h-4 w-4" />
          <span v-if="cartStore.count > 0">{{ toFa(cartStore.count) }}</span>
          <span v-else>سبد</span>
        </RouterLink>
        <RouterLink v-if="authStore.isLoggedIn" to="/account" class="flex h-9 w-9 items-center justify-center rounded-full bg-muted text-muted-foreground hover:bg-maroon/10 hover:text-maroon transition-colors"><User class="h-4 w-4" /></RouterLink>
        <RouterLink v-else to="/auth" class="hidden text-xs text-muted-foreground hover:text-maroon md:block">ورود</RouterLink>
        <button class="md:hidden" @click="open = !open"><X v-if="open" class="h-5 w-5" /><Menu v-else class="h-5 w-5" /></button>
      </div>
    </div>
    <div class="h-px w-full bg-border" />
    <div v-if="open" class="border-t border-border bg-background md:hidden">
      <nav class="flex flex-col px-6 py-4">
        <RouterLink v-for="l in links" :key="l.to" :to="l.to" @click="open = false" class="py-3 text-sm text-muted-foreground hover:text-maroon">{{ l.label }}</RouterLink>
        <RouterLink v-if="!authStore.isLoggedIn" to="/auth" @click="open = false" class="py-3 text-sm text-maroon">ورود / ثبت‌نام</RouterLink>
      </nav>
    </div>
  </header>

  <!-- ── Variant 4: Bold ──────────────────────────────────── -->
  <header v-else class="sticky top-0 z-50">
    <div class="bg-maroon px-6 py-2.5">
      <div class="mx-auto flex max-w-7xl items-center justify-between">
        <RouterLink to="/" class="text-2xl font-light tracking-tight text-white">
          نـوار<span class="opacity-60">.</span>
        </RouterLink>
        <div class="flex items-center gap-4">
          <button @click="searchOpen = true" class="text-white/70 hover:text-white transition-colors"><Search class="h-5 w-5" /></button>
          <RouterLink to="/wishlist" class="relative text-white/70 hover:text-white transition-colors">
            <Heart class="h-5 w-5" :class="wishlistStore.count > 0 ? 'fill-white text-white' : ''" />
            <span v-if="wishlistStore.count > 0" class="absolute -top-1.5 -left-1.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-white px-0.5 text-[9px] text-maroon">{{ toFa(wishlistStore.count) }}</span>
          </RouterLink>
          <RouterLink to="/cart" class="relative text-white/70 hover:text-white transition-colors">
            <ShoppingBag class="h-5 w-5" />
            <span v-if="cartStore.count > 0" class="absolute -top-1.5 -left-1.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-white px-0.5 text-[9px] text-maroon">{{ toFa(cartStore.count) }}</span>
          </RouterLink>
          <RouterLink v-if="!authStore.isLoggedIn" to="/auth" class="text-xs text-white/70 hover:text-white">ورود</RouterLink>
          <RouterLink v-else to="/account" class="text-white/70 hover:text-white"><User class="h-5 w-5" /></RouterLink>
          <button class="md:hidden text-white" @click="open = !open"><X v-if="open" class="h-5 w-5" /><Menu v-else class="h-5 w-5" /></button>
        </div>
      </div>
    </div>
    <div class="border-b border-border bg-background/95 backdrop-blur-md hidden md:block">
      <nav class="mx-auto flex max-w-7xl items-center gap-0 px-6">
        <RouterLink v-for="l in links" :key="l.to" :to="l.to"
          :class="['px-5 py-3 text-sm transition-colors border-b-2', isActive(l) ? 'border-maroon text-maroon' : 'border-transparent text-muted-foreground hover:text-foreground hover:border-border']">
          {{ l.label }}
        </RouterLink>
      </nav>
    </div>
    <div v-if="open" class="border-b border-border bg-background md:hidden">
      <nav class="flex flex-col px-6 py-4">
        <RouterLink v-for="l in links" :key="l.to" :to="l.to" @click="open = false" class="py-3 text-sm text-muted-foreground hover:text-maroon">{{ l.label }}</RouterLink>
        <RouterLink v-if="!authStore.isLoggedIn" to="/auth" @click="open = false" class="py-3 text-sm text-maroon">ورود / ثبت‌نام</RouterLink>
      </nav>
    </div>
  </header>

  <SearchModal v-if="searchOpen" @close="searchOpen = false" />
</template>
