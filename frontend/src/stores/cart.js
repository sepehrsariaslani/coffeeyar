import { computed, reactive } from 'vue'

const KEY = 'coffeeyar_cart'

function load() {
  try {
    const raw = localStorage.getItem(KEY)
    if (!raw) return []
    const parsed = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

const state = reactive({
  items: typeof window !== 'undefined' ? load() : [],
})

function save() {
  if (typeof window === 'undefined') return
  localStorage.setItem(KEY, JSON.stringify(state.items))
}

function getItemKey(product, variant) {
  return variant?.name ? `${product.slug}:${variant.name}` : product.slug
}

function variantTitle(variant) {
  if (!variant) return ''
  if (variant.title) return variant.title
  return (variant.attributes || [])
    .map((row) => `${row.attribute_title || row.attribute}: ${row.attribute_value || row.option_title}`)
    .join('، ')
}

function add(product, qty = 1, variant = null) {
  const key = getItemKey(product, variant)
  const existing = state.items.find((item) => item.key === key)
  if (existing) {
    existing.qty += qty
  } else {
    state.items.push({
      key,
      slug: product.slug,
      title: product.title,
      variant_id: variant?.name || '',
      variant_title: variantTitle(variant),
      variant_attributes: variant?.attributes || [],
      qty,
      price_toman: variant?.effective_price_toman || product.effective_price_toman,
      image: variant?.image || product.image,
    })
  }
  save()
}

function remove(key) {
  state.items = state.items.filter((item) => item.key !== key)
  save()
}

function clear() {
  state.items = []
  save()
}

function setQty(key, qty) {
  const target = state.items.find((item) => item.key === key)
  if (!target) return
  target.qty = Math.max(1, Number(qty) || 1)
  save()
}

const subtotal = computed(() => state.items.reduce((sum, item) => sum + item.price_toman * item.qty, 0))
const count = computed(() => state.items.reduce((sum, item) => sum + item.qty, 0))

export function useCart() {
  return {
    state,
    add,
    remove,
    clear,
    setQty,
    subtotal,
    count,
  }
}
