<script setup>
import { ref, computed } from "vue";
import { RotateCcw, Check, X, ChevronDown, ChevronUp, AlertCircle } from "lucide-vue-next";
import { useReturnsStore } from "@/stores/returns.js";
import { formatPrice } from "@/lib/data.js";
import { toFa } from "@/lib/utils.js";

const store = useReturnsStore();
const statusFilter = ref("all");
const expanded = ref(null);
const adminNote = ref("");
const processingId = ref(null);

const filtered = computed(() => {
  if (statusFilter.value === "all") return store.requests;
  return store.requests.filter((r) => r.status === statusFilter.value);
});

function toggle(id) {
  expanded.value = expanded.value === id ? null : id;
  adminNote.value = "";
  processingId.value = null;
}

function startProcess(id) {
  processingId.value = id;
  adminNote.value = store.requests.find((r) => r.id === id)?.adminNote || "";
}

function approve(id) {
  store.updateStatus(id, "تایید شده", adminNote.value);
  processingId.value = null;
}

function reject(id) {
  store.updateStatus(id, "رد شده", adminNote.value);
  processingId.value = null;
}

const STATUS_STYLE = {
  "در انتظار بررسی": { bg: "#fefce8", text: "#854d0e", dot: "#ca8a04" },
  "تایید شده":       { bg: "#f0fdf4", text: "#14532d", dot: "#16a34a" },
  "رد شده":          { bg: "#fef2f2", text: "#7f1d1d", dot: "#ef4444" },
};

const REASON_LABELS = {
  defective: "کالای معیوب",
  wrong_item: "کالای اشتباه",
  not_as_described: "مطابق توضیحات نیست",
  changed_mind: "انصراف از خرید",
  other: "سایر",
};
</script>

<template>
  <div class="ar-page" dir="rtl">
    <div class="ar-header">
      <div>
        <h1 class="ar-title">مرجوعی‌ها</h1>
        <p class="ar-sub">مدیریت درخواست‌های بازگشت کالا</p>
      </div>
      <div class="ar-stats">
        <div class="ar-stat">
          <div class="ar-stat__val">{{ toFa(store.pending.length) }}</div>
          <div class="ar-stat__lbl">در انتظار</div>
        </div>
        <div class="ar-stat">
          <div class="ar-stat__val">{{ toFa(store.approved.length) }}</div>
          <div class="ar-stat__lbl">تایید شده</div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="ar-filters">
      <button
        v-for="s in ['all', 'در انتظار بررسی', 'تایید شده', 'رد شده']"
        :key="s"
        type="button"
        class="ar-filter-btn"
        :class="statusFilter === s ? 'ar-filter-btn--active' : ''"
        @click="statusFilter = s"
      >
        {{ s === 'all' ? 'همه' : s }}
      </button>
    </div>

    <!-- Empty -->
    <div v-if="filtered.length === 0" class="ar-empty">
      <RotateCcw class="ar-empty__icon" />
      <p>درخواست مرجوعی‌ای یافت نشد.</p>
    </div>

    <!-- List -->
    <div v-else class="ar-list">
      <div v-for="req in filtered" :key="req.id" class="ar-item">
        <div class="ar-item__head" @click="toggle(req.id)">
          <div class="ar-item__id-block">
            <span class="ar-item__id">{{ req.id }}</span>
            <span class="ar-item__order">سفارش: {{ req.orderRef }}</span>
          </div>
          <span
            class="ar-status"
            :style="{ background: STATUS_STYLE[req.status]?.bg, color: STATUS_STYLE[req.status]?.text }"
          >
            <span class="ar-status__dot" :style="{ background: STATUS_STYLE[req.status]?.dot }" />
            {{ req.status }}
          </span>
          <div class="ar-item__right">
            <span class="ar-item__amount">{{ formatPrice(req.totalAmount) }} تومان</span>
            <component :is="expanded === req.id ? ChevronUp : ChevronDown" class="h-4 w-4 text-gray-400" />
          </div>
        </div>

        <!-- Expanded -->
        <div v-if="expanded === req.id" class="ar-item__body">
          <div class="ar-info-grid">
            <div class="ar-info">
              <span class="ar-info__lbl">دلیل مرجوعی</span>
              <span class="ar-info__val">{{ REASON_LABELS[req.reason] || req.reason }}</span>
            </div>
            <div class="ar-info">
              <span class="ar-info__lbl">تاریخ درخواست</span>
              <span class="ar-info__val">{{ req.date }}</span>
            </div>
            <div v-if="req.description" class="ar-info ar-info--full">
              <span class="ar-info__lbl">توضیحات</span>
              <span class="ar-info__val">{{ req.description }}</span>
            </div>
            <div v-if="req.adminNote" class="ar-info ar-info--full">
              <span class="ar-info__lbl">یادداشت ادمین</span>
              <span class="ar-info__val">{{ req.adminNote }}</span>
            </div>
          </div>

          <!-- Items -->
          <div v-if="req.items?.length" class="ar-items">
            <div class="ar-items__title">اقلام</div>
            <div v-for="item in req.items" :key="item.id" class="ar-item-row">
              <span>{{ item.name }}</span>
              <span class="ar-item-row__price">{{ formatPrice(item.unitPrice * item.qty) }} تومان</span>
            </div>
          </div>

          <!-- Process buttons -->
          <div v-if="req.status === 'در انتظار بررسی'" class="ar-process">
            <div v-if="processingId === req.id" class="ar-process__form">
              <textarea
                v-model="adminNote"
                placeholder="یادداشت (اختیاری)"
                rows="2"
                class="ar-note"
              />
              <div class="ar-process__btns">
                <button type="button" class="ar-btn ar-btn--reject" @click="reject(req.id)">
                  <X class="h-4 w-4" /> رد درخواست
                </button>
                <button type="button" class="ar-btn ar-btn--approve" @click="approve(req.id)">
                  <Check class="h-4 w-4" /> تایید و بازپرداخت
                </button>
              </div>
            </div>
            <button v-else type="button" class="ar-btn ar-btn--process" @click="startProcess(req.id)">
              <AlertCircle class="h-4 w-4" /> بررسی درخواست
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ar-page { padding: 2rem; font-family: 'Vazirmatn', sans-serif; }
.ar-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem; }
.ar-title { font-size: 1.3rem; font-weight: 500; color: #1a1a1a; }
.ar-sub { font-size: 0.8rem; color: #9ca3af; margin-top: 0.2rem; }
.ar-stats { display: flex; gap: 1.5rem; }
.ar-stat { text-align: center; }
.ar-stat__val { font-size: 1.5rem; font-weight: 300; color: #800000; }
.ar-stat__lbl { font-size: 0.7rem; color: #9ca3af; }
.ar-filters { display: flex; gap: 0.5rem; margin-bottom: 1.25rem; flex-wrap: wrap; }
.ar-filter-btn { padding: 0.4rem 0.85rem; border: 1px solid #e5e7eb; background: none; font-family: 'Vazirmatn', sans-serif; font-size: 0.8rem; cursor: pointer; color: #6b7280; }
.ar-filter-btn:hover { border-color: #800000; color: #800000; }
.ar-filter-btn--active { border-color: #800000; background: #800000; color: #fff; }
.ar-empty { text-align: center; padding: 4rem 1rem; color: #9ca3af; }
.ar-empty__icon { width: 40px; height: 40px; margin: 0 auto 1rem; opacity: 0.4; }
.ar-list { border: 1px solid #e5e7eb; }
.ar-item { border-bottom: 1px solid #e5e7eb; background: #fff; }
.ar-item:last-child { border-bottom: none; }
.ar-item__head { display: flex; align-items: center; gap: 1rem; padding: 1rem 1.25rem; cursor: pointer; transition: background 0.15s; }
.ar-item__head:hover { background: #fafafa; }
.ar-item__id-block { flex: 1; min-width: 0; }
.ar-item__id { display: block; font-size: 0.85rem; font-weight: 500; color: #1a1a1a; direction: ltr; text-align: right; }
.ar-item__order { font-size: 0.75rem; color: #9ca3af; }
.ar-status { display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.3rem 0.65rem; font-size: 0.75rem; white-space: nowrap; }
.ar-status__dot { width: 6px; height: 6px; border-radius: 50%; }
.ar-item__right { display: flex; align-items: center; gap: 0.75rem; }
.ar-item__amount { font-size: 0.85rem; font-weight: 500; color: #800000; white-space: nowrap; }
.ar-item__body { padding: 1.25rem; border-top: 1px solid #f3f4f6; background: #fafafa; }
.ar-info-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem; margin-bottom: 1rem; }
.ar-info { display: flex; flex-direction: column; gap: 0.2rem; }
.ar-info--full { grid-column: 1 / -1; }
.ar-info__lbl { font-size: 0.7rem; color: #9ca3af; letter-spacing: 0.05em; }
.ar-info__val { font-size: 0.85rem; color: #374151; }
.ar-items { margin-bottom: 1rem; }
.ar-items__title { font-size: 0.72rem; color: #9ca3af; margin-bottom: 0.5rem; }
.ar-item-row { display: flex; justify-content: space-between; font-size: 0.82rem; padding: 0.3rem 0; border-bottom: 1px solid #f3f4f6; }
.ar-item-row:last-child { border-bottom: none; }
.ar-item-row__price { color: #800000; }
.ar-process { margin-top: 1rem; }
.ar-process__form { display: flex; flex-direction: column; gap: 0.75rem; }
.ar-note { border: 1px solid #d1d5db; padding: 0.5rem 0.75rem; font-family: 'Vazirmatn', sans-serif; font-size: 0.82rem; resize: vertical; outline: none; width: 100%; box-sizing: border-box; }
.ar-note:focus { border-color: #800000; }
.ar-process__btns { display: flex; gap: 0.75rem; justify-content: flex-end; flex-wrap: wrap; }
.ar-btn { display: flex; align-items: center; gap: 0.35rem; padding: 0.5rem 1rem; border: none; font-family: 'Vazirmatn', sans-serif; font-size: 0.82rem; cursor: pointer; }
.ar-btn--process { background: #f3f4f6; color: #374151; border: 1px solid #e5e7eb; }
.ar-btn--process:hover { border-color: #800000; color: #800000; }
.ar-btn--reject { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
.ar-btn--reject:hover { background: #b91c1c; color: #fff; }
.ar-btn--approve { background: #800000; color: #fff; }
.ar-btn--approve:hover { opacity: 0.9; }
</style>
