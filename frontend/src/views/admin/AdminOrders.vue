<script setup>
import { ref, computed, watch } from "vue";
import { formatPrice } from "@/lib/data.js";
import { Check, Pencil, X, Printer, BarChart2 } from "lucide-vue-next";
import ViewSwitcher from "@/components/admin/ViewSwitcher.vue";

const orders = ref([
  {
    id: "۱۰۲۴",
    customer: "علی محمدی",
    phone: "۰۹۱۲۱۲۳۴۵۶۷",
    address: "تهران، خیابان ولیعصر، پلاک ۱۲",
    total: 960000,
    status: "در حال آماده‌سازی",
    date: "۱۴۰۳/۰۳/۰۴",
    payMethod: "آنلاین",
    items: [
      { name: "اتیوپی یرگاچف", qty: 1, price: 480000 },
      { name: "کلمبیا هویلا", qty: 1, price: 480000 },
    ],
  },
  {
    id: "۱۰۲۳",
    customer: "سارا رضایی",
    phone: "۰۹۳۵۹۸۷۶۵۴۳",
    address: "اصفهان، خیابان چهارباغ، پلاک ۴۵",
    total: 480000,
    status: "ارسال شده",
    date: "۱۴۰۳/۰۳/۰۳",
    payMethod: "آنلاین",
    items: [{ name: "اتیوپی یرگاچف", qty: 1, price: 480000 }],
  },
  {
    id: "۱۰۲۲",
    customer: "محمد کریمی",
    phone: "۰۹۱۸۴۵۶۷۸۹۰",
    address: "مشهد، بلوار وکیل‌آباد، پلاک ۷",
    total: 1340000,
    status: "تحویل شده",
    date: "۱۴۰۳/۰۳/۰۲",
    payMethod: "پرداخت در محل",
    items: [
      { name: "فرنچ پرس کلاسیک", qty: 1, price: 850000 },
      { name: "کنیا AA — ۲۵۰ گرم", qty: 1, price: 540000 },
    ],
  },
  {
    id: "۱۰۲۱",
    customer: "نگار حسینی",
    phone: "۰۹۳۳۱۲۳۴۵۶۷",
    address: "شیراز، خیابان زند، پلاک ۳",
    total: 420000,
    status: "تحویل شده",
    date: "۱۴۰۳/۰۳/۰۱",
    payMethod: "آنلاین",
    items: [{ name: "کلمبیا هویلا", qty: 1, price: 420000 }],
  },
]);

const statusOptions = ["در حال آماده‌سازی", "ارسال شده", "تحویل شده", "لغو شده"];

const statusColor = {
  "در حال آماده‌سازی": "text-maroon bg-maroon/10",
  "ارسال شده": "text-foreground bg-muted",
  "تحویل شده": "text-muted-foreground bg-muted",
  "لغو شده": "text-destructive bg-destructive/10",
};

const statusDot = {
  "در حال آماده‌سازی": "bg-maroon",
  "ارسال شده": "bg-foreground",
  "تحویل شده": "bg-muted-foreground",
  "لغو شده": "bg-red-500",
};

const inlineEdit = ref(null);
const inlineForm = ref({});

function openInline(o) {
  if (inlineEdit.value === o.id) { inlineEdit.value = null; return; }
  inlineForm.value = { id: o.id, customer: o.customer, total: o.total, status: o.status };
  inlineEdit.value = o.id;
}

function saveInline() {
  orders.value = orders.value.map((o) =>
    o.id === inlineForm.value.id ? { ...o, ...inlineForm.value } : o
  );
  inlineEdit.value = null;
}

const filterStatus = ref("all");
const filtered = computed(() =>
  filterStatus.value === "all"
    ? orders.value
    : orders.value.filter((o) => o.status === filterStatus.value)
);

const counts = computed(() => ({
  all: orders.value.length,
  "در حال آماده‌سازی": orders.value.filter((o) => o.status === "در حال آماده‌سازی").length,
  "ارسال شده": orders.value.filter((o) => o.status === "ارسال شده").length,
  "تحویل شده": orders.value.filter((o) => o.status === "تحویل شده").length,
}));

/* ── Print invoice ── */
const printOrder = ref(null);

function openPrint(o) {
  printOrder.value = o;
  setTimeout(() => window.print(), 200);
}

// ── View mode ──
const viewMode = ref(localStorage.getItem("navar-orders-view") || "list");
watch(viewMode, (v) => localStorage.setItem("navar-orders-view", v));

// ── Kanban columns (by status) ──
const kanbanCols = [
  { status: "در حال آماده‌سازی", accent: "border-t-maroon", dot: "bg-maroon" },
  { status: "ارسال شده",         accent: "border-t-blue-500", dot: "bg-blue-500" },
  { status: "تحویل شده",         accent: "border-t-green-600", dot: "bg-green-600" },
  { status: "لغو شده",           accent: "border-t-red-500", dot: "bg-red-500" },
];

// ── Report stats ──
const orderReportStats = computed(() => {
  const total = orders.value.reduce((s, o) => s + o.total, 0);
  const avg = orders.value.length ? Math.round(total / orders.value.length) : 0;
  const maxTotal = Math.max(...orders.value.map((o) => o.total), 1);
  return { total, avg, maxTotal };
});

// ── Gantt: orders grouped by date ──
const ganttDates = computed(() => {
  const map = new Map();
  for (const o of [...orders.value].sort((a, b) => b.date.localeCompare(a.date))) {
    if (!map.has(o.date)) map.set(o.date, []);
    map.get(o.date).push(o);
  }
  return [...map.entries()].map(([date, items]) => ({ date, items }));
});
</script>

<template>
  <div class="p-4 md:p-10">
    <div class="mb-8 flex flex-wrap items-end justify-between gap-4">
      <div>
        <h1 class="text-3xl font-light">سفارش‌ها <span class="text-maroon">.</span></h1>
        <p class="mt-2 text-sm text-muted-foreground">مدیریت سفارش‌های مشتریان</p>
      </div>
      <ViewSwitcher v-model="viewMode" :modes="['list','kanban','report','gantt']" />
    </div>

    <!-- Status filter tabs -->
    <div class="mb-6 flex flex-wrap gap-1 border-b border-border">
      <button
        v-for="f in [
          { v: 'all', l: 'همه', c: counts.all },
          { v: 'در حال آماده‌سازی', l: 'در حال آماده‌سازی', c: counts['در حال آماده‌سازی'] },
          { v: 'ارسال شده', l: 'ارسال شده', c: counts['ارسال شده'] },
          { v: 'تحویل شده', l: 'تحویل شده', c: counts['تحویل شده'] },
        ]"
        :key="f.v"
        @click="filterStatus = f.v"
        :class="['px-4 py-2.5 text-sm transition-colors relative shrink-0', filterStatus === f.v ? 'text-foreground after:absolute after:bottom-0 after:right-0 after:left-0 after:h-0.5 after:bg-maroon' : 'text-muted-foreground hover:text-foreground']"
      >
        {{ f.l }} <span class="mr-1 text-xs text-muted-foreground">({{ f.c }})</span>
      </button>
    </div>

    <!-- ── LIST VIEW ── -->
    <template v-if="viewMode === 'list'">
    <!-- MOBILE: Card list -->
    <div class="md:hidden space-y-3">
      <div v-for="o in filtered" :key="o.id" :class="['border border-border', inlineEdit === o.id ? 'border-maroon/30' : '']">
        <div class="flex items-start gap-3 p-3">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <span class="font-mono text-xs text-muted-foreground">#{{ o.id }}</span>
              <span :class="['inline-flex items-center gap-1.5 px-2 py-0.5 text-xs rounded-sm', statusColor[o.status] || 'bg-muted text-muted-foreground']">
                <span :class="['h-1.5 w-1.5 rounded-full shrink-0', statusDot[o.status] || 'bg-muted-foreground']" />
                {{ o.status }}
              </span>
            </div>
            <div class="font-medium text-sm">{{ o.customer }}</div>
            <div class="mt-1 flex items-center gap-3">
              <span class="text-maroon text-sm font-medium">{{ formatPrice(o.total) }}</span>
              <span class="text-xs text-muted-foreground">{{ o.date }}</span>
            </div>
          </div>
          <div class="flex items-center gap-1">
            <button
              @click="openPrint(o)"
              class="p-2 hover:bg-accent text-muted-foreground hover:text-maroon"
              title="چاپ فاکتور"
            >
              <Printer class="h-4 w-4" />
            </button>
            <button
              @click="openInline(o)"
              :class="['p-2 hover:bg-accent shrink-0', inlineEdit === o.id ? 'text-maroon' : 'text-muted-foreground hover:text-maroon']"
            >
              <X v-if="inlineEdit === o.id" class="h-4 w-4" />
              <Pencil v-else class="h-4 w-4" />
            </button>
          </div>
        </div>

        <!-- Mobile inline edit -->
        <div v-if="inlineEdit === o.id" class="border-t border-maroon/20 bg-maroon/5 p-3 space-y-3">
          <label class="block">
            <span class="text-xs text-muted-foreground uppercase tracking-wider">نام مشتری</span>
            <input v-model="inlineForm.customer" class="mt-1 w-full border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon" />
          </label>
          <label class="block">
            <span class="text-xs text-muted-foreground uppercase tracking-wider">مبلغ (تومان)</span>
            <input type="number" v-model.number="inlineForm.total" class="mt-1 w-full border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon" />
          </label>
          <label class="block">
            <span class="text-xs text-muted-foreground uppercase tracking-wider">وضعیت</span>
            <select v-model="inlineForm.status" class="mt-1 w-full border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon">
              <option v-for="s in statusOptions" :key="s">{{ s }}</option>
            </select>
          </label>
          <div class="flex gap-2 justify-end">
            <button @click="inlineEdit = null" class="border border-border px-4 py-1.5 text-xs hover:bg-accent">انصراف</button>
            <button @click="saveInline" class="bg-maroon px-5 py-1.5 text-xs text-maroon-foreground hover:opacity-90 flex items-center gap-1.5">
              <Check class="h-3 w-3" /> ذخیره
            </button>
          </div>
        </div>
      </div>
      <div v-if="filtered.length === 0" class="border border-dashed border-border p-12 text-center text-sm text-muted-foreground">سفارشی یافت نشد</div>
    </div>

    <!-- DESKTOP: Table -->
    <div class="hidden md:block border border-border">
      <table class="w-full text-sm">
        <thead class="bg-muted text-xs uppercase tracking-widest text-muted-foreground">
          <tr>
            <th class="px-6 py-4 text-right">شماره</th>
            <th class="px-6 py-4 text-right">مشتری</th>
            <th class="px-6 py-4 text-right">تاریخ</th>
            <th class="px-6 py-4 text-right">مبلغ</th>
            <th class="px-6 py-4 text-right">وضعیت</th>
            <th class="px-6 py-4"></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-border">
          <template v-for="o in filtered" :key="o.id">
            <tr :class="['transition-colors', inlineEdit === o.id ? 'bg-maroon/5' : 'hover:bg-accent/40']">
              <td class="px-6 py-4 font-mono text-muted-foreground">#{{ o.id }}</td>
              <td class="px-6 py-4 font-medium">{{ o.customer }}</td>
              <td class="px-6 py-4 text-muted-foreground">{{ o.date }}</td>
              <td class="px-6 py-4 text-maroon font-medium">{{ formatPrice(o.total) }}</td>
              <td class="px-6 py-4">
                <span :class="['inline-flex items-center gap-1.5 px-2.5 py-1 text-xs', statusColor[o.status] || 'bg-muted text-muted-foreground']">
                  <span :class="['h-1.5 w-1.5 rounded-full shrink-0', statusDot[o.status] || 'bg-muted-foreground']" />
                  {{ o.status }}
                </span>
              </td>
              <td class="px-6 py-4">
                <div class="flex justify-end gap-1">
                  <button
                    @click="openPrint(o)"
                    class="p-2 hover:bg-accent transition-colors text-muted-foreground hover:text-maroon"
                    title="چاپ فاکتور"
                  >
                    <Printer class="h-3.5 w-3.5" />
                  </button>
                  <button
                    @click="openInline(o)"
                    :class="['p-2 hover:bg-accent transition-colors', inlineEdit === o.id ? 'text-maroon' : 'text-muted-foreground hover:text-maroon']"
                    title="ویرایش سریع"
                  >
                    <X v-if="inlineEdit === o.id" class="h-3.5 w-3.5" />
                    <Pencil v-else class="h-3.5 w-3.5" />
                  </button>
                </div>
              </td>
            </tr>

            <!-- Inline edit row -->
            <tr v-if="inlineEdit === o.id" class="bg-maroon/5 border-b border-maroon/20">
              <td colspan="6" class="px-6 py-4">
                <div class="flex flex-wrap items-end gap-4">
                  <label class="block">
                    <span class="text-xs text-muted-foreground uppercase tracking-wider block mb-1">نام مشتری</span>
                    <input v-model="inlineForm.customer" class="border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon w-44" />
                  </label>
                  <label class="block">
                    <span class="text-xs text-muted-foreground uppercase tracking-wider block mb-1">مبلغ (تومان)</span>
                    <input type="number" v-model.number="inlineForm.total" class="border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon w-36" />
                  </label>
                  <label class="block">
                    <span class="text-xs text-muted-foreground uppercase tracking-wider block mb-1">وضعیت سفارش</span>
                    <select v-model="inlineForm.status" class="border border-border bg-background px-3 py-2 text-sm outline-none focus:border-maroon w-48">
                      <option v-for="s in statusOptions" :key="s">{{ s }}</option>
                    </select>
                  </label>
                  <div class="flex items-end gap-2 mr-auto">
                    <button @click="inlineEdit = null" class="border border-border px-4 py-2 text-xs hover:bg-accent">انصراف</button>
                    <button @click="saveInline" class="bg-maroon px-5 py-2 text-xs text-maroon-foreground hover:opacity-90 flex items-center gap-1.5">
                      <Check class="h-3.5 w-3.5" /> ذخیره
                    </button>
                  </div>
                </div>
              </td>
            </tr>
          </template>
          <tr v-if="filtered.length === 0">
            <td colspan="6" class="px-6 py-16 text-center text-muted-foreground">سفارشی یافت نشد</td>
          </tr>
        </tbody>
      </table>
    </div>
    </template><!-- /list -->

    <!-- ── KANBAN VIEW ── -->
    <template v-else-if="viewMode === 'kanban'">
      <div class="flex gap-4 overflow-x-auto pb-6" style="min-height:420px">
        <div v-for="col in kanbanCols" :key="col.status" class="flex-shrink-0 w-64">
          <div :class="['flex flex-col h-full border border-border border-t-2', col.accent]">
            <div class="border-b border-border px-4 py-3 flex items-center justify-between bg-muted/40">
              <div class="flex items-center gap-2">
                <span :class="['h-2 w-2 rounded-full shrink-0', col.dot]" />
                <span class="text-xs font-medium">{{ col.status }}</span>
              </div>
              <span class="text-xs text-muted-foreground border border-border px-1.5 py-0.5 bg-background">
                {{ orders.filter(o => o.status === col.status).length }}
              </span>
            </div>
            <div class="p-2 space-y-2 flex-1">
              <div
                v-for="o in orders.filter(o => o.status === col.status)"
                :key="o.id"
                class="bg-background border border-border p-3 cursor-pointer hover:border-maroon/40 transition-colors"
                @click="openInline(o)"
              >
                <div class="flex items-center gap-2 mb-2">
                  <span class="text-xs font-mono text-muted-foreground">#{{ o.id }}</span>
                  <span class="text-xs text-muted-foreground mr-auto">{{ o.date }}</span>
                </div>
                <div class="font-medium text-sm">{{ o.customer }}</div>
                <div class="text-maroon text-sm font-medium mt-1">{{ formatPrice(o.total) }}</div>
                <div class="text-xs text-muted-foreground mt-1">{{ o.payMethod }}</div>
              </div>
              <div
                v-if="orders.filter(o => o.status === col.status).length === 0"
                class="p-4 text-center text-xs text-muted-foreground border border-dashed border-border"
              >خالی</div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- ── REPORT VIEW ── -->
    <template v-else-if="viewMode === 'report'">
      <div class="space-y-6 max-w-3xl">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div
            v-for="stat in [
              { label: 'کل سفارشات', value: orders.length },
              { label: 'در آماده‌سازی', value: counts['در حال آماده‌سازی'] },
              { label: 'ارسال شده', value: counts['ارسال شده'] },
              { label: 'تحویل شده', value: counts['تحویل شده'] },
            ]"
            :key="stat.label"
            class="border border-border p-5"
          >
            <div class="text-xs uppercase tracking-widest text-muted-foreground">{{ stat.label }}</div>
            <div class="mt-2 text-2xl font-light text-maroon">{{ stat.value }}</div>
          </div>
        </div>
        <div class="border border-border p-6">
          <div class="text-xs uppercase tracking-widest text-muted-foreground mb-2">درآمد کل</div>
          <div class="text-4xl font-light text-maroon">{{ formatPrice(orderReportStats.total) }}</div>
          <div class="text-xs text-muted-foreground mt-1">میانگین هر سفارش: {{ formatPrice(orderReportStats.avg) }}</div>
        </div>
        <div class="border border-border p-6">
          <div class="text-xs uppercase tracking-widest text-muted-foreground mb-5">سفارشات بر اساس وضعیت</div>
          <div class="space-y-4">
            <div v-for="s in statusOptions" :key="s" class="flex items-center gap-4">
              <span class="text-sm w-44 truncate">{{ s }}</span>
              <div class="flex-1 h-2 bg-muted rounded-full overflow-hidden">
                <div
                  class="h-full bg-maroon rounded-full transition-all"
                  :style="`width:${orders.length ? (orders.filter(o => o.status === s).length / orders.length * 100) : 0}%`"
                />
              </div>
              <span class="text-xs text-muted-foreground w-6 text-left">{{ orders.filter(o => o.status === s).length }}</span>
            </div>
          </div>
        </div>
        <div class="border border-border p-6">
          <div class="text-xs uppercase tracking-widest text-muted-foreground mb-5">مقایسه مبالغ سفارشات</div>
          <div class="space-y-2.5">
            <div v-for="o in [...orders].sort((a,b) => b.total - a.total)" :key="o.id" class="flex items-center gap-3">
              <span class="text-xs font-mono text-muted-foreground w-12">#{{ o.id }}</span>
              <span class="text-xs w-28 truncate">{{ o.customer }}</span>
              <div class="flex-1 h-1.5 bg-muted rounded-full overflow-hidden">
                <div class="h-full bg-maroon/70 rounded-full" :style="`width:${(o.total / orderReportStats.maxTotal * 100)}%`" />
              </div>
              <span class="text-xs text-maroon w-24 text-left">{{ formatPrice(o.total) }}</span>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- ── GANTT / TIMELINE VIEW ── -->
    <template v-else-if="viewMode === 'gantt'">
      <div class="space-y-6">
        <div v-for="dateGroup in ganttDates" :key="dateGroup.date" class="flex gap-6">
          <div class="w-28 shrink-0 pt-2 text-right">
            <div class="text-xs font-medium text-maroon">{{ dateGroup.date }}</div>
            <div class="text-[10px] text-muted-foreground mt-0.5">{{ dateGroup.items.length }} سفارش</div>
          </div>
          <div class="flex-1 relative border-r border-border pr-5">
            <div class="absolute right-0 top-3.5 w-2 h-2 -mr-1 rounded-full bg-maroon ring-2 ring-background" />
            <div class="space-y-2">
              <div
                v-for="o in dateGroup.items"
                :key="o.id"
                class="border border-border bg-background p-3 hover:border-maroon/40 cursor-pointer transition-colors"
                @click="openInline(o)"
              >
                <div class="flex flex-wrap items-center gap-x-4 gap-y-1">
                  <span class="font-mono text-xs text-muted-foreground">#{{ o.id }}</span>
                  <span class="font-medium text-sm">{{ o.customer }}</span>
                  <span :class="['inline-flex items-center gap-1.5 px-2 py-0.5 text-xs', statusColor[o.status] || 'bg-muted text-muted-foreground']">
                    <span :class="['h-1.5 w-1.5 rounded-full shrink-0', statusDot[o.status] || 'bg-muted-foreground']" />
                    {{ o.status }}
                  </span>
                  <span class="text-sm text-maroon font-medium mr-auto">{{ formatPrice(o.total) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="ganttDates.length === 0" class="border border-dashed border-border p-16 text-center text-sm text-muted-foreground">
          سفارشی یافت نشد
        </div>
      </div>
    </template>

  </div>

  <!-- ── Print Invoice (hidden on screen, shown on print) ── -->
  <div v-if="printOrder" id="print-invoice" class="hidden print:block fixed inset-0 bg-white p-10 z-[9999] text-sm font-[Vazirmatn]" dir="rtl">
    <div class="max-w-2xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between border-b-2 border-gray-800 pb-6 mb-8">
        <div>
          <h1 class="text-3xl font-bold tracking-tight">نـوار<span style="color:#8B1A1A">.</span></h1>
          <p class="text-xs text-gray-500 mt-1">فروشگاه تخصصی قهوه و اکسسوری</p>
        </div>
        <div class="text-left">
          <p class="text-xs text-gray-400 uppercase tracking-wider">فاکتور فروش</p>
          <p class="text-2xl font-light text-gray-800 mt-1">#{{ printOrder.id }}</p>
          <p class="text-xs text-gray-500 mt-1">{{ printOrder.date }}</p>
        </div>
      </div>

      <!-- Customer Info -->
      <div class="grid grid-cols-2 gap-8 mb-8">
        <div>
          <p class="text-[10px] uppercase tracking-widest text-gray-400 mb-2">مشتری</p>
          <p class="font-semibold text-gray-800">{{ printOrder.customer }}</p>
          <p v-if="printOrder.phone" class="text-xs text-gray-500 mt-1">{{ printOrder.phone }}</p>
          <p v-if="printOrder.address" class="text-xs text-gray-500 mt-1 leading-5">{{ printOrder.address }}</p>
        </div>
        <div>
          <p class="text-[10px] uppercase tracking-widest text-gray-400 mb-2">جزئیات سفارش</p>
          <div class="space-y-1">
            <div class="flex gap-2 text-xs">
              <span class="text-gray-400 w-24">وضعیت:</span>
              <span class="font-medium text-gray-700">{{ printOrder.status }}</span>
            </div>
            <div class="flex gap-2 text-xs">
              <span class="text-gray-400 w-24">روش پرداخت:</span>
              <span class="font-medium text-gray-700">{{ printOrder.payMethod }}</span>
            </div>
            <div class="flex gap-2 text-xs">
              <span class="text-gray-400 w-24">تاریخ:</span>
              <span class="font-medium text-gray-700">{{ printOrder.date }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Items -->
      <table class="w-full mb-8">
        <thead>
          <tr class="border-b border-gray-200 text-[10px] uppercase tracking-widest text-gray-400">
            <th class="text-right pb-3 font-normal">محصول</th>
            <th class="text-center pb-3 font-normal">تعداد</th>
            <th class="text-left pb-3 font-normal">قیمت واحد</th>
            <th class="text-left pb-3 font-normal">جمع</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="item in printOrder.items" :key="item.name" class="py-3">
            <td class="py-3 text-gray-800 font-medium">{{ item.name }}</td>
            <td class="py-3 text-center text-gray-500">{{ item.qty }}</td>
            <td class="py-3 text-left text-gray-600">{{ formatPrice(item.price) }}</td>
            <td class="py-3 text-left font-semibold text-gray-800">{{ formatPrice(item.price * item.qty) }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Total -->
      <div class="border-t-2 border-gray-800 pt-4 flex justify-between items-center">
        <span class="text-[10px] uppercase tracking-widest text-gray-400">جمع کل</span>
        <span class="text-2xl font-light" style="color:#8B1A1A">{{ formatPrice(printOrder.total) }}</span>
      </div>

      <!-- Footer -->
      <div class="mt-16 pt-6 border-t border-gray-200 text-center text-[10px] text-gray-400">
        <p>نوار — فروشگاه تخصصی قهوه و اکسسوری</p>
        <p class="mt-1">با تشکر از خرید شما</p>
      </div>
    </div>
  </div>
</template>

<style>
@media print {
  body > *:not(#print-invoice) { display: none !important; }
  #print-invoice { display: block !important; position: fixed; inset: 0; }
}
</style>
