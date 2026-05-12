
/**
 * ============================================
 * 认证状态管理 - 对接后端 API
 * ============================================
 * 管理管理员登录状态，与后端 JWT 认证交互。
 * 包含用户信息（头像、昵称、简介等）。
 * 
 * 使用方式:
 *   import { useAuth } from '@/stores/auth'
 *   const { auth, login, logout } = useAuth()
 */

import { reactive } from 'vue'

// ===== 后端 API 地址（自动判断开发/生产环境） =====
const isDev = window.location.port === '8080' || window.location.port === '3001'
const API_BASE = isDev ? `http://${window.location.hostname}:8000` : ''

// ===== 存储键名 =====
const TOKEN_KEY = 'admin_token'
const USERNAME_KEY = 'admin_username'
const NICKNAME_KEY = 'admin_nickname'
const AVATAR_KEY = 'admin_avatar'

/**
 * 认证状态
 */
const auth = reactive({
    /** 是否已登录 */
    isAdmin: !!localStorage.getItem(TOKEN_KEY),
    /** 用户名 */
    username: localStorage.getItem(USERNAME_KEY) || '',
    /** 昵称 */
    nickname: localStorage.getItem(NICKNAME_KEY) || '',
    /** 头像URL */
    avatar: localStorage.getItem(AVATAR_KEY) || '',
})

/**
 * 认证相关方法
 */
export function useAuth() {
    /**
     * 登录 - 调用后端 API
     */
    async function login(username, password) {
        try {
            const res = await fetch(`${API_BASE}/api/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            })

            if (!res.ok) {
                const err = await res.json()
                throw new Error(err.detail || '登录失败')
            }

            const data = await res.json()

            // 保存令牌和用户信息
            localStorage.setItem(TOKEN_KEY, data.access_token)
            localStorage.setItem(USERNAME_KEY, data.username)
            localStorage.setItem(NICKNAME_KEY, data.nickname || '')
            localStorage.setItem(AVATAR_KEY, data.avatar || '')

            // 更新响应式状态
            auth.isAdmin = true
            auth.username = data.username
            auth.nickname = data.nickname || ''
            auth.avatar = data.avatar || ''

            return true
        } catch (e) {
            console.error('登录失败:', e)
            throw e
        }
    }

    /**
     * 登出 - 清除本地存储
     */
    function logout() {
        localStorage.removeItem(TOKEN_KEY)
        localStorage.removeItem(USERNAME_KEY)
        localStorage.removeItem(NICKNAME_KEY)
        localStorage.removeItem(AVATAR_KEY)
        auth.isAdmin = false
        auth.username = ''
        auth.nickname = ''
        auth.avatar = ''
    }

    /**
     * 获取认证令牌
     */
    function getToken() {
        return localStorage.getItem(TOKEN_KEY)
    }

    /**
     * 验证令牌是否有效
     */
    async function verifyToken() {
        const token = getToken()
        if (!token) return false

        try {
            const res = await fetch(`${API_BASE}/api/auth/verify`, {
                headers: { 'Authorization': `Bearer ${token}` },
            })
            if (res.ok) {
                const data = await res.json()
                // 同步更新用户信息
                if (data.nickname) {
                    localStorage.setItem(NICKNAME_KEY, data.nickname)
                    auth.nickname = data.nickname
                }
                if (data.avatar) {
                    localStorage.setItem(AVATAR_KEY, data.avatar)
                    auth.avatar = data.avatar
                }
            }
            return res.ok
        } catch {
            return false
        }
    }

    /**
     * 获取用户完整信息
     */
    async function fetchProfile() {
        const token = getToken()
        if (!token) return null

        try {
            const res = await fetch(`${API_BASE}/api/auth/profile`, {
                headers: { 'Authorization': `Bearer ${token}` },
            })
            if (!res.ok) return null
            return await res.json()
        } catch {
            return null
        }
    }

    /**
     * 更新用户信息
     */
    async function updateProfile(data) {
        const token = getToken()
        if (!token) throw new Error('未登录')

        const res = await fetch(`${API_BASE}/api/auth/profile`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(data),
        })

        if (!res.ok) {
            const err = await res.json()
            throw new Error(err.detail || '更新失败')
        }

        const profile = await res.json()

        // 更新本地存储和状态
        if (profile.nickname) {
            localStorage.setItem(NICKNAME_KEY, profile.nickname)
            auth.nickname = profile.nickname
        }
        if (profile.avatar !== undefined) {
            localStorage.setItem(AVATAR_KEY, profile.avatar)
            auth.avatar = profile.avatar
        }

        return profile
    }

    return { auth, login, logout, getToken, verifyToken, fetchProfile, updateProfile, API_BASE }
}
