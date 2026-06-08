import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useNotificationsStore } from "./notifications.js";

const BALANCE_KEY = "navar_wallet_balance_v1";
const TXN_KEY = "navar_wallet_txns_v1";

function load(key, fallback) {
  try { const r = localStorage.getItem(key); return r ? JSON.parse(r) : fallback; } catch { return fallback; }
}
function save(key, v) { localStorage.setItem(key, JSON.stringify(v)); }

export const useWalletStore = defineStore("wallet", () => {
  const balance = ref(load(BALANCE_KEY, 0));
  const transactions = ref(load(TXN_KEY, []));

  const formattedBalance = computed(() =>
    balance.value.toLocaleString("fa-IR") + " تومان"
  );

  function charge(amount, description = "شارژ کیف پول") {
    balance.value += amount;
    save(BALANCE_KEY, balance.value);
    _addTxn({ type: "charge", amount, description });
    try {
      const notif = useNotificationsStore();
      notif.add("کیف پول شما شارژ شد", `مبلغ ${amount.toLocaleString("fa-IR")} تومان به کیف پول شما اضافه شد.`, "wallet");
    } catch {}
  }

  function spend(amount, description = "پرداخت سفارش") {
    if (balance.value < amount) return false;
    balance.value -= amount;
    save(BALANCE_KEY, balance.value);
    _addTxn({ type: "spend", amount, description });
    return true;
  }

  function refund(amount, description = "بازگشت وجه") {
    balance.value += amount;
    save(BALANCE_KEY, balance.value);
    _addTxn({ type: "refund", amount, description });
    try {
      const notif = useNotificationsStore();
      notif.add("بازگشت وجه", `مبلغ ${amount.toLocaleString("fa-IR")} تومان به کیف پول شما بازگشت داده شد.`, "refund");
    } catch {}
  }

  function _addTxn(txn) {
    transactions.value.unshift({
      id: Date.now().toString(),
      ...txn,
      date: new Date().toLocaleDateString("fa-IR"),
      time: new Date().toLocaleTimeString("fa-IR"),
    });
    if (transactions.value.length > 100) transactions.value = transactions.value.slice(0, 100);
    save(TXN_KEY, transactions.value);
  }

  return { balance, transactions, formattedBalance, charge, spend, refund };
});
