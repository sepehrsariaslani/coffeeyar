<script setup>
defineProps({
  /** Loader size: sm | md | lg. */
  size: { type: String, default: "md" },
  /** Optional caption shown under the cup. Pass empty string to hide. */
  text: { type: String, default: "در حال بارگذاری..." },
  /**
   * Visual style of the loader:
   * - "cup"  : pulsing cup with rising steam + crema wave (default)
   * - "pour" : coffee pouring into a filling cup
   * - "beans": three coffee beans bouncing in sequence
   */
  variant: { type: String, default: "cup" },
});
</script>

<template>
  <div class="coffee-loader" :class="[`coffee-loader--${size}`, `coffee-loader--${variant}`]">
    <!-- ── Variant: Cup ─────────────────────────────── -->
    <div v-if="variant === 'cup'" class="coffee-loader__cup">
      <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M14 12l2-6M22 12l2-6M30 12l2-6M38 12l2-6" class="steam" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
        <rect x="8" y="16" width="44" height="34" rx="4" class="cup-body" stroke="currentColor" stroke-width="2.5" fill="none" />
        <clipPath id="cupClip"><rect x="11" y="19" width="38" height="28" rx="2" /></clipPath>
        <g clip-path="url(#cupClip)">
          <rect x="11" y="19" width="38" height="28" class="cup-fill" fill="currentColor" opacity="0.15" />
          <path class="cup-liquid" fill="currentColor" opacity="0.9" d="M11 34 q9.5 -6 19 0 t19 0 V47 H11 Z" />
        </g>
        <path d="M52 24h4a4 4 0 0 1 0 8h-4" class="cup-handle" stroke="currentColor" stroke-width="2.5" fill="none" />
        <ellipse cx="30" cy="52" rx="22" ry="3" class="cup-shadow" fill="currentColor" opacity="0.08" />
      </svg>
    </div>

    <!-- ── Variant: Pour ────────────────────────────── -->
    <div v-else-if="variant === 'pour'" class="coffee-loader__cup">
      <svg viewBox="0 0 64 72" fill="none" xmlns="http://www.w3.org/2000/svg">
        <!-- pouring stream -->
        <rect x="30.5" y="6" width="3" height="22" rx="1.5" class="pour-stream" fill="currentColor" />
        <!-- cup -->
        <rect x="10" y="30" width="40" height="30" rx="4" class="cup-body" stroke="currentColor" stroke-width="2.5" fill="none" />
        <clipPath id="pourClip"><rect x="13" y="33" width="34" height="24" rx="2" /></clipPath>
        <g clip-path="url(#pourClip)">
          <rect x="13" class="pour-fill" width="34" height="24" fill="currentColor" opacity="0.85" />
        </g>
        <path d="M50 38h4a4 4 0 0 1 0 8h-4" class="cup-handle" stroke="currentColor" stroke-width="2.5" fill="none" />
        <ellipse cx="30" cy="62" rx="20" ry="3" fill="currentColor" opacity="0.08" />
      </svg>
    </div>

    <!-- ── Variant: Beans ───────────────────────────── -->
    <div v-else class="coffee-loader__beans">
      <span class="bean"></span>
      <span class="bean"></span>
      <span class="bean"></span>
    </div>

    <p v-if="text" class="coffee-loader__text">{{ text }}</p>
  </div>
</template>

<style scoped>
.coffee-loader {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  color: var(--maroon, #7A2232);
}

/* ── Cup / Pour shared sizing ── */
.coffee-loader__cup {
  position: relative;
  width: 52px;
  height: 56px;
}
.coffee-loader--sm .coffee-loader__cup { width: 36px; height: 40px; }
.coffee-loader--lg .coffee-loader__cup { width: 80px; height: 86px; }
.coffee-loader__cup svg { width: 100%; height: 100%; overflow: visible; }

/* ── Steam ── */
.steam {
  animation: steamRise 2s ease-out infinite;
  transform-origin: center;
  opacity: 0;
}
.steam { stroke-dasharray: 1; }
@keyframes steamRise {
  0%   { opacity: 0; transform: translateY(2px); }
  35%  { opacity: 0.55; }
  100% { opacity: 0; transform: translateY(-7px); }
}

/* ── Cup body subtle pulse ── */
.cup-body { animation: cupPulse 2s ease-in-out infinite; }
@keyframes cupPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.65; }
}

/* ── Liquid wave (cup variant) ── */
.cup-liquid {
  animation: waveMove 1.6s linear infinite, liquidRise 2.6s ease-in-out infinite alternate;
}
@keyframes waveMove {
  0%   { transform: translateX(0); }
  100% { transform: translateX(-19px); }
}
@keyframes liquidRise {
  0%   { transform: translateY(6px); }
  100% { transform: translateY(0); }
}

/* ── Pour variant ── */
.pour-stream {
  transform-origin: top;
  animation: pourPulse 1.6s ease-in-out infinite;
}
@keyframes pourPulse {
  0%, 100% { transform: scaleY(0.4); opacity: 0.3; }
  50%      { transform: scaleY(1);   opacity: 1; }
}
.pour-fill {
  transform-origin: bottom;
  animation: fillUp 2.4s ease-in-out infinite;
}
@keyframes fillUp {
  0%   { transform: translateY(24px); }
  60%  { transform: translateY(2px); }
  80%  { transform: translateY(2px); }
  100% { transform: translateY(24px); }
}

/* ── Beans variant ── */
.coffee-loader__beans {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  height: 40px;
}
.coffee-loader--sm .coffee-loader__beans { height: 28px; gap: 0.35rem; }
.coffee-loader--lg .coffee-loader__beans { height: 56px; gap: 0.7rem; }
.bean {
  width: 14px;
  height: 18px;
  background: currentColor;
  border-radius: 50% / 60%;
  position: relative;
  transform: rotate(35deg);
  animation: beanBounce 0.9s ease-in-out infinite;
}
.coffee-loader--sm .bean { width: 10px; height: 13px; }
.coffee-loader--lg .bean { width: 20px; height: 26px; }
.bean::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(to right, transparent 46%, var(--background, #f9f6f1) 46%, var(--background, #f9f6f1) 54%, transparent 54%);
  opacity: 0.5;
}
.bean:nth-child(1) { animation-delay: 0s; }
.bean:nth-child(2) { animation-delay: 0.15s; }
.bean:nth-child(3) { animation-delay: 0.3s; }
@keyframes beanBounce {
  0%, 100% { transform: rotate(35deg) translateY(0); opacity: 0.5; }
  50%      { transform: rotate(35deg) translateY(-10px); opacity: 1; }
}

/* ── Caption ── */
.coffee-loader__text {
  font-family: "Vazirmatn", sans-serif;
  font-size: 0.8rem;
  opacity: 0.6;
  animation: textPulse 1.5s ease-in-out infinite;
}
.coffee-loader--sm .coffee-loader__text { font-size: 0.72rem; }
.coffee-loader--lg .coffee-loader__text { font-size: 0.9rem; }
@keyframes textPulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 0.3; }
}

@media (prefers-reduced-motion: reduce) {
  .steam, .cup-body, .cup-liquid, .pour-stream, .pour-fill, .bean, .coffee-loader__text {
    animation: none !important;
  }
}
</style>
