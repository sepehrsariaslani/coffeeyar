<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";

const props = defineProps({
  modelValue: { type: [String, Number, Object], default: "" },
  options: { type: Array, default: () => [] },
  placeholder: { type: String, default: "انتخاب کنید…" },
  labelKey: { type: String, default: "label" },
  valueKey: { type: String, default: "value" },
  clearable: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  searchable: { type: Boolean, default: true },
});

const emit = defineEmits(["update:modelValue", "select"]);

const rootRef = ref(null);
const panelRef = ref(null);
const searchInputRef = ref(null);
const isOpen = ref(false);
const searchQuery = ref("");
const panelStyle = ref({});

const normalized = computed(() =>
  (props.options || []).map((o) => {
    if (o && typeof o === "object") {
      const lbl = o[props.labelKey] ?? o.label ?? o[props.valueKey] ?? o.value ?? "";
      const val = o[props.valueKey] ?? o.value ?? "";
      return { label: String(lbl), value: val, raw: o };
    }
    return { label: String(o ?? ""), value: o, raw: o };
  })
);

const filtered = computed(() => {
  const q = searchQuery.value.trim().toLowerCase();
  if (!q) return normalized.value;
  return normalized.value.filter((o) => o.label.toLowerCase().includes(q));
});

const selectedLabel = computed(() => {
  const v = props.modelValue;
  if (v === null || v === undefined || v === "") return "";
  const match = normalized.value.find((o) => String(o.value) === String(v));
  return match ? match.label : String(v);
});

const hasValue = computed(() => props.modelValue !== null && props.modelValue !== undefined && props.modelValue !== "");

function isSelected(val) {
  return String(props.modelValue ?? "") === String(val ?? "");
}

function selectOption(opt) {
  emit("update:modelValue", opt.value);
  emit("select", opt.raw ?? opt);
  close();
}

function clearSelection(e) {
  e.stopPropagation();
  emit("update:modelValue", "");
  emit("select", null);
}

async function toggleOpen() {
  if (props.disabled) return;
  isOpen.value = !isOpen.value;
  if (isOpen.value) {
    await nextTick();
    if (props.searchable) searchInputRef.value?.focus();
  } else {
    searchQuery.value = "";
  }
}

function close() {
  isOpen.value = false;
  searchQuery.value = "";
}

function onDocumentClick(e) {
  if (!isOpen.value) return;
  if (!rootRef.value?.contains(e.target) && !panelRef.value?.contains(e.target)) close();
}

function updatePanelPosition() {
  const rect = rootRef.value?.getBoundingClientRect();
  if (!rect) return;
  const vH = window.innerHeight;
  const vW = window.innerWidth;
  const ph = panelRef.value?.offsetHeight || 260;
  const spaceBelow = vH - rect.bottom;
  const openUp = spaceBelow < ph && rect.top > spaceBelow;
  const top = openUp ? rect.top - 6 - ph : rect.bottom + 6;
  const width = Math.max(180, Math.min(rect.width, vW - 16));
  const left = Math.max(8, Math.min(rect.left, vW - width - 8));
  panelStyle.value = { left: `${left}px`, top: `${Math.max(8, top)}px`, width: `${width}px` };
}

watch(isOpen, async (open) => {
  if (open) {
    await nextTick();
    updatePanelPosition();
    window.addEventListener("resize", updatePanelPosition);
    window.addEventListener("scroll", updatePanelPosition, true);
  } else {
    window.removeEventListener("resize", updatePanelPosition);
    window.removeEventListener("scroll", updatePanelPosition, true);
  }
});

onMounted(() => document.addEventListener("mousedown", onDocumentClick));
onBeforeUnmount(() => {
  document.removeEventListener("mousedown", onDocumentClick);
  window.removeEventListener("resize", updatePanelPosition);
  window.removeEventListener("scroll", updatePanelPosition, true);
});
</script>

<template>
  <div ref="rootRef" class="app-select" :class="{ 'app-select--open': isOpen }">
    <button
      type="button"
      class="app-select__trigger"
      :class="{ 'app-select__trigger--disabled': disabled }"
      :disabled="disabled"
      @click="toggleOpen"
    >
      <span :class="['app-select__label', !selectedLabel && 'app-select__label--placeholder']">
        {{ selectedLabel || placeholder }}
      </span>
      <span class="app-select__icons">
        <button
          v-if="clearable && hasValue"
          type="button"
          class="app-select__clear"
          @click="clearSelection"
        >×</button>
        <svg
          class="app-select__chevron"
          :class="{ 'app-select__chevron--up': isOpen }"
          width="12" height="12" viewBox="0 0 12 12" fill="none"
        >
          <path d="M2 4L6 8L10 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
      </span>
    </button>

    <Teleport to="body">
      <div
        v-if="isOpen"
        ref="panelRef"
        class="app-select__panel"
        :style="panelStyle"
      >
        <div v-if="searchable" class="app-select__search-wrap">
          <input
            ref="searchInputRef"
            v-model="searchQuery"
            type="text"
            class="app-select__search"
            placeholder="جستجو…"
            @keydown.esc.prevent="close"
          />
          <button v-if="searchQuery" class="app-select__search-clear" type="button" @click="searchQuery = ''">×</button>
        </div>

        <div class="app-select__list">
          <button
            v-for="opt in filtered"
            :key="String(opt.value)"
            type="button"
            class="app-select__option"
            :class="{ 'app-select__option--selected': isSelected(opt.value) }"
            @click="selectOption(opt)"
          >
            <span>{{ opt.label }}</span>
            <svg v-if="isSelected(opt.value)" class="app-select__check" width="13" height="13" viewBox="0 0 13 13" fill="none">
              <path d="M2 6.5L5.5 10L11 3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
            </svg>
          </button>
          <div v-if="!filtered.length" class="app-select__empty">نتیجه‌ای پیدا نشد</div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.app-select { position: relative; width: 100%; font-family: 'Vazirmatn', sans-serif; }
.app-select--open { z-index: 1200; }

.app-select__trigger {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 0.6rem 0.9rem;
  border: 1px solid var(--border);
  background: var(--background);
  color: var(--foreground);
  cursor: pointer;
  transition: border-color 0.15s;
  text-align: right;
}
.app-select__trigger:not(.app-select__trigger--disabled):hover { border-color: var(--foreground); }
.app-select__trigger--disabled { opacity: 0.5; cursor: not-allowed; }

.app-select__label { flex: 1; font-size: 0.875rem; text-align: right; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.app-select__label--placeholder { color: var(--muted-foreground); }

.app-select__icons { display: flex; align-items: center; gap: 4px; flex-shrink: 0; }

.app-select__clear {
  width: 18px; height: 18px; display: flex; align-items: center; justify-content: center;
  font-size: 14px; color: var(--muted-foreground); background: none; border: none; cursor: pointer;
}
.app-select__clear:hover { color: var(--foreground); }

.app-select__chevron { color: var(--muted-foreground); transition: transform 0.2s; flex-shrink: 0; }
.app-select__chevron--up { transform: rotate(180deg); }

.app-select__panel {
  position: fixed;
  z-index: 2000;
  border: 1px solid var(--border);
  background: var(--background);
  box-shadow: 0 4px 24px rgba(0,0,0,0.1);
  overflow: hidden;
  font-family: 'Vazirmatn', sans-serif;
}

.app-select__search-wrap { padding: 8px; border-bottom: 1px solid var(--border); position: relative; }
.app-select__search {
  width: 100%; padding: 0.4rem 0.7rem; font-size: 0.82rem; font-family: 'Vazirmatn', sans-serif;
  border: 1px solid var(--border); background: var(--background); color: var(--foreground);
  outline: none;
}
.app-select__search:focus { border-color: var(--foreground); }
.app-select__search-clear {
  position: absolute; left: 14px; top: 50%; transform: translateY(-50%);
  background: none; border: none; cursor: pointer; color: var(--muted-foreground); font-size: 15px;
}

.app-select__list { max-height: 220px; overflow-y: auto; padding: 4px 0; }

.app-select__option {
  width: 100%; display: flex; align-items: center; justify-content: space-between;
  gap: 8px; padding: 0.5rem 0.9rem; font-size: 0.875rem; text-align: right;
  color: var(--foreground); background: none; border: none; cursor: pointer;
  font-family: 'Vazirmatn', sans-serif; transition: background 0.12s;
}
.app-select__option:hover { background: var(--accent); }
.app-select__option--selected { color: var(--maroon); background: var(--accent); }

.app-select__check { color: var(--maroon); flex-shrink: 0; }

.app-select__empty { padding: 0.6rem 0.9rem; font-size: 0.82rem; color: var(--muted-foreground); text-align: center; }
</style>
