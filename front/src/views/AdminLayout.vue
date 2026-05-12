<template>
    <div class="admin-layout">
        <!-- 主内容 -->
        <main class="admin-main">
            <div class="admin-topbar">
                <h2 class="admin-page-title">{{ pageTitle }}</h2>
                <div class="admin-user">
                    <span class="admin-user-name">{{ auth.nickname || auth.username || '管理员' }}</span>
                    <div class="admin-avatar">{{ (auth.nickname || auth.username || 'A')[0].toUpperCase() }}</div>
                </div>
            </div>
            <div class="admin-content">
                <slot />
            </div>
        </main>

        <!-- 底部导航栏 -->
        <AdminSidebar />
    </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/stores/auth'
import AdminSidebar from '@/components/AdminSidebar.vue'

const route = useRoute()
const router = useRouter()
const { auth, verifyToken, logout } = useAuth()

const pageTitle = computed(() => {
    const map = {
        '/admin': '概览',
        '/admin/articles': '文章管理',
        '/admin/editor': '写文章',
        '/admin/moments': '动态管理',
        '/admin/books': '书籍管理',
        '/admin/mottos': '一句话',
        '/admin/profile': '个人资料',
        '/admin/settings': '账号设置',
        '/admin/tools': '管理工具',
    }
    return map[route.path] || '管理后台'
})

onMounted(async () => {
    // 进入管理页面时检查登录是否失效
    const valid = await verifyToken()
    if (!valid) {
        logout()
        router.push('/login')
    }
})
</script>

<style scoped>
.admin-layout {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background: linear-gradient(180deg, rgb(80, 106, 121) 0%, #354752 100%);
}

/* ===== 主内容 ===== */
.admin-main {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    padding-bottom: 60px;
}

.admin-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 32px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    flex-shrink: 0;
}

.admin-page-title {
    font-size: 20px;
    font-weight: 700;
    color: #FFFFFF;
}

.admin-user {
    display: flex;
    align-items: center;
    gap: 10px;
}

.admin-user-name {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.6);
}

.admin-avatar {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: rgba(0, 242, 192, 0.15);
    color: #00F2C0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 600;
}

.admin-content {
    flex: 1;
    overflow-y: auto;
    padding: 28px 32px 100px;
}
</style>
