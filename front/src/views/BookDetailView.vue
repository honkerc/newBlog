<template>
    <div class="book-detail-page">
        <!-- 骨架屏 -->
        <div class="skeleton-book-detail" v-if="loading">
            <div class="skeleton-book-hero">
                <Skeleton type="rect" width="200px" height="280px" borderRadius="16px" />
                <div class="skeleton-book-info">
                    <Skeleton type="text" width="60px" height="12px" />
                    <Skeleton type="title" width="80%" height="28px" />
                    <Skeleton type="text" width="100%" />
                    <Skeleton type="text" width="90%" />
                    <div class="skeleton-book-meta">
                        <Skeleton type="text" width="80px" height="12px" />
                        <Skeleton type="text" width="80px" height="12px" />
                    </div>
                </div>
            </div>
            <div class="skeleton-book-content">
                <Skeleton type="text" width="100%" />
                <Skeleton type="text" width="100%" />
                <Skeleton type="text" width="75%" />
                <div style="height: 16px"></div>
                <Skeleton type="text" width="100%" />
                <Skeleton type="text" width="85%" />
                <Skeleton type="text" width="100%" />
                <Skeleton type="text" width="60%" />
            </div>
        </div>

        <template v-else-if="book">

            <!-- 返回链接 -->
            <div class="back-link" @click="goBack">
                <i class="fas fa-arrow-left"></i> 返回书架
            </div>

            <!-- 书籍头部 -->
            <div class="book-hero">
                <div class="hero-cover" v-if="book.cover_url">
                    <img :src="resolveThumbUrl(book.cover_url)" alt="" />
                </div>
                <div class="hero-info">
                    <div class="hero-tags">
                        <span class="hero-cat">📖 读书</span>
                        <span class="hero-author" v-if="book.author">{{ book.author }}</span>
                        <span class="hero-id">#{{ book.id }}</span>
                    </div>
                    <h1 class="hero-title">{{ book.title }}</h1>
                    <p class="hero-summary" v-if="book.summary">{{ book.summary }}</p>
                    <div class="hero-meta">
                        <span class="meta-item">
                            <i class="far fa-eye"></i> {{ book.view_count }}
                        </span>
                        <span class="meta-dot"></span>
                        <span class="meta-item">
                            <i class="far fa-heart"></i> {{ book.like_count }}
                        </span>
                        <span class="meta-dot"></span>
                        <span class="meta-item">
                            <i class="far fa-calendar"></i> {{ formatDate(book.created_at) }}
                        </span>
                    </div>
                </div>
            </div>

            <!-- 书籍简介（支持 Markdown） -->
            <div class="book-content" v-if="book.summary">
                <div class="content-head">
                    <i class="fas fa-align-left"></i> 书籍简介
                </div>
                <div class="content-body" v-html="renderMarkdown(book.summary)"></div>
            </div>

            <!-- 读书笔记 -->
            <div class="notes-section" v-if="notes.length">
                <div class="notes-head">
                    <i class="fas fa-pen-fancy"></i> 读书笔记
                    <span class="notes-count">{{ notes.length }} 篇</span>
                </div>

                <div class="notes-list">
                    <div class="note-item" v-for="note in notes" :key="note.id" @click="goToNote(note.id)">
                        <div class="note-num">{{ note.id }}</div>
                        <div class="note-info">
                            <div class="note-title">{{ note.title }}</div>
                            <div class="note-summary">{{ note.summary }}</div>
                            <div class="note-meta">
                                <span class="meta-item">
                                    <i class="far fa-eye"></i> {{ note.view_count }}
                                </span>
                                <span class="meta-dot"></span>
                                <span class="meta-item">
                                    <i class="far fa-heart"></i> {{ note.like_count }}
                                </span>
                                <span class="meta-dot"></span>
                                <span class="meta-item">
                                    <i class="far fa-calendar"></i> {{ formatDate(note.created_at) }}
                                </span>
                            </div>
                        </div>
                        <div class="note-arrow">
                            <i class="fas fa-arrow-right"></i>
                        </div>
                    </div>
                </div>
            </div>

            <div class="empty-text" v-else-if="!loading">暂无读书笔记</div>
        </template>

        <div class="empty-text" v-else-if="!loading">书籍不存在</div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { publicApi, resolveImageUrl, resolveThumbUrl } from '@/utils/api'
import Skeleton from '@/components/Skeleton.vue'

const route = useRoute()
const router = useRouter()
const loading = ref(true)
const book = ref(null)
const notes = ref([])

function goBack() {
    router.push('/reading')
}

function goToNote(id) {
    router.push(`/post/${id}`)
}

function formatDate(dateStr) {
    if (!dateStr) return ''
    const d = new Date(dateStr)
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return `${y}.${m}.${day}`
}

function renderMarkdown(content) {
    if (!content) return ''
    let html = content
        .replace(/^### (.+)$/gm, '<h3>$1</h3>')
        .replace(/^## (.+)$/gm, '<h2>$1</h2>')
        .replace(/^# (.+)$/gm, '<h1>$1</h1>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        .replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
        .replace(/^- (.+)$/gm, '<li>$1</li>')
        .replace(/^\d\. (.+)$/gm, '<li>$1</li>')
        .replace(/\n\n/g, '</p><p>')
        .replace(/^(.+)$/gm, (m) => {
            if (m.startsWith('<')) return m
            return m
        })
    return '<p>' + html + '</p>'
}

onMounted(async () => {
    try {
        const tag = route.params.tag
        const res = await publicApi.getBookDetail(tag)
        book.value = res.book || null
        notes.value = res.notes || []
    } catch (e) {
        console.error('加载书籍详情失败:', e)
    } finally {
        loading.value = false
    }
})
</script>

<style scoped>
.book-detail-page {
    padding: 0 20px 60px;
}

/* ===== 骨架屏 ===== */
.skeleton-book-detail {
    padding: 40px 0;
}

.skeleton-book-hero {
    display: flex;
    gap: 32px;
    padding-bottom: 32px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    margin-bottom: 32px;
}

.skeleton-book-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 10px;
    justify-content: center;
}

.skeleton-book-meta {
    display: flex;
    gap: 12px;
    margin-top: 4px;
}

.skeleton-book-content {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

/* ===== 返回链接 ===== */
.back-link {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 40px 0 24px;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.3);
    cursor: pointer;
    transition: color 0.2s ease;
}

.back-link i {
    font-size: 11px;
}

.back-link:hover {
    color: #00F2C0;
}

/* ===== 书籍头部 ===== */
.book-hero {
    display: flex;
    gap: 32px;
    padding-bottom: 32px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    margin-bottom: 32px;
}

.hero-cover {
    flex-shrink: 0;
    width: 180px;
    aspect-ratio: 3 / 4;
    border-radius: 8px;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.03);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 0 2px 8px rgba(0, 0, 0, 0.3);
}

.hero-cover img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.hero-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.hero-tags {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
}

.hero-cat {
    font-size: 12px;
    padding: 3px 12px;
    border-radius: 6px;
    font-weight: 500;
    background: rgba(0, 242, 192, 0.1);
    color: #00F2C0;
}

.hero-author {
    font-size: 11px;
    padding: 2px 10px;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.04);
    color: rgba(255, 255, 255, 0.4);
    font-family: 'JetBrains Mono', monospace;
}

.hero-id {
    font-size: 10px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.2);
    font-family: 'JetBrains Mono', monospace;
    background: rgba(255, 255, 255, 0.03);
    padding: 2px 8px;
    border-radius: 4px;
}

.hero-title {
    font-size: 28px;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1.3;
    letter-spacing: -0.3px;
    margin-bottom: 10px;
}

.hero-summary {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.4);
    line-height: 1.7;
    margin-bottom: 16px;
}

.hero-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.2);
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 4px;
}

.meta-item i {
    font-size: 12px;
}

.meta-dot {
    width: 2px;
    height: 2px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
}

/* ===== 书籍简介 ===== */
.book-content {
    margin-bottom: 40px;
}

.content-head {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 600;
    color: #EFF3F8;
    margin-bottom: 16px;
}

.content-head i {
    font-size: 14px;
    color: #00F2C0;
}

.content-body {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.65);
    line-height: 1.8;
}

.content-body :deep(h2) {
    font-size: 18px;
    font-weight: 600;
    color: #EFF3F8;
    margin: 24px 0 12px;
}

.content-body :deep(h3) {
    font-size: 15px;
    font-weight: 600;
    color: #EFF3F8;
    margin: 20px 0 10px;
}

.content-body :deep(strong) {
    color: rgba(255, 255, 255, 0.8);
}

.content-body :deep(blockquote) {
    border-left: 3px solid rgba(0, 242, 192, 0.3);
    padding: 8px 16px;
    margin: 12px 0;
    color: rgba(255, 255, 255, 0.5);
    font-style: italic;
    background: rgba(255, 255, 255, 0.02);
    border-radius: 0 8px 8px 0;
}

.content-body :deep(li) {
    padding: 2px 0;
    margin-left: 20px;
}

/* ===== 读书笔记 ===== */
.notes-section {
    margin-top: 8px;
}

.notes-head {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 600;
    color: #EFF3F8;
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.notes-head i {
    font-size: 14px;
    color: #00F2C0;
}

.notes-count {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.2);
    font-family: 'JetBrains Mono', monospace;
    font-weight: 400;
}

/* ===== 笔记列表 ===== */
.notes-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.note-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 20px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    cursor: pointer;
    transition: all 0.3s ease;
}

.note-item:hover {
    background: rgba(0, 242, 192, 0.04);
    border-color: rgba(0, 242, 192, 0.12);
    transform: translateX(4px);
}

.note-num {
    flex-shrink: 0;
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: rgba(0, 242, 192, 0.08);
    color: #00F2C0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
}

.note-info {
    flex: 1;
    min-width: 0;
}

.note-title {
    font-size: 14px;
    font-weight: 600;
    color: #EFF3F8;
    line-height: 1.4;
    margin-bottom: 4px;
}

.note-summary {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.3);
    line-height: 1.5;
    margin-bottom: 6px;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.note-meta {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 10px;
    color: rgba(255, 255, 255, 0.15);
}

.note-meta .meta-item {
    display: flex;
    align-items: center;
    gap: 3px;
}

.note-meta .meta-item i {
    font-size: 10px;
}

.note-meta .meta-dot {
    width: 2px;
    height: 2px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
}

.note-arrow {
    flex-shrink: 0;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255, 255, 255, 0.1);
    font-size: 12px;
    transition: all 0.3s ease;
}

.note-item:hover .note-arrow {
    color: #00F2C0;
    transform: translateX(4px);
}

.loading-text,
.empty-text {
    text-align: center;
    padding: 60px;
    color: rgba(255, 255, 255, 0.15);
    font-size: 14px;
}

/* ===== 响应式 ===== */
@media (max-width: 640px) {
    .book-hero {
        flex-direction: column;
        gap: 20px;
    }

    .hero-cover {
        width: 140px;
    }

    .hero-title {
        font-size: 22px;
    }

    .book-detail-page {
        padding: 0 12px 40px;
    }
}
</style>
