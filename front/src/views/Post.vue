<template>
    <div class="post-layout">
        <!-- 骨架屏 -->
        <div class="skeleton-post" v-if="loading">
            <div class="skeleton-post-header">
                <Skeleton type="title" width="70%" height="28px" />
                <div class="skeleton-post-meta">
                    <Skeleton type="text" width="60px" height="12px" />
                    <Skeleton type="text" width="100px" height="12px" />
                    <Skeleton type="text" width="80px" height="12px" />
                </div>
                <Skeleton type="image" height="300px" borderRadius="16px" />
            </div>
            <div class="skeleton-post-content">
                <Skeleton type="text" width="100%" />
                <Skeleton type="text" width="100%" />
                <Skeleton type="text" width="85%" />
                <Skeleton type="text" width="100%" />
                <Skeleton type="text" width="60%" />
                <div style="height: 20px"></div>
                <Skeleton type="text" width="100%" />
                <Skeleton type="text" width="90%" />
                <Skeleton type="text" width="100%" />
                <Skeleton type="text" width="70%" />
                <div style="height: 20px"></div>
                <Skeleton type="text" width="100%" />
                <Skeleton type="text" width="100%" />
                <Skeleton type="text" width="55%" />
            </div>
        </div>


        <!-- 错误状态 -->
        <div class="loading-container" v-else-if="error">
            <div class="error-text">{{ error }}</div>
        </div>

        <!-- Markdown 内容 -->
        <main class="markdown-body" v-else>
            <!-- 文章头部 -->
            <div class="post-header">
                <h1 class="post-title">{{ post.title }}</h1>
                <div class="post-meta">
                    <span class="meta-category" v-if="post.category">{{ post.category }}</span>
                    <span class="meta-date">{{ formatDate(post.created_at) }}</span>
                    <span class="meta-views"><i class="far fa-eye"></i> {{ post.view_count }}</span>
                    <span class="meta-likes"><i class="far fa-heart"></i> {{ post.like_count }}</span>
                </div>
                <div class="post-cover" v-if="post.cover_url">
                    <img :src="resolveThumbUrl(post.cover_url)" alt="cover" />
                </div>
            </div>

            <!-- 渲染 Markdown 内容 -->
            <div class="markdown-body" v-html="renderedContent"></div>
        </main>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { publicApi, resolveImageUrl, resolveThumbUrl } from '@/utils/api'
import Skeleton from '@/components/Skeleton.vue'
import { marked } from 'marked'
import hljs from 'highlight.js'

// 自定义代码块渲染，使用 highlight.js 高亮
const renderer = new marked.Renderer()
function escapeHtml(str) {
    const map = { '&': 'amp', '<': 'lt', '>': 'gt', '"': 'quot' }
    return str.replace(/[&<>"]/g, function (m) { return '&' + map[m] + ';' })
}

renderer.code = function ({ text, lang }) {
    // 转义 HTML 实体，防止代码中的 HTML 标签被浏览器渲染
    const escaped = escapeHtml(text)

    let highlighted
    if (lang && hljs.getLanguage(lang)) {
        try {
            highlighted = hljs.highlight(escaped, { language: lang }).value
        } catch (e) {
            highlighted = escaped
        }
    } else {
        highlighted = hljs.highlightAuto(escaped).value
    }

    const langAttr = lang ? ' data-lang="' + lang + '"' : ''
    return '<pre' + langAttr + '><code class="hljs language-' + (lang || '') + '">' + highlighted + '</code></pre>'
}

marked.setOptions({
    renderer,
    breaks: true,
    gfm: true,
})

const route = useRoute()
const loading = ref(true)
const error = ref('')
const post = ref({})
const activeToc = ref('')
const toc = ref([])

function formatDate(dateStr) {
    if (!dateStr) return ''
    const d = new Date(dateStr)
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return `${y}.${m}.${day}`
}

const renderedContent = computed(() => {
    if (!post.value.content) return ''
    return marked.parse(post.value.content, { breaks: true, gfm: true })
})

// 从渲染后的内容提取 TOC
function extractToc(content) {
    if (!content) return []
    const items = []
    const headingRegex = /<h([1-6])\s+id="([^"]+)">([^<]+)<\/h[1-6]>/g
    let match
    while ((match = headingRegex.exec(content)) !== null) {
        const level = parseInt(match[1])
        const id = match[2]
        const text = match[3]
        if (level <= 2) {
            items.push({ id, text, children: [] })
        }
    }
    return items
}

function scrollTo(id) {
    const el = document.getElementById(id)
    if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' })
        activeToc.value = id
    }
}

function onScroll() {
    const headings = document.querySelectorAll('.markdown-body h1, .markdown-body h2')
    let currentId = activeToc.value
    for (const h of headings) {
        const rect = h.getBoundingClientRect()
        if (rect.top <= 120) {
            currentId = h.id
        }
    }
    activeToc.value = currentId
}

onMounted(async () => {
    const id = route.params.id
    if (!id) {
        error.value = '文章不存在'
        loading.value = false
        return
    }

    try {
        const res = await publicApi.getPost(id)
        post.value = res
        await nextTick()
        // 提取目录
        toc.value = extractToc(renderedContent.value)
        if (toc.value.length > 0) {
            activeToc.value = toc.value[0].id
        }
    } catch (e) {
        console.error('加载文章失败:', e)
        error.value = '文章加载失败: ' + e.message
    } finally {
        loading.value = false
    }
})
</script>

<style scoped>
.post-layout {
    min-height: 100%;
    position: relative;
    padding: 0 24px 60px;
}

/* ===== 骨架屏 ===== */
.skeleton-post {
    padding: 32px 0;
}

.skeleton-post-header {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 32px;
    padding-bottom: 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.skeleton-post-meta {
    display: flex;
    gap: 12px;
}

.skeleton-post-content {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

/* ===== 加载/错误状态 ===== */
.loading-container {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 400px;
}

.loading-text {
    color: rgba(255, 255, 255, 0.3);
    font-size: 14px;
}

.error-text {
    color: #ff6b6b;
    font-size: 14px;
}

/* ===== Markdown 内容 ===== */
.markdown-body {
    max-width: 800px;
    margin: 0 auto;
}

/* ===== 文章头部 ===== */
.post-header {
    margin-bottom: 32px;
    padding-bottom: 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.post-title {
    font-size: 28px;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1.3;
    margin-bottom: 12px;
    letter-spacing: -0.3px;
}

.post-meta {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.3);
    flex-wrap: wrap;
}

.meta-category {
    padding: 2px 10px;
    border-radius: 10px;
    font-size: 11px;
    color: #00F2C0;
    background: rgba(0, 242, 192, 0.1);
    border: 1px solid rgba(0, 242, 192, 0.2);
}

.meta-views i,
.meta-likes i {
    margin-right: 3px;
}

.post-cover {
    margin-top: 20px;
    border-radius: 16px;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.03);
}

.post-cover img {
    width: 100%;
    display: block;
    max-height: 400px;
    object-fit: cover;
}

/* ===== 文章内容使用全局 post.css 的 .markdown-body 样式 ===== */

/* ===== 响应式断点 ===== */
@media (min-width: 1600px) {
    .markdown-body {
        max-width: 900px;
    }
}

@media (max-width: 900px) {
    .post-layout {
        padding: 0 12px 60px;
    }
}

@media (max-width: 600px) {
    .post-layout {
        padding: 0 8px 60px;
    }

    .post-title {
        font-size: 22px;
    }
}
</style>
