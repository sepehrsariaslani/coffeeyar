<script setup>
import { computed, defineAsyncComponent, shallowRef, watch } from "vue";
import { useRoute } from "vue-router";
import { DESIGN_THEMES, useLayoutStore } from "@/stores/layout.js";

defineProps({
  product: { type: Object, required: true },
  variant: { type: String, default: null },
});

const route = useRoute();
const layoutStore = useLayoutStore();
const themeKey = computed(() => {
  const key = layoutStore.getComponentTheme("productCard", route.path);
  return DESIGN_THEMES[key] ? key : "minimal";
});

const map = {
  minimal: () => import("@/themes/default/ProductCard.vue"),
  bento: () => import("@/themes/default/ProductCard.vue"),
  modern: () => import("@/themes/default/ProductCard.vue"),
  dark: () => import("@/themes/dark/ProductCard.vue"),
  earthy: () => import("@/themes/earthy/ProductCard.vue"),
  scandinavian: () => import("@/themes/default/ProductCard.vue"),
  swiss: () => import("@/themes/default/ProductCard.vue"),
  glass: () => import("@/themes/glass/ProductCard.vue"),
};

const Impl = shallowRef(defineAsyncComponent(map[themeKey.value]));
watch(themeKey, (key) => {
  Impl.value = defineAsyncComponent(map[key]);
});
</script>

<template>
  <div class="design-component-scope" :data-design-theme="themeKey">
    <Suspense>
      <component :is="Impl" v-bind="$props" />
    </Suspense>
  </div>
</template>
