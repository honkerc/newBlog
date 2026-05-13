<template>
    <div class="app">
        <div class="page-content">
            <router-view />
        </div>

        <!-- 底部 Tab 导航 -->
        <nav class="bottom-nav" v-if="showNav">
            <router-link v-for="tab in tabs" :key="tab.path" :to="tab.path" class="nav-item"
                :class="{ active: $route.path === tab.path }">
                <i :class="tab.icon"></i>
                <span>{{ tab.label }}</span>
            </router-link>
        </nav>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const tabs = [
    { path: '/', label: '打卡', icon: 'fas fa-check-circle' },
    { path: '/motto', label: '一言', icon: 'fas fa-quote-right' },
    { path: '/today', label: '今日', icon: 'fas fa-calendar-day' },
    { path: '/daily', label: '精进', icon: 'fas fa-chart-line' },
    { path: '/reading', label: '读书', icon: 'fas fa-book-open' },
    { path: '/settings', label: '设置', icon: 'fas fa-cog' },
]

const showNav = computed(() => {
    return route.path !== '/login'
})
</script>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --theme: #00F2C0;
    --theme-rgb: 0, 242, 192;
    --theme-light: rgba(var(--theme-rgb), 0.12);
    --theme-border: rgba(var(--theme-rgb), 0.2);

    --bg: #354752;
    --bg-gradient-start: rgb(80, 106, 121);
    --bg-gradient-end: #354752;
    --bg-card: rgba(11, 14, 20, 0.3);
    --bg-surface: rgba(255, 255, 255, 0.05);
    --bg-surface-hover: rgba(255, 255, 255, 0.08);

    --text: #FFFFFF;
    --text-secondary: #EFF3F8;
    --text-tertiary: #CBD5F0;
    --text-muted: rgba(255, 255, 255, 0.3);
    --text-dim: rgba(255, 255, 255, 0.15);

    --accent: var(--theme);
    --accent-rgb: var(--theme-rgb);
    --accent-light: var(--theme-light);

    --border: rgba(255, 255, 255, 0.06);
    --border-light: rgba(255, 255, 255, 0.1);

    --nav-height: 64px;
    --radius: 14px;
    --radius-sm: 8px;
    --radius-md: 12px;
    --shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    --shadow-lg: 0 4px 16px rgba(0, 0, 0, 0.15);
}


html,
body {
    height: 100%;
    background: linear-gradient(180deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans SC', sans-serif;
    -webkit-font-smoothing: antialiased;
    overflow: hidden;
}

#app {
    height: 100%;
    background: linear-gradient(180deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
}

.app {
    height: 100%;
    display: flex;
    flex-direction: column;
    max-width: 480px;
    margin: 0 auto;
    position: relative;
}

.page-content {
    flex: 1;
    overflow-y: auto;
    padding: 0 16px 80px;
    padding-top: env(safe-area-inset-top, 0px);
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    -ms-overflow-style: none;
}

.page-content::-webkit-scrollbar {
    display: none;
}

/* ===== 底部导航 ===== */
.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 480px;
    height: var(--nav-height);
    display: flex;
    align-items: center;
    justify-content: space-around;
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    padding-bottom: env(safe-area-inset-bottom, 0);
    z-index: 100;
}


.nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3px;
    padding: 6px 12px;
    text-decoration: none;
    color: var(--text-dim);
    font-size: 10px;
    transition: color 0.2s;
    border-radius: 10px;
    min-width: 56px;
}

.nav-item i {
    font-size: 20px;
    transition: transform 0.2s;
}

.nav-item.active {
    color: var(--accent);
}

.nav-item.active i {
    transform: scale(1.1);
}

/* ===== 通用组件样式 ===== */
.page-header {
    padding: 24px 0 16px;
    text-align: center;
}

.page-header h1 {
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.3px;
}

.page-header p {
    font-size: 13px;
    color: var(--text-secondary);
    margin-top: 4px;
}

.form-group {
    margin-bottom: 16px;
}

.form-group label {
    display: block;
    font-size: 12px;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 6px;
    letter-spacing: 0.3px;
}

.form-input {
    width: 100%;
    padding: 12px 14px;
    border-radius: 10px;
    border: 1px solid var(--border);
    background: var(--bg-surface);
    color: var(--text);
    font-size: 15px;
    font-family: inherit;
    outline: none;
    transition: border-color 0.2s;
}

.form-input::placeholder {
    color: rgba(255, 255, 255, 0.2);
}

.form-input:focus {
    border-color: var(--accent);
}

.form-textarea {
    width: 100%;
    min-height: 100px;
    padding: 12px 14px;
    border-radius: 10px;
    border: 1px solid var(--border);
    background: var(--bg-surface);
    color: var(--text);
    font-size: 15px;
    font-family: inherit;
    outline: none;
    resize: vertical;
    transition: border-color 0.2s;
    line-height: 1.6;
}

.form-textarea::placeholder {
    color: rgba(255, 255, 255, 0.2);
}

.form-textarea:focus {
    border-color: var(--accent);
}

.btn-primary {
    width: 100%;
    padding: 14px;
    border-radius: 12px;
    border: 1px solid rgba(var(--theme-rgb), 0.25);
    background: rgba(var(--theme-rgb), 0.08);
    color: var(--accent);
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    font-family: inherit;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}

.btn-primary:active {
    transform: scale(0.98);
}

.btn-primary:disabled {
    opacity: 0.3;
    cursor: not-allowed;
    transform: none;
}

.toast {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    padding: 10px 20px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 500;
    z-index: 9999;
    animation: toastIn 0.3s ease;
    max-width: 360px;
    text-align: center;
}

.toast.success {
    background: rgba(var(--theme-rgb), 0.12);
    color: var(--accent);
    border: 1px solid rgba(var(--theme-rgb), 0.2);
}

.toast.error {
    background: rgba(255, 107, 107, 0.12);
    color: #ff6b6b;
    border: 1px solid rgba(255, 107, 107, 0.2);
}


@keyframes toastIn {
    from {
        opacity: 0;
        transform: translateX(-50%) translateY(-10px);
    }

    to {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }
}
</style>
