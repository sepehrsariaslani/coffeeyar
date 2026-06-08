<script setup>
import { useSiteSettingsStore } from "@/stores/siteSettings.js";
import { ref } from "vue";
import { Save, ExternalLink, Info, Check, Truck, CreditCard } from "lucide-vue-next";

const store = useSiteSettingsStore();
const saved = ref(false);

function saveAll() {
  store.save();
  saved.value = true;
  setTimeout(() => (saved.value = false), 2000);
}
</script>

<template>
  <div class="p-4 md:p-10 max-w-3xl" dir="rtl">
    <div class="mb-8 flex flex-wrap items-end justify-between gap-4">
      <div>
        <h1 class="text-3xl font-light">تنظیمات سایت <span class="text-maroon">.</span></h1>
        <p class="mt-2 text-sm text-muted-foreground">اطلاعات فروشگاه، روش‌های پرداخت، ارسال و درگاه</p>
      </div>
      <button
        type="button"
        @click="saveAll"
        :class="['flex items-center gap-2 px-5 py-2.5 text-sm transition-colors', saved ? 'bg-green-600 text-white' : 'bg-maroon text-maroon-foreground hover:opacity-90']"
      >
        <Check v-if="saved" class="h-4 w-4" />
        <Save v-else class="h-4 w-4" />
        {{ saved ? 'ذخیره شد' : 'ذخیره تغییرات' }}
      </button>
    </div>

    <div class="space-y-10">

      <!-- Shop Info -->
      <section class="border border-border p-6 space-y-4">
        <h2 class="text-xs uppercase tracking-widest text-maroon">اطلاعات فروشگاه</h2>
        <div class="grid gap-4 sm:grid-cols-2">
          <label class="block">
            <span class="field-label">نام فروشگاه</span>
            <input v-model="store.settings.shopName" @input="store.save()" class="field-input" />
          </label>
          <label class="block">
            <span class="field-label">شماره تماس</span>
            <input v-model="store.settings.phone" @input="store.save()" dir="ltr" placeholder="021-12345678" class="field-input" />
          </label>
          <label class="block">
            <span class="field-label">ایمیل</span>
            <input v-model="store.settings.email" @input="store.save()" dir="ltr" placeholder="info@example.ir" class="field-input" />
          </label>
          <label class="block">
            <span class="field-label">آدرس</span>
            <input v-model="store.settings.address" @input="store.save()" placeholder="تهران، خیابان ..." class="field-input" />
          </label>
        </div>
        <label class="block">
          <span class="field-label">توضیح کوتاه (در فوتر نمایش داده می‌شود)</span>
          <textarea v-model="store.settings.description" @input="store.save()" rows="2" class="field-input resize-none" />
        </label>
      </section>

      <!-- Social Links -->
      <section class="border border-border p-6 space-y-4">
        <h2 class="text-xs uppercase tracking-widest text-maroon">شبکه‌های اجتماعی</h2>
        <div class="grid gap-4 sm:grid-cols-2">
          <label class="block">
            <span class="field-label">لینک اینستاگرام</span>
            <input v-model="store.settings.instagram" @input="store.save()" dir="ltr" placeholder="https://instagram.com/..." class="field-input" />
          </label>
          <label class="block">
            <span class="field-label">لینک تلگرام / واتساپ</span>
            <input v-model="store.settings.telegram" @input="store.save()" dir="ltr" placeholder="https://t.me/..." class="field-input" />
          </label>
        </div>
      </section>

      <!-- Payment Methods -->
      <section class="border border-border p-6 space-y-5">
        <div class="flex items-center gap-3">
          <CreditCard class="h-4 w-4 text-maroon" />
          <h2 class="text-xs uppercase tracking-widest text-maroon">روش‌های پرداخت</h2>
        </div>
        <p class="text-xs text-muted-foreground -mt-2">روش‌هایی که می‌خواهید در صفحه checkout نمایش داده شوند را فعال کنید.</p>

        <div class="space-y-3">
          <label class="flex items-center justify-between border border-border p-4 cursor-pointer hover:bg-accent/30 transition-colors">
            <div>
              <div class="text-sm font-medium">پرداخت آنلاین (درگاه بانکی)</div>
              <div class="text-xs text-muted-foreground mt-0.5">اتصال به درگاه زرین‌پال یا سایر درگاه‌ها</div>
            </div>
            <input type="checkbox" v-model="store.settings.paymentMethods.online" @change="store.save()" class="accent-[var(--maroon)] h-4 w-4" />
          </label>

          <label class="flex items-center justify-between border border-border p-4 cursor-pointer hover:bg-accent/30 transition-colors">
            <div>
              <div class="text-sm font-medium">پرداخت در محل (COD)</div>
              <div class="text-xs text-muted-foreground mt-0.5">کارت‌خوان یا نقد هنگام تحویل</div>
            </div>
            <input type="checkbox" v-model="store.settings.paymentMethods.cod" @change="store.save()" class="accent-[var(--maroon)] h-4 w-4" />
          </label>

          <label class="flex items-center justify-between border border-border p-4 cursor-pointer hover:bg-accent/30 transition-colors">
            <div>
              <div class="text-sm font-medium">کیف پول</div>
              <div class="text-xs text-muted-foreground mt-0.5">استفاده از موجودی کیف پول کاربر</div>
            </div>
            <input type="checkbox" v-model="store.settings.paymentMethods.wallet" @change="store.save()" class="accent-[var(--maroon)] h-4 w-4" />
          </label>
        </div>

        <div v-if="!store.settings.paymentMethods.online && !store.settings.paymentMethods.cod && !store.settings.paymentMethods.wallet"
          class="border border-amber-200 bg-amber-50 p-3 text-xs text-amber-700 dark:border-amber-800 dark:bg-amber-950 dark:text-amber-300">
          ⚠ هیچ روش پرداختی فعال نیست. حداقل یک روش را فعال کنید.
        </div>
      </section>

      <!-- Shipping Methods -->
      <section class="border border-border p-6 space-y-5">
        <div class="flex items-center gap-3">
          <Truck class="h-4 w-4 text-maroon" />
          <h2 class="text-xs uppercase tracking-widest text-maroon">روش‌های ارسال</h2>
        </div>
        <p class="text-xs text-muted-foreground -mt-2">هزینه و شرایط ارسال را تنظیم کنید.</p>

        <!-- Standard Shipping -->
        <div class="border border-border p-5 space-y-4">
          <div class="flex items-center justify-between">
            <div class="font-medium text-sm">ارسال عادی</div>
            <label class="flex items-center gap-2 cursor-pointer">
              <span class="text-xs text-muted-foreground">فعال</span>
              <input type="checkbox" v-model="store.settings.shipping.standard.enabled" @change="store.save()" class="accent-[var(--maroon)] h-4 w-4" />
            </label>
          </div>
          <div :class="['grid gap-4 sm:grid-cols-2', !store.settings.shipping.standard.enabled ? 'opacity-50 pointer-events-none' : '']">
            <label class="block">
              <span class="field-label">عنوان نمایشی</span>
              <input v-model="store.settings.shipping.standard.label" @input="store.save()" class="field-input" placeholder="ارسال عادی" />
            </label>
            <label class="block">
              <span class="field-label">زمان تحویل</span>
              <input v-model="store.settings.shipping.standard.days" @input="store.save()" class="field-input" placeholder="۲ تا ۴ روز کاری" />
            </label>
            <label class="block">
              <span class="field-label">هزینه ارسال (تومان)</span>
              <input type="number" v-model.number="store.settings.shipping.standard.price" @input="store.save()" dir="ltr" class="field-input" min="0" />
            </label>
            <label class="block">
              <span class="field-label">آستانه ارسال رایگان (تومان)</span>
              <input type="number" v-model.number="store.settings.shipping.standard.freeThreshold" @input="store.save()" dir="ltr" class="field-input" min="0" placeholder="0 = بدون ارسال رایگان" />
            </label>
          </div>
          <p v-if="store.settings.shipping.standard.enabled && store.settings.shipping.standard.freeThreshold > 0" class="text-xs text-muted-foreground">
            ✓ ارسال رایگان برای خریدهای بالای {{ store.settings.shipping.standard.freeThreshold.toLocaleString('fa-IR') }} تومان
          </p>
        </div>

        <!-- Express Shipping -->
        <div class="border border-border p-5 space-y-4">
          <div class="flex items-center justify-between">
            <div class="font-medium text-sm">ارسال اکسپرس</div>
            <label class="flex items-center gap-2 cursor-pointer">
              <span class="text-xs text-muted-foreground">فعال</span>
              <input type="checkbox" v-model="store.settings.shipping.express.enabled" @change="store.save()" class="accent-[var(--maroon)] h-4 w-4" />
            </label>
          </div>
          <div :class="['grid gap-4 sm:grid-cols-2', !store.settings.shipping.express.enabled ? 'opacity-50 pointer-events-none' : '']">
            <label class="block">
              <span class="field-label">عنوان نمایشی</span>
              <input v-model="store.settings.shipping.express.label" @input="store.save()" class="field-input" placeholder="ارسال اکسپرس" />
            </label>
            <label class="block">
              <span class="field-label">زمان تحویل</span>
              <input v-model="store.settings.shipping.express.days" @input="store.save()" class="field-input" placeholder="۲۴ ساعته" />
            </label>
            <label class="block">
              <span class="field-label">هزینه ارسال (تومان)</span>
              <input type="number" v-model.number="store.settings.shipping.express.price" @input="store.save()" dir="ltr" class="field-input" min="0" />
            </label>
          </div>
        </div>
      </section>

      <!-- Enamad -->
      <section class="border border-border p-6 space-y-5">
        <div class="flex items-start justify-between gap-4">
          <div>
            <h2 class="text-xs uppercase tracking-widest text-maroon">نماد اعتماد الکترونیکی (اینماد)</h2>
            <p class="mt-1.5 text-xs text-muted-foreground">نماد اینماد اعتبار کسب‌وکار شما را نزد مشتری اثبات می‌کند و برای فروشگاه‌های اینترنتی اجباری است.</p>
          </div>
          <a href="https://enamad.ir" target="_blank" rel="noopener" class="shrink-0 flex items-center gap-1.5 border border-border px-3 py-1.5 text-xs hover:bg-accent whitespace-nowrap">
            <ExternalLink class="h-3 w-3" /> سایت اینماد
          </a>
        </div>

        <div class="bg-muted/40 border border-border p-4 space-y-2">
          <div class="flex items-center gap-2 text-xs font-medium text-maroon mb-3">
            <Info class="h-3.5 w-3.5" /> راهنمای دریافت نماد اینماد
          </div>
          <div class="space-y-2 text-xs text-muted-foreground">
            <div class="flex gap-3"><span class="w-5 h-5 rounded-full bg-maroon text-white flex items-center justify-center shrink-0 text-[10px]">۱</span><span>به سایت <strong class="text-foreground">enamad.ir</strong> مراجعه کنید و ثبت‌نام کنید.</span></div>
            <div class="flex gap-3"><span class="w-5 h-5 rounded-full bg-maroon text-white flex items-center justify-center shrink-0 text-[10px]">۲</span><span>از بخش "کسب‌وکار من" → "افزودن کسب‌وکار" دامنه‌ی سایت خود را وارد کنید.</span></div>
            <div class="flex gap-3"><span class="w-5 h-5 rounded-full bg-maroon text-white flex items-center justify-center shrink-0 text-[10px]">۳</span><span>مدارک هویتی و کسب‌وکار را بارگذاری کنید. معمولاً ۱ تا ۳ روز کاری طول می‌کشد.</span></div>
            <div class="flex gap-3"><span class="w-5 h-5 rounded-full bg-maroon text-white flex items-center justify-center shrink-0 text-[10px]">۴</span><span>بعد از تأیید، از بخش "نماد" → "دریافت کد" کد HTML را کپی کنید.</span></div>
            <div class="flex gap-3"><span class="w-5 h-5 rounded-full bg-maroon text-white flex items-center justify-center shrink-0 text-[10px]">۵</span><span>کد HTML را در کادر زیر paste کنید و دکمه‌ی «ذخیره» را بزنید.</span></div>
          </div>
        </div>

        <label class="block">
          <span class="field-label">کد HTML نماد اینماد (از سایت enamad.ir کپی کنید)</span>
          <textarea
            v-model="store.settings.enamadCode"
            @input="store.save()"
            dir="ltr"
            rows="5"
            placeholder='<a referrerpolicy="origin" target="_blank" href="https://trustseal.enamad.ir/?id=...">'
            class="field-input resize-none text-xs font-mono"
          />
        </label>

        <div v-if="store.settings.enamadCode" class="border border-border p-4 bg-muted/20">
          <div class="text-xs text-muted-foreground mb-3">پیش‌نمایش نماد:</div>
          <div v-html="store.settings.enamadCode" class="inline-block" />
        </div>
        <div v-else class="border border-dashed border-border p-4 text-center text-xs text-muted-foreground">
          بعد از وارد کردن کد اینماد، نماد اینجا نمایش داده می‌شود
        </div>
      </section>

      <!-- Zarinpal -->
      <section class="border border-border p-6 space-y-5">
        <div class="flex items-start justify-between gap-4">
          <div>
            <h2 class="text-xs uppercase tracking-widest text-maroon">درگاه پرداخت زرین‌پال</h2>
            <p class="mt-1.5 text-xs text-muted-foreground">زرین‌پال یکی از امن‌ترین و پرکاربردترین درگاه‌های پرداخت اینترنتی ایران است.</p>
          </div>
          <a href="https://zarinpal.com" target="_blank" rel="noopener" class="shrink-0 flex items-center gap-1.5 border border-border px-3 py-1.5 text-xs hover:bg-accent whitespace-nowrap">
            <ExternalLink class="h-3 w-3" /> سایت زرین‌پال
          </a>
        </div>

        <div class="bg-muted/40 border border-border p-4 space-y-2">
          <div class="flex items-center gap-2 text-xs font-medium text-maroon mb-3">
            <Info class="h-3.5 w-3.5" /> راهنمای اتصال زرین‌پال
          </div>
          <div class="space-y-2 text-xs text-muted-foreground">
            <div class="flex gap-3"><span class="w-5 h-5 rounded-full bg-maroon text-white flex items-center justify-center shrink-0 text-[10px]">۱</span><span>به <strong class="text-foreground">zarinpal.com</strong> بروید و یک حساب تجاری (Business) باز کنید.</span></div>
            <div class="flex gap-3"><span class="w-5 h-5 rounded-full bg-maroon text-white flex items-center justify-center shrink-0 text-[10px]">۲</span><span>از منوی داشبورد → "درگاه پرداخت" → "ایجاد درگاه جدید" اقدام کنید.</span></div>
            <div class="flex gap-3"><span class="w-5 h-5 rounded-full bg-maroon text-white flex items-center justify-center shrink-0 text-[10px]">۳</span><span>اطلاعات کسب‌وکار و مدارک هویتی را بارگذاری کنید.</span></div>
            <div class="flex gap-3"><span class="w-5 h-5 rounded-full bg-maroon text-white flex items-center justify-center shrink-0 text-[10px]">۴</span><span>بعد از تأیید، <strong class="text-foreground">Merchant ID</strong> خود را از تنظیمات درگاه کپی کنید.</span></div>
            <div class="flex gap-3"><span class="w-5 h-5 rounded-full bg-maroon text-white flex items-center justify-center shrink-0 text-[10px]">۵</span><span>Merchant ID را در کادر زیر وارد کنید و درگاه را فعال کنید.</span></div>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" v-model="store.settings.zarinpalEnabled" @change="store.save()" class="accent-[var(--maroon)]" />
            <span class="text-sm">درگاه زرین‌پال فعال باشد</span>
          </label>
        </div>

        <label class="block">
          <span class="field-label">Merchant ID زرین‌پال</span>
          <input
            v-model="store.settings.zarinpalMerchantId"
            @input="store.save()"
            dir="ltr"
            :disabled="!store.settings.zarinpalEnabled"
            placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            class="field-input font-mono disabled:opacity-40 disabled:cursor-not-allowed"
          />
        </label>

        <div class="flex items-center gap-3">
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" v-model="store.settings.zarinpalSandbox" @change="store.save()" :disabled="!store.settings.zarinpalEnabled" class="accent-[var(--maroon)]" />
            <span class="text-sm">حالت آزمایشی (Sandbox) — برای تست قبل از راه‌اندازی واقعی</span>
          </label>
        </div>

        <div v-if="store.settings.zarinpalEnabled && store.settings.zarinpalMerchantId" class="border border-green-200 bg-green-50 p-4 text-xs text-green-800 dark:border-green-800 dark:bg-green-950 dark:text-green-300">
          ✓ Merchant ID ذخیره شد. درگاه زرین‌پال {{ store.settings.zarinpalSandbox ? 'در حالت آزمایشی' : 'واقعی' }} فعال است.
        </div>
      </section>

    </div>
  </div>
</template>

<style scoped>
.field-label {
  display: block;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--muted-foreground);
  margin-bottom: 0.375rem;
}
.field-input {
  display: block;
  width: 100%;
  border: 1px solid var(--color-border);
  background-color: var(--color-background);
  padding: 0.625rem 0.75rem;
  font-size: 0.875rem;
  outline: none;
  margin-top: 0.25rem;
}
.field-input:focus { border-color: var(--color-maroon); }
</style>
