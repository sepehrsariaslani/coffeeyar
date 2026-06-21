<script setup>
import { computed } from "vue";
import { useWishlistStore } from "@/stores/wishlist.js";
import { useLayoutStore } from "@/stores/layout.js";
const props = defineProps({ product: { type: Object, required: true }, variant: { type: String, default: null } });
const wishlistStore = useWishlistStore();
const layoutStore = useLayoutStore();
const cardVariant = computed(() => props.variant || layoutStore.cardVariant);
const formatPrice = (v) => Number(v || 0).toLocaleString('fa-IR');
const meta = computed(() => {
  if (props.product.type === 'accessory') return { origin: props.product.category, roast: props.product.brand, notes: props.product.specs?.slice(0,2).map(s=>s.value).join(' · ') };
  return { origin: props.product.origin, roast: props.product.roast, notes: props.product.notes?.join(' · ') };
});
</script>

<template>
  <!-- Standard -->
  <article v-if="cardVariant === 'standard'" class="dk-card" @click="$router.push(`/products/${product.slug || product.id}`)">
    <div class="dk-card__media">
      <img v-if="product.image" :src="product.image" :alt="product.name" class="dk-card__img" />
      <div v-else class="dk-card__placeholder" />
      <button class="dk-card__wish" :class="{'dk-card__wish--on': wishlistStore.isWishlisted(product.id)}" @click.stop="wishlistStore.toggle(product.id)">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
      </button>
    </div>
    <div class="dk-card__body">
      <div class="dk-card__meta"><span class="dk-card__origin">{{ meta.origin }}</span><span class="dk-card__roast">{{ meta.roast }}</span></div>
      <h3 class="dk-card__title">{{ product.name }}</h3>
      <p class="dk-card__notes">{{ meta.notes }}</p>
      <p class="dk-card__price">{{ formatPrice(product.price) }} <span>تومان</span></p>
    </div>
  </article>

  <!-- Compact -->
  <article v-else-if="cardVariant === 'compact'" class="dk-compact" @click="$router.push(`/products/${product.slug || product.id}`)">
    <div class="dk-compact__media">
      <img v-if="product.image" :src="product.image" :alt="product.name" class="dk-compact__img" />
      <div v-else class="dk-compact__placeholder" />
      <div class="dk-compact__overlay"><p class="dk-compact__price">{{ formatPrice(product.price) }} <span>تومان</span></p></div>
    </div>
    <div class="dk-compact__body">
      <h3 class="dk-compact__title">{{ product.name }}</h3>
      <p class="dk-compact__sub">{{ meta.origin }}</p>
    </div>
  </article>

  <!-- Horizontal -->
  <article v-else class="dk-card-h" @click="$router.push(`/products/${product.slug || product.id}`)">
    <div class="dk-card-h__media">
      <img v-if="product.image" :src="product.image" :alt="product.name" class="dk-card-h__img" />
      <div v-else class="dk-card-h__placeholder" />
    </div>
    <div class="dk-card-h__body">
      <div class="dk-card-h__origin">{{ meta.origin }}</div>
      <h3 class="dk-card-h__title">{{ product.name }}</h3>
      <p class="dk-card-h__price">{{ formatPrice(product.price) }} <span>تومان</span></p>
    </div>
  </article>
</template>

<style scoped>
.dk-card { cursor:pointer; display:flex; flex-direction:column; background:#1a1a1a; border:1px solid rgba(255,255,255,0.07); transition:border-color 0.2s, transform 0.2s; }
.dk-card:hover { border-color: rgba(201,146,63,0.4); transform: translateY(-2px); }
.dk-card:hover .dk-card__title { color: #C9923F; }
.dk-card__media { aspect-ratio:4/5; overflow:hidden; position:relative; background:#111; }
.dk-card__img { width:100%; height:100%; object-fit:cover; transition:transform 0.45s cubic-bezier(0.25,0.46,0.45,0.94); filter:brightness(0.85); }
.dk-card:hover .dk-card__img { transform:scale(1.04); filter:brightness(0.95); }
.dk-card__placeholder { width:100%; height:100%; background:linear-gradient(135deg,#1e1e1e,#161616); }
.dk-card__wish { position:absolute; top:0.75rem; left:0.75rem; width:30px; height:30px; display:flex; align-items:center; justify-content:center; background:rgba(0,0,0,0.6); border:1px solid rgba(255,255,255,0.12); border-radius:50%; cursor:pointer; color:rgba(255,255,255,0.4); opacity:0; transform:scale(0.8); transition:all 0.2s; }
.dk-card:hover .dk-card__wish { opacity:1; transform:scale(1); }
.dk-card__wish--on { opacity:1!important; transform:scale(1)!important; color:#C9923F; }
.dk-card__wish--on svg { fill:#C9923F; }
.dk-card__body { padding:0.9rem 0.85rem; border-top:1px solid rgba(255,255,255,0.06); }
.dk-card__meta { display:flex; align-items:center; justify-content:space-between; margin-bottom:0.35rem; }
.dk-card__origin { font-size:0.68rem; letter-spacing:0.12em; color:#C9923F; text-transform:uppercase; font-weight:500; }
.dk-card__roast { font-size:0.65rem; color:rgba(255,255,255,0.3); border:1px solid rgba(255,255,255,0.1); padding:0.1rem 0.4rem; }
.dk-card__title { font-size:0.88rem; font-weight:400; color:rgba(255,255,255,0.82); margin:0 0 0.25rem; transition:color 0.2s; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.dk-card__notes { font-size:0.7rem; color:rgba(255,255,255,0.3); margin:0 0 0.4rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.dk-card__price { font-size:0.82rem; color:rgba(255,255,255,0.6); margin:0; }
.dk-card__price span { font-size:0.68rem; color:rgba(255,255,255,0.3); }

.dk-compact { cursor:pointer; display:flex; flex-direction:column; background:#1a1a1a; border:1px solid rgba(255,255,255,0.07); }
.dk-compact:hover { border-color:rgba(201,146,63,0.3); }
.dk-compact__media { aspect-ratio:1/1; overflow:hidden; position:relative; background:#111; }
.dk-compact__img { width:100%; height:100%; object-fit:cover; transition:transform 0.4s; filter:brightness(0.85); }
.dk-compact:hover .dk-compact__img { transform:scale(1.05); filter:brightness(0.95); }
.dk-compact__placeholder { width:100%; height:100%; background:linear-gradient(135deg,#1e1e1e,#161616); }
.dk-compact__overlay { position:absolute; inset:0; background:linear-gradient(to top, rgba(0,0,0,0.7) 0%, transparent 50%); display:flex; align-items:flex-end; padding:0.75rem; opacity:0; transition:opacity 0.25s; }
.dk-compact:hover .dk-compact__overlay { opacity:1; }
.dk-compact__price { font-size:0.8rem; color:#fff; margin:0; }
.dk-compact__price span { font-size:0.65rem; opacity:0.65; }
.dk-compact__body { padding:0.6rem 0.75rem; }
.dk-compact__title { font-size:0.82rem; font-weight:400; color:rgba(255,255,255,0.8); margin:0 0 0.15rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.dk-compact__sub { font-size:0.68rem; color:rgba(255,255,255,0.3); margin:0; }

.dk-card-h { cursor:pointer; display:flex; background:#1a1a1a; border-bottom:1px solid rgba(255,255,255,0.07); height:120px; overflow:hidden; transition:background 0.15s; }
.dk-card-h:hover { background:#1f1f1f; }
.dk-card-h__media { width:95px; min-width:95px; overflow:hidden; }
.dk-card-h__img { width:100%; height:100%; object-fit:cover; filter:brightness(0.8); }
.dk-card-h__placeholder { width:100%; height:100%; background:linear-gradient(135deg,#1e1e1e,#161616); }
.dk-card-h__body { flex:1; padding:0.85rem 1rem; display:flex; flex-direction:column; justify-content:center; gap:0.25rem; min-width:0; }
.dk-card-h__origin { font-size:0.62rem; letter-spacing:0.1em; text-transform:uppercase; color:#C9923F; font-weight:500; }
.dk-card-h__title { font-size:0.85rem; font-weight:400; color:rgba(255,255,255,0.8); margin:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.dk-card-h__price { font-size:0.78rem; color:rgba(255,255,255,0.5); }
.dk-card-h__price span { font-size:0.65rem; color:rgba(255,255,255,0.3); }
</style>
