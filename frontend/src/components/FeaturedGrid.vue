<script setup>
import { shallowRef, watch, defineAsyncComponent } from 'vue'
import { useThemeStore } from '@/stores/theme.js'

defineProps({
  items: { type: Array, default: () => [] },
})

const store = useThemeStore()
const map = {
  '':             () => import('@/themes/default/FeaturedGrid.vue'),
  'dark':         () => import('@/themes/dark/FeaturedGrid.vue'),
  'theme-earthy': () => import('@/themes/earthy/FeaturedGrid.vue'),
  'theme-glass':  () => import('@/themes/glass/FeaturedGrid.vue'),
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
