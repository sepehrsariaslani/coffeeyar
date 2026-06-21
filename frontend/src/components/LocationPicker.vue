<template>
  <!-- Trigger button -->
  <button type="button" class="loc-trigger" @click="open = true">
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
      <circle cx="12" cy="9" r="2.5"/>
    </svg>
    {{ coords ? 'ویرایش موقعیت روی نقشه' : 'انتخاب موقعیت روی نقشه' }}
  </button>

  <!-- Mini preview -->
  <div v-if="coords" class="loc-preview">
    <div ref="previewMapEl" class="loc-preview__map" />
    <div class="loc-preview__meta">
      <span class="loc-preview__coords">{{ coords[0].toFixed(5) }}, {{ coords[1].toFixed(5) }}</span>
      <button type="button" class="loc-preview__remove" @click="removeCoords">حذف موقعیت</button>
    </div>
  </div>

  <!-- Modal -->
  <teleport to="body">
    <div v-if="open" class="loc-modal-backdrop" @click.self="cancel">
      <div class="loc-modal">
        <header class="loc-modal__header">
          <div>
            <div class="loc-modal__title">انتخاب موقعیت روی نقشه</div>
            <div class="loc-modal__hint">روی نقشه کلیک کنید تا موقعیت مشخص شود</div>
          </div>
          <button type="button" class="loc-modal__close" @click="cancel">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
        </header>

        <div class="loc-modal__search">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="جستجوی آدرس..."
            class="loc-modal__search-input"
            @keydown.enter.prevent="searchAddress"
          />
          <button type="button" class="loc-modal__search-btn" @click="searchAddress" :disabled="searching">
            <span v-if="searching" class="loc-modal__spinner" />
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
              <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
            </svg>
          </button>
        </div>

        <div ref="mapEl" class="loc-modal__map" />

        <div v-if="pendingCoords" class="loc-modal__result">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#800000" stroke-width="2" stroke-linecap="round">
            <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/>
          </svg>
          <span v-if="reversing">در حال شناسایی آدرس...</span>
          <span v-else>{{ pendingAddress || `${pendingCoords[0].toFixed(4)}, ${pendingCoords[1].toFixed(4)}` }}</span>
        </div>

        <footer class="loc-modal__footer">
          <button type="button" class="loc-modal__btn-cancel" @click="cancel">انصراف</button>
          <button type="button" class="loc-modal__btn-confirm" :disabled="!pendingCoords" @click="confirm">
            تأیید موقعیت
          </button>
        </footer>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { ref, watch, nextTick, onUnmounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix default marker icons
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
})

const props = defineProps({
  modelValue: { type: Array, default: null },
})

const emit = defineEmits(['update:modelValue', 'address-resolved'])

const open = ref(false)
const mapEl = ref(null)
const previewMapEl = ref(null)
const coords = ref(props.modelValue || null)
const pendingCoords = ref(null)
const pendingAddress = ref('')
const reversing = ref(false)
const searching = ref(false)
const searchQuery = ref('')

let mainMap = null
let mainMarker = null
let previewMap = null

const IRAN_CENTER = [32.4279, 53.6880]
const IRAN_ZOOM = 5

function initMainMap() {
  if (!mapEl.value || mainMap) return
  mainMap = L.map(mapEl.value, { center: IRAN_CENTER, zoom: IRAN_ZOOM })
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap',
    maxZoom: 19,
  }).addTo(mainMap)

  if (coords.value) {
    mainMarker = L.marker(coords.value, { draggable: true }).addTo(mainMap)
    mainMap.setView(coords.value, 14)
    pendingCoords.value = coords.value
    mainMarker.on('dragend', () => {
      const ll = mainMarker.getLatLng()
      setPending([ll.lat, ll.lng])
    })
  }

  mainMap.on('click', (e) => {
    const ll = [e.latlng.lat, e.latlng.lng]
    if (mainMarker) {
      mainMarker.setLatLng(ll)
    } else {
      mainMarker = L.marker(ll, { draggable: true }).addTo(mainMap)
      mainMarker.on('dragend', () => {
        const p = mainMarker.getLatLng()
        setPending([p.lat, p.lng])
      })
    }
    setPending(ll)
  })
}

async function setPending(ll) {
  pendingCoords.value = ll
  pendingAddress.value = ''
  reversing.value = true
  try {
    const res = await fetch(
      `https://nominatim.openstreetmap.org/reverse?lat=${ll[0]}&lon=${ll[1]}&format=json&accept-language=fa`,
      { headers: { 'Accept-Language': 'fa' } }
    )
    const data = await res.json()
    if (data.address) {
      const a = data.address
      const province = a.province || a.state || a.county || ''
      const city = a.city || a.town || a.village || ''
      pendingAddress.value = data.display_name?.split(',').slice(0, 3).join('، ') || ''
      emit('address-resolved', { province, city, display: pendingAddress.value })
    }
  } catch { /* ignore */ } finally {
    reversing.value = false
  }
}

async function searchAddress() {
  if (!searchQuery.value.trim()) return
  searching.value = true
  try {
    const res = await fetch(
      `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(searchQuery.value)}&format=json&limit=1&accept-language=fa&countrycodes=ir`
    )
    const data = await res.json()
    if (data[0]) {
      const ll = [parseFloat(data[0].lat), parseFloat(data[0].lon)]
      mainMap.setView(ll, 15)
      if (mainMarker) {
        mainMarker.setLatLng(ll)
      } else {
        mainMarker = L.marker(ll, { draggable: true }).addTo(mainMap)
        mainMarker.on('dragend', () => {
          const p = mainMarker.getLatLng()
          setPending([p.lat, p.lng])
        })
      }
      await setPending(ll)
    }
  } catch { /* ignore */ } finally {
    searching.value = false
  }
}

function confirm() {
  coords.value = pendingCoords.value
  emit('update:modelValue', coords.value)
  open.value = false
  destroyMainMap()
  nextTick(initPreviewMap)
}

function cancel() {
  open.value = false
  destroyMainMap()
}

function removeCoords() {
  coords.value = null
  pendingCoords.value = null
  emit('update:modelValue', null)
  destroyPreviewMap()
}

function destroyMainMap() {
  if (mainMap) { mainMap.remove(); mainMap = null; mainMarker = null }
}

function destroyPreviewMap() {
  if (previewMap) { previewMap.remove(); previewMap = null }
}

function initPreviewMap() {
  if (!previewMapEl.value || !coords.value) return
  if (previewMap) previewMap.remove()
  previewMap = L.map(previewMapEl.value, {
    center: coords.value, zoom: 14,
    zoomControl: false, attributionControl: false,
    dragging: false, scrollWheelZoom: false, doubleClickZoom: false,
    touchZoom: false, keyboard: false,
  })
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(previewMap)
  L.marker(coords.value).addTo(previewMap)
}

watch(open, async (val) => {
  if (val) {
    pendingCoords.value = coords.value || null
    pendingAddress.value = ''
    await nextTick()
    initMainMap()
  }
})

watch(() => props.modelValue, (val) => { coords.value = val })

onUnmounted(() => { destroyMainMap(); destroyPreviewMap() })
</script>

<style scoped>
.loc-trigger {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.8rem;
  color: #3f3a36;
  border: 1px dashed #C8C2BA;
  background: #FAFAF8;
  padding: 0.55rem 1rem;
  cursor: pointer;
  transition: border-color 0.2s, color 0.2s;
}
.loc-trigger:hover { border-color: #800000; color: #800000; }

.loc-preview { margin-top: 0.75rem; border: 1px solid #E8E4DE; overflow: hidden; }
.loc-preview__map { height: 120px; pointer-events: none; }
.loc-preview__meta {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0.5rem 0.75rem; background: #FAFAF8;
}
.loc-preview__coords { font-family: 'Vazirmatn', sans-serif; font-size: 0.7rem; color: #9e9890; direction: ltr; }
.loc-preview__remove {
  font-family: 'Vazirmatn', sans-serif; font-size: 0.7rem; color: #9e9890;
  background: none; border: none; cursor: pointer; padding: 0;
}
.loc-preview__remove:hover { color: #800000; }

.loc-modal-backdrop {
  position: fixed; inset: 0; z-index: 9999;
  background: rgba(10,10,10,0.5); backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center; padding: 1rem;
}
.loc-modal {
  background: #fff; width: 100%; max-width: 680px;
  max-height: 90vh; display: flex; flex-direction: column;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}
.loc-modal__header {
  display: flex; align-items: flex-start; justify-content: space-between;
  padding: 1.25rem 1.5rem; border-bottom: 1px solid #E8E4DE;
}
.loc-modal__title { font-family: 'Vazirmatn', sans-serif; font-size: 0.95rem; font-weight: 500; color: #1a1a1a; }
.loc-modal__hint { font-family: 'Vazirmatn', sans-serif; font-size: 0.75rem; color: #9e9890; margin-top: 0.2rem; }
.loc-modal__close {
  padding: 0.25rem; background: none; border: none; cursor: pointer;
  color: #9e9890; transition: color 0.2s;
}
.loc-modal__close:hover { color: #1a1a1a; }

.loc-modal__search {
  display: flex; gap: 0; border-bottom: 1px solid #E8E4DE;
}
.loc-modal__search-input {
  flex: 1; border: none; outline: none; padding: 0.75rem 1rem;
  font-family: 'Vazirmatn', sans-serif; font-size: 0.85rem; color: #1a1a1a;
  background: #FAFAF8; direction: rtl;
}
.loc-modal__search-input::placeholder { color: #9e9890; }
.loc-modal__search-btn {
  padding: 0 1rem; border: none; background: #F0EDE8; cursor: pointer;
  color: #3f3a36; display: flex; align-items: center;
  transition: background 0.2s;
}
.loc-modal__search-btn:hover { background: #E8E4DE; }
.loc-modal__search-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.loc-modal__spinner {
  width: 14px; height: 14px; border: 2px solid #C8C2BA;
  border-top-color: #800000; border-radius: 50%; animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.loc-modal__map { flex: 1; min-height: 340px; }

.loc-modal__result {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.65rem 1rem; background: #FFF8F0; border-top: 1px solid #E8E4DE;
  font-family: 'Vazirmatn', sans-serif; font-size: 0.78rem; color: #5a5550;
}

.loc-modal__footer {
  display: flex; gap: 0.75rem; padding: 1rem 1.5rem;
  border-top: 1px solid #E8E4DE; background: #FAFAF8;
}
.loc-modal__btn-cancel {
  padding: 0.6rem 1.25rem; border: 1px solid #E8E4DE; background: #fff;
  font-family: 'Vazirmatn', sans-serif; font-size: 0.85rem; cursor: pointer;
  color: #3f3a36; transition: background 0.2s;
}
.loc-modal__btn-cancel:hover { background: #F0EDE8; }
.loc-modal__btn-confirm {
  flex: 1; padding: 0.6rem 1.25rem; border: none; background: #1a1a1a;
  font-family: 'Vazirmatn', sans-serif; font-size: 0.85rem; cursor: pointer;
  color: #fff; transition: background 0.2s;
}
.loc-modal__btn-confirm:hover { background: #2d2d2d; }
.loc-modal__btn-confirm:disabled { background: #C8C2BA; cursor: not-allowed; }
</style>
