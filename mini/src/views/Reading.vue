<template>
    <div class="page">
        <div class="page-header">
            <div class="header-top">
                <div class="header-title-group">
                    <h1>读书</h1>
                    <p class="header-desc">记录阅读的足迹</p>
                </div>
                <div class="header-icon">
                    <i class="fas fa-book-open"></i>
                </div>
            </div>
        </div>

        <!-- 选择书籍 -->
        <div class="form-group">
            <label>选择书籍</label>
            <div class="select-wrap">
                <select v-model="selectedBookId" class="form-select">
                    <option value="">-- 选择书籍 --</option>
                    <option v-for="book in books" :key="book.id" :value="book.id">
                        {{ book.title }} {{ book.author ? '- ' + book.author : '' }}
                    </option>
                </select>
                <i class="fas fa-chevron-down select-arrow"></i>
            </div>
        </div>

        <div class="form-group fill">
            <label>读后感 / 笔记</label>
            <textarea v-model="notes" class="form-textarea fill" placeholder="有什么想记录的？"></textarea>
        </div>

        <button class="btn-primary" @click="submit" :disabled="submitting || !selectedBookId">
            <i class="fas fa-book-open"></i>
            <span>{{ submitting ? '提交中...' : '记录' }}</span>
        </button>

        <div class="toast success" v-if="toastMsg">{{ toastMsg }}</div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/utils/api'

const books = ref([])
const selectedBookId = ref('')
const notes = ref('')
const submitting = ref(false)
const toastMsg = ref('')

onMounted(async () => {
    try {
        const res = await api.getBooks({ page_size: 100 })
        books.value = res.items || []
    } catch (e) {
        console.error('加载书籍列表失败:', e)
    }
})

async function submit() {
    if (!selectedBookId.value) return
    submitting.value = true
    try {
        const book = books.value.find(b => b.id === Number(selectedBookId.value))
        if (!book) return

        const baseTitle = `读书笔记 - ${book.title}`
        let title = baseTitle
        const existing = await api.getPosts({ category: '读书', tag: book.title, page_size: 50 })
        const existingTitles = (existing.items || []).map(p => p.title)
        if (existingTitles.includes(title)) {
            let i = 1
            while (existingTitles.includes(`${baseTitle}（${i}）`)) {
                i++
            }
            title = `${baseTitle}（${i}）`
        }

        await api.createPost({
            title,
            content: notes.value.trim(),
            category: '读书',
            tag: book.title,
            is_published: true,
            is_book: false,
        })

        toastMsg.value = '记录成功 📚'
        notes.value = ''
        selectedBookId.value = ''
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

/* ===== 选择器 ===== */
.select-wrap {
    position: relative;
}

.form-select {
    width: 100%;
    padding: 12px 14px;
    padding-right: 36px;
    border-radius: 10px;
    border: 1px solid var(--border);
    background: var(--bg-surface);
    color: var(--text);
    font-size: 15px;
    font-family: inherit;
    outline: none;
    appearance: none;
    -webkit-appearance: none;
    cursor: pointer;
    transition: border-color 0.2s;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}

.form-select:focus {
    border-color: var(--accent);
}

.form-select option {
    background: #354752;
    color: #FFFFFF;
}

.select-arrow {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-dim);
    font-size: 12px;
    pointer-events: none;
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
