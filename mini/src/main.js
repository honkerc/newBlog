import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import App from './App.vue'
import Login from './views/Login.vue'
import CheckIn from './views/CheckIn.vue'
import Motto from './views/Motto.vue'
import Daily from './views/Daily.vue'
import Reading from './views/Reading.vue'
import Today from './views/Today.vue'
import Settings from './views/Settings.vue'

const routes = [
    { path: '/', component: CheckIn, meta: { title: '打卡', icon: 'fa-check-circle', auth: true } },
    { path: '/motto', component: Motto, meta: { title: '一句话', icon: 'fa-quote-right', auth: true } },
    { path: '/daily', component: Daily, meta: { title: '日精进', icon: 'fa-chart-line', auth: true } },
    { path: '/reading', component: Reading, meta: { title: '读书', icon: 'fa-book-open', auth: true } },
    { path: '/today', component: Today, meta: { title: '今日', icon: 'fa-calendar-day', auth: true } },
    { path: '/login', component: Login },
    { path: '/settings', component: Settings },
]

const router = createRouter({
    history: createWebHashHistory(),
    routes,
})

// 验证 token 是否有效
async function verifyToken(token) {
    try {
        const STORAGE_KEY = 'mini_server_url'
        const DEFAULT_URL = ''
        const API_BASE = localStorage.getItem(STORAGE_KEY) || DEFAULT_URL
        const res = await fetch(`${API_BASE}/api/auth/verify`, {
            headers: { 'Authorization': `Bearer ${token}` },
        })
        return res.ok
    } catch {
        return false
    }
}

router.beforeEach(async (to, from, next) => {
    const token = localStorage.getItem('mini_token')
    if (to.meta.auth && !token) {
        next('/login')
    } else if (to.meta.auth && token) {
        // 有 token 时验证是否有效
        const valid = await verifyToken(token)
        if (!valid) {
            localStorage.removeItem('mini_token')
            next('/login')
        } else {
            next()
        }
    } else {
        next()
    }
})

// 记住上次访问的页面
router.afterEach((to) => {
    if (to.path !== '/login') {
        localStorage.setItem('mini_last_path', to.path)
    }
})

// 启动时跳转到上次访问的页面
const savedPath = localStorage.getItem('mini_last_path')
if (savedPath && savedPath !== '/login') {
    // 需要在路由就绪后跳转
    setTimeout(() => {
        const token = localStorage.getItem('mini_token')
        if (token) {
            router.push(savedPath).catch(() => { })
        }
    }, 0)
}

const app = createApp(App)
app.use(router)
app.mount('#app')
