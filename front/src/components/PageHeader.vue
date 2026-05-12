<template>
    <div class="page-header">
        <!-- 装饰背景 -->
        <div class="header-bg">
            <div class="header-glow"></div>
            <div class="header-particles">
                <span class="particle" v-for="n in 6" :key="n" :style="{
                    left: (10 + n * 15) + '%',
                    top: (20 + (n * 7) % 60) + '%',
                    width: (4 + n % 3 * 2) + 'px',
                    height: (4 + n % 3 * 2) + 'px',
                    animationDelay: (n * 0.4) + 's',
                    opacity: 0.15 + n * 0.03
                }">
                </span>
            </div>
        </div>

        <div class="header-content">
            <!-- 图标 -->
            <div class="header-icon" v-if="icon">
                <i :class="icon"></i>
            </div>

            <!-- 标题区 -->
            <div class="header-text">
                <h1 class="header-title">{{ title }}</h1>
                <p class="header-desc" v-if="desc">{{ desc }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    title: { type: String, required: true },
    desc: { type: String, default: '' },
    icon: { type: String, default: '' },
})
</script>

<style scoped>
.page-header {
    position: relative;
    padding: 48px 0 32px;
    margin-bottom: 28px;
    overflow: hidden;
}

/* ===== 装饰背景 ===== */
.header-bg {
    position: absolute;
    inset: 0;
    pointer-events: none;
}

.header-glow {
    position: absolute;
    top: -40px;
    left: -20px;
    width: 300px;
    height: 200px;
    background: radial-gradient(ellipse, var(--theme) 0%, transparent 70%);
    opacity: 0.04;
}

.header-particles {
    position: absolute;
    inset: 0;
}

.particle {
    position: absolute;
    border-radius: 50%;
    background: var(--theme);
    animation: float 6s ease-in-out infinite;
}

@keyframes float {

    0%,
    100% {
        transform: translateY(0) scale(1);
    }

    50% {
        transform: translateY(-12px) scale(1.2);
    }
}

/* ===== 内容 ===== */
.header-content {
    position: relative;
    z-index: 1;
    display: flex;
    align-items: center;
    gap: 20px;
}

.header-icon {
    width: 52px;
    height: 52px;
    border-radius: 16px;
    background: var(--theme-light);
    border: 1px solid var(--theme-border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    color: var(--theme);
    flex-shrink: 0;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.page-header:hover .header-icon {
    transform: scale(1.05) rotate(-3deg);
    box-shadow: 0 0 24px color-mix(in srgb, var(--theme) 15%, transparent);
}

.header-text {
    flex: 1;
    min-width: 0;
}

.header-title {
    font-size: 34px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -1px;
    line-height: 1.2;
    margin: 0;
}

.header-desc {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.3);
    margin-top: 8px;
    letter-spacing: 1px;
    font-weight: 300;
}

/* ===== 响应式 ===== */
@media (max-width: 600px) {
    .page-header {
        padding: 32px 0 24px;
    }

    .header-content {
        gap: 14px;
    }

    .header-icon {
        width: 42px;
        height: 42px;
        font-size: 18px;
        border-radius: 12px;
    }

    .header-title {
        font-size: 26px;
    }

    .header-desc {
        font-size: 13px;
    }
}
</style>
