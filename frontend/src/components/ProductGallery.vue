<template>
  <div class="gallery">
    <div class="gallery__frame">
      <img
        v-if="image"
        :src="image"
        :alt="alt"
        class="gallery__img"
        :class="{ 'gallery__img--loaded': loaded }"
        @load="loaded = true"
      />
      <div v-else class="gallery__placeholder">
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
          <rect x="8" y="12" width="32" height="24" rx="2" stroke="#C8C2BA" stroke-width="1.5"/>
          <circle cx="18" cy="21" r="3" stroke="#C8C2BA" stroke-width="1.5"/>
          <path d="M8 32L16 24L22 30L30 22L40 32" stroke="#C8C2BA" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <div v-if="image && !loaded" class="gallery__shimmer" />
    </div>
    <div v-if="badge" class="gallery__badge">{{ badge }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  image: { type: String, default: null },
  alt: { type: String, default: '' },
  badge: { type: String, default: null },
})

const loaded = ref(false)
</script>

<style scoped>
.gallery {
  position: relative;
  width: 100%;
}

.gallery__frame {
  position: relative;
  aspect-ratio: 4 / 5;
  overflow: hidden;
  background-color: #F0EDE8;
  border: 1px solid #E8E4DE;
}

.gallery__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transition: opacity 0.4s ease;
}

.gallery__img--loaded {
  opacity: 1;
}

.gallery__placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #EDE9E4, #E4DFD9);
}

.gallery__shimmer {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, #F0EDE8 25%, #E8E4DE 50%, #F0EDE8 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.gallery__badge {
  position: absolute;
  top: 1.25rem;
  right: 1.25rem;
  background-color: #800000;
  color: #fff;
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.7rem;
  font-weight: 400;
  letter-spacing: 0.06em;
  padding: 0.3rem 0.65rem;
}
</style>
