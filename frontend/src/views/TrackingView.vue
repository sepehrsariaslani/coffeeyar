<script setup>
import { ref, computed } from "vue";
import { Search, Package, Truck, CheckCircle2, Clock, MapPin, Phone } from "lucide-vue-next";
import TheLayout from "@/components/site/TheLayout.vue";
import { useAccountStore } from "@/stores/account.js";
import { toFa } from "@/lib/utils.js";
function formatPrice(n) { return n ? Number(n).toLocaleString("fa-IR") : "۰"; }

const accountStore = useAccountStore();
const query = ref("");
const result = ref(null);
const searched = ref(false);

function search() {
  searched.value = true;
  result.value = null;
  const q = query.value.trim();
  if (!q) return;
  const order = accountStore.orders.find(
    (o) => o.id === q || o.trackingCode === q || o.id.replace("ORD-", "") === q
  );
  result.value = order || null;
}

const steps = [
  { key: "در حال پردازش", label: "ثبت سفارش", icon: Package },
  { key: "تایید شده", label: "تایید سفارش", icon: CheckCircle2 },
  { key: "در حال ارسال", label: "ارسال شد", icon: Truck },
  { key: "تحویل داده شده", label: "تحویل داده شده", icon: MapPin },
];

const stepOrder = ["در حال پردازش", "تایید شده", "در حال ارسال", "تحویل داده شده"];

const currentStepIdx = computed(() => {
  if (!result.value) return -1;
  return stepOrder.indexOf(result.value.status);
});

const STATUS_COLOR = {
  "در حال پردازش": { bg: "#fefce8", text: "#854d0e", dot: "#ca8a04" },
  "تایید شده": { bg: "#eff6ff", text: "#1e40af", dot: "#3b82f6" },
  "در حال ارسال": { bg: "#f5f3ff", text: "#5b21b6", dot: "#7c3aed" },
  "تحویل داده شده": { bg: "#f0fdf4", text: "#14532d", dot: "#16a34a" },
  "لغو شده": { bg: "#fef2f2", text: "#7f1d1d", dot: "#ef4444" },
};
</script>

<template>
  <TheLayout>
    <div class="trk-page">
      <div class="trk-hero">
        <div class="trk-hero__inner">
          <p class="trk-hero__tag">پیگیری مرسوله</p>
          <h1 class="trk-hero__title">وضعیت سفارش</h1>
          <p class="trk-hero__sub">شماره سفارش یا کد رهگیری را وارد کنید</p>

          <div class="trk-search">
            <input
              v-model="query"
              @keyup.enter="search"
              placeholder="مثال: ORD-۱۰۰۱ یا RH۱۲۳۴۵۶۷"
              class="trk-input"
              dir="ltr"
            />
            <button type="button" @click="search" class="trk-btn">
              <Search class="h-4 w-4" />
              جستجو
            </button>
          </div>
        </div>
      </div>

      <div class="trk-body">

        <!-- not searched yet -->
        <div v-if="!searched" class="trk-hint">
          <Package class="trk-hint__icon" />
          <p>شماره سفارش یا کد رهگیری را در بالا وارد کنید.</p>
        </div>

        <!-- not found -->
        <div v-else-if="searched && !result" class="trk-hint trk-hint--warn">
          <Search class="trk-hint__icon" />
          <p>سفارشی با این مشخصات پیدا نشد.</p>
          <p class="trk-hint__small">شماره سفارش به شکل ORD-XXXX است.</p>
        </div>

        <!-- result -->
        <div v-else-if="result" class="trk-card">
          <div class="trk-card__head">
            <div>
              <div class="trk-card__id">{{ result.id }}</div>
              <div class="trk-card__date">تاریخ: {{ result.date }}</div>
            </div>
            <span
              class="trk-status"
              :style="{ background: STATUS_COLOR[result.status]?.bg, color: STATUS_COLOR[result.status]?.text }"
            >
              <span class="trk-status__dot" :style="{ background: STATUS_COLOR[result.status]?.dot }" />
              {{ result.status }}
            </span>
          </div>

          <!-- Tracking code -->
          <div v-if="result.trackingCode" class="trk-code">
            <Truck class="h-4 w-4 shrink-0" />
            <span>کد رهگیری پست:</span>
            <span class="trk-code__val" dir="ltr">{{ result.trackingCode }}</span>
          </div>

          <!-- Steps -->
          <div v-if="result.status !== 'لغو شده'" class="trk-steps">
            <div
              v-for="(step, i) in steps"
              :key="step.key"
              class="trk-step"
              :class="{
                'trk-step--done': i <= currentStepIdx,
                'trk-step--active': i === currentStepIdx,
              }"
            >
              <div class="trk-step__icon">
                <component :is="step.icon" class="h-4 w-4" />
              </div>
              <div class="trk-step__line" v-if="i < steps.length - 1" />
              <div class="trk-step__label">{{ step.label }}</div>
            </div>
          </div>

          <!-- Cancelled notice -->
          <div v-else class="trk-cancelled">
            این سفارش لغو شده است.
          </div>

          <!-- Items -->
          <div class="trk-items">
            <div class="trk-items__title">اقلام سفارش</div>
            <div v-for="item in result.items" :key="item.productId" class="trk-item">
              <div class="trk-item__info">
                <div class="trk-item__name">{{ item.name }}</div>
                <div class="trk-item__meta">
                  <span v-if="item.weight">{{ item.weight }}</span>
                  <span v-if="item.grind"> · {{ item.grind }}</span>
                  <span> × {{ toFa(item.qty) }}</span>
                </div>
              </div>
              <div class="trk-item__price">{{ formatPrice(item.unitPrice * item.qty) }} تومان</div>
            </div>
          </div>

          <!-- Address -->
          <div class="trk-addr">
            <MapPin class="h-4 w-4 shrink-0 text-maroon" />
            <span>{{ result.address }}</span>
          </div>
        </div>
      </div>
    </div>
  </TheLayout>
</template>

<style scoped>
.trk-page { font-family: 'Vazirmatn', sans-serif; }
.trk-hero { background: linear-gradient(135deg, #1a1a1a 0%, #2d2a28 100%); color: #fff; padding: 4rem 5vw; }
.trk-hero__inner { max-width: 600px; margin: 0 auto; text-align: center; }
.trk-hero__tag { font-size: 0.7rem; letter-spacing: 0.25em; color: #9e9890; text-transform: uppercase; margin-bottom: 0.5rem; }
.trk-hero__title { font-size: 2.2rem; font-weight: 300; margin: 0 0 0.5rem; }
.trk-hero__sub { font-size: 0.85rem; color: #9e9890; margin-bottom: 1.5rem; }
.trk-search { display: flex; gap: 0; max-width: 480px; margin: 0 auto; }
.trk-input {
  flex: 1; padding: 0.75rem 1rem; background: #fff; border: none; outline: none;
  font-family: 'Vazirmatn', sans-serif; font-size: 0.9rem; color: #1a1a1a; text-align: center;
}
.trk-btn {
  padding: 0.75rem 1.5rem; background: #800000; color: #fff; border: none; cursor: pointer;
  display: flex; align-items: center; gap: 0.4rem; font-family: 'Vazirmatn', sans-serif;
  font-size: 0.85rem; white-space: nowrap;
}
.trk-btn:hover { opacity: 0.9; }
.trk-body { max-width: 680px; margin: 0 auto; padding: 3rem 5vw 5rem; }
.trk-hint { text-align: center; padding: 3rem 1rem; color: #9e9890; }
.trk-hint--warn { color: #b91c1c; }
.trk-hint__icon { width: 48px; height: 48px; margin: 0 auto 1rem; opacity: 0.4; }
.trk-hint__small { font-size: 0.78rem; margin-top: 0.5rem; color: #9ca3af; }

.trk-card { border: 1px solid #e5e7eb; background: #fff; }
.trk-card__head { display: flex; align-items: flex-start; justify-content: space-between; padding: 1.25rem 1.5rem; border-bottom: 1px solid #f3f4f6; gap: 1rem; }
.trk-card__id { font-size: 1rem; font-weight: 500; color: #1a1a1a; direction: ltr; text-align: right; }
.trk-card__date { font-size: 0.78rem; color: #9ca3af; margin-top: 0.2rem; }
.trk-status { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.35rem 0.75rem; font-size: 0.78rem; border-radius: 2px; white-space: nowrap; }
.trk-status__dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }

.trk-code { display: flex; align-items: center; gap: 0.5rem; padding: 0.85rem 1.5rem; background: #f9fafb; border-bottom: 1px solid #f3f4f6; font-size: 0.85rem; color: #374151; }
.trk-code__val { font-family: monospace; font-size: 0.95rem; color: #800000; font-weight: 600; letter-spacing: 0.05em; }

.trk-steps { display: flex; align-items: flex-start; padding: 2rem 1.5rem; gap: 0; }
.trk-step { flex: 1; display: flex; flex-direction: column; align-items: center; position: relative; }
.trk-step__icon {
  width: 38px; height: 38px; border-radius: 50%; border: 2px solid #d1d5db;
  display: flex; align-items: center; justify-content: center; color: #d1d5db;
  background: #fff; z-index: 1; position: relative;
}
.trk-step--done .trk-step__icon { border-color: #800000; color: #800000; background: #fff8f8; }
.trk-step--active .trk-step__icon { border-color: #800000; background: #800000; color: #fff; box-shadow: 0 0 0 4px rgba(128,0,0,0.1); }
.trk-step__line {
  position: absolute; top: 19px; right: 50%; width: 100%;
  height: 2px; background: #d1d5db;
}
.trk-step--done .trk-step__line { background: #800000; }
.trk-step__label { font-size: 0.68rem; color: #6b7280; margin-top: 0.5rem; text-align: center; }
.trk-step--done .trk-step__label, .trk-step--active .trk-step__label { color: #800000; }

.trk-cancelled { padding: 1rem 1.5rem; text-align: center; background: #fef2f2; color: #b91c1c; font-size: 0.85rem; }

.trk-items { border-top: 1px solid #f3f4f6; padding: 1.25rem 1.5rem; }
.trk-items__title { font-size: 0.75rem; color: #9ca3af; letter-spacing: 0.1em; margin-bottom: 0.75rem; }
.trk-item { display: flex; justify-content: space-between; align-items: flex-start; padding: 0.6rem 0; border-bottom: 1px solid #f9fafb; gap: 1rem; }
.trk-item:last-child { border-bottom: none; }
.trk-item__name { font-size: 0.9rem; color: #1a1a1a; }
.trk-item__meta { font-size: 0.75rem; color: #9ca3af; margin-top: 0.2rem; }
.trk-item__price { font-size: 0.85rem; color: #800000; white-space: nowrap; flex-shrink: 0; }

.trk-addr { display: flex; align-items: center; gap: 0.5rem; padding: 1rem 1.5rem; border-top: 1px solid #f3f4f6; font-size: 0.82rem; color: #374151; }
</style>
