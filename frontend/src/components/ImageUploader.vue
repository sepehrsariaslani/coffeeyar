<script setup>
import { ref } from "vue";
import { Upload, X, Loader2 } from "lucide-vue-next";
import { api } from "@/lib/api.js";

const props = defineProps({
  /** Current image URL (v-model). */
  modelValue: { type: String, default: "" },
  /** Field label shown above the uploader. */
  label: { type: String, default: "تصویر" },
  /** Helper hint text. */
  hint: { type: String, default: "PNG، JPG یا WebP — حداکثر ۵ مگابایت" },
});
const emit = defineEmits(["update:modelValue"]);

const dragging = ref(false);
const error = ref("");
const uploading = ref(false);

/**
 * Validate and upload the chosen file to the server, then emit the
 * returned public URL. Falls back to a base64 data URL if the upload
 * endpoint is unreachable, so the admin is never blocked.
 * @param {File} file The selected image file.
 * @returns {Promise<void>}
 */
async function processFile(file) {
  error.value = "";
  if (!file) return;
  if (!file.type.startsWith("image/")) { error.value = "فایل باید تصویر باشد"; return; }
  if (file.size > 5 * 1024 * 1024) { error.value = "حجم فایل بیشتر از ۵ مگابایت است"; return; }

  uploading.value = true;
  try {
    const res = await api.uploadImage(file);
    emit("update:modelValue", res.url);
  } catch (e) {
    // Fallback: inline as data URL so the admin can still save
    console.error("آپلود ناموفق بود، استفاده از حالت محلی:", e.message);
    const reader = new FileReader();
    reader.onload = (ev) => emit("update:modelValue", ev.target.result);
    reader.readAsDataURL(file);
    error.value = "آپلود سرور ناموفق بود — تصویر به‌صورت محلی ذخیره شد";
  } finally {
    uploading.value = false;
  }
}

function onInput(e) { processFile(e.target.files[0]); }
function onDrop(e) { dragging.value = false; processFile(e.dataTransfer.files[0]); }
function clear() { emit("update:modelValue", ""); }
</script>

<template>
  <div class="img-uploader">
    <label v-if="label" class="img-uploader__label">{{ label }}</label>

    <div v-if="modelValue" class="img-uploader__preview">
      <img :src="modelValue" alt="preview" class="img-uploader__img" />
      <button type="button" class="img-uploader__clear" @click="clear" title="حذف تصویر">
        <X class="h-4 w-4" />
      </button>
    </div>

    <label
      v-else
      class="img-uploader__drop"
      :class="dragging ? 'img-uploader__drop--active' : ''"
      @dragover.prevent="dragging = true"
      @dragleave="dragging = false"
      @drop.prevent="onDrop"
    >
      <input type="file" accept="image/*" class="sr-only" :disabled="uploading" @change="onInput" />
      <Loader2 v-if="uploading" class="h-8 w-8 text-maroon mb-2 img-uploader__spin" />
      <Upload v-else class="h-8 w-8 text-muted-foreground mb-2" />
      <span class="img-uploader__cta">{{ uploading ? "در حال آپلود..." : "انتخاب یا رها کردن تصویر" }}</span>
      <span class="img-uploader__hint">{{ hint }}</span>
    </label>

    <p v-if="error" class="img-uploader__error">{{ error }}</p>
  </div>
</template>

<style scoped>
.img-uploader { display: flex; flex-direction: column; gap: 0.35rem; }
.img-uploader__label { font-size: 0.75rem; color: #6b7280; font-family: 'Vazirmatn', sans-serif; }
.img-uploader__preview { position: relative; display: inline-block; }
.img-uploader__img { width: 100%; max-height: 200px; object-fit: cover; border: 1px solid #e5e7eb; border-radius: 6px; }
.img-uploader__clear {
  position: absolute; top: 6px; left: 6px;
  background: #1a1a1a; color: #fff; border: none; border-radius: 4px;
  padding: 4px; cursor: pointer; display: flex; align-items: center; justify-content: center;
}
.img-uploader__clear:hover { background: #800000; }
.img-uploader__drop {
  border: 2px dashed #d1d5db; padding: 2rem 1.5rem; border-radius: 8px;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 0.25rem; cursor: pointer; transition: border-color 0.2s, background 0.2s;
  text-align: center;
}
.img-uploader__drop:hover, .img-uploader__drop--active {
  border-color: #800000; background: rgba(128,0,0,0.03);
}
.img-uploader__cta { font-family: 'Vazirmatn', sans-serif; font-size: 0.85rem; color: #374151; }
.img-uploader__hint { font-family: 'Vazirmatn', sans-serif; font-size: 0.72rem; color: #9ca3af; }
.img-uploader__error { font-family: 'Vazirmatn', sans-serif; font-size: 0.75rem; color: #dc2626; }
.img-uploader__spin { animation: iuSpin 0.8s linear infinite; }
@keyframes iuSpin { to { transform: rotate(360deg); } }
</style>
