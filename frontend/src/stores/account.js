import { defineStore } from "pinia";
import { ref } from "vue";

export const STATUS_COLOR = {
  "در حال پردازش": "text-amber-600 bg-amber-50",
  "تایید شده": "text-blue-600 bg-blue-50",
  "در حال ارسال": "text-purple-600 bg-purple-50",
  "تحویل داده شده": "text-green-600 bg-green-50",
  "لغو شده": "text-red-600 bg-red-50",
};

const PROFILE_KEY = "navar_profile";
const ADDRESSES_KEY = "navar_addresses";
const ORDERS_KEY = "navar_orders";

const mockOrders = [
  {
    id: "ORD-۱۰۰۱",
    date: "۱۴۰۳/۰۲/۱۵",
    status: "تحویل داده شده",
    items: [
      {
        productId: "ethiopia-yirgacheffe",
        name: "اتیوپی یرگاچف",
        image: "",
        weight: "۲۵۰ گرم",
        grind: "V60",
        unitPrice: 480000,
        qty: 1,
      },
    ],
    totalPrice: 480000,
    address: "تهران، خیابان ولیعصر، پلاک ۴۲",
    trackingCode: "RH۱۲۳۴۵۶۷",
  },
  {
    id: "ORD-۱۰۰۲",
    date: "۱۴۰۳/۰۳/۰۸",
    status: "در حال ارسال",
    items: [
      {
        productId: "colombia-huila",
        name: "کلمبیا هویلا",
        image: "",
        weight: "۵۰۰ گرم",
        grind: "فرنچ پرس",
        unitPrice: 420000 * 1.9,
        qty: 1,
      },
      {
        productId: "ethiopia-yirgacheffe",
        name: "اتیوپی یرگاچف",
        image: "",
        weight: "۲۵۰ گرم",
        grind: "دانه کامل",
        unitPrice: 480000,
        qty: 2,
      },
    ],
    totalPrice: 420000 * 1.9 + 480000 * 2,
    address: "تهران، خیابان ولیعصر، پلاک ۴۲",
    trackingCode: "RH۷۶۵۴۳۲۱",
  },
  {
    id: "ORD-۱۰۰۳",
    date: "۱۴۰۳/۰۳/۲۴",
    status: "در حال پردازش",
    items: [
      {
        productId: "kenya-aa",
        name: "کنیا AA",
        image: "",
        weight: "۱ کیلوگرم",
        grind: "اسپرسو",
        unitPrice: 540000 * 3.5,
        qty: 1,
      },
    ],
    totalPrice: 540000 * 3.5,
    address: "تهران، خیابان ولیعصر، پلاک ۴۲",
  },
];

const defaultAddresses = [
  {
    id: "addr-1",
    label: "خانه",
    fullName: "",
    phone: "",
    province: "تهران",
    city: "تهران",
    street: "",
    postalCode: "",
    isDefault: true,
  },
];

function load(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

function save(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch {}
}

export const useAccountStore = defineStore("account", () => {
  const profile = ref(load(PROFILE_KEY, { name: "", email: "", phone: "" }));
  const addresses = ref(load(ADDRESSES_KEY, defaultAddresses));
  const orders = ref(load(ORDERS_KEY, mockOrders));

  function updateProfile(patch) {
    profile.value = { ...profile.value, ...patch };
    save(PROFILE_KEY, profile.value);
  }

  function addAddress(addr) {
    const newAddr = { ...addr, id: Date.now().toString() };
    if (addr.isDefault) {
      addresses.value = addresses.value.map((a) => ({ ...a, isDefault: false }));
    }
    addresses.value.push(newAddr);
    save(ADDRESSES_KEY, addresses.value);
  }

  function updateAddress(addr) {
    if (addr.isDefault) {
      addresses.value = addresses.value.map((a) => ({
        ...a,
        isDefault: a.id === addr.id,
      }));
    } else {
      const idx = addresses.value.findIndex((a) => a.id === addr.id);
      if (idx !== -1) addresses.value[idx] = addr;
    }
    save(ADDRESSES_KEY, addresses.value);
  }

  function removeAddress(id) {
    addresses.value = addresses.value.filter((a) => a.id !== id);
    save(ADDRESSES_KEY, addresses.value);
  }

  return { profile, addresses, orders, updateProfile, addAddress, updateAddress, removeAddress };
});
