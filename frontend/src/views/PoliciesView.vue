<script setup>
import { ref, computed } from "vue";
import { usePoliciesStore } from "@/stores/policies.js";
import { useSeo } from "@/composables/useSeo.js";
import TheLayout from "@/components/site/TheLayout.vue";

useSeo({ title: "قوانین و مقررات", description: "شرایط استفاده، قوانین بازگشت کالا، حریم خصوصی و شرایط ارسال فروشگاه." });

const store = usePoliciesStore();
const activeTab = ref("terms");

const tabs = [
  { key: "terms",    icon: "📋" },
  { key: "return",   icon: "↩️" },
  { key: "privacy",  icon: "🔒" },
  { key: "shipping", icon: "📦" },
];

const active = computed(() => store.policies?.[activeTab.value]);

function renderContent(text) {
  return text
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\n\n/g, "</p><p class='mt-4'>")
    .replace(/\n/g, "<br/>");
}
</script>

<template>
  <TheLayout>
    <div dir="rtl" class="min-h-screen font-[Vazirmatn]">

      <!-- Header -->
      <section class="border-b border-border">
        <div class="mx-auto max-w-7xl px-6 py-14">
          <span class="text-xs uppercase tracking-[0.3em] text-maroon">حقوقی</span>
          <h1 class="mt-3 text-4xl font-light">قوانین و مقررات</h1>
          <p class="mt-3 max-w-xl text-muted-foreground text-sm leading-7">
            استفاده از خدمات ما به منزله‌ی پذیرش شرایط زیر است. لطفاً قبل از خرید این قوانین را مطالعه کنید.
          </p>
        </div>
      </section>

      <div class="mx-auto max-w-7xl px-6 py-12 grid gap-10 lg:grid-cols-[280px_1fr]">

        <!-- Sidebar tabs -->
        <nav class="space-y-1 self-start lg:sticky lg:top-6">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            @click="activeTab = tab.key"
            :class="[
              'w-full flex items-center gap-3 px-4 py-3 text-sm text-right transition-colors',
              activeTab === tab.key
                ? 'border border-maroon bg-maroon/5 text-maroon font-medium'
                : 'border border-transparent hover:border-border hover:bg-accent text-foreground'
            ]"
          >
            <span class="text-base">{{ tab.icon }}</span>
            <span>{{ store.policies[tab.key]?.title }}</span>
          </button>
        </nav>

        <!-- Content panel -->
        <article class="border border-border p-8 lg:p-10">
          <h2 class="text-2xl font-light mb-6 text-foreground">{{ active?.title }}</h2>
          <div class="prose-like">
            <p v-html="renderContent(active?.content || '')" class="text-sm leading-8 text-foreground/80" />
          </div>
          <div class="mt-10 border-t border-border pt-6 flex items-center justify-between text-xs text-muted-foreground">
            <span>آخرین بروزرسانی: {{ new Date().toLocaleDateString('fa-IR') }}</span>
            <RouterLink to="/contact" class="hover:text-maroon transition-colors">سوال دارید؟ تماس بگیرید ←</RouterLink>
          </div>
        </article>

      </div>
    </div>
  </TheLayout>
</template>
