<script setup>
import { toFa } from "@/lib/utils.js";

const props = defineProps({
  flavor: Object,
});

const size = 280;
const cx = size / 2;
const cy = size / 2 + 12;
const R = 110;

const angles = [-90, 150, 30];
const labels = ["عطر", "اسیدیته", "تلخی"];

function vertex(i, r) {
  const a = (angles[i] * Math.PI) / 180;
  return [cx + Math.cos(a) * r, cy + Math.sin(a) * r];
}

const outer = [0, 1, 2].map((i) => vertex(i, R));

const grid = [0.25, 0.5, 0.75, 1].map((s) =>
  [0, 1, 2].map((i) => vertex(i, R * s).join(",")).join(" ")
);

function valPoints() {
  const values = [props.flavor.aroma, props.flavor.acidity, props.flavor.bitterness];
  return [0, 1, 2]
    .map((i) => vertex(i, (R * values[i]) / 10).join(","))
    .join(" ");
}

function valueDot(i) {
  const values = [props.flavor.aroma, props.flavor.acidity, props.flavor.bitterness];
  return vertex(i, (R * values[i]) / 10);
}

function labelPos(i) {
  const a = (angles[i] * Math.PI) / 180;
  return [cx + Math.cos(a) * (R + 22), cy + Math.sin(a) * (R + 22)];
}

function getValue(i) {
  return [props.flavor.aroma, props.flavor.acidity, props.flavor.bitterness][i];
}
</script>

<template>
  <div class="flex flex-col items-center">
    <svg :width="size" :height="size + 20" :viewBox="`0 0 ${size} ${size + 20}`">
      <polygon
        v-for="(pts, i) in grid"
        :key="i"
        :points="pts"
        fill="none"
        stroke="var(--border)"
        stroke-width="1"
      />
      <line
        v-for="([x, y], i) in outer"
        :key="i"
        :x1="cx"
        :y1="cy"
        :x2="x"
        :y2="y"
        stroke="var(--border)"
        stroke-width="1"
      />
      <polygon
        :points="valPoints()"
        fill="var(--maroon)"
        fill-opacity="0.18"
        stroke="var(--maroon)"
        stroke-width="1.5"
      />
      <circle
        v-for="i in [0, 1, 2]"
        :key="i"
        :cx="valueDot(i)[0]"
        :cy="valueDot(i)[1]"
        r="4"
        fill="var(--maroon)"
      />
      <g v-for="i in [0, 1, 2]" :key="i">
        <text
          :x="labelPos(i)[0]"
          :y="labelPos(i)[1]"
          text-anchor="middle"
          dominant-baseline="middle"
          font-size="12"
          fill="var(--foreground)"
          font-family="Vazirmatn"
        >
          {{ labels[i] }}
        </text>
        <text
          :x="labelPos(i)[0]"
          :y="labelPos(i)[1] + 14"
          text-anchor="middle"
          dominant-baseline="middle"
          font-size="11"
          fill="var(--maroon)"
          font-family="Vazirmatn"
        >
          {{ toFa(getValue(i)) }} / ۱۰
        </text>
      </g>
    </svg>
  </div>
</template>
