<template>
    <div class="moments-layout">
        <!-- 左侧：动态列表 -->
        <div class="moments-main">
            <div class="page-head">
                <h1 class="head-title">动态</h1>
                <p class="head-desc">生活碎片 · 日常记录</p>
            </div>

            <!-- 分类筛选 -->
            <div class="filter-bar">
                <button class="filter-btn" :class="{ active: activeCategory === '' }"
                    @click="activeCategory = ''; loadMoments()">
                    <i class="fas fa-layer-group"></i> 全部
                </button>
                <button class="filter-btn" :class="{ active: activeCategory === 'moment' }"
                    @click="activeCategory = 'moment'; loadMoments()">
                    <i class="fas fa-camera"></i> 朋友圈
                </button>
                <button class="filter-btn" :class="{ active: activeCategory === 'sports' }"
                    @click="activeCategory = 'sports'; loadMoments()">
                    <i class="fas fa-running"></i> 运动
                </button>
                <button class="filter-btn" :class="{ active: activeCategory === 'daily' }"
                    @click="activeCategory = 'daily'; loadMoments()">
                    <i class="fas fa-sun"></i> 日常
                </button>
                <button class="filter-btn" :class="{ active: activeCategory === 'study' }"
                    @click="activeCategory = 'study'; loadMoments()">
                    <i class="fas fa-graduation-cap"></i> 学习
                </button>
            </div>

            <!-- 骨架屏 -->
            <div class="skeleton-list" v-if="loading">
                <div class="skeleton-item" v-for="n in 5" :key="n">
                    <Skeleton type="circle" width="44px" height="44px" borderRadius="12px" />
                    <div class="skeleton-item-body">
                        <Skeleton type="text" width="120px" height="12px" />
                        <Skeleton type="text" width="100%" height="14px" />
                    </div>
                </div>
            </div>

            <!-- 动态列表 -->
            <div class="feed-list" v-else-if="items.length">
                <div class="feed-card" v-for="(item, i) in items" :key="item.id" :id="'feed-' + item.id">
                    <!-- 左侧：分类图标 -->
                    <div class="card-left">
                        <div class="card-icon" :class="item.category">
                            <i :class="categoryIcon(item.category)"></i>
                        </div>
                    </div>

                    <!-- 右侧内容 -->
                    <div class="card-body">
                        <div class="card-top">
                            <span class="card-category" :class="item.category">{{ categoryLabel(item.category) }}</span>
                            <span class="card-date">{{ formatDate(item.created_at) }}</span>
                        </div>

                        <div class="card-content">{{ item.content }}</div>

                        <!-- 图片 -->
                        <div class="card-images" v-if="item.imagesList && item.imagesList.length">
                            <div class="card-img-item" v-for="(img, j) in item.imagesList" :key="j"
                                @click="previewIndex = getGlobalImageIndex(i, j)">
                                <img :src="resolveThumbUrl(img)" alt=""
                                    @error="$event.target.src = resolveImageUrl(img)" />
                            </div>
                        </div>

                        <!-- 朋友圈：底部操作 -->
                        <div class="card-footer" v-if="item.category === 'moment'">
                            <div class="card-actions">
                                <span class="action-btn" :class="{ liked: item.liked }" @click="toggleLike(i)">
                                    <i class="far fa-heart"></i>
                                    <span v-if="item.like_count">{{ item.like_count }}</span>
                                </span>
                                <span class="action-btn" @click="toggleComment(i)">
                                    <i class="far fa-comment"></i>
                                    <span v-if="item.comment_count">{{ item.comment_count }}</span>
                                </span>
                            </div>
                        </div>

                        <!-- 朋友圈：评论框 -->
                        <div class="card-comment-box" v-if="item.showComment">
                            <input type="text" v-model="item.commentText" placeholder="说点什么..."
                                @keyup.enter="submitComment(i)" />
                            <button @click="submitComment(i)">发送</button>
                        </div>

                        <!-- 朋友圈：评论列表 -->
                        <div class="card-comments" v-if="item.commentList && item.commentList.length">
                            <div class="comment-item" v-for="(c, k) in item.commentList" :key="k">
                                <span class="comment-name">{{ c.name }}</span>
                                <span class="comment-text">：{{ c.text }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="empty-text" v-else>暂无动态</div>
        </div>

        <!-- 右侧：热力图 -->
        <div class="moments-sidebar">
            <HeatmapWidget />
        </div>

        <!-- 图片预览 -->
        <div class="preview-overlay" v-if="previewIndex !== null" @click="previewIndex = null">
            <img :src="allImages[previewIndex]" alt="" @click.stop />
            <span class="preview-close" @click="previewIndex = null">&times;</span>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { publicApi, likeApi, resolveImageUrl, resolveThumbUrl } from '@/utils/api'
import HeatmapWidget from '@/components/HeatmapWidget.vue'
import Skeleton from '@/components/Skeleton.vue'

const previewIndex = ref(null)
const loading = ref(true)
const items = ref([])
const activeCategory = ref('')
const highlightId = ref(null)

function formatDate(dateStr) {
    if (!dateStr) return ''
    const d = new Date(dateStr)
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return `${y}.${m}.${day}`
}

function categoryLabel(cat) {
    const map = { moment: '朋友圈', sports: '运动', daily: '日常', study: '学习' }
    return map[cat] || cat
}

function categoryIcon(cat) {
    const map = { moment: 'fas fa-camera', sports: 'fas fa-running', daily: 'fas fa-sun', study: 'fas fa-graduation-cap' }
    return map[cat] || 'fas fa-check-circle'
}

// ===== 图片预览 =====
const allImages = computed(() => {
    return items.value.flatMap(m => m.imagesList || [])
})

function getGlobalImageIndex(itemIdx, imgIdx) {
    let count = 0
    for (let i = 0; i < itemIdx; i++) {
        count += (items.value[i].imagesList || []).length
    }
    return count + imgIdx
}

// ===== 朋友圈操作 =====
async function toggleLike(i) {
    const m = items.value[i]
    if (m.category !== 'moment') return
    try {
        const res = await likeApi.toggleLike(m.id)
        m.liked = res.liked
        m.like_count = res.like_count
    } catch (e) {
        console.error('点赞失败:', e)
    }
}

function toggleComment(i) {
    const m = items.value[i]
    if (m.category !== 'moment') return
    m.showComment = !m.showComment
}

function submitComment(i) {
    const m = items.value[i]
    if (m.category !== 'moment' || !m.commentText.trim()) return
    m.commentList.push({ name: '克莱·C', text: m.commentText.trim() })
    m.comment_count = m.commentList.length
    m.commentText = ''
    m.showComment = false
}

// ===== 高亮滚动 =====
function scrollToHighlight() {
    if (!highlightId.value) return
    nextTick(() => {
        const el = document.getElementById('feed-' + highlightId.value)
        if (el) {
            setTimeout(() => {
                el.scrollIntoView({ behavior: 'smooth', block: 'center' })
                el.classList.add('feed-highlight')
                setTimeout(() => el.classList.remove('feed-highlight'), 3000)
            }, 200)
        }
    })
}

// ===== 加载数据 =====
async function loadMoments() {
    loading.value = true
    try {
        const params = { page: 1, page_size: 100 }
        if (activeCategory.value) {
            params.category = activeCategory.value
        }
        const res = await publicApi.getMoments(params)
        const rawItems = res.items || []
        items.value = rawItems.map(item => ({
            ...item,
            imagesList: item.images ? item.images.split(',').filter(Boolean).map(s => resolveImageUrl(s.trim())) : [],
            liked: false,
            showComment: false,
            commentText: '',
            commentList: [],
        }))
    } catch (e) {
        console.error('加载动态失败:', e)
        items.value = []
    } finally {
        loading.value = false
        scrollToHighlight()
    }
}

onMounted(() => {
    const params = new URLSearchParams(window.location.search)
    const id = params.get('id')
    if (id) {
        highlightId.value = id
    }
    loadMoments()
})
</script>

<style scoped>
.moments-layout {
    display: flex;
    gap: 32px;
    align-items: flex-start;
}

.moments-main {
    flex: 1;
    min-width: 0;
    width: 100%;
}

/* ===== 头部 ===== */
.page-head {
    padding: 48px 0 28px;
    margin-bottom: 28px;
    position: relative;
}

.head-title {
    font-size: 42px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -1px;
    line-height: 1.15;
    margin: 0;
    background: linear-gradient(135deg, #FFFFFF 60%, rgba(255, 255, 255, 0.5));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.head-desc {
    font-size: 15px;
    color: rgba(255, 255, 255, 0.35);
    margin-top: 10px;
    font-weight: 400;
    letter-spacing: 0.3px;
}

/* ===== 筛选栏 ===== */
.filter-bar {
    display: flex;
    gap: 4px;
    margin-bottom: 24px;
    padding: 4px;
    background: rgba(255, 255, 255, 0.02);
    border-radius: 10px;
    flex-wrap: wrap;
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
    font-family: inherit;
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

/* ===== 动态列表 ===== */
.feed-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.feed-card {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 14px 18px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 14px;
    border: 1px solid transparent;
    transition: all 0.2s ease;
}

.feed-card:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.06);
}

/* ===== 高亮动画 ===== */
.feed-card.feed-highlight {
    background: rgba(0, 242, 192, 0.08);
    border-color: rgba(0, 242, 192, 0.25);
    box-shadow: 0 0 30px rgba(0, 242, 192, 0.08);
    animation: highlight-pulse 3s ease-out;
}

@keyframes highlight-pulse {
    0% {
        background: rgba(0, 242, 192, 0.15);
        border-color: rgba(0, 242, 192, 0.4);
    }

    50% {
        background: rgba(0, 242, 192, 0.08);
        border-color: rgba(0, 242, 192, 0.25);
    }

    100% {
        background: rgba(0, 242, 192, 0.08);
        border-color: rgba(0, 242, 192, 0.25);
    }
}

/* ===== 左侧 ===== */
.card-left {
    flex-shrink: 0;
}

.card-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
}

.card-icon.moment {
    background: rgba(0, 242, 192, 0.12);
    color: #00F2C0;
}

.card-icon.sports {
    background: rgba(255, 107, 107, 0.12);
    color: #ff6b6b;
}

.card-icon.study {
    background: rgba(162, 155, 254, 0.12);
    color: #a29bfe;
}

.card-icon.daily {
    background: rgba(253, 203, 110, 0.12);
    color: #fdcb6e;
}

/* ===== 中间内容 ===== */
.card-body {
    flex: 1;
    min-width: 0;
}

.card-top {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 6px;
}

.card-category {
    font-size: 11px;
    padding: 2px 10px;
    border-radius: 10px;
    font-weight: 500;
}

.card-category.moment {
    color: #00F2C0;
    background: rgba(0, 242, 192, 0.1);
}

.card-category.sports {
    color: #ff6b6b;
    background: rgba(255, 107, 107, 0.1);
}

.card-category.study {
    color: #a29bfe;
    background: rgba(162, 155, 254, 0.1);
}

.card-category.daily {
    color: #fdcb6e;
    background: rgba(253, 203, 110, 0.1);
}

.card-date {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.2);
    font-family: 'JetBrains Mono', 'Noto Sans Mono', monospace;
}

.card-content {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.6);
    line-height: 1.7;
    white-space: pre-wrap;
}

/* ===== 图片 ===== */
.card-images {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 4px;
    margin-top: 10px;
    max-width: 360px;
}

.card-images:has(.card-img-item:only-child) {
    grid-template-columns: 1fr;
    max-width: 200px;
}

.card-images:has(.card-img-item:first-child:nth-last-child(2)),
.card-images:has(.card-img-item:first-child:nth-last-child(2) ~ .card-img-item) {
    grid-template-columns: 1fr 1fr;
    max-width: 260px;
}

.card-images:has(.card-img-item:first-child:nth-last-child(3),
    .card-img-item:first-child:nth-last-child(3) ~ .card-img-item) {
    grid-template-columns: repeat(3, 1fr);
    max-width: 320px;
}

.card-img-item {
    aspect-ratio: 1;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.03);
    cursor: pointer;
    border-radius: 6px;
}

.card-images:has(.card-img-item:only-child) .card-img-item {
    aspect-ratio: 16 / 9;
    border-radius: 8px;
}

.card-img-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.35s ease;
}

.card-img-item:hover img {
    transform: scale(1.08);
}

/* ===== 底部操作 ===== */
.card-footer {
    display: flex;
    justify-content: flex-end;
    margin-top: 8px;
}

.card-actions {
    display: flex;
    gap: 16px;
}

.action-btn {
    display: flex;
    align-items: center;
    gap: 4px;
    color: rgba(255, 255, 255, 0.25);
    cursor: pointer;
    transition: all 0.2s ease;
    user-select: none;
    font-size: 12px;
}

.action-btn:hover {
    color: rgba(255, 255, 255, 0.5);
}

.action-btn.liked {
    color: #ff6b6b;
}

.action-btn.liked i {
    font-weight: 900;
}

/* ===== 评论框 ===== */
.card-comment-box {
    display: flex;
    gap: 8px;
    margin-top: 10px;
}

.card-comment-box input {
    flex: 1;
    padding: 8px 12px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.05);
    color: #EFF3F8;
    font-size: 13px;
    outline: none;
    transition: border-color 0.2s;
}

.card-comment-box input:focus {
    border-color: rgba(0, 242, 192, 0.3);
}

.card-comment-box input::placeholder {
    color: rgba(255, 255, 255, 0.2);
}

.card-comment-box button {
    padding: 8px 16px;
    border-radius: 8px;
    border: none;
    background: rgba(0, 242, 192, 0.15);
    color: #00F2C0;
    font-size: 13px;
    cursor: pointer;
    transition: background 0.2s;
}

.card-comment-box button:hover {
    background: rgba(0, 242, 192, 0.25);
}

/* ===== 评论列表 ===== */
.card-comments {
    margin-top: 10px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 8px;
    padding: 8px 12px;
}

.comment-item {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
    line-height: 1.8;
}

.comment-name {
    color: #00F2C0;
    font-weight: 500;
}

.comment-text {
    color: rgba(255, 255, 255, 0.6);
}

/* ===== 右侧：热力图 ===== */
.moments-sidebar {
    width: 200px;
    flex-shrink: 0;
    position: sticky;
    top: 24px;
}

/* ===== 图片预览 ===== */
.preview-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.85);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    cursor: pointer;
}

.preview-overlay img {
    max-width: 90vw;
    max-height: 90vh;
    object-fit: contain;
    border-radius: 8px;
    cursor: default;
}

.preview-close {
    position: absolute;
    top: 20px;
    right: 24px;
    font-size: 36px;
    color: #FFFFFF;
    cursor: pointer;
    opacity: 0.6;
    transition: opacity 0.2s;
    line-height: 1;
}

.preview-close:hover {
    opacity: 1;
}

/* ===== 骨架屏 ===== */
.skeleton-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.skeleton-item {
    display: flex;
    gap: 16px;
    padding: 14px 18px;
    align-items: flex-start;
}

.skeleton-item-body {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.empty-text {
    text-align: center;
    padding: 60px;
    color: rgba(255, 255, 255, 0.15);
    font-size: 14px;
}

/* ===== 响应式 ===== */
@media (max-width: 900px) {
    .moments-layout {
        flex-direction: column;
    }

    .moments-sidebar {
        width: 100%;
        position: static;
    }
}

@media (max-width: 600px) {
    .head-title {
        font-size: 26px;
    }

    .filter-bar {
        gap: 2px;
        padding: 3px;
    }

    .filter-btn {
        padding: 5px 10px;
        font-size: 12px;
    }

    .card-images {
        grid-template-columns: repeat(3, 1fr);
        max-width: 280px;
    }
}
</style>
