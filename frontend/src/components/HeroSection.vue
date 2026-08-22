<script setup>
import { computed, defineAsyncComponent, shallowRef, watch } from "vue";
import { useRoute } from "vue-router";
import { DESIGN_THEMES, useLayoutStore } from "@/stores/layout.js";

defineProps({
  image:    { type: String, default: null },
  title:    { type: String, default: "" },
  subtitle: { type: String, default: "" },
  eyebrow:  { type: String, default: "مجموعه ۱۴۰۳" },
  ctaLabel: { type: String, default: "مشاهده محصولات" },
});

const route = useRoute();
const layoutStore = useLayoutStore();
const themeKey = computed(() => {
  const key = layoutStore.getComponentTheme("hero", route.path);
  return DESIGN_THEMES[key] ? key : "minimal";
});

const map = {
  minimal: () => import("@/themes/default/HeroSection.vue"),
  bento: () => import("@/themes/default/HeroSection.vue"),
  modern: () => import("@/themes/default/HeroSection.vue"),
  dark: () => import("@/themes/dark/HeroSection.vue"),
  earthy: () => import("@/themes/earthy/HeroSection.vue"),
  scandinavian: () => import("@/themes/default/HeroSection.vue"),
  swiss: () => import("@/themes/default/HeroSection.vue"),
  glass: () => import("@/themes/glass/HeroSection.vue"),
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
