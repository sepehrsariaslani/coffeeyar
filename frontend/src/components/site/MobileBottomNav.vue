<script setup>
import { computed } from "vue";
import { useRoute, RouterLink } from "vue-router";
import { Home, Package, ShoppingBag, BookOpen, User } from "lucide-vue-next";
import { useCartStore } from "@/stores/cart.js";

const route = useRoute();
const cartStore = useCartStore();

const navItems = [
  { to: "/", label: "خانه", icon: Home, exact: true },
  { to: "/products", label: "محصولات", icon: Package },
  { to: "/cart", label: "سبد", icon: ShoppingBag },
  { to: "/blog", label: "بلاگ", icon: BookOpen },
  { to: "/account", label: "حساب من", icon: User },
];

function isActive(item) {
  if (item.exact) return route.path === item.to;
  return route.path.startsWith(item.to);
}

const isAdmin = computed(() => route.path.startsWith("/admin"));
</script>

<template>
  <nav
    v-if="!isAdmin"
    class="fixed bottom-0 left-0 right-0 z-50 border-t border-border bg-background/95 backdrop-blur-md md:hidden"
    :style="{ paddingBottom: 'env(safe-area-inset-bottom)' }"
  >
    <div class="flex">
      <RouterLink
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        :class="[
          'relative flex flex-1 flex-col items-center gap-1 py-2.5 text-center transition-colors',
          isActive(item) ? 'text-maroon' : 'text-muted-foreground',
        ]"
      >
        <div class="relative">
          <component :is="item.icon" class="h-5 w-5" />
          <span
            v-if="item.to === '/cart' && cartStore.count > 0"
            class="absolute -top-1.5 -right-1.5 flex h-4 w-4 items-center justify-center rounded-full bg-maroon text-[9px] font-bold text-maroon-foreground"
          >
            {{ cartStore.count > 9 ? "+۹" : cartStore.count }}
          </span>
        </div>
        <span class="text-[10px]">{{ item.label }}</span>
        <span
          v-if="isActive(item)"
          class="absolute bottom-0 left-1/2 h-0.5 w-8 -translate-x-1/2 bg-maroon"
        />
      </RouterLink>
    </div>
  </nav>
</template>
