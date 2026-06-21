<script setup>
import { ref } from "vue";
import { RouterLink, RouterView, useRoute } from "vue-router";
import {
  Package, FileText, ShoppingBag, LayoutDashboard, ArrowRight,
  Users, Layers, FileEdit, HelpCircle, Menu, X, FolderOpen, PieChart,
  Tag, RotateCcw, Bell, MessageSquare, Globe, Ticket, Receipt, Palette,
  ChevronDown, Image,
} from "lucide-vue-next";
import { useAdminNotificationsStore } from "@/stores/adminNotifications.js";

const route = useRoute();
const sidebarOpen = ref(false);
const adminNotifStore = useAdminNotificationsStore();

const navGroups = [
  {
    label: null,
    items: [
      { to: "/admin", label: "داشبورد", icon: LayoutDashboard, exact: true },
    ],
  },
  {
    label: "محصولات",
    items: [
      { to: "/admin/products",   label: "محصولات",           icon: Package },
      { to: "/admin/product-attributes", label: "ویژگی‌ها",    icon: Tag },
      { to: "/admin/groups",     label: "گروه‌های محصول",    icon: FolderOpen },
      { to: "/admin/templates",  label: "قالب‌ها",           icon: Layers },
      { to: "/admin/profiles",   label: "پروفایل‌های محصول", icon: PieChart },
      { to: "/admin/categories", label: "دسته‌بندی‌ها",      icon: Tag },
    ],
  },
  {
    label: "سفارش‌ها",
    items: [
      { to: "/admin/orders",    label: "سفارش‌ها",  icon: ShoppingBag },
      { to: "/admin/returns",   label: "مرجوعی‌ها", icon: RotateCcw },
      { to: "/admin/customers", label: "مشتریان",   icon: Users },
    ],
  },
  {
    label: "محتوا",
    items: [
      { to: "/admin/posts",        label: "بلاگ",                 icon: FileText },
      { to: "/admin/content",      label: "مدیریت محتوا",         icon: FileEdit },
      { to: "/admin/faq",          label: "سوالات متداول",        icon: HelpCircle },
      { to: "/admin/product-faqs", label: "سوالات محصولات",       icon: MessageSquare },
      { to: "/admin/policies",     label: "قوانین سایت",          icon: FileText },
    ],
  },
  {
    label: "بازاریابی",
    items: [
      { to: "/admin/coupons", label: "کدهای تخفیف", icon: Ticket },
      { to: "/admin/invoice", label: "فاکتور سریع", icon: Receipt },
    ],
  },
  {
    label: "تنظیمات",
    items: [
      { to: "/admin/site-settings", label: "تنظیمات سایت", icon: Globe },
      { to: "/admin/appearance",    label: "ظاهر و قالب",  icon: Palette },
    ],
  },
];

// Track which groups are collapsed (all open by default)
const collapsed = ref({});

function toggleGroup(label) {
  collapsed.value[label] = !collapsed.value[label];
}

function isGroupCollapsed(label) {
  return !!collapsed.value[label];
}

function isActive(item) {
  if (item.exact) return route.path === item.to;
  return route.path.startsWith(item.to);
}

function isGroupActive(group) {
  return group.items.some((item) => isActive(item));
}

function closeOnNav() {
  sidebarOpen.value = false;
}
</script>

<template>
  <div class="flex min-h-screen bg-background" dir="rtl">
    <!-- Mobile overlay -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 z-30 bg-black/40 md:hidden"
      @click="sidebarOpen = false"
    />

    <!-- Sidebar -->
    <aside
      :class="[
        'fixed top-0 right-0 z-40 h-full w-64 border-l border-border bg-sidebar transition-transform duration-300 md:relative md:translate-x-0',
        sidebarOpen ? 'translate-x-0' : 'translate-x-full md:translate-x-0',
      ]"
    >
      <!-- Brand -->
      <div class="border-b border-border p-5 flex items-center justify-between">
        <div>
          <RouterLink to="/" class="text-lg font-medium" @click="closeOnNav">
            نـوار<span class="text-maroon">.</span>
          </RouterLink>
          <div class="mt-0.5 text-xs text-muted-foreground">پنل مدیریت</div>
        </div>
        <button
          type="button"
          class="p-1.5 hover:bg-accent md:hidden"
          @click="sidebarOpen = false"
        >
          <X class="h-4 w-4" />
        </button>
      </div>

      <!-- Nav groups -->
      <nav class="p-3 overflow-y-auto h-[calc(100vh-120px)] space-y-1">
        <template v-for="group in navGroups" :key="group.label || 'top'">

          <!-- Group header (only for named groups) -->
          <button
            v-if="group.label"
            type="button"
            class="w-full flex items-center justify-between px-2 py-1.5 mt-2 text-left"
            @click="toggleGroup(group.label)"
          >
            <span
              class="text-[10px] uppercase tracking-widest font-semibold transition-colors"
              :class="isGroupActive(group) ? 'text-maroon' : 'text-muted-foreground'"
            >
              {{ group.label }}
            </span>
            <ChevronDown
              class="h-3 w-3 text-muted-foreground transition-transform duration-200"
              :class="isGroupCollapsed(group.label) ? '-rotate-90' : ''"
            />
          </button>

          <!-- Group items -->
          <div
            v-if="!group.label || !isGroupCollapsed(group.label)"
            class="space-y-0.5"
          >
            <RouterLink
              v-for="n in group.items"
              :key="n.to"
              :to="n.to"
              @click="closeOnNav"
              :class="[
                'flex items-center gap-3 px-3 py-2 text-sm transition-colors rounded-sm',
                isActive(n)
                  ? 'bg-foreground text-background'
                  : 'text-muted-foreground hover:bg-accent hover:text-foreground',
              ]"
            >
              <component :is="n.icon" class="h-4 w-4 shrink-0" />
              {{ n.label }}
            </RouterLink>
          </div>

        </template>
      </nav>

      <!-- Back to site -->
      <div class="absolute bottom-5 right-5">
        <RouterLink to="/" class="flex items-center gap-2 text-xs text-muted-foreground hover:text-maroon">
          بازگشت به سایت <ArrowRight class="h-3 w-3" />
        </RouterLink>
      </div>
    </aside>

    <!-- Main content -->
    <div class="flex-1 min-w-0 flex flex-col">
      <!-- Mobile top bar -->
      <header class="flex items-center gap-3 border-b border-border bg-sidebar px-4 py-3 md:hidden">
        <button
          type="button"
          @click="sidebarOpen = true"
          class="p-1.5 hover:bg-accent"
        >
          <Menu class="h-5 w-5" />
        </button>
        <RouterLink to="/" class="text-base font-medium">
          نـوار<span class="text-maroon">.</span>
        </RouterLink>
        <span class="text-xs text-muted-foreground">پنل مدیریت</span>
        <RouterLink to="/admin" class="mr-auto relative p-1.5 hover:bg-accent">
          <Bell class="h-5 w-5 text-muted-foreground" />
          <span v-if="adminNotifStore.unread > 0" class="absolute -top-0.5 -left-0.5 flex h-4 w-4 items-center justify-center rounded-full bg-maroon text-[9px] text-white">
            {{ adminNotifStore.unread > 9 ? '۹+' : adminNotifStore.unread }}
          </span>
        </RouterLink>
      </header>

      <main class="flex-1 overflow-auto">
        <RouterView />
      </main>
    </div>
  </div>
</template>
