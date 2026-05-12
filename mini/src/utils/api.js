/**
 * API 基础地址
 * - Capacitor (Android 原生): 使用配置的服务器地址
 * - 开发环境 (localhost:3001): 使用 localhost:8000
 * - 生产环境 (Nginx 反向代理): 使用同源地址（空字符串）
 *
 * 通过 window.location.port 判断：
 *   8080/3001 → 开发环境，需要加端口
 *   其他       → 生产环境（Nginx 已代理 /api/ 到后端）
 */

// 在 Capacitor 原生环境中，使用配置的服务器地址
const isCapacitor = typeof window !== 'undefined' && window.Capacitor !== undefined
let API_BASE = ''

if (isCapacitor) {
    // Android 原生应用 → 连接到服务器
    API_BASE = 'http://honkerc.cn'
} else {
    const isDev = window.location.port === '8080' || window.location.port === '3001'
    API_BASE = isDev ? `http://${window.location.hostname}:8000` : ''
}

function getToken() {
    return localStorage.getItem('mini_token')
}

async function request(url, options = {}) {
    const token = getToken()
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    }
    if (token) {
        headers['Authorization'] = `Bearer ${token}`
    }

    const res = await fetch(`${API_BASE}${url}`, {
        ...options,
        headers,
    })

    if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        throw new Error(err.detail || `请求失败 (${res.status})`)
    }

    return res.json()
}

export const api = {
    // ==================== 认证 ====================
    login(username, password) {
        return request('/api/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username, password }),
        })
    },
    verifyToken() {
        return request('/api/auth/verify')
    },
    getProfile() {
        return request('/api/auth/profile')
    },
    updateProfile(data) {
        return request('/api/auth/profile', {
            method: 'PUT',
            body: JSON.stringify(data),
        })
    },
    changePassword(data) {
        return request('/api/auth/password', {
            method: 'PUT',
            body: JSON.stringify(data),
        })
    },

    // ==================== 打卡（使用动态 API） ====================
    createCheckIn(data) {
        return request('/api/moments', {
            method: 'POST',
            body: JSON.stringify(data),
        })
    },
    deleteCheckIn(id) {
        return request(`/api/moments/${id}`, { method: 'DELETE' })
    },

    // ==================== 一句话 ====================
    createMotto(data) {
        return request('/api/mottos', {
            method: 'POST',
            body: JSON.stringify(data),
        })
    },
    getMottos(params = {}) {
        const qs = new URLSearchParams(params).toString()
        return request(`/api/mottos?${qs}`)
    },
    getLatestMottos() {
        return request('/api/mottos/latest')
    },
    updateMotto(id, data) {
        return request(`/api/mottos/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        })
    },
    deleteMotto(id) {
        return request(`/api/mottos/${id}`, { method: 'DELETE' })
    },

    // ==================== 文章（日精进、读书笔记） ====================
    createPost(data) {
        return request('/api/posts', {
            method: 'POST',
            body: JSON.stringify(data),
        })
    },
    updatePost(id, data) {
        return request(`/api/posts/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        })
    },
    deletePost(id) {
        return request(`/api/posts/${id}`, { method: 'DELETE' })
    },
    getPosts(params = {}) {
        const qs = new URLSearchParams(params).toString()
        return request(`/api/posts?${qs}`)
    },
    getPost(id) {
        return request(`/api/posts/${id}`)
    },
    getLatestPosts() {
        return request('/api/posts/latest')
    },
    getCategories() {
        return request('/api/posts/categories')
    },
    getStats() {
        return request('/api/posts/stats')
    },
    getAllPosts(params = {}) {
        const qs = new URLSearchParams(params).toString()
        return request(`/api/posts/admin/all?${qs}`)
    },

    // ==================== 书籍 ====================
    getBooks(params = {}) {
        const qs = new URLSearchParams(params).toString()
        return request(`/api/books?${qs}`)
    },
    getBook(id) {
        return request(`/api/books/${id}`)
    },
    getBookByTag(tag) {
        return request(`/api/books/by-tag/${encodeURIComponent(tag)}`)
    },
    createBook(data) {
        return request('/api/books', {
            method: 'POST',
            body: JSON.stringify(data),
        })
    },
    updateBook(id, data) {
        return request(`/api/books/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        })
    },
    deleteBook(id) {
        return request(`/api/books/${id}`, {
            method: 'DELETE',
        })
    },

    // ==================== 动态 ====================
    getMoments(params = {}) {
        const qs = new URLSearchParams(params).toString()
        return request(`/api/moments?${qs}`)
    },
    getLatestMoments() {
        return request('/api/moments/latest')
    },
    getMomentCategories() {
        return request('/api/moments/categories')
    },
    createMoment(data) {
        return request('/api/moments', {
            method: 'POST',
            body: JSON.stringify(data),
        })
    },
    updateMoment(id, data) {
        return request(`/api/moments/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        })
    },
    deleteMoment(id) {
        return request(`/api/moments/${id}`, {
            method: 'DELETE',
        })
    },

    // ==================== 动态 Feed ====================
    getFeed(params = {}) {
        const qs = new URLSearchParams(params).toString()
        return request(`/api/feed?${qs}`)
    },

    // ==================== 今日记录 ====================
    getTodaySummary() {
        return request('/api/today')
    },

    // ==================== 搜索 ====================
    search(params = {}) {
        const qs = new URLSearchParams(params).toString()
        return request(`/api/search?${qs}`)
    },

    // ==================== 热力图 ====================
    getHeatmap(days = 60) {
        return request(`/api/heatmap?days=${days}`)
    },

    // ==================== 上传 ====================
    uploadFile(file) {
        const token = getToken()
        const formData = new FormData()
        formData.append('file', file)

        return fetch(`${API_BASE}/api/upload`, {
            method: 'POST',
            headers: token ? { 'Authorization': `Bearer ${token}` } : {},
            body: formData,
        }).then(async (res) => {
            if (!res.ok) {
                const err = await res.json().catch(() => ({}))
                throw new Error(err.detail || `上传失败 (${res.status})`)
            }
            return res.json()
        })
    },

    // ==================== 点赞 ====================
    toggleLike(momentId) {
        return request(`/api/likes/${momentId}`, { method: 'POST' })
    },
    getLikeStatus(momentId) {
        return request(`/api/likes/${momentId}`)
    },

    // ==================== 健康检查 ====================
    healthCheck() {
        return request('/api/health')
    },
}

export function resolveImageUrl(url) {
    if (!url) return ''
    if (url.startsWith('http://') || url.startsWith('https://')) return url
    if (url.startsWith('/')) return `${API_BASE}${url}`
    return url
}
