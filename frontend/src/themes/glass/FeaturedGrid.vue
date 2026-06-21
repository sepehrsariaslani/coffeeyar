<template>
  <section v-if="items.length" class="gl-featured">
    <div class="gl-featured__grid">
      <RouterLink v-for="(item, i) in displayItems" :key="item.id" :to="`/products/${item.id}`" class="gl-featured__item">
        <div class="gl-featured__media">
          <img v-if="item.image" :src="item.image" :alt="item.name" class="gl-featured__img" />
          <div v-else class="gl-featured__placeholder" />
          <div class="gl-featured__shimmer" />
        </div>
        <div class="gl-featured__info">
          <span class="gl-featured__name">{{ item.name }}</span>
          <span class="gl-featured__arrow">←</span>
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
.gl-featured { padding: 2rem 5vw; }
.gl-featured__grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.75rem;
}
@media (max-width: 768px) { .gl-featured__grid { grid-template-columns: repeat(2, 1fr); } }
.gl-featured__item {
  background: rgba(255,255,255,0.42);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid rgba(255,255,255,0.65);
  border-radius: 16px;
  overflow: hidden;
  text-decoration: none;
  display: flex; flex-direction: column;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.75), 0 4px 16px rgba(100,60,220,0.08);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.gl-featured__item:hover {
  transform: translateY(-4px);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.75), 0 12px 32px rgba(100,60,220,0.16);
}
.gl-featured__media { aspect-ratio: 3/4; overflow: hidden; position: relative; }
.gl-featured__img { width:100%; height:100%; object-fit:contain; padding:8px; transition: transform 0.5s cubic-bezier(0.25,0.46,0.45,0.94); }
.gl-featured__item:hover .gl-featured__img { transform: scale(1.05); }
.gl-featured__placeholder { width:100%; height:100%; background: linear-gradient(135deg, rgba(180,140,255,0.3), rgba(140,200,255,0.3)); }
.gl-featured__shimmer {
  position: absolute; inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.12) 0%, transparent 60%);
  pointer-events: none;
}
.gl-featured__info {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0.65rem 0.85rem;
  border-top: 1px solid rgba(255,255,255,0.55);
}
.gl-featured__name { font-size: 0.78rem; color: rgba(15,8,40,0.8); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 80%; }
.gl-featured__arrow { font-size: 0.85rem; color: oklch(0.46 0.22 278); transition: transform 0.2s; }
.gl-featured__item:hover .gl-featured__arrow { transform: translateX(-4px); }
</style>
