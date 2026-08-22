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
  if (props.product.type === 'accessory') return { origin: props.product.category_title || props.product.category, roast: props.product.brand, notes: props.product.specs?.slice(0,2).map(s=>s.value).join(' · ') };
  return { origin: props.product.origin, roast: props.product.roast, notes: props.product.notes?.join(' · ') };
});
</script>

<template>
  <!-- Standard -->
  <article v-if="cardVariant === 'standard'" class="ea-card" @click="$router.push(`/products/${product.slug || product.id}`)">
    <div class="ea-card__media">
      <img v-if="product.image" :src="product.image" :alt="product.name" class="ea-card__img" />
      <div v-else class="ea-card__placeholder" />
      <button class="ea-card__wish" :class="{'ea-card__wish--on': wishlistStore.isWishlisted(product.id)}" @click.stop="wishlistStore.toggle(product.id)">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
      </button>
    </div>
    <div class="ea-card__body">
      <div class="ea-card__meta"><span class="ea-card__origin">{{ meta.origin }}</span><span class="ea-card__roast">{{ meta.roast }}</span></div>
      <h3 class="ea-card__title">{{ product.name }}</h3>
      <p class="ea-card__notes">{{ meta.notes }}</p>
      <p class="ea-card__price">{{ formatPrice(product.price) }} <span>تومان</span></p>
    </div>
  </article>

  <!-- Compact -->
  <article v-else-if="cardVariant === 'compact'" class="ea-compact" @click="$router.push(`/products/${product.slug || product.id}`)">
    <div class="ea-compact__media">
      <img v-if="product.image" :src="product.image" :alt="product.name" class="ea-compact__img" />
      <div v-else class="ea-compact__placeholder" />
      <div class="ea-compact__overlay"><p class="ea-compact__price">{{ formatPrice(product.price) }} <span>تومان</span></p></div>
    </div>
    <div class="ea-compact__body">
      <h3 class="ea-compact__title">{{ product.name }}</h3>
      <p class="ea-compact__sub">{{ meta.origin }}</p>
    </div>
  </article>

  <!-- Horizontal -->
  <article v-else class="ea-card-h" @click="$router.push(`/products/${product.slug || product.id}`)">
    <div class="ea-card-h__media">
      <img v-if="product.image" :src="product.image" :alt="product.name" class="ea-card-h__img" />
      <div v-else class="ea-card-h__placeholder" />
    </div>
    <div class="ea-card-h__body">
      <div class="ea-card-h__origin">{{ meta.origin }}</div>
      <h3 class="ea-card-h__title">{{ product.name }}</h3>
      <p class="ea-card-h__price">{{ formatPrice(product.price) }} <span>تومان</span></p>
    </div>
  </article>
</template>

<style scoped>
.ea-card { cursor:pointer; display:flex; flex-direction:column; background:#FDFAF5; border:1.5px solid #D6CBB8; border-radius:12px; overflow:hidden; transition:transform 0.22s, box-shadow 0.22s; }
.ea-card:hover { transform:translateY(-4px); box-shadow:0 12px 32px rgba(45,36,22,0.12); }
.ea-card:hover .ea-card__title { color:#4a7c59; }
.ea-card__media { aspect-ratio:4/5; overflow:hidden; position:relative; background:#EDE5D6; border-radius:10px 10px 0 0; }
.ea-card__img { width:100%; height:100%; object-fit:contain; padding:8px; transition:transform 0.45s cubic-bezier(0.25,0.46,0.45,0.94); }
.ea-card:hover .ea-card__img { transform:scale(1.04); }
.ea-card__placeholder { width:100%; height:100%; background:linear-gradient(135deg,#E8DFC9,#DDD3BC); }
.ea-card__wish { position:absolute; top:0.75rem; left:0.75rem; width:30px; height:30px; display:flex; align-items:center; justify-content:center; background:rgba(253,250,245,0.9); backdrop-filter:blur(4px); border:1.5px solid #D6CBB8; border-radius:50%; cursor:pointer; color:#9e8a72; opacity:0; transform:scale(0.8); transition:all 0.2s; }
.ea-card:hover .ea-card__wish { opacity:1; transform:scale(1); }
.ea-card__wish--on { opacity:1!important; transform:scale(1)!important; color:#4a7c59; }
.ea-card__wish--on svg { fill:#4a7c59; }
.ea-card__body { padding:0.9rem; border-top:1.5px solid #D6CBB8; }
.ea-card__meta { display:flex; align-items:center; justify-content:space-between; margin-bottom:0.35rem; }
.ea-card__origin { font-size:0.68rem; letter-spacing:0.1em; color:#4a7c59; text-transform:uppercase; font-weight:600; }
.ea-card__roast { font-size:0.65rem; color:#9e8a72; background:#EDE5D6; padding:0.15rem 0.5rem; border-radius:9999px; }
.ea-card__title { font-size:0.88rem; font-weight:500; color:#2d2416; margin:0 0 0.25rem; transition:color 0.2s; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.ea-card__notes { font-size:0.7rem; color:#9e8a72; margin:0 0 0.4rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.ea-card__price { font-size:0.82rem; color:#4a5540; margin:0; font-weight:500; }
.ea-card__price span { font-size:0.68rem; color:#9e8a72; font-weight:400; }

.ea-compact { cursor:pointer; display:flex; flex-direction:column; background:#FDFAF5; border:1.5px solid #D6CBB8; border-radius:12px; overflow:hidden; transition:transform 0.22s; }
.ea-compact:hover { transform:translateY(-3px); }
.ea-compact__media { aspect-ratio:1/1; overflow:hidden; position:relative; }
.ea-compact__img { width:100%; height:100%; object-fit:contain; padding:6px; transition:transform 0.4s; }
.ea-compact:hover .ea-compact__img { transform:scale(1.05); }
.ea-compact__placeholder { width:100%; height:100%; background:linear-gradient(135deg,#E8DFC9,#DDD3BC); }
.ea-compact__overlay { position:absolute; inset:0; background:linear-gradient(to top, rgba(30,20,8,0.55) 0%, transparent 55%); display:flex; align-items:flex-end; padding:0.75rem; opacity:0; transition:opacity 0.25s; }
.ea-compact:hover .ea-compact__overlay { opacity:1; }
.ea-compact__price { font-size:0.8rem; color:#fff; margin:0; }
.ea-compact__price span { font-size:0.65rem; opacity:0.75; }
.ea-compact__body { padding:0.65rem 0.85rem; }
.ea-compact__title { font-size:0.82rem; font-weight:500; color:#2d2416; margin:0 0 0.15rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.ea-compact__sub { font-size:0.68rem; color:#9e8a72; margin:0; }

.ea-card-h { cursor:pointer; display:flex; background:#FDFAF5; border-bottom:1.5px solid #D6CBB8; height:120px; overflow:hidden; transition:background 0.15s; }
.ea-card-h:hover { background:#F5EFE4; }
.ea-card-h:hover .ea-card-h__title { color:#4a7c59; }
.ea-card-h__media { width:100px; min-width:100px; overflow:hidden; border-radius:8px 0 0 8px; }
.ea-card-h__img { width:100%; height:100%; object-fit:contain; padding:4px; }
.ea-card-h__placeholder { width:100%; height:100%; background:linear-gradient(135deg,#E8DFC9,#DDD3BC); }
.ea-card-h__body { flex:1; padding:0.85rem 1rem; display:flex; flex-direction:column; justify-content:center; gap:0.25rem; min-width:0; }
.ea-card-h__origin { font-size:0.62rem; letter-spacing:0.1em; text-transform:uppercase; color:#4a7c59; font-weight:600; }
.ea-card-h__title { font-size:0.85rem; font-weight:500; color:#2d2416; margin:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; transition:color 0.2s; }
.ea-card-h__price { font-size:0.78rem; color:#4a5540; font-weight:500; }
.ea-card-h__price span { font-size:0.65rem; color:#9e8a72; font-weight:400; }
</style>
