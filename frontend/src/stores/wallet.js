import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { api } from "@/lib/api.js";
import { useAuthStore } from "./auth.js";
import { useNotificationsStore } from "./notifications.js";

/**
 * Wallet store — backed by the Frappe `Customer Wallet` doctype.
 * Balance and transactions are persisted server-side per user.
 */
export const useWalletStore = defineStore("wallet", () => {
  const balance = ref(0);
  const transactions = ref([]);
  const loading = ref(false);
  const loaded = ref(false);

  const formattedBalance = computed(() =>
    Number(balance.value).toLocaleString("fa-IR") + " تومان"
  );

  /**
   * Load the wallet (balance + transactions) from the server.
   * @param {boolean} [force=false] Re-fetch even if already loaded.
   * @returns {Promise<void>}
   */
  async function fetchWallet(force = false) {
    const auth = useAuthStore();
    if (!auth.isLoggedIn) return;
    if (loaded.value && !force) return;
    loading.value = true;
    try {
      const res = await api.wallet.get();
      balance.value = res.balance || 0;
      transactions.value = (res.transactions || []).map(normalizeTxn);
      loaded.value = true;
    } catch (e) {
      console.error("خطا در دریافت کیف پول:", e.message);
    } finally {
      loading.value = false;
    }
  }

  /**
   * Charge the wallet by a positive amount.
   * @param {number} amount Toman amount to add.
   * @param {string} [description] Optional label for the transaction.
   * @returns {Promise<boolean>} Whether the charge succeeded.
   */
  async function charge(amount, description = "شارژ کیف پول") {
    try {
      const res = await api.wallet.charge(amount, description);
      balance.value = res.balance ?? balance.value + amount;
      await fetchWallet(true);
      try {
        const notif = useNotificationsStore();
        await notif.refresh();
      } catch {}
      return true;
    } catch (e) {
      console.error("خطا در شارژ کیف پول:", e.message);
      return false;
    }
  }

  /**
   * Spend from the wallet (e.g. paying for an order).
   * @param {number} amount Toman amount to deduct.
   * @param {string} [description] Optional label for the transaction.
   * @returns {Promise<boolean>} Whether the spend succeeded (false if insufficient funds).
   */
  async function spend(amount, description = "پرداخت سفارش") {
    if (balance.value < amount) return false;
    try {
      const res = await api.wallet.spend(amount, description);
      balance.value = res.balance ?? balance.value - amount;
      await fetchWallet(true);
      return true;
    } catch (e) {
      console.error("خطا در پرداخت از کیف پول:", e.message);
      return false;
    }
  }

  return { balance, transactions, loading, loaded, formattedBalance, fetchWallet, charge, spend };
});

/**
 * Normalize a raw wallet transaction into the UI shape.
 * @param {object} t Raw transaction from the API.
 * @returns {object} Normalized transaction.
 */
function normalizeTxn(t) {
  const d = t.datetime ? new Date(t.datetime) : new Date();
  return {
    id: t.id,
    type: t.type,
    amount: Number(t.amount || 0),
    description: t.description || "",
    date: d.toLocaleDateString("fa-IR"),
    time: d.toLocaleTimeString("fa-IR"),
  };
}
