<template>
    <div class="settings-page">
        <div class="page-header">
            <button class="btn-back" @click="goBack">
                <i class="fas fa-arrow-left"></i>
            </button>
            <h1>设置</h1>
            <div style="width: 36px;"></div>
        </div>

        <div class="settings-section">
            <div class="section-title">服务器配置</div>
            <div class="form-group">
                <label>后端 API 地址</label>
                <input type="text" v-model="serverUrl" class="form-input" placeholder="http://127.0.0.1:8000"
                    @keyup.enter="saveSettings" />
                <p class="form-hint">输入后端服务的完整地址，例如 http://192.168.1.100:8000</p>
            </div>

            <div class="form-group">
                <label>连接测试</label>
                <button class="btn-secondary" @click="testConnection" :disabled="testing">
                    {{ testing ? '测试中...' : '测试连接' }}
                </button>
                <p class="form-hint" v-if="testResult" :class="testResult.ok ? 'text-success' : 'text-error'">
                    {{ testResult.msg }}
                </p>
            </div>

            <button class="btn-primary" @click="saveSettings">
                <i class="fas fa-save"></i>
                保存设置
            </button>
        </div>

        <div class="settings-section">
            <div class="section-title">关于</div>
            <div class="about-info">
                <div class="info-row">
                    <span>当前地址</span>
                    <span class="info-value">{{ currentUrl }}</span>
                </div>
                <div class="info-row">
                    <span>版本</span>
                    <span class="info-value">1.0.0</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const serverUrl = ref('')
const testing = ref(false)
const testResult = ref(null)
const currentUrl = ref('')

const STORAGE_KEY = 'mini_server_url'
const DEFAULT_URL = 'https://honkerc.cn'

onMounted(() => {
    currentUrl.value = localStorage.getItem(STORAGE_KEY) || DEFAULT_URL
    serverUrl.value = currentUrl.value
})

function goBack() {
    router.back()
}

async function testConnection() {
    let url = serverUrl.value.trim()
    if (!url) {
        testResult.value = { ok: false, msg: '请输入服务器地址' }
        return
    }
    // 去掉末尾的 /
    url = url.replace(/\/+$/, '')
    testing.value = true
    testResult.value = null
    try {
        const res = await fetch(`${url}/api/health`, { signal: AbortSignal.timeout(5000) })
        if (res.ok) {
            testResult.value = { ok: true, msg: '✅ 连接成功！' }
        } else {
            testResult.value = { ok: false, msg: `❌ 服务器返回状态码 ${res.status}` }
        }
    } catch (e) {
        testResult.value = { ok: false, msg: `❌ 连接失败：${e.message}` }
    } finally {
        testing.value = false
    }
}

function saveSettings() {
    let url = serverUrl.value.trim()
    if (!url) {
        url = DEFAULT_URL
    }
    // 去掉末尾的 /
    url = url.replace(/\/+$/, '')
    localStorage.setItem(STORAGE_KEY, url)
    currentUrl.value = url
    serverUrl.value = url
    testResult.value = { ok: true, msg: '✅ 设置已保存' }
}
</script>

<style scoped>
.settings-page {
    padding: 0 16px 80px;
}

.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 0;
}

.page-header h1 {
    font-size: 18px;
    font-weight: 700;
}

.btn-back {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    border: none;
    background: var(--bg-surface);
    color: var(--text);
    font-size: 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
}

.btn-back:active {
    background: var(--bg-surface-hover);
}

.settings-section {
    margin-top: 24px;
}

.section-title {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-tertiary);
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.form-hint {
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 6px;
}

.text-success {
    color: var(--accent) !important;
}

.text-error {
    color: #ff6b6b !important;
}

.btn-secondary {
    width: 100%;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid var(--border);
    background: var(--bg-surface);
    color: var(--text);
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    font-family: inherit;
}

.btn-secondary:active {
    background: var(--bg-surface-hover);
}

.btn-secondary:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

.about-info {
    background: var(--bg-card);
    border-radius: var(--radius);
    overflow: hidden;
}

.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 16px;
    font-size: 14px;
    border-bottom: 1px solid var(--border);
}

.info-row:last-child {
    border-bottom: none;
}

.info-value {
    color: var(--text-secondary);
    font-size: 13px;
    max-width: 60%;
    text-align: right;
    word-break: break-all;
}
</style>
