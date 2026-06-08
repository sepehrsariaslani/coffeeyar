<script setup>
import { ref, computed } from "vue";
import TheLayout from "@/components/site/TheLayout.vue";
import { useSeo } from "@/composables/useSeo.js";
import { useContentStore } from "@/stores/content.js";
import { Mail, Phone, MapPin, Clock, Instagram, Send, MessageCircle, CheckCircle } from "lucide-vue-next";

useSeo({ title: "تماس با ما — نوار", description: "سؤال، همکاری یا فقط یک سلام." });

const contentStore = useContentStore();
const ct = computed(() => contentStore.content.contact);

const sent  = ref(false);
const form  = ref({ name: "", email: "", subject: "", message: "" });
const loading = ref(false);

function submit(e) {
  e.preventDefault();
  loading.value = true;
  setTimeout(() => { loading.value = false; sent.value = true; }, 900);
}

const contacts = computed(() => [
  { icon: Mail,    label: "ایمیل",    value: ct.value.email || "hello@navar.coffee", href: `mailto:${ct.value.email || "hello@navar.coffee"}` },
  { icon: Phone,   label: "تلفن",    value: ct.value.phone || "۰۲۱ ۸۸۸۸ ۸۸۸۸",      href: `tel:${(ct.value.phone || "").replace(/[^0-9]/g, "")}` },
  { icon: MapPin,  label: "نشانی",   value: ct.value.address || "تهران", href: "#" },
  { icon: Clock,   label: "ساعت کار", value: ct.value.workingHours || "شنبه–پنجشنبه، ۹–۱۸",  href: null },
]);

const socials = [
  { icon: Instagram, label: "اینستاگرام", href: "#" },
  { icon: Send,      label: "تلگرام",     href: "#" },
  { icon: MessageCircle, label: "واتساپ", href: "#" },
];

const subjects = ["سفارش", "همکاری", "نمایندگی", "بازخورد", "سایر"];
</script>

<template>
  <TheLayout>

    <!-- ── Hero ─────────────────────────────────────── -->
    <section class="border-b border-border bg-muted/20">
      <div class="mx-auto max-w-7xl px-6 py-20 md:py-28">
        <span class="text-xs uppercase tracking-[0.3em] text-maroon">{{ ct.heroTag || "ارتباط" }}</span>
        <h1 class="mt-4 text-4xl font-light md:text-6xl">{{ ct.heroTitle || "تماس با ما" }}</h1>
        <p class="mt-4 max-w-lg text-muted-foreground leading-7">
          خوشحال می‌شویم از شما بشنویم. سؤال، همکاری، نمایندگی یا فقط یک سلام.
        </p>
      </div>
    </section>

    <!-- ── Main Contact Section ──────────────────────── -->
    <section>
      <div class="mx-auto grid max-w-7xl gap-0 md:grid-cols-5">

        <!-- Left: Contact info -->
        <div class="md:col-span-2 border-b md:border-b-0 md:border-l border-border bg-muted/10 px-8 py-12 md:px-10 md:py-16">
          <h2 class="text-xl font-light mb-8">راه‌های ارتباطی</h2>
          <div class="space-y-7">
            <component
              v-for="c in contacts" :key="c.label"
              :is="c.href && c.href !== '#' ? 'a' : 'div'"
              :href="c.href && c.href !== '#' ? c.href : undefined"
              class="flex items-start gap-4 group"
              :class="c.href && c.href !== '#' ? 'hover:text-maroon transition-colors' : ''"
            >
              <div class="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center border border-border bg-background group-hover:border-maroon/40 group-hover:bg-maroon/5 transition-all">
                <component :is="c.icon" class="h-4 w-4 text-maroon" />
              </div>
              <div>
                <div class="text-[10px] uppercase tracking-widest text-muted-foreground">{{ c.label }}</div>
                <div class="mt-0.5 text-sm font-medium">{{ c.value }}</div>
              </div>
            </component>
          </div>

          <!-- Social links -->
          <div class="mt-12 pt-8 border-t border-border">
            <div class="text-xs uppercase tracking-widest text-muted-foreground mb-4">شبکه‌های اجتماعی</div>
            <div class="flex gap-3">
              <a
                v-for="s in socials" :key="s.label"
                :href="s.href"
                :title="s.label"
                class="flex h-9 w-9 items-center justify-center border border-border hover:border-maroon hover:bg-maroon/5 hover:text-maroon text-muted-foreground transition-all"
              >
                <component :is="s.icon" class="h-4 w-4" />
              </a>
            </div>
          </div>

          <!-- Map placeholder -->
          <div class="mt-10 border border-border bg-muted/30 overflow-hidden">
            <div class="h-36 bg-gradient-to-br from-muted to-muted/50 flex items-center justify-center">
              <div class="text-center">
                <MapPin class="h-6 w-6 text-maroon mx-auto mb-2" />
                <p class="text-xs text-muted-foreground">تهران، ولیعصر</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Right: Form -->
        <div class="md:col-span-3 px-8 py-12 md:px-14 md:py-16">

          <!-- Success state -->
          <Transition name="fade" mode="out-in">
            <div v-if="sent" class="flex flex-col items-center justify-center h-full text-center py-20">
              <CheckCircle class="h-12 w-12 text-maroon mb-5" />
              <h3 class="text-2xl font-light">پیام دریافت شد</h3>
              <p class="mt-3 text-muted-foreground max-w-sm leading-7">
                ممنون از تماس شما. تیم نوار ظرف ۲۴ ساعت پاسخ خواهد داد.
              </p>
              <button @click="sent = false; form = { name: '', email: '', subject: '', message: '' }" class="mt-8 border border-border px-6 py-2.5 text-sm hover:border-maroon hover:text-maroon transition-colors">
                ارسال پیام جدید
              </button>
            </div>

            <form v-else @submit="submit" class="space-y-7">
              <h2 class="text-xl font-light mb-8">ارسال پیام</h2>

              <!-- Subject tabs -->
              <div>
                <label class="text-[10px] uppercase tracking-widest text-muted-foreground block mb-3">موضوع</label>
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="s in subjects" :key="s" type="button"
                    @click="form.subject = s"
                    :class="['border px-4 py-1.5 text-xs transition-all', form.subject === s ? 'border-maroon bg-maroon/5 text-maroon' : 'border-border text-muted-foreground hover:border-maroon/40']"
                  >{{ s }}</button>
                </div>
              </div>

              <!-- Name + Email -->
              <div class="grid gap-6 sm:grid-cols-2">
                <div class="relative">
                  <input
                    v-model="form.name" required placeholder=" "
                    class="peer w-full border-b border-border bg-transparent pb-2.5 pt-5 text-sm outline-none focus:border-maroon transition-colors"
                  />
                  <label class="absolute top-0 right-0 text-[10px] uppercase tracking-widest text-muted-foreground peer-placeholder-shown:text-sm peer-placeholder-shown:top-3 peer-placeholder-shown:tracking-normal peer-focus:top-0 peer-focus:text-[10px] peer-focus:tracking-widest transition-all">نام</label>
                </div>
                <div class="relative">
                  <input
                    v-model="form.email" required type="email" placeholder=" "
                    class="peer w-full border-b border-border bg-transparent pb-2.5 pt-5 text-sm outline-none focus:border-maroon transition-colors"
                  />
                  <label class="absolute top-0 right-0 text-[10px] uppercase tracking-widest text-muted-foreground peer-placeholder-shown:text-sm peer-placeholder-shown:top-3 peer-placeholder-shown:tracking-normal peer-focus:top-0 peer-focus:text-[10px] peer-focus:tracking-widest transition-all">ایمیل</label>
                </div>
              </div>

              <!-- Message -->
              <div class="relative">
                <textarea
                  v-model="form.message" required rows="6" placeholder=" "
                  class="peer w-full resize-none border-b border-border bg-transparent pb-2.5 pt-5 text-sm outline-none focus:border-maroon transition-colors"
                />
                <label class="absolute top-0 right-0 text-[10px] uppercase tracking-widest text-muted-foreground peer-placeholder-shown:text-sm peer-placeholder-shown:top-3 peer-placeholder-shown:tracking-normal peer-focus:top-0 peer-focus:text-[10px] peer-focus:tracking-widest transition-all">پیام</label>
              </div>

              <div class="flex items-center gap-4 pt-2">
                <button
                  type="submit"
                  :disabled="loading"
                  class="flex items-center gap-2 bg-foreground px-8 py-3.5 text-sm text-background hover:opacity-80 disabled:opacity-50 transition-opacity"
                >
                  <Send class="h-3.5 w-3.5" :class="loading ? 'animate-spin' : ''" />
                  {{ loading ? 'در حال ارسال...' : 'ارسال پیام' }}
                </button>
                <p class="text-xs text-muted-foreground">پاسخ در کمتر از ۲۴ ساعت</p>
              </div>
            </form>
          </Transition>
        </div>

      </div>
    </section>

    <!-- ── FAQ teaser ────────────────────────────────── -->
    <section class="border-t border-border bg-muted/20">
      <div class="mx-auto max-w-7xl px-6 py-12 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <div class="text-xs uppercase tracking-widest text-maroon mb-1">سؤال دارید؟</div>
          <p class="text-sm text-muted-foreground">پرسش‌های متداول ما را بررسی کنید — شاید پاسخ‌تان آنجاست.</p>
        </div>
        <a href="/faq" class="shrink-0 border border-border px-6 py-2.5 text-sm hover:border-maroon hover:text-maroon transition-colors">
          سؤالات متداول
        </a>
      </div>
    </section>

  </TheLayout>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
