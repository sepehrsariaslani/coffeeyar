<script setup>
import { computed } from "vue";
import { products, posts, formatPrice } from "@/lib/data.js";
import { TrendingUp, Package, Users, DollarSign, Bell, Check, X, ShoppingBag, ArrowUpRight, ArrowDownRight } from "lucide-vue-next";
import { useAdminNotificationsStore } from "@/stores/adminNotifications.js";

const adminNotifStore = useAdminNotificationsStore();

const stats = [
  { label: "فروش این ماه", value: "۱۲٬۴۸۰٬۰۰۰", unit: "تومان", icon: DollarSign, change: "+۲۳٪", up: true },
  { label: "سفارش‌ها", value: "۲۴", unit: "سفارش", icon: Package, change: "+۸٪", up: true },
  { label: "مشتریان", value: "۱۸", unit: "نفر", icon: Users, change: "+۱۲٪", up: true },
  { label: "میانگین سفارش", value: "۵۲۰٬۰۰۰", unit: "تومان", icon: TrendingUp, change: "-۳٪", up: false },
];

const weeklyData = [
  { day: "شنبه", amount: 1800000, orders: 3 },
  { day: "یکشنبه", amount: 2400000, orders: 5 },
  { day: "دوشنبه", amount: 1200000, orders: 2 },
  { day: "سه‌شنبه", amount: 3100000, orders: 7 },
  { day: "چهارشنبه", amount: 2700000, orders: 4 },
  { day: "پنجشنبه", amount: 3800000, orders: 8 },
  { day: "جمعه", amount: 980000, orders: 2 },
];

const maxAmount = computed(() => Math.max(...weeklyData.map((d) => d.amount)));

const topProducts = [
  { name: "اتیوپی یرگاچف", sold: 12, revenue: 5760000 },
  { name: "کلمبیا هویلا", sold: 9, revenue: 3780000 },
  { name: "برزیل سرادو", sold: 7, revenue: 2660000 },
  { name: "فرنچ پرس کلاسیک", sold: 4, revenue: 3400000 },
];

const maxSold = computed(() => Math.max(...topProducts.map((p) => p.sold)));
</script>

<template>
  <div class="p-4 md:p-10">
    <div class="mb-8">
      <h1 class="text-3xl font-light">داشبورد <span class="text-maroon">.</span></h1>
      <p class="mt-2 text-sm text-muted-foreground">نگاهی کلی به وضعیت فروشگاه</p>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 gap-px bg-border lg:grid-cols-4 mb-10">
      <div v-for="s in stats" :key="s.label" class="bg-background p-6">
        <div class="flex items-center justify-between">
          <span class="text-xs uppercase tracking-widest text-muted-foreground">{{ s.label }}</span>
          <component :is="s.icon" class="h-4 w-4 text-maroon" />
        </div>
        <div class="mt-4 text-2xl font-light">{{ s.value }}</div>
        <div class="mt-1 text-xs text-muted-foreground">{{ s.unit }}</div>
        <div :class="['mt-3 flex items-center gap-1 text-xs', s.up ? 'text-green-600' : 'text-red-500']">
          <ArrowUpRight v-if="s.up" class="h-3 w-3" />
          <ArrowDownRight v-else class="h-3 w-3" />
          {{ s.change }} نسبت به ماه گذشته
        </div>
      </div>
    </div>

    <!-- Weekly Chart + Top Products -->
    <div class="grid gap-8 lg:grid-cols-[1.6fr_1fr] mb-10">
      <!-- Bar Chart -->
      <div class="border border-border p-6">
        <div class="mb-6 flex items-center justify-between">
          <h2 class="text-sm font-medium">فروش هفته جاری</h2>
          <span class="text-xs text-muted-foreground">{{ formatPrice(weeklyData.reduce((s, d) => s + d.amount, 0)) }}</span>
        </div>
        <div class="flex items-end gap-2 h-40">
          <div
            v-for="d in weeklyData"
            :key="d.day"
            class="flex flex-1 flex-col items-center gap-1.5"
          >
            <div class="text-[9px] text-muted-foreground">{{ d.orders }}</div>
            <div class="relative w-full group">
              <div
                class="w-full bg-maroon/20 hover:bg-maroon/40 transition-colors rounded-sm cursor-pointer"
                :style="{ height: Math.max(4, (d.amount / maxAmount) * 120) + 'px' }"
              >
                <div
                  class="absolute -top-6 right-1/2 translate-x-1/2 hidden group-hover:block bg-foreground text-background text-[9px] px-1.5 py-0.5 whitespace-nowrap z-10"
                >
                  {{ formatPrice(d.amount) }}
                </div>
              </div>
            </div>
            <div class="text-[9px] text-muted-foreground whitespace-nowrap">{{ d.day }}</div>
          </div>
        </div>
      </div>

      <!-- Top Products -->
      <div class="border border-border p-6">
        <h2 class="mb-5 text-sm font-medium">پرفروش‌ترین محصولات</h2>
        <div class="space-y-4">
          <div v-for="(p, i) in topProducts" :key="p.name">
            <div class="flex items-center justify-between mb-1.5">
              <div class="flex items-center gap-2">
                <span class="text-[10px] text-maroon w-4">{{ i + 1 }}</span>
                <span class="text-sm leading-tight">{{ p.name }}</span>
              </div>
              <span class="text-xs text-muted-foreground">{{ p.sold }} عدد</span>
            </div>
            <div class="h-1.5 w-full rounded-full bg-muted">
              <div
                class="h-1.5 rounded-full bg-maroon transition-all duration-700"
                :style="{ width: (p.sold / maxSold * 100) + '%' }"
              />
            </div>
            <div class="mt-1 text-[10px] text-muted-foreground text-left ltr">{{ formatPrice(p.revenue) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Notifications + Recent -->
    <div class="grid gap-10 lg:grid-cols-2">
      <!-- Admin Notifications -->
      <div>
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xs uppercase tracking-widest text-muted-foreground flex items-center gap-2">
            <Bell class="h-3.5 w-3.5" /> اعلان‌های سفارش
            <span v-if="adminNotifStore.unread > 0" class="flex h-4 w-4 items-center justify-center rounded-full bg-maroon text-[9px] text-white">
              {{ adminNotifStore.unread }}
            </span>
          </h2>
          <button v-if="adminNotifStore.notifications.length > 0" @click="adminNotifStore.markAllRead()"
            class="text-[10px] text-muted-foreground hover:text-maroon flex items-center gap-1">
            <Check class="h-3 w-3" /> همه خوانده شد
          </button>
        </div>
        <div v-if="adminNotifStore.notifications.length === 0" class="border border-dashed border-border p-8 text-center text-sm text-muted-foreground">
          هنوز سفارش جدیدی ثبت نشده
        </div>
        <ul v-else class="divide-y divide-border border-y border-border">
          <li v-for="n in adminNotifStore.notifications.slice(0, 6)" :key="n.id"
            :class="['flex items-start gap-3 py-3.5', n.read ? 'opacity-60' : '']">
            <span :class="['mt-1 flex h-6 w-6 shrink-0 items-center justify-center rounded-full', n.read ? 'bg-muted' : 'bg-maroon/10']">
              <ShoppingBag :class="['h-3 w-3', n.read ? 'text-muted-foreground' : 'text-maroon']" />
            </span>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <p class="text-sm font-medium leading-tight">{{ n.title }}</p>
                <button @click="adminNotifStore.remove(n.id)" class="text-muted-foreground hover:text-red-500 shrink-0 mt-0.5">
                  <X class="h-3 w-3" />
                </button>
              </div>
              <p class="mt-0.5 text-xs text-muted-foreground truncate">{{ n.body }}</p>
              <p v-if="n.amount" class="mt-0.5 text-xs text-maroon font-medium">{{ formatPrice(n.amount) }}</p>
              <p class="mt-0.5 text-[10px] text-muted-foreground">{{ n.time }}</p>
            </div>
          </li>
        </ul>
      </div>

      <div class="grid gap-8">
        <div>
          <h2 class="text-xs uppercase tracking-widest text-muted-foreground">آخرین محصولات</h2>
          <ul class="mt-4 divide-y divide-border border-y border-border">
            <li v-for="p in products.slice(0, 4)" :key="p.id" class="flex items-center justify-between py-4">
              <span class="text-sm">{{ p.name }}</span>
              <span class="text-sm text-maroon">{{ formatPrice(p.price) }}</span>
            </li>
          </ul>
        </div>
        <div>
          <h2 class="text-xs uppercase tracking-widest text-muted-foreground">آخرین مقالات</h2>
          <ul class="mt-4 divide-y divide-border border-y border-border">
            <li v-for="p in posts.slice(0, 4)" :key="p.slug" class="flex items-center justify-between py-4">
              <span class="text-sm">{{ p.title }}</span>
              <span class="text-xs text-muted-foreground">{{ p.date }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
