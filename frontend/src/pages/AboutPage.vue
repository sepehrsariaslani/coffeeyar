<template>
  <main class="page-wrap content-page">
    <h1>{{ page?.hero_title || page?.title || 'درباره ما' }}</h1>
    <p v-if="page?.hero_subtitle">{{ page.hero_subtitle }}</p>
    <div v-if="page?.body_html" v-html="page.body_html"></div>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { api } from '@/utils/api'

const page = ref(null)

onMounted(async () => {
  page.value = await api.getSitePage('about-us').catch(() => null)
})
</script>
