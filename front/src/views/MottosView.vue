<template>
    <div class="mottos-page" @click="randomMotto">
        <div class="skeleton-area" v-if="loading">
            <div class="skeleton-line"></div>
            <div class="skeleton-line" style="width: 60%"></div>
        </div>

        <div class="motto-stage" v-else-if="mottos.length">
            <!-- 装饰光晕 -->
            <div class="glow"></div>

            <transition name="fade" mode="out-in">
                <p class="motto-text" :key="currentMotto.id">{{ currentMotto.content }}</p>
            </transition>

            <span class="motto-date">{{ formatDate(currentMotto.created_at) }}</span>
        </div>

        <div class="empty-state" v-else>
            <p class="empty-text">暂无语录</p>
        </div>

        <!-- 底部登录按钮 -->
        <router-link to="/login" class="login-btn" v-if="!isLoggedIn">
            <i class="fas fa-lock"></i>
            管理
        </router-link>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { publicApi } from '@/utils/api'

const loading = ref(true)
const mottos = ref([])
const currentIndex = ref(0)
const isLoggedIn = ref(!!localStorage.getItem('admin_token'))
let timer = null

const currentMotto = computed(() => mottos.value[currentIndex.value] || {})

function formatDate(dateStr) {
    if (!dateStr) return ''
    const d = new Date(dateStr)
    return `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, '0')}.${String(d.getDate()).padStart(2, '0')}`
}

function randomMotto() {
    if (mottos.value.length <= 1) return
    let newIdx
    do {
        newIdx = Math.floor(Math.random() * mottos.value.length)
    } while (newIdx === currentIndex.value)
    currentIndex.value = newIdx
    if (timer) {
        clearInterval(timer)
        timer = setInterval(randomMotto, 8000)
    }
}

onMounted(async () => {
    try {
        const res = await publicApi.getMottos({ page: 1, page_size: 100 })
        const items = res.items || []
        mottos.value = items
        if (mottos.value.length > 0) {
            currentIndex.value = Math.floor(Math.random() * mottos.value.length)
            timer = setInterval(randomMotto, 8000)
        }
    } catch (e) {
        console.error('加载语录失败:', e)
    } finally {
        loading.value = false
    }
})

onUnmounted(() => {
    if (timer) clearInterval(timer)
})
</script>

<style scoped>
.mottos-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: calc(100vh - 120px);
    padding: 40px 32px 80px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

/* ===== 装饰光晕 ===== */
.glow {
    position: fixed;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    background: var(--theme);
    pointer-events: none;
    filter: blur(100px);
    opacity: 0.08;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    animation: pulse 6s ease-in-out infinite;
}

@keyframes pulse {

    0%,
    100% {
        transform: translate(-50%, -50%) scale(1);
        opacity: 0.08;
    }

    50% {
        transform: translate(-50%, -50%) scale(1.15);
        opacity: 0.12;
    }
}

/* ===== 语录 ===== */
.motto-stage {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 32px;
    position: relative;
    z-index: 1;
}

.motto-text {
    font-size: 28px;
    color: rgba(255, 255, 255, 0.9);
    line-height: 1.7;
    font-weight: 300;
    text-align: center;
    max-width: 640px;
    margin: 0;
    font-family: 'Noto Serif SC', 'Source Han Serif SC', 'STSong', serif;
    user-select: none;
}

.motto-date {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.15);
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 1px;
}

/* ===== 底部登录按钮 ===== */
.login-btn {
    position: fixed;
    bottom: 32px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 24px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.2);
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    text-decoration: none;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.3s;
    z-index: 10;
    letter-spacing: 0.5px;
}

.login-btn:hover {
    color: rgba(255, 255, 255, 0.5);
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.12);
}

.login-btn i {
    font-size: 11px;
}

/* ===== 骨架屏 ===== */
.skeleton-area {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    width: 100%;
    max-width: 480px;
}

.skeleton-line {
    height: 18px;
    border-radius: 9px;
    width: 80%;
    background: linear-gradient(90deg,
            rgba(255, 255, 255, 0.03) 0%,
            rgba(255, 255, 255, 0.07) 50%,
            rgba(255, 255, 255, 0.03) 100%);
    background-size: 200% 100%;
    animation: shimmer 1.5s ease-in-out infinite;
}

@keyframes shimmer {
    0% {
        background-position: 200% 0;
    }

    100% {
        background-position: -200% 0;
    }
}

/* ===== 空状态 ===== */
.empty-state {
    display: flex;
    align-items: center;
    justify-content: center;
}

.empty-text {
    font-size: 16px;
    color: rgba(255, 255, 255, 0.15);
}

/* ===== 过渡 ===== */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.6s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

/* ===== 响应式 ===== */
@media (max-width: 600px) {
    .mottos-page {
        padding: 32px 20px 70px;
    }

    .motto-text {
        font-size: 22px;
    }

    .motto-stage {
        gap: 24px;
    }

    .glow {
        width: 280px;
        height: 280px;
    }

    .login-btn {
        bottom: 24px;
        padding: 8px 20px;
        font-size: 12px;
    }
}
</style>
