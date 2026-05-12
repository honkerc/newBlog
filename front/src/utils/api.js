/**
 * ============================================
 * API 工具 - 封装后端接口调用
 * ============================================
 * 统一管理 API 地址和请求方法。
 */

/**
 * API 基础地址
 * - 生产环境（Nginx 反向代理）：使用同源地址（空字符串）
 * - 开发环境：使用 localhost:8000
 *
 * 通过 window.location.port 判断：
 *   8080/3001 → 开发环境，需要加端口
 *   其他       → 生产环境（Nginx 已代理 /api/ 到后端）
 */
const isDev = window.location.port === '8080' || window.location.port === '3001'
const API_BASE = isDev ? `http://${window.location.hostname}:8000` : ''

/**
 * 解析图片 URL
 * 将后端返回的相对路径（如 /uploads/xxx.jpg）转为完整 URL
 */
export function resolveImageUrl(url) {
    if (!url) return ''
    if (url.startsWith('http://') || url.startsWith('https://')) return url
    if (url.startsWith('/')) return `${API_BASE}${url}`
    return url
}

/**
 * 解析缩略图 URL
 * 将原始图片 URL 转为缩略图 URL（加 thumb_ 前缀）。
 * 如果已经是缩略图或无法转换，返回原 URL。
 * 前端默认使用缩略图显示，点击图片时才加载原始图片。
 */
export function resolveThumbUrl(url) {
    if (!url) return ''
    const fullUrl = resolveImageUrl(url)
    // 从完整 URL 中提取路径部分
    const uploadsMarker = '/uploads/'
    const idx = fullUrl.indexOf(uploadsMarker)
    if (idx === -1) return fullUrl
    const base = fullUrl.substring(0, idx + uploadsMarker.length)
    const filename = fullUrl.substring(idx + uploadsMarker.length)
    // 如果已经是缩略图，不再重复添加
    if (filename.startsWith('thumb_')) return fullUrl
    // 构造缩略图文件名
    const dotIdx = filename.lastIndexOf('.')
    const name = dotIdx > 0 ? filename.substring(0, dotIdx) : filename
    return `${base}thumb_${name}.jpg`
}

/**
 * 获取认证令牌
 */
function getToken() {
    return localStorage.getItem('admin_token')
}

/**
 * 通用请求方法
 */
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

/**
 * 公开 API - 无需登录
 */
export const publicApi = {
    // 文章
    getPosts(params = {}) {
        const query = new URLSearchParams(params).toString()
        return request(`/api/posts?${query}`)
    },
    getLatestPosts() {
        return request('/api/posts/latest')
    },
    getPost(id) {
        return request(`/api/posts/${id}`)
    },
    getCategories() {
        return request('/api/posts/categories')
    },
    // 动态
    getMoments(params = {}) {
        const query = new URLSearchParams(params).toString()
        return request(`/api/moments?${query}`)
    },
    getLatestMoments() {
        return request('/api/moments/latest')
    },
    getMomentCategories() {
        return request('/api/moments/categories')
    },
    // 读书
    getBooks() {
        return request('/api/books')
    },
    getBookDetail(tag) {
        return request(`/api/books/by-tag/${encodeURIComponent(tag)}`)
    },
    // 搜索
    search(params = {}) {
        const query = new URLSearchParams(params).toString()
        return request(`/api/search?${query}`)
    },
    // 一句话
    getMottos(params = {}) {
        const query = new URLSearchParams(params).toString()
        return request(`/api/mottos?${query}`)
    },
    getLatestMottos() {
        return request('/api/mottos/latest')
    },
    // 动态 Feed（所有动态统一时间线）
    getFeed(params = {}) {
        const query = new URLSearchParams(params).toString()
        return request(`/api/feed?${query}`)
    },
    // 用户信息（公开，无需登录）
    getProfile() {
        return request('/api/auth/public')
    },
    // 热力图
    getHeatmap(days = 60) {
        return request(`/api/heatmap?days=${days}`)
    },
    // 健康检查
    healthCheck() {
        return request('/api/health')
    },
}

/**
 * 点赞 API - 无需登录，基于 IP
 */
export const likeApi = {
    toggleLike(momentId) {
        return request(`/api/likes/${momentId}`, { method: 'POST' })
    },
    getLikeStatus(momentId) {
        return request(`/api/likes/${momentId}`)
    },
}

/**
 * 管理 API - 需要登录
 */
export const adminApi = {
    // 文章
    getPosts(params = {}) {
        const query = new URLSearchParams(params).toString()
        return request(`/api/posts/admin/all?${query}`)
    },
    // 书籍
    getBooks() {
        return request('/api/books')
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
    getPost(id) {
        return request(`/api/posts/${id}`)
    },
    getStats() {
        return request('/api/posts/stats')
    },
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
        return request(`/api/posts/${id}`, {
            method: 'DELETE',
        })
    },
    // 动态
    getMoments(params = {}) {
        const query = new URLSearchParams(params).toString()
        return request(`/api/moments?${query}`)
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
    // 评论
    getComments(postId) {
        return request(`/api/comments/${postId}`)
    },
    createComment(postId, data) {
        return request(`/api/comments/${postId}`, {
            method: 'POST',
            body: JSON.stringify(data),
        })
    },
    deleteComment(commentId) {
        return request(`/api/comments/${commentId}`, {
            method: 'DELETE',
        })
    },
    // 标签
    getTags() {
        return request('/api/tags')
    },
    createTag(name) {
        return request('/api/tags', {
            method: 'POST',
            body: JSON.stringify({ name }),
        })
    },
    deleteTag(tagId) {
        return request(`/api/tags/${tagId}`, {
            method: 'DELETE',
        })
    },
    // 文件上传
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
    // 热力图
    getHeatmap(days = 60) {
        return request(`/api/heatmap?days=${days}`)
    },
    // 用户
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
    // 一句话
    getMottos(params = {}) {
        const query = new URLSearchParams(params).toString()
        return request(`/api/mottos?${query}`)
    },
    createMotto(data) {
        return request('/api/mottos', {
            method: 'POST',
            body: JSON.stringify(data),
        })
    },
    updateMotto(id, data) {
        return request(`/api/mottos/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        })
    },
    deleteMotto(id) {
        return request(`/api/mottos/${id}`, {
            method: 'DELETE',
        })
    },
    // 令牌验证
    verifyToken() {
        return request('/api/auth/verify')
    },
    // 健康检查
    healthCheck() {
        return request('/api/health')
    },
}
