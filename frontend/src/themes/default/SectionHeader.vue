<template>
  <header class="section-header">
    <div class="section-header__left">
      <span v-if="tag" class="section-header__tag">{{ tag }}</span>
      <h2 class="section-header__title">{{ title }}</h2>
    </div>
    <RouterLink v-if="to" :to="to" class="section-header__link">
      {{ linkLabel }}
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M10 7H4M7 4L4 7L7 10" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </RouterLink>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'
defineProps({
  title: { type: String, required: true },
  tag: { type: String, default: null },
  to: { type: String, default: null },
  linkLabel: { type: String, default: 'نمایش همه' },
})
</script>

<style scoped>
.section-header { display: flex; align-items: flex-end; justify-content: space-between; padding: 3.5rem 5vw 1.5rem; border-bottom: 1px solid #E8E4DE; }
.section-header__left { display: flex; flex-direction: column; gap: 0.35rem; }
.section-header__tag { font-size: 0.7rem; letter-spacing: 0.2em; text-transform: uppercase; color: #9e9890; font-family: 'Vazirmatn', sans-serif; }
.section-header__title { font-family: 'Vazirmatn', sans-serif; font-size: clamp(1.3rem, 2.5vw, 1.8rem); font-weight: 300; color: #111; margin: 0; letter-spacing: -0.01em; }
.section-header__link { display: inline-flex; align-items: center; gap: 0.4rem; font-family: 'Vazirmatn', sans-serif; font-size: 0.8rem; letter-spacing: 0.08em; color: #800000; text-decoration: none; padding-bottom: 1px; border-bottom: 1px solid transparent; transition: border-color 0.2s; }
.section-header__link:hover { border-bottom-color: #800000; }
</style>
