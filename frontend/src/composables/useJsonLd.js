import { watchEffect, onUnmounted, isRef } from "vue";

function resolve(v) {
  if (isRef(v)) return v.value;
  if (typeof v === "function") return v();
  return v;
}

export function useJsonLd(schemaFn) {
  let el = null;

  function inject() {
    const schema = resolve(schemaFn);
    if (!schema) return;
    if (!el) {
      el = document.createElement("script");
      el.setAttribute("type", "application/ld+json");
      document.head.appendChild(el);
    }
    el.textContent = JSON.stringify(schema);
  }

  function remove() {
    if (el && el.parentNode) {
      el.parentNode.removeChild(el);
      el = null;
    }
  }

  watchEffect(inject);
  onUnmounted(remove);
}
