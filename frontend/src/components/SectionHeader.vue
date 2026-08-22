<script setup>
import { computed, defineAsyncComponent, shallowRef, watch } from "vue";
import { useRoute } from "vue-router";
import { DESIGN_THEMES, useLayoutStore } from "@/stores/layout.js";

defineProps({
  title: { type: String, required: true },
  tag: { type: String, default: null },
  to: { type: String, default: null },
  linkLabel: { type: String, default: "نمایش همه" },
});

const route = useRoute();
const layoutStore = useLayoutStore();
const themeKey = computed(() => {
  const key = layoutStore.getComponentTheme("sectionHeader", route.path);
  return DESIGN_THEMES[key] ? key : "minimal";
});

const map = {
  minimal: () => import("@/themes/default/SectionHeader.vue"),
  bento: () => import("@/themes/default/SectionHeader.vue"),
  modern: () => import("@/themes/default/SectionHeader.vue"),
  dark: () => import("@/themes/dark/SectionHeader.vue"),
  earthy: () => import("@/themes/earthy/SectionHeader.vue"),
  scandinavian: () => import("@/themes/default/SectionHeader.vue"),
  swiss: () => import("@/themes/default/SectionHeader.vue"),
  glass: () => import("@/themes/glass/SectionHeader.vue"),
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
