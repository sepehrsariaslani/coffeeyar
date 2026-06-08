<script setup>
import { shallowRef, watch, defineAsyncComponent } from 'vue'
import { useThemeStore } from '@/stores/theme.js'

defineProps({
  image:    { type: String, default: null },
  title:    { type: String, default: '' },
  subtitle: { type: String, default: '' },
})

const store = useThemeStore()
const map = {
  '':             () => import('@/themes/default/HeroSection.vue'),
  'dark':         () => import('@/themes/dark/HeroSection.vue'),
  'theme-earthy': () => import('@/themes/earthy/HeroSection.vue'),
  'theme-glass':  () => import('@/themes/glass/HeroSection.vue'),
}
const Impl = shallowRef(defineAsyncComponent(map[store.theme.themeClass] ?? map['']))
watch(() => store.theme.themeClass, cls => {
  Impl.value = defineAsyncComponent(map[cls] ?? map[''])
})
</script>

<template>
  <Suspense>
    <component :is="Impl" v-bind="$props" />
  </Suspense>
</template>
