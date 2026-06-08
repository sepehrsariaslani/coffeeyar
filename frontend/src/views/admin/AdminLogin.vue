<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth.js";
import { Eye, EyeOff, Loader2, Lock, ShieldCheck } from "lucide-vue-next";
import CoffeeLoader from "@/components/CoffeeLoader.vue";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const form = ref({ email: "", password: "" });
const showPass = ref(false);
const loading = ref(false);
const error = ref("");

// If an admin is already logged in, skip straight to the panel.
onMounted(() => {
  if (authStore.isLoggedIn && authStore.isAdmin) {
    router.replace(route.query.redirect || "/admin");
  }
});

/**
 * Authenticate the admin. Only users with the System Manager role
 * (is_admin) are allowed past this gate — regular customers are rejected.
 * @param {Event} e Submit event.
 * @returns {Promise<void>}
 */
async function submit(e) {
  e.preventDefault();
  error.value = "";
  loading.value = true;
  const result = await authStore.login(form.value);
  if (!result.ok) {
    error.value = result.error || "ایمیل یا رمز عبور نادرست است";
    loading.value = false;
    return;
  }
  if (!authStore.isAdmin) {
    error.value = "این حساب کاربری دسترسی مدیریت ندارد.";
    authStore.logout();
    loading.value = false;
    return;
  }
  loading.value = false;
  router.replace(route.query.redirect || "/admin");
}
</script>

<template>
  <div class="admin-login">
    <div class="admin-login__card">
      <div class="admin-login__brand">
        <div class="admin-login__logo">
          <ShieldCheck class="admin-login__logo-icon" />
        </div>
        <h1 class="admin-login__title">ورود به پنل مدیریت</h1>
        <p class="admin-login__sub">برای دسترسی به بخش مدیریت، وارد شوید</p>
      </div>

      <div v-if="error" class="admin-login__error">
        <span>⚠</span> {{ error }}
      </div>

      <form @submit="submit" class="admin-login__form">
        <label class="admin-login__field">
          <span class="admin-login__label">ایمیل مدیر</span>
          <input
            v-model="form.email"
            required
            type="email"
            dir="ltr"
            placeholder="admin@example.com"
            class="admin-login__input"
            autocomplete="username"
          />
        </label>

        <label class="admin-login__field">
          <span class="admin-login__label">رمز عبور</span>
          <div class="admin-login__pass">
            <input
              v-model="form.password"
              required
              :type="showPass ? 'text' : 'password'"
              dir="ltr"
              placeholder="••••••••"
              class="admin-login__input"
              autocomplete="current-password"
            />
            <button type="button" class="admin-login__eye" @click="showPass = !showPass">
              <EyeOff v-if="showPass" class="admin-login__eye-icon" />
              <Eye v-else class="admin-login__eye-icon" />
            </button>
          </div>
        </label>

        <button type="submit" :disabled="loading" class="admin-login__submit">
          <Loader2 v-if="loading" class="admin-login__spin" />
          <Lock v-else class="admin-login__submit-icon" />
          {{ loading ? "در حال ورود..." : "ورود به پنل" }}
        </button>
      </form>

      <div v-if="loading" class="admin-login__loader">
        <CoffeeLoader size="sm" text="در حال احراز هویت..." />
      </div>

      <p class="admin-login__footer">
        دسترسی فقط برای مدیران سیستم — ورود مشتریان از
        <RouterLink to="/auth" class="admin-login__link">این صفحه</RouterLink>
      </p>
    </div>
  </div>
</template>

<style scoped>
.admin-login {
  min-height: 100dvh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  background:
    radial-gradient(ellipse 70% 50% at 50% 0%, rgba(128, 0, 0, 0.14), transparent 60%),
    linear-gradient(135deg, #1a1a1a 0%, #2d2a28 100%);
  font-family: "Vazirmatn", Tahoma, sans-serif;
}
.admin-login__card {
  width: 100%;
  max-width: 400px;
  background: #fff;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 2.5rem 2rem;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.45);
}
.admin-login__brand {
  text-align: center;
  margin-bottom: 2rem;
}
.admin-login__logo {
  width: 56px;
  height: 56px;
  margin: 0 auto 1rem;
  border-radius: 14px;
  background: linear-gradient(135deg, #800000, #a52a2a);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(128, 0, 0, 0.35);
}
.admin-login__logo-icon { width: 28px; height: 28px; color: #fff; }
.admin-login__title { font-size: 1.3rem; font-weight: 600; color: #1a1a1a; margin: 0; }
.admin-login__sub { font-size: 0.82rem; color: #8a8480; margin: 0.4rem 0 0; }
.admin-login__error {
  display: flex; align-items: center; gap: 0.5rem;
  background: #fef2f2; border: 1px solid #fecaca; color: #991b1b;
  font-size: 0.82rem; padding: 0.7rem 0.9rem; border-radius: 8px; margin-bottom: 1.25rem;
}
.admin-login__form { display: flex; flex-direction: column; gap: 1.1rem; }
.admin-login__field { display: flex; flex-direction: column; gap: 0.45rem; }
.admin-login__label { font-size: 0.72rem; letter-spacing: 0.05em; color: #8a8480; }
.admin-login__pass { position: relative; }
.admin-login__input {
  width: 100%;
  border: 1px solid #e5e1db;
  background: #faf9f7;
  border-radius: 8px;
  padding: 0.7rem 0.9rem;
  font-size: 0.9rem;
  color: #1a1a1a;
  outline: none;
  transition: border-color 0.2s, background 0.2s;
  box-sizing: border-box;
  font-family: inherit;
}
.admin-login__input:focus { border-color: #800000; background: #fff; }
.admin-login__eye {
  position: absolute; left: 0.7rem; top: 50%; transform: translateY(-50%);
  background: none; border: none; cursor: pointer; color: #b0a99f; padding: 0; display: flex;
}
.admin-login__eye:hover { color: #1a1a1a; }
.admin-login__eye-icon { width: 17px; height: 17px; }
.admin-login__submit {
  display: flex; align-items: center; justify-content: center; gap: 0.5rem;
  margin-top: 0.4rem;
  padding: 0.8rem;
  background: linear-gradient(135deg, #800000, #a52a2a);
  color: #fff; font-size: 0.9rem; font-weight: 500;
  border: none; border-radius: 8px; cursor: pointer;
  transition: opacity 0.2s, transform 0.1s;
  font-family: inherit;
}
.admin-login__submit:hover:not(:disabled) { opacity: 0.92; }
.admin-login__submit:active:not(:disabled) { transform: scale(0.99); }
.admin-login__submit:disabled { opacity: 0.6; cursor: default; }
.admin-login__submit-icon { width: 16px; height: 16px; }
.admin-login__spin { width: 16px; height: 16px; animation: adminspin 0.8s linear infinite; }
@keyframes adminspin { to { transform: rotate(360deg); } }
.admin-login__loader { display: flex; justify-content: center; margin-top: 1.25rem; }
.admin-login__footer { text-align: center; font-size: 0.74rem; color: #b0a99f; margin: 1.5rem 0 0; }
.admin-login__link { color: #800000; text-decoration: none; }
.admin-login__link:hover { text-decoration: underline; }
</style>
