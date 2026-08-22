<script setup>
import { computed, defineAsyncComponent, shallowRef, watch, watchEffect } from "vue";
import { useRoute } from "vue-router";
import { DESIGN_THEMES, useLayoutStore, applyDesignTheme } from "@/stores/layout.js";

const layoutStore = useLayoutStore();
const route = useRoute();
const themeKey = computed(() => {
  const key = layoutStore.getComponentTheme("layout", route.path);
  return DESIGN_THEMES[key] ? key : "minimal";
});

const map = {
  minimal: () => import("@/themes/default/TheLayout.vue"),
  bento: () => import("@/themes/default/TheLayout.vue"),
  modern: () => import("@/themes/default/TheLayout.vue"),
  dark: () => import("@/themes/dark/TheLayout.vue"),
  earthy: () => import("@/themes/earthy/TheLayout.vue"),
  scandinavian: () => import("@/themes/default/TheLayout.vue"),
  swiss: () => import("@/themes/default/TheLayout.vue"),
  glass: () => import("@/themes/glass/TheLayout.vue"),
};

const Impl = shallowRef(defineAsyncComponent(map[themeKey.value]));
watch(themeKey, (key) => {
  Impl.value = defineAsyncComponent(map[key]);
});

// Apply the page-level design to document chrome. Per-component overrides
// are rendered in their own design scopes by the child resolvers.
watchEffect(() => {
  applyDesignTheme(layoutStore.getEffectiveDesign(route.path));
});
</script>

<template>
  <div class="design-component-scope" :data-design-theme="themeKey">
    <Suspense>
      <component :is="Impl">
        <template v-for="(_, name) in $slots" #[name]="slotProps">
          <slot :name="name" v-bind="slotProps || {}" />
        </template>
      </component>
    </Suspense>
  </div>
</template>
