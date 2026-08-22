<script setup>
import { computed, defineAsyncComponent, shallowRef, watch } from "vue";
import { useRoute } from "vue-router";
import { DESIGN_THEMES, useLayoutStore } from "@/stores/layout.js";

const route = useRoute();
const layoutStore = useLayoutStore();
const themeKey = computed(() => {
  const key = layoutStore.getComponentTheme("footer", route.path);
  return DESIGN_THEMES[key] ? key : "minimal";
});

const map = {
  minimal: () => import("@/components/site/TheFooter.vue"),
  bento: () => import("@/components/site/TheFooter.vue"),
  modern: () => import("@/components/site/TheFooter.vue"),
  dark: () => import("@/themes/dark/TheFooter.vue"),
  earthy: () => import("@/themes/earthy/TheFooter.vue"),
  scandinavian: () => import("@/components/site/TheFooter.vue"),
  swiss: () => import("@/components/site/TheFooter.vue"),
  glass: () => import("@/themes/glass/TheFooter.vue"),
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
