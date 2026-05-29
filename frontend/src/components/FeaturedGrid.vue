<template>
  <section v-if="items.length" class="featured">
    <div class="featured__grid">
      <RouterLink
        v-for="(item, i) in displayItems"
        :key="item.slug"
        :to="`/product/${item.slug}`"
        class="featured__item"
        :class="`featured__item--${i}`"
      >
        <div class="featured__media">
          <img v-if="item.image" :src="item.image" :alt="item.title" class="featured__img" />
          <div v-else class="featured__placeholder" />
        </div>
        <div class="featured__info">
          <span class="featured__name">{{ item.title }}</span>
          <span class="featured__arrow">←</span>
        </div>
      </RouterLink>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  items: { type: Array, default: () => [] },
})

const displayItems = computed(() => props.items.slice(0, 4))
</script>

<style scoped>
.featured {
  padding: 0 5vw;
  margin: 2.5rem 0;
}

.featured__grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  background-color: #E8E4DE;
  border: 1px solid #E8E4DE;
}

.featured__item {
  background-color: #FAFAF8;
  display: flex;
  flex-direction: column;
  text-decoration: none;
  overflow: hidden;
  position: relative;
}

.featured__item:hover .featured__img {
  transform: scale(1.04);
}

.featured__item:hover .featured__arrow {
  opacity: 1;
  transform: translateX(-4px);
}

.featured__media {
  aspect-ratio: 3/4;
  overflow: hidden;
  background-color: #F0EDE8;
}

.featured__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.featured__placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #EDE9E4 0%, #E4DFD9 100%);
}

.featured__info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.9rem 1rem;
  border-top: 1px solid #E8E4DE;
}

.featured__name {
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.82rem;
  font-weight: 400;
  color: #222;
  letter-spacing: 0.01em;
}

.featured__arrow {
  font-size: 0.9rem;
  color: #800000;
  opacity: 0;
  transition: opacity 0.2s, transform 0.25s ease;
}

/* Responsive */
@media (max-width: 768px) {
  .featured__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .featured {
    padding: 0 4vw;
  }
}
</style>
