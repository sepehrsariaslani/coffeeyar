<template>
  <article class="card" @click="$router.push(`/product/${product.slug}`)">
    <div class="card__media">
      <img v-if="product.image" :src="product.image" :alt="product.title" class="card__img" />
      <div v-else class="card__placeholder" />
    </div>
    <footer class="card__footer">
      <h3 class="card__title">{{ product.title }}</h3>
      <p class="card__price">{{ formatPrice(product.effective_price_toman) }} <span>تومان</span></p>
    </footer>
  </article>
</template>

<script setup>
defineProps({
  product: { type: Object, required: true },
})

const formatPrice = (value) => Number(value || 0).toLocaleString('fa-IR')
</script>

<style scoped>
.card {
  cursor: pointer;
  display: flex;
  flex-direction: column;
  background-color: #FAFAF8;
}

.card:hover .card__img {
  transform: scale(1.03);
}

.card:hover .card__title {
  color: #800000;
}

.card__media {
  aspect-ratio: 1 / 1;
  overflow: hidden;
  background-color: #F0EDE8;
}

.card__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.45s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.card__placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #EDE9E4, #E0DBD5);
}

.card__footer {
  padding: 0.85rem 0.1rem;
  border-top: 1px solid #E8E4DE;
}

.card__title {
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.85rem;
  font-weight: 400;
  color: #1a1a1a;
  margin: 0 0 0.35rem;
  transition: color 0.2s;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card__price {
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.78rem;
  color: #666058;
  margin: 0;
  font-weight: 300;
}

.card__price span {
  font-size: 0.7rem;
  color: #9e9890;
}
</style>
