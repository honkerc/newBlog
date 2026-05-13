<template>
    <nav class="bottom-bar">
        <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">
            <i class="fas fa-compass"></i>
            <span>发现</span>
        </router-link>
        <router-link to="/articles" class="nav-link" :class="{ active: $route.path === '/articles' }">
            <i class="fas fa-newspaper"></i>
            <span>文章</span>
        </router-link>
        <router-link to="/reading" class="nav-link" :class="{ active: $route.path === '/reading' }">
            <i class="fas fa-book"></i>
            <span>读书</span>
        </router-link>
        <router-link to="/daily" class="nav-link" :class="{ active: $route.path === '/daily' }">
            <i class="fas fa-chart-line"></i>
            <span>精进</span>
        </router-link>
        <router-link to="/moments" class="nav-link" :class="{ active: $route.path === '/moments' }">
            <i class="fas fa-camera"></i>
            <span>动态</span>
        </router-link>
        <router-link to="/mottos" class="nav-link" :class="{ active: $route.path === '/mottos' }">
            <i class="fas fa-quote-right"></i>
            <span>一言</span>
        </router-link>
        <router-link :to="isLoggedIn ? '/admin' : '/login'" class="nav-link login-link">
            <i class="fas fa-lock"></i>
            <span>管理</span>
        </router-link>
    </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isLoggedIn = ref(!!localStorage.getItem('admin_token'))
</script>

<style scoped>
.bottom-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2px;
    padding: 8px 16px;
    padding-bottom: calc(8px + env(safe-area-inset-bottom, 0px));
    z-index: 100;
    background: var(--bg-gradient-end);
    border-top: 1px solid var(--border-color);
}

.nav-link {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3px;
    padding: 8px 18px;
    border-radius: 8px;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.5px;
    color: rgba(255, 255, 255, 0.4);
    text-decoration: none;
    transition: all 0.25s ease;
    min-width: 56px;
}

.nav-link i {
    font-size: 1.15rem;
    transition: all 0.25s ease;
}

.nav-link span {
    font-size: 9px;
    letter-spacing: 0.8px;
    opacity: 0.8;
}

.nav-link:hover {
    color: rgba(255, 255, 255, 0.65);
}

.nav-link.active {
    color: var(--theme);
}

.nav-link.active i {
    filter: drop-shadow(0 0 6px color-mix(in srgb, var(--theme) 40%, transparent));
}

.login-link {
    color: rgba(255, 255, 255, 0.15);
}

.login-link:hover {
    color: rgba(255, 255, 255, 0.35);
}

@media (max-width: 600px) {
    .bottom-bar {
        padding: 6px 12px;
    }

    .nav-link {
        padding: 6px 10px;
        min-width: 40px;
    }
}
</style>
