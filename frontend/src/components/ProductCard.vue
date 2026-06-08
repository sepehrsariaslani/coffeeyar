<script setup>
import { shallowRef, watch, defineAsyncComponent } from 'vue'
import { useThemeStore } from '@/stores/theme.js'

defineProps({
  product: { type: Object, required: true },
  variant: { type: String, default: null },
})

const store = useThemeStore()
const map = {
  '':             () => import('@/themes/default/ProductCard.vue'),
  'dark':         () => import('@/themes/dark/ProductCard.vue'),
  'theme-earthy': () => import('@/themes/earthy/ProductCard.vue'),
  'theme-glass':  () => import('@/themes/glass/ProductCard.vue'),
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
