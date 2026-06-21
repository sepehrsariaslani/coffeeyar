<script setup>
import { computed } from "vue";
import { useWishlistStore } from "@/stores/wishlist.js";
import { useLayoutStore } from "@/stores/layout.js";

const props = defineProps({
  product: { type: Object, required: true },
  variant: { type: String, default: null },
});

const wishlistStore = useWishlistStore();
const layoutStore = useLayoutStore();
const cardVariant = computed(() => props.variant || layoutStore.cardVariant);
const formatPrice = (value) => Number(value || 0).toLocaleString('fa-IR');

const meta = computed(() => {
  if (props.product.type === 'accessory') {
    return { origin: props.product.category, roast: props.product.brand, notes: props.product.specs?.slice(0, 2).map(s => s.value).join(' · ') };
  }
  return { origin: props.product.origin, roast: props.product.roast, notes: props.product.notes?.join(' · ') };
});
</script>

<template>
  <article v-if="cardVariant === 'standard'" class="card" @click="$router.push(`/products/${product.slug || product.id}`)">
    <div class="card__media">
      <img v-if="product.image" :src="product.image" :alt="product.name" class="card__img" />
      <div v-else class="card__placeholder" />
      <span v-if="product.type === 'accessory'" class="card__badge">اکسسوری</span>
      <span v-if="product.stock === 'low_stock'" class="card__stock-badge card__stock-badge--low">موجودی محدود</span>
      <span v-if="product.stock === 'out_of_stock'" class="card__stock-badge card__stock-badge--out">ناموجود</span>
      <button class="card__wishlist" :class="{ 'card__wishlist--active': wishlistStore.isWishlisted(product.id) }" @click.stop="wishlistStore.toggle(product.id)">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" /></svg>
      </button>
    </div>
    <footer class="card__footer">
      <div class="card__meta">
        <span class="card__origin">{{ meta.origin }}</span>
        <span class="card__roast">{{ meta.roast }}</span>
      </div>
      <h3 class="card__title">{{ product.name }}</h3>
      <p class="card__notes">{{ meta.notes }}</p>
      <p class="card__price">{{ formatPrice(product.price) }} <span>تومان</span></p>
    </footer>
  </article>

  <article v-else-if="cardVariant === 'compact'" class="card-compact" @click="$router.push(`/products/${product.slug || product.id}`)">
    <div class="card-compact__media">
      <img v-if="product.image" :src="product.image" :alt="product.name" class="card-compact__img" />
      <div v-else class="card-compact__placeholder" />
      <div class="card-compact__overlay">
        <p class="card-compact__price">{{ formatPrice(product.price) }} <span>تومان</span></p>
      </div>
      <button class="card-compact__wishlist" :class="{ 'card-compact__wishlist--active': wishlistStore.isWishlisted(product.id) }" @click.stop="wishlistStore.toggle(product.id)">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" /></svg>
      </button>
    </div>
    <div class="card-compact__body">
      <h3 class="card-compact__title">{{ product.name }}</h3>
      <p class="card-compact__sub">{{ meta.origin }} · {{ meta.roast }}</p>
    </div>
  </article>

  <article v-else class="card-h" @click="$router.push(`/products/${product.slug || product.id}`)">
    <div class="card-h__media">
      <img v-if="product.image" :src="product.image" :alt="product.name" class="card-h__img" />
      <div v-else class="card-h__placeholder" />
    </div>
    <div class="card-h__body">
      <div class="card-h__meta">
        <span class="card-h__origin">{{ meta.origin }}</span>
        <button class="card-h__wishlist" :class="{ 'card-h__wishlist--active': wishlistStore.isWishlisted(product.id) }" @click.stop="wishlistStore.toggle(product.id)">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" /></svg>
        </button>
      </div>
      <h3 class="card-h__title">{{ product.name }}</h3>
      <p class="card-h__notes">{{ meta.notes }}</p>
      <div class="card-h__footer">
        <span class="card-h__price">{{ formatPrice(product.price) }} <span class="card-h__currency">تومان</span></span>
        <span class="card-h__roast">{{ meta.roast }}</span>
      </div>
    </div>
  </article>
</template>

<style scoped>
.card { cursor: pointer; display: flex; flex-direction: column; background-color: #FAFAF8; }
.card:hover .card__img { transform: scale(1.03); }
.card:hover .card__title { color: #800000; }
.card__media { aspect-ratio: 4 / 5; overflow: hidden; background-color: #F0EDE8; position: relative; }
.card__img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.45s cubic-bezier(0.25,0.46,0.45,0.94); }
.card__placeholder { width: 100%; height: 100%; background: linear-gradient(135deg,#EDE9E4,#E0DBD5); }
.card__badge { position: absolute; top: 0.75rem; right: 0.75rem; font-size: 0.65rem; letter-spacing: 0.08em; background-color: #800000; color: #fff; padding: 0.2rem 0.5rem; }
.card__wishlist { position: absolute; top: 0.75rem; left: 0.75rem; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; background-color: rgba(255,255,255,0.9); backdrop-filter: blur(4px); border: none; cursor: pointer; color: #9e9890; opacity: 0; transform: scale(0.85); transition: opacity 0.2s, transform 0.2s, color 0.2s; }
.card:hover .card__wishlist { opacity: 1; transform: scale(1); }
.card__wishlist--active { opacity: 1 !important; transform: scale(1) !important; color: #800000; }
.card__wishlist--active svg { fill: #800000; }
.card__wishlist:hover { color: #800000; }
.card__footer { padding: 1rem 0.1rem; border-top: 1px solid #E8E4DE; }
.card__meta { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.35rem; }
.card__origin { font-size: 0.7rem; letter-spacing: 0.1em; color: #800000; text-transform: uppercase; }
.card__roast { font-size: 0.68rem; color: #9e9890; border: 1px solid #E8E4DE; padding: 0.1rem 0.4rem; }
.card__title { font-size: 0.9rem; font-weight: 400; color: #1a1a1a; margin: 0 0 0.25rem; transition: color 0.2s; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.card__notes { font-size: 0.72rem; color: #9e9890; margin: 0 0 0.4rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.card__price { font-size: 0.82rem; color: #3f3a36; margin: 0; }
.card__price span { font-size: 0.7rem; color: #9e9890; }

.card__stock-badge { position: absolute; bottom: 0.75rem; right: 0.75rem; font-size: 0.62rem; font-family: Vazirmatn, sans-serif; letter-spacing: 0.04em; padding: 0.2rem 0.55rem; font-weight: 500; }
.card__stock-badge--low { background-color: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
.card__stock-badge--out { background-color: #f3f4f6; color: #6b7280; border: 1px solid #e5e7eb; }

.card-compact { cursor: pointer; display: flex; flex-direction: column; background-color: #FAFAF8; }
.card-compact:hover .card-compact__img { transform: scale(1.05); }
.card-compact__media { aspect-ratio: 1 / 1; overflow: hidden; background-color: #F0EDE8; position: relative; }
.card-compact__img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s cubic-bezier(0.25,0.46,0.45,0.94); }
.card-compact__placeholder { width: 100%; height: 100%; background: linear-gradient(135deg,#EDE9E4,#E0DBD5); }
.card-compact__overlay { position: absolute; inset: 0; background: linear-gradient(to top, rgba(10,10,10,0.55) 0%, transparent 50%); display: flex; align-items: flex-end; padding: 0.75rem; opacity: 0; transition: opacity 0.25s; }
.card-compact:hover .card-compact__overlay { opacity: 1; }
.card-compact__price { font-size: 0.8rem; color: #fff; margin: 0; }
.card-compact__price span { font-size: 0.65rem; opacity: 0.75; }
.card-compact__wishlist { position: absolute; top: 0.5rem; left: 0.5rem; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.85); border: none; cursor: pointer; color: #9e9890; opacity: 0; transition: opacity 0.2s, color 0.2s; }
.card-compact:hover .card-compact__wishlist { opacity: 1; }
.card-compact__wishlist--active { opacity: 1 !important; color: #800000; }
.card-compact__wishlist--active svg { fill: #800000; }
.card-compact__body { padding: 0.65rem 0.1rem; }
.card-compact__title { font-size: 0.82rem; font-weight: 400; color: #1a1a1a; margin: 0 0 0.2rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.card-compact__sub { font-size: 0.68rem; color: #9e9890; margin: 0; }

.card-h { cursor: pointer; display: flex; flex-direction: row; gap: 0; background-color: #FAFAF8; border-bottom: 1px solid #E8E4DE; height: 130px; overflow: hidden; }
.card-h:hover { background-color: #F5F2EE; }
.card-h:hover .card-h__title { color: #800000; }
.card-h__media { width: 110px; min-width: 110px; overflow: hidden; position: relative; }
.card-h__img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s; }
.card-h:hover .card-h__img { transform: scale(1.05); }
.card-h__placeholder { width: 100%; height: 100%; background: linear-gradient(135deg,#EDE9E4,#E0DBD5); }
.card-h__body { flex: 1; padding: 1rem; display: flex; flex-direction: column; justify-content: space-between; min-width: 0; }
.card-h__meta { display: flex; align-items: center; justify-content: space-between; }
.card-h__origin { font-size: 0.65rem; letter-spacing: 0.1em; color: #800000; text-transform: uppercase; }
.card-h__wishlist { width: 26px; height: 26px; display: flex; align-items: center; justify-content: center; background: transparent; border: none; cursor: pointer; color: #c8c2ba; transition: color 0.2s; }
.card-h__wishlist:hover, .card-h__wishlist--active { color: #800000; }
.card-h__wishlist--active svg { fill: #800000; }
.card-h__title { font-size: 0.85rem; font-weight: 400; color: #1a1a1a; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; transition: color 0.2s; }
.card-h__notes { font-size: 0.7rem; color: #9e9890; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.card-h__footer { display: flex; align-items: center; justify-content: space-between; }
.card-h__price { font-size: 0.8rem; color: #3f3a36; }
.card-h__currency { font-size: 0.68rem; color: #9e9890; }
.card-h__roast { font-size: 0.66rem; color: #9e9890; border: 1px solid #E8E4DE; padding: 0.1rem 0.4rem; }
</style>
