<template>
    <!-- ===== 添加/编辑书籍表单 ===== -->
    <div class="admin-books" v-if="isFormMode">
        <div class="page-header">
            <h2>{{ editingBook ? '编辑书籍' : '添加书籍' }}</h2>
            <p class="page-desc">{{ editingBook ? '修改书籍信息' : '添加一本新书到书架' }}</p>
        </div>

        <div class="book-form">
            <div class="form-group">
                <label>书名 <span class="required">*</span></label>
                <input type="text" v-model="form.title" placeholder="输入书名" class="form-input" />
            </div>
            <div class="form-group">
                <label>作者</label>
                <input type="text" v-model="form.author" placeholder="输入作者" class="form-input" />
            </div>
            <div class="form-group">
                <label>封面图片</label>
                <div class="cover-upload" @click="triggerUpload">
                    <img v-if="form.cover_url" :src="resolveImageUrl(form.cover_url)" class="cover-preview" />
                    <div v-else class="cover-placeholder">
                        <i class="fas fa-book"></i>
                        <span>点击上传封面</span>
                    </div>
                </div>
                <input type="file" ref="fileInput" accept="image/*" @change="onUpload" style="display:none" />
            </div>
            <div class="form-group">
                <label>简介</label>
                <textarea v-model="form.summary" placeholder="书籍简介..." rows="4" class="form-textarea"></textarea>
            </div>
            <div class="form-actions">
                <button class="form-btn cancel" @click="cancelForm">
                    <i class="fas fa-times"></i> 取消
                </button>
                <button class="form-btn submit" @click="handleSubmit" :disabled="submitting">
                    <i class="fas fa-check"></i>
                    <span>{{ submitting ? '保存中...' : (editingBook ? '保存修改' : '添加到书架') }}</span>
                </button>
            </div>
        </div>
    </div>

    <!-- ===== 书籍列表 ===== -->
    <div class="admin-books" v-else>
        <div class="page-header">
            <div class="header-left">
                <h2>书籍管理</h2>
                <span class="header-count">{{ books.length }} 本</span>
            </div>
            <button class="create-btn" @click="addBook">
                <i class="fas fa-plus"></i> 添加书籍
            </button>
        </div>

        <div class="loading-text" v-if="loading">加载中...</div>

        <div class="book-grid" v-else>
            <div class="book-card" v-for="book in books" :key="book.id">
                <div class="card-glow"></div>
                <div class="card-cover" v-if="book.cover_url">
                    <img :src="resolveThumbUrl(book.cover_url)" alt="" />
                </div>
                <div class="card-cover placeholder" v-else>
                    <i class="fas fa-book"></i>
                </div>
                <div class="card-body">
                    <div class="card-top">
                        <span class="card-id">#{{ book.id }}</span>
                        <span class="card-author" v-if="book.author">{{ book.author }}</span>
                    </div>
                    <div class="card-title">{{ book.title }}</div>
                    <div class="card-summary" v-if="book.summary">{{ book.summary }}</div>
                    <div class="card-footer">
                        <div class="card-meta">
                            <span class="meta-item" title="阅读量">
                                <i class="far fa-eye"></i>
                                <span class="meta-num">{{ book.view_count }}</span>
                            </span>
                            <span class="meta-divider"></span>
                            <span class="meta-item" title="点赞数">
                                <i class="far fa-heart"></i>
                                <span class="meta-num">{{ book.like_count }}</span>
                            </span>
                            <span class="meta-divider"></span>
                            <span class="meta-item">
                                <i class="far fa-calendar"></i>
                                {{ formatDate(book.created_at) }}
                            </span>
                        </div>
                        <div class="card-actions">
                            <button class="action-btn edit" @click="editBook($event, book)" title="编辑">
                                <i class="fas fa-pen"></i>
                            </button>
                            <button class="action-btn danger" @click="deleteBook($event, book.id)" title="删除">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="empty-text" v-if="!books.length">暂无书籍，点击右上角添加</div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { adminApi, resolveImageUrl, resolveThumbUrl } from '@/utils/api'
import { useToast } from '@/utils/toast'

const router = useRouter()
const route = useRoute()
const { toast } = useToast()

const isFormMode = ref(false)
const editingBook = ref(null)

// ===== 添加/编辑书籍表单 =====
const fileInput = ref(null)
const submitting = ref(false)

const form = reactive({
    title: '',
    author: '',
    cover_url: '',
    summary: '',
})

function triggerUpload() {
    fileInput.value.click()
}

async function onUpload(e) {
    const file = e.target.files[0]
    if (!file) return
    try {
        const result = await adminApi.uploadFile(file)
        form.cover_url = result.url
        toast('封面上传成功', 'success')
    } catch (e) {
        toast('封面上传失败: ' + e.message, 'error')
    }
    e.target.value = ''
}

function resetForm() {
    form.title = ''
    form.author = ''
    form.cover_url = ''
    form.summary = ''
    editingBook.value = null
    isFormMode.value = false
}

function cancelForm() {
    resetForm()
}

async function handleSubmit() {
    if (!form.title.trim()) {
        toast('请输入书名', 'error')
        return
    }

    submitting.value = true
    try {
        const data = {
            title: form.title.trim(),
            author: form.author.trim(),
            cover_url: form.cover_url || '',
            summary: form.summary || '',
        }

        if (editingBook.value) {
            await adminApi.updateBook(editingBook.value.id, data)
            toast('书籍已更新', 'success')
        } else {
            await adminApi.createBook(data)
            toast('书籍已添加到书架', 'success')
        }
        resetForm()
        await loadBooks()
    } catch (e) {
        toast('操作失败: ' + e.message, 'error')
    } finally {
        submitting.value = false
    }
}

// ===== 书籍列表 =====
const loading = ref(false)
const books = ref([])

function formatDate(dateStr) {
    if (!dateStr) return ''
    const d = new Date(dateStr)
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return `${y}.${m}.${day}`
}

function addBook() {
    editingBook.value = null
    form.title = ''
    form.author = ''
    form.cover_url = ''
    form.summary = ''
    isFormMode.value = true
}

function editBook(e, book) {
    e.stopPropagation()
    editingBook.value = book
    form.title = book.title || ''
    form.author = book.author || ''
    form.cover_url = book.cover_url || ''
    form.summary = book.summary || ''
    isFormMode.value = true
}

async function deleteBook(e, id) {
    e.stopPropagation()
    if (!confirm('确定要删除这本书吗？')) return
    try {
        await adminApi.deleteBook(id)
        toast('书籍已删除', 'success')
        books.value = books.value.filter(b => b.id !== id)
    } catch (e) {
        toast('删除失败: ' + e.message, 'error')
    }
}

async function loadBooks() {
    loading.value = true
    try {
        const res = await adminApi.getBooks()
        if (res && res.items) {
            books.value = res.items
        }
    } catch (e) {
        toast('加载书籍失败: ' + e.message, 'error')
    } finally {
        loading.value = false
    }
}

onMounted(async () => {
    await loadBooks()
})
</script>

<style scoped>
.admin-books {
    max-width: 900px;
    margin: 0 auto;
}

.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 28px;
}

.header-left {
    display: flex;
    align-items: baseline;
    gap: 12px;
}

.header-left h2 {
    font-size: 24px;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.3px;
}

.header-count {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.2);
    font-family: 'JetBrains Mono', monospace;
}

.page-desc {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.3);
    margin-top: 6px;
}

.create-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 18px;
    border-radius: 10px;
    border: none;
    background: rgba(0, 242, 192, 0.1);
    color: #00F2C0;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: inherit;
}

.create-btn i {
    font-size: 12px;
}

.create-btn:hover {
    background: rgba(0, 242, 192, 0.18);
}

.loading-text,
.empty-text {
    text-align: center;
    padding: 60px;
    color: rgba(255, 255, 255, 0.15);
    font-size: 14px;
}

/* ===== 添加/编辑书籍表单 ===== */
.book-form {
    display: flex;
    flex-direction: column;
    gap: 24px;
    max-width: 600px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-group label {
    font-size: 13px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.4);
}

.required {
    color: #ff5f56;
}

.form-input,
.form-textarea {
    padding: 12px 16px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    background: rgba(255, 255, 255, 0.02);
    color: #EFF3F8;
    font-size: 14px;
    font-family: inherit;
    outline: none;
    transition: all 0.2s ease;
}

.form-input:focus,
.form-textarea:focus {
    border-color: rgba(0, 242, 192, 0.2);
    background: rgba(255, 255, 255, 0.04);
}

.form-textarea {
    resize: vertical;
    min-height: 100px;
}

.cover-upload {
    width: 100%;
    height: 200px;
    border-radius: 14px;
    border: 2px dashed rgba(255, 255, 255, 0.08);
    overflow: hidden;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.cover-upload:hover {
    border-color: rgba(0, 242, 192, 0.2);
    background: rgba(0, 242, 192, 0.02);
}

.cover-preview {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.cover-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    color: rgba(255, 255, 255, 0.15);
}

.cover-placeholder i {
    font-size: 40px;
}

.cover-placeholder span {
    font-size: 13px;
}

.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    padding-top: 8px;
}

.form-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 24px;
    border-radius: 10px;
    border: none;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: inherit;
}

.form-btn i {
    font-size: 13px;
}

.form-btn.cancel {
    background: rgba(255, 255, 255, 0.04);
    color: rgba(255, 255, 255, 0.4);
}

.form-btn.cancel:hover {
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.6);
}

.form-btn.submit {
    background: rgba(0, 242, 192, 0.12);
    color: #00F2C0;
}

.form-btn.submit:hover {
    background: rgba(0, 242, 192, 0.2);
}

.form-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* ===== 书籍卡片 ===== */
.book-grid {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.book-card {
    display: flex;
    gap: 20px;
    padding: 16px 20px;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.book-card:hover {
    background: rgba(255, 255, 255, 0.04);
    border-color: rgba(0, 242, 192, 0.1);
}

.card-glow {
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 0% 0%, rgba(0, 242, 192, 0.02), transparent 50%);
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.4s ease;
}

.book-card:hover .card-glow {
    opacity: 1;
}

.card-cover {
    width: 80px;
    height: 110px;
    border-radius: 8px;
    overflow: hidden;
    flex-shrink: 0;
    background: rgba(255, 255, 255, 0.03);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

.card-cover img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.card-cover.placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
}

.card-cover.placeholder i {
    font-size: 28px;
    color: rgba(255, 255, 255, 0.08);
}

.card-body {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.card-top {
    display: flex;
    align-items: center;
    gap: 8px;
}

.card-id {
    font-size: 10px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.15);
    font-family: 'JetBrains Mono', monospace;
}

.card-author {
    font-size: 10px;
    padding: 1px 8px;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.04);
    color: rgba(255, 255, 255, 0.3);
    font-family: 'JetBrains Mono', monospace;
}

.card-title {
    font-size: 16px;
    font-weight: 600;
    color: #EFF3F8;
    line-height: 1.3;
}

.card-summary {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.3);
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.card-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: auto;
    padding-top: 6px;
}

.card-meta {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    color: rgba(255, 255, 255, 0.15);
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 3px;
}

.meta-item i {
    font-size: 10px;
}

.meta-divider {
    width: 2px;
    height: 2px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.08);
}

.card-actions {
    display: flex;
    gap: 4px;
}

.action-btn {
    width: 28px;
    height: 28px;
    border-radius: 6px;
    border: none;
    background: transparent;
    color: rgba(255, 255, 255, 0.15);
    font-size: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
}

.action-btn.edit:hover {
    background: rgba(0, 242, 192, 0.1);
    color: #00F2C0;
}

.action-btn.danger:hover {
    background: rgba(255, 107, 107, 0.1);
    color: #ff6b6b;
}
</style>
