<template>
    <nav class="admin-bottom-bar">
        <router-link to="/admin" class="nav-link" :class="{ active: $route.path === '/admin' }">
            <i class="fas fa-gauge-high"></i>
            <span>概览</span>
        </router-link>
        <router-link to="/admin/articles" class="nav-link"
            :class="{ active: $route.path.startsWith('/admin/articles') }">
            <i class="fas fa-newspaper"></i>
            <span>文章</span>
        </router-link>
        <router-link to="/admin/editor" class="nav-link" :class="{ active: $route.path === '/admin/editor' }">
            <i class="fas fa-pen"></i>
            <span>写文章</span>
        </router-link>
        <router-link to="/admin/moments" class="nav-link" :class="{ active: $route.path === '/admin/moments' }">
            <i class="fas fa-camera"></i>
            <span>动态</span>
        </router-link>
        <router-link to="/admin/books" class="nav-link" :class="{ active: $route.path.startsWith('/admin/books') }">
            <i class="fas fa-book"></i>
            <span>书籍</span>
        </router-link>
        <router-link to="/admin/mottos" class="nav-link" :class="{ active: $route.path === '/admin/mottos' }">
            <i class="fas fa-quote-right"></i>
            <span>一言</span>
        </router-link>
        <router-link to="/admin/profile" class="nav-link" :class="{ active: $route.path === '/admin/profile' }">
            <i class="fas fa-user-gear"></i>
            <span>资料</span>
        </router-link>
        <router-link to="/admin/settings" class="nav-link" :class="{ active: $route.path === '/admin/settings' }">
            <i class="fas fa-cog"></i>
            <span>设置</span>
        </router-link>
        <router-link to="/admin/tools" class="nav-link" :class="{ active: $route.path === '/admin/tools' }">
            <i class="fas fa-tools"></i>
            <span>工具</span>
        </router-link>
        <router-link to="/" class="nav-link back-link">
            <i class="fas fa-arrow-left"></i>
            <span>返回</span>
        </router-link>
    </nav>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<style scoped>
.admin-bottom-bar {
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
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}

.nav-link {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3px;
    padding: 8px 14px;
    border-radius: 8px;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.5px;
    color: rgba(255, 255, 255, 0.4);
    text-decoration: none;
    transition: all 0.25s ease;
    min-width: 48px;
    flex-shrink: 0;
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

.back-link {
    color: rgba(255, 255, 255, 0.2);
}

.back-link:hover {
    color: rgba(255, 255, 255, 0.45);
}

@media (max-width: 600px) {
    .admin-bottom-bar {
        padding: 6px 8px;
        justify-content: flex-start;
    }

    .nav-link {
        padding: 6px 10px;
        min-width: 40px;
    }
}
</style>
