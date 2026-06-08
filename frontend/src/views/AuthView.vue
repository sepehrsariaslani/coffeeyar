<script setup>
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth.js";
import { Eye, EyeOff, Loader2, Coffee, ShieldCheck, Truck } from "lucide-vue-next";
import TheLayout from "@/components/site/TheLayout.vue";
import { useSeo } from "@/composables/useSeo.js";

useSeo({ title: "ورود / ثبت‌نام", description: "وارد حساب کاربری خود شوید یا ثبت‌نام کنید" });

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const tab = ref("login");
const showPass = ref(false);
const loading = ref(false);
const error = ref("");

const loginForm = ref({ email: "", password: "" });
const registerForm = ref({ name: "", email: "", phone: "", password: "", confirm: "" });

async function submitLogin(e) {
  e.preventDefault();
  error.value = "";
  loading.value = true;
  await new Promise((r) => setTimeout(r, 600));
  const result = authStore.login(loginForm.value);
  loading.value = false;
  if (result.ok) {
    const redirect = route.query.redirect || "/account";
    router.push(redirect);
  } else error.value = result.error;
}

async function submitRegister(e) {
  e.preventDefault();
  error.value = "";
  if (registerForm.value.password !== registerForm.value.confirm) {
    error.value = "رمز عبور و تکرار آن یکسان نیستند";
    return;
  }
  if (registerForm.value.password.length < 6) {
    error.value = "رمز عبور باید حداقل ۶ کاراکتر باشد";
    return;
  }
  loading.value = true;
  await new Promise((r) => setTimeout(r, 600));
  const result = authStore.register(registerForm.value);
  loading.value = false;
  if (result.ok) {
    const redirect = route.query.redirect || "/account";
    router.push(redirect);
  } else error.value = result.error;
}

const perks = [
  { icon: Coffee, text: "سفارش آسان‌تر با ذخیره آدرس" },
  { icon: ShieldCheck, text: "پیگیری کامل سفارش‌هایتان" },
  { icon: Truck, text: "اعلان ارسال و تحویل" },
];
</script>

<template>
  <TheLayout>
    <div class="min-h-[calc(100vh-80px)] grid lg:grid-cols-[1fr_1.1fr]">
      <!-- Left panel — brand visual -->
      <div class="hidden lg:flex flex-col justify-between border-l border-border bg-foreground text-background p-16">
        <div>
          <span class="text-xs uppercase tracking-[0.3em] text-maroon">نـوار</span>
          <h2 class="mt-8 text-4xl font-light leading-snug">
            قهوه‌ای که<br />
            <span class="italic text-maroon">می‌خواستی</span>.
          </h2>
          <p class="mt-6 text-sm leading-8 text-background/60 max-w-xs">
            با داشتن حساب کاربری، تجربه خریدت رو کامل‌تر کن.
          </p>
        </div>

        <div class="space-y-5">
          <div v-for="p in perks" :key="p.text" class="flex items-center gap-4">
            <div class="flex h-10 w-10 shrink-0 items-center justify-center border border-background/20">
              <component :is="p.icon" class="h-4 w-4 text-maroon" />
            </div>
            <span class="text-sm text-background/70">{{ p.text }}</span>
          </div>
        </div>

        <div class="text-xs text-background/30">© ۱۴۰۳ نوار. تمامی حقوق محفوظ است.</div>
      </div>

      <!-- Right panel — form -->
      <div class="flex flex-col justify-center px-6 py-16 md:px-16 lg:px-20">
        <div class="mx-auto w-full max-w-md">
          <div class="mb-8">
            <span class="text-xs uppercase tracking-[0.3em] text-maroon">حساب کاربری</span>
            <h1 class="mt-3 text-3xl font-light">{{ tab === "login" ? "خوش برگشتی" : "بیا عضو ما شو" }}</h1>
            <p class="mt-2 text-sm text-muted-foreground">
              {{ tab === "login" ? "وارد حساب کاربری‌ات شو" : "ثبت‌نام رایگان در کمتر از یک دقیقه" }}
            </p>
          </div>

          <!-- Tabs -->
          <div class="mb-8 flex gap-1 border-b border-border">
            <button @click="tab = 'login'; error = ''"
              :class="['pb-3 px-1 text-sm transition-colors', tab === 'login' ? 'border-b-2 border-maroon text-maroon font-medium' : 'text-muted-foreground hover:text-foreground']">
              ورود
            </button>
            <button @click="tab = 'register'; error = ''"
              :class="['pb-3 px-1 text-sm transition-colors mr-5', tab === 'register' ? 'border-b-2 border-maroon text-maroon font-medium' : 'text-muted-foreground hover:text-foreground']">
              ثبت‌نام
            </button>
          </div>

          <!-- Error -->
          <div v-if="error" class="mb-5 flex items-center gap-2 border border-maroon/40 bg-maroon/5 px-4 py-3 text-sm text-maroon">
            <span class="text-maroon">⚠</span> {{ error }}
          </div>

          <!-- Login form -->
          <form v-if="tab === 'login'" @submit="submitLogin" class="space-y-5">
            <label class="block">
              <span class="text-xs uppercase tracking-widest text-muted-foreground">ایمیل</span>
              <input v-model="loginForm.email" required type="email" dir="ltr" placeholder="you@example.com"
                class="mt-2 w-full border border-border bg-background px-4 py-3 text-sm outline-none focus:border-maroon transition-colors" />
            </label>
            <label class="block">
              <div class="flex items-center justify-between">
                <span class="text-xs uppercase tracking-widest text-muted-foreground">رمز عبور</span>
              </div>
              <div class="relative mt-2">
                <input v-model="loginForm.password" required :type="showPass ? 'text' : 'password'" dir="ltr" placeholder="••••••••"
                  class="w-full border border-border bg-background px-4 py-3 text-sm outline-none focus:border-maroon transition-colors" />
                <button type="button" @click="showPass = !showPass" class="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors">
                  <EyeOff v-if="showPass" class="h-4 w-4" />
                  <Eye v-else class="h-4 w-4" />
                </button>
              </div>
            </label>
            <button type="submit" :disabled="loading"
              class="w-full bg-maroon py-3.5 text-sm text-white hover:opacity-90 disabled:opacity-60 flex items-center justify-center gap-2 transition-opacity">
              <Loader2 v-if="loading" class="h-4 w-4 animate-spin" />
              {{ loading ? "در حال ورود..." : "ورود به حساب" }}
            </button>
            <p class="text-center text-xs text-muted-foreground">
              حساب ندارید؟
              <button type="button" @click="tab = 'register'; error = ''" class="text-maroon hover:underline font-medium">ثبت‌نام کنید</button>
            </p>
          </form>

          <!-- Register form -->
          <form v-else @submit="submitRegister" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <label class="block col-span-2">
                <span class="text-xs uppercase tracking-widest text-muted-foreground">نام و نام خانوادگی</span>
                <input v-model="registerForm.name" required placeholder="علی محمدی"
                  class="mt-2 w-full border border-border bg-background px-4 py-3 text-sm outline-none focus:border-maroon transition-colors" />
              </label>
              <label class="block">
                <span class="text-xs uppercase tracking-widest text-muted-foreground">ایمیل</span>
                <input v-model="registerForm.email" required type="email" dir="ltr" placeholder="you@example.com"
                  class="mt-2 w-full border border-border bg-background px-4 py-3 text-sm outline-none focus:border-maroon transition-colors" />
              </label>
              <label class="block">
                <span class="text-xs uppercase tracking-widest text-muted-foreground">موبایل</span>
                <input v-model="registerForm.phone" required type="tel" dir="ltr" placeholder="۰۹۱۲..."
                  class="mt-2 w-full border border-border bg-background px-4 py-3 text-sm outline-none focus:border-maroon transition-colors" />
              </label>
            </div>
            <label class="block">
              <span class="text-xs uppercase tracking-widest text-muted-foreground">رمز عبور</span>
              <div class="relative mt-2">
                <input v-model="registerForm.password" required :type="showPass ? 'text' : 'password'" dir="ltr" placeholder="حداقل ۶ کاراکتر"
                  class="w-full border border-border bg-background px-4 py-3 text-sm outline-none focus:border-maroon transition-colors" />
                <button type="button" @click="showPass = !showPass" class="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground">
                  <EyeOff v-if="showPass" class="h-4 w-4" />
                  <Eye v-else class="h-4 w-4" />
                </button>
              </div>
            </label>
            <label class="block">
              <span class="text-xs uppercase tracking-widest text-muted-foreground">تکرار رمز عبور</span>
              <input v-model="registerForm.confirm" required :type="showPass ? 'text' : 'password'" dir="ltr" placeholder="••••••••"
                class="mt-2 w-full border border-border bg-background px-4 py-3 text-sm outline-none focus:border-maroon transition-colors" />
            </label>
            <button type="submit" :disabled="loading"
              class="w-full bg-maroon py-3.5 text-sm text-white hover:opacity-90 disabled:opacity-60 flex items-center justify-center gap-2 transition-opacity">
              <Loader2 v-if="loading" class="h-4 w-4 animate-spin" />
              {{ loading ? "در حال ثبت‌نام..." : "ایجاد حساب رایگان" }}
            </button>
            <p class="text-center text-xs text-muted-foreground">
              حساب دارید؟
              <button type="button" @click="tab = 'login'; error = ''" class="text-maroon hover:underline font-medium">وارد شوید</button>
            </p>
          </form>
        </div>
      </div>
    </div>
  </TheLayout>
</template>
