<script setup>
import { ref, computed } from "vue";
import { useContentStore } from "@/stores/content.js";
import TheLayout from "@/components/site/TheLayout.vue";

const store = useContentStore();

const faq = computed(() => store.content.faq || {
  title: "سوالات متداول",
  subtitle: "پاسخ سوال‌های رایج درباره محصولات، ارسال و خدمات نوار",
  items: [],
});

const expanded = ref(null);

function toggle(id) {
  expanded.value = expanded.value === id ? null : id;
}
</script>

<template>
  <TheLayout>
    <!-- Hero -->
    <section class="border-b border-border py-20 text-center">
      <div class="mb-3 text-xs uppercase tracking-widest text-maroon">پشتیبانی</div>
      <h1 class="text-4xl font-light md:text-5xl">{{ faq.title }}</h1>
      <p class="mx-auto mt-4 max-w-xl text-sm text-muted-foreground">{{ faq.subtitle }}</p>
    </section>

    <!-- FAQ list -->
    <section class="mx-auto max-w-3xl px-6 py-16">
      <div v-if="faq.items && faq.items.length" class="divide-y divide-border border-y border-border">
        <div v-for="(item, idx) in faq.items" :key="item.id || idx">
          <button
            type="button"
            class="flex w-full items-center justify-between py-5 text-right transition-colors hover:text-maroon"
            @click="toggle(item.id || idx)"
          >
            <span class="text-base font-medium">{{ item.q }}</span>
            <span class="mr-4 shrink-0 text-xl font-light text-muted-foreground transition-transform" :class="{ 'rotate-45': expanded === (item.id || idx) }">+</span>
          </button>
          <div
            v-show="expanded === (item.id || idx)"
            class="pb-5 text-sm leading-relaxed text-muted-foreground"
          >
            {{ item.a }}
          </div>
        </div>
      </div>

      <div v-else class="py-20 text-center text-muted-foreground">
        هنوز سوالی اضافه نشده است.
      </div>

      <!-- CTA -->
      <div class="mt-16 border border-border p-8 text-center">
        <div class="text-xs uppercase tracking-widest text-maroon mb-3">هنوز سوال داری؟</div>
        <h2 class="text-2xl font-light mb-2">با ما تماس بگیر</h2>
        <p class="text-sm text-muted-foreground mb-5">تیم پشتیبانی نوار در ساعات کاری پاسخگوی تمام سوال‌های شماست.</p>
        <RouterLink to="/contact" class="inline-flex items-center gap-2 bg-foreground px-6 py-3 text-sm text-background hover:opacity-80">
          صفحه تماس ←
        </RouterLink>
      </div>
    </section>
  </TheLayout>
</template>
