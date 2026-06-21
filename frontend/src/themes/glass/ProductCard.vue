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
const formatPrice = (v) => Number(v || 0).toLocaleString('fa-IR');
const meta = computed(() => {
  if (props.product.type === 'accessory') return { origin: props.product.category, roast: props.product.brand, notes: props.product.specs?.slice(0,2).map(s=>s.value).join(' · ') };
  return { origin: props.product.origin, roast: props.product.roast, notes: props.product.notes?.join(' · ') };
});
</script>

<template>
  <!-- Standard -->
  <article v-if="cardVariant === 'standard'" class="gl-card" @click="$router.push(`/products/${product.slug || product.id}`)">
    <div class="gl-card__media">
      <img v-if="product.image" :src="product.image" :alt="product.name" class="gl-card__img" />
      <div v-else class="gl-card__placeholder" />
      <button class="gl-card__wish" :class="{'gl-card__wish--on': wishlistStore.isWishlisted(product.id)}" @click.stop="wishlistStore.toggle(product.id)">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
      </button>
      <span v-if="meta.roast" class="gl-card__badge">{{ meta.roast }}</span>
    </div>
    <div class="gl-card__body">
      <div class="gl-card__origin">{{ meta.origin }}</div>
      <h3 class="gl-card__title">{{ product.name }}</h3>
      <p class="gl-card__notes">{{ meta.notes }}</p>
      <p class="gl-card__price">{{ formatPrice(product.price) }} <span>تومان</span></p>
    </div>
  </article>

  <!-- Compact -->
  <article v-else-if="cardVariant === 'compact'" class="gl-compact" @click="$router.push(`/products/${product.slug || product.id}`)">
    <div class="gl-compact__media">
      <img v-if="product.image" :src="product.image" :alt="product.name" class="gl-compact__img" />
      <div v-else class="gl-compact__placeholder" />
      <div class="gl-compact__overlay"><p class="gl-compact__price">{{ formatPrice(product.price) }} <span>تومان</span></p></div>
    </div>
    <div class="gl-compact__body">
      <h3 class="gl-compact__title">{{ product.name }}</h3>
      <p class="gl-compact__sub">{{ meta.origin }}</p>
    </div>
  </article>

  <!-- Horizontal -->
  <article v-else class="gl-card-h" @click="$router.push(`/products/${product.slug || product.id}`)">
    <div class="gl-card-h__media">
      <img v-if="product.image" :src="product.image" :alt="product.name" class="gl-card-h__img" />
      <div v-else class="gl-card-h__placeholder" />
    </div>
    <div class="gl-card-h__body">
      <div class="gl-card-h__origin">{{ meta.origin }}</div>
      <h3 class="gl-card-h__title">{{ product.name }}</h3>
      <p class="gl-card-h__price">{{ formatPrice(product.price) }} <span>تومان</span></p>
    </div>
  </article>
</template>

<style scoped>
/* ── Standard ── */
.gl-card {
  cursor: pointer;
  display: flex; flex-direction: column;
  background: rgba(255,255,255,0.44);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255,255,255,0.65);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: inset 0 1.5px 0 rgba(255,255,255,0.8), 0 8px 32px rgba(100,60,220,0.10), 0 2px 8px rgba(0,0,0,0.05);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.gl-card:hover {
  transform: translateY(-5px);
  box-shadow: inset 0 1.5px 0 rgba(255,255,255,0.8), 0 20px 48px rgba(100,60,220,0.18), 0 4px 12px rgba(0,0,0,0.08);
}
.gl-card__media { aspect-ratio: 4/5; overflow: hidden; position: relative; }
.gl-card__img { width:100%; height:100%; object-fit:contain; padding:8px; transition: transform 0.5s cubic-bezier(0.25,0.46,0.45,0.94); }
.gl-card:hover .gl-card__img { transform: scale(1.05); }
.gl-card__placeholder { width:100%; height:100%; background: linear-gradient(135deg, rgba(180,140,255,0.35), rgba(140,200,255,0.35)); }
.gl-card__wish {
  position: absolute; top: 0.7rem; left: 0.7rem;
  width: 30px; height: 30px;
  display: flex; align-items: center; justify-content: center;
  background: rgba(255,255,255,0.7); backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.85); border-radius: 50%;
  cursor: pointer; color: rgba(80,60,150,0.55);
  opacity: 0; transform: scale(0.75);
  transition: all 0.2s;
}
.gl-card:hover .gl-card__wish { opacity: 1; transform: scale(1); }
.gl-card__wish--on { opacity: 1 !important; transform: scale(1) !important; color: oklch(0.46 0.22 278); }
.gl-card__wish--on svg { fill: oklch(0.46 0.22 278); }
.gl-card__badge {
  position: absolute; top: 0.7rem; right: 0.7rem;
  font-size: 0.62rem; letter-spacing: 0.08em;
  background: rgba(100,60,220,0.65); backdrop-filter: blur(6px);
  color: #fff; padding: 0.2rem 0.55rem; border-radius: 0.4rem;
  border: 1px solid rgba(255,255,255,0.35);
}
.gl-card__body { padding: 0.9rem 1rem; }
.gl-card__origin { font-size: 0.66rem; letter-spacing: 0.12em; text-transform: uppercase; color: oklch(0.46 0.22 278); font-weight: 600; margin-bottom: 0.3rem; }
.gl-card__title { font-size: 0.88rem; font-weight: 500; color: rgba(15,8,40,0.85); margin: 0 0 0.25rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; transition: color 0.2s; }
.gl-card:hover .gl-card__title { color: oklch(0.38 0.22 278); }
.gl-card__notes { font-size: 0.7rem; color: rgba(20,10,60,0.45); margin: 0 0 0.5rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.gl-card__price { font-size: 0.82rem; color: rgba(15,8,40,0.7); margin: 0; }
.gl-card__price span { font-size: 0.68rem; color: rgba(20,10,60,0.4); }

/* ── Compact ── */
.gl-compact { cursor:pointer; background: rgba(255,255,255,0.44); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.65); border-radius: 16px; overflow: hidden; transition: transform 0.25s; }
.gl-compact:hover { transform: translateY(-4px); }
.gl-compact__media { aspect-ratio: 1/1; position: relative; overflow: hidden; }
.gl-compact__img { width:100%; height:100%; object-fit:contain; padding:6px; transition: transform 0.45s; }
.gl-compact:hover .gl-compact__img { transform: scale(1.06); }
.gl-compact__placeholder { width:100%; height:100%; background: linear-gradient(135deg, rgba(180,140,255,0.35), rgba(140,200,255,0.35)); }
.gl-compact__overlay { position: absolute; inset: 0; background: linear-gradient(to top, rgba(20,8,60,0.5) 0%, transparent 55%); display: flex; align-items: flex-end; padding: 0.75rem; opacity: 0; transition: opacity 0.25s; }
.gl-compact:hover .gl-compact__overlay { opacity: 1; }
.gl-compact__price { font-size: 0.8rem; color: #fff; margin: 0; }
.gl-compact__price span { font-size: 0.65rem; opacity: 0.75; }
.gl-compact__body { padding: 0.6rem 0.85rem; }
.gl-compact__title { font-size: 0.82rem; font-weight: 500; color: rgba(15,8,40,0.85); margin: 0 0 0.15rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.gl-compact__sub { font-size: 0.68rem; color: rgba(20,10,60,0.5); margin: 0; }

/* ── Horizontal ── */
.gl-card-h { cursor:pointer; display:flex; background: rgba(255,255,255,0.44); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.65); border-radius: 14px; overflow:hidden; height:110px; transition: transform 0.2s; }
.gl-card-h:hover { transform: translateY(-2px); }
.gl-card-h__media { width:90px; min-width:90px; overflow:hidden; }
.gl-card-h__img { width:100%; height:100%; object-fit:contain; padding:4px; }
.gl-card-h__placeholder { width:100%; height:100%; background: linear-gradient(135deg, rgba(180,140,255,0.3), rgba(140,200,255,0.3)); }
.gl-card-h__body { flex:1; padding:0.75rem 1rem; display:flex; flex-direction:column; justify-content:center; gap:0.25rem; min-width:0; }
.gl-card-h__origin { font-size:0.62rem; letter-spacing:0.1em; text-transform:uppercase; color: oklch(0.46 0.22 278); font-weight:600; }
.gl-card-h__title { font-size:0.84rem; font-weight:500; color:rgba(15,8,40,0.85); margin:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.gl-card-h__price { font-size:0.78rem; color:rgba(15,8,40,0.65); }
.gl-card-h__price span { font-size:0.65rem; color:rgba(20,10,60,0.4); }
</style>
