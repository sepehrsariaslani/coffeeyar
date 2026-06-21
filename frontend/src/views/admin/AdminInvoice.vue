<script setup>
import { ref, computed } from "vue";
import { Plus, Trash2, Printer, Search, X } from "lucide-vue-next";
import { useProductsStore } from "@/stores/products.js";
function formatPrice(n) { return n ? Number(n).toLocaleString("fa-IR") : "۰"; }
const productsStore = useProductsStore();

const customer = ref({ name: "", phone: "", address: "" });
const searchQ = ref("");
const lines = ref([]);
const discount = ref(0);
const note = ref("");
const invoiceRef = "NV-" + Math.random().toString(36).slice(2, 8).toUpperCase();
const today = new Date().toLocaleDateString("fa-IR");

const filtered = computed(() =>
  searchQ.value.trim()
    ? productsStore.products.filter((p) =>
        (p.name && p.name.includes(searchQ.value)) || (p.short_description && p.short_description.includes(searchQ.value))
      ).slice(0, 8)
    : []
);

function addProduct(p) {
  const existing = lines.value.find((l) => l.id === p.id);
  if (existing) { existing.qty++; }
  else { lines.value.push({ id: p.id, name: p.name, unitPrice: p.price, qty: 1 }); }
  searchQ.value = "";
}

function removeLine(idx) { lines.value.splice(idx, 1); }

const subtotal = computed(() => lines.value.reduce((s, l) => s + l.unitPrice * l.qty, 0));
const discountAmt = computed(() => Math.round(subtotal.value * (Number(discount.value) || 0) / 100));
const total = computed(() => subtotal.value - discountAmt.value);

function print() { window.print(); }
</script>

<template>
  <div class="p-4 md:p-8 max-w-2xl mx-auto">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-light">فاکتور سریع <span class="text-maroon">.</span></h1>
        <p class="mt-1 text-xs text-muted-foreground">شماره: {{ invoiceRef }} — {{ today }}</p>
      </div>
      <button
        @click="print"
        class="flex items-center gap-2 bg-maroon px-4 py-2.5 text-sm text-white hover:opacity-90 print:hidden"
      >
        <Printer class="h-4 w-4" />
        چاپ
      </button>
    </div>

    <!-- Customer Info -->
    <div class="mb-6 border border-border p-5">
      <h2 class="mb-4 text-xs uppercase tracking-widest text-maroon">اطلاعات مشتری</h2>
      <div class="grid gap-3 sm:grid-cols-2">
        <label class="block">
          <span class="text-xs text-muted-foreground">نام مشتری</span>
          <input v-model="customer.name" placeholder="علی محمدی"
            class="mt-1.5 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon print:border-0 print:p-0" />
        </label>
        <label class="block">
          <span class="text-xs text-muted-foreground">شماره موبایل</span>
          <input v-model="customer.phone" type="tel" dir="ltr" placeholder="09xx xxx xxxx"
            class="mt-1.5 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon print:border-0 print:p-0" />
        </label>
        <label class="block sm:col-span-2">
          <span class="text-xs text-muted-foreground">آدرس (اختیاری)</span>
          <input v-model="customer.address" placeholder="شهر، خیابان..."
            class="mt-1.5 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon print:border-0 print:p-0" />
        </label>
      </div>
    </div>

    <!-- Product Search -->
    <div class="mb-6 print:hidden">
      <div class="relative">
        <Search class="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <input
          v-model="searchQ"
          placeholder="جستجو برای افزودن محصول..."
          class="w-full border border-border bg-background py-3 pr-9 pl-4 text-sm outline-none focus:border-maroon"
        />
        <button v-if="searchQ" @click="searchQ = ''" class="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground">
          <X class="h-4 w-4" />
        </button>
      </div>
      <div v-if="filtered.length" class="border border-t-0 border-border bg-background shadow-sm">
        <button
          v-for="p in filtered"
          :key="p.id"
          @click="addProduct(p)"
          class="flex w-full items-center justify-between px-4 py-3 text-sm hover:bg-muted/50 text-right"
        >
          <span>{{ p.name }}</span>
          <span class="text-xs text-maroon">{{ formatPrice(p.price) }}</span>
        </button>
      </div>
    </div>

    <!-- Invoice Lines -->
    <div class="mb-6 border border-border">
      <div class="border-b border-border bg-muted/30 px-4 py-2.5 text-xs uppercase tracking-widest text-muted-foreground grid grid-cols-[1fr_80px_80px_32px] gap-2">
        <span>محصول</span><span class="text-center">تعداد</span><span class="text-center">مبلغ</span><span></span>
      </div>
      <div v-if="lines.length === 0" class="py-10 text-center text-sm text-muted-foreground">
        هنوز محصولی اضافه نشده است.
      </div>
      <div v-for="(l, idx) in lines" :key="idx" class="grid grid-cols-[1fr_80px_80px_32px] gap-2 items-center px-4 py-3 border-b last:border-0 border-border text-sm">
        <span class="leading-snug">{{ l.name }}</span>
        <div class="flex items-center justify-center gap-1">
          <button @click="l.qty > 1 ? l.qty-- : removeLine(idx)" class="h-6 w-6 border border-border flex items-center justify-center text-xs hover:border-maroon print:hidden">−</button>
          <span class="w-6 text-center">{{ l.qty }}</span>
          <button @click="l.qty++" class="h-6 w-6 border border-border flex items-center justify-center text-xs hover:border-maroon print:hidden">+</button>
        </div>
        <div class="text-center text-xs text-maroon">{{ formatPrice(l.unitPrice * l.qty) }}</div>
        <button @click="removeLine(idx)" class="text-muted-foreground hover:text-red-500 print:hidden flex justify-center">
          <Trash2 class="h-3.5 w-3.5" />
        </button>
      </div>
    </div>

    <!-- Totals -->
    <div class="border border-border p-5 mb-6">
      <div class="mb-3 flex items-center gap-3">
        <span class="text-xs text-muted-foreground">تخفیف (٪)</span>
        <input
          v-model="discount"
          type="number"
          min="0"
          max="100"
          dir="ltr"
          placeholder="0"
          class="w-20 border border-border bg-background px-2 py-1.5 text-sm outline-none focus:border-maroon print:hidden text-center"
        />
        <span class="text-xs text-muted-foreground print:inline hidden">{{ discount }}٪</span>
      </div>
      <dl class="space-y-2 text-sm">
        <div class="flex justify-between">
          <dt class="text-muted-foreground">جمع کالاها</dt>
          <dd>{{ formatPrice(subtotal) }}</dd>
        </div>
        <div v-if="discountAmt > 0" class="flex justify-between text-maroon">
          <dt>تخفیف ({{ discount }}٪)</dt>
          <dd>− {{ formatPrice(discountAmt) }}</dd>
        </div>
        <div class="flex justify-between border-t border-border pt-3 font-medium">
          <dt>قابل پرداخت</dt>
          <dd class="text-maroon text-lg font-light">{{ formatPrice(total) }}</dd>
        </div>
      </dl>
    </div>

    <!-- Note -->
    <div class="mb-6">
      <label class="block">
        <span class="text-xs uppercase tracking-widest text-muted-foreground">یادداشت (اختیاری)</span>
        <textarea v-model="note" rows="2" placeholder="توضیحات یا پیام برای مشتری..."
          class="mt-2 w-full border border-border bg-background px-3 py-2.5 text-sm outline-none focus:border-maroon resize-none print:border-0 print:p-0" />
      </label>
    </div>

    <!-- Print Footer -->
    <div class="hidden print:block border-t border-border pt-4 text-xs text-muted-foreground text-center">
      <p>نـوار — قهوه تخصصی</p>
      <p class="mt-1">فاکتور شماره {{ invoiceRef }} — تاریخ {{ today }}</p>
      <p v-if="note" class="mt-2">یادداشت: {{ note }}</p>
    </div>
  </div>
</template>

<style>
@media print {
  aside, header, .print\\:hidden { display: none !important; }
  body { font-size: 12px; }
}
</style>
