<template>
    <div class="sidebar">
        <!-- Logo -->
        <div class="logo-section">
            <div class="logo-icon">
                <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                    <rect x="2" y="2" width="24" height="24" rx="6" stroke="currentColor" stroke-width="1.5"
                        opacity="0.15" />
                    <circle cx="14" cy="14" r="4" fill="currentColor" opacity="0.08" />
                    <circle cx="14" cy="14" r="1.5" fill="currentColor" opacity="0.35" />
                </svg>
            </div>
            <span class="logo-title">魂牵梦绕</span>
        </div>

        <!-- 导航 -->
        <nav class="nav">
            <router-link to="/" class="nav-item" :class="{ active: $route.path === '/' }">
                <i class="fas fa-compass"></i>
                <span>发现</span>
            </router-link>
            <router-link to="/articles" class="nav-item" :class="{ active: $route.path === '/articles' }">
                <i class="fas fa-newspaper"></i>
                <span>文章</span>
            </router-link>
            <router-link to="/reading" class="nav-item" :class="{ active: $route.path === '/reading' }">
                <i class="fas fa-book"></i>
                <span>读书</span>
            </router-link>
            <router-link to="/daily" class="nav-item" :class="{ active: $route.path === '/daily' }">
                <i class="fas fa-chart-line"></i>
                <span>精进</span>
            </router-link>
            <router-link to="/moments" class="nav-item" :class="{ active: $route.path === '/moments' }">
                <i class="fas fa-camera"></i>
                <span>动态</span>
            </router-link>
            <router-link to="/mottos" class="nav-item" :class="{ active: $route.path === '/mottos' }">
                <i class="fas fa-quote-right"></i>
                <span>一言</span>
            </router-link>
        </nav>

        <!-- 底部 -->
        <div class="sidebar-footer">
            <div class="theme-selector" @click="themeOpen = !themeOpen">
                <div class="theme-current">
                    <div class="theme-dot" :style="{ background: currentColor }"></div>
                    <span>主题</span>
                </div>
                <i class="fas fa-chevron-down" :class="{ open: themeOpen }"></i>
            </div>
            <transition name="slide">
                <div class="theme-panel" v-if="themeOpen">
                    <button v-for="t in themes" :key="t.id" class="theme-option"
                        :class="{ active: currentTheme === t.id }" @click="setTheme(t.id)">
                        <span class="option-dot" :style="{ background: t.color }"></span>
                        <span class="option-label">{{ t.name }}</span>
                    </button>
                </div>
            </transition>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const themes = [
    { id: 'jade', name: '翡翠绿', color: '#00F2C0' },
    { id: 'slate', name: '石板灰', color: '#7a8a9a' },
    { id: 'aurora', name: '极光紫', color: '#a29bfe' },
    { id: 'sunset', name: '暖阳橙', color: '#fdcb6e' },
    { id: 'ocean', name: '深海蓝', color: '#74b9ff' },
    { id: 'sakura', name: '樱花粉', color: '#fd79a8' },
    { id: 'graphite', name: '石墨灰', color: '#b2bec3' },
    { id: 'flame', name: '烈焰红', color: '#ff6b6b' },
    { id: 'forest', name: '森林绿', color: '#55efc4' },
    { id: 'midnight', name: '暗夜紫', color: '#6c5ce7' },
    { id: 'amber', name: '琥珀金', color: '#f9ca24' },
]

const currentTheme = ref('jade')
const themeOpen = ref(false)

const currentColor = computed(() => {
    const t = themes.find(t => t.id === currentTheme.value)
    return t ? t.color : '#00F2C0'
})

function setTheme(id) {
    currentTheme.value = id
    document.documentElement.setAttribute('data-theme', id)
    localStorage.setItem('blog_theme', id)
}

onMounted(() => {
    const saved = localStorage.getItem('blog_theme') || 'jade'
    currentTheme.value = saved
    document.documentElement.setAttribute('data-theme', saved)
})
</script>

<style scoped>
/* ===== 侧边栏 ===== */
.sidebar {
    height: 100vh;
    width: 220px;
    background: var(--sidebar-bg);
    border-right: 1px solid var(--sidebar-border);
    display: flex;
    flex-direction: column;
    padding: 0;
    position: relative;
    z-index: 10;
}

/* ===== Logo ===== */
.logo-section {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 28px 20px 20px;
    flex-shrink: 0;
}

.logo-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    color: var(--theme);
}

.logo-title {
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 1px;
    color: rgba(255, 255, 255, 0.85);
}

/* ===== 导航 ===== */
.nav {
    flex: 1;
    padding: 8px 12px;
    display: flex;
    flex-direction: column;
    gap: 2px;
    overflow-y: auto;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.35);
    text-decoration: none;
    transition: all 0.2s ease;
    cursor: pointer;
}

.nav-item i {
    width: 18px;
    font-size: 0.95rem;
    text-align: center;
    flex-shrink: 0;
}

/* 激活 */
.nav-item.active {
    color: #fff;
    background: rgba(255, 255, 255, 0.06);
}

/* hover */
.nav-item:hover:not(.active) {
    color: rgba(255, 255, 255, 0.55);
    background: rgba(255, 255, 255, 0.03);
}

/* ===== 底部 ===== */
.sidebar-footer {
    padding: 12px;
    flex-shrink: 0;
    border-top: 1px solid var(--sidebar-border);
}

.theme-selector {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.2);
    cursor: pointer;
    transition: all 0.2s ease;
    user-select: none;
}

.theme-selector:hover {
    background: rgba(255, 255, 255, 0.03);
    color: rgba(255, 255, 255, 0.35);
}

.theme-current {
    display: flex;
    align-items: center;
    gap: 8px;
}

.theme-dot {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    flex-shrink: 0;
    border: 2px solid rgba(255, 255, 255, 0.06);
}

.theme-selector i {
    font-size: 10px;
    transition: transform 0.3s ease;
    opacity: 0.4;
}

.theme-selector i.open {
    transform: rotate(180deg);
}

/* 主题面板 */
.theme-panel {
    padding: 8px 4px 2px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2px;
}

.theme-option {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 10px;
    border-radius: 6px;
    border: none;
    background: transparent;
    color: rgba(255, 255, 255, 0.2);
    font-size: 11px;
    cursor: pointer;
    transition: all 0.15s ease;
    width: 100%;
    text-align: left;
}

.theme-option:hover {
    background: rgba(255, 255, 255, 0.04);
    color: rgba(255, 255, 255, 0.35);
}

.theme-option.active {
    color: rgba(255, 255, 255, 0.5);
    background: rgba(255, 255, 255, 0.04);
}

.option-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    flex-shrink: 0;
    border: 2px solid rgba(255, 255, 255, 0.06);
}

.option-label {
    flex: 1;
    font-size: 11px;
}

/* 下拉动画 */
.slide-enter-active,
.slide-leave-active {
    transition: all 0.25s ease;
}

.slide-enter-from,
.slide-leave-to {
    opacity: 0;
    transform: translateY(-6px);
}
</style>
