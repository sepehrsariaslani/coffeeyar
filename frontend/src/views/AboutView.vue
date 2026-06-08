<script setup>
import { computed } from "vue";
import TheLayout from "@/components/site/TheLayout.vue";
import aboutImg from "@/assets/about.jpg";
import { useContentStore } from "@/stores/content.js";
import { useSeo } from "@/composables/useSeo.js";
import { Leaf, Flame, Truck, Award } from "lucide-vue-next";

useSeo({ title: "درباره ما — نوار", description: "داستان نوار، از منشأ دانه تا فنجان شما." });

const contentStore = useContentStore();
const ab = computed(() => contentStore.content.about);

const pillars = computed(() =>
  contentStore.content.about.values.length
    ? contentStore.content.about.values.map((v, i) => ({
        icon: [Leaf, Flame, Truck, Award][i % 4],
        n: String(i + 1).padStart(2, "۰"),
        title: v.title,
        desc: v.description,
      }))
    : []
);
</script>

<template>
  <TheLayout>

    <!-- ── Hero ─────────────────────────────────────── -->
    <section class="border-b border-border">
      <div class="mx-auto max-w-7xl px-6 py-20 md:py-32">
        <span class="text-xs uppercase tracking-[0.3em] text-maroon">{{ ab.heroTag }}</span>
        <h1 class="mt-4 max-w-3xl text-4xl font-light leading-tight md:text-6xl">
          {{ ab.heroTitle }}
        </h1>
        <div class="mt-10 grid grid-cols-3 gap-8 max-w-sm">
          <div v-for="s in ab.stats" :key="s.value" class="border-t-2 border-maroon pt-4">
            <div class="text-3xl font-light text-maroon">{{ s.value }}</div>
            <div class="mt-1.5 text-xs text-muted-foreground leading-snug">{{ s.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Story ─────────────────────────────────────── -->
    <section class="border-b border-border">
      <div class="mx-auto grid max-w-7xl gap-0 md:grid-cols-2">
        <div class="border-b md:border-b-0 md:border-l border-border overflow-hidden">
          <img :src="aboutImg" alt="دستان برشته‌کار" loading="lazy" class="w-full h-full object-cover min-h-72" />
        </div>
        <div class="flex flex-col justify-center px-8 md:px-14 py-16">
          <span class="text-xs uppercase tracking-[0.3em] text-maroon mb-4">داستان ما</span>
          <h2 class="text-3xl font-light">{{ ab.storyTitle }}</h2>
          <div class="mt-8 space-y-5 leading-8 text-muted-foreground">
            <p v-for="(para, i) in ab.storyParagraphs" :key="i">{{ para }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Pillars ───────────────────────────────────── -->
    <section class="border-b border-border">
      <div class="mx-auto max-w-7xl px-6 py-16">
        <div class="flex items-center gap-3 mb-10">
          <div class="h-px flex-1 bg-border" />
          <span class="text-xs uppercase tracking-[0.3em] text-maroon">چرا نوار؟</span>
          <div class="h-px flex-1 bg-border" />
        </div>
        <div class="grid gap-px bg-border sm:grid-cols-2 lg:grid-cols-4">
          <div v-for="p in pillars" :key="p.n" class="bg-background p-8 group hover:bg-maroon/3 transition-colors">
            <div class="flex items-start justify-between mb-5">
              <component :is="p.icon" class="h-5 w-5 text-maroon opacity-60 group-hover:opacity-100 transition-opacity" />
              <span class="text-[10px] text-muted-foreground/50 font-mono">{{ p.n }}</span>
            </div>
            <h3 class="text-base font-medium">{{ p.title }}</h3>
            <p class="mt-3 text-sm leading-7 text-muted-foreground">{{ p.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Timeline ──────────────────────────────────── -->
    <section class="border-b border-border bg-muted/20">
      <div class="mx-auto max-w-7xl px-6 py-16 md:py-24">
        <span class="text-xs uppercase tracking-[0.3em] text-maroon">تاریخچه</span>
        <h2 class="mt-4 text-3xl font-light md:text-4xl">مسیری که آمدیم</h2>
        <div class="relative mt-14">
          <div class="absolute right-[3.5rem] top-0 bottom-0 w-px bg-border md:right-1/2" />
          <div class="space-y-10">
            <div
              v-for="(event, i) in ab.timeline" :key="i"
              :class="['relative flex gap-8 md:gap-0', i % 2 === 0 ? 'md:flex-row' : 'md:flex-row-reverse']"
            >
              <div :class="['hidden md:flex md:w-1/2', i % 2 === 0 ? 'md:justify-end md:pl-16' : 'md:justify-start md:pr-16']">
                <div class="max-w-sm">
                  <div class="text-xs uppercase tracking-widest text-maroon">{{ event.year }}</div>
                  <h3 class="mt-2 text-xl font-light">{{ event.title }}</h3>
                  <p class="mt-3 text-sm leading-7 text-muted-foreground">{{ event.description }}</p>
                </div>
              </div>
              <div class="relative flex w-28 shrink-0 flex-col items-center md:w-0">
                <div class="relative z-10 flex h-8 w-8 items-center justify-center border-2 border-maroon bg-background shadow-sm">
                  <div class="h-2 w-2 bg-maroon" />
                </div>
                <div class="mt-2 text-xs font-medium text-maroon md:hidden">{{ event.year }}</div>
              </div>
              <div class="flex-1 pb-4 md:hidden">
                <h3 class="text-lg font-light">{{ event.title }}</h3>
                <p class="mt-2 text-sm leading-7 text-muted-foreground">{{ event.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Mission + Vision ──────────────────────────── -->
    <section class="border-b border-border">
      <div class="mx-auto max-w-7xl px-6 py-16 md:py-24">
        <div class="grid gap-0 md:grid-cols-2 md:divide-x md:divide-x-reverse divide-border">
          <div class="md:pl-16 pb-10 md:pb-0">
            <span class="text-xs uppercase tracking-[0.3em] text-maroon">ماموریت</span>
            <p class="mt-6 text-xl font-light leading-9">{{ ab.mission }}</p>
          </div>
          <div class="md:pr-16 pt-10 md:pt-0 border-t md:border-t-0 border-border">
            <span class="text-xs uppercase tracking-[0.3em] text-maroon">چشم‌انداز</span>
            <p class="mt-6 text-xl font-light leading-9">{{ ab.vision }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Values ────────────────────────────────────── -->
    <section class="border-b border-border">
      <div class="mx-auto max-w-7xl px-6 py-16 md:py-24">
        <span class="text-xs uppercase tracking-[0.3em] text-maroon">ارزش‌های کلیدی</span>
        <h2 class="mt-4 text-3xl font-light md:text-4xl">آنچه به آن اعتقاد داریم</h2>
        <div class="mt-12 grid gap-px bg-border md:grid-cols-2 lg:grid-cols-4">
          <div v-for="v in ab.values" :key="v.title" class="bg-background p-8">
            <div class="mb-4 h-0.5 w-10 bg-maroon" />
            <h3 class="text-lg font-light">{{ v.title }}</h3>
            <p class="mt-3 text-sm leading-7 text-muted-foreground">{{ v.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Manifesto ─────────────────────────────────── -->
    <section class="bg-foreground text-background">
      <div class="mx-auto max-w-4xl px-6 py-28 text-center">
        <div class="text-xs uppercase tracking-[0.4em] text-maroon mb-8">فلسفه‌ی ما</div>
        <p class="text-2xl font-light leading-relaxed md:text-4xl">
          "قهوه‌ی خوب از <span class="text-maroon">صبر</span> ساخته می‌شود،<br class="hidden md:block" /> نه از سرعت."
        </p>
      </div>
    </section>

  </TheLayout>
</template>
