<template>
    <div class="page">
        <div class="page-header">
            <div class="header-top">
                <div class="header-title-group">
                    <h1>精进</h1>
                    <p class="header-desc">每天进步一点点</p>
                </div>
                <div class="header-icon">
                    <i class="fas fa-chart-line"></i>
                </div>
            </div>
        </div>

        <div class="form-group fill">
            <label>今天学到了什么？</label>
            <textarea v-model="content" class="form-textarea fill" placeholder="记录今天的收获、感悟、进步……"></textarea>
        </div>

        <button class="btn-primary" @click="submit" :disabled="submitting || !content.trim()">
            <i class="fas fa-chart-line"></i>
            <span>{{ submitting ? '提交中...' : '记录' }}</span>
        </button>

        <div class="toast success" v-if="toastMsg">{{ toastMsg }}</div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/utils/api'

const content = ref('')
const submitting = ref(false)
const toastMsg = ref('')
const editingId = ref(null)

function getDateStr() {
    const d = new Date()
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return `${y}${m}${day}`
}

function getTodayTitle() {
    return `精进${getDateStr()}`
}

onMounted(async () => {
    try {
        const res = await api.getPosts({ category: '精进', page_size: 50 })
        const todayTitle = getTodayTitle()
        const existing = (res.items || []).find(p => p.title === todayTitle)
        if (existing) {
            editingId.value = existing.id
            content.value = existing.content || ''
        }
    } catch (e) {
        console.error('加载今日精进失败:', e)
    }
})

async function submit() {
    if (!content.value.trim()) return
    submitting.value = true
    try {
        const data = {
            title: getTodayTitle(),
            content: content.value.trim(),
            category: '精进',
            tag: '精进',
            cover_url: '',
            is_published: true,
            is_book: false,
        }

        if (editingId.value) {
            await api.updatePost(editingId.value, data)
            toastMsg.value = '已更新 🎉'
        } else {
            await api.createPost(data)
            toastMsg.value = '记录成功 🎉'
        }

        content.value = ''
        editingId.value = null
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
    padding-top: 4px;
    display: flex;
    flex-direction: column;
    min-height: calc(100vh - 80px - var(--nav-height));
}

/* ===== 页头 ===== */
.page-header {
    padding: 20px 0 24px;
    text-align: left;
    flex-shrink: 0;
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

/* ===== 表单撑满 ===== */
.form-group.fill {
    flex: 1;
    display: flex;
    flex-direction: column;
    margin-bottom: 12px;
}

.form-group.fill .form-textarea.fill {
    flex: 1;
    min-height: 0;
    resize: none;
}

.btn-primary {
    flex-shrink: 0;
}
</style>
