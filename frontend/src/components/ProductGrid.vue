<template>
  <section class="product-grid">
    <div class="product-grid__inner">
      <ProductCard v-for="item in items" :key="item.slug" :product="item" />
    </div>
  </section>
</template>

<script setup>
import ProductCard from './ProductCard.vue'

defineProps({
  items: { type: Array, default: () => [] },
})
</script>

<style scoped>
.product-grid {
  padding: 2rem 5vw 5rem;
}

.product-grid__inner {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2.5rem 1.5rem;
}

@media (max-width: 1024px) {
  .product-grid__inner {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .product-grid__inner {
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
