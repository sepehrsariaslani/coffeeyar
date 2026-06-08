<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter, RouterLink } from "vue-router";
import { Lock, Tag, X, Wallet, UserCheck } from "lucide-vue-next";
import TheLayout from "@/components/site/TheLayout.vue";
import { useCartStore } from "@/stores/cart.js";
import { useWalletStore } from "@/stores/wallet.js";
import { useNotificationsStore } from "@/stores/notifications.js";
import { useAdminNotificationsStore } from "@/stores/adminNotifications.js";
import { useCouponsStore } from "@/stores/coupons.js";
import { useAuthStore } from "@/stores/auth.js";
import { useSiteSettingsStore } from "@/stores/siteSettings.js";
import { toFa } from "@/lib/utils.js";

function formatPrice(n) {
  if (!n && n !== 0) return "۰";
  return Number(n).toLocaleString("fa-IR");
}
import { useSeo } from "@/composables/useSeo.js";

useSeo({ title: "پرداخت", description: "تکمیل سفارش و پرداخت" });

const router = useRouter();
const cartStore = useCartStore();
const walletStore = useWalletStore();
const notifStore = useNotificationsStore();
const adminNotifStore = useAdminNotificationsStore();
const couponsStore = useCouponsStore();
const authStore = useAuthStore();
const siteSettings = useSiteSettingsStore();

const pm = computed(() => siteSettings.settings.paymentMethods);
const sm = computed(() => siteSettings.settings.shipping);

const pay = ref("online");
const ship = ref("standard");

// ── Form fields ────────────────────────────────────────────────────────────
const formName     = ref("");
const formPhone    = ref("");
const formEmail    = ref("");
const formProvince = ref("");
const formCity     = ref("");
const formPostal   = ref("");
const formUnit     = ref("");
const formAddress  = ref("");

const autofilled = ref(false);

onMounted(() => {
  if (authStore.isLoggedIn && authStore.user) {
    const u = authStore.user;
    formName.value     = u.name     || "";
    formPhone.value    = u.phone    || "";
    formEmail.value    = u.email    || "";
    formProvince.value = u.province || "";
    formCity.value     = u.city     || "";
    formPostal.value   = u.postalCode || "";
    formUnit.value     = u.unit     || "";
    formAddress.value  = u.address  || "";
    if (u.name || u.phone) autofilled.value = true;
  }

  // auto-select first enabled payment method
  if (!pm.value.online && pm.value.cod) pay.value = "cod";
  else if (!pm.value.online && !pm.value.cod && pm.value.wallet) pay.value = "wallet";
  else pay.value = "online";

  // auto-select first enabled shipping method
  if (!sm.value.standard?.enabled && sm.value.express?.enabled) ship.value = "express";
  else ship.value = "standard";
});

// ── Coupon ─────────────────────────────────────────────────────────────────
const couponInput = ref("");
const coupon = ref(null);
const couponError = ref("");

function applyCoupon() {
  couponError.value = "";
  const result = couponsStore.validate(couponInput.value, subtotal.value);
  if (result.ok) {
    coupon.value = { code: result.coupon.code, label: result.coupon.label, pct: result.coupon.type === "percent" ? result.coupon.value : 0, fixed: result.coupon.type === "fixed" ? result.coupon.value : 0 };
  } else {
    couponError.value = result.error;
  }
}

function removeCoupon() {
  coupon.value = null;
  couponInput.value = "";
  couponError.value = "";
}

// ── Totals ─────────────────────────────────────────────────────────────────
const subtotal = computed(() => cartStore.total);
const discount = computed(() => {
  if (!coupon.value) return 0;
  if (coupon.value.fixed) return Math.min(coupon.value.fixed, subtotal.value);
  return Math.round(subtotal.value * coupon.value.pct / 100);
});
const shippingCost = computed(() => {
  const s = sm.value[ship.value];
  if (!s) return 0;
  if (s.freeThreshold > 0 && subtotal.value >= s.freeThreshold) return 0;
  return s.price || 0;
});
const total = computed(() => subtotal.value - discount.value + shippingCost.value);

const walletError = ref("");

// ── Submit ─────────────────────────────────────────────────────────────────
function submit(e) {
  e.preventDefault();
  walletError.value = "";
  const ref_ = "NV-" + Math.random().toString(36).slice(2, 8).toUpperCase();
  const itemsSummary = cartStore.items.map((i) => `${i.name} ×${i.qty}`).join("، ");

  // Save address to user profile
  if (authStore.isLoggedIn) {
    authStore.updateUser({
      name:       formName.value,
      phone:      formPhone.value,
      email:      formEmail.value,
      province:   formProvince.value,
      city:       formCity.value,
      postalCode: formPostal.value,
      unit:       formUnit.value,
      address:    formAddress.value,
    });
  }

  if (pay.value === "wallet") {
    if (walletStore.balance < total.value) {
      walletError.value = `موجودی کیف پول (${formatPrice(walletStore.balance)}) کافی نیست.`;
      return;
    }
    walletStore.spend(total.value, `پرداخت سفارش ${ref_}`);
    notifStore.add("سفارش ثبت شد", `سفارش ${ref_} با موفقیت ثبت شد و مبلغ از کیف پول کسر شد.`, "order");
    adminNotifStore.add(`سفارش جدید — ${ref_}`, itemsSummary, ref_, total.value);
    localStorage.setItem("navar-last-order", JSON.stringify({
      ref: ref_,
      items: cartStore.items.map((i) => ({ name: i.name, qty: i.qty, price: i.unitPrice, image: i.image })),
      subtotal: subtotal.value, discount: discount.value, shipping: shippingCost.value,
      total: total.value, coupon: coupon.value?.code || null, payMethod: pay.value,
      date: new Date().toLocaleDateString("fa-IR"),
    }));
    cartStore.clear();
    router.push(`/payment?amount=0&ref=${ref_}&wallet=1`);
    return;
  }

  adminNotifStore.add(`سفارش جدید — ${ref_}`, itemsSummary, ref_, total.value);
  notifStore.add("سفارش ثبت شد", `سفارش ${ref_} ثبت شد و در حال پردازش است.`, "order");

  localStorage.setItem("navar-last-order", JSON.stringify({
    ref: ref_,
    items: cartStore.items.map((i) => ({ name: i.name, qty: i.qty, price: i.unitPrice, image: i.image })),
    subtotal: subtotal.value, discount: discount.value, shipping: shippingCost.value,
    total: total.value, coupon: coupon.value?.code || null, payMethod: pay.value,
    date: new Date().toLocaleDateString("fa-IR"),
  }));

  cartStore.clear();
  if (pay.value === "online") {
    router.push(`/payment?amount=${total.value}&ref=${ref_}`);
  } else {
    router.push(`/payment?amount=0&ref=${ref_}&cod=1`);
  }
}
</script>

<template>
  <TheLayout>
    <!-- Empty state -->
    <section v-if="cartStore.items.length === 0" class="mx-auto max-w-xl px-6 py-32 text-center">
      <h1 class="text-2xl font-light">سبد خرید خالی است</h1>
      <RouterLink to="/products" class="mt-6 inline-block text-maroon">مشاهده محصولات</RouterLink>
    </section>

    <template v-else>
      <section class="border-b border-border">
        <div class="mx-auto max-w-7xl px-6 py-12">
          <span class="text-xs uppercase tracking-[0.3em] text-maroon">تکمیل سفارش</span>
          <h1 class="mt-3 text-4xl font-light">پرداخت</h1>
        </div>
      </section>

      <form @submit="submit" class="mx-auto grid max-w-7xl gap-12 px-6 py-12 lg:grid-cols-[1.5fr_1fr]">
        <div class="space-y-10">

          <!-- Autofill notice -->
          <div v-if="autofilled" class="flex items-center gap-3 border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-800 dark:border-green-800 dark:bg-green-950 dark:text-green-300">
            <UserCheck class="h-4 w-4 shrink-0" />
            اطلاعات حساب شما پیش‌پر شد. در صورت نیاز ویرایش کنید.
          </div>

          <!-- Contact -->
          <div>
            <div class="mb-5 flex items-center gap-3">
              <span class="text-xs text-maroon">۰۱</span>
              <h2 class="text-lg font-medium">اطلاعات تماس</h2>
              <div class="h-px flex-1 bg-border" />
              <RouterLink v-if="!authStore.isLoggedIn" to="/auth" class="text-xs text-maroon hover:underline">
                ورود برای پیش‌پر خودکار
              </RouterLink>
            </div>
            <div class="grid gap-4 md:grid-cols-2">
              <div>
                <label class="block text-xs uppercase tracking-widest text-muted-foreground">نام و نام خانوادگی</label>
                <input required v-model="formName" class="mt-2 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon" />
              </div>
              <div>
                <label class="block text-xs uppercase tracking-widest text-muted-foreground">شماره موبایل</label>
                <input required type="tel" dir="ltr" v-model="formPhone" class="mt-2 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon" />
              </div>
              <div class="md:col-span-2">
                <label class="block text-xs uppercase tracking-widest text-muted-foreground">ایمیل (اختیاری)</label>
                <input type="email" dir="ltr" v-model="formEmail" class="mt-2 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon" />
              </div>
            </div>
          </div>

          <!-- Address -->
          <div>
            <div class="mb-5 flex items-center gap-3">
              <span class="text-xs text-maroon">۰۲</span>
              <h2 class="text-lg font-medium">آدرس ارسال</h2>
              <div class="h-px flex-1 bg-border" />
            </div>
            <div class="grid gap-4 md:grid-cols-2">
              <div>
                <label class="block text-xs uppercase tracking-widest text-muted-foreground">استان</label>
                <input required v-model="formProvince" class="mt-2 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon" />
              </div>
              <div>
                <label class="block text-xs uppercase tracking-widest text-muted-foreground">شهر</label>
                <input required v-model="formCity" class="mt-2 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon" />
              </div>
              <div>
                <label class="block text-xs uppercase tracking-widest text-muted-foreground">کد پستی</label>
                <input required dir="ltr" v-model="formPostal" class="mt-2 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon" />
              </div>
              <div>
                <label class="block text-xs uppercase tracking-widest text-muted-foreground">پلاک / واحد</label>
                <input v-model="formUnit" class="mt-2 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon" />
              </div>
              <div class="md:col-span-2">
                <label class="block text-xs uppercase tracking-widest text-muted-foreground">آدرس کامل</label>
                <textarea required rows="3" v-model="formAddress" class="mt-2 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon" />
              </div>
            </div>
          </div>

          <!-- Shipping -->
          <div>
            <div class="mb-5 flex items-center gap-3">
              <span class="text-xs text-maroon">۰۳</span>
              <h2 class="text-lg font-medium">روش ارسال</h2>
              <div class="h-px flex-1 bg-border" />
            </div>
            <div class="grid gap-3 md:grid-cols-2">
              <button
                v-if="sm.standard?.enabled"
                type="button"
                @click="ship = 'standard'"
                :class="['flex items-center justify-between border p-4 text-right transition-colors', ship === 'standard' ? 'border-maroon bg-maroon/5' : 'border-border hover:border-foreground']"
              >
                <div>
                  <div class="text-sm font-medium">{{ sm.standard.label }}</div>
                  <div class="mt-1 text-xs text-muted-foreground">{{ sm.standard.days }}</div>
                </div>
                <div class="text-xs text-maroon">
                  {{ sm.standard.freeThreshold > 0 && subtotal >= sm.standard.freeThreshold ? "رایگان" : formatPrice(sm.standard.price) }}
                </div>
              </button>
              <button
                v-if="sm.express?.enabled"
                type="button"
                @click="ship = 'express'"
                :class="['flex items-center justify-between border p-4 text-right transition-colors', ship === 'express' ? 'border-maroon bg-maroon/5' : 'border-border hover:border-foreground']"
              >
                <div>
                  <div class="text-sm font-medium">{{ sm.express.label }}</div>
                  <div class="mt-1 text-xs text-muted-foreground">{{ sm.express.days }}</div>
                </div>
                <div class="text-xs text-maroon">{{ formatPrice(sm.express.price) }}</div>
              </button>
              <div v-if="!sm.standard?.enabled && !sm.express?.enabled" class="text-sm text-muted-foreground border border-dashed border-border p-4 text-center">
                روش ارسال فعالی موجود نیست
              </div>
            </div>
            <p v-if="sm.standard?.enabled && sm.standard.freeThreshold > 0 && subtotal < sm.standard.freeThreshold" class="mt-2 text-xs text-muted-foreground">
              برای ارسال رایگان {{ formatPrice(sm.standard.freeThreshold - subtotal) }} دیگر خرید کنید.
            </p>
          </div>

          <!-- Payment method -->
          <div>
            <div class="mb-5 flex items-center gap-3">
              <span class="text-xs text-maroon">۰۴</span>
              <h2 class="text-lg font-medium">روش پرداخت</h2>
              <div class="h-px flex-1 bg-border" />
            </div>
            <div class="grid gap-3 md:grid-cols-3">
              <button
                v-if="pm.online"
                type="button"
                @click="pay = 'online'"
                :class="['flex items-center justify-between border p-4 text-right transition-colors', pay === 'online' ? 'border-maroon bg-maroon/5' : 'border-border hover:border-foreground']"
              >
                <div>
                  <div class="text-sm font-medium">پرداخت آنلاین</div>
                  <div class="mt-1 text-xs text-muted-foreground">درگاه امن بانکی</div>
                </div>
                <Lock class="h-4 w-4 text-maroon" />
              </button>
              <button
                v-if="pm.cod"
                type="button"
                @click="pay = 'cod'"
                :class="['flex items-center justify-between border p-4 text-right transition-colors', pay === 'cod' ? 'border-maroon bg-maroon/5' : 'border-border hover:border-foreground']"
              >
                <div>
                  <div class="text-sm font-medium">پرداخت در محل</div>
                  <div class="mt-1 text-xs text-muted-foreground">کارت‌خوان یا نقد</div>
                </div>
              </button>
              <button
                v-if="pm.wallet"
                type="button"
                @click="pay = 'wallet'"
                :class="['flex items-center justify-between border p-4 text-right transition-colors', pay === 'wallet' ? 'border-maroon bg-maroon/5' : 'border-border hover:border-foreground']"
              >
                <div>
                  <div class="text-sm font-medium">کیف پول</div>
                  <div class="mt-1 text-xs text-muted-foreground">موجودی: {{ formatPrice(walletStore.balance) }} ت</div>
                </div>
                <Wallet class="h-4 w-4 text-maroon" />
              </button>
              <div v-if="!pm.online && !pm.cod && !pm.wallet" class="text-sm text-muted-foreground border border-dashed border-border p-4 text-center">
                روش پرداخت فعالی موجود نیست
              </div>
            </div>
            <p v-if="walletError" class="mt-2 text-xs text-maroon">{{ walletError }}</p>
          </div>
        </div>

        <!-- Summary -->
        <aside class="h-fit border border-maroon/30 bg-muted/40 p-7">
          <div class="text-xs uppercase tracking-widest text-maroon">خلاصه</div>
          <h2 class="mt-1 text-xl font-light">سفارش شما</h2>

          <ul class="mt-5 divide-y divide-border border-y border-border">
            <li v-for="i in cartStore.items" :key="i.id" class="flex gap-3 py-3 text-sm">
              <img :src="i.image" alt="" class="h-14 w-14 object-cover shrink-0" />
              <div class="flex-1 min-w-0">
                <div class="line-clamp-1">{{ i.name }}</div>
                <div class="text-xs text-muted-foreground">{{ i.weight }} · {{ i.grind }} × {{ toFa(i.qty) }}</div>
              </div>
              <div class="text-xs text-maroon shrink-0">{{ formatPrice(i.unitPrice * i.qty) }}</div>
            </li>
          </ul>

          <!-- Coupon -->
          <div class="mt-5">
            <div v-if="coupon" class="flex items-center justify-between border border-maroon/30 bg-maroon/5 px-3 py-2.5">
              <div class="flex items-center gap-2 text-sm">
                <Tag class="h-4 w-4 text-maroon shrink-0" />
                <span class="text-maroon font-medium">{{ coupon.code }}</span>
                <span class="text-xs text-muted-foreground">— {{ coupon.label }}</span>
              </div>
              <button type="button" @click="removeCoupon" class="text-muted-foreground hover:text-maroon">
                <X class="h-4 w-4" />
              </button>
            </div>
            <div v-else class="flex gap-2">
              <input
                v-model="couponInput"
                placeholder="کد تخفیف"
                dir="ltr"
                class="flex-1 border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon"
              />
              <button type="button" @click="applyCoupon" class="border border-maroon px-4 py-2 text-xs text-maroon hover:bg-maroon hover:text-white transition-colors">
                اعمال
              </button>
            </div>
            <p v-if="couponError" class="mt-1.5 text-xs text-maroon">{{ couponError }}</p>
          </div>

          <dl class="mt-4 space-y-2 text-sm">
            <div class="flex justify-between">
              <dt class="text-muted-foreground">جمع کالاها</dt>
              <dd>{{ formatPrice(subtotal) }}</dd>
            </div>
            <div v-if="discount > 0" class="flex justify-between text-maroon">
              <dt>تخفیف ({{ coupon.pct }}٪)</dt>
              <dd>− {{ formatPrice(discount) }}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-muted-foreground">ارسال</dt>
              <dd>{{ shippingCost === 0 ? "رایگان" : formatPrice(shippingCost) }}</dd>
            </div>
          </dl>

          <div class="mt-4 flex items-baseline justify-between border-t border-border pt-4">
            <span class="text-sm">قابل پرداخت</span>
            <span class="text-xl font-light text-maroon">{{ formatPrice(total) }}</span>
          </div>

          <button type="submit" class="mt-5 w-full bg-maroon py-3.5 text-sm text-maroon-foreground hover:opacity-90 flex items-center justify-center gap-2">
            <Lock class="h-4 w-4" />
            {{ pay === 'online' ? 'پرداخت آنلاین' : pay === 'wallet' ? 'پرداخت با کیف پول' : 'ثبت سفارش' }}
          </button>
          <p class="mt-3 text-center text-[11px] text-muted-foreground">
            با ثبت سفارش،
            <RouterLink to="/policies" class="text-maroon hover:underline">قوانین فروشگاه</RouterLink>
            را می‌پذیرید.
          </p>
          <p v-if="pay === 'online'" class="mt-1.5 text-center text-[11px] text-muted-foreground flex items-center justify-center gap-1">
            <Lock class="h-3 w-3" /> پرداخت امن با رمزنگاری SSL
          </p>

          <!-- Coupon hints -->
          <div class="mt-4 border-t border-border pt-4">
            <div class="text-xs text-muted-foreground">کدهای تخفیف فعال:</div>
            <div class="mt-1.5 flex flex-wrap gap-1">
              <button
                v-for="c in couponsStore.coupons.filter(c => c.active)"
                :key="c.code"
                type="button"
                @click="couponInput = c.code; applyCoupon()"
                class="border border-border px-2 py-0.5 text-[10px] hover:border-maroon hover:text-maroon transition-colors font-mono"
              >
                {{ c.code }}
              </button>
            </div>
          </div>
        </aside>
      </form>
    </template>
  </TheLayout>
</template>
