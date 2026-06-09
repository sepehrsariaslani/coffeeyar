import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";
import { resolve } from "path";

export default defineConfig({
  // آدرس پایه برای فراپه معمولا باید به این شکل باشد تا فایل‌ها از مسیر درست لود شوند
  base: process.env.VITE_BASE_URL || "/assets/coffeeyar/frontend/",
  
  plugins: [vue(), tailwindcss()],
  
  resolve: {
    alias: {
      "@": resolve(__dirname, "src"),
    },
  },

  // === این بخش اضافه شده است ===
  build: {
    // خروجی را مستقیم در پوشه public اپلیکیشن می‌ریزد
    outDir: resolve(__dirname, "../coffeeyar/public/frontend"),
    emptyOutDir: true, // فایل‌های بیلد قبلی را پاک می‌کند
  },
  // ==============================

  server: {
    host: "0.0.0.0",
    port: 5000,
    allowedHosts: true,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
