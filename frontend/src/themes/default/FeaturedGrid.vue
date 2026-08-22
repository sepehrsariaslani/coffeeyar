<template>
  <section v-if="items.length" class="featured">
    <div class="featured__grid">
      <RouterLink v-for="(item, i) in displayItems" :key="item.id" :to="`/products/${item.id}`" class="featured__item" :class="`featured__item--${i}`">
        <div class="featured__media">
          <img v-if="item.image" :src="item.image" :alt="item.name" class="featured__img" />
          <div v-else class="featured__placeholder" />
        </div>
        <div class="featured__info">
          <span class="featured__name">{{ item.name }}</span>
          <span class="featured__arrow">←</span>
        </div>
      </RouterLink>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
const props = defineProps({ items: { type: Array, default: () => [] } })
const displayItems = computed(() => props.items.slice(0, 4))
</script>

<style scoped>
.featured { padding: 0 5vw; margin: 2.5rem 0; }
.featured__grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1px; background-color: var(--border, #E8E4DE); border: 1px solid var(--border, #E8E4DE); }
@media (max-width: 768px) { .featured__grid { grid-template-columns: repeat(2, 1fr); } }
.featured__item { background-color: var(--card, #FAFAF8); display: flex; flex-direction: column; text-decoration: none; overflow: hidden; position: relative; }
.featured__item:hover .featured__img { transform: scale(1.04); }
.featured__media { aspect-ratio: 3/4; overflow: hidden; background-color: var(--muted, #F0EDE8); }
.featured__img { width: 100%; height: 100%; object-fit: contain; padding: 8px; transition: transform 0.5s cubic-bezier(0.25,0.46,0.45,0.94); }
.featured__placeholder { width: 100%; height: 100%; background: linear-gradient(135deg, var(--muted, #EDE9E4), #E0DBD5); }
.featured__info { display: flex; align-items: center; justify-content: space-between; padding: 0.75rem 0.85rem; border-top: 1px solid var(--border, #E8E4DE); }
.featured__name { font-size: 0.78rem; color: var(--foreground, #1a1a1a); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 80%; }
.featured__arrow { font-size: 0.85rem; color: var(--muted-foreground, #9e9890); transition: transform 0.2s; }
.featured__item:hover .featured__arrow { transform: translateX(-4px); color: var(--maroon, #800000); }
</style>
