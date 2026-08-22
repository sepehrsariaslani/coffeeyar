<template>
  <header class="gl-sh">
    <div class="gl-sh__left">
      <span v-if="tag" class="gl-sh__tag">{{ tag }}</span>
      <h2 class="gl-sh__title">{{ title }}</h2>
    </div>
    <RouterLink v-if="to" :to="to" class="gl-sh__link">
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
.gl-sh {
  display: flex; align-items: flex-end; justify-content: space-between;
  padding: 3rem 5vw 1.25rem;
}
.gl-sh__left { display: flex; flex-direction: column; gap: 0.4rem; }
.gl-sh__tag {
  display: inline-block;
  font-size: 0.65rem; letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--maroon, #8a5a44); font-weight: 600;
  background: rgba(255,255,255,0.55);
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.7);
  padding: 0.2rem 0.7rem; border-radius: 9999px;
  width: fit-content;
}
.gl-sh__title {
  font-size: clamp(1.3rem, 2.5vw, 1.8rem);
  font-weight: 300; color: var(--foreground, #3d2f26);
  margin: 0; letter-spacing: -0.015em;
}
.gl-sh__link {
  display: inline-flex; align-items: center; gap: 0.4rem;
  font-size: 0.78rem; font-weight: 500;
  color: var(--maroon, #8a5a44);
  text-decoration: none;
  padding: 0.3rem 0.85rem;
  background: rgba(255,255,255,0.52);
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.7);
  border-radius: 9999px;
  transition: all 0.2s;
}
.gl-sh__link:hover {
  background: rgba(255,255,255,0.75);
  color: var(--maroon, #6f4635);
}
</style>
