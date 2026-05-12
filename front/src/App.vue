<template>
  <div class="app-wrapper">
    <!-- 全局 CSS 黑色生命力背景 -->
    <div class="global-bg" aria-hidden="true">
      <!-- 1. 星云粒子系统 - 数百粒子构成旋转星云 -->
      <div class="nebula-layer"></div>

      <!-- 2. 能量光波 - 从底部涌动的生命能量 -->
      <div class="energy-wave wave-1"></div>
      <div class="energy-wave wave-2"></div>
      <div class="energy-wave wave-3"></div>

      <!-- 3. 呼吸光晕 - 深邃空间中的生命脉动 -->
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
      <div class="orb orb-3"></div>
      <div class="orb orb-4"></div>

      <!-- 4. 流动光河 -->
      <div class="light-river"></div>

      <!-- 5. 荆棘玫瑰 SVG 保留（作为点缀） -->
      <div class="rose-silhouette">
        <svg viewBox="0 0 400 500" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M200 500 C200 420 195 350 190 300 C185 250 180 220 175 200" stroke="rgba(255,255,255,0.03)"
            stroke-width="2" fill="none" stroke-linecap="round" />
          <path d="M170 195 C140 170 120 140 130 115 C140 90 165 95 175 120 C180 135 175 165 170 195Z"
            fill="rgba(255,255,255,0.02)" stroke="rgba(255,255,255,0.025)" stroke-width="0.5" />
          <path d="M175 195 C200 165 220 135 215 110 C210 85 185 90 178 115 C173 130 175 165 175 195Z"
            fill="rgba(255,255,255,0.02)" stroke="rgba(255,255,255,0.025)" stroke-width="0.5" />
          <path d="M172 190 C155 155 148 125 158 105 C168 85 185 95 182 118 C180 138 175 168 172 190Z"
            fill="rgba(255,255,255,0.025)" stroke="rgba(255,255,255,0.03)" stroke-width="0.5" />
          <path d="M178 190 C198 153 212 122 205 100 C198 78 182 90 180 115 C178 135 178 168 178 190Z"
            fill="rgba(255,255,255,0.025)" stroke="rgba(255,255,255,0.03)" stroke-width="0.5" />
          <path d="M174 185 C162 158 158 130 165 112 C172 94 185 102 182 122 C180 140 177 168 174 185Z"
            fill="rgba(255,255,255,0.035)" stroke="rgba(255,255,255,0.04)" stroke-width="0.5" />
          <path d="M176 185 C190 156 195 128 188 110 C181 92 170 100 172 120 C174 140 176 168 176 185Z"
            fill="rgba(255,255,255,0.035)" stroke="rgba(255,255,255,0.04)" stroke-width="0.5" />
          <circle cx="175" cy="155" r="2" fill="rgba(255,255,255,0.05)" />
        </svg>
      </div>
    </div>

    <Layout>
      <template #main>
        <router-view />
      </template>
    </Layout>
    <Toast ref="toastRef" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Layout from './components/Layout.vue';
import Toast from './components/Toast.vue';
import { registerToast } from '@/utils/toast'

const toastRef = ref(null)

onMounted(() => {
  if (toastRef.value) {
    registerToast(toastRef.value.toast)
  }
})
</script>
<style>
@import url(@/assets/style.css);
@import url(@/assets/post.css);

/* ===== 全局 CSS 黑色生命力背景 ===== */
.app-wrapper {
  position: relative;
  min-height: 100vh;
}

.global-bg {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

/* ===== 1. 星云粒子层 ===== */
.nebula-layer {
  position: absolute;
  inset: 0;
  background-image:
    /* 粒子群 1 - 大粒子 */
    radial-gradient(1px 1px at 10% 20%, rgba(255, 255, 255, 0.12) 50%, transparent 50%),
    radial-gradient(1.5px 1.5px at 25% 45%, rgba(255, 255, 255, 0.08) 50%, transparent 50%),
    radial-gradient(1px 1px at 40% 15%, rgba(255, 255, 255, 0.1) 50%, transparent 50%),
    radial-gradient(2px 2px at 55% 60%, rgba(255, 255, 255, 0.06) 50%, transparent 50%),
    radial-gradient(1px 1px at 70% 30%, rgba(255, 255, 255, 0.1) 50%, transparent 50%),
    radial-gradient(1.5px 1.5px at 85% 70%, rgba(255, 255, 255, 0.07) 50%, transparent 50%),
    radial-gradient(1px 1px at 15% 75%, rgba(255, 255, 255, 0.09) 50%, transparent 50%),
    radial-gradient(1px 1px at 90% 15%, rgba(255, 255, 255, 0.08) 50%, transparent 50%),
    radial-gradient(2px 2px at 50% 85%, rgba(255, 255, 255, 0.05) 50%, transparent 50%),
    radial-gradient(1px 1px at 35% 55%, rgba(255, 255, 255, 0.11) 50%, transparent 50%),
    /* 粒子群 2 - 带光晕的粒子 */
    radial-gradient(3px 3px at 20% 35%, rgba(0, 242, 192, 0.04) 50%, transparent 50%),
    radial-gradient(2.5px 2.5px at 65% 25%, rgba(0, 242, 192, 0.035) 50%, transparent 50%),
    radial-gradient(3px 3px at 80% 55%, rgba(0, 242, 192, 0.03) 50%, transparent 50%),
    radial-gradient(2px 2px at 45% 40%, rgba(0, 242, 192, 0.04) 50%, transparent 50%),
    radial-gradient(2.5px 2.5px at 5% 60%, rgba(0, 242, 192, 0.03) 50%, transparent 50%),
    /* 粒子群 3 - 微小粒子 */
    radial-gradient(0.8px 0.8px at 12% 8%, rgba(255, 255, 255, 0.15) 50%, transparent 50%),
    radial-gradient(0.8px 0.8px at 33% 22%, rgba(255, 255, 255, 0.12) 50%, transparent 50%),
    radial-gradient(0.8px 0.8px at 48% 38%, rgba(255, 255, 255, 0.14) 50%, transparent 50%),
    radial-gradient(0.8px 0.8px at 62% 52%, rgba(255, 255, 255, 0.1) 50%, transparent 50%),
    radial-gradient(0.8px 0.8px at 78% 68%, rgba(255, 255, 255, 0.13) 50%, transparent 50%),
    radial-gradient(0.8px 0.8px at 92% 82%, rgba(255, 255, 255, 0.11) 50%, transparent 50%),
    radial-gradient(0.8px 0.8px at 7% 92%, rgba(255, 255, 255, 0.12) 50%, transparent 50%),
    radial-gradient(0.8px 0.8px at 58% 5%, rgba(255, 255, 255, 0.1) 50%, transparent 50%),
    radial-gradient(0.8px 0.8px at 75% 42%, rgba(255, 255, 255, 0.15) 50%, transparent 50%),
    radial-gradient(0.8px 0.8px at 30% 68%, rgba(255, 255, 255, 0.12) 50%, transparent 50%);
  background-size: 200% 200%;
  animation: nebulaDrift 30s ease-in-out infinite;
}

@keyframes nebulaDrift {
  0% {
    background-position: 0% 0%;
    opacity: 0.6;
  }

  25% {
    background-position: 30% 20%;
    opacity: 0.8;
  }

  50% {
    background-position: 60% 40%;
    opacity: 0.5;
  }

  75% {
    background-position: 20% 60%;
    opacity: 0.7;
  }

  100% {
    background-position: 0% 0%;
    opacity: 0.6;
  }
}

/* ===== 2. 能量光波 ===== */
.energy-wave {
  position: absolute;
  left: -10%;
  right: -10%;
  height: 60px;
  border-radius: 50%;
  filter: blur(40px);
  opacity: 0.15;
}

.wave-1 {
  bottom: 10%;
  background: radial-gradient(ellipse at center, rgba(0, 242, 192, 0.3) 0%, transparent 70%);
  animation: waveSurge 8s ease-in-out infinite;
}

.wave-2 {
  bottom: 25%;
  background: radial-gradient(ellipse at center, rgba(0, 242, 192, 0.2) 0%, transparent 70%);
  animation: waveSurge 10s ease-in-out infinite 1s;
  height: 80px;
  opacity: 0.1;
}

.wave-3 {
  bottom: 5%;
  background: radial-gradient(ellipse at center, rgba(255, 255, 255, 0.15) 0%, transparent 70%);
  animation: waveSurge 7s ease-in-out infinite 0.5s;
  height: 40px;
  opacity: 0.08;
}

@keyframes waveSurge {

  0%,
  100% {
    transform: scaleX(1) scaleY(1);
    opacity: 0.12;
  }

  50% {
    transform: scaleX(1.15) scaleY(1.8);
    opacity: 0.25;
  }
}

/* ===== 3. 呼吸光晕 ===== */
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  animation: orbBreathe 6s ease-in-out infinite;
}

.orb-1 {
  width: 300px;
  height: 300px;
  top: 15%;
  right: 10%;
  background: radial-gradient(circle, rgba(0, 242, 192, 0.06) 0%, transparent 70%);
  animation-delay: 0s;
  animation-duration: 8s;
}

.orb-2 {
  width: 200px;
  height: 200px;
  bottom: 30%;
  left: 5%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.04) 0%, transparent 70%);
  animation-delay: 2s;
  animation-duration: 6s;
}

.orb-3 {
  width: 150px;
  height: 150px;
  top: 50%;
  left: 40%;
  background: radial-gradient(circle, rgba(0, 242, 192, 0.03) 0%, transparent 70%);
  animation-delay: 4s;
  animation-duration: 10s;
}

.orb-4 {
  width: 250px;
  height: 250px;
  top: 5%;
  left: 20%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.03) 0%, transparent 70%);
  animation-delay: 1s;
  animation-duration: 7s;
}

@keyframes orbBreathe {

  0%,
  100% {
    transform: scale(1);
    opacity: 0.3;
  }

  50% {
    transform: scale(1.4);
    opacity: 0.6;
  }
}

/* ===== 4. 流动光河 ===== */
.light-river {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 40%;
  background:
    linear-gradient(0deg,
      transparent 0%,
      rgba(0, 242, 192, 0.015) 20%,
      transparent 40%,
      rgba(0, 242, 192, 0.01) 60%,
      transparent 80%,
      rgba(255, 255, 255, 0.008) 100%);
  filter: blur(30px);
  animation: riverFlow 12s ease-in-out infinite;
}

@keyframes riverFlow {

  0%,
  100% {
    opacity: 0.3;
    transform: translateY(0) scaleY(1);
  }

  50% {
    opacity: 0.6;
    transform: translateY(-10px) scaleY(1.1);
  }
}

/* ===== 5. 玫瑰剪影 ===== */
.rose-silhouette {
  position: absolute;
  right: -20px;
  top: 50%;
  transform: translateY(-50%);
  width: 200px;
  height: 260px;
  opacity: 0.3;
  animation: roseGlow 8s ease-in-out infinite;
}

.rose-silhouette svg {
  width: 100%;
  height: 100%;
}

@keyframes roseGlow {

  0%,
  100% {
    opacity: 0.25;
    filter: blur(0px);
  }

  50% {
    opacity: 0.4;
    filter: blur(1px);
  }
}

/* ===== 响应式 ===== */
@media (max-width: 900px) {
  .rose-silhouette {
    width: 140px;
    height: 180px;
    right: -15px;
    opacity: 0.2;
  }

  .orb-1 {
    width: 200px;
    height: 200px;
  }

  .orb-3 {
    display: none;
  }
}

@media (max-width: 600px) {
  .rose-silhouette {
    width: 100px;
    height: 130px;
    right: -10px;
    opacity: 0.15;
  }

  .orb-2 {
    width: 120px;
    height: 120px;
  }

  .orb-4 {
    display: none;
  }

  .energy-wave {
    filter: blur(20px);
  }
}
</style>
