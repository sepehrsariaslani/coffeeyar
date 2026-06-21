<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  coords: { type: Array, required: true },
})

const el = ref(null)
let map = null

function initMap() {
  if (!el.value || !props.coords) return
  if (map) map.remove()
  map = L.map(el.value, {
    center: props.coords,
    zoom: 14,
    zoomControl: false,
    attributionControl: false,
    dragging: false,
    scrollWheelZoom: false,
    doubleClickZoom: false,
    touchZoom: false,
    keyboard: false,
  })
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map)
  L.marker(props.coords).addTo(map)
}

onMounted(initMap)
onUnmounted(() => { if (map) map.remove() })
watch(() => props.coords, initMap)
</script>

<template>
  <div ref="el" class="addr-mini-map" />
</template>

<style scoped>
.addr-mini-map {
  height: 130px;
  width: 100%;
  pointer-events: none;
}
</style>
