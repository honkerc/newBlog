<template>
    <div class="daily-layout">
        <!-- 左侧：时间线 -->
        <div class="daily-main">
            <div class="page-head">
                <h1 class="head-title">日精进</h1>
                <p class="head-desc">每天进步一点点，记录成长路上的每一个脚印</p>
            </div>

            <!-- 骨架屏 -->
            <div class="skeleton-list" v-if="loading">
                <div class="skeleton-item" v-for="n in 5" :key="n">
                    <Skeleton type="circle" width="12px" height="12px" borderRadius="50%" />
                    <div class="skeleton-item-body">
                        <Skeleton type="text" width="120px" height="12px" />
                        <Skeleton type="card" height="120px" borderRadius="14px" />
                    </div>
                </div>
            </div>

            <!-- 时间线 -->
            <div class="timeline" v-else-if="articles.length">

                <div class="timeline-item" v-for="article in articles" :key="article.id" @click="goToPost(article.id)">
                    <div class="timeline-dot"></div>
                    <div class="timeline-date">{{ formatDate(article.created_at) }}</div>
                    <div class="timeline-card">
                        <div class="card-header">
                            <h3 class="card-title">{{ article.title }}</h3>
                            <span class="card-tag" v-if="article.tag">{{ article.tag }}</span>
                        </div>
                        <p class="card-summary">{{ article.summary }}</p>
                        <div class="card-cover" v-if="article.cover_url">
                            <img :src="resolveThumbUrl(article.cover_url)" alt="" />
                        </div>
                        <div class="card-footer">
                            <span class="card-category">{{ article.category }}</span>
                            <span class="card-stats">
                                <i class="fas fa-eye"></i> {{ article.view_count }}
                                <i class="fas fa-heart"></i> {{ article.like_count }}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="empty-text" v-else>暂无日精进记录</div>
        </div>

        <!-- 右侧：热力图 -->
        <div class="daily-sidebar">
            <HeatmapWidget />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { publicApi, resolveImageUrl, resolveThumbUrl } from '@/utils/api'
import HeatmapWidget from '@/components/HeatmapWidget.vue'
import Skeleton from '@/components/Skeleton.vue'

const router = useRouter()
const loading = ref(true)
const articles = ref([])

function formatDate(dateStr) {
    if (!dateStr) return ''
    const d = new Date(dateStr)
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return `${y}.${m}.${day}`
}

function goToPost(id) {
    router.push(`/post/${id}`)
}

onMounted(async () => {
    try {
        const res = await publicApi.getPosts({ page: 1, page_size: 50, tag: '日精进' })
        articles.value = res.items || []
    } catch (e) {
        console.error('加载日精进失败:', e)
    } finally {
        loading.value = false
    }
})
</script>

<style scoped>
.daily-layout {
    display: flex;
    gap: 32px;
    align-items: flex-start;
    padding: 0 16px 60px;
}

.daily-main {
    flex: 1;
    min-width: 0;
}

/* ===== 头部 ===== */
.page-head {
    padding: 48px 0 28px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    margin-bottom: 32px;
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

/* ===== 时间线 ===== */
.timeline {
    position: relative;
    padding-left: 32px;
}

.timeline::before {
    content: '';
    position: absolute;
    left: 10px;
    top: 0;
    bottom: 0;
    width: 2px;
    background: linear-gradient(180deg, rgba(0, 242, 192, 0.3), rgba(0, 242, 192, 0.05));
    border-radius: 1px;
}

.timeline-item {
    position: relative;
    margin-bottom: 28px;
    cursor: pointer;
}

.timeline-dot {
    position: absolute;
    left: -26px;
    top: 24px;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #00F2C0;
    border: 3px solid rgba(0, 242, 192, 0.2);
    box-shadow: 0 0 12px rgba(0, 242, 192, 0.2);
    transition: all 0.3s ease;
}

.timeline-item:hover .timeline-dot {
    transform: scale(1.3);
    box-shadow: 0 0 20px rgba(0, 242, 192, 0.4);
}

.timeline-date {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.25);
    font-family: 'JetBrains Mono', 'Noto Sans Mono', monospace;
    margin-bottom: 8px;
    padding-top: 4px;
}

.timeline-card {
    position: relative;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 14px;
    padding: 20px;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.timeline-card::before {
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

.timeline-card::after {
    content: '';
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

.timeline-card:hover {
    background: rgba(255, 255, 255, 0.04);
    border-color: rgba(255, 255, 255, 0.1);
    transform: translateX(4px);
}

.timeline-card:hover::before {
    opacity: 1;
}

.timeline-card:hover::after {
    opacity: 1;
}

.card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
}

.card-title {
    font-size: 18px;
    font-weight: 600;
    color: #EFF3F8;
    line-height: 1.4;
    flex: 1;
}

.card-tag {
    font-size: 11px;
    color: #00F2C0;
    background: rgba(0, 242, 192, 0.1);
    padding: 2px 10px;
    border-radius: 10px;
    font-weight: 500;
    flex-shrink: 0;
}

.card-summary {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.45);
    line-height: 1.7;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.card-cover {
    margin-top: 14px;
    border-radius: 12px;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.03);
}

.card-cover img {
    width: 100%;
    max-height: 240px;
    object-fit: cover;
    display: block;
    transition: transform 0.5s ease;
}

.timeline-card:hover .card-cover img {
    transform: scale(1.03);
}

.card-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.card-category {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.3);
}

.card-stats {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.25);
    display: flex;
    gap: 12px;
}

.card-stats i {
    margin-right: 3px;
    font-size: 11px;
}

.loading-text,
.empty-text {
    text-align: center;
    padding: 60px;
    color: rgba(255, 255, 255, 0.15);
    font-size: 14px;
}

/* ===== 骨架屏 ===== */
.skeleton-list {
    padding-left: 32px;
}

.skeleton-item {
    display: flex;
    gap: 14px;
    margin-bottom: 28px;
    align-items: flex-start;
}

.skeleton-item-body {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

/* ===== 右侧：热力图 ===== */
.daily-sidebar {
    width: 200px;
    flex-shrink: 0;
    position: sticky;
    top: 24px;
}

/* ===== 响应式 ===== */
@media (max-width: 900px) {
    .daily-layout {
        flex-direction: column;
    }

    .daily-sidebar {
        width: 100%;
        position: static;
    }
}

@media (max-width: 600px) {
    .timeline {
        padding-left: 24px;
    }

    .timeline-dot {
        left: -20px;
        width: 10px;
        height: 10px;
    }

    .card-title {
        font-size: 16px;
    }

    .head-title {
        font-size: 26px;
    }

    .daily-layout {
        padding: 0 12px 40px;
    }
}
</style>
