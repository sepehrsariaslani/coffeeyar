<script setup>
import { computed } from 'vue'
import { toFa } from '@/lib/utils.js'

const props = defineProps({
  traits:  { type: Array,  required: true },
  ratings: { type: Object, required: true },
})

const SIZE = 260
const cx = SIZE / 2
const cy = SIZE / 2
const R  = 90

const N = computed(() => props.traits.length)

function angleRad(i) {
  return ((-90 + (360 / N.value) * i) * Math.PI) / 180
}

function vertex(i, r) {
  return [cx + Math.cos(angleRad(i)) * r, cy + Math.sin(angleRad(i)) * r]
}

const grid = computed(() =>
  [0.25, 0.5, 0.75, 1].map(s =>
    Array.from({ length: N.value }, (_, i) => vertex(i, R * s).join(',')).join(' ')
  )
)

const valuePoints = computed(() =>
  props.traits.map((t, i) => {
    const v = Math.min(10, Math.max(0, props.ratings[t.id] ?? 0))
    return vertex(i, (R * v) / 10).join(',')
  }).join(' ')
)

function valueDot(i) {
  const v = Math.min(10, Math.max(0, props.ratings[props.traits[i].id] ?? 0))
  return vertex(i, (R * v) / 10)
}

function labelPos(i) {
  const a = angleRad(i)
  return [cx + Math.cos(a) * (R + 26), cy + Math.sin(a) * (R + 26)]
}

const axes = computed(() =>
  Array.from({ length: N.value }, (_, i) => ({ outer: vertex(i, R), i }))
)

const VB = SIZE + 80
</script>

<template>
  <div class="flex flex-col items-center">
    <svg
      :width="VB"
      :height="VB"
      :viewBox="`-40 -40 ${VB} ${VB}`"
      overflow="visible"
    >
      <polygon
        v-for="(pts, gi) in grid"
        :key="gi"
        :points="pts"
        fill="none"
        stroke="var(--border)"
        stroke-width="1"
      />

      <line
        v-for="ax in axes"
        :key="ax.i"
        :x1="cx" :y1="cy"
        :x2="ax.outer[0]" :y2="ax.outer[1]"
        stroke="var(--border)"
        stroke-width="1"
      />

      <polygon
        :points="valuePoints"
        fill="var(--maroon)"
        fill-opacity="0.18"
        stroke="var(--maroon)"
        stroke-width="1.5"
      />

      <circle
        v-for="(t, i) in traits"
        :key="t.id"
        :cx="valueDot(i)[0]"
        :cy="valueDot(i)[1]"
        r="4"
        fill="var(--maroon)"
      />

      <g v-for="(t, i) in traits" :key="t.id + '-lbl'">
        <text
          :x="labelPos(i)[0]"
          :y="labelPos(i)[1] - 7"
          text-anchor="middle"
          dominant-baseline="middle"
          font-size="11"
          fill="var(--foreground)"
          font-family="Vazirmatn"
        >{{ t.name }}</text>
        <text
          :x="labelPos(i)[0]"
          :y="labelPos(i)[1] + 8"
          text-anchor="middle"
          dominant-baseline="middle"
          font-size="10"
          fill="var(--maroon)"
          font-family="Vazirmatn"
        >{{ toFa(ratings[t.id] ?? 0) }}/۱۰</text>
      </g>
    </svg>
  </div>
</template>
