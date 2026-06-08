<script setup>
import { computed } from "vue";
import { RouterLink } from "vue-router";
import { Heart, ShoppingBag } from "lucide-vue-next";
import TheLayout from "@/components/site/TheLayout.vue";
import SectionHeader from "@/components/SectionHeader.vue";
import ProductCard from "@/components/ProductCard.vue";
import { useWishlistStore } from "@/stores/wishlist.js";
import { products } from "@/lib/data.js";
import { useSeo } from "@/composables/useSeo.js";

useSeo({ title: "علاقه‌مندی‌ها", description: "محصولات موردعلاقه شما در نوار" });

const wishlistStore = useWishlistStore();

const wishlisted = computed(() =>
  products.filter((p) => wishlistStore.ids.includes(p.id))
);
</script>

<template>
  <TheLayout>
    <section class="border-b border-border">
      <div class="mx-auto max-w-7xl px-6 py-12">
        <span class="text-xs uppercase tracking-[0.3em] text-maroon">مجموعه شما</span>
        <h1 class="mt-3 text-4xl font-light">علاقه‌مندی‌ها</h1>
        <p class="mt-2 text-sm text-muted-foreground">
          {{ wishlisted.length ? `${wishlisted.length} محصول ذخیره‌شده` : "هنوز محصولی ذخیره نشده" }}
        </p>
      </div>
    </section>

    <!-- Empty state -->
    <section v-if="wishlisted.length === 0" class="flex flex-col items-center justify-center px-6 py-32 text-center">
      <div class="flex h-20 w-20 items-center justify-center rounded-full border border-dashed border-border">
        <Heart class="h-8 w-8 text-muted-foreground/50" />
      </div>
      <h2 class="mt-6 text-xl font-light">لیست علاقه‌مندی‌ها خالی است</h2>
      <p class="mt-2 max-w-xs text-sm leading-7 text-muted-foreground">
        روی آیکون قلب روی هر محصول کلیک کنید تا اینجا ذخیره شود.
      </p>
      <RouterLink
        to="/products"
        class="mt-8 inline-flex items-center gap-2 border-b border-maroon pb-0.5 text-sm text-maroon transition-[gap] hover:gap-3"
      >
        مشاهده همه محصولات
        <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
          <path d="M12 8H4M8 4L4 8L8 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </RouterLink>
    </section>

    <!-- Product grid -->
    <section v-else class="px-[5vw] py-12">
      <div class="wishlist-grid">
        <ProductCard v-for="p in wishlisted" :key="p.id" :product="p" />
      </div>

      <div class="mt-12 flex items-center justify-between border-t border-border pt-8">
        <RouterLink to="/products" class="text-sm text-muted-foreground hover:text-maroon">
          ادامه خرید
        </RouterLink>
        <RouterLink to="/cart" class="inline-flex items-center gap-2 bg-maroon px-6 py-3 text-sm text-white hover:opacity-90">
          <ShoppingBag class="h-4 w-4" />
          مشاهده سبد خرید
        </RouterLink>
      </div>
    </section>
  </TheLayout>
</template>

<style scoped>
.wishlist-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2.5rem 1.5rem;
}
@media (max-width: 1024px) { .wishlist-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 768px) { .wishlist-grid { grid-template-columns: repeat(2, 1fr); gap: 1.5rem 1rem; } }
</style>
