<script setup>
import { ref, watch, onMounted } from "vue";
import QRCode from "qrcode";

const props = defineProps({
  /** The value (URL or text) to encode in the QR code. */
  value: { type: String, required: true },
  /** Pixel size of the rendered QR code (width = height). */
  size: { type: Number, default: 200 },
  /** Foreground (module) color. */
  color: { type: String, default: "#1a1a1a" },
  /** Background color. */
  background: { type: String, default: "#ffffff" },
  /** Quiet-zone margin in modules. */
  margin: { type: Number, default: 1 },
});

const dataUrl = ref("");
const error = ref("");

/**
 * Render the QR code to a data URL whenever the value or styling changes.
 * @returns {Promise<void>}
 */
async function render() {
  if (!props.value) {
    dataUrl.value = "";
    return;
  }
  try {
    dataUrl.value = await QRCode.toDataURL(props.value, {
      width: props.size,
      margin: props.margin,
      color: { dark: props.color, light: props.background },
      errorCorrectionLevel: "M",
    });
    error.value = "";
  } catch (e) {
    error.value = e.message;
  }
}

onMounted(render);
watch(() => [props.value, props.size, props.color, props.background], render);
</script>

<template>
  <div class="qr" :style="{ width: size + 'px', height: size + 'px' }">
    <img v-if="dataUrl" :src="dataUrl" :alt="`QR: ${value}`" class="qr__img" />
    <div v-else-if="error" class="qr__error">خطا در ساخت QR</div>
    <div v-else class="qr__placeholder" />
  </div>
</template>

<style scoped>
.qr {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  overflow: hidden;
}
.qr__img { width: 100%; height: 100%; display: block; }
.qr__placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(110deg, #f0ede8 8%, #e5e1db 18%, #f0ede8 33%);
  background-size: 200% 100%;
  animation: qrShimmer 1.2s ease-in-out infinite;
}
@keyframes qrShimmer {
  to { background-position: -200% 0; }
}
.qr__error {
  font-family: "Vazirmatn", sans-serif;
  font-size: 0.75rem;
  color: #b91c1c;
}
</style>
