<template>
  <main class="page-wrap">
    <section class="section-head">
      <h2>{{ pageTitle }}</h2>
    </section>

    <section class="products-grid">
      <ProductCard v-for="item in products" :key="item.slug" :product="item" />
    </section>

    <p v-if="!products.length" class="empty-note">محصولی برای نمایش موجود نیست.</p>
  </main>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { api } from '@/utils/api'
import ProductCard from '@/components/ProductCard.vue'

const props = defineProps({
  categorySlug: {
    type: String,
    default: '',
  },
})

const products = ref([])

const pageTitle = computed(() => (props.categorySlug ? 'محصولات' : 'همه محصولات'))

async function load() {
  const filters = props.categorySlug ? { category_slug: props.categorySlug } : {}
  const res = await api.listProducts(filters, 'default', 1)
  products.value = res.items || []
}

watch(() => props.categorySlug, load)
onMounted(load)
</script>
