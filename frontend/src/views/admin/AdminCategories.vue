<script setup>
import { ref, computed, reactive } from "vue";
import {
  Plus, Pencil, Trash2, ChevronDown, ChevronUp, ChevronRight,
  Check, X, Tag, Settings2, Layers
} from "lucide-vue-next";
import { useCategoriesStore } from "@/stores/categories.js";

const store = useCategoriesStore();
const expanded = ref(new Set(store.roots.map((r) => r.id)));

function toggleExpand(id) {
  const s = new Set(expanded.value);
  if (s.has(id)) s.delete(id); else s.add(id);
  expanded.value = s;
}

const ICON_SUGGESTIONS = ["📦","☕","🫖","👔","✏️","📱","🏠","⚽","💄","📚","🍎","🎮","💎","🧴","🧸","🛒","🖥️","👟","🎵","🌿","🌱","🔀","🫗","⚙️","🍕","🎨","🏪","💻","🚗","🏋️"];
const ATTR_TYPES = [
  { value: "text", label: "متن آزاد" },
  { value: "select", label: "انتخاب از لیست" },
  { value: "number", label: "عدد" },
  { value: "tags", label: "برچسب‌ها" },
];

const editing = ref(null);
const editingTarget = ref(null);
const form = reactive({
  name: "", slug: "", icon: "📦", color: "#6b7280", parentId: null,
  attributes: [],
  hasVariants: false, variantLabel: "وزن",
  defaultVariantsText: "۲۵۰ گرم، ۵۰۰ گرم، ۱ کیلوگرم",
  hasGrinds: false,
  defaultGrindsText: "دانه کامل، اسپرسو، موکاپات، فرنچ پرس، V60",
});

function resetForm(defaults = {}) {
  Object.assign(form, {
    name: "", slug: "", icon: "📦", color: "#6b7280", parentId: null,
    attributes: [],
    hasVariants: false, variantLabel: "وزن",
    defaultVariantsText: "۲۵۰ گرم، ۵۰۰ گرم، ۱ کیلوگرم",
    hasGrinds: false,
    defaultGrindsText: "دانه کامل، اسپرسو، موکاپات، فرنچ پرس، V60",
    ...defaults,
  });
}

function startAddRoot() {
  resetForm();
  editing.value = "new-root";
  editingTarget.value = null;
}

function startAddSub(parentId) {
  resetForm({ parentId, icon: store.getById(parentId)?.icon || "📦", color: store.getById(parentId)?.color || "#6b7280" });
  editing.value = "new-sub";
  editingTarget.value = null;
}

function startEdit(cat) {
  resetForm({
    name: cat.name,
    slug: cat.slug || "",
    icon: cat.icon || "📦",
    color: cat.color || "#6b7280",
    parentId: cat.parentId,
    attributes: cat.attributes ? cat.attributes.map((a) => ({ ...a, options: [...(a.options || [])] })) : [],
    hasVariants: cat.hasVariants || false,
    variantLabel: cat.variantLabel || "وزن",
    defaultVariantsText: (cat.defaultVariants || []).map((v) => (typeof v === "object" ? v.label : v)).join("، "),
    hasGrinds: cat.hasGrinds || false,
    defaultGrindsText: (cat.defaultGrinds || []).join("، "),
  });
  editing.value = "edit";
  editingTarget.value = cat.id;
}

function cancel() { editing.value = null; editingTarget.value = null; }

function save() {
  if (!form.name.trim()) return;
  const isRoot = !form.parentId;
  const data = {
    name: form.name,
    slug: form.slug || form.name.replace(/\s+/g, "-").toLowerCase(),
    icon: form.icon,
    color: form.color,
    parentId: form.parentId || null,
    attributes: isRoot ? form.attributes : [],
    hasVariants: isRoot ? form.hasVariants : false,
    variantLabel: isRoot ? form.variantLabel : "",
    defaultVariants: isRoot && form.hasVariants
      ? form.defaultVariantsText.split(/[،,]/).map((s) => s.trim()).filter(Boolean).map((label) => ({ label, multiplier: 1 }))
      : [],
    hasGrinds: isRoot ? form.hasGrinds : false,
    defaultGrinds: isRoot && form.hasGrinds
      ? form.defaultGrindsText.split(/[،,]/).map((s) => s.trim()).filter(Boolean)
      : [],
  };
  if (editing.value === "edit") {
    store.update(editingTarget.value, data);
  } else {
    store.add(data);
  }
  cancel();
}

function addAttr() {
  form.attributes.push({ key: "", label: "", type: "text", options: [] });
}

function removeAttr(i) { form.attributes.splice(i, 1); }

function addOption(attr) {
  if (!attr.options) attr.options = [];
  attr.options.push("");
}
function removeOption(attr, i) { attr.options.splice(i, 1); }

const isEditingRoot = computed(() => editing.value !== null && !form.parentId);
</script>

<template>
  <div class="ap-page" dir="rtl">
    <div class="ap-header">
      <div>
        <h1 class="ap-title">دسته‌بندی‌ها <span style="color:#8B1A1A">.</span></h1>
        <p class="ap-sub">ساختار درختی محصولات — ۲ سطح: دسته اصلی ← زیردسته</p>
      </div>
      <button type="button" class="ap-add-btn" @click="startAddRoot">
        <Plus class="h-4 w-4" /> دسته اصلی جدید
      </button>
    </div>

    <!-- ── Form Panel ── -->
    <div v-if="editing" class="ap-form-card">
      <div class="ap-form-head">
        <div class="flex items-center gap-2">
          <Layers class="h-4 w-4 text-maroon" style="color:#8B1A1A" />
          <h2 class="ap-form-title">
            {{ editing === 'edit' ? 'ویرایش دسته‌بندی' : (form.parentId ? 'زیردسته جدید' : 'دسته اصلی جدید') }}
          </h2>
          <span v-if="form.parentId" class="ap-badge-parent">زیر: {{ store.getById(form.parentId)?.icon }} {{ store.getById(form.parentId)?.name }}</span>
        </div>
        <button type="button" class="ap-form-close" @click="cancel"><X class="h-4 w-4" /></button>
      </div>

      <div class="ap-form-body">
        <!-- Basic fields -->
        <div class="ap-form-grid">
          <div class="ap-field">
            <label class="ap-label">نام دسته‌بندی *</label>
            <input v-model="form.name" class="ap-input" placeholder="مثال: پوشاک" />
          </div>
          <div class="ap-field">
            <label class="ap-label">شناسه (slug)</label>
            <input v-model="form.slug" class="ap-input" dir="ltr" placeholder="clothes" />
          </div>
          <div class="ap-field">
            <label class="ap-label">رنگ</label>
            <div class="ap-color-row">
              <input type="color" v-model="form.color" class="ap-color-pick" />
              <input v-model="form.color" class="ap-input ap-input--sm" dir="ltr" />
            </div>
          </div>
          <div class="ap-field">
            <label class="ap-label">آیکون</label>
            <div class="ap-icon-row">
              <input v-model="form.icon" class="ap-input ap-input--icon" />
              <div class="ap-icon-grid">
                <button v-for="ic in ICON_SUGGESTIONS" :key="ic" type="button"
                  class="ap-icon-btn" :class="form.icon === ic ? 'ap-icon-btn--active' : ''"
                  @click="form.icon = ic">{{ ic }}</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Root-only: Attributes -->
        <template v-if="isEditingRoot">
          <div class="ap-section-sep">
            <div class="ap-section-title">
              <Tag class="h-3.5 w-3.5" style="color:#8B1A1A" />
              ویژگی‌های محصول
              <span class="ap-section-hint">فیلدهایی که محصولات این دسته باید پر کنند</span>
            </div>
            <button type="button" class="ap-link" @click="addAttr">+ افزودن ویژگی</button>
          </div>

          <div class="ap-attrs-list">
            <div v-for="(attr, i) in form.attributes" :key="i" class="ap-attr-row">
              <div class="ap-attr-fields">
                <div class="ap-field">
                  <label class="ap-label">کلید (key)</label>
                  <input v-model="attr.key" class="ap-input" dir="ltr" placeholder="origin" />
                </div>
                <div class="ap-field">
                  <label class="ap-label">برچسب نمایشی</label>
                  <input v-model="attr.label" class="ap-input" placeholder="خاستگاه" />
                </div>
                <div class="ap-field">
                  <label class="ap-label">نوع</label>
                  <select v-model="attr.type" class="ap-input">
                    <option v-for="t in ATTR_TYPES" :key="t.value" :value="t.value">{{ t.label }}</option>
                  </select>
                </div>
                <button type="button" class="ap-attr-del" @click="removeAttr(i)">
                  <Trash2 class="h-3.5 w-3.5" />
                </button>
              </div>
              <!-- Options for select type -->
              <div v-if="attr.type === 'select'" class="ap-options-wrap">
                <span class="ap-label">گزینه‌ها:</span>
                <div class="ap-options-list">
                  <div v-for="(opt, oi) in attr.options" :key="oi" class="ap-option-row">
                    <input :value="opt" @input="attr.options[oi] = $event.target.value" class="ap-input ap-input--sm" placeholder="گزینه..." />
                    <button type="button" class="ap-attr-del" @click="removeOption(attr, oi)"><X class="h-3 w-3" /></button>
                  </div>
                  <button type="button" class="ap-link ap-link--sm" @click="addOption(attr)">+ گزینه</button>
                </div>
              </div>
            </div>
            <div v-if="form.attributes.length === 0" class="ap-attrs-empty">
              هیچ ویژگی‌ای تعریف نشده — کلیک کنید و ویژگی اضافه کنید
            </div>
          </div>

          <!-- Variants (weights) -->
          <div class="ap-section-sep">
            <div class="ap-section-title">
              <Settings2 class="h-3.5 w-3.5" style="color:#8B1A1A" />
              واریانت‌های محصول
            </div>
          </div>
          <div class="ap-form-grid">
            <div class="ap-field ap-field--full ap-toggle-row">
              <label class="ap-toggle-label">
                <input type="checkbox" v-model="form.hasVariants" class="ap-toggle-cb" />
                <span>محصولات این دسته واریانت دارند (مثل وزن)</span>
              </label>
            </div>
            <template v-if="form.hasVariants">
              <div class="ap-field">
                <label class="ap-label">نام واریانت</label>
                <input v-model="form.variantLabel" class="ap-input" placeholder="وزن" />
              </div>
              <div class="ap-field ap-field--full">
                <label class="ap-label">واریانت‌های پیش‌فرض (با ، جدا کنید)</label>
                <input v-model="form.defaultVariantsText" class="ap-input" placeholder="۲۵۰ گرم، ۵۰۰ گرم، ۱ کیلوگرم" />
              </div>
            </template>
          </div>

          <!-- Grinds -->
          <div class="ap-form-grid" style="margin-top:.5rem">
            <div class="ap-field ap-field--full ap-toggle-row">
              <label class="ap-toggle-label">
                <input type="checkbox" v-model="form.hasGrinds" class="ap-toggle-cb" />
                <span>محصولات این دسته نوع آسیاب دارند</span>
              </label>
            </div>
            <div v-if="form.hasGrinds" class="ap-field ap-field--full">
              <label class="ap-label">انواع آسیاب پیش‌فرض (با ، جدا کنید)</label>
              <input v-model="form.defaultGrindsText" class="ap-input" placeholder="دانه کامل، اسپرسو، موکاپات" />
            </div>
          </div>
        </template>

        <div class="ap-form-actions">
          <button type="button" class="ap-btn-ghost" @click="cancel">انصراف</button>
          <button type="button" class="ap-btn-save" @click="save">
            <Check class="h-4 w-4" /> ذخیره
          </button>
        </div>
      </div>
    </div>

    <!-- ── Tree ── -->
    <div class="ap-tree">
      <div v-if="store.roots.length === 0" class="ap-tree-empty">
        هیچ دسته‌بندی‌ای وجود ندارد — دکمه «دسته اصلی جدید» را بزنید
      </div>

      <div v-for="root in store.roots" :key="root.id" class="ap-root-card">
        <!-- Root header -->
        <div class="ap-root-head">
          <button type="button" class="ap-expand-btn" @click="toggleExpand(root.id)">
            <component :is="expanded.has(root.id) ? ChevronDown : ChevronRight" class="h-4 w-4" />
          </button>
          <span class="ap-cat-icon" :style="{ background: root.color + '20', borderColor: root.color }">{{ root.icon }}</span>
          <div class="ap-cat-info">
            <div class="ap-cat-name-txt">{{ root.name }}</div>
            <div class="ap-cat-slug">{{ root.slug }}</div>
          </div>
          <!-- Attribute chips -->
          <div class="ap-attr-chips">
            <span v-for="a in (root.attributes || [])" :key="a.key" class="ap-attr-chip">
              {{ a.label }}
              <span class="ap-attr-type">{{ a.type }}</span>
            </span>
            <span v-if="root.hasVariants" class="ap-attr-chip ap-attr-chip--variant">{{ root.variantLabel }}</span>
            <span v-if="root.hasGrinds" class="ap-attr-chip ap-attr-chip--grind">آسیاب</span>
          </div>
          <div class="ap-root-actions">
            <span class="ap-sub-count">{{ store.children(root.id).length }} زیردسته</span>
            <button type="button" class="ap-action-btn" @click="store.reorder(root.id, 'up')" title="بالاتر"><ChevronUp class="h-3 w-3" /></button>
            <button type="button" class="ap-action-btn" @click="store.reorder(root.id, 'down')" title="پایین‌تر"><ChevronDown class="h-3 w-3" /></button>
            <button type="button" class="ap-action-btn" @click="startEdit(root)" title="ویرایش"><Pencil class="h-3.5 w-3.5" /></button>
            <button type="button" class="ap-action-btn ap-action-btn--del" @click="store.remove(root.id)" title="حذف"><Trash2 class="h-3.5 w-3.5" /></button>
          </div>
        </div>

        <!-- Sub-categories -->
        <div v-if="expanded.has(root.id)" class="ap-subs">
          <div v-for="sub in store.children(root.id)" :key="sub.id" class="ap-sub-row">
            <span class="ap-sub-indent" :style="{ borderColor: root.color + '50' }"></span>
            <span class="ap-cat-icon ap-cat-icon--sm" :style="{ background: sub.color + '20', borderColor: sub.color }">{{ sub.icon }}</span>
            <span class="ap-sub-name">{{ sub.name }}</span>
            <span class="ap-sub-slug">{{ sub.slug }}</span>
            <div class="ap-sub-actions">
              <button type="button" class="ap-action-btn" @click="store.reorder(sub.id, 'up')"><ChevronUp class="h-3 w-3" /></button>
              <button type="button" class="ap-action-btn" @click="store.reorder(sub.id, 'down')"><ChevronDown class="h-3 w-3" /></button>
              <button type="button" class="ap-action-btn" @click="startEdit(sub)"><Pencil class="h-3.5 w-3.5" /></button>
              <button type="button" class="ap-action-btn ap-action-btn--del" @click="store.remove(sub.id)"><Trash2 class="h-3.5 w-3.5" /></button>
            </div>
          </div>
          <button type="button" class="ap-add-sub-btn" @click="startAddSub(root.id)">
            <Plus class="h-3 w-3" /> افزودن زیردسته به «{{ root.name }}»
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ap-page { padding: 2rem; font-family: 'Vazirmatn', sans-serif; max-width: 900px; }
.ap-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem; gap: 1rem; flex-wrap: wrap; }
.ap-title { font-size: 1.5rem; font-weight: 300; color: #1a1a1a; }
.ap-sub { font-size: 0.78rem; color: #9ca3af; margin-top: 0.25rem; }
.ap-add-btn { display: flex; align-items: center; gap: 0.4rem; padding: 0.6rem 1.1rem; background: #1a1a1a; color: #fff; border: none; cursor: pointer; font-family: 'Vazirmatn', sans-serif; font-size: 0.82rem; white-space: nowrap; }
.ap-add-btn:hover { background: #8B1A1A; }

.ap-form-card { border: 1px solid #e5e7eb; background: #fff; margin-bottom: 1.5rem; }
.ap-form-head { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.25rem; border-bottom: 1px solid #f3f4f6; gap: 1rem; }
.ap-form-title { font-size: 0.95rem; font-weight: 500; }
.ap-form-close { background: none; border: none; cursor: pointer; color: #9ca3af; padding: 2px; display: flex; }
.ap-form-close:hover { color: #8B1A1A; }
.ap-badge-parent { font-size: 0.7rem; background: #fff8f8; color: #8B1A1A; border: 1px solid #fca5a5; padding: 0.2rem 0.5rem; }
.ap-form-body { padding: 1.25rem; }
.ap-form-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
.ap-field { display: flex; flex-direction: column; gap: 0.3rem; }
.ap-field--full { grid-column: 1 / -1; }
.ap-label { font-size: 0.72rem; color: #6b7280; text-transform: uppercase; letter-spacing: .04em; }
.ap-input { border: 1px solid #d1d5db; padding: 0.5rem 0.75rem; font-family: 'Vazirmatn', sans-serif; font-size: 0.85rem; outline: none; background: #fff; width: 100%; box-sizing: border-box; }
.ap-input:focus { border-color: #8B1A1A; }
.ap-input--sm { max-width: 140px; }
.ap-input--icon { width: 60px; }
.ap-color-row { display: flex; align-items: center; gap: 0.5rem; }
.ap-color-pick { width: 40px; height: 36px; border: 1px solid #d1d5db; padding: 2px; cursor: pointer; background: none; }
.ap-icon-row { display: flex; flex-direction: column; gap: 0.5rem; }
.ap-icon-grid { display: flex; flex-wrap: wrap; gap: 0.3rem; }
.ap-icon-btn { width: 30px; height: 30px; border: 1px solid #e5e7eb; background: #f9fafb; cursor: pointer; font-size: 0.9rem; display: flex; align-items: center; justify-content: center; }
.ap-icon-btn:hover { border-color: #8B1A1A; }
.ap-icon-btn--active { border-color: #8B1A1A; background: #fff8f8; }
.ap-section-sep { display: flex; align-items: center; justify-content: space-between; margin: 1.25rem 0 0.75rem; padding-top: 1rem; border-top: 1px solid #f3f4f6; }
.ap-section-title { display: flex; align-items: center; gap: 0.4rem; font-size: 0.78rem; font-weight: 500; color: #374151; text-transform: uppercase; letter-spacing: .05em; }
.ap-section-hint { font-size: 0.72rem; color: #9ca3af; font-weight: 400; text-transform: none; letter-spacing: 0; }
.ap-link { font-size: 0.78rem; color: #8B1A1A; background: none; border: none; cursor: pointer; text-decoration: underline; }
.ap-link--sm { font-size: 0.72rem; }
.ap-attrs-list { display: flex; flex-direction: column; gap: 0.75rem; }
.ap-attr-row { border: 1px solid #f3f4f6; padding: 0.75rem; background: #fafafa; }
.ap-attr-fields { display: grid; grid-template-columns: 1fr 1fr 140px 30px; gap: 0.5rem; align-items: end; }
.ap-attr-del { width: 28px; height: 36px; border: 1px solid #fca5a5; background: #fff; color: #dc2626; cursor: pointer; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 1.2rem; }
.ap-attr-del:hover { background: #fee2e2; }
.ap-options-wrap { margin-top: 0.6rem; display: flex; align-items: flex-start; gap: 0.75rem; flex-wrap: wrap; }
.ap-options-list { display: flex; flex-wrap: wrap; gap: 0.35rem; align-items: center; flex: 1; }
.ap-option-row { display: flex; align-items: center; gap: 0.25rem; }
.ap-attrs-empty { font-size: 0.78rem; color: #9ca3af; text-align: center; padding: 1rem; border: 1px dashed #e5e7eb; }
.ap-toggle-row { flex-direction: row; align-items: center; }
.ap-toggle-label { display: flex; align-items: center; gap: 0.5rem; cursor: pointer; font-size: 0.85rem; color: #374151; }
.ap-toggle-cb { width: 16px; height: 16px; accent-color: #8B1A1A; }
.ap-form-actions { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1.5rem; }
.ap-btn-ghost { padding: 0.5rem 1rem; border: 1px solid #d1d5db; background: none; font-family: 'Vazirmatn', sans-serif; font-size: 0.82rem; cursor: pointer; }
.ap-btn-ghost:hover { border-color: #8B1A1A; color: #8B1A1A; }
.ap-btn-save { display: flex; align-items: center; gap: 0.35rem; padding: 0.5rem 1.2rem; background: #8B1A1A; color: #fff; border: none; font-family: 'Vazirmatn', sans-serif; font-size: 0.82rem; cursor: pointer; }
.ap-btn-save:hover { opacity: 0.9; }

.ap-tree { display: flex; flex-direction: column; gap: 1rem; }
.ap-tree-empty { text-align: center; color: #9ca3af; padding: 3rem; border: 2px dashed #e5e7eb; font-size: 0.9rem; }
.ap-root-card { border: 1px solid #e5e7eb; background: #fff; overflow: hidden; }
.ap-root-head { display: flex; align-items: center; gap: 0.6rem; padding: 0.9rem 1rem; background: #fafafa; border-bottom: 1px solid #f3f4f6; flex-wrap: wrap; }
.ap-expand-btn { width: 28px; height: 28px; border: 1px solid #e5e7eb; background: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center; flex-shrink: 0; color: #6b7280; }
.ap-expand-btn:hover { border-color: #8B1A1A; color: #8B1A1A; }
.ap-cat-icon { display: inline-flex; align-items: center; justify-content: center; width: 34px; height: 34px; border: 1px solid; font-size: 1.1rem; flex-shrink: 0; }
.ap-cat-icon--sm { width: 26px; height: 26px; font-size: 0.85rem; }
.ap-cat-info { min-width: 120px; }
.ap-cat-name-txt { font-size: 0.9rem; font-weight: 500; color: #1a1a1a; }
.ap-cat-slug { font-size: 0.7rem; color: #9ca3af; font-family: monospace; }
.ap-attr-chips { display: flex; flex-wrap: wrap; gap: 0.3rem; flex: 1; min-width: 0; }
.ap-attr-chip { font-size: 0.65rem; padding: 0.15rem 0.5rem; border: 1px solid #e5e7eb; background: #f9fafb; color: #374151; display: flex; align-items: center; gap: 0.3rem; }
.ap-attr-chip--variant { border-color: #6b4226; color: #6b4226; background: #6b422610; }
.ap-attr-chip--grind { border-color: #8b6914; color: #8b6914; background: #8b691410; }
.ap-attr-type { font-size: 0.6rem; color: #9ca3af; }
.ap-root-actions { display: flex; gap: 0.3rem; align-items: center; flex-shrink: 0; margin-right: auto; }
.ap-sub-count { font-size: 0.7rem; color: #9ca3af; white-space: nowrap; padding: 0.2rem 0.4rem; background: #f3f4f6; }
.ap-action-btn { width: 28px; height: 28px; border: 1px solid #e5e7eb; background: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center; color: #6b7280; }
.ap-action-btn:hover { border-color: #374151; color: #374151; }
.ap-action-btn--del:hover { border-color: #dc2626; color: #dc2626; }

.ap-subs { padding: 0; }
.ap-sub-row { display: flex; align-items: center; gap: 0.5rem; padding: 0.6rem 1rem; border-bottom: 1px solid #f3f4f6; }
.ap-sub-row:last-of-type { border-bottom: none; }
.ap-sub-indent { width: 2px; height: 32px; background: currentColor; border-right: 2px solid #e5e7eb; margin-right: 0.5rem; flex-shrink: 0; }
.ap-sub-name { font-size: 0.85rem; color: #374151; flex: 1; }
.ap-sub-slug { font-size: 0.7rem; color: #9ca3af; font-family: monospace; min-width: 80px; }
.ap-sub-actions { display: flex; gap: 0.25rem; }
.ap-add-sub-btn { display: flex; align-items: center; gap: 0.35rem; width: 100%; padding: 0.55rem 1.25rem; background: none; border: none; border-top: 1px dashed #e5e7eb; font-family: 'Vazirmatn', sans-serif; font-size: 0.78rem; color: #9ca3af; cursor: pointer; }
.ap-add-sub-btn:hover { color: #8B1A1A; background: #fff8f8; }
</style>
