import { createApp } from "vue";
import { createPinia } from "pinia";
import { router } from "./router/index.js";
import App from "./App.vue";
import "./styles.css";

const app = createApp(App);
const pinia = createPinia();
app.use(pinia);
app.use(router);

app.mount("#app");

import { useThemeStore } from "./stores/theme.js";
const themeStore = useThemeStore();
themeStore.theme;

import { useLayoutStore } from "./stores/layout.js";
useLayoutStore();

// Auto-detect active Frappe session (cookie-based) on startup
import { useAuthStore } from "./stores/auth.js";
const authStore = useAuthStore();
authStore.tryFrappeSession();
