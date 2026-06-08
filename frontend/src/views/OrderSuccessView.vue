<script setup>
import { computed, onMounted, ref } from "vue";
import { useRoute, RouterLink } from "vue-router";
import { CheckCircle2, Package, MapPin, Clock, ShoppingBag, ChevronLeft } from "lucide-vue-next";
import TheLayout from "@/components/site/TheLayout.vue";
import { useSeo } from "@/composables/useSeo.js";

useSeo({ title: "سفارش ثبت شد", description: "سفارش شما با موفقیت ثبت و پردازش شد." });

const route = useRoute();
const ref_ = computed(() => route.query.ref || "");
const amount = computed(() => Number(route.query.amount) || 0);

const order = ref(null);

onMounted(() => {
  try {
    const raw = localStorage.getItem("navar-last-order");
    if (raw) order.value = JSON.parse(raw);
  } catch {}
});

const formatPrice = (n) =>
  new Intl.NumberFormat("fa-IR").format(n) + " تومان";

const estimatedDays = computed(() => {
  const d = new Date();
  d.setDate(d.getDate() + 5);
  return d.toLocaleDateString("fa-IR", { month: "long", day: "numeric" });
});

function stepStatus(idx) {
  if (idx === 0) return "done";
  if (idx === 1) return "active";
  return "pending";
}
const steps = [
  { label: "سفارش ثبت شد", icon: CheckCircle2 },
  { label: "در حال آماده‌سازی", icon: Package },
  { label: "ارسال شد", icon: MapPin },
  { label: "تحویل داده شد", icon: ShoppingBag },
];
</script>

<template>
  <TheLayout>
    <div class="min-h-[80vh] bg-background font-[Vazirmatn]" dir="rtl">

      <!-- Hero band -->
      <div class="border-b border-border bg-background">
        <div class="mx-auto max-w-3xl px-6 py-16 text-center">
          <div class="inline-flex h-20 w-20 items-center justify-center rounded-full bg-green-50 mb-6">
            <CheckCircle2 class="h-10 w-10 text-green-500" />
          </div>
          <h1 class="text-3xl font-light text-foreground">سفارش شما ثبت شد!</h1>
          <p class="mt-3 text-muted-foreground">
            با تشکر از خرید شما. کد پیگیری سفارشتان:
            <span class="mx-2 font-mono font-semibold text-maroon tracking-widest">{{ ref_ || (order?.ref) }}</span>
          </p>
        </div>
      </div>

      <div class="mx-auto max-w-3xl px-6 py-12 space-y-8">

        <!-- Order timeline -->
        <div class="rounded-none border border-border bg-card p-6">
          <h2 class="text-xs uppercase tracking-[0.3em] text-maroon mb-8">وضعیت سفارش</h2>
          <div class="relative">
            <div class="absolute top-4 right-4 left-4 h-px bg-border" />
            <div class="relative flex justify-between">
              <div
                v-for="(step, idx) in steps"
                :key="idx"
                class="flex flex-col items-center gap-2 text-center"
                style="width: 25%"
              >
                <div
                  :class="[
                    'relative z-10 flex h-8 w-8 items-center justify-center rounded-full border-2 text-xs font-medium transition-all',
                    stepStatus(idx) === 'done' ? 'border-green-500 bg-green-500 text-white' :
                    stepStatus(idx) === 'active' ? 'border-maroon bg-background text-maroon animate-pulse' :
                    'border-border bg-background text-muted-foreground'
                  ]"
                >
                  <component :is="step.icon" class="h-4 w-4" />
                </div>
                <span :class="[
                  'text-[10px] leading-tight',
                  stepStatus(idx) === 'done' ? 'text-green-600 font-medium' :
                  stepStatus(idx) === 'active' ? 'text-foreground font-medium' :
                  'text-muted-foreground'
                ]">{{ step.label }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Two-col info -->
        <div class="grid gap-4 md:grid-cols-2">

          <!-- Order summary -->
          <div class="border border-border bg-card p-6 space-y-4">
            <h2 class="text-xs uppercase tracking-[0.3em] text-maroon">جزئیات سفارش</h2>

            <div v-if="order" class="space-y-3">
              <div v-for="item in order.items" :key="item.name" class="flex items-center gap-3">
                <div class="h-10 w-10 shrink-0 overflow-hidden bg-[#F0EDE8]">
                  <img v-if="item.image" :src="item.image" :alt="item.name" class="h-full w-full object-cover" />
                </div>
                <div class="min-w-0 flex-1">
                  <div class="truncate text-sm text-foreground">{{ item.name }}</div>
                  <div class="text-xs text-muted-foreground">× {{ item.qty.toLocaleString('fa-IR') }}</div>
                </div>
                <div class="text-sm font-medium text-foreground shrink-0">{{ formatPrice(item.price * item.qty) }}</div>
              </div>

              <div class="border-t border-border pt-3 space-y-1.5 text-sm">
                <div class="flex justify-between text-muted-foreground">
                  <span>جمع کالاها</span>
                  <span>{{ formatPrice(order.subtotal) }}</span>
                </div>
                <div v-if="order.discount > 0" class="flex justify-between text-green-600">
                  <span>تخفیف کد {{ order.coupon }}</span>
                  <span>- {{ formatPrice(order.discount) }}</span>
                </div>
                <div class="flex justify-between text-muted-foreground">
                  <span>هزینه ارسال</span>
                  <span>{{ order.shipping === 0 ? 'رایگان' : formatPrice(order.shipping) }}</span>
                </div>
                <div class="flex justify-between border-t border-border pt-2 font-semibold text-foreground">
                  <span>مبلغ پرداختی</span>
                  <span class="text-maroon">{{ formatPrice(order.total) }}</span>
                </div>
              </div>
            </div>

            <div v-else class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-muted-foreground">شماره سفارش</span>
                <span class="font-mono font-medium text-foreground">{{ ref_ }}</span>
              </div>
              <div v-if="amount > 0" class="flex justify-between border-t border-border pt-2">
                <span class="text-muted-foreground">مبلغ پرداختی</span>
                <span class="font-semibold text-maroon">{{ formatPrice(amount) }}</span>
              </div>
            </div>
          </div>

          <!-- Delivery info -->
          <div class="space-y-4">

            <div class="border border-border bg-card p-6 space-y-4">
              <h2 class="text-xs uppercase tracking-[0.3em] text-maroon">زمان تحویل</h2>
              <div class="flex items-start gap-3">
                <Clock class="mt-0.5 h-4 w-4 shrink-0 text-muted-foreground" />
                <div>
                  <div class="text-sm font-medium text-foreground">تحویل تخمینی</div>
                  <div class="text-sm text-muted-foreground">تا {{ estimatedDays }}</div>
                </div>
              </div>
              <div class="flex items-start gap-3">
                <MapPin class="mt-0.5 h-4 w-4 shrink-0 text-muted-foreground" />
                <div>
                  <div class="text-sm font-medium text-foreground">روش ارسال</div>
                  <div class="text-sm text-muted-foreground">
                    {{ order?.payMethod === 'cod' ? 'پرداخت در محل' : 'ارسال پستی' }}
                  </div>
                </div>
              </div>
            </div>

            <div class="border border-border bg-card p-6 space-y-3">
              <h2 class="text-xs uppercase tracking-[0.3em] text-maroon">پیگیری سفارش</h2>
              <p class="text-xs leading-6 text-muted-foreground">
                با مراجعه به صفحه‌ی حساب کاربری یا وارد کردن کد پیگیری می‌توانید وضعیت سفارش خود را دنبال کنید.
              </p>
              <div class="flex items-center gap-2 rounded border border-border bg-background px-3 py-2">
                <span class="text-xs text-muted-foreground">کد پیگیری:</span>
                <span class="flex-1 font-mono text-sm font-semibold tracking-widest text-maroon">{{ ref_ || order?.ref }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Action buttons -->
        <div class="flex flex-col gap-3 sm:flex-row sm:justify-center">
          <RouterLink
            to="/account"
            class="flex items-center justify-center gap-2 bg-maroon px-8 py-3 text-sm text-white hover:opacity-90 transition-opacity"
          >
            <Package class="h-4 w-4" />
            مشاهده سفارش‌های من
          </RouterLink>
          <RouterLink
            to="/products"
            class="flex items-center justify-center gap-2 border border-border px-8 py-3 text-sm text-foreground hover:border-maroon hover:text-maroon transition-colors"
          >
            <ChevronLeft class="h-4 w-4" />
            ادامه خرید
          </RouterLink>
          <RouterLink
            to="/tracking"
            class="flex items-center justify-center gap-2 border border-border px-8 py-3 text-sm text-foreground hover:border-maroon hover:text-maroon transition-colors"
          >
            ردیابی سفارش
          </RouterLink>
        </div>

      </div>
    </div>
  </TheLayout>
</template>
