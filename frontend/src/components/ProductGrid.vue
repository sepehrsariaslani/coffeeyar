<template>
  <section class="product-grid">
    <div class="product-grid__inner" :class="`product-grid__inner--cols-${cols}`">
      <ProductCard v-for="item in items" :key="item.id" :product="item" />
    </div>
  </section>
</template>

<script setup>
import ProductCard from './ProductCard.vue'

defineProps({
  items: { type: Array, default: () => [] },
  cols: { type: Number, default: 4 },
})
</script>

<style scoped>
.product-grid {
  padding: 2rem 5vw 5rem;
}

.product-grid__inner {
  display: grid;
  gap: 2.5rem 1.5rem;
}

.product-grid__inner--cols-4 {
  grid-template-columns: repeat(4, 1fr);
}

.product-grid__inner--cols-3 {
  grid-template-columns: repeat(3, 1fr);
}

@media (max-width: 1024px) {
  .product-grid__inner--cols-4 {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .product-grid__inner--cols-4,
  .product-grid__inner--cols-3 {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem 1rem;
  }
}

@media (max-width: 400px) {
  .product-grid {
    padding: 1.5rem 4vw 4rem;
  }
}
</style>
