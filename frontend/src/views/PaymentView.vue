<script setup>
import { ref, computed, onMounted } from "vue";

import { useRoute, useRouter } from "vue-router";
import { Lock, CheckCircle2, Loader2, ShieldCheck, CreditCard } from "lucide-vue-next";
function formatPrice(n) { return n ? Number(n).toLocaleString("fa-IR") : "۰"; }

const route = useRoute();
const router = useRouter();

const amount = computed(() => Number(route.query.amount) || 0);
const orderRef = computed(() => route.query.ref || "");

const step = ref("form"); // form | processing | done
const cardNum = ref("");
const expiry = ref("");
const cvv2 = ref("");
const cardPass = ref("");
const error = ref("");

onMounted(() => {
  const isCod = route.query.cod === "1";
  const isWallet = route.query.wallet === "1";
  if (isCod || isWallet) {
    router.replace(`/order-success?ref=${route.query.ref || ""}&amount=${route.query.amount || 0}`);
  }
});

function formatCard(val) {
  return val.replace(/\D/g, "").replace(/(\d{4})(?=\d)/g, "$1-").slice(0, 19);
}
function formatExpiry(val) {
  return val.replace(/\D/g, "").replace(/(\d{2})(?=\d)/, "$1/").slice(0, 5);
}

function onCardInput(e) { cardNum.value = formatCard(e.target.value); }
function onExpiryInput(e) { expiry.value = formatExpiry(e.target.value); }

async function pay(e) {
  e.preventDefault();
  error.value = "";
  if (cardNum.value.replace(/-/g, "").length < 16) { error.value = "شماره کارت معتبر نیست"; return; }
  if (expiry.value.length < 5) { error.value = "تاریخ انقضا معتبر نیست"; return; }
  if (cvv2.value.length < 3) { error.value = "CVV2 معتبر نیست"; return; }
  if (cardPass.value.length < 4) { error.value = "رمز دوم معتبر نیست"; return; }

  step.value = "processing";
  await new Promise((r) => setTimeout(r, 3000));
  router.replace(`/order-success?ref=${orderRef.value}&amount=${amount.value}`);
}
</script>

<template>
  <div class="min-h-screen bg-[#f5f5f0] font-[Vazirmatn]" dir="rtl">

    <!-- Bank Header -->
    <header class="bg-[#00539C] text-white shadow-lg">
      <div class="mx-auto flex max-w-3xl items-center justify-between px-6 py-4">
        <div class="flex items-center gap-3">
          <div class="rounded bg-white/20 p-1.5">
            <CreditCard class="h-5 w-5" />
          </div>
          <div>
            <div class="text-sm font-semibold">درگاه پرداخت امن</div>
            <div class="text-[10px] opacity-70">Navar Payment Gateway</div>
          </div>
        </div>
        <div class="flex items-center gap-2 text-xs opacity-80">
          <Lock class="h-3.5 w-3.5" />
          SSL Secured
        </div>
      </div>
    </header>

    <!-- Processing -->
    <div v-if="step === 'processing'" class="flex min-h-[70vh] flex-col items-center justify-center gap-6 text-center px-6">
      <div class="relative">
        <div class="h-20 w-20 rounded-full border-4 border-[#00539C]/20 border-t-[#00539C] animate-spin" />
        <CreditCard class="absolute inset-0 m-auto h-8 w-8 text-[#00539C]" />
      </div>
      <div>
        <div class="text-lg font-medium text-gray-800">در حال پردازش پرداخت...</div>
        <div class="mt-2 text-sm text-gray-500">لطفاً صفحه را نبندید</div>
      </div>
      <div class="flex gap-1">
        <span v-for="i in 3" :key="i" class="h-2 w-2 rounded-full bg-[#00539C] animate-bounce" :style="{ animationDelay: `${(i-1) * 0.2}s` }" />
      </div>
    </div>

    <!-- Success -->
    <div v-else-if="step === 'done'" class="flex min-h-[70vh] flex-col items-center justify-center gap-5 text-center px-6">
      <CheckCircle2 class="h-16 w-16 text-green-500" />
      <div>
        <div class="text-2xl font-medium text-gray-800">پرداخت موفق بود!</div>
        <div class="mt-2 text-sm text-gray-500">سفارش شما با موفقیت ثبت شد</div>
      </div>
      <div class="rounded-lg border border-gray-200 bg-white px-6 py-4 text-right space-y-2 w-full max-w-xs">
        <div class="flex justify-between text-sm">
          <span class="text-gray-500">کد پیگیری</span>
          <span class="font-mono font-medium text-[#00539C]">{{ orderRef }}</span>
        </div>
        <div class="flex justify-between text-sm">
          <span class="text-gray-500">مبلغ پرداختی</span>
          <span class="font-medium text-green-600">{{ formatPrice(amount) }}</span>
        </div>
      </div>
      <div class="flex gap-3 mt-2">
        <button @click="goAccount" class="bg-[#00539C] px-6 py-2.5 text-sm text-white hover:opacity-90 rounded">مشاهده سفارش‌ها</button>
        <button @click="goHome" class="border border-gray-300 px-6 py-2.5 text-sm text-gray-700 hover:bg-gray-50 rounded">بازگشت به خانه</button>
      </div>
    </div>

    <!-- Form -->
    <div v-else class="mx-auto max-w-3xl px-4 py-8">
      <div class="grid gap-6 lg:grid-cols-[1fr_320px]">

        <!-- Card form -->
        <div class="rounded-lg border border-gray-200 bg-white shadow-sm">
          <div class="border-b border-gray-100 px-6 py-4">
            <div class="text-sm font-semibold text-gray-700">اطلاعات کارت بانکی</div>
            <div class="mt-0.5 text-xs text-gray-400">اطلاعات شما رمزگذاری شده و امن است</div>
          </div>

          <form @submit="pay" class="space-y-5 p-6">
            <!-- Error -->
            <div v-if="error" class="rounded border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{{ error }}</div>

            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1.5">شماره کارت</label>
              <div class="relative">
                <input
                  :value="cardNum"
                  @input="onCardInput"
                  placeholder="---- ---- ---- ----"
                  maxlength="19"
                  dir="ltr"
                  class="w-full rounded border border-gray-300 px-3 py-3 text-left font-mono text-base tracking-widest outline-none focus:border-[#00539C] focus:ring-1 focus:ring-[#00539C]/30"
                />
                <CreditCard class="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-300" />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1.5">تاریخ انقضا</label>
                <input
                  :value="expiry"
                  @input="onExpiryInput"
                  placeholder="MM/YY"
                  maxlength="5"
                  dir="ltr"
                  class="w-full rounded border border-gray-300 px-3 py-3 text-left font-mono outline-none focus:border-[#00539C] focus:ring-1 focus:ring-[#00539C]/30"
                />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-1.5">CVV2</label>
                <input
                  v-model="cvv2"
                  placeholder="•••"
                  maxlength="4"
                  type="password"
                  dir="ltr"
                  class="w-full rounded border border-gray-300 px-3 py-3 text-left font-mono outline-none focus:border-[#00539C] focus:ring-1 focus:ring-[#00539C]/30"
                />
              </div>
            </div>

            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1.5">رمز دوم (اینترنتی)</label>
              <input
                v-model="cardPass"
                type="password"
                placeholder="رمز دوم پویا یا ثابت"
                dir="ltr"
                class="w-full rounded border border-gray-300 px-3 py-3 outline-none focus:border-[#00539C] focus:ring-1 focus:ring-[#00539C]/30"
              />
              <p class="mt-1.5 text-[11px] text-gray-400">رمز پویا از برنامه همراه بانک خود دریافت کنید</p>
            </div>

            <button type="submit" class="w-full rounded bg-[#00539C] py-3.5 text-sm font-medium text-white hover:opacity-90 flex items-center justify-center gap-2">
              <Lock class="h-4 w-4" />
              پرداخت {{ formatPrice(amount) }}
            </button>
          </form>
        </div>

        <!-- Summary -->
        <div class="space-y-4">
          <div class="rounded-lg border border-gray-200 bg-white shadow-sm p-5">
            <div class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">خلاصه تراکنش</div>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-500">شماره سفارش</span>
                <span class="font-mono text-xs text-gray-700">{{ orderRef }}</span>
              </div>
              <div class="flex justify-between border-t border-gray-100 pt-2 mt-2">
                <span class="text-gray-500">مبلغ قابل پرداخت</span>
                <span class="font-semibold text-[#00539C] text-base">{{ formatPrice(amount) }}</span>
              </div>
            </div>
          </div>

          <div class="rounded-lg border border-gray-200 bg-white shadow-sm p-5 space-y-3">
            <div class="flex items-center gap-2 text-xs text-gray-500">
              <ShieldCheck class="h-4 w-4 text-green-500 shrink-0" />
              پرداخت امن با رمزنگاری SSL
            </div>
            <div class="flex items-center gap-2 text-xs text-gray-500">
              <Lock class="h-4 w-4 text-green-500 shrink-0" />
              اطلاعات کارت شما ذخیره نمی‌شود
            </div>
          </div>

          <div class="rounded-lg border border-gray-100 bg-gray-50 p-4 text-center">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Visa_Inc._logo.svg/200px-Visa_Inc._logo.svg.png" alt="Visa" class="h-5 inline-block mx-2 grayscale opacity-50" />
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Mastercard_2019_logo.svg/200px-Mastercard_2019_logo.svg.png" alt="Mastercard" class="h-5 inline-block mx-2 grayscale opacity-50" />
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="mt-12 border-t border-gray-200 bg-white px-6 py-4 text-center text-[11px] text-gray-400">
      این درگاه توسط نوار ارائه می‌شود · تمام اطلاعات رمزنگاری شده است
    </footer>
  </div>
</template>
