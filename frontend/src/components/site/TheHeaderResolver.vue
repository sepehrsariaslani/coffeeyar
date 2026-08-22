<script setup>
import { computed, defineAsyncComponent, shallowRef, watch } from "vue";
import { useRoute } from "vue-router";
import { DESIGN_THEMES, useLayoutStore } from "@/stores/layout.js";

const route = useRoute();
const layoutStore = useLayoutStore();
const themeKey = computed(() => {
  const key = layoutStore.getComponentTheme("header", route.path);
  return DESIGN_THEMES[key] ? key : "minimal";
});

const map = {
  minimal: () => import("@/components/site/TheHeader.vue"),
  bento: () => import("@/components/site/TheHeader.vue"),
  modern: () => import("@/components/site/TheHeader.vue"),
  dark: () => import("@/themes/dark/TheHeader.vue"),
  earthy: () => import("@/themes/earthy/TheHeader.vue"),
  scandinavian: () => import("@/components/site/TheHeader.vue"),
  swiss: () => import("@/components/site/TheHeader.vue"),
  glass: () => import("@/themes/glass/TheHeader.vue"),
};

const Impl = shallowRef(defineAsyncComponent(map[themeKey.value]));
watch(themeKey, (key) => {
  Impl.value = defineAsyncComponent(map[key]);
});
</script>

<template>
  <div class="design-component-scope" :data-design-theme="themeKey">
    <Suspense>
      <component :is="Impl" v-bind="$attrs" />
    </Suspense>
  </div>
</template>
