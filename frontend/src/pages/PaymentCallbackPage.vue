<template>
  <main class="page-wrap content-page">
    <h1>{{ title }}</h1>
    <p>{{ description }}</p>
    <RouterLink to="/all-products" class="btn">بازگشت به فروشگاه</RouterLink>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '@/utils/api'
import { useCart } from '@/stores/cart'

const route = useRoute()
const cart = useCart()

const title = ref('در حال بررسی پرداخت...')
const description = ref('لطفا منتظر بمانید')

onMounted(async () => {
  try {
    const result = await api.verifyPayment(route.query.order_id, route.query.Authority, route.query.Status)
    if (result?.ok) {
      title.value = 'پرداخت موفق'
      description.value = `سفارش ${result.order_id} با موفقیت ثبت شد.`
      cart.clear()
    } else {
      title.value = 'پرداخت ناموفق'
      description.value = 'پرداخت تایید نشد یا لغو شده است.'
    }
  } catch {
    title.value = 'خطا در تایید پرداخت'
    description.value = 'در تایید تراکنش خطایی رخ داد.'
  }
})
</script>
