<template>
  <section v-if="variants?.length" class="variant-picker">
    <div class="variant-picker__header">
      <span class="variant-picker__label">انتخاب ویژگی‌ها</span>
      <span v-if="modelValue" class="variant-picker__selected-name">{{ modelValue.title }}</span>
    </div>

    <div v-if="attributeGroups.length" class="variant-picker__groups">
      <div v-for="group in attributeGroups" :key="group.attribute" class="variant-group">
        <div class="variant-group__title">{{ group.title }}</div>
        <div class="variant-group__options">
          <button
            v-for="value in group.values"
            :key="`${group.attribute}:${value}`"
            type="button"
            class="variant-chip"
            :class="{ 'variant-chip--active': selected[group.attribute] === value }"
            :disabled="!isValueAvailable(group.attribute, value)"
            @click="selectValue(group.attribute, value)"
          >
            {{ value }}
          </button>
        </div>
      </div>
    </div>

    <div v-else class="variant-picker__list">
      <button
        v-for="variant in variants"
        :key="variant.name"
        type="button"
        class="variant-btn"
        :class="{ 'variant-btn--active': modelValue?.name === variant.name }"
        @click="emitVariant(variant)"
      >
        <span class="variant-btn__title">{{ variant.title }}</span>
        <span class="variant-btn__price">
          {{ formatPrice(variant.effective_price_toman) }}
          <small>تومان</small>
        </span>
      </button>
    </div>

    <p v-if="attributeGroups.length && !modelValue" class="variant-picker__hint">
      لطفاً همه ویژگی‌های محصول را انتخاب کنید.
    </p>
  </section>
</template>

<script setup>
import { computed, reactive, watch } from 'vue'

const props = defineProps({
  variants:          { type: Array,  default: () => [] },
  variantAttributes: { type: Array,  default: () => [] },
  modelValue:        { type: Object, default: null },
})

const emit = defineEmits(['update:modelValue'])
const selected = reactive({})

const formatPrice = (v) => Number(v || 0).toLocaleString('fa-IR')

const attributeGroups = computed(() => {
  const fromTemplate = (props.variantAttributes || [])
    .filter((attr) => !attr.numeric_values)
    .map((attr) => ({
      attribute: attr.attribute,
      title: attr.title || attr.attribute,
      values: (attr.values || []).map((row) => row.value || row.title).filter(Boolean),
    }))
    .filter((attr) => attr.values.length)

  if (fromTemplate.length) return fromTemplate

  const groups = new Map()
  ;(props.variants || []).forEach((variant) => {
    ;(variant.attributes || []).forEach((row) => {
      const value = row.attribute_value || row.option_title
      if (!row.attribute || !value) return
      if (!groups.has(row.attribute)) {
        groups.set(row.attribute, {
          attribute: row.attribute,
          title: row.attribute_title || row.attribute,
          values: [],
        })
      }
      const group = groups.get(row.attribute)
      if (!group.values.includes(value)) group.values.push(value)
    })
  })

  return Array.from(groups.values())
})

const variantMatches = (variant, choices, partial = false) => {
  const attrs = new Map(
    (variant.attributes || []).map((row) => [row.attribute, row.attribute_value || row.option_title]),
  )

  return Object.entries(choices).every(([attribute, value]) => {
    if (!value) return true
    if (partial && !attrs.has(attribute)) return true
    return attrs.get(attribute) === value
  })
}

function findMatchingVariant(choices = selected) {
  const required = attributeGroups.value.map((group) => group.attribute)
  const complete = required.every((attribute) => choices[attribute])
  if (!complete) return null
  return (props.variants || []).find((variant) => variantMatches(variant, choices)) || null
}

function isValueAvailable(attribute, value) {
  const choices = { ...selected, [attribute]: value }
  return (props.variants || []).some((variant) => variantMatches(variant, choices, true))
}

function selectValue(attribute, value) {
  selected[attribute] = selected[attribute] === value ? '' : value
  emit('update:modelValue', findMatchingVariant())
}

function emitVariant(variant) {
  emit('update:modelValue', variant)
}

function syncSelectedFromVariant(variant) {
  Object.keys(selected).forEach((key) => delete selected[key])
  ;(variant?.attributes || []).forEach((row) => {
    const value = row.attribute_value || row.option_title
    if (row.attribute && value) selected[row.attribute] = value
  })
}

watch(
  () => props.modelValue?.name,
  () => syncSelectedFromVariant(props.modelValue),
  { immediate: true },
)
</script>

<style scoped>
.variant-picker {
  margin: 1.5rem 0;
}

.variant-picker__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.85rem;
}

.variant-picker__label {
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.72rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #9e9890;
}

.variant-picker__selected-name,
.variant-picker__hint {
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.78rem;
  color: #6b6560;
}

.variant-picker__groups,
.variant-picker__list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.variant-group__title {
  margin-bottom: 0.45rem;
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.82rem;
  color: #3f3a36;
}

.variant-group__options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
}

.variant-chip,
.variant-btn {
  border: 1px solid #E8E4DE;
  background-color: #FAFAF8;
  cursor: pointer;
  font-family: 'Vazirmatn', sans-serif;
  transition: border-color 0.2s, background-color 0.2s, color 0.2s;
}

.variant-chip {
  min-height: 38px;
  padding: 0 0.85rem;
  color: #222;
}

.variant-chip:hover:not(:disabled),
.variant-btn:hover {
  border-color: #bbb5ad;
  background-color: #F5F3F0;
}

.variant-chip--active,
.variant-btn--active {
  border-color: #800000;
  background-color: #fff;
  color: #800000;
}

.variant-chip:disabled {
  color: #b8b1a9;
  cursor: not-allowed;
  opacity: 0.55;
}

.variant-btn {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.85rem 1rem;
  text-align: right;
}

.variant-btn__title {
  font-size: 0.88rem;
  font-weight: 400;
  color: inherit;
}

.variant-btn__price {
  font-size: 0.82rem;
  color: #6b6560;
  font-weight: 300;
}

.variant-btn__price small {
  font-size: 0.7rem;
  color: #9e9890;
  margin-right: 0.25rem;
}
</style>
