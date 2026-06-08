<template>
  <header class="dk-sh">
    <div class="dk-sh__left">
      <span v-if="tag" class="dk-sh__tag">{{ tag }}</span>
      <h2 class="dk-sh__title">{{ title }}</h2>
    </div>
    <RouterLink v-if="to" :to="to" class="dk-sh__link">
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
.dk-sh { display: flex; align-items: flex-end; justify-content: space-between; padding: 3.5rem 5vw 1.5rem; border-bottom: 1px solid rgba(255,255,255,0.07); }
.dk-sh__left { display: flex; flex-direction: column; gap: 0.35rem; }
.dk-sh__tag { font-size: 0.68rem; letter-spacing: 0.18em; text-transform: uppercase; color: #C9923F; font-weight: 500; }
.dk-sh__title { font-size: clamp(1.3rem, 2.5vw, 1.8rem); font-weight: 300; color: rgba(255,255,255,0.88); margin: 0; letter-spacing: -0.01em; }
.dk-sh__link { display: inline-flex; align-items: center; gap: 0.4rem; font-size: 0.78rem; color: #C9923F; text-decoration: none; padding-bottom: 1px; border-bottom: 1px solid transparent; transition: border-color 0.2s; }
.dk-sh__link:hover { border-bottom-color: #C9923F; }
</style>
