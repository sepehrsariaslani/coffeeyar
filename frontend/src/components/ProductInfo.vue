<template>
  <header class="product-info">
    <nav class="product-info__breadcrumb">
      <RouterLink to="/" class="product-info__crumb">خانه</RouterLink>
      <span class="product-info__sep">·</span>
      <RouterLink v-if="category" :to="`/category/${category.slug}`" class="product-info__crumb">
        {{ category.title }}
      </RouterLink>
      <span v-if="category" class="product-info__sep">·</span>
      <span class="product-info__crumb product-info__crumb--current">{{ title }}</span>
    </nav>

    <h1 class="product-info__title">{{ title }}</h1>

    <div class="product-info__price-row">
      <span class="product-info__price">{{ formattedPrice }}</span>
      <span class="product-info__unit">تومان</span>
      <span v-if="hasDiscount" class="product-info__original">{{ formattedOriginal }}</span>
    </div>

    <p v-if="description" class="product-info__desc">{{ description }}</p>
  </header>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title:         { type: String, default: '' },
  price:         { type: [Number, String], default: 0 },
  originalPrice: { type: [Number, String], default: null },
  description:   { type: String, default: null },
  category:      { type: Object, default: null },
})

const fmt = (v) => Number(v || 0).toLocaleString('fa-IR')

const formattedPrice    = computed(() => fmt(props.price))
const formattedOriginal = computed(() => fmt(props.originalPrice))
const hasDiscount       = computed(() => props.originalPrice && Number(props.originalPrice) > Number(props.price))
</script>

<style scoped>
.product-info {
  display: flex;
  flex-direction: column;
  gap: 0;
}

/* Breadcrumb */
.product-info__breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-bottom: 1.75rem;
  flex-wrap: wrap;
}

.product-info__crumb {
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.72rem;
  color: #9e9890;
  text-decoration: none;
  letter-spacing: 0.02em;
  transition: color 0.2s;
}

.product-info__crumb:hover {
  color: #111;
}

.product-info__crumb--current {
  color: #555;
}

.product-info__sep {
  color: #C8C2BA;
  font-size: 0.7rem;
}

/* Title */
.product-info__title {
  font-family: 'Vazirmatn', sans-serif;
  font-size: clamp(1.5rem, 3vw, 2.25rem);
  font-weight: 300;
  color: #111;
  line-height: 1.3;
  letter-spacing: -0.01em;
  margin-bottom: 1.25rem;
}

/* Price */
.product-info__price-row {
  display: flex;
  align-items: baseline;
  gap: 0.4rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid #E8E4DE;
  margin-bottom: 1.25rem;
}

.product-info__price {
  font-family: 'Vazirmatn', sans-serif;
  font-size: 1.5rem;
  font-weight: 400;
  color: #111;
  letter-spacing: -0.02em;
}

.product-info__unit {
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.8rem;
  color: #9e9890;
  font-weight: 300;
}

.product-info__original {
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.85rem;
  color: #C8C2BA;
  text-decoration: line-through;
  margin-right: auto;
}

/* Description */
.product-info__desc {
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.9rem;
  line-height: 1.85;
  color: #5a5550;
  font-weight: 300;
  margin-bottom: 0.5rem;
}
</style>