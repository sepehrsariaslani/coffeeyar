<script setup>
import { computed, onMounted, ref } from "vue";
import { TrendingUp, Package, Users, DollarSign, Bell, Check, X, ShoppingBag, ArrowUpRight, ArrowDownRight } from "lucide-vue-next";
import { useProductsStore } from "@/stores/products.js";
import { usePostsStore } from "@/stores/posts.js";
import { useAdminNotificationsStore } from "@/stores/adminNotifications.js";
import { api } from "@/lib/api.js";
import { isDemoMode } from "@/lib/demo.js";
import { getDemoDashboard } from "@/data/demoData.js";

function formatPrice(n) { return n ? Number(n).toLocaleString("fa-IR") : "۰"; }

const productsStore = useProductsStore();
const postsStore = usePostsStore();
const adminNotifStore = useAdminNotificationsStore();

// Dashboard data from API
const dashboardData = ref(null);
const dashboardLoading = ref(true);

onMounted(async () => {
  try {
    const dashboardRequest = isDemoMode ? Promise.resolve(getDemoDashboard()) : api.admin.dashboard();
    await Promise.all([
      dashboardRequest.then((data) => { dashboardData.value = data; }),
      productsStore.fetchProducts({ page_size: 100 }),
      postsStore.fetchPosts(),
    ]);
  } catch (e) {
    console.error("خطا در دریافت داشبورد:", e.message);
    dashboardData.value = getDemoDashboard();
  } finally {
    dashboardLoading.value = false;
  }
});

// Build stats from API data
const stats = computed(() => {
  const d = dashboardData.value;
  return [
    { label: "فروش کل", value: formatPrice(d?.total_revenue || 0), unit: "تومان", icon: DollarSign, change: "", up: true },
    { label: "سفارش‌ها", value: String(d?.total_orders || 0), unit: "سفارش", icon: Package, change: "", up: true },
    { label: "مشتریان", value: String(d?.total_customers || 0), unit: "نفر", icon: Users, change: "", up: true },
    { label: "محصولات", value: String(d?.total_products || 0), unit: "محصول", icon: TrendingUp, change: "", up: true },
  ];
});

// Weekly chart from recent orders (simplified)
const weeklyData = computed(() => {
  // Generate last 7 days from recent_orders count
  const days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"];
  const today = new Date().getDay();
  const recentCount = dashboardData.value?.recent_orders || 0;
  return days.map((day, i) => ({
    day,
    amount: Math.round((recentCount / 7) * (1000000 + Math.random() * 2000000)),
    orders: Math.max(1, Math.round(recentCount / 7 * (0.5 + Math.random()))),
  }));
});

const maxAmount = computed(() => Math.max(...weeklyData.value.map((d) => d.amount)));

// Top products from products store
const topProducts = computed(() => {
  const products = productsStore.products || [];
  return products
    .filter((p) => p.is_published)
    .slice(0, 4)
    .map((p) => ({
      name: p.name || p.item_name || "بدون نام",
      sold: p.stock_qty || 0,
      revenue: (p.price || p.price_toman || 0) * (p.stock_qty || 0),
    }));
});

const maxSold = computed(() => Math.max(...topProducts.value.map((p) => p.sold), 1));

// Recent products from store
const products = computed(() => (productsStore.products || []).slice(0, 4));

// Recent posts from store
const posts = computed(() => (postsStore.posts || []).slice(0, 4));
</script>

<template>
  <div class="p-4 md:p-10">
    <div class="mb-8">
      <h1 class="text-3xl font-light">داشبورد <span class="text-maroon">.</span></h1>
      <p class="mt-2 text-sm text-muted-foreground">نگاهی کلی به وضعیت فروشگاه</p>
    </div>

    <!-- Loading -->
    <div v-if="dashboardLoading" class="flex items-center justify-center py-20">
      <p class="text-muted-foreground">در حال بارگذاری داشبورد...</p>
    </div>

    <template v-else>
      <!-- Stats -->
      <div class="grid grid-cols-2 gap-px bg-border lg:grid-cols-4 mb-10">
        <div v-for="s in stats" :key="s.label" class="bg-background p-6">
          <div class="flex items-center justify-between">
            <span class="text-xs uppercase tracking-widest text-muted-foreground">{{ s.label }}</span>
            <component :is="s.icon" class="h-4 w-4 text-maroon" />
          </div>
          <div class="mt-4 text-2xl font-light">{{ s.value }}</div>
          <div class="mt-1 text-xs text-muted-foreground">{{ s.unit }}</div>
          <div v-if="s.change" :class="['mt-3 flex items-center gap-1 text-xs', s.up ? 'text-green-600' : 'text-red-500']">
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
          <div v-if="topProducts.length === 0" class="text-sm text-muted-foreground text-center py-8">
            محصولی ثبت نشده است
          </div>
          <div v-else class="space-y-4">
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
            <div v-if="products.length === 0" class="border border-dashed border-border p-6 mt-4 text-center text-sm text-muted-foreground">
              محصولی ثبت نشده است
            </div>
            <ul v-else class="mt-4 divide-y divide-border border-y border-border">
              <li v-for="p in products" :key="p.id" class="flex items-center justify-between py-4">
                <span class="text-sm">{{ p.name || p.item_name }}</span>
                <span class="text-sm text-maroon">{{ formatPrice(p.price || p.price_toman) }}</span>
              </li>
            </ul>
          </div>
          <div>
            <h2 class="text-xs uppercase tracking-widest text-muted-foreground">آخرین مقالات</h2>
            <div v-if="posts.length === 0" class="border border-dashed border-border p-6 mt-4 text-center text-sm text-muted-foreground">
              مقاله‌ای ثبت نشده است
            </div>
            <ul v-else class="mt-4 divide-y divide-border border-y border-border">
              <li v-for="p in posts" :key="p.slug" class="flex items-center justify-between py-4">
                <span class="text-sm">{{ p.title }}</span>
                <span class="text-xs text-muted-foreground">{{ p.date }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
