<template>
  <div class="app-shell">
    <header class="site-header">
      <div class="site-header-left">
        <button class="menu-btn mobile-only" @click="menuOpen = true">☰</button>
        <RouterLink to="/" class="brand">{{ storeName }}</RouterLink>
      </div>

      <nav class="desktop-nav">
        <RouterLink v-for="link in topLinks" :key="link.to" :to="link.to">{{ link.label }}</RouterLink>
      </nav>

      <div class="site-header-right">
        <RouterLink to="/checkout" class="cart-pill" :class="{ 'cart-pill--pulse': cartPulse }">
          سبد ({{ cart.count.value }})
        </RouterLink>
      </div>
    </header>

    <CategoryMenu :open="menuOpen" :links="topLinks" @close="menuOpen = false" />

    <RouterView />

    <nav class="mobile-bottom-nav">
      <RouterLink v-for="link in bottomLinks" :key="`bottom-${link.to}`" :to="link.to">{{ link.label }}</RouterLink>
    </nav>

    <div v-if="flyToCart.visible" class="cart-fly" :style="flyToCart.style" aria-hidden="true">
      <img v-if="flyToCart.image" :src="flyToCart.image" alt="" />
      <span v-else class="cart-fly__dot"></span>
    </div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import CategoryMenu from '@/components/CategoryMenu.vue'
import { useCart } from '@/stores/cart'
import { api } from '@/utils/api'

const menuOpen = ref(false)
const cart = useCart()
const storeName = ref(window.store_name || 'فروشگاه')

const fallbackTopLinks = [
  { label: 'همه محصولات', to: '/all-products' },
  { label: 'بلاگ', to: '/blog' },
  { label: 'درباره ما', to: '/about-us' },
  { label: 'شوروم', to: '/showroom' },
]

const fallbackBottomLinks = [
  { label: 'خانه', to: '/' },
  { label: 'محصولات', to: '/all-products' },
  { label: 'بلاگ', to: '/blog' },
  { label: 'تسویه', to: '/checkout' },
]

const topLinks = ref(fallbackTopLinks)
const bottomLinks = ref(fallbackBottomLinks)
const cartPulse = ref(false)
const flyToCart = reactive({
  visible: false,
  image: '',
  style: {},
})

let pulseTimer = null
let flyTimer = null
let cartAddHandler = null

function pulseCart() {
  cartPulse.value = false
  requestAnimationFrame(() => {
    cartPulse.value = true
  })
  if (pulseTimer) clearTimeout(pulseTimer)
  pulseTimer = setTimeout(() => {
    cartPulse.value = false
  }, 420)
}

function startFlyToCart(detail = {}) {
  const cartEl = document.querySelector('.cart-pill')
  if (!cartEl) {
    pulseCart()
    return
  }

  const sourceRect = detail.sourceRect
  const targetRect = cartEl.getBoundingClientRect()
  if (!sourceRect) {
    pulseCart()
    return
  }

  const startX = sourceRect.left + sourceRect.width / 2
  const startY = sourceRect.top + sourceRect.height / 2
  const endX = targetRect.left + targetRect.width / 2
  const endY = targetRect.top + targetRect.height / 2

  flyToCart.visible = true
  flyToCart.image = detail.image || ''
  flyToCart.style = {
    left: `${startX - 26}px`,
    top: `${startY - 26}px`,
    transform: 'translate3d(0, 0, 0) scale(1)',
    opacity: '0.92',
  }

  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      flyToCart.style = {
        ...flyToCart.style,
        transform: `translate3d(${endX - startX}px, ${endY - startY}px, 0) scale(0.18)`,
        opacity: '0.2',
      }
    })
  })

  if (flyTimer) clearTimeout(flyTimer)
  flyTimer = setTimeout(() => {
    flyToCart.visible = false
    flyToCart.image = ''
    pulseCart()
  }, 620)
}

onMounted(async () => {
  try {
    const nav = await api.getNavigation()
    topLinks.value = nav.header?.length ? nav.header : fallbackTopLinks
    bottomLinks.value = nav.mobile?.length ? nav.mobile : fallbackBottomLinks
  } catch {
    topLinks.value = fallbackTopLinks
    bottomLinks.value = fallbackBottomLinks
  }

  cartAddHandler = (event) => startFlyToCart(event.detail)
  window.addEventListener('cart:add', cartAddHandler)
})

onBeforeUnmount(() => {
  if (pulseTimer) clearTimeout(pulseTimer)
  if (flyTimer) clearTimeout(flyTimer)
  if (cartAddHandler) window.removeEventListener('cart:add', cartAddHandler)
})
</script>

<style scoped>
.cart-pill--pulse {
  animation: cartPulse 0.38s ease;
}

@keyframes cartPulse {
  0% {
    transform: scale(1);
  }
  45% {
    transform: scale(1.08);
  }
  100% {
    transform: scale(1);
  }
}

.cart-fly {
  position: fixed;
  width: 52px;
  height: 52px;
  border-radius: 14px;
  overflow: hidden;
  background: #f4eeee;
  border: 1px solid #e4d6d6;
  box-shadow: 0 8px 20px rgba(92, 26, 34, 0.18);
  transition: transform 0.56s cubic-bezier(0.2, 0.9, 0.2, 1), opacity 0.56s ease;
  pointer-events: none;
  z-index: 120;
}

.cart-fly img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cart-fly__dot {
  display: block;
  width: 100%;
  height: 100%;
  background: #5c1a22;
}
</style>
