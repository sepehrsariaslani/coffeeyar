<script setup>
import { ref, computed } from "vue";
import { useContentStore } from "@/stores/content.js";
import { Plus, Trash2, GripVertical, ChevronDown, ChevronUp } from "lucide-vue-next";

const store = useContentStore();

if (!store.content.faq) {
  store.content.faq = {
    title: "سوالات متداول",
    subtitle: "پاسخ سوال‌های رایج درباره محصولات، ارسال و خدمات نوار",
    items: [
      { id: "1", q: "آیا قهوه‌ها تازه برشته شده هستند؟", a: "بله، تمام قهوه‌های نوار در دفعات کوچک و بعد از دریافت سفارش برشته می‌شوند. بسته‌بندی با گاز نیتروژن تازگی را تا ۶ ماه حفظ می‌کند." },
      { id: "2", q: "ارسال به کجاها انجام می‌شود؟", a: "ما به سراسر ایران ارسال می‌کنیم. ارسال از طریق پست پیشتاز و تیپاکس انجام می‌شود و معمولاً ۲ تا ۴ روز کاری طول می‌کشد." },
      { id: "3", q: "هزینه ارسال چقدر است؟", a: "برای سفارش‌های بالای ۵۰۰ هزار تومان ارسال رایگان است. برای سفارش‌های کمتر، هزینه ارسال بر اساس وزن و مقصد محاسبه می‌شود." },
      { id: "4", q: "آیا می‌توانم نوع آسیاب را انتخاب کنم؟", a: "بله، برای تمام قهوه‌های دانه می‌توانید نوع آسیاب خود را مشخص کنید: دانه کامل، اسپرسو، فرنچ پرس، V60 و موکاپات." },
      { id: "5", q: "سیاست بازگشت محصول چیست؟", a: "اگر از محصول رضایت ندارید تا ۷ روز بعد از دریافت می‌توانید با ما تماس بگیرید. در صورت عیب کارخانه‌ای، جایگزینی رایگان است." },
    ],
  };
  store.save();
}

const faq = computed(() => store.content.faq);
const expanded = ref(null);
const editItem = ref(null);

function addItem() {
  const item = { id: Date.now().toString(), q: "", a: "" };
  faq.value.items.push(item);
  editItem.value = item.id;
  store.save();
}

function removeItem(id) {
  if (confirm("این سوال حذف شود؟")) {
    faq.value.items = faq.value.items.filter((i) => i.id !== id);
    store.save();
  }
}

function moveUp(idx) {
  if (idx === 0) return;
  const arr = faq.value.items;
  [arr[idx - 1], arr[idx]] = [arr[idx], arr[idx - 1]];
  store.save();
}

function moveDown(idx) {
  const arr = faq.value.items;
  if (idx === arr.length - 1) return;
  [arr[idx], arr[idx + 1]] = [arr[idx + 1], arr[idx]];
  store.save();
}
</script>

<template>
  <div class="p-6 md:p-10">
    <div class="mb-8 flex flex-wrap items-end justify-between gap-4">
      <div>
        <h1 class="text-3xl font-light">سوالات متداول <span class="text-maroon">.</span></h1>
        <p class="mt-2 text-sm text-muted-foreground">سوالات و پاسخ‌های صفحه FAQ را مدیریت کنید</p>
      </div>
      <div class="flex gap-3">
        <a href="/faq" target="_blank" class="border border-border px-4 py-2.5 text-sm hover:bg-accent">مشاهده صفحه</a>
        <button type="button" @click="addItem" class="inline-flex items-center gap-2 bg-maroon px-5 py-2.5 text-sm text-maroon-foreground hover:opacity-90">
          <Plus class="h-4 w-4" /> سوال جدید
        </button>
      </div>
    </div>

    <!-- Page metadata -->
    <div class="mb-8 border border-border p-5 space-y-4">
      <div class="text-xs uppercase tracking-widest text-maroon mb-3">تنظیمات صفحه</div>
      <label class="block">
        <span class="field-label">عنوان صفحه</span>
        <input v-model="faq.title" @change="store.save()" class="mt-1.5 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon" />
      </label>
      <label class="block">
        <span class="field-label">توضیح زیر عنوان</span>
        <input v-model="faq.subtitle" @change="store.save()" class="mt-1.5 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon" />
      </label>
    </div>

    <!-- FAQ items -->
    <div class="space-y-2">
      <div v-for="(item, idx) in faq.items" :key="item.id" class="border border-border">
        <div
          class="flex cursor-pointer items-center justify-between p-4 hover:bg-accent/30"
          @click="expanded = expanded === item.id ? null : item.id; editItem = null"
        >
          <div class="flex items-center gap-3 min-w-0">
            <span class="text-xs text-muted-foreground w-5 shrink-0">{{ idx + 1 }}</span>
            <span class="text-sm font-medium truncate">{{ item.q || "سوال بدون عنوان" }}</span>
          </div>
          <div class="flex items-center gap-1 shrink-0 mr-2">
            <button type="button" @click.stop="moveUp(idx)" class="p-1.5 hover:bg-accent text-muted-foreground hover:text-foreground" title="بالاتر">
              <ChevronUp class="h-3.5 w-3.5" />
            </button>
            <button type="button" @click.stop="moveDown(idx)" class="p-1.5 hover:bg-accent text-muted-foreground hover:text-foreground" title="پایین‌تر">
              <ChevronDown class="h-3.5 w-3.5" />
            </button>
            <button
              type="button"
              @click.stop="editItem = editItem === item.id ? null : item.id; expanded = item.id"
              :class="['px-3 py-1.5 text-xs', editItem === item.id ? 'bg-maroon text-maroon-foreground' : 'border border-border hover:bg-accent']"
            >
              {{ editItem === item.id ? "در حال ویرایش" : "ویرایش" }}
            </button>
            <button type="button" @click.stop="removeItem(item.id)" class="p-1.5 hover:bg-accent text-maroon">
              <Trash2 class="h-3.5 w-3.5" />
            </button>
          </div>
        </div>

        <!-- Edit mode -->
        <div v-if="editItem === item.id" class="border-t border-border bg-muted/20 p-5 space-y-4">
          <label class="block">
            <span class="field-label">سوال</span>
            <input v-model="item.q" @input="store.save()" placeholder="سوال را اینجا بنویسید..." class="mt-1.5 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon" />
          </label>
          <label class="block">
            <span class="field-label">پاسخ</span>
            <textarea v-model="item.a" @input="store.save()" rows="5" placeholder="پاسخ کامل را اینجا بنویسید..." class="mt-1.5 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon resize-none" />
          </label>
        </div>

        <!-- Preview mode -->
        <div v-else-if="expanded === item.id" class="border-t border-border bg-muted/20 p-5">
          <p class="text-sm text-muted-foreground leading-relaxed">{{ item.a || "پاسخی وارد نشده." }}</p>
        </div>
      </div>

      <div v-if="faq.items.length === 0" class="border border-dashed border-border p-16 text-center text-muted-foreground text-sm">
        سوالی اضافه نشده. با کلیک «سوال جدید» شروع کنید.
      </div>
    </div>
  </div>
</template>

<style scoped>
.field-label {
  display: block;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--muted-foreground);
}
</style>
