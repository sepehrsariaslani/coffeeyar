<script setup>
import { ref, computed, onMounted } from "vue";
import { RouterLink } from "vue-router";
import {
  User, Package, MapPin, ChevronLeft, ChevronDown,
  Edit2, Check, Plus, Trash2, Heart, Wallet, RotateCcw, Bell, CreditCard, Palette,
} from "lucide-vue-next";
import TheLayout from "@/components/site/TheLayout.vue";
import LocationPicker from "@/components/LocationPicker.vue";
import AddrMiniMap from "@/components/AddrMiniMap.vue";
import ProductCard from "@/components/ProductCard.vue";
import { useAccountStore } from "@/stores/account.js";
import { useWishlistStore } from "@/stores/wishlist.js";
import { useWalletStore } from "@/stores/wallet.js";
import { useNotificationsStore } from "@/stores/notifications.js";
import { useReturnsStore } from "@/stores/returns.js";
import { useProductsStore } from "@/stores/products.js";
import { toFa } from "@/lib/utils.js";
function formatPrice(n) { return n ? Number(n).toLocaleString("fa-IR") : "۰"; }

const accountStore = useAccountStore();
const wishlistStore = useWishlistStore();
const walletStore = useWalletStore();
const notifStore = useNotificationsStore();
const returnsStore = useReturnsStore();
const productsStore = useProductsStore();
const tab = ref("orders");

onMounted(async () => {
  await Promise.all([
    accountStore.init(),
    productsStore.fetchProducts({ page_size: 100 }),
    walletStore.fetchWallet(),
    notifStore.refresh(),
    returnsStore.fetchReturns(),
  ]);
  // Keep the profile form in sync once the real profile arrives
  profileForm.value = { ...accountStore.profile };
});

// ── Wallet
const chargeAmount = ref("");
const chargeSuccess = ref(false);
async function doCharge() {
  const amt = Number(String(chargeAmount.value).replace(/,/g, ""));
  if (!amt || amt < 10000) return;
  const ok = await walletStore.charge(amt, "شارژ دستی کیف پول");
  if (!ok) return;
  chargeAmount.value = "";
  chargeSuccess.value = true;
  setTimeout(() => (chargeSuccess.value = false), 3000);
}

const TXN_LABEL = { charge: "شارژ کیف پول", spend: "پرداخت", refund: "بازگشت وجه" };
const TXN_COLOR = { charge: "#16a34a", spend: "#dc2626", refund: "#2563eb" };

// ── Returns
const returnOrderId = ref("");
const returnReason = ref("defective");
const returnDesc = ref("");
const returnSuccess = ref(false);
function submitReturn() {
  if (!returnOrderId.value) return;
  const order = accountStore.orders.find((o) => o.id === returnOrderId.value);
  if (!order) return;
  returnsStore.submit({
    orderId: order.id,
    orderRef: order.id,
    reason: returnReason.value,
    description: returnDesc.value,
    items: order.items,
    totalAmount: order.totalPrice,
  });
  returnOrderId.value = "";
  returnReason.value = "defective";
  returnDesc.value = "";
  returnSuccess.value = true;
  setTimeout(() => (returnSuccess.value = false), 3000);
}

const RETURN_STATUS = {
  "در انتظار بررسی": { bg: "#fefce8", text: "#854d0e" },
  "تایید شده":       { bg: "#f0fdf4", text: "#14532d" },
  "رد شده":          { bg: "#fef2f2", text: "#7f1d1d" },
};

const NOTIF_ICON = {
  wallet: "💰", refund: "💸", return: "↩️", success: "✅", info: "ℹ️", order: "📦",
};

const wishlistedProducts = computed(() =>
  productsStore.products.filter((p) => wishlistStore.ids.includes(p.id))
);

const displayName = computed(() => accountStore.profile.name || "مشتری گرامی");
const initials = computed(() => {
  const n = accountStore.profile.name || "م گ";
  const parts = n.trim().split(" ");
  return parts.length >= 2 ? parts[0][0] + parts[1][0] : n[0] || "م";
});

const totalSpent = computed(() =>
  accountStore.orders.reduce((s, o) => s + o.totalPrice, 0)
);
const activeOrders = computed(() =>
  accountStore.orders.filter(
    (o) => o.status !== "تحویل داده شده" && o.status !== "لغو شده"
  )
);

const STATUS_STYLE = {
  "در حال پردازش":  { dot: "#b8860b", bg: "#fdfaee", text: "#7a5c00" },
  "تایید شده":      { dot: "#3a7abf", bg: "#f0f5fc", text: "#1e4d80" },
  "در حال ارسال":   { dot: "#6a4fbf", bg: "#f4f0fc", text: "#3d2580" },
  "تحویل داده شده": { dot: "#3a8a5e", bg: "#f0faf5", text: "#1e5c3a" },
  "لغو شده":        { dot: "#888",    bg: "#f5f5f5", text: "#555"    },
};

const tabs = [
  { id: "orders",      label: "سفارش‌ها",      icon: Package    },
  { id: "wishlist",    label: "علاقه‌مندی‌ها", icon: Heart      },
  { id: "wallet",      label: "کیف پول",       icon: Wallet     },
  { id: "returns",     label: "مرجوعی",        icon: RotateCcw  },
  { id: "notifs",      label: "اعلان‌ها",      icon: Bell       },
  { id: "profile",     label: "پروفایل",       icon: User       },
  { id: "addresses",   label: "آدرس‌ها",       icon: MapPin     },
];

// ── Orders
const expandedOrder = ref(null);

// ── Profile
const profileForm = ref({ ...accountStore.profile });
const profileSaved = ref(false);
function saveProfile(e) {
  e.preventDefault();
  accountStore.updateProfile(profileForm.value);
  profileSaved.value = true;
  setTimeout(() => (profileSaved.value = false), 2000);
}

// ── Addresses
const editing = ref(null);
const addrCoords = ref(null);

const emptyAddr = () => ({
  label: "خانه", isDefault: false, province: "", city: "",
  street: "", postalCode: "", fullName: "", phone: "", coords: null,
});
const addressForm = ref(emptyAddr());

function startEdit(addr) {
  editing.value = addr;
  if (addr === "new") {
    addressForm.value = emptyAddr();
    addrCoords.value = null;
  } else {
    addressForm.value = { ...addr };
    addrCoords.value = addr.coords || null;
  }
}

function onAddressResolved({ province, city }) {
  if (province && !addressForm.value.province) addressForm.value.province = province;
  if (city && !addressForm.value.city) addressForm.value.city = city;
}

function saveAddress(e) {
  e.preventDefault();
  const data = { ...addressForm.value, coords: addrCoords.value };
  if (editing.value === "new") {
    accountStore.addAddress(data);
  } else {
    accountStore.updateAddress({ ...data, id: editing.value.id });
  }
  editing.value = null;
}
</script>

<template>
  <TheLayout>

    <!-- ── Top Banner ──────────────────────────────────── -->
    <div class="acct-banner">
      <div class="acct-banner__inner">
        <div class="acct-avatar">{{ initials }}</div>
        <div class="acct-banner__info">
          <div class="acct-banner__greeting">خوش آمدید،</div>
          <h1 class="acct-banner__name">{{ displayName }}</h1>
          <div v-if="accountStore.profile.email" class="acct-banner__email">
            {{ accountStore.profile.email }}
          </div>
        </div>
        <div class="acct-stats">
          <div class="acct-stat">
            <div class="acct-stat__val">{{ toFa(accountStore.orders.length) }}</div>
            <div class="acct-stat__lbl">سفارش کل</div>
          </div>
          <div class="acct-stat acct-stat--sep" />
          <div class="acct-stat">
            <div class="acct-stat__val acct-stat__val--accent">{{ toFa(activeOrders.length) }}</div>
            <div class="acct-stat__lbl">سفارش فعال</div>
          </div>
          <div class="acct-stat acct-stat--sep" />
          <div class="acct-stat">
            <div class="acct-stat__val">{{ formatPrice(totalSpent) }}</div>
            <div class="acct-stat__lbl">مجموع خرید (تومان)</div>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Tab Bar ─────────────────────────────────────── -->
    <div class="acct-tabbar">
      <div class="acct-tabbar__inner">
        <button
          v-for="t in tabs" :key="t.id" type="button"
          class="acct-tab" :class="tab === t.id ? 'acct-tab--active' : ''"
          @click="tab = t.id"
        >
          <component :is="t.icon" class="acct-tab__icon" />
          {{ t.label }}
        </button>
        <RouterLink to="/appearance" class="acct-tab acct-tab--appearance">
          <Palette class="acct-tab__icon" />
          ظاهر سایت
        </RouterLink>
        <RouterLink to="/" class="acct-tab acct-tab--back">
          <ChevronLeft class="acct-tab__icon" />
          فروشگاه
        </RouterLink>
      </div>
    </div>

    <!-- ── Content ─────────────────────────────────────── -->
    <div class="acct-content">

      <!-- ════ WISHLIST ════ -->
      <div v-if="tab === 'wishlist'">
        <div v-if="wishlistedProducts.length === 0" class="acct-empty">
          <Heart class="acct-empty__icon" />
          <p class="acct-empty__text">هنوز محصولی به علاقه‌مندی‌ها اضافه نشده است.</p>
          <RouterLink to="/products" class="acct-empty__cta">مشاهده محصولات</RouterLink>
        </div>
        <div v-else>
          <div class="wishlist-account-grid">
            <ProductCard v-for="p in wishlistedProducts" :key="p.id" :product="p" />
          </div>
          <div class="mt-6 text-center">
            <RouterLink to="/wishlist" class="text-sm text-maroon hover:underline">مشاهده صفحه کامل علاقه‌مندی‌ها</RouterLink>
          </div>
        </div>
      </div>

      <!-- ════ ORDERS ════ -->
      <div v-if="tab === 'orders'">
        <div v-if="accountStore.orders.length === 0" class="acct-empty">
          <Package class="acct-empty__icon" />
          <p class="acct-empty__text">هنوز سفارشی ثبت نشده است.</p>
          <RouterLink to="/products" class="acct-empty__cta">رفتن به فروشگاه</RouterLink>
        </div>

        <div v-else class="orders-list">
          <div
            v-for="order in accountStore.orders" :key="order.id"
            class="order-card"
          >
            <!-- Header row -->
            <div
              class="order-card__head"
              @click="expandedOrder = expandedOrder === order.id ? null : order.id"
            >
              <div class="order-card__id-block">
                <div class="order-card__id">{{ order.id }}</div>
                <div class="order-card__date">{{ order.date }}</div>
              </div>
              <div class="order-card__middle">
                <span
                  class="order-status-pill"
                  :style="{
                    background: STATUS_STYLE[order.status]?.bg || '#f5f5f5',
                    color: STATUS_STYLE[order.status]?.text || '#555',
                  }"
                >
                  <span
                    class="order-status-pill__dot"
                    :style="{ background: STATUS_STYLE[order.status]?.dot || '#888' }"
                  />
                  {{ order.status }}
                </span>
                <div class="order-card__items-count">
                  {{ toFa(order.items.length) }} قلم
                </div>
              </div>
              <div class="order-card__right">
                <div class="order-card__price">{{ formatPrice(order.totalPrice) }} <span>تومان</span></div>
                <ChevronDown
                  class="order-card__chevron"
                  :class="expandedOrder === order.id ? 'order-card__chevron--open' : ''"
                />
              </div>
            </div>

            <!-- Expanded -->
            <div v-if="expandedOrder === order.id" class="order-card__body">
              <div class="order-items">
                <div
                  v-for="item in order.items" :key="item.productId"
                  class="order-item"
                >
                  <div class="order-item__info">
                    <div class="order-item__name">{{ item.name }}</div>
                    <div class="order-item__meta">{{ item.weight }} · {{ item.grind }} × {{ toFa(item.qty) }}</div>
                  </div>
                  <div class="order-item__price">{{ formatPrice(item.unitPrice * item.qty) }} تومان</div>
                </div>
              </div>
              <div class="order-card__footer-row">
                <div class="order-card__address">
                  <MapPin class="order-card__address-icon" />
                  {{ order.address }}
                </div>
                <div v-if="order.trackingCode" class="order-card__tracking">
                  کد رهگیری:
                  <span class="order-card__tracking-code">{{ order.trackingCode }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ════ WALLET ════ -->
      <div v-if="tab === 'wallet'" class="wallet-pane">
        <div class="pane-header">
          <h2 class="pane-title">کیف پول</h2>
          <p class="pane-sub">موجودی و تراکنش‌های کیف پول شما</p>
        </div>

        <!-- Balance card -->
        <div class="wallet-balance-card">
          <div class="wallet-balance-card__label">موجودی فعلی</div>
          <div class="wallet-balance-card__amount">{{ formatPrice(walletStore.balance) }} <span>تومان</span></div>
        </div>

        <!-- Charge form -->
        <div class="wallet-charge-box">
          <div class="wallet-charge-box__title">شارژ کیف پول</div>
          <div class="wallet-charge-presets">
            <button v-for="amt in [50000, 100000, 200000, 500000]" :key="amt" type="button"
              class="wallet-preset-btn" @click="chargeAmount = amt">
              {{ formatPrice(amt) }}
            </button>
          </div>
          <div class="wallet-charge-row">
            <input v-model="chargeAmount" type="number" min="10000" step="1000"
              placeholder="مبلغ دلخواه (تومان)" class="form-input" dir="ltr" />
            <button type="button" class="save-btn" @click="doCharge" style="white-space:nowrap">
              <Check v-if="chargeSuccess" class="h-4 w-4" />
              {{ chargeSuccess ? 'شارژ شد ✓' : 'شارژ' }}
            </button>
          </div>
          <p class="wallet-charge-hint">حداقل مبلغ شارژ: ۱۰,۰۰۰ تومان</p>
        </div>

        <!-- Transactions -->
        <div class="wallet-txns">
          <div class="wallet-txns__title">تاریخچه تراکنش‌ها</div>
          <div v-if="walletStore.transactions.length === 0" class="acct-empty">
            <Wallet class="acct-empty__icon" />
            <p class="acct-empty__text">تراکنشی ثبت نشده است.</p>
          </div>
          <div v-else class="wallet-txn-list">
            <div v-for="txn in walletStore.transactions" :key="txn.id" class="wallet-txn">
              <div class="wallet-txn__info">
                <div class="wallet-txn__desc">{{ txn.description || TXN_LABEL[txn.type] }}</div>
                <div class="wallet-txn__date">{{ txn.date }} — {{ txn.time }}</div>
              </div>
              <div class="wallet-txn__amount" :style="{ color: TXN_COLOR[txn.type] }">
                {{ txn.type === 'spend' ? '−' : '+' }}{{ formatPrice(txn.amount) }} تومان
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ════ RETURNS ════ -->
      <div v-if="tab === 'returns'" class="returns-pane">
        <div class="pane-header">
          <h2 class="pane-title">درخواست مرجوعی</h2>
          <p class="pane-sub">بازگشت کالا و دریافت وجه</p>
        </div>

        <!-- New return form -->
        <div class="return-form-card">
          <div class="return-form-card__title">درخواست جدید</div>
          <div class="form-grid">
            <label class="form-field form-field--full">
              <span class="form-label">سفارش مورد نظر *</span>
              <select v-model="returnOrderId" class="form-input">
                <option value="">— انتخاب سفارش —</option>
                <option v-for="o in accountStore.orders.filter(o => o.status === 'تحویل داده شده')" :key="o.id" :value="o.id">
                  {{ o.id }} — {{ formatPrice(o.totalPrice) }} تومان
                </option>
              </select>
            </label>
            <label class="form-field">
              <span class="form-label">دلیل مرجوعی *</span>
              <select v-model="returnReason" class="form-input">
                <option value="defective">کالای معیوب</option>
                <option value="wrong_item">کالای اشتباه</option>
                <option value="not_as_described">مطابق توضیحات نیست</option>
                <option value="changed_mind">انصراف از خرید</option>
                <option value="other">سایر</option>
              </select>
            </label>
            <label class="form-field form-field--full">
              <span class="form-label">توضیحات (اختیاری)</span>
              <textarea v-model="returnDesc" rows="3" class="form-input form-input--textarea"
                placeholder="جزئیات بیشتر درباره دلیل مرجوعی..." />
            </label>
          </div>
          <div v-if="returnSuccess" class="return-success">درخواست مرجوعی با موفقیت ثبت شد. پس از بررسی، وجه به کیف پول شما بازگشت داده می‌شود.</div>
          <button type="button" class="save-btn mt-4" @click="submitReturn" :disabled="!returnOrderId">
            <RotateCcw class="h-4 w-4" />
            ثبت درخواست مرجوعی
          </button>
        </div>

        <!-- Existing returns -->
        <div class="returns-list" v-if="returnsStore.requests.length">
          <div class="wallet-txns__title mt-6">درخواست‌های قبلی</div>
          <div v-for="req in returnsStore.requests" :key="req.id" class="return-item">
            <div class="return-item__head">
              <div>
                <div class="return-item__id">{{ req.id }}</div>
                <div class="return-item__date">{{ req.date }}</div>
              </div>
              <span class="return-status" :style="{ background: RETURN_STATUS[req.status]?.bg, color: RETURN_STATUS[req.status]?.text }">
                {{ req.status }}
              </span>
            </div>
            <div v-if="req.adminNote" class="return-item__note">یادداشت: {{ req.adminNote }}</div>
          </div>
        </div>
      </div>

      <!-- ════ NOTIFICATIONS ════ -->
      <div v-if="tab === 'notifs'" class="notifs-pane">
        <div class="pane-header pane-header--row">
          <div>
            <h2 class="pane-title">اعلان‌ها</h2>
            <p class="pane-sub">{{ toFa(notifStore.unreadCount) }} اعلان خوانده نشده</p>
          </div>
          <div class="notifs-actions">
            <button v-if="notifStore.items.length" type="button" class="btn-ghost" @click="notifStore.markAllRead()">همه خوانده شد</button>
            <button v-if="notifStore.items.length" type="button" class="btn-ghost" style="color:#dc2626;border-color:#fecaca" @click="notifStore.clear()">پاک کردن همه</button>
          </div>
        </div>

        <div v-if="notifStore.items.length === 0" class="acct-empty">
          <Bell class="acct-empty__icon" />
          <p class="acct-empty__text">اعلانی وجود ندارد.</p>
        </div>

        <div v-else class="notifs-list">
          <div
            v-for="n in notifStore.items"
            :key="n.id"
            class="notif-item"
            :class="n.read ? '' : 'notif-item--unread'"
            @click="notifStore.markRead(n.id)"
          >
            <span class="notif-item__icon">{{ NOTIF_ICON[n.type] || 'ℹ️' }}</span>
            <div class="notif-item__body">
              <div class="notif-item__title">{{ n.title }}</div>
              <div v-if="n.body" class="notif-item__text">{{ n.body }}</div>
              <div class="notif-item__date">{{ n.date }} — {{ n.time }}</div>
            </div>
            <button type="button" class="notif-item__del" @click.stop="notifStore.remove(n.id)" title="حذف">
              <Trash2 class="h-3.5 w-3.5" />
            </button>
          </div>
        </div>
      </div>

      <!-- ════ PROFILE ════ -->
      <div v-if="tab === 'profile'" class="profile-pane">
        <div class="pane-header">
          <h2 class="pane-title">اطلاعات حساب کاربری</h2>
          <p class="pane-sub">مشخصات تماس خود را ویرایش کنید</p>
        </div>

        <form @submit="saveProfile" class="profile-form">
          <div class="profile-form__avatar-row">
            <div class="profile-form__avatar">{{ initials }}</div>
            <div>
              <div class="profile-form__avatar-name">{{ displayName }}</div>
              <div class="profile-form__avatar-hint">نام نمایشی شما در سیستم</div>
            </div>
          </div>

          <div class="form-grid">
            <label class="form-field form-field--full">
              <span class="form-label">نام و نام خانوادگی</span>
              <input
                v-model="profileForm.name"
                placeholder="نام خود را وارد کنید"
                class="form-input"
              />
            </label>
            <label class="form-field">
              <span class="form-label">ایمیل</span>
              <input
                v-model="profileForm.email"
                type="email" dir="ltr"
                placeholder="email@example.com"
                class="form-input"
              />
            </label>
            <label class="form-field">
              <span class="form-label">شماره موبایل</span>
              <input
                v-model="profileForm.phone"
                type="tel"
                placeholder="۰۹۱۲۱۲۳۴۵۶۷"
                class="form-input"
              />
            </label>
          </div>

          <button type="submit" class="save-btn">
            <Check v-if="profileSaved" class="save-btn__icon" />
            <Edit2 v-else class="save-btn__icon" />
            {{ profileSaved ? "ذخیره شد ✓" : "ذخیره تغییرات" }}
          </button>
        </form>
      </div>

      <!-- ════ ADDRESSES ════ -->
      <div v-if="tab === 'addresses'">

        <!-- Address Form -->
        <div v-if="editing">
          <div class="pane-header">
            <button type="button" class="pane-back" @click="editing = null">
              <ChevronLeft class="h-4 w-4" /> بازگشت به لیست آدرس‌ها
            </button>
            <h2 class="pane-title">{{ editing === 'new' ? 'افزودن آدرس جدید' : 'ویرایش آدرس' }}</h2>
          </div>

          <form @submit="saveAddress" class="addr-form">

            <!-- Label row -->
            <div class="addr-label-chips">
              <span class="form-label">نوع آدرس</span>
              <div class="addr-chips">
                <button
                  v-for="lbl in ['خانه','محل کار','سایر']" :key="lbl"
                  type="button"
                  class="addr-chip"
                  :class="addressForm.label === lbl ? 'addr-chip--active' : ''"
                  @click="addressForm.label = lbl"
                >{{ lbl }}</button>
              </div>
            </div>

            <div class="form-grid">
              <label class="form-field">
                <span class="form-label">نام گیرنده</span>
                <input v-model="addressForm.fullName" class="form-input" placeholder="نام و نام خانوادگی گیرنده" />
              </label>
              <label class="form-field">
                <span class="form-label">شماره موبایل</span>
                <input v-model="addressForm.phone" type="tel" class="form-input" placeholder="۰۹۱۲۱۲۳۴۵۶۷" />
              </label>
              <label class="form-field">
                <span class="form-label">استان</span>
                <input required v-model="addressForm.province" class="form-input" placeholder="مثال: تهران" />
              </label>
              <label class="form-field">
                <span class="form-label">شهر</span>
                <input required v-model="addressForm.city" class="form-input" placeholder="مثال: تهران" />
              </label>
              <label class="form-field form-field--full">
                <span class="form-label">آدرس کامل</span>
                <textarea required v-model="addressForm.street" rows="3" class="form-input form-input--textarea" placeholder="خیابان، کوچه، پلاک و واحد" />
              </label>
              <label class="form-field">
                <span class="form-label">کد پستی</span>
                <input v-model="addressForm.postalCode" dir="ltr" class="form-input" placeholder="1234567890" />
              </label>
            </div>

            <!-- Map picker -->
            <div class="form-section">
              <div class="form-section__title">
                <MapPin class="h-3.5 w-3.5" />
                موقعیت جغرافیایی
              </div>
              <p class="form-section__hint">
                با انتخاب موقعیت روی نقشه، شهر و استان به‌صورت خودکار پر می‌شود.
              </p>
              <LocationPicker
                v-model="addrCoords"
                @address-resolved="onAddressResolved"
              />
            </div>

            <!-- Default checkbox -->
            <label class="default-check">
              <input type="checkbox" v-model="addressForm.isDefault" class="default-check__input" />
              <span class="default-check__box" :class="addressForm.isDefault ? 'default-check__box--on' : ''" />
              <span class="default-check__label">این آدرس را به عنوان پیش‌فرض ذخیره کن</span>
            </label>

            <div class="addr-form-actions">
              <button type="button" class="btn-ghost" @click="editing = null">انصراف</button>
              <button type="submit" class="save-btn">ذخیره آدرس</button>
            </div>
          </form>
        </div>

        <!-- Address List -->
        <div v-else>
          <div class="pane-header pane-header--row">
            <div>
              <h2 class="pane-title">آدرس‌های ذخیره‌شده</h2>
              <p class="pane-sub">{{ toFa(accountStore.addresses.length) }} آدرس</p>
            </div>
            <button type="button" class="add-addr-btn" @click="startEdit('new')">
              <Plus class="h-4 w-4" /> آدرس جدید
            </button>
          </div>

          <div v-if="accountStore.addresses.length === 0" class="acct-empty">
            <MapPin class="acct-empty__icon" />
            <p class="acct-empty__text">هنوز آدرسی ثبت نشده است.</p>
            <button type="button" class="acct-empty__cta" @click="startEdit('new')">افزودن آدرس</button>
          </div>

          <div v-else class="addr-grid">
            <div
              v-for="addr in accountStore.addresses" :key="addr.id"
              class="addr-card"
              :class="addr.isDefault ? 'addr-card--default' : ''"
            >
              <!-- Mini map if coords exist -->
              <div v-if="addr.coords" class="addr-card__map-wrap">
                <AddrMiniMap :coords="addr.coords" />
              </div>

              <div class="addr-card__body">
                <div class="addr-card__top">
                  <div class="addr-card__label-row">
                    <span class="addr-card__label">{{ addr.label || 'آدرس' }}</span>
                    <span v-if="addr.isDefault" class="addr-default-badge">پیش‌فرض</span>
                  </div>
                  <div class="addr-card__actions">
                    <button type="button" class="addr-action-btn" @click="startEdit(addr)" title="ویرایش">
                      <Edit2 class="h-3.5 w-3.5" />
                    </button>
                    <button type="button" class="addr-action-btn addr-action-btn--del"
                      @click="accountStore.removeAddress(addr.id)" title="حذف">
                      <Trash2 class="h-3.5 w-3.5" />
                    </button>
                  </div>
                </div>

                <div v-if="addr.fullName" class="addr-card__name">{{ addr.fullName }}</div>
                <div class="addr-card__text">
                  {{ [addr.province, addr.city, addr.street].filter(Boolean).join('، ') }}
                </div>
                <div v-if="addr.postalCode" class="addr-card__postal">
                  کد پستی: {{ addr.postalCode }}
                </div>
                <div v-if="addr.phone" class="addr-card__phone">{{ addr.phone }}</div>

                <div v-if="addr.coords" class="addr-card__coords">
                  <MapPin class="h-3 w-3" />
                  {{ addr.coords[0].toFixed(4) }}, {{ addr.coords[1].toFixed(4) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </TheLayout>
</template>

<style scoped>
/* ── Banner ── */
.acct-banner {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2a28 100%);
  color: #fff;
  border-bottom: 1px solid #3a3530;
}
.acct-banner__inner {
  max-width: 900px;
  margin: 0 auto;
  padding: 2.5rem 5vw;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}
.acct-avatar {
  width: 60px; height: 60px;
  background: #F0EDE8;
  color: #1a1a1a;
  border-radius: 0;
  display: flex; align-items: center; justify-content: center;
  font-family: 'Vazirmatn', sans-serif;
  font-size: 1.2rem; font-weight: 500;
  flex-shrink: 0;
}
.acct-banner__info { flex: 1; min-width: 160px; }
.acct-banner__greeting { font-family: 'Vazirmatn', sans-serif; font-size: 0.72rem; color: #9e9890; letter-spacing: 0.1em; }
.acct-banner__name { font-family: 'Vazirmatn', sans-serif; font-size: 1.5rem; font-weight: 300; margin: 0.2rem 0 0; }
.acct-banner__email { font-family: 'Vazirmatn', sans-serif; font-size: 0.78rem; color: #9e9890; margin-top: 0.15rem; direction: ltr; text-align: right; }

.acct-stats { display: flex; align-items: center; gap: 0; }
.acct-stat { text-align: center; padding: 0 1.5rem; }
.acct-stat--sep { width: 1px; height: 36px; background: #3a3530; padding: 0; flex-shrink: 0; }
.acct-stat__val { font-family: 'Vazirmatn', sans-serif; font-size: 1.2rem; font-weight: 400; color: #F0EDE8; }
.acct-stat__val--accent { color: #c8c2ba; }
.acct-stat__lbl { font-family: 'Vazirmatn', sans-serif; font-size: 0.65rem; color: #6b6560; margin-top: 0.15rem; white-space: nowrap; }

/* ── Tab Bar ── */
.acct-tabbar {
  background: #FAFAF8;
  border-bottom: 1px solid #E8E4DE;
  position: sticky;
  top: 0;
  z-index: 10;
}
.acct-tabbar__inner {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 5vw;
  display: flex;
  align-items: stretch;
}
.acct-tab {
  display: inline-flex; align-items: center; gap: 0.45rem;
  padding: 0.9rem 1.25rem;
  font-family: 'Vazirmatn', sans-serif; font-size: 0.82rem;
  color: #9e9890; background: none; border: none; cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: color 0.2s, border-color 0.2s;
  text-decoration: none; white-space: nowrap;
}
.acct-tab:hover { color: #3f3a36; }
.acct-tab--active { color: #1a1a1a; border-bottom-color: #800000; }
.acct-tab--appearance { margin-right: auto; font-size: 0.75rem; color: #9e9890; }
.acct-tab--appearance:hover { color: #1a1a1a; }
.acct-tab--back { font-size: 0.75rem; color: #C8C2BA; }
.acct-tab--back:hover { color: #6b6560; }
.acct-tab__icon { width: 15px; height: 15px; flex-shrink: 0; }

/* ── Content ── */
.acct-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 2.5rem 5vw 5rem;
}

/* ── Wishlist grid ── */
.wishlist-account-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem 1rem;
  padding-bottom: 1rem;
}
@media (max-width: 768px) {
  .wishlist-account-grid { grid-template-columns: repeat(2, 1fr); }
}

/* ── Empty state ── */
.acct-empty {
  text-align: center;
  padding: 4rem 1rem;
  border: 1px dashed #E8E4DE;
}
.acct-empty__icon { width: 40px; height: 40px; color: #C8C2BA; margin: 0 auto 1rem; }
.acct-empty__text { font-family: 'Vazirmatn', sans-serif; font-size: 0.9rem; color: #9e9890; }
.acct-empty__cta {
  display: inline-block; margin-top: 1rem;
  font-family: 'Vazirmatn', sans-serif; font-size: 0.82rem;
  color: #1a1a1a; border-bottom: 1px solid #1a1a1a;
  text-decoration: none; padding-bottom: 1px;
  background: none; border-top: none; border-left: none; border-right: none;
  cursor: pointer;
}

/* ── Orders ── */
.orders-list { display: flex; flex-direction: column; gap: 0; border: 1px solid #E8E4DE; }
.order-card { border-bottom: 1px solid #E8E4DE; background: #fff; }
.order-card:last-child { border-bottom: none; }

.order-card__head {
  display: flex; align-items: center; gap: 1rem;
  padding: 1.1rem 1.25rem; cursor: pointer;
  transition: background 0.15s;
}
.order-card__head:hover { background: #FAFAF8; }

.order-card__id-block { min-width: 100px; }
.order-card__id { font-family: 'Vazirmatn', sans-serif; font-size: 0.85rem; font-weight: 500; color: #1a1a1a; direction: ltr; text-align: right; }
.order-card__date { font-family: 'Vazirmatn', sans-serif; font-size: 0.72rem; color: #9e9890; margin-top: 0.15rem; }

.order-card__middle { display: flex; align-items: center; gap: 0.75rem; flex: 1; }
.order-status-pill {
  display: inline-flex; align-items: center; gap: 0.35rem;
  padding: 0.25rem 0.7rem;
  font-family: 'Vazirmatn', sans-serif; font-size: 0.72rem; font-weight: 400;
  border-radius: 2px;
}
.order-status-pill__dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.order-card__items-count { font-family: 'Vazirmatn', sans-serif; font-size: 0.72rem; color: #9e9890; }

.order-card__right { display: flex; align-items: center; gap: 0.75rem; margin-right: auto; }
.order-card__price { font-family: 'Vazirmatn', sans-serif; font-size: 0.9rem; color: #1a1a1a; }
.order-card__price span { font-size: 0.7rem; color: #9e9890; }
.order-card__chevron { width: 16px; height: 16px; color: #9e9890; transition: transform 0.2s; }
.order-card__chevron--open { transform: rotate(180deg); }

.order-card__body { background: #FAFAF8; border-top: 1px solid #E8E4DE; padding: 1.25rem; }

.order-items { display: flex; flex-direction: column; gap: 0.65rem; margin-bottom: 1rem; }
.order-item { display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
.order-item__name { font-family: 'Vazirmatn', sans-serif; font-size: 0.85rem; color: #1a1a1a; }
.order-item__meta { font-family: 'Vazirmatn', sans-serif; font-size: 0.72rem; color: #9e9890; margin-top: 0.1rem; }
.order-item__price { font-family: 'Vazirmatn', sans-serif; font-size: 0.82rem; color: #3f3a36; white-space: nowrap; }

.order-card__footer-row { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; border-top: 1px solid #E8E4DE; padding-top: 0.85rem; flex-wrap: wrap; }
.order-card__address { display: flex; align-items: flex-start; gap: 0.4rem; font-family: 'Vazirmatn', sans-serif; font-size: 0.75rem; color: #9e9890; }
.order-card__address-icon { width: 12px; height: 12px; margin-top: 1px; flex-shrink: 0; }
.order-card__tracking { font-family: 'Vazirmatn', sans-serif; font-size: 0.75rem; color: #6b6560; }
.order-card__tracking-code { font-family: 'Vazirmatn', sans-serif; font-size: 0.75rem; color: #1a1a1a; font-weight: 500; direction: ltr; display: inline-block; }

/* ── Profile ── */
.pane-header { margin-bottom: 2rem; }
.pane-header--row { display: flex; align-items: flex-end; justify-content: space-between; flex-wrap: wrap; gap: 1rem; }
.pane-back {
  display: inline-flex; align-items: center; gap: 0.35rem;
  font-family: 'Vazirmatn', sans-serif; font-size: 0.78rem; color: #9e9890;
  background: none; border: none; cursor: pointer; padding: 0; margin-bottom: 0.85rem;
  transition: color 0.2s;
}
.pane-back:hover { color: #1a1a1a; }
.pane-title { font-family: 'Vazirmatn', sans-serif; font-size: 1.3rem; font-weight: 300; color: #1a1a1a; margin: 0; }
.pane-sub { font-family: 'Vazirmatn', sans-serif; font-size: 0.78rem; color: #9e9890; margin-top: 0.25rem; }

.profile-pane { max-width: 560px; }
.profile-form__avatar-row { display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem; padding-bottom: 1.5rem; border-bottom: 1px solid #E8E4DE; }
.profile-form__avatar { width: 52px; height: 52px; background: #1a1a1a; color: #F0EDE8; display: flex; align-items: center; justify-content: center; font-family: 'Vazirmatn', sans-serif; font-size: 1.1rem; flex-shrink: 0; }
.profile-form__avatar-name { font-family: 'Vazirmatn', sans-serif; font-size: 0.9rem; font-weight: 500; color: #1a1a1a; }
.profile-form__avatar-hint { font-family: 'Vazirmatn', sans-serif; font-size: 0.72rem; color: #9e9890; margin-top: 0.15rem; }

/* ── Form shared ── */
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.form-field { display: flex; flex-direction: column; gap: 0.4rem; }
.form-field--full { grid-column: 1 / -1; }
.form-label { font-family: 'Vazirmatn', sans-serif; font-size: 0.7rem; letter-spacing: 0.08em; color: #9e9890; }
.form-input {
  border: 1px solid #E8E4DE;
  background: #fff;
  padding: 0.65rem 0.85rem;
  font-family: 'Vazirmatn', sans-serif;
  font-size: 0.85rem;
  color: #1a1a1a;
  outline: none;
  transition: border-color 0.2s;
}
.form-input:focus { border-color: #3f3a36; }
.form-input--textarea { resize: vertical; min-height: 90px; }
.form-input::placeholder { color: #C8C2BA; }

.form-section { margin-top: 1.5rem; padding-top: 1.25rem; border-top: 1px solid #E8E4DE; grid-column: 1 / -1; }
.form-section__title { display: flex; align-items: center; gap: 0.4rem; font-family: 'Vazirmatn', sans-serif; font-size: 0.8rem; font-weight: 500; color: #3f3a36; margin-bottom: 0.35rem; }
.form-section__hint { font-family: 'Vazirmatn', sans-serif; font-size: 0.75rem; color: #9e9890; margin-bottom: 0.85rem; }

/* ── Buttons ── */
.save-btn {
  display: inline-flex; align-items: center; gap: 0.5rem;
  margin-top: 1.75rem;
  padding: 0.7rem 1.75rem;
  background: #1a1a1a; color: #F0EDE8;
  font-family: 'Vazirmatn', sans-serif; font-size: 0.85rem;
  border: none; cursor: pointer;
  transition: background 0.2s;
}
.save-btn:hover { background: #2d2a28; }
.save-btn__icon { width: 15px; height: 15px; }

.btn-ghost {
  padding: 0.7rem 1.5rem;
  border: 1px solid #E8E4DE; background: #fff;
  font-family: 'Vazirmatn', sans-serif; font-size: 0.85rem; color: #3f3a36;
  cursor: pointer; transition: background 0.2s;
}
.btn-ghost:hover { background: #F5F3F0; }

.addr-form-actions { display: flex; gap: 0.75rem; margin-top: 1.75rem; }
.addr-form-actions .save-btn { margin-top: 0; flex: 1; justify-content: center; }

/* ── Address label chips ── */
.addr-label-chips { display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }
.addr-chips { display: flex; gap: 0.4rem; }
.addr-chip {
  padding: 0.35rem 0.85rem;
  border: 1px solid #E8E4DE; background: #fff;
  font-family: 'Vazirmatn', sans-serif; font-size: 0.8rem; color: #6b6560;
  cursor: pointer; transition: all 0.15s;
}
.addr-chip:hover { border-color: #3f3a36; color: #1a1a1a; }
.addr-chip--active { border-color: #1a1a1a; background: #1a1a1a; color: #F0EDE8; }

/* ── Default checkbox ── */
.default-check { display: flex; align-items: center; gap: 0.65rem; cursor: pointer; margin-top: 1rem; }
.default-check__input { display: none; }
.default-check__box {
  width: 16px; height: 16px; border: 1.5px solid #E8E4DE; background: #fff;
  flex-shrink: 0; transition: all 0.15s; position: relative;
}
.default-check__box--on { border-color: #1a1a1a; background: #1a1a1a; }
.default-check__box--on::after {
  content: ''; position: absolute; top: 2px; right: 4px;
  width: 4px; height: 8px; border: 1.5px solid #fff;
  border-top: none; border-left: none; transform: rotate(45deg);
}
.default-check__label { font-family: 'Vazirmatn', sans-serif; font-size: 0.82rem; color: #5a5550; }

/* ── Add addr button ── */
.add-addr-btn {
  display: inline-flex; align-items: center; gap: 0.4rem;
  padding: 0.55rem 1.1rem;
  border: 1px solid #3f3a36; background: #fff;
  font-family: 'Vazirmatn', sans-serif; font-size: 0.82rem; color: #3f3a36;
  cursor: pointer; transition: all 0.15s; white-space: nowrap;
}
.add-addr-btn:hover { background: #1a1a1a; color: #F0EDE8; border-color: #1a1a1a; }

/* ── Address cards ── */
.addr-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1px; background: #E8E4DE; border: 1px solid #E8E4DE; }
.addr-card { background: #fff; display: flex; flex-direction: column; }
.addr-card--default { background: #FAFAF8; }

.addr-card__map-wrap { position: relative; }
.addr-card__map { height: 130px; pointer-events: none; }

.addr-card__body { padding: 1.1rem 1.1rem; flex: 1; }
.addr-card__top { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 0.65rem; }
.addr-card__label-row { display: flex; align-items: center; gap: 0.5rem; }
.addr-card__label { font-family: 'Vazirmatn', sans-serif; font-size: 0.85rem; font-weight: 500; color: #1a1a1a; }
.addr-default-badge {
  font-family: 'Vazirmatn', sans-serif; font-size: 0.65rem;
  background: #f5f0e8; color: #7a5c00;
  padding: 0.1rem 0.45rem; border-radius: 2px;
}
.addr-card__actions { display: flex; gap: 0.2rem; }
.addr-action-btn {
  padding: 0.3rem; background: none; border: none; cursor: pointer;
  color: #C8C2BA; transition: color 0.15s;
}
.addr-action-btn:hover { color: #3f3a36; }
.addr-action-btn--del:hover { color: #800000; }

.addr-card__name { font-family: 'Vazirmatn', sans-serif; font-size: 0.82rem; color: #1a1a1a; margin-bottom: 0.3rem; }
.addr-card__text { font-family: 'Vazirmatn', sans-serif; font-size: 0.78rem; color: #6b6560; line-height: 1.6; }
.addr-card__postal { font-family: 'Vazirmatn', sans-serif; font-size: 0.72rem; color: #9e9890; margin-top: 0.3rem; direction: ltr; text-align: right; }
.addr-card__phone { font-family: 'Vazirmatn', sans-serif; font-size: 0.72rem; color: #9e9890; margin-top: 0.2rem; }
.addr-card__coords {
  display: flex; align-items: center; gap: 0.25rem; margin-top: 0.5rem;
  font-family: 'Vazirmatn', sans-serif; font-size: 0.68rem; color: #C8C2BA; direction: ltr; justify-content: flex-end;
}

/* ── Wallet ── */
.wallet-pane { }
.wallet-balance-card {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2a28 100%);
  color: #fff; padding: 2rem 2rem; margin-bottom: 1.5rem;
  display: flex; flex-direction: column; gap: 0.5rem;
}
.wallet-balance-card__label { font-family: 'Vazirmatn', sans-serif; font-size: 0.72rem; color: #9e9890; letter-spacing: 0.1em; }
.wallet-balance-card__amount { font-family: 'Vazirmatn', sans-serif; font-size: 2rem; font-weight: 300; color: #F0EDE8; }
.wallet-balance-card__amount span { font-size: 0.9rem; color: #9e9890; }
.wallet-charge-box { border: 1px solid #E8E4DE; padding: 1.5rem; margin-bottom: 2rem; }
.wallet-charge-box__title { font-family: 'Vazirmatn', sans-serif; font-size: 0.85rem; font-weight: 500; color: #1a1a1a; margin-bottom: 1rem; }
.wallet-charge-presets { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem; }
.wallet-preset-btn {
  border: 1px solid #E8E4DE; padding: 0.4rem 0.85rem;
  font-family: 'Vazirmatn', sans-serif; font-size: 0.78rem; color: #3f3a36;
  background: none; cursor: pointer; transition: border-color 0.15s, color 0.15s;
}
.wallet-preset-btn:hover { border-color: #800000; color: #800000; }
.wallet-charge-row { display: flex; gap: 0.75rem; align-items: stretch; }
.wallet-charge-hint { font-family: 'Vazirmatn', sans-serif; font-size: 0.72rem; color: #9e9890; margin-top: 0.5rem; }
.wallet-txns { }
.wallet-txns__title { font-family: 'Vazirmatn', sans-serif; font-size: 0.78rem; letter-spacing: 0.1em; color: #9e9890; margin-bottom: 1rem; }
.wallet-txn-list { border: 1px solid #E8E4DE; }
.wallet-txn { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 0.9rem 1.25rem; border-bottom: 1px solid #E8E4DE; }
.wallet-txn:last-child { border-bottom: none; }
.wallet-txn__desc { font-family: 'Vazirmatn', sans-serif; font-size: 0.85rem; color: #1a1a1a; }
.wallet-txn__date { font-family: 'Vazirmatn', sans-serif; font-size: 0.72rem; color: #9e9890; margin-top: 0.15rem; }
.wallet-txn__amount { font-family: 'Vazirmatn', sans-serif; font-size: 0.9rem; font-weight: 500; white-space: nowrap; }

/* ── Returns ── */
.return-form-card { border: 1px solid #E8E4DE; padding: 1.5rem; margin-bottom: 1.5rem; }
.return-form-card__title { font-family: 'Vazirmatn', sans-serif; font-size: 0.85rem; font-weight: 500; color: #1a1a1a; margin-bottom: 1rem; }
.return-success { background: #f0fdf4; border: 1px solid #bbf7d0; color: #14532d; padding: 0.85rem 1rem; font-family: 'Vazirmatn', sans-serif; font-size: 0.82rem; margin-top: 0.75rem; }
.returns-list { }
.return-item { border: 1px solid #E8E4DE; padding: 1rem 1.25rem; margin-bottom: 0.5rem; background: #fff; }
.return-item__head { display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; }
.return-item__id { font-family: 'Vazirmatn', sans-serif; font-size: 0.85rem; font-weight: 500; color: #1a1a1a; direction: ltr; text-align: right; }
.return-item__date { font-family: 'Vazirmatn', sans-serif; font-size: 0.72rem; color: #9e9890; margin-top: 0.15rem; }
.return-status { font-family: 'Vazirmatn', sans-serif; font-size: 0.75rem; padding: 0.25rem 0.65rem; white-space: nowrap; }
.return-item__note { font-family: 'Vazirmatn', sans-serif; font-size: 0.78rem; color: #6b6560; margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #E8E4DE; }
.notifs-actions { display: flex; gap: 0.5rem; flex-wrap: wrap; }

/* ── Notifications ── */
.notifs-list { border: 1px solid #E8E4DE; }
.notif-item {
  display: flex; align-items: flex-start; gap: 0.75rem;
  padding: 1rem 1.25rem; border-bottom: 1px solid #E8E4DE; cursor: pointer;
  transition: background 0.15s;
}
.notif-item:last-child { border-bottom: none; }
.notif-item:hover { background: #FAFAF8; }
.notif-item--unread { background: rgba(128,0,0,0.03); }
.notif-item__icon { font-size: 1.2rem; flex-shrink: 0; line-height: 1; padding-top: 2px; }
.notif-item__body { flex: 1; min-width: 0; }
.notif-item__title { font-family: 'Vazirmatn', sans-serif; font-size: 0.85rem; font-weight: 500; color: #1a1a1a; }
.notif-item--unread .notif-item__title { color: #800000; }
.notif-item__text { font-family: 'Vazirmatn', sans-serif; font-size: 0.78rem; color: #6b6560; margin-top: 0.2rem; line-height: 1.6; }
.notif-item__date { font-family: 'Vazirmatn', sans-serif; font-size: 0.68rem; color: #9e9890; margin-top: 0.3rem; }
.notif-item__del { background: none; border: none; cursor: pointer; color: #C8C2BA; padding: 2px; display: flex; flex-shrink: 0; }
.notif-item__del:hover { color: #dc2626; }

/* ── Responsive ── */
@media (max-width: 640px) {
  .acct-banner__inner { flex-direction: column; align-items: flex-start; }
  .acct-stats { margin-top: 0.5rem; }
  .form-grid { grid-template-columns: 1fr; }
  .form-field--full { grid-column: 1; }
  .addr-grid { grid-template-columns: 1fr; }
  .wallet-charge-row { flex-direction: column; }
}
</style>
