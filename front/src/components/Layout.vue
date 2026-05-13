<template>
    <div class="app-container">
        <div class="main-layout">
            <!-- 左侧边栏抽屉（仅普通模式） -->
            <div class="sidebar-drawer" :class="{ open: drawerVisible }" v-if="sidebarMode !== 'admin'">
                <div v-show="sidebarMode === 'normal'">
                    <slot name="sidebar">
                        <Sidebar></Sidebar>
                    </slot>
                </div>
            </div>

            <!-- 主内容区 -->
            <div class="main-content" :class="{ 'has-admin-bar': sidebarMode === 'admin' }">
                <Top v-if="sidebarMode !== 'admin'" />
                <div class="content-body" :class="{ 'has-admin-bar': sidebarMode === 'admin' }">
                    <slot name="main">
                        <Main></Main>
                    </slot>
                </div>
                <!-- 管理后台底部导航栏 -->
                <AdminSidebar v-if="sidebarMode === 'admin'" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuth } from '@/stores/auth';
import Sidebar from './Sidebar.vue';
import AdminSidebar from './AdminSidebar.vue';
import Main from './Main.vue';
import Top from './Top.vue';

const router = useRouter()
const route = useRoute()
const { auth } = useAuth()

const MODE_KEY = 'sidebar_mode';
const sidebarMode = ref(null)
const drawerVisible = computed(() => sidebarMode.value === 'normal')

// 根据路由自动切换模式
function syncModeFromRoute() {
    const isAdminRoute = route.path.startsWith('/admin')
    if (isAdminRoute) {
        sidebarMode.value = 'admin'
    } else if (sidebarMode.value === 'admin') {
        // 从 admin 页面离开时，如果之前没有保存的模式，关闭侧边栏
        sidebarMode.value = null
    }
    // 路由切换时滚动到顶部
    nextTick(() => {
        const content = document.querySelector('.content-body')
        if (content) content.scrollTop = 0
    })
}

// 初始化
syncModeFromRoute()

// 监听路由变化
watch(() => route.path, () => {
    syncModeFromRoute()
})

watch(sidebarMode, (val) => {
    localStorage.setItem(MODE_KEY, val || 'closed')
})

function toggleSidebar() {
    if (sidebarMode.value === 'normal') {
        sidebarMode.value = null
    } else {
        sidebarMode.value = 'normal'
    }
}

function toggleAdminSidebar() {
    if (!auth.isAdmin) {
        router.push('/login')
        return
    }
    if (sidebarMode.value === 'admin') {
        sidebarMode.value = null
    } else {
        sidebarMode.value = 'admin'
    }
}
</script>

<style scoped>
.app-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    position: relative;
}

.main-layout {
    flex: 1;
    display: flex;
    overflow: hidden;
    position: relative;
}

/* 抽屉式侧边栏（仅普通模式） */
.sidebar-drawer {
    flex-shrink: 0;
    width: 220px;
    z-index: 20;
    transition: margin-left 0.3s ease;
    height: 100%;
}

.sidebar-drawer.open {
    margin-left: 0;
}

.sidebar-drawer:not(.open) {
    margin-left: -220px;
}

.main-content {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    transition: margin-left 0.3s ease;
}

.main-content.has-admin-bar {
    padding-bottom: 0;
}

.content-body {
    flex: 1;
    overflow-y: auto;
    padding: 28px 32px 32px;
    width: 100%;
    max-width: 1060px;
    margin: 0 auto;
}

.content-body.has-admin-bar {
    padding-bottom: 100px;
}

/* ===== 响应式 ===== */
@media (max-width: 900px) {
    .content-body {
        padding: 24px 20px 32px;
    }
}

@media (max-width: 600px) {
    .content-body {
        padding: 16px 14px 32px;
    }
}
</style>
