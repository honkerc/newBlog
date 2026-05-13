<template>
    <div class="login-page">
        <div class="login-header">
            <div class="login-logo">
                <i class="fas fa-check-circle"></i>
            </div>
            <h1>Mini</h1>
            <p>打卡助手</p>
        </div>

        <div class="login-form">
            <div class="form-group">
                <label>用户名</label>
                <input type="text" v-model="username" class="form-input" placeholder="输入用户名"
                    @keyup.enter="handleLogin" />
            </div>
            <div class="form-group">
                <label>密码</label>
                <input type="password" v-model="password" class="form-input" placeholder="输入密码"
                    @keyup.enter="handleLogin" />
            </div>

            <div class="error-msg" v-if="error">{{ error }}</div>

            <button class="btn-primary" @click="handleLogin" :disabled="loading">
                <i class="fas fa-sign-in-alt"></i>
                {{ loading ? '登录中...' : '登录' }}
            </button>

            <button class="btn-settings" @click="goSettings">
                <i class="fas fa-cog"></i>
                服务器设置
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '@/utils/api'

const router = useRouter()
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
    if (!username.value || !password.value) {
        error.value = '请输入用户名和密码'
        return
    }

    loading.value = true
    error.value = ''

    try {
        const data = await api.login(username.value, password.value)
        localStorage.setItem('mini_token', data.access_token)
        router.push('/')
    } catch (e) {
        error.value = e.message || '登录失败'
    } finally {
        loading.value = false
    }
}

function goSettings() {
    router.push('/settings')
}
</script>

<style scoped>
.login-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 24px;
}

.login-header {
    text-align: center;
    margin-bottom: 40px;
}

.login-logo {
    width: 72px;
    height: 72px;
    border-radius: 22px;
    background: rgba(255, 255, 255, 0.06);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}

.login-logo i {
    font-size: 36px;
    color: var(--accent);
}

.login-header h1 {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: var(--text);
}

.login-header p {
    font-size: 14px;
    color: var(--text-secondary);
    margin-top: 4px;
}

.login-form {
    width: 100%;
    max-width: 320px;
}

.login-form .form-group {
    margin-bottom: 16px;
}

.login-form .form-input {
    background: var(--bg-surface);
    border: 1px solid var(--border);
}

.error-msg {
    font-size: 13px;
    color: #ff6b6b;
    text-align: center;
    padding: 8px;
    background: rgba(255, 107, 107, 0.08);
    border-radius: 8px;
    margin-bottom: 16px;
}

.btn-settings {
    width: 100%;
    padding: 12px;
    margin-top: 12px;
    border-radius: 10px;
    border: 1px solid var(--border);
    background: transparent;
    color: var(--text-tertiary);
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    font-family: inherit;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.btn-settings:active {
    background: var(--bg-surface);
    color: var(--text-secondary);
}
</style>
