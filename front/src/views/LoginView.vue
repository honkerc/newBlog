<template>
    <div class="login-page">
        <div class="login-header">
            <div class="login-logo">
                <i class="fas fa-feather-alt"></i>
            </div>
            <h1>魂牵梦绕</h1>
            <p>管理后台</p>
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
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/stores/auth'

const router = useRouter()
const { login } = useAuth()

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
        await login(username.value, password.value)
        router.push('/admin')
    } catch (e) {
        error.value = e.message || '登录失败，请检查用户名和密码'
    } finally {
        loading.value = false
    }
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
    color: var(--theme);
}

.login-header h1 {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: var(--text-primary);
}

.login-header p {
    font-size: 14px;
    color: var(--text-muted);
    margin-top: 4px;
}

.login-form {
    width: 100%;
    max-width: 320px;
}

.form-group {
    margin-bottom: 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-group label {
    font-size: 13px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.45);
    letter-spacing: 0.3px;
}

.form-input {
    width: 100%;
    padding: 12px 16px;
    border-radius: 12px;
    border: 1px solid var(--border-color);
    background: var(--bg-surface);
    color: var(--text-secondary);
    font-size: 14px;
    font-family: inherit;
    outline: none;
    transition: all var(--transition);
    box-sizing: border-box;
}

.form-input:focus {
    border-color: var(--theme-border);
    background: var(--bg-surface-hover);
}

.form-input::placeholder {
    color: var(--text-dim);
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

.btn-primary {
    width: 100%;
    padding: 12px 28px;
    border-radius: 12px;
    border: none;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: all var(--transition);
    font-family: inherit;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: var(--theme-light);
    color: var(--theme);
    border: 1px solid var(--theme-border);
}

.btn-primary:hover:not(:disabled) {
    background: rgba(var(--theme-rgb), 0.25);
    transform: translateY(-1px);
}

.btn-primary:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}
</style>
