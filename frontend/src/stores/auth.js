import { defineStore } from "pinia";
import { ref, computed } from "vue";

const USERS_KEY = "navar_users_v1";
const SESSION_KEY = "navar_session_v1";

function loadUsers() {
  try { return JSON.parse(localStorage.getItem(USERS_KEY)) || []; } catch { return []; }
}
function saveUsers(u) { localStorage.setItem(USERS_KEY, JSON.stringify(u)); }
function loadSession() {
  try { return JSON.parse(localStorage.getItem(SESSION_KEY)) || null; } catch { return null; }
}
function saveSession(s) {
  if (s) localStorage.setItem(SESSION_KEY, JSON.stringify(s));
  else localStorage.removeItem(SESSION_KEY);
}

function hashSimple(str) {
  let h = 0;
  for (let i = 0; i < str.length; i++) h = Math.imul(31, h) + str.charCodeAt(i) | 0;
  return h.toString(16);
}

export const useAuthStore = defineStore("auth", () => {
  const users = ref(loadUsers());
  const session = ref(loadSession());

  const isLoggedIn = computed(() => !!session.value);
  const user = computed(() => session.value);

  function register({ name, email, phone, password }) {
    if (users.value.find((u) => u.email === email))
      return { ok: false, error: "این ایمیل قبلاً ثبت شده است" };
    const newUser = { id: Date.now().toString(), name, email, phone, passwordHash: hashSimple(password), createdAt: new Date().toLocaleDateString("fa-IR") };
    users.value.push(newUser);
    saveUsers(users.value);
    const { passwordHash: _, ...safeUser } = newUser;
    session.value = safeUser;
    saveSession(safeUser);
    return { ok: true };
  }

  function login({ email, password }) {
    const found = users.value.find((u) => u.email === email && u.passwordHash === hashSimple(password));
    if (!found) return { ok: false, error: "ایمیل یا رمز عبور اشتباه است" };
    const { passwordHash: _, ...safeUser } = found;
    session.value = safeUser;
    saveSession(safeUser);
    return { ok: true };
  }

  function logout() {
    session.value = null;
    saveSession(null);
  }

  function updateUser(patch) {
    if (!session.value) return;
    session.value = { ...session.value, ...patch };
    saveSession(session.value);
    users.value = users.value.map((u) => u.id === session.value.id ? { ...u, ...patch } : u);
    saveUsers(users.value);
  }

  return { isLoggedIn, user, register, login, logout, updateUser };
});
