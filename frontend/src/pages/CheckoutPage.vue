<template>
  <main class="page-wrap checkout-page">
    <header class="checkout-page__head">
      <h1>سبد خرید و تسویه حساب</h1>
      <p>مرور سفارش و ثبت اطلاعات ارسال</p>
    </header>

    <section v-if="cart.state.items.length" class="checkout-layout">
      <section class="checkout-card checkout-items">
        <article v-for="item in cart.state.items" :key="item.key" class="checkout-item">
          <img v-if="item.image" :src="item.image" :alt="item.title" class="checkout-item__image" />
          <div v-else class="checkout-item__image checkout-item__image--placeholder"></div>

          <div class="checkout-item__meta">
            <h3>{{ item.title }}</h3>
            <small v-if="item.variant_title">{{ item.variant_title }}</small>
            <p>{{ formatPrice(item.price_toman) }} تومان</p>
          </div>

          <div class="checkout-item__qty">
            <button type="button" @click="decrement(item)">−</button>
            <input type="number" min="1" :value="item.qty" @input="updateQty(item.key, $event.target.value)" />
            <button type="button" @click="increment(item)">+</button>
          </div>

          <div class="checkout-item__sum">
            <strong>{{ formatPrice(item.price_toman * item.qty) }}</strong>
            <button type="button" class="checkout-item__remove" @click="cart.remove(item.key)">حذف</button>
          </div>
        </article>
      </section>

      <aside class="checkout-side">
        <section class="checkout-card checkout-summary">
          <h2>خلاصه پرداخت</h2>
          <p><span>جمع کالا</span><strong>{{ formatPrice(cart.subtotal.value) }} تومان</strong></p>
          <p><span>هزینه ارسال</span><strong>{{ formatPrice(shippingFee) }} تومان</strong></p>
          <p class="checkout-summary__total"><span>جمع نهایی</span><strong>{{ formatPrice(cart.subtotal.value + shippingFee) }} تومان</strong></p>
        </section>

        <form class="checkout-card checkout-form" @submit.prevent="submitOrder">
          <h2>اطلاعات گیرنده</h2>
          <input v-model="form.customer_name" placeholder="نام و نام خانوادگی" required />
          <input v-model="form.mobile" placeholder="شماره موبایل" required />
          <textarea v-model="form.shipping_address" placeholder="آدرس ارسال" required></textarea>
          <textarea v-model="form.notes" placeholder="توضیحات (اختیاری)"></textarea>
          <button class="checkout-submit" :disabled="loading">
            {{ loading ? 'در حال انتقال...' : 'پرداخت آنلاین' }}
          </button>
        </form>
      </aside>
    </section>

    <section v-else class="checkout-empty">
      <p>سبد خرید شما خالی است.</p>
      <RouterLink to="/all-products" class="checkout-back">رفتن به محصولات</RouterLink>
    </section>

    <p class="error" v-if="errorMsg">{{ errorMsg }}</p>
  </main>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { api } from '@/utils/api'
import { useCart } from '@/stores/cart'

const cart = useCart()
const shippingFee = Number(window.shipping_fee_toman || 120000)
const loading = ref(false)
const errorMsg = ref('')

const form = reactive({
  customer_name: '',
  mobile: '',
  shipping_address: '',
  notes: '',
})

const formatPrice = (value) => Number(value || 0).toLocaleString('fa-IR')

function updateQty(key, qty) {
  cart.setQty(key, qty)
}

function increment(item) {
  cart.setQty(item.key, Number(item.qty) + 1)
}

function decrement(item) {
  cart.setQty(item.key, Math.max(1, Number(item.qty) - 1))
}

async function submitOrder() {
  try {
    loading.value = true
    errorMsg.value = ''

    const created = await api.createOrder({
      customer_name: form.customer_name,
      mobile: form.mobile,
      shipping_address: form.shipping_address,
      notes: form.notes,
      items: cart.state.items.map((item) => ({
        product_slug: item.slug,
        variant_id: item.variant_id,
        qty: item.qty,
      })),
    })

    const started = await api.startPayment(created.order_id, created.public_token)
    window.location.href = started.payment_url
  } catch (error) {
    errorMsg.value = 'خطا در شروع پرداخت. لطفا دوباره تلاش کنید.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.checkout-page {
  padding-top: 1.5rem;
}

.checkout-page__head h1 {
  margin: 0;
  font-size: 1.35rem;
  font-weight: 500;
}

.checkout-page__head p {
  margin: 0.4rem 0 0;
  color: #6a6460;
  font-size: 0.9rem;
}

.checkout-layout {
  margin-top: 1.2rem;
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.checkout-card {
  background: #fff;
  border: 1px solid #ece8e3;
  padding: 0.9rem;
}

.checkout-items {
  display: grid;
  gap: 0.8rem;
}

.checkout-item {
  display: grid;
  grid-template-columns: 72px 1fr;
  gap: 0.8rem;
  border-bottom: 1px solid #f3efea;
  padding-bottom: 0.8rem;
}

.checkout-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.checkout-item__image {
  width: 72px;
  height: 72px;
  object-fit: cover;
  background: #f4f2ef;
}

.checkout-item__image--placeholder {
  border: 1px solid #ece8e3;
}

.checkout-item__meta h3 {
  margin: 0;
  font-size: 0.94rem;
  font-weight: 500;
}

.checkout-item__meta small {
  color: #716b66;
}

.checkout-item__meta p {
  margin: 0.35rem 0 0;
  color: #37322f;
}

.checkout-item__qty {
  margin-top: 0.6rem;
  display: inline-flex;
  align-items: center;
  border: 1px solid #ece8e3;
  width: fit-content;
}

.checkout-item__qty button {
  width: 32px;
  height: 32px;
  border: none;
  background: #faf9f8;
  cursor: pointer;
}

.checkout-item__qty input {
  width: 46px;
  height: 32px;
  border: none;
  text-align: center;
  outline: none;
}

.checkout-item__sum {
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.checkout-item__remove {
  border: none;
  background: transparent;
  color: #5c1a22;
  cursor: pointer;
  font-size: 0.78rem;
}

.checkout-summary h2,
.checkout-form h2 {
  margin: 0 0 0.75rem;
  font-size: 1rem;
  font-weight: 500;
}

.checkout-summary p {
  margin: 0.5rem 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.checkout-summary__total {
  margin-top: 0.8rem !important;
  padding-top: 0.7rem;
  border-top: 1px solid #eee8e4;
}

.checkout-summary__total strong {
  color: #5c1a22;
}

.checkout-form input,
.checkout-form textarea {
  width: 100%;
  border: 1px solid #ece8e3;
  background: #fff;
  padding: 0.72rem 0.75rem;
  font-family: inherit;
  margin-top: 0.6rem;
  outline: none;
}

.checkout-form textarea {
  min-height: 96px;
  resize: vertical;
}

.checkout-submit {
  margin-top: 0.9rem;
  width: 100%;
  height: 44px;
  border: 1px solid #5c1a22;
  background: #5c1a22;
  color: #fff;
  font-family: inherit;
  cursor: pointer;
}

.checkout-submit:disabled {
  opacity: 0.72;
  cursor: wait;
}

.checkout-empty {
  margin-top: 1.2rem;
  border: 1px solid #ece8e3;
  padding: 1.1rem;
  text-align: center;
}

.checkout-back {
  display: inline-block;
  margin-top: 0.6rem;
  color: #5c1a22;
}

.error {
  margin-top: 0.8rem;
}

@media (min-width: 980px) {
  .checkout-layout {
    grid-template-columns: 1.35fr 0.9fr;
    align-items: start;
    gap: 1.1rem;
  }

  .checkout-side {
    position: sticky;
    top: 86px;
    display: grid;
    gap: 1rem;
  }

  .checkout-item {
    grid-template-columns: 82px 1fr auto;
    align-items: start;
  }

  .checkout-item__image {
    width: 82px;
    height: 82px;
  }

  .checkout-item__sum {
    margin-top: 0;
    min-width: 140px;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.5rem;
  }
}
</style>
