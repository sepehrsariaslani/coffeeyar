import { watchEffect, isRef } from "vue";

function resolve(v) {
  if (isRef(v)) return v.value;
  if (typeof v === "function") return v();
  return v;
}

function setMeta(attr, key, content) {
  if (!content) return;
  let el = document.querySelector(`meta[${attr}="${key}"]`);
  if (!el) {
    el = document.createElement("meta");
    el.setAttribute(attr, key);
    document.head.appendChild(el);
  }
  el.setAttribute("content", content);
}

export function useSeo(options = {}) {
  watchEffect(() => {
    const title = resolve(options.title);
    const description = resolve(options.description);
    const image = resolve(options.image);
    const type = resolve(options.type) || "website";

    if (title) {
      document.title = title.includes("نوار") ? title : `${title} — نوار`;
    }

    setMeta("name", "description", description);
    setMeta("name", "robots", "index, follow");
    setMeta("property", "og:title", title ? (title.includes("نوار") ? title : `${title} — نوار`) : undefined);
    setMeta("property", "og:description", description);
    setMeta("property", "og:type", type);
    setMeta("property", "og:site_name", "نوار — قهوه تخصصی");
    if (image) setMeta("property", "og:image", image);
    setMeta("name", "twitter:card", "summary_large_image");
    setMeta("name", "twitter:title", title);
    setMeta("name", "twitter:description", description);
  });
}
