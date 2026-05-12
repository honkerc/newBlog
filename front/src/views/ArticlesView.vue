<template>
    <div class="articles-page">
        <div class="articles-inner">
            <!-- 左侧：文章列表 -->
            <div class="articles-main">
                <div class="page-head">
                    <h1 class="head-title">文章</h1>
                    <p class="head-desc">记录思考，沉淀知识</p>
                </div>

                <!-- 话题标签 -->
                <div class="topics-bar">
                    <span class="topic-tag" :class="{ active: activeCategory === '' }" @click="filterByCategory('')">#
                        全部</span>
                    <span class="topic-tag" v-for="cat in categories" :key="cat"
                        :class="{ active: activeCategory === cat }" @click="filterByCategory(cat)"># {{ cat }}</span>
                </div>

                <!-- 骨架屏 -->
                <div class="skeleton-masonry" v-if="loading">
                    <div class="skeleton-col" v-for="col in 3" :key="col">
                        <div class="skeleton-card" v-for="n in col === 1 ? 3 : 2" :key="n">
                            <Skeleton type="image" />
                            <div class="skeleton-card-body">
                                <Skeleton type="title" />
                                <Skeleton type="text" width="90%" />
                                <Skeleton type="text" width="60%" />
                                <div class="skeleton-card-footer">
                                    <Skeleton type="text" width="80px" height="10px" />
                                    <Skeleton type="text" width="60px" height="10px" />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 瀑布流 -->
                <div class="masonry" v-else>

                    <div class="masonry-col" v-for="col in 3" :key="col">
                        <div class="masonry-item" v-for="(article, i) in articlesInCol(col)" :key="i"
                            @click="goToPost(article.id)">
                            <div class="item-cover" v-if="article.cover_url">
                                <img :src="resolveThumbUrl(article.cover_url)" alt="" />
                                <div class="cover-tag">{{ article.tag || article.category }}</div>
                            </div>
                            <div class="item-body">
                                <h3 class="item-title">{{ article.title }}</h3>
                                <p class="item-excerpt">{{ article.summary }}</p>
                                <div class="item-footer">
                                    <span class="item-date">{{ formatDate(article.created_at) }}</span>
                                    <span class="item-read">{{ article.view_count }} 次阅读</span>
                                    <span class="item-likes"><i class="far fa-heart"></i> {{ article.like_count
                                        }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="empty-text" v-if="!articles.length">暂无文章</div>
                </div>
            </div>

            <!-- 右侧：热力图 -->
            <div class="articles-sidebar">
                <HeatmapWidget />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { publicApi, resolveImageUrl, resolveThumbUrl } from '@/utils/api'
import HeatmapWidget from '@/components/HeatmapWidget.vue'
import Skeleton from '@/components/Skeleton.vue'

const router = useRouter()
const loading = ref(true)
const articles = ref([])
const categories = ref([])
const activeCategory = ref('')

function formatDate(dateStr) {
    if (!dateStr) return ''
    const d = new Date(dateStr)
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return `${y}.${m}.${day}`
}

function articlesInCol(col) {
    return articles.value.filter((_, i) => i % 3 === col - 1)
}

function goToPost(id) {
    router.push(`/post/${id}`)
}

function filterByCategory(cat) {
    activeCategory.value = cat
    loadArticles()
}

async function loadArticles() {
    loading.value = true
    try {
        const params = { page: 1, page_size: 50 }
        if (activeCategory.value) {
            params.category = activeCategory.value
        }
        const res = await publicApi.getPosts(params)
        articles.value = res.items || []
    } catch (e) {
        console.error('加载文章列表失败:', e)
        articles.value = []
    } finally {
        loading.value = false
    }
}

onMounted(async () => {
    try {
        const catRes = await publicApi.getCategories()
        categories.value = (catRes.items || []).map(c => c.name)
    } catch (e) {
        console.error('加载分类失败:', e)
    }
    await loadArticles()
})
</script>

<style scoped>
.articles-page {
    padding: 0 16px 60px;
}

.articles-inner {
    display: flex;
    gap: 32px;
    align-items: flex-start;
}

.articles-main {
    flex: 1;
    min-width: 0;
}

/* ===== 头部 ===== */
.page-head {
    padding: 48px 0 28px;
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

/* ===== 话题标签 ===== */
.topics-bar {
    display: flex;
    gap: 8px;
    padding: 20px 0 24px;
    flex-wrap: wrap;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    margin-bottom: 28px;
}

.topic-tag {
    padding: 5px 14px;
    border-radius: 16px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.4);
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.06);
    cursor: pointer;
    transition: all 0.2s ease;
}

.topic-tag:hover {
    color: rgba(255, 255, 255, 0.7);
    background: rgba(255, 255, 255, 0.08);
}

.topic-tag.active {
    color: #00F2C0;
    background: rgba(0, 242, 192, 0.1);
    border-color: rgba(0, 242, 192, 0.2);
}

/* ===== 瀑布流 ===== */
.masonry {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    align-items: start;
}

.masonry-col {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.masonry-item {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 18px;
    overflow: hidden;
    transition: all 0.3s ease;
    cursor: pointer;
}

.masonry-item:hover {
    background: rgba(0, 242, 192, 0.08);
    border-color: rgba(0, 242, 192, 0.2);
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
}

/* ===== 封面 ===== */
.item-cover {
    position: relative;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.03);
}

.item-cover img {
    width: 100%;
    display: block;
    aspect-ratio: 16 / 10;
    object-fit: cover;
    transition: transform 0.5s ease;
}

.masonry-item:hover .item-cover img {
    transform: scale(1.05);
}

.cover-tag {
    position: absolute;
    top: 10px;
    left: 10px;
    padding: 2px 10px;
    border-radius: 10px;
    font-size: 10px;
    color: #FFFFFF;
    background: rgba(0, 0, 0, 0.35);
    backdrop-filter: blur(4px);
    font-weight: 500;
}

/* ===== 内容 ===== */
.item-body {
    padding: 14px 16px 16px;
}

.item-title {
    font-size: 15px;
    font-weight: 600;
    color: #EFF3F8;
    line-height: 1.4;
    margin-bottom: 6px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.item-excerpt {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.45);
    line-height: 1.6;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.item-footer {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 12px;
    padding-top: 10px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    font-size: 11px;
    color: rgba(255, 255, 255, 0.25);
}

.item-date {
    flex: 1;
}

.item-read {
    font-family: 'JetBrains Mono', 'Noto Sans Mono', monospace;
}

.item-likes {
    display: flex;
    align-items: center;
    gap: 3px;
    transition: color 0.2s ease;
}

.item-likes:hover {
    color: #ff6b6b;
}

.loading-text,
.empty-text {
    text-align: center;
    padding: 60px;
    color: rgba(255, 255, 255, 0.15);
    font-size: 14px;
}

/* ===== 骨架屏 ===== */
.skeleton-masonry {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
}

.skeleton-col {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.skeleton-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 18px;
    overflow: hidden;
}

.skeleton-card-body {
    padding: 14px 16px 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.skeleton-card-footer {
    display: flex;
    gap: 12px;
    margin-top: 4px;
}

/* ===== 右侧：热力图 ===== */
.articles-sidebar {
    width: 200px;
    flex-shrink: 0;
    position: sticky;
    top: 24px;
}

/* ===== 响应式 ===== */
@media (max-width: 900px) {
    .articles-inner {
        flex-direction: column;
    }

    .articles-sidebar {
        width: 100%;
        position: static;
    }

    .masonry {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 600px) {
    .masonry {
        grid-template-columns: 1fr;
    }

    .head-title {
        font-size: 26px;
    }

    .articles-page {
        padding: 0 12px 40px;
    }
}
</style>
