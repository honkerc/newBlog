<template>
    <div class="search-page">
        <div class="search-inner">
            <!-- 搜索框 -->
            <div class="search-header">
                <div class="search-bar">
                    <i class="fas fa-search search-bar-icon"></i>
                    <input ref="searchInput" type="text" v-model="query" placeholder="搜索文章、动态..."
                        @keyup.enter="doSearch" class="search-bar-input" />
                    <button v-if="query" class="search-clear" @click="query = ''; results = []; searched = false">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="search-hint" v-if="!searched">输入关键词，搜索文章和动态</div>
            </div>

            <!-- 骨架屏 -->
            <div class="skeleton-search" v-if="loading">
                <div class="skeleton-search-results">
                    <div class="skeleton-search-item" v-for="n in 5" :key="n">
                        <Skeleton type="circle" width="40px" height="40px" borderRadius="10px" />
                        <div class="skeleton-search-body">
                            <Skeleton type="text" width="60px" height="12px" />
                            <Skeleton type="title" />
                            <Skeleton type="text" width="85%" />
                            <div class="skeleton-search-footer">
                                <Skeleton type="text" width="80px" height="10px" />
                                <Skeleton type="text" width="50px" height="10px" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 搜索结果 -->
            <div class="search-results" v-if="searched && !loading">

                <div class="result-meta" v-if="results.length">
                    共找到 <strong>{{ total }}</strong> 条结果
                </div>
                <div class="result-empty" v-if="!results.length">
                    <i class="fas fa-search"></i>
                    <p>没有找到 "{{ lastQuery }}" 的相关内容</p>
                </div>
                <div class="result-list">
                    <div class="result-item" v-for="item in results" :key="item.type + '-' + item.id"
                        @click="goToResult(item)">
                        <div class="result-icon" :class="item.type">
                            <i :class="item.type === 'post' ? 'fas fa-file-alt' : 'fas fa-clock'"></i>
                        </div>
                        <div class="result-body">
                            <div class="result-type">{{ item.type === 'post' ? '文章' : '动态' }}</div>
                            <div class="result-title" v-if="item.title" v-html="highlightText(item.title)"></div>
                            <div class="result-snippet" v-html="highlightText(item.snippet)"></div>
                            <div class="result-footer">
                                <span class="result-date">{{ formatDate(item.created_at) }}</span>
                                <span class="result-category" v-if="item.category">{{ item.category }}</span>
                                <span class="result-match" v-if="item.matched_in_title">标题匹配</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { publicApi } from '@/utils/api'
import Skeleton from '@/components/Skeleton.vue'

const router = useRouter()
const route = useRoute()

const searchInput = ref(null)
const query = ref('')
const lastQuery = ref('')
const results = ref([])
const total = ref(0)
const loading = ref(false)
const searched = ref(false)

function formatDate(dateStr) {
    if (!dateStr) return ''
    const d = new Date(dateStr)
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return `${y}.${m}.${day}`
}

function highlightText(text) {
    if (!text || !lastQuery.value) return text || ''
    const q = lastQuery.value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    const regex = new RegExp(`(${q})`, 'gi')
    return text.replace(regex, '<mark>$1</mark>')
}

async function doSearch() {
    const q = query.value.trim()
    if (!q) return

    lastQuery.value = q
    loading.value = true
    searched.value = true

    try {
        const res = await publicApi.search({ q, page: 1, page_size: 20 })
        results.value = res.items || []
        total.value = res.total || 0
    } catch (e) {
        console.error('搜索失败:', e)
        results.value = []
        total.value = 0
    } finally {
        loading.value = false
    }
}

function goToResult(item) {
    router.push(item.url)
}

onMounted(async () => {
    // 如果 URL 有 q 参数，自动搜索
    const q = route.query.q
    if (q) {
        query.value = q
        await nextTick()
        doSearch()
    }
    // 聚焦搜索框
    searchInput.value?.focus()
})
</script>

<style scoped>
.search-page {
    padding: 0 16px 60px;
}

.search-inner {}

/* ===== 搜索框 ===== */
.search-header {
    padding: 60px 0 40px;
    text-align: center;
}

.search-bar {
    display: flex;
    align-items: center;
    max-width: 560px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 0 18px;
    height: 52px;
    transition: all 0.3s ease;
}

.search-bar:focus-within {
    border-color: rgba(0, 242, 192, 0.2);
    background: rgba(255, 255, 255, 0.05);
    box-shadow: 0 0 0 4px rgba(0, 242, 192, 0.04);
}

.search-bar-icon {
    color: rgba(255, 255, 255, 0.15);
    font-size: 16px;
    margin-right: 14px;
    flex-shrink: 0;
    transition: color 0.2s;
}

.search-bar:focus-within .search-bar-icon {
    color: rgba(0, 242, 192, 0.4);
}

.search-bar-input {
    flex: 1;
    border: none;
    outline: none;
    background: transparent;
    color: #EFF3F8;
    font-size: 16px;
    font-family: inherit;
}

.search-bar-input::placeholder {
    color: rgba(255, 255, 255, 0.12);
}

.search-clear {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    border: none;
    background: transparent;
    color: rgba(255, 255, 255, 0.15);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
    flex-shrink: 0;
}

.search-clear:hover {
    color: rgba(255, 255, 255, 0.5);
    background: rgba(255, 255, 255, 0.04);
}

.search-hint {
    margin-top: 16px;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.12);
}

/* ===== 加载状态 ===== */
.search-loading {
    display: flex;
    justify-content: center;
    padding: 60px;
}

.loading-spinner {
    width: 24px;
    height: 24px;
    border: 2px solid rgba(255, 255, 255, 0.04);
    border-top-color: #00F2C0;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

/* ===== 骨架屏 ===== */
.skeleton-search {
    padding: 0;
}

.skeleton-search-results {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.skeleton-search-item {
    display: flex;
    gap: 14px;
    padding: 16px 18px;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.04);
}

.skeleton-search-body {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.skeleton-search-footer {
    display: flex;
    gap: 12px;
    margin-top: 2px;
}

/* ===== 搜索结果 ===== */
.result-meta {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.2);
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

.result-meta strong {
    color: rgba(255, 255, 255, 0.5);
}

.result-empty {
    text-align: center;
    padding: 60px 20px;
    color: rgba(255, 255, 255, 0.1);
}

.result-empty i {
    font-size: 32px;
    margin-bottom: 12px;
}

.result-empty p {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.15);
}

.result-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.result-item {
    display: flex;
    gap: 14px;
    padding: 16px 18px;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.04);
    cursor: pointer;
    transition: all 0.2s ease;
}

.result-item:hover {
    background: rgba(255, 255, 255, 0.04);
    border-color: rgba(255, 255, 255, 0.08);
    transform: translateX(4px);
}

.result-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: 15px;
}

.result-icon.post {
    background: rgba(0, 242, 192, 0.08);
    color: #00F2C0;
}

.result-icon.moment {
    background: rgba(255, 193, 7, 0.08);
    color: #ffc107;
}

.result-body {
    flex: 1;
    min-width: 0;
}

.result-type {
    font-size: 11px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.15);
    margin-bottom: 4px;
}

.result-title {
    font-size: 15px;
    font-weight: 600;
    color: #EFF3F8;
    margin-bottom: 4px;
    line-height: 1.4;
}

.result-snippet {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.45);
    line-height: 1.6;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.result-snippet :deep(mark) {
    background: rgba(0, 242, 192, 0.15);
    color: #00F2C0;
    padding: 0 2px;
    border-radius: 2px;
}

.result-title :deep(mark) {
    background: rgba(0, 242, 192, 0.15);
    color: #00F2C0;
    padding: 0 2px;
    border-radius: 2px;
}

.result-footer {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 8px;
    font-size: 11px;
    color: rgba(255, 255, 255, 0.15);
}

.result-category {
    padding: 1px 8px;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.04);
}

.result-match {
    padding: 1px 8px;
    border-radius: 6px;
    background: rgba(0, 242, 192, 0.08);
    color: rgba(0, 242, 192, 0.5);
    font-size: 10px;
}

/* ===== 响应式 ===== */
@media (max-width: 600px) {
    .search-header {
        padding: 40px 0 24px;
    }

    .search-bar {
        height: 46px;
        padding: 0 14px;
    }

    .search-bar-input {
        font-size: 14px;
    }

    .result-item {
        padding: 14px;
    }
}
</style>
