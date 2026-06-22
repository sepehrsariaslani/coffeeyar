<script setup>
import { computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useCategoriesStore } from "@/stores/categories.js";

const router = useRouter();
const route = useRoute();
const categoriesStore = useCategoriesStore();

const categories = computed(() => categoriesStore.roots);

// Hide on products page (it has its own category tabs)
const showBar = computed(() => route.path !== "/products");

function goToCategory(cat) {
  router.push(`/products?category=${cat.slug}`);
}
</script>

<template>
  <div
    v-if="categories.length && showBar"
    class="sticky top-0 z-40 border-b border-border bg-background/95 backdrop-blur-md"
  >
    <nav
      class="mx-auto flex max-w-7xl items-center gap-1 overflow-x-auto px-4 py-2 md:px-6 md:flex-wrap md:gap-2 md:overflow-visible md:py-2.5"
    >
      <button
        v-for="cat in categories"
        :key="cat.id"
        type="button"
        @click="goToCategory(cat)"
        class="shrink-0 inline-flex items-center gap-1.5 rounded-full border border-border px-3.5 py-1.5 text-xs text-muted-foreground transition-colors hover:border-maroon hover:text-maroon md:px-4 md:text-sm"
      >
        <span class="text-sm">{{ cat.icon }}</span>
        <span class="font-[Vazirmatn]">{{ cat.name }}</span>
      </button>
    </nav>
  </div>
</template>
