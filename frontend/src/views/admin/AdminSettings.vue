<script setup>
import { computed, ref, watch, toRaw } from "vue";
import { useThemeStore } from "@/stores/theme.js";
import { RotateCcw, Monitor, Smartphone, RefreshCw, Check } from "lucide-vue-next";

const store = useThemeStore();
const t = computed(() => store.theme);

/* ── Live preview iframe ── */
const iframeRef = ref(null);
const previewReady = ref(false);
const previewDevice = ref("desktop"); // "desktop" | "mobile"
const previewPage = ref("/");
const iframeKey = ref(0); // force reload when page switches

const pages = [
  { path: "/", label: "خانه" },
  { path: "/products", label: "محصولات" },
  { path: "/blog", label: "بلاگ" },
  { path: "/about", label: "درباره ما" },
];

function sendThemeToIframe(themeVal) {
  try {
    iframeRef.value?.contentWindow?.postMessage(
      { type: "navar-theme-preview", theme: toRaw(themeVal) },
      "*"
    );
  } catch {}
}

function onIframeLoad() {
  previewReady.value = true;
  // small delay so the iframe's Vue app fully mounts
  setTimeout(() => sendThemeToIframe(toRaw(store.theme)), 120);
}

function switchPage(path) {
  previewPage.value = path;
  previewReady.value = false;
  iframeKey.value++;
}

// Send theme on every change (debounced via rAF)
let rafId = null;
watch(
  () => store.theme,
  (val) => {
    if (rafId) cancelAnimationFrame(rafId);
    rafId = requestAnimationFrame(() => {
      sendThemeToIframe(toRaw(val));
    });
  },
  { deep: true }
);

/* ── Color presets ── */
const accentPresets = [
  { label: "مارون کلاسیک", accentHue: 22,  accentChroma: 0.09, accentLightness: 0.42 },
  { label: "قهوه‌ای گرم",  accentHue: 40,  accentChroma: 0.10, accentLightness: 0.40 },
  { label: "سبز زیتون",   accentHue: 120, accentChroma: 0.07, accentLightness: 0.38 },
  { label: "آبی نیلی",    accentHue: 230, accentChroma: 0.10, accentLightness: 0.40 },
  { label: "بنفش تیره",   accentHue: 280, accentChroma: 0.10, accentLightness: 0.38 },
  { label: "خاکستری تیره",accentHue: 0,   accentChroma: 0,    accentLightness: 0.35 },
];

const bgPresets = [
  { label: "کرم استخوانی", bgLightness: 0.982, bgChroma: 0.006, bgHue: 75  },
  { label: "سفید خالص",    bgLightness: 1.000, bgChroma: 0,     bgHue: 0   },
  { label: "کرم گرم",      bgLightness: 0.975, bgChroma: 0.010, bgHue: 70  },
  { label: "خاکستری روشن", bgLightness: 0.970, bgChroma: 0.002, bgHue: 240 },
  { label: "صورتی شیری",   bgLightness: 0.978, bgChroma: 0.008, bgHue: 10  },
  { label: "سبز شیری",     bgLightness: 0.978, bgChroma: 0.007, bgHue: 140 },
];

function applyAccentPreset(p) {
  store.theme.accentHue = p.accentHue;
  store.theme.accentChroma = p.accentChroma;
  store.theme.accentLightness = p.accentLightness;
}
function applyBgPreset(p) {
  store.theme.bgLightness = p.bgLightness;
  store.theme.bgChroma = p.bgChroma;
  store.theme.bgHue = p.bgHue;
}

const accentColor   = (p) => `oklch(${p.accentLightness} ${p.accentChroma} ${p.accentHue})`;
const bgColor       = (p) => `oklch(${p.bgLightness} ${p.bgChroma} ${p.bgHue})`;
const currentAccent = computed(() => accentColor(t.value));
const currentBg     = computed(() => bgColor(t.value));
const currentBorder = computed(() =>
  `oklch(${t.value.bgLightness - 0.1} ${t.value.bgChroma * 0.5} ${t.value.bgHue})`
);

/* Scale factor: we render the iframe at 1280px wide then scale it down */
const IFRAME_RENDER_W  = 1280;
const DESKTOP_PANEL_W  = 520; // px allocated for the preview column
const MOBILE_FRAME_W   = 390;
const MOBILE_FRAME_H   = 780;

const desktopScale = computed(() => DESKTOP_PANEL_W / IFRAME_RENDER_W);
const mobileScale  = computed(() => (DESKTOP_PANEL_W * 0.5) / MOBILE_FRAME_W);
</script>

<template>
  <div class="min-h-screen" dir="rtl">

    <!-- Page header -->
    <div class="border-b border-border bg-background px-6 py-5 md:px-10">
      <div class="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-light">تنظیمات ظاهری <span class="text-maroon">.</span></h1>
          <p class="mt-1 text-sm text-muted-foreground">رنگ‌های سایت را با پیش‌نمایش زنده شخصی‌سازی کنید</p>
        </div>
        <button
          type="button"
          @click="store.reset()"
          class="flex items-center gap-2 border border-border px-4 py-2 text-sm hover:bg-accent"
        >
          <RotateCcw class="h-3.5 w-3.5" /> بازگشت به پیش‌فرض
        </button>
      </div>
    </div>

    <!-- Two-column layout: controls + live preview -->
    <div class="flex flex-col lg:flex-row lg:items-start">

      <!-- ── Controls ── -->
      <div class="flex-1 min-w-0 space-y-6 p-6 md:p-10 lg:max-w-xl">

        <!-- ── Theme / Style Presets ── -->
        <section class="border border-border p-5">
          <h2 class="text-sm font-medium">پیش‌ساخته‌های تم</h2>
          <p class="mt-0.5 mb-4 text-xs text-muted-foreground">ظاهر کلی سایت را انتخاب کنید</p>
          <div class="grid grid-cols-2 gap-3 sm:grid-cols-4">

            <!-- Default -->
            <button
              type="button"
              @click="store.setThemeClass('')"
              :class="['relative flex flex-col overflow-hidden border-2 transition-all text-right', store.theme.themeClass === '' ? 'border-foreground' : 'border-border hover:border-foreground/40']"
            >
              <div class="h-16 w-full bg-[oklch(0.982_0.006_75)] flex flex-col gap-1 p-2">
                <div class="h-2 w-full rounded-sm bg-[oklch(0.876_0.009_75)]" />
                <div class="flex gap-1 mt-0.5">
                  <div class="h-6 w-5 bg-[oklch(0.876_0.009_75)]" />
                  <div class="flex-1 space-y-1">
                    <div class="h-1.5 rounded-sm bg-[oklch(0.876_0.009_75)] w-3/4" />
                    <div class="h-1.5 rounded-sm bg-[oklch(0.876_0.009_75)] w-1/2" />
                  </div>
                </div>
                <div class="h-3 w-2/3 rounded-none bg-[oklch(0.42_0.09_22)] mt-auto" />
              </div>
              <div class="p-2 bg-background flex items-center justify-between">
                <span class="text-[11px] font-medium">پیش‌فرض</span>
                <Check v-if="store.theme.themeClass === ''" class="h-3 w-3 text-maroon" />
              </div>
            </button>

            <!-- Dark -->
            <button
              type="button"
              @click="store.setThemeClass('dark')"
              :class="['relative flex flex-col overflow-hidden border-2 transition-all text-right', store.theme.themeClass === 'dark' ? 'border-foreground' : 'border-border hover:border-foreground/40']"
            >
              <div class="h-16 w-full bg-[oklch(0.12_0.005_60)] flex flex-col gap-1 p-2">
                <div class="h-2 w-full rounded-sm bg-[oklch(0.2_0.005_60)]" />
                <div class="flex gap-1 mt-0.5">
                  <div class="h-6 w-5 bg-[oklch(0.2_0.005_60)]" />
                  <div class="flex-1 space-y-1">
                    <div class="h-1.5 rounded-sm bg-[oklch(0.3_0.005_60)] w-3/4" />
                    <div class="h-1.5 rounded-sm bg-[oklch(0.25_0.005_60)] w-1/2" />
                  </div>
                </div>
                <div class="h-3 w-2/3 rounded-none bg-[oklch(0.62_0.1_40)] mt-auto" />
              </div>
              <div class="p-2 bg-background flex items-center justify-between">
                <span class="text-[11px] font-medium">تیره</span>
                <Check v-if="store.theme.themeClass === 'dark'" class="h-3 w-3 text-maroon" />
              </div>
            </button>

            <!-- Earthy -->
            <button
              type="button"
              @click="store.setThemeClass('theme-earthy')"
              :class="['relative flex flex-col overflow-hidden border-2 transition-all text-right', store.theme.themeClass === 'theme-earthy' ? 'border-foreground' : 'border-border hover:border-foreground/40']"
            >
              <div class="h-16 w-full bg-[oklch(0.972_0.009_100)] flex flex-col gap-1 p-2">
                <div class="h-2 w-full rounded-sm bg-[oklch(0.862_0.014_100)]" />
                <div class="flex gap-1 mt-0.5">
                  <div class="h-6 w-5 bg-[oklch(0.862_0.014_100)] rounded-sm" />
                  <div class="flex-1 space-y-1">
                    <div class="h-1.5 rounded bg-[oklch(0.862_0.014_100)] w-3/4" />
                    <div class="h-1.5 rounded bg-[oklch(0.862_0.014_100)] w-1/2" />
                  </div>
                </div>
                <div class="h-3 w-2/3 rounded bg-[oklch(0.42_0.13_145)] mt-auto" />
              </div>
              <div class="p-2 bg-background flex items-center justify-between">
                <span class="text-[11px] font-medium">طبیعی</span>
                <Check v-if="store.theme.themeClass === 'theme-earthy'" class="h-3 w-3 text-maroon" />
              </div>
            </button>

            <!-- Liquid Glass ✨ -->
            <button
              type="button"
              @click="store.setThemeClass('theme-glass')"
              :class="['relative flex flex-col overflow-hidden border-2 transition-all text-right', store.theme.themeClass === 'theme-glass' ? 'border-foreground' : 'border-border hover:border-foreground/40']"
            >
              <!-- Animated gradient preview -->
              <div class="h-16 w-full relative overflow-hidden" style="background: radial-gradient(ellipse 90% 70% at 15% 15%, oklch(0.72 0.18 280), transparent 60%), radial-gradient(ellipse 70% 70% at 88% 80%, oklch(0.7 0.20 340), transparent 55%), oklch(0.78 0.08 270);">
                <!-- Frosted card mockup -->
                <div class="absolute inset-x-2 top-1.5 bottom-4 rounded-lg overflow-hidden" style="background: rgba(255,255,255,0.4); backdrop-filter: blur(6px); border: 1px solid rgba(255,255,255,0.6);">
                  <div class="absolute inset-x-2 top-1 h-1 rounded-full bg-white/60" />
                  <div class="absolute inset-x-2 top-3 h-0.5 rounded-full bg-white/30" />
                  <div class="absolute inset-x-2 top-4.5 h-0.5 rounded-full bg-white/30" />
                  <div class="absolute left-2 right-8 bottom-1.5 h-2 rounded-full" style="background: oklch(0.48 0.2 278 / 0.8)" />
                </div>
              </div>
              <div class="p-2 bg-background flex items-center justify-between">
                <span class="text-[11px] font-medium">Liquid Glass</span>
                <Check v-if="store.theme.themeClass === 'theme-glass'" class="h-3 w-3 text-maroon" />
              </div>
            </button>

          </div>

          <!-- Glass mode active notice -->
          <Transition name="fade">
            <div v-if="store.theme.themeClass === 'theme-glass'" class="mt-4 flex items-start gap-2.5 rounded-lg p-3" style="background: rgba(255,255,255,0.4); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.6);">
              <span class="text-base leading-none mt-0.5">✦</span>
              <div>
                <p class="text-xs font-medium">Liquid Glass فعال است</p>
                <p class="text-[11px] text-muted-foreground mt-0.5">تمام سطح‌های سایت شیشه‌ای و نیمه‌شفاف می‌شوند. پس‌زمینه رنگارنگ از زیر شیشه دیده می‌شود.</p>
              </div>
            </div>
          </Transition>
        </section>

        <!-- Accent color -->
        <section class="border border-border p-5">
          <h2 class="text-sm font-medium">رنگ اکسنت (تأکید)</h2>
          <p class="mt-0.5 mb-4 text-xs text-muted-foreground">دکمه‌ها، لینک‌ها و المان‌های تأکیدی</p>

          <div class="grid grid-cols-3 gap-2 sm:grid-cols-6 mb-5">
            <button
              v-for="p in accentPresets"
              :key="p.label"
              type="button"
              @click="applyAccentPreset(p)"
              :title="p.label"
              :class="[
                'flex flex-col items-center gap-1.5 p-2.5 border transition-all',
                Math.round(store.theme.accentHue) === p.accentHue && Math.round(store.theme.accentChroma * 100) === Math.round(p.accentChroma * 100)
                  ? 'border-foreground shadow-sm'
                  : 'border-border hover:border-foreground/40',
              ]"
            >
              <span class="h-7 w-7 rounded-full border border-black/10 shadow-sm" :style="{ backgroundColor: accentColor(p) }" />
              <span class="text-[10px] text-center text-muted-foreground leading-tight">{{ p.label }}</span>
            </button>
          </div>

          <div class="space-y-3">
            <div class="grid grid-cols-[1fr_auto] items-center gap-3">
              <div>
                <div class="field-label mb-1">هیو — ۰ تا ۳۶۰</div>
                <input type="range" min="0" max="360" step="1"
                  v-model.number="t.accentHue"
                  class="w-full accent-[var(--maroon)] h-1.5 rounded cursor-pointer" />
              </div>
              <span class="w-9 text-center text-xs tabular-nums text-muted-foreground">{{ t.accentHue }}</span>
            </div>
            <div class="grid grid-cols-[1fr_auto] items-center gap-3">
              <div>
                <div class="field-label mb-1">کروما (شدت) — ۰ تا ۰.۲۵</div>
                <input type="range" min="0" max="0.25" step="0.005"
                  v-model.number="t.accentChroma"
                  class="w-full accent-[var(--maroon)] h-1.5 rounded cursor-pointer" />
              </div>
              <span class="w-9 text-center text-xs tabular-nums text-muted-foreground">{{ t.accentChroma.toFixed(2) }}</span>
            </div>
            <div class="grid grid-cols-[1fr_auto] items-center gap-3">
              <div>
                <div class="field-label mb-1">روشنایی — ۰.۲ تا ۰.۷</div>
                <input type="range" min="0.2" max="0.7" step="0.01"
                  v-model.number="t.accentLightness"
                  class="w-full accent-[var(--maroon)] h-1.5 rounded cursor-pointer" />
              </div>
              <span class="w-9 text-center text-xs tabular-nums text-muted-foreground">{{ t.accentLightness.toFixed(2) }}</span>
            </div>
          </div>

          <div class="mt-4 flex items-center gap-3">
            <span class="h-8 w-8 rounded-sm border border-black/10 shadow-sm" :style="{ backgroundColor: currentAccent }" />
            <span class="text-xs font-mono text-muted-foreground">{{ currentAccent }}</span>
          </div>
        </section>

        <!-- Background color -->
        <section class="border border-border p-5">
          <h2 class="text-sm font-medium">رنگ پس‌زمینه</h2>
          <p class="mt-0.5 mb-4 text-xs text-muted-foreground">پس‌زمینه کلی صفحات سایت</p>

          <div class="grid grid-cols-3 gap-2 sm:grid-cols-6 mb-5">
            <button
              v-for="p in bgPresets"
              :key="p.label"
              type="button"
              @click="applyBgPreset(p)"
              :title="p.label"
              :class="[
                'flex flex-col items-center gap-1.5 p-2.5 border transition-all',
                Math.round(store.theme.bgLightness * 1000) === Math.round(p.bgLightness * 1000)
                  ? 'border-foreground shadow-sm'
                  : 'border-border hover:border-foreground/40',
              ]"
            >
              <span class="h-7 w-7 rounded-full border border-black/20 shadow-sm" :style="{ backgroundColor: bgColor(p) }" />
              <span class="text-[10px] text-center text-muted-foreground leading-tight">{{ p.label }}</span>
            </button>
          </div>

          <div class="space-y-3">
            <div class="grid grid-cols-[1fr_auto] items-center gap-3">
              <div>
                <div class="field-label mb-1">روشنایی — ۰.۹۵ تا ۱</div>
                <input type="range" min="0.95" max="1.0" step="0.001"
                  v-model.number="t.bgLightness"
                  class="w-full accent-[var(--maroon)] h-1.5 rounded cursor-pointer" />
              </div>
              <span class="w-12 text-center text-xs tabular-nums text-muted-foreground">{{ t.bgLightness.toFixed(3) }}</span>
            </div>
            <div class="grid grid-cols-[1fr_auto] items-center gap-3">
              <div>
                <div class="field-label mb-1">کروما — ۰ تا ۰.۰۲</div>
                <input type="range" min="0" max="0.02" step="0.001"
                  v-model.number="t.bgChroma"
                  class="w-full accent-[var(--maroon)] h-1.5 rounded cursor-pointer" />
              </div>
              <span class="w-12 text-center text-xs tabular-nums text-muted-foreground">{{ t.bgChroma.toFixed(3) }}</span>
            </div>
            <div class="grid grid-cols-[1fr_auto] items-center gap-3">
              <div>
                <div class="field-label mb-1">هیو — ۰ تا ۳۶۰</div>
                <input type="range" min="0" max="360" step="1"
                  v-model.number="t.bgHue"
                  class="w-full accent-[var(--maroon)] h-1.5 rounded cursor-pointer" />
              </div>
              <span class="w-9 text-center text-xs tabular-nums text-muted-foreground">{{ t.bgHue }}</span>
            </div>
          </div>

          <div class="mt-4 flex items-center gap-3">
            <span class="h-8 w-8 rounded-sm border border-black/20 shadow-sm" :style="{ backgroundColor: currentBg }" />
            <span class="text-xs font-mono text-muted-foreground">{{ currentBg }}</span>
          </div>
        </section>

      </div>

      <!-- ── Live Preview Panel ── -->
      <div class="lg:sticky lg:top-0 lg:h-screen w-full lg:w-[560px] shrink-0 border-t border-border lg:border-t-0 lg:border-r bg-muted/40 flex flex-col">

        <!-- Preview toolbar -->
        <div class="flex items-center justify-between gap-3 border-b border-border px-4 py-3 bg-background">
          <div class="flex items-center gap-1">
            <span class="text-xs text-muted-foreground ml-2">صفحه:</span>
            <button
              v-for="pg in pages"
              :key="pg.path"
              type="button"
              @click="switchPage(pg.path)"
              :class="[
                'px-2.5 py-1 text-xs transition-colors rounded-sm',
                previewPage === pg.path ? 'bg-foreground text-background' : 'hover:bg-accent text-muted-foreground',
              ]"
            >
              {{ pg.label }}
            </button>
          </div>
          <div class="flex items-center gap-1 shrink-0">
            <button
              type="button"
              @click="previewDevice = 'desktop'"
              :class="['p-1.5 rounded-sm transition-colors', previewDevice === 'desktop' ? 'bg-foreground text-background' : 'hover:bg-accent text-muted-foreground']"
              title="دسکتاپ"
            >
              <Monitor class="h-3.5 w-3.5" />
            </button>
            <button
              type="button"
              @click="previewDevice = 'mobile'"
              :class="['p-1.5 rounded-sm transition-colors', previewDevice === 'mobile' ? 'bg-foreground text-background' : 'hover:bg-accent text-muted-foreground']"
              title="موبایل"
            >
              <Smartphone class="h-3.5 w-3.5" />
            </button>
            <button
              type="button"
              @click="() => { previewReady = false; iframeKey++ }"
              class="p-1.5 rounded-sm hover:bg-accent text-muted-foreground hover:text-foreground"
              title="بارگذاری مجدد"
            >
              <RefreshCw class="h-3.5 w-3.5" />
            </button>
          </div>
        </div>

        <!-- Preview frame area -->
        <div class="flex-1 overflow-hidden flex items-start justify-center py-6 px-4">

          <!-- Desktop mode: full-width scaled iframe -->
          <div v-if="previewDevice === 'desktop'" class="w-full">
            <!-- Browser chrome mockup -->
            <div class="border border-border rounded-t-md bg-muted overflow-hidden shadow-lg">
              <div class="flex items-center gap-1.5 px-3 py-2 border-b border-border bg-background">
                <span class="h-2.5 w-2.5 rounded-full bg-red-400/70" />
                <span class="h-2.5 w-2.5 rounded-full bg-yellow-400/70" />
                <span class="h-2.5 w-2.5 rounded-full bg-green-400/70" />
                <div class="mr-2 flex-1 rounded bg-muted px-3 py-0.5 text-[10px] text-muted-foreground text-center truncate">
                  نوار — فروشگاه قهوه
                </div>
              </div>
              <!-- Scaled iframe wrapper -->
              <div
                class="relative overflow-hidden"
                :style="{
                  height: `${Math.round(IFRAME_RENDER_W * 0.6 * desktopScale)}px`,
                }"
              >
                <div
                  :style="{
                    width: `${IFRAME_RENDER_W}px`,
                    height: `${Math.round(IFRAME_RENDER_W * 0.6)}px`,
                    transform: `scale(${desktopScale})`,
                    transformOrigin: 'top right',
                    position: 'absolute',
                    top: 0,
                    right: 0,
                  }"
                >
                  <iframe
                    :key="iframeKey"
                    ref="iframeRef"
                    :src="previewPage"
                    @load="onIframeLoad"
                    class="border-0 pointer-events-none select-none"
                    :style="{ width: `${IFRAME_RENDER_W}px`, height: `${Math.round(IFRAME_RENDER_W * 0.6)}px` }"
                    sandbox="allow-scripts allow-same-origin"
                    aria-hidden="true"
                  />
                </div>
                <!-- Loading overlay -->
                <Transition name="fade">
                  <div v-if="!previewReady" class="absolute inset-0 flex items-center justify-center bg-muted/80 backdrop-blur-sm z-10">
                    <div class="flex flex-col items-center gap-2 text-muted-foreground">
                      <RefreshCw class="h-5 w-5 animate-spin" />
                      <span class="text-xs">در حال بارگذاری...</span>
                    </div>
                  </div>
                </Transition>
              </div>
            </div>
          </div>

          <!-- Mobile mode: phone frame -->
          <div v-else class="flex justify-center">
            <!-- Phone mockup -->
            <div
              class="relative rounded-[2rem] border-[8px] border-foreground/80 bg-foreground/80 shadow-2xl overflow-hidden"
              :style="{ width: `${Math.round(MOBILE_FRAME_W * mobileScale)}px`, height: `${Math.round(MOBILE_FRAME_H * mobileScale)}px` }"
            >
              <!-- Notch -->
              <div class="absolute top-0 left-1/2 -translate-x-1/2 z-20 h-4 w-20 rounded-b-xl bg-foreground/80" />
              <!-- Iframe scaled into phone -->
              <div
                class="relative overflow-hidden rounded-[1.4rem] bg-background"
                :style="{ width: '100%', height: '100%' }"
              >
                <div
                  :style="{
                    width: `${MOBILE_FRAME_W}px`,
                    height: `${MOBILE_FRAME_H}px`,
                    transform: `scale(${mobileScale})`,
                    transformOrigin: 'top right',
                    position: 'absolute',
                    top: 0,
                    right: 0,
                  }"
                >
                  <iframe
                    :key="iframeKey + '-m'"
                    ref="iframeRef"
                    :src="previewPage"
                    @load="onIframeLoad"
                    class="border-0 pointer-events-none select-none"
                    :style="{ width: `${MOBILE_FRAME_W}px`, height: `${MOBILE_FRAME_H}px` }"
                    sandbox="allow-scripts allow-same-origin"
                    aria-hidden="true"
                  />
                </div>
                <!-- Loading overlay -->
                <Transition name="fade">
                  <div v-if="!previewReady" class="absolute inset-0 flex items-center justify-center bg-muted/80 backdrop-blur-sm z-10 rounded-[1.4rem]">
                    <RefreshCw class="h-4 w-4 animate-spin text-muted-foreground" />
                  </div>
                </Transition>
              </div>
            </div>
          </div>
        </div>

        <!-- Preview footer hint -->
        <div class="border-t border-border px-4 py-2.5 bg-background">
          <p class="text-xs text-muted-foreground text-center">
            پیش‌نمایش زنده — تغییرات فوری اعمال می‌شوند
          </p>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.field-label {
  display: block;
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  color: var(--color-muted-foreground);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
