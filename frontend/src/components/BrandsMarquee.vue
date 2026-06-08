<script setup>
const brands = [
  { name: "Tim Wendelboe", country: "نروژ" },
  { name: "Square Mile", country: "انگلستان" },
  { name: "Onyx Coffee Lab", country: "آمریکا" },
  { name: "Intelligentsia", country: "آمریکا" },
  { name: "کافه کتاب", country: "تهران" },
  { name: "Counter Culture", country: "آمریکا" },
  { name: "قهوه آریا", country: "تهران" },
  { name: "Koppi Roasters", country: "سوئد" },
  { name: "قهوه سپید", country: "اصفهان" },
  { name: "Heart Coffee", country: "پورتلند" },
  { name: "کافه نگار", country: "مشهد" },
  { name: "Fuglen Coffee", country: "اسلو" },
];
</script>

<template>
  <section class="border-b border-border overflow-hidden py-6 bg-muted/30">
    <div class="mb-4 px-[5vw]">
      <span class="text-xs uppercase tracking-[0.3em] text-maroon/70">برندهایی که با ما هستند</span>
    </div>
    <div class="marquee-track">
      <div class="marquee-inner">
        <div
          v-for="(b, i) in [...brands, ...brands]"
          :key="i"
          class="marquee-item"
        >
          <div class="text-sm font-medium leading-tight">{{ b.name }}</div>
          <div class="mt-0.5 text-[10px] text-muted-foreground tracking-wider uppercase">{{ b.country }}</div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.marquee-track {
  overflow: hidden;
  -webkit-mask-image: linear-gradient(to left, transparent 0%, black 10%, black 90%, transparent 100%);
  mask-image: linear-gradient(to left, transparent 0%, black 10%, black 90%, transparent 100%);
}

.marquee-inner {
  display: flex;
  width: max-content;
  animation: marquee-rtl 40s linear infinite;
}

.marquee-inner:hover {
  animation-play-state: paused;
}

.marquee-item {
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 160px;
  padding: 0.75rem 2rem;
  border-left: 1px solid var(--border);
  cursor: default;
  transition: background-color 0.2s;
}

.marquee-item:hover {
  background-color: color-mix(in srgb, var(--maroon) 4%, transparent);
}

@keyframes marquee-rtl {
  0%   { transform: translateX(0); }
  100% { transform: translateX(50%); }
}
</style>
