<script setup>
import { shallowRef, watch, watchEffect, defineAsyncComponent } from 'vue'
import { useRoute } from 'vue-router'
import { useThemeStore } from '@/stores/theme.js'
import { useLayoutStore, applyDesignTheme } from '@/stores/layout.js'

const store = useThemeStore()
const layoutStore = useLayoutStore()
const route = useRoute()

const map = {
  '':             () => import('@/themes/default/TheLayout.vue'),
  'dark':         () => import('@/themes/dark/TheLayout.vue'),
  'theme-earthy': () => import('@/themes/earthy/TheLayout.vue'),
  'theme-glass':  () => import('@/themes/glass/TheLayout.vue'),
}
const Impl = shallowRef(defineAsyncComponent(map[store.theme.themeClass] ?? map['']))
watch(() => store.theme.themeClass, cls => {
  Impl.value = defineAsyncComponent(map[cls] ?? map[''])
})

watchEffect(() => {
  applyDesignTheme(layoutStore.getEffectiveDesign(route.path))
})
</script>

<template>
  <Suspense>
    <component :is="Impl">
      <template v-for="(_, name) in $slots" #[name]="slotProps">
        <slot :name="name" v-bind="slotProps || {}" />
      </template>
    </component>
  </Suspense>
</template>
