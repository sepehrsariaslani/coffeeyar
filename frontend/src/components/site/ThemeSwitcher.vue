<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRoute } from "vue-router";
import { Palette, X, RotateCcw, Lock, LockOpen } from "lucide-vue-next";
import {
  useLayoutStore,
  DESIGN_THEMES,
  ACCENT_COLORS,
  BUTTON_STYLES,
  PAGE_LIST,
  resolvePagePath,
} from "@/stores/layout.js";

const layoutStore = useLayoutStore();
const route = useRoute();
const open = ref(false);
const panelRef = ref(null);

const themes = Object.entries(DESIGN_THEMES).map(([key, val]) => ({ key, ...val }));
const currentPageKey = computed(() => resolvePagePath(route.path));

const currentPageLabel = computed(() => {
  const match = PAGE_LIST.find((p) => p.path === currentPageKey.value);
  return match ? match.label : null;
});

const isPageLocked = computed(() =>
  !!layoutStore.pageDesigns[currentPageKey.value]
);

const pageTheme = computed(() =>
  layoutStore.pageDesigns[currentPageKey.value] || layoutStore.themeName
);

function lockPage(themeKey) {
  layoutStore.setPageDesign(currentPageKey.value, themeKey);
}

function unlockPage() {
  layoutStore.setPageDesign(currentPageKey.value, null);
}

function toggle() { open.value = !open.value; }

function onClickOutside(e) {
  if (panelRef.value && !panelRef.value.contains(e.target)) {
    open.value = false;
  }
}
onMounted(() => window.addEventListener("mousedown", onClickOutside));
onUnmounted(() => window.removeEventListener("mousedown", onClickOutside));

function reset() {
  layoutStore.themeName   = "minimal";
  layoutStore.accentColor = "default";
  layoutStore.buttonStyle = "sharp";
}
</script>

<template>
  <div ref="panelRef" class="relative">
    <!-- Trigger -->
    <button
      type="button"
      @click="toggle"
      :title="'شخصی‌سازی ظاهر'"
      :class="[
        'relative flex h-8 w-8 items-center justify-center transition-colors',
        open ? 'text-maroon' : 'text-muted-foreground hover:text-maroon',
      ]"
    >
      <Palette class="h-4 w-4" />
      <!-- Dot when a page override is active -->
      <span
        v-if="isPageLocked"
        class="absolute top-1 right-1 h-1.5 w-1.5 rounded-full bg-maroon"
      />
    </button>

    <!-- Panel -->
    <Transition
      enter-active-class="transition-all duration-200"
      enter-from-class="opacity-0 translate-y-1 scale-95"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition-all duration-150"
      leave-from-class="opacity-100 translate-y-0 scale-100"
      leave-to-class="opacity-0 translate-y-1 scale-95"
    >
      <div
        v-if="open"
        class="absolute left-0 top-full z-[200] mt-3 w-72 border border-border bg-background shadow-xl"
        dir="rtl"
      >
        <!-- Header -->
        <div class="flex items-center justify-between border-b border-border px-4 py-3">
          <span class="text-[10px] uppercase tracking-[0.25em] text-maroon">شخصی‌سازی</span>
          <button type="button" @click="open = false" class="text-muted-foreground hover:text-foreground">
            <X class="h-3.5 w-3.5" />
          </button>
        </div>

        <div class="space-y-5 p-4">

          <!-- ── Design Theme (global) ── -->
          <section>
            <div class="mb-3 text-[10px] uppercase tracking-[0.2em] text-muted-foreground">تم طراحی</div>
            <div class="grid grid-cols-4 gap-2">
              <button
                v-for="t in themes"
                :key="t.key"
                type="button"
                @click="layoutStore.themeName = t.key"
                :title="t.label"
                :class="[
                  'flex flex-col items-center gap-1.5 p-1.5 transition-colors',
                  layoutStore.themeName === t.key
                    ? 'ring-2 ring-maroon ring-offset-1 ring-offset-background'
                    : 'hover:bg-accent',
                ]"
              >
                <div
                  class="relative h-9 w-full overflow-hidden border border-border"
                  :style="{ background: t.preview.bg }"
                >
                  <div class="absolute bottom-0 left-0 right-0 h-2.5" :style="{ background: t.preview.accent }" />
                  <div class="absolute right-1 top-1.5 h-1.5 w-5 opacity-70" :style="{ background: t.preview.text }" />
                  <div
                    v-if="layoutStore.themeName === t.key"
                    class="absolute inset-0 flex items-center justify-center bg-black/10"
                  >
                    <div class="flex h-4 w-4 items-center justify-center rounded-full bg-white/80">
                      <div class="h-1.5 w-1.5 rounded-full bg-maroon" />
                    </div>
                  </div>
                </div>
                <span class="text-[9px] leading-tight text-muted-foreground">{{ t.label }}</span>
              </button>
            </div>
          </section>

          <!-- ── Accent Color ── -->
          <section>
            <div class="mb-3 text-[10px] uppercase tracking-[0.2em] text-muted-foreground">رنگ تاکید</div>
            <div class="flex flex-wrap gap-1.5">
              <button
                v-for="a in ACCENT_COLORS"
                :key="a.id"
                type="button"
                @click="layoutStore.accentColor = a.id"
                :title="a.label"
                :class="[
                  'flex items-center gap-1.5 border px-2.5 py-1.5 text-[10px] transition-colors',
                  layoutStore.accentColor === a.id
                    ? 'border-foreground bg-foreground text-background'
                    : 'border-border hover:border-foreground',
                ]"
              >
                <span class="h-2.5 w-2.5 flex-shrink-0 rounded-full border border-white/30 shadow-sm" :style="{ background: a.color }" />
                {{ a.label }}
              </button>
            </div>
          </section>

          <!-- ── Button Shape ── -->
          <section>
            <div class="mb-3 text-[10px] uppercase tracking-[0.2em] text-muted-foreground">شکل دکمه</div>
            <div class="grid grid-cols-3 gap-2">
              <button
                v-for="s in BUTTON_STYLES"
                :key="s.id"
                type="button"
                @click="layoutStore.buttonStyle = s.id"
                :class="[
                  'flex flex-col items-center gap-2 border py-3 text-[10px] transition-colors',
                  layoutStore.buttonStyle === s.id
                    ? 'border-maroon bg-maroon text-maroon-foreground'
                    : 'border-border hover:border-maroon',
                ]"
              >
                <span
                  class="h-4 w-12 bg-current opacity-20"
                  :style="{
                    borderRadius:
                      s.id === 'pill' ? '9999px' :
                      s.id === 'rounded' ? '6px' : '0px',
                  }"
                />
                {{ s.label }}
              </button>
            </div>
          </section>

          <!-- ── Per-page Lock ── -->
          <section class="border-t border-border pt-4">
            <div class="mb-3 flex items-center justify-between">
              <div class="text-[10px] uppercase tracking-[0.2em] text-muted-foreground">تم این صفحه</div>
              <span
                v-if="currentPageLabel"
                class="rounded-full border border-border px-2 py-0.5 text-[9px] text-muted-foreground"
              >{{ currentPageLabel }}</span>
            </div>

            <!-- Locked state -->
            <div v-if="isPageLocked" class="space-y-3">
              <div class="flex items-center justify-between rounded-sm border border-maroon/30 bg-maroon/5 px-3 py-2">
                <div class="flex items-center gap-1.5">
                  <Lock class="h-3 w-3 text-maroon" />
                  <span class="text-[10px] text-maroon">
                    قفل شده روی «{{ DESIGN_THEMES[pageTheme]?.label }}»
                  </span>
                </div>
                <button
                  type="button"
                  @click="unlockPage"
                  class="text-[9px] text-muted-foreground hover:text-maroon transition-colors underline underline-offset-2"
                >رفع قفل</button>
              </div>
              <!-- Mini theme picker for this page -->
              <div class="grid grid-cols-4 gap-1.5">
                <button
                  v-for="t in themes"
                  :key="t.key"
                  type="button"
                  @click="lockPage(t.key)"
                  :title="t.label"
                  :class="[
                    'flex flex-col items-center gap-1 p-1 transition-colors',
                    pageTheme === t.key
                      ? 'ring-2 ring-maroon ring-offset-1 ring-offset-background'
                      : 'hover:bg-accent',
                  ]"
                >
                  <div
                    class="relative h-7 w-full overflow-hidden border border-border"
                    :style="{ background: t.preview.bg }"
                  >
                    <div class="absolute bottom-0 left-0 right-0 h-2" :style="{ background: t.preview.accent }" />
                    <div
                      v-if="pageTheme === t.key"
                      class="absolute inset-0 flex items-center justify-center bg-black/10"
                    >
                      <div class="h-1.5 w-1.5 rounded-full bg-maroon" />
                    </div>
                  </div>
                  <span class="text-[8px] leading-tight text-muted-foreground">{{ t.label }}</span>
                </button>
              </div>
            </div>

            <!-- Unlocked state -->
            <button
              v-else
              type="button"
              @click="lockPage(layoutStore.themeName)"
              class="flex w-full items-center justify-center gap-2 border border-dashed border-border py-2.5 text-[10px] text-muted-foreground hover:border-maroon hover:text-maroon transition-colors"
            >
              <LockOpen class="h-3 w-3" />
              قفل تم خاص برای این صفحه
            </button>
          </section>

          <!-- Reset global -->
          <button
            type="button"
            @click="reset"
            class="flex w-full items-center justify-center gap-1.5 border border-dashed border-border py-2 text-[10px] text-muted-foreground hover:border-foreground hover:text-foreground transition-colors"
          >
            <RotateCcw class="h-3 w-3" />
            بازگشت به پیش‌فرض
          </button>

        </div>
      </div>
    </Transition>
  </div>
</template>
