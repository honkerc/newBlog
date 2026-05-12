<template>
    <div class="page">
        <div class="page-header">
            <div class="header-top">
                <div class="header-title-group">
                    <h1>一句话</h1>
                    <p class="header-desc">记录触动你的瞬间</p>
                </div>
                <div class="header-icon">
                    <i class="fas fa-quote-right"></i>
                </div>
            </div>
        </div>

        <!-- 随机展示 -->
        <div class="quote-card" v-if="latestMotto">
            <i class="fas fa-quote-left quote-icon"></i>
            <p class="quote-text">{{ latestMotto.content }}</p>
            <p class="quote-source" v-if="latestMotto.location">—— {{ latestMotto.location }}</p>
        </div>

        <!-- 输入 -->
        <div class="form-group">
            <label>写一句话</label>
            <textarea v-model="content" class="form-textarea" placeholder="今天有什么触动你的话？"
                style="min-height: 80px;"></textarea>
        </div>

        <div class="form-group">
            <label>位置（可选）</label>
            <input type="text" v-model="source" class="form-input" placeholder="书籍、电影、地点……" />
        </div>

        <button class="btn-primary" @click="submit" :disabled="submitting || !content.trim()">
            <i class="fas fa-quote-right"></i>
            <span>{{ submitting ? '提交中...' : '记录' }}</span>
        </button>

        <div class="toast success" v-if="toastMsg">{{ toastMsg }}</div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/utils/api'

const content = ref('')
const source = ref('')
const submitting = ref(false)
const toastMsg = ref('')
const latestMotto = ref(null)

onMounted(async () => {
    try {
        const res = await api.getLatestMottos()
        if (res.items && res.items.length) {
            latestMotto.value = res.items[0]
        }
    } catch (e) {
        console.error('加载语录失败:', e)
    }
})

async function submit() {
    if (!content.value.trim()) return
    submitting.value = true
    try {
        await api.createMotto({
            content: content.value.trim(),
            location: source.value.trim() || '',
            is_published: true,
        })
        toastMsg.value = '记录成功 ✨'
        content.value = ''
        source.value = ''
        setTimeout(() => toastMsg.value = '', 2000)
    } catch (e) {
        toastMsg.value = '提交失败: ' + e.message
        setTimeout(() => toastMsg.value = '', 3000)
    } finally {
        submitting.value = false
    }
}
</script>

<style scoped>
.page {
    padding-top: 8px;
}

/* ===== 页头 ===== */
.page-header {
    padding: 20px 0 24px;
    text-align: left;
}

.header-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.header-title-group h1 {
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.3px;
}

.header-desc {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.3);
    margin-top: 2px;
}

.header-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: rgba(var(--theme-rgb), 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    color: var(--accent);
}

.quote-card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: var(--radius);
    padding: 20px;
    margin-bottom: 24px;
    position: relative;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}

.quote-icon {
    font-size: 18px;
    color: var(--accent);
    opacity: 0.4;
    margin-bottom: 8px;
}

.quote-text {
    font-size: 15px;
    line-height: 1.7;
    color: var(--text);
    font-style: italic;
}

.quote-source {
    font-size: 12px;
    color: var(--text-dim);
    margin-top: 8px;
    text-align: right;
}
</style>
