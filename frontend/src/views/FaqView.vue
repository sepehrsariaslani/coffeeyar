<script setup>
import { ref, onMounted } from "vue";
import TheLayout from "@/components/site/TheLayout.vue";
import { useFaqStore } from "@/stores/faq.js";
import { useSeo } from "@/composables/useSeo.js";

useSeo({ title: "سوالات متداول — نوار", description: "پاسخ سوال‌های رایج درباره محصولات، ارسال و خدمات نوار" });

const faqStore = useFaqStore();
const expanded = ref(null);

function toggle(id) {
  expanded.value = expanded.value === id ? null : id;
}

onMounted(() => faqStore.fetchFaqs());
</script>

<template>
  <TheLayout>
    <section class="border-b border-border py-20 text-center">
      <div class="mb-3 text-xs uppercase tracking-widest text-maroon">پشتیبانی</div>
      <h1 class="text-4xl font-light md:text-5xl">سوالات متداول</h1>
      <p class="mx-auto mt-4 max-w-xl text-sm text-muted-foreground">پاسخ سوال‌های رایج درباره محصولات، ارسال و خدمات نوار</p>
    </section>

    <section class="mx-auto max-w-3xl px-6 py-16">
      <div v-if="faqStore.loading" class="py-12 text-center text-muted-foreground">در حال بارگذاری...</div>
      <div v-else-if="faqStore.faqs.length" class="divide-y divide-border border-y border-border">
        <div v-for="item in faqStore.faqs" :key="item.id">
          <button
            type="button"
            class="flex w-full items-center justify-between py-5 text-right transition-colors hover:text-maroon"
            @click="toggle(item.id)"
          >
            <span class="text-base font-medium">{{ item.question }}</span>
            <span class="mr-4 shrink-0 text-xl font-light text-muted-foreground transition-transform" :class="{ 'rotate-45': expanded === item.id }">+</span>
          </button>
          <div v-show="expanded === item.id" class="pb-5 text-sm leading-relaxed text-muted-foreground">
            {{ item.answer }}
          </div>
        </div>
      </div>
      <div v-else class="py-12 text-center text-muted-foreground">سوالی ثبت نشده است.</div>
    </section>

    <!-- CTA -->
    <section class="border-t border-border bg-muted/20 py-16 text-center">
      <h2 class="text-xl font-medium">سوالی داری که اینجا نیست؟</h2>
      <p class="mt-2 text-sm text-muted-foreground">با ما تماس بگیر، خوشحال می‌شیم کمک کنیم.</p>
      <a href="/contact" class="mt-6 inline-block border border-maroon px-8 py-3 text-sm text-maroon hover:bg-maroon hover:text-white transition-colors">
        تماس با ما
      </a>
    </section>
  </TheLayout>
</template>
