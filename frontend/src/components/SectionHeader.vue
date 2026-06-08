<script setup>
import { shallowRef, watch, defineAsyncComponent } from 'vue'
import { useThemeStore } from '@/stores/theme.js'

defineProps({
  title: { type: String, required: true },
  tag: { type: String, default: null },
  to: { type: String, default: null },
  linkLabel: { type: String, default: 'نمایش همه' },
})

const store = useThemeStore()
const map = {
  '':             () => import('@/themes/default/SectionHeader.vue'),
  'dark':         () => import('@/themes/dark/SectionHeader.vue'),
  'theme-earthy': () => import('@/themes/earthy/SectionHeader.vue'),
  'theme-glass':  () => import('@/themes/glass/SectionHeader.vue'),
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
