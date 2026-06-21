<template>
  <header class="ea-sh">
    <div class="ea-sh__left">
      <span v-if="tag" class="ea-sh__tag">{{ tag }}</span>
      <h2 class="ea-sh__title">{{ title }}</h2>
    </div>
    <RouterLink v-if="to" :to="to" class="ea-sh__link">
      {{ linkLabel }}
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M10 7H4M7 4L4 7L7 10" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </RouterLink>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'
defineProps({ title: { type: String, required: true }, tag: { type: String, default: null }, to: { type: String, default: null }, linkLabel: { type: String, default: 'نمایش همه' } })
</script>

<style scoped>
.ea-sh { display: flex; align-items: flex-end; justify-content: space-between; padding: 3.5rem 5vw 1.5rem; border-bottom: 1.5px solid #D6CBB8; }
.ea-sh__left { display: flex; flex-direction: column; gap: 0.4rem; }
.ea-sh__tag { display: inline-flex; align-items: center; gap: 0.3rem; font-size: 0.68rem; letter-spacing: 0.15em; text-transform: uppercase; color: #4a7c59; font-weight: 600; background: rgba(74,124,89,0.1); padding: 0.2rem 0.65rem; border-radius: 9999px; width: fit-content; }
.ea-sh__tag::before { content: '🌿'; font-size: 0.75rem; }
.ea-sh__title { font-size: clamp(1.3rem, 2.5vw, 1.8rem); font-weight: 400; color: #2d2416; margin: 0; letter-spacing: -0.01em; }
.ea-sh__link { display: inline-flex; align-items: center; gap: 0.4rem; font-size: 0.78rem; font-weight: 500; color: #4a7c59; text-decoration: none; padding: 0.3rem 0.85rem; background: rgba(74,124,89,0.1); border-radius: 9999px; transition: all 0.2s; }
.ea-sh__link:hover { background: rgba(74,124,89,0.18); }
</style>
