<template>
  <main v-if="product" class="product-page">
    <section class="product-page__grid">
      <ProductGallery
        :image="product.image"
        :alt="product.title"
        :badge="product.in_stock ? 'موجود' : null"
      />

      <section class="product-page__content">
        <ProductInfo
          :title="product.title"
          :price="activePrice"
          :original-price="activeOriginalPrice"
          :description="product.short_description"
          :category="product.category"
        />

        <VarientPicker
          v-if="product.variants?.length"
          v-model="selectedVariant"
          :variants="product.variants"
        />

        <div class="product-page__actions">
          <button class="btn btn--primary" :disabled="addDisabled" @click="addToCart($event)">افزودن به سبد</button>
          <RouterLink class="btn btn--ghost" to="/checkout">تسویه حساب</RouterLink>
        </div>
      </section>
    </section>

    <section v-if="product.description" class="product-page__description" v-html="product.description"></section>
  </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import ProductGallery from '@/components/ProductGallery.vue'
import ProductInfo from '@/components/ProductInfo.vue'
import VarientPicker from '@/components/VarientPicker.vue'
import { api } from '@/utils/api'
import { useCart } from '@/stores/cart'

const props = defineProps({ slug: { type: String, required: true } })
const product = ref(null)
const selectedVariant = ref(null)
const { add } = useCart()

const activePrice = computed(
  () => selectedVariant.value?.effective_price_toman || product.value?.effective_price_toman || 0,
)

const activeOriginalPrice = computed(
  () => selectedVariant.value?.price_toman || product.value?.price_toman || null,
)
const addDisabled = computed(() => !!(product.value?.has_variants && !selectedVariant.value))

function addToCart(event) {
  if (!product.value) return
  if (product.value.has_variants && !selectedVariant.value) return

  add(product.value, 1, selectedVariant.value)

  if (typeof window !== 'undefined') {
    const sourceRect = event?.currentTarget?.getBoundingClientRect?.()
    window.dispatchEvent(
      new CustomEvent('cart:add', {
        detail: {
          image: selectedVariant.value?.image || product.value?.image || '',
          sourceRect,
        },
      }),
    )
  }
}

onMounted(async () => {
  product.value = await api.getProduct(props.slug)
  selectedVariant.value = product.value?.variants?.[0] || null
})
</script>

<style scoped>
.product-page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem 1rem 3rem;
}

.product-page__grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.product-page__content {
  display: flex;
  flex-direction: column;
}

.product-page__actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
}

.btn {
  height: 44px;
  padding: 0 1rem;
  border: 1px solid #e8e4de;
  background: #fff;
  color: #1f1f1f;
  text-decoration: none;
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.88rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.btn--primary {
  background: #800000;
  border-color: #800000;
  color: #fff;
}

.btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.btn:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.btn--ghost:hover {
  border-color: #800000;
  color: #800000;
}

.product-page__variant-message {
  margin: 0.5rem 0 0;
  color: #800000;
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.84rem;
}

.product-page__description {
  margin-top: 2.25rem;
  padding-top: 1.25rem;
  border-top: 1px solid #e8e4de;
  color: #3f3a36;
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.92rem;
  line-height: 1.9;
}

@media (max-width: 900px) {
  .product-page__grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .product-page {
    padding-top: 1.25rem;
  }
}
</style>
