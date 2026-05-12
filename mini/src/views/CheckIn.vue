<template>
    <div class="page">
        <div class="page-header">
            <div class="header-top">
                <div class="header-date">
                    <span class="date-day">{{ dayNum }}</span>
                    <div class="date-info">
                        <span class="date-weekday">{{ weekday }}</span>
                        <span class="date-month">{{ monthYear }}</span>
                    </div>
                </div>
                <div class="header-time">
                    <i class="fas fa-clock"></i>
                    <span>{{ timeStr }}</span>
                </div>
            </div>
        </div>

        <!-- 类别选择 -->
        <div class="category-grid">
            <div v-for="cat in categories" :key="cat.value" class="category-btn"
                :class="{ active: selectedCategory === cat.value }" @click="selectedCategory = cat.value">
                <div class="cat-icon" :class="cat.value">
                    <i :class="cat.icon"></i>
                </div>
                <span>{{ cat.label }}</span>
            </div>
        </div>

        <!-- 内容输入 -->
        <div class="form-group fill">
            <label>打卡内容</label>
            <textarea v-model="content" class="form-textarea fill" placeholder="今天做了什么？有什么感受？"></textarea>
        </div>

        <!-- 图片上传 -->
        <div class="form-group">
            <label>照片（可选）</label>
            <div class="upload-area">
                <div class="image-list" v-if="images.length">
                    <div class="image-item" v-for="(img, i) in images" :key="i">
                        <img :src="img" alt="" />
                        <button class="img-remove" @click="images.splice(i, 1)">&times;</button>
                    </div>
                </div>
                <button class="upload-btn" @click="pickImage">
                    <i class="fas fa-camera"></i>
                    <span>{{ images.length ? '继续添加' : '拍照或选择照片' }}</span>
                </button>
            </div>
        </div>

        <!-- 提交 -->
        <button class="btn-primary" @click="submit" :disabled="submitting || !selectedCategory || !content.trim()">
            <i class="fas fa-check-circle"></i>
            <span>{{ submitting ? '提交中...' : '打卡' }}</span>
        </button>

        <!-- Toast -->
        <div class="toast success" v-if="toastMsg">{{ toastMsg }}</div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { api, resolveImageUrl } from '@/utils/api'

const now = new Date()
const dayNum = now.getDate()
const weekday = now.toLocaleDateString('zh-CN', { weekday: 'long' })
const monthYear = now.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long' })
const timeStr = now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })

const categories = [
    { value: 'moment', label: '朋友圈', icon: 'fas fa-camera' },
    { value: 'sports', label: '运动', icon: 'fas fa-running' },
    { value: 'daily', label: '日常', icon: 'fas fa-sun' },
    { value: 'study', label: '学习', icon: 'fas fa-graduation-cap' },
]

const selectedCategory = ref('')
const content = ref('')
const images = ref([])
const submitting = ref(false)
const toastMsg = ref('')

function pickImage() {
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = 'image/*'
    input.multiple = true
    input.onchange = async () => {
        for (const file of input.files) {
            try {
                const res = await api.uploadFile(file)
                images.value.push(resolveImageUrl(res.url))
            } catch (e) {
                console.error('上传失败:', e)
            }
        }
    }
    input.click()
}

async function submit() {
    if (!selectedCategory.value || !content.value.trim()) return
    submitting.value = true
    try {
        await api.createCheckIn({
            category: selectedCategory.value,
            content: content.value.trim(),
            images: images.value.map(u => u.replace('http://localhost:8000', '')).join(','),
            is_published: true,
        })
        toastMsg.value = '打卡成功 🎉'
        content.value = ''
        images.value = []
        selectedCategory.value = ''
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

.header-date {
    display: flex;
    align-items: center;
    gap: 12px;
}

.header-time {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.5);
    font-family: 'JetBrains Mono', 'SF Mono', monospace;
    letter-spacing: 0.5px;
    background: rgba(255, 255, 255, 0.04);
    padding: 6px 14px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.04);
}

.header-time i {
    font-size: 12px;
    opacity: 0.6;
}

.date-day {
    font-size: 42px;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1;
    letter-spacing: -1px;
}

.date-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.date-weekday {
    font-size: 14px;
    font-weight: 600;
    color: #EFF3F8;
}

.date-month {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.3);
}

/* ===== 类别网格 ===== */
.category-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 16px;
    flex-shrink: 0;
}

.category-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 16px 12px;
    border-radius: var(--radius);
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.06);
    cursor: pointer;
    transition: all 0.25s ease;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}

.category-btn:active {
    transform: scale(0.96);
}

.category-btn.active {
    border-color: var(--accent);
    background: rgba(var(--theme-rgb), 0.08);
}

.cat-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}

.cat-icon.moment {
    background: rgba(0, 242, 192, 0.12);
    color: #00F2C0;
}

.cat-icon.sports {
    background: rgba(255, 107, 107, 0.12);
    color: #ff6b6b;
}

.cat-icon.study {
    background: rgba(162, 155, 254, 0.12);
    color: #a29bfe;
}

.cat-icon.daily {
    background: rgba(253, 203, 110, 0.12);
    color: #fdcb6e;
}


.category-btn span {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-secondary);
}

.category-btn.active span {
    color: var(--text);
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

/* ===== 图片上传 ===== */
.upload-area {
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex-shrink: 0;
}

.image-list {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}

.image-item {
    position: relative;
    width: 72px;
    height: 72px;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
}


.image-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.img-remove {
    position: absolute;
    top: 2px;
    right: 2px;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: none;
    background: rgba(0, 0, 0, 0.5);
    color: #fff;
    font-size: 14px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 1;
}

.upload-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 12px;
    border-radius: 10px;
    border: 1px dashed var(--border);
    background: var(--bg-surface);
    color: var(--text-dim);
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s;
    font-family: inherit;
}

.upload-btn:hover {
    border-color: var(--accent);
    color: var(--accent);
}

.btn-primary {
    flex-shrink: 0;
}
</style>
