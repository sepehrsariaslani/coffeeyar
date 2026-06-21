<template>
  <section v-if="items.length" class="dk-featured">
    <div class="dk-featured__grid">
      <RouterLink v-for="item in displayItems" :key="item.id" :to="`/products/${item.id}`" class="dk-featured__item">
        <div class="dk-featured__media">
          <img v-if="item.image" :src="item.image" :alt="item.name" class="dk-featured__img" />
          <div v-else class="dk-featured__placeholder" />
        </div>
        <div class="dk-featured__info">
          <span class="dk-featured__name">{{ item.name }}</span>
          <span class="dk-featured__arrow">←</span>
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
.dk-featured { padding: 2rem 5vw; }
.dk-featured__grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1px; background-color: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.06); }
@media (max-width: 768px) { .dk-featured__grid { grid-template-columns: repeat(2, 1fr); } }
.dk-featured__item { background-color: #1a1a1a; display: flex; flex-direction: column; text-decoration: none; overflow: hidden; transition: background 0.2s; }
.dk-featured__item:hover { background-color: #1f1f1f; }
.dk-featured__item:hover .dk-featured__img { transform: scale(1.04); filter: brightness(0.95); }
.dk-featured__media { aspect-ratio: 3/4; overflow: hidden; background-color: #111; }
.dk-featured__img { width: 100%; height: 100%; object-fit: contain; padding: 8px; transition: transform 0.5s cubic-bezier(0.25,0.46,0.45,0.94), filter 0.3s; filter: brightness(0.8); }
.dk-featured__placeholder { width: 100%; height: 100%; background: linear-gradient(135deg, #1e1e1e, #161616); }
.dk-featured__info { display: flex; align-items: center; justify-content: space-between; padding: 0.7rem 0.85rem; border-top: 1px solid rgba(255,255,255,0.06); }
.dk-featured__name { font-size: 0.78rem; color: rgba(255,255,255,0.65); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 80%; }
.dk-featured__arrow { font-size: 0.85rem; color: rgba(255,255,255,0.25); transition: transform 0.2s, color 0.2s; }
.dk-featured__item:hover .dk-featured__arrow { transform: translateX(-4px); color: #C9923F; }
</style>
