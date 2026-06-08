<script setup>
import { ref } from "vue";
import { usePoliciesStore } from "@/stores/policies.js";
import { Save, Check, ExternalLink } from "lucide-vue-next";

const store = usePoliciesStore();
const saved = ref(false);
const activeTab = ref("terms");

const tabs = [
  { key: "terms",    label: "شرایط استفاده",    icon: "📋" },
  { key: "return",   label: "بازگشت کالا",       icon: "↩️" },
  { key: "privacy",  label: "حریم خصوصی",        icon: "🔒" },
  { key: "shipping", label: "شرایط ارسال",        icon: "📦" },
];

function saveAll() {
  store.save();
  saved.value = true;
  setTimeout(() => (saved.value = false), 2000);
}
</script>

<template>
  <div class="p-4 md:p-10 max-w-5xl" dir="rtl">
    <div class="mb-8 flex flex-wrap items-end justify-between gap-4">
      <div>
        <h1 class="text-3xl font-light">قوانین سایت <span class="text-maroon">.</span></h1>
        <p class="mt-2 text-sm text-muted-foreground">متن قوانین، مقررات و سیاست‌های فروشگاه را ویرایش کنید</p>
      </div>
      <div class="flex items-center gap-3">
        <a href="/policies" target="_blank" class="flex items-center gap-1.5 border border-border px-4 py-2.5 text-sm hover:bg-accent">
          <ExternalLink class="h-3.5 w-3.5" />
          مشاهده در سایت
        </a>
        <button
          @click="saveAll"
          :class="['flex items-center gap-2 px-5 py-2.5 text-sm transition-colors', saved ? 'bg-green-600 text-white' : 'bg-maroon text-maroon-foreground hover:opacity-90']"
        >
          <Check v-if="saved" class="h-4 w-4" />
          <Save v-else class="h-4 w-4" />
          {{ saved ? "ذخیره شد" : "ذخیره تغییرات" }}
        </button>
      </div>
    </div>

    <!-- Tabs -->
    <div class="flex gap-1 border-b border-border mb-6">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="activeTab = tab.key"
        :class="[
          'flex items-center gap-2 px-4 py-2.5 text-sm transition-colors border-b-2 -mb-px',
          activeTab === tab.key
            ? 'border-maroon text-maroon font-medium'
            : 'border-transparent text-muted-foreground hover:text-foreground'
        ]"
      >
        <span>{{ tab.icon }}</span>
        {{ tab.label }}
      </button>
    </div>

    <!-- Editor -->
    <div v-for="tab in tabs" :key="tab.key" v-show="activeTab === tab.key" class="space-y-4">
      <div class="border border-border p-6 space-y-4">
        <label class="block">
          <span class="block text-xs uppercase tracking-widest text-muted-foreground mb-2">عنوان بخش</span>
          <input
            v-model="store.policies[tab.key].title"
            @input="store.save()"
            class="w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon"
          />
        </label>

        <label class="block">
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs uppercase tracking-widest text-muted-foreground">متن قوانین</span>
            <span class="text-xs text-muted-foreground">از **متن** برای bold استفاده کنید</span>
          </div>
          <textarea
            v-model="store.policies[tab.key].content"
            @input="store.save()"
            rows="18"
            class="w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon resize-y font-[Vazirmatn] leading-7"
          />
        </label>
      </div>

      <div class="border border-border p-5 bg-muted/20">
        <div class="text-xs uppercase tracking-widest text-muted-foreground mb-3">پیش‌نمایش</div>
        <div class="text-sm leading-8 text-foreground/80"
          v-html="store.policies[tab.key].content
            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n\n/g, '</p><p class=\'mt-3\'>')
            .replace(/\n/g, '<br/>')"
        />
      </div>
    </div>
  </div>
</template>
