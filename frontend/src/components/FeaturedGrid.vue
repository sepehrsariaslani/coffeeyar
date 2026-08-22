<script setup>
import { computed, defineAsyncComponent, shallowRef, watch } from "vue";
import { useRoute } from "vue-router";
import { DESIGN_THEMES, useLayoutStore } from "@/stores/layout.js";

defineProps({
  items: { type: Array, default: () => [] },
});

const route = useRoute();
const layoutStore = useLayoutStore();
const themeKey = computed(() => {
  const key = layoutStore.getComponentTheme("featuredGrid", route.path);
  return DESIGN_THEMES[key] ? key : "minimal";
});

const map = {
  minimal: () => import("@/themes/default/FeaturedGrid.vue"),
  bento: () => import("@/themes/default/FeaturedGrid.vue"),
  modern: () => import("@/themes/default/FeaturedGrid.vue"),
  dark: () => import("@/themes/dark/FeaturedGrid.vue"),
  earthy: () => import("@/themes/earthy/FeaturedGrid.vue"),
  scandinavian: () => import("@/themes/default/FeaturedGrid.vue"),
  swiss: () => import("@/themes/default/FeaturedGrid.vue"),
  glass: () => import("@/themes/glass/FeaturedGrid.vue"),
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
