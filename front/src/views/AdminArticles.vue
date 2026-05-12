<template>
    <div class="admin-articles">
        <div class="page-header">
            <div class="header-left">
                <h2>文章管理</h2>
                <span class="header-count">{{ filteredArticles.length }} 篇</span>
            </div>
            <button class="create-btn" @click="createArticle">
                <i class="fas fa-plus"></i> 新建文章
            </button>
        </div>

        <!-- 筛选栏 -->
        <div class="filter-bar">
            <button class="filter-btn" :class="{ active: activeFilter === '' }" @click="setFilter('')">
                <i class="fas fa-layer-group"></i> 全部
            </button>
            <button class="filter-btn" v-for="cat in categories" :key="cat" :class="{ active: activeFilter === cat }"
                @click="setFilter(cat)">
                <span class="dot" :style="{ background: catColors[cat]?.text || '#00F2C0' }"></span>
                {{ cat }}
            </button>
        </div>

        <div class="loading-text" v-if="loading">加载中...</div>

        <div class="card-grid" v-else>
            <div class="article-card" v-for="article in filteredArticles" :key="article.id"
                @click="goArticle(article.id)">
                <div class="card-glow"></div>
                <div class="card-top">
                    <span class="card-id">#{{ article.id }}</span>
                    <span class="card-cat" v-if="article.category" :style="catStyle(article.category)">{{
                        article.category }}</span>
                </div>
                <div class="card-title">{{ article.title }}</div>
                <div class="card-footer">
                    <div class="card-meta">
                        <span class="meta-item" title="阅读量">
                            <i class="far fa-eye"></i>
                            <span class="meta-num">{{ article.view_count }}</span>
                        </span>
                        <span class="meta-divider"></span>
                        <span class="meta-item" title="点赞数">
                            <i class="far fa-heart"></i>
                            <span class="meta-num">{{ article.like_count }}</span>
                        </span>
                        <span class="meta-divider"></span>
                        <span class="meta-item">
                            <i class="far fa-calendar"></i>
                            {{ formatDate(article.created_at) }}
                        </span>
                    </div>
                    <div class="card-actions">
                        <button class="action-btn edit" @click="editArticle($event, article.id)" title="编辑">
                            <i class="fas fa-pen"></i>
                        </button>
                        <button class="action-btn danger" @click="deleteArticle($event, article.id)" title="删除">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>

            <div class="empty-text" v-if="!filteredArticles.length">暂无文章</div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { adminApi } from '@/utils/api'
import { useToast } from '@/utils/toast'

const router = useRouter()
const { toast } = useToast()
const loading = ref(true)
const articles = ref([])
const activeFilter = ref('')

const catColors = {
    '技术': { bg: 'rgba(0, 242, 192, 0.12)', text: '#00F2C0' },
    '生活': { bg: 'rgba(255, 217, 61, 0.12)', text: '#FFD93D' },
    '随笔': { bg: 'rgba(108, 92, 231, 0.12)', text: '#6C5CE7' },
    '教程': { bg: 'rgba(0, 210, 255, 0.12)', text: '#00D2FF' },
    '分享': { bg: 'rgba(255, 107, 107, 0.12)', text: '#FF6B6B' },
}

function catStyle(cat) {
    const c = catColors[cat]
    return c ? { background: c.bg, color: c.text } : {}
}

const categories = computed(() => {
    const cats = new Set()
    articles.value.forEach(a => { if (a.category) cats.add(a.category) })
    return [...cats]
})

const filteredArticles = computed(() => {
    if (!activeFilter.value) return articles.value
    return articles.value.filter(a => a.category === activeFilter.value)
})

function setFilter(cat) {
    activeFilter.value = cat
}

function createArticle() {
    router.push('/admin/editor')
}

function formatDate(dateStr) {
    if (!dateStr) return ''
    const d = new Date(dateStr)
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return `${y}.${m}.${day}`
}

function goArticle(id) {
    window.open(`/post/${id}`, '_blank')
}

function editArticle(e, id) {
    e.stopPropagation()
    router.push(`/admin/editor?id=${id}`)
}

async function deleteArticle(e, id) {
    e.stopPropagation()
    try {
        await adminApi.deletePost(id)
        articles.value = articles.value.filter(a => a.id !== id)
        toast('文章已删除', 'success')
    } catch (e) {
        toast('删除失败: ' + e.message, 'error')
    }
}

onMounted(async () => {
    try {
        const res = await adminApi.getPosts({ page: 1, page_size: 50 })
        articles.value = res.items || []
    } catch (e) {
        console.error('加载文章列表失败:', e)
    } finally {
        loading.value = false
    }
})
</script>

<style scoped>
.admin-articles {
    max-width: 960px;
    margin: 0 auto;
}

/* ===== 页头 ===== */
.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
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
    font-size: 12px;
    color: rgba(255, 255, 255, 0.15);
    font-family: 'JetBrains Mono', monospace;
}

.create-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 7px 16px;
    border-radius: 8px;
    border: none;
    background: rgba(0, 242, 192, 0.1);
    color: #00F2C0;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
}

.create-btn i {
    font-size: 11px;
}

.create-btn:hover {
    background: rgba(0, 242, 192, 0.18);
}

/* ===== 筛选栏 ===== */
.filter-bar {
    display: flex;
    gap: 4px;
    margin-bottom: 24px;
    padding: 4px;
    background: rgba(255, 255, 255, 0.02);
    border-radius: 10px;
}

.filter-btn {
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 6px 14px;
    border-radius: 7px;
    border: none;
    background: transparent;
    color: rgba(255, 255, 255, 0.2);
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.filter-btn i {
    font-size: 11px;
}

.filter-btn:hover {
    color: rgba(255, 255, 255, 0.5);
    background: rgba(255, 255, 255, 0.03);
}

.filter-btn.active {
    color: #FFFFFF;
    background: rgba(255, 255, 255, 0.06);
}

.dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
}

/* ===== 卡片网格 ===== */
.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 12px;
}

.article-card {
    position: relative;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 14px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.article-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.06), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.article-card:hover {
    background: rgba(255, 255, 255, 0.04);
    border-color: rgba(255, 255, 255, 0.1);
    transform: translateY(-3px);
}

.article-card:hover::before {
    opacity: 1;
}

/* ===== 发光效果 ===== */
.card-glow {
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 50% 0%, rgba(0, 242, 192, 0.03), transparent 60%);
    opacity: 0;
    transition: opacity 0.4s ease;
    pointer-events: none;
}

.article-card:hover .card-glow {
    opacity: 1;
}

/* ===== 卡片顶部 ===== */
.card-top {
    position: relative;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 10px;
}

.card-id {
    font-size: 10px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.2);
    font-family: 'JetBrains Mono', monospace;
    background: rgba(255, 255, 255, 0.03);
    padding: 2px 8px;
    border-radius: 4px;
}

.card-cat {
    font-size: 10px;
    padding: 2px 10px;
    border-radius: 6px;
    font-weight: 500;
}

/* ===== 标题 ===== */
.card-title {
    position: relative;
    flex: 1;
    font-size: 16px;
    font-weight: 600;
    color: #EFF3F8;
    line-height: 1.5;
    margin-bottom: 14px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* ===== 底部 ===== */
.card-footer {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 10px;
    border-top: 1px solid rgba(255, 255, 255, 0.04);
}

.card-meta {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 10px;
    color: rgba(255, 255, 255, 0.2);
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 3px;
}

.meta-item i {
    font-size: 10px;
}

.meta-num {
    font-family: 'JetBrains Mono', monospace;
}

.meta-divider {
    width: 2px;
    height: 2px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
}

.card-actions {
    display: flex;
    gap: 2px;
}

.action-btn {
    width: 26px;
    height: 26px;
    border-radius: 6px;
    border: none;
    background: transparent;
    color: rgba(255, 255, 255, 0.1);
    font-size: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
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

/* ===== 状态 ===== */
.loading-text,
.empty-text {
    text-align: center;
    padding: 60px;
    color: rgba(255, 255, 255, 0.15);
    font-size: 14px;
}
</style>
