<script setup>
defineProps({
  size: { type: String, default: "md" },
  text: { type: String, default: "در حال بارگذاری..." },
});
</script>

<template>
  <div class="coffee-loader" :class="`coffee-loader--${size}`">
    <div class="coffee-loader__cup">
      <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="8" y="16" width="44" height="34" rx="4" class="cup-body" stroke="currentColor" stroke-width="2.5" fill="none"/>
        <rect x="12" y="20" width="36" height="26" rx="2" class="cup-fill" fill="currentColor" opacity="0.12"/>
        <path d="M52 24h4a4 4 0 0 1 0 8h-4" class="cup-handle" stroke="currentColor" stroke-width="2.5" fill="none"/>
        <path d="M14 14l2-6M22 14l2-6M30 14l2-6M38 14l2-6" class="steam" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" opacity="0.5"/>
        <ellipse cx="30" cy="48" rx="22" ry="3" class="cup-shadow" fill="currentColor" opacity="0.08"/>
      </svg>
      <div class="coffee-loader__wave">
        <span></span><span></span><span></span>
      </div>
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

.coffee-loader__cup {
  position: relative;
  width: 48px;
  height: 48px;
}

.coffee-loader--sm .coffee-loader__cup { width: 32px; height: 32px; }
.coffee-loader--lg .coffee-loader__cup { width: 72px; height: 72px; }

.coffee-loader__cup svg {
  width: 100%;
  height: 100%;
}

.cup-body {
  animation: cupPulse 1.5s ease-in-out infinite;
}

@keyframes cupPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.steam {
  animation: steamRise 2s ease-out infinite;
  transform-origin: center;
}
.steam:nth-child(4) { animation-delay: 0s; }
.steam:nth-child(5) { animation-delay: 0.4s; }
.steam:nth-child(6) { animation-delay: 0.8s; }
.steam:nth-child(7) { animation-delay: 1.2s; }

@keyframes steamRise {
  0% { opacity: 0; transform: translateY(0); }
  30% { opacity: 0.5; }
  100% { opacity: 0; transform: translateY(-8px); }
}

.coffee-loader__wave {
  position: absolute;
  bottom: 6px;
  left: 12px;
  right: 12px;
  display: flex;
  gap: 3px;
  align-items: flex-end;
  height: 10px;
}

.coffee-loader__wave span {
  flex: 1;
  height: 100%;
  background: currentColor;
  border-radius: 2px;
  animation: waveBounce 0.8s ease-in-out infinite;
}

.coffee-loader__wave span:nth-child(1) { animation-delay: 0s; height: 40%; }
.coffee-loader__wave span:nth-child(2) { animation-delay: 0.15s; height: 70%; }
.coffee-loader__wave span:nth-child(3) { animation-delay: 0.3s; height: 100%; }

@keyframes waveBounce {
  0%, 100% { transform: scaleY(0.4); }
  50% { transform: scaleY(1); }
}

.coffee-loader__text {
  font-size: 0.8rem;
  opacity: 0.6;
  animation: textPulse 1.5s ease-in-out infinite;
}

@keyframes textPulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 0.3; }
}
</style>
