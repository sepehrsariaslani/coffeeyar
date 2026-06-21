<template>
  <section v-if="items.length" class="ea-featured">
    <div class="ea-featured__grid">
      <RouterLink v-for="item in displayItems" :key="item.id" :to="`/products/${item.id}`" class="ea-featured__item">
        <div class="ea-featured__media">
          <img v-if="item.image" :src="item.image" :alt="item.name" class="ea-featured__img" />
          <div v-else class="ea-featured__placeholder" />
        </div>
        <div class="ea-featured__info">
          <span class="ea-featured__name">{{ item.name }}</span>
          <span class="ea-featured__arrow">←</span>
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
.ea-featured { padding: 2rem 5vw; }
.ea-featured__grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; }
@media (max-width: 768px) { .ea-featured__grid { grid-template-columns: repeat(2, 1fr); } }
.ea-featured__item { background-color: #FDFAF5; border: 1.5px solid #D6CBB8; border-radius: 12px; display: flex; flex-direction: column; text-decoration: none; overflow: hidden; transition: transform 0.22s, box-shadow 0.22s; }
.ea-featured__item:hover { transform: translateY(-4px); box-shadow: 0 10px 28px rgba(45,36,22,0.10); }
.ea-featured__item:hover .ea-featured__img { transform: scale(1.04); }
.ea-featured__media { aspect-ratio: 3/4; overflow: hidden; background-color: #EDE5D6; }
.ea-featured__img { width: 100%; height: 100%; object-fit: contain; padding: 8px; transition: transform 0.5s cubic-bezier(0.25,0.46,0.45,0.94); }
.ea-featured__placeholder { width: 100%; height: 100%; background: linear-gradient(135deg, #E8DFC9, #DDD3BC); }
.ea-featured__info { display: flex; align-items: center; justify-content: space-between; padding: 0.65rem 0.85rem; border-top: 1.5px solid #D6CBB8; }
.ea-featured__name { font-size: 0.78rem; color: #2d2416; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 80%; font-weight: 500; }
.ea-featured__arrow { font-size: 0.85rem; color: #9e8a72; transition: transform 0.2s, color 0.2s; }
.ea-featured__item:hover .ea-featured__arrow { transform: translateX(-4px); color: #4a7c59; }
</style>
