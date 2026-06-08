import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { api } from "@/lib/api.js";

const SESSION_KEY = "navar_session_v1";

function loadSession() {
  try { return JSON.parse(localStorage.getItem(SESSION_KEY)) || null; } catch { return null; }
}
function saveSession(s) {
  if (s) localStorage.setItem(SESSION_KEY, JSON.stringify(s));
  else localStorage.removeItem(SESSION_KEY);
}

export const useAuthStore = defineStore("auth", () => {
  const session = ref(loadSession());
  const loading = ref(false);
  const error = ref("");

  const isLoggedIn = computed(() => !!session.value);
  const user = computed(() => session.value);
  const isAdmin = computed(() => !!session.value?.is_admin);

  async function register({ name, email, phone, password }) {
    loading.value = true;
    error.value = "";
    try {
      const res = await api.auth.register({ name, email, phone, password });
      session.value = res.user;
      saveSession(res.user);
      return { ok: true };
    } catch (e) {
      error.value = e.message;
      return { ok: false, error: e.message };
    } finally {
      loading.value = false;
    }
  }

  async function login({ email, password }) {
    loading.value = true;
    error.value = "";
    try {
      const res = await api.auth.login({ email, password });
      session.value = res.user;
      saveSession(res.user);
      return { ok: true };
    } catch (e) {
      error.value = e.message;
      return { ok: false, error: e.message };
    } finally {
      loading.value = false;
    }
  }

  function logout() {
    api.auth.logout();
    session.value = null;
    saveSession(null);
  }

  async function updateUser(patch) {
    if (!session.value) return;
    try {
      const updated = await api.auth.updateMe(patch);
      session.value = { ...session.value, ...updated };
      saveSession(session.value);
      return { ok: true };
    } catch (e) {
      return { ok: false, error: e.message };
    }
  }

  async function fetchMe() {
    if (!api.getToken()) return;
    try {
      const u = await api.auth.me();
      session.value = { ...session.value, ...u };
      saveSession(session.value);
    } catch {
      logout();
    }
  }

  return { isLoggedIn, user, isAdmin, loading, error, register, login, logout, updateUser, fetchMe };
});
