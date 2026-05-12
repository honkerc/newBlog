<template>
    <div class="admin-editor">
        <!-- 专注模式：纯内容编辑区 -->
        <div class="focus-mode" v-show="focusActive">
            <textarea v-model="form.content" placeholder="开始写作..." class="focus-input"></textarea>
            <button class="focus-exit" @click="focusActive = false" title="退出专注模式">
                <i class="fas fa-compress"></i>
            </button>
        </div>

        <!-- 步骤 1：编辑器 -->
        <div class="step-content" v-show="step === 1 && !focusActive">
            <!-- 顶部栏 -->
            <div class="editor-topbar">
                <div class="topbar-tabs">
                    <button class="tab-btn" :class="{ active: mode === 'edit' }" @click="mode = 'edit'">
                        <i class="fas fa-pen"></i> 编辑
                    </button>
                    <button class="tab-btn" :class="{ active: mode === 'preview' }" @click="mode = 'preview'">
                        <i class="fas fa-eye"></i> 预览
                    </button>
                    <button class="tab-btn" :class="{ active: mode === 'split' }" @click="mode = 'split'">
                        <i class="fas fa-columns"></i> 双栏
                    </button>
                </div>
                <div class="topbar-right">
                    <button class="focus-btn" @click="focusActive = true" title="专注模式">
                        <i class="fas fa-expand"></i>
                    </button>
                    <button class="nav-btn next" @click="step = 2">
                        下一步 <i class="fas fa-arrow-right"></i>
                    </button>
                </div>
            </div>

            <div class="editor-write">
                <div class="content-area" :class="{ split: mode === 'split' }"
                    v-if="mode === 'edit' || mode === 'split'" style="position: relative;">
                    <input type="text" v-model="form.title" placeholder="无标题" class="title-input" />
                    <textarea ref="contentInput" v-model="form.content" placeholder="开始写作..." class="content-input"
                        @input="onContentInput" @keydown="onContentKeydown" @click="closeSlashMenu"></textarea>
                    <!-- 隐藏的文件上传输入 -->
                    <input type="file" ref="uploadInput" accept="image/*,video/*,.pdf,.doc,.docx,.zip"
                        @change="onUploadSelected" style="display:none" />
                    <!-- 斜杠菜单 -->
                    <div class="slash-menu" v-if="slashMenu.visible" :style="slashMenu.style">
                        <div class="slash-search">
                            <i class="fas fa-search"></i>
                            <input type="text" v-model="slashMenu.filter" placeholder="过滤..." @keydown="onSlashKeydown"
                                ref="slashInput" />
                        </div>
                        <div class="slash-items">
                            <div class="slash-item" v-for="(item, i) in filteredSlashItems" :key="i"
                                :class="{ selected: slashMenu.selected === i }" @click="insertSlashItem(item)"
                                @mouseenter="slashMenu.selected = i">
                                <div class="slash-icon"><i :class="item.icon"></i></div>
                                <div class="slash-info">
                                    <div class="slash-name">{{ item.name }}</div>
                                    <div class="slash-desc">{{ item.desc }}</div>
                                </div>
                            </div>
                            <div class="slash-empty" v-if="!filteredSlashItems.length">无匹配</div>
                        </div>
                    </div>
                </div>
                <div class="preview-area" :class="{ split: mode === 'split', full: mode === 'preview' }"
                    v-if="mode === 'preview' || mode === 'split'">
                    <div class="markdown-body" v-html="renderedContent"></div>
                </div>
            </div>
        </div>

        <!-- 步骤 2：详细信息 -->
        <div class="step-content" v-show="step === 2">
            <!-- 步骤指示器 -->
            <div class="step-indicator">
                <div class="step-item" :class="{ active: step === 1, done: step > 1 }">
                    <span class="step-num">1</span>
                    <span class="step-label">写文章</span>
                </div>
                <div class="step-line" :class="{ active: step > 1 }"></div>
                <div class="step-item" :class="{ active: step === 2, done: step > 2 }">
                    <span class="step-num">2</span>
                    <span class="step-label">详细信息</span>
                </div>
            </div>

            <!-- 详细信息表单 -->
            <div class="detail-grid">
                <div class="detail-section">
                    <h4 class="detail-title">分类与标签</h4>
                    <div class="form-group">
                        <label>分类</label>
                        <select v-model="form.category" class="form-select">
                            <option value="">选择分类</option>
                            <option value="技术">技术</option>
                            <option value="设计">设计</option>
                            <option value="生活">生活</option>
                            <option value="读书">读书</option>
                            <option value="阅读">阅读</option>
                            <option value="旅行">旅行</option>
                            <option value="思考">思考</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>标签</label>
                        <div class="tag-input-wrap">
                            <input type="text" v-model="form.tag" placeholder="输入标签" class="form-input"
                                @focus="onTagFocus" @input="onTagInput" />
                            <!-- 读书笔记提示 -->
                            <div class="book-hint" v-if="form.category === '读书' && form.tag">
                                <i class="fas fa-book-open"></i>
                                将作为 <strong>{{ form.tag }}</strong> 的读书笔记
                            </div>
                            <!-- 书籍建议下拉 -->
                            <div class="book-suggestions" v-if="showBookSuggestions && filteredBooks.length">
                                <div class="suggestion-item" v-for="book in filteredBooks" :key="book.id"
                                    @click="selectBook(book)">
                                    <span class="suggestion-icon"><i class="fas fa-book"></i></span>
                                    <span class="suggestion-name">{{ book.title }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="detail-section">
                    <h4 class="detail-title">封面</h4>
                    <ImageUploader v-model="form.cover_url" />
                </div>

                <div class="detail-section full">
                    <h4 class="detail-title">摘要</h4>
                    <textarea v-model="form.summary" placeholder="文章摘要..." rows="4" class="form-textarea"></textarea>
                </div>
            </div>

            <!-- 底部操作栏 -->
            <div class="bottom-bar">
                <button class="nav-btn prev" @click="step = 1">
                    <i class="fas fa-arrow-left"></i> 上一步
                </button>
                <div class="bottom-actions">
                    <button class="action-btn draft" @click="handleSaveDraft" :disabled="saving">
                        <i class="fas fa-save"></i> 存草稿
                    </button>
                    <button class="action-btn publish" @click="handleSave" :disabled="saving">
                        <i class="fas fa-check"></i>
                        <span>{{ saving ? '发布中...' : '发布' }}</span>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { adminApi } from '@/utils/api'
import { useToast } from '@/utils/toast'
import { marked } from 'marked'
import hljs from 'highlight.js'
import ImageUploader from '@/components/ImageUploader.vue'

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

const router = useRouter()
const route = useRoute()
const { toast } = useToast()

const step = ref(1)
const mode = ref('edit')
const focusActive = ref(false)

// 专注模式时隐藏 Top 组件
watch(focusActive, (val) => {
    const topEl = document.querySelector('.top-menu')
    if (topEl) {
        topEl.style.display = val ? 'none' : ''
    }
})
const editingId = ref(null)
const saving = ref(false)

const form = reactive({
    title: '',
    category: '',
    tag: '',
    cover_url: '',
    summary: '',
    content: '',
})

const DRAFT_KEY = 'editor_draft'

// ===== 书籍建议下拉 =====
const books = ref([])
const showBookSuggestions = ref(false)
const filteredBooks = computed(() => {
    if (!books.value.length) return []
    if (!form.tag) return books.value
    const q = form.tag.toLowerCase()
    return books.value.filter(b => b.title.toLowerCase().includes(q))
})

function onTagFocus() {
    if (form.category === '读书' && books.value.length) {
        showBookSuggestions.value = true
    }
}

function onTagInput() {
    if (form.category === '读书' && books.value.length) {
        showBookSuggestions.value = true
    }
}

function selectBook(book) {
    form.tag = book.title
    showBookSuggestions.value = false
}

// 点击其他地方关闭建议
function closeSuggestions(e) {
    if (!e.target.closest('.tag-input-wrap')) {
        showBookSuggestions.value = false
    }
}

// ===== 斜杠菜单 =====
const contentInput = ref(null)
const slashInput = ref(null)
const uploadInput = ref(null)
let pendingUploadType = null // 'image' | 'file' | 'video'

const slashItems = [
    // 优先显示：上传、表格、代码块
    { name: '图片上传', desc: '上传并插入图片', icon: 'fas fa-image', insert: '__upload_image__', filter: 'image 图片 上传' },
    { name: '文件上传', desc: '上传并插入文件链接', icon: 'fas fa-file', insert: '__upload_file__', filter: 'file 文件 上传' },
    { name: '视频上传', desc: '上传并插入视频', icon: 'fas fa-video', insert: '__upload_video__', filter: 'video 视频 上传' },
    { name: '代码块', desc: '代码片段', icon: 'fas fa-code', insert: '```\n\n```', filter: 'code 代码 代码块' },
    { name: '表格', desc: '插入表格', icon: 'fas fa-table', insert: '| 列1 | 列2 | 列3 |\n| --- | --- | --- |\n| 内容 | 内容 | 内容 |', filter: 'table 表格' },
    // 常用格式
    { name: '粗体', desc: '加粗文本', icon: 'fas fa-bold', insert: '**粗体文本**', filter: 'bold 粗体' },
    { name: '斜体', desc: '斜体文本', icon: 'fas fa-italic', insert: '*斜体文本*', filter: 'italic 斜体' },
    { name: '链接', desc: '插入链接', icon: 'fas fa-link', insert: '[链接文字](url)', filter: 'link 链接 url' },
    { name: '行内代码', desc: '行内代码', icon: 'fas fa-terminal', insert: '`代码`', filter: 'inline code 行内代码' },
    // 块级元素
    { name: '无序列表', desc: '项目列表', icon: 'fas fa-list-ul', insert: '- ', filter: 'ul 无序列表 列表' },
    { name: '有序列表', desc: '编号列表', icon: 'fas fa-list-ol', insert: '1. ', filter: 'ol 有序列表 编号' },
    { name: '任务列表', desc: '待办事项', icon: 'fas fa-check-square', insert: '- [ ] ', filter: 'todo 任务 待办' },
    { name: '引用', desc: '引用文本', icon: 'fas fa-quote-right', insert: '> ', filter: 'quote 引用 块引用' },
    { name: '分割线', desc: '水平分割线', icon: 'fas fa-minus', insert: '\n---\n', filter: 'hr 分割线 分隔线' },
    // 标题（默认不显示，搜索时可用）
    { name: '标题 1', desc: '大标题', icon: 'fas fa-heading', insert: '# ', filter: 'h1 标题 1', hidden: true },
    { name: '标题 2', desc: '中标题', icon: 'fas fa-heading', insert: '## ', filter: 'h2 标题 2', hidden: true },
    { name: '标题 3', desc: '小标题', icon: 'fas fa-heading', insert: '### ', filter: 'h3 标题 3', hidden: true },
]

const slashMenu = reactive({
    visible: false,
    filter: '',
    selected: 0,
    style: { top: '0px', left: '0px' },
})

const filteredSlashItems = computed(() => {
    if (!slashMenu.filter) return slashItems.filter(item => !item.hidden)
    const q = slashMenu.filter.toLowerCase()
    return slashItems.filter(item => item.filter.toLowerCase().includes(q))
})

// 记录斜杠菜单触发时的插入位置（移除 / 后的光标位置）
let slashInsertPos = -1

function onContentInput(e) {
    const textarea = e.target
    const val = textarea.value
    const cursorPos = textarea.selectionStart
    const textBefore = val.substring(0, cursorPos)
    const slashIdx = textBefore.lastIndexOf('/')

    if (slashIdx !== -1 && (slashIdx === 0 || textBefore[slashIdx - 1] === '\n' || textBefore[slashIdx - 1] === ' ')) {
        const afterSlash = textBefore.substring(slashIdx + 1)
        // 只显示菜单，如果后面没有换行
        if (!afterSlash.includes('\n')) {
            slashMenu.filter = afterSlash
            slashMenu.selected = 0
            slashMenu.visible = true

            // 移除输入的 / 字符，并记录插入位置
            const before = val.substring(0, slashIdx)
            const after = val.substring(cursorPos)
            form.content = before + after
            slashInsertPos = slashIdx

            // 恢复光标位置到 / 被移除的位置
            requestAnimationFrame(() => {
                textarea.setSelectionRange(slashIdx, slashIdx)
            })

            // 定位菜单
            const rect = textarea.getBoundingClientRect()
            const lineHeight = 24
            const lines = before.split('\n')
            const lineNum = lines.length
            const lastLineLen = lines[lines.length - 1].length
            // 估算位置
            const charWidth = 8.5
            const left = Math.min(lastLineLen * charWidth, textarea.clientWidth - 280)
            const top = (lineNum - 1) * lineHeight + 28
            slashMenu.style = {
                top: top + 'px',
                left: Math.max(0, left) + 'px',
            }

            // 下次 tick 聚焦搜索框
            setTimeout(() => {
                slashInput.value?.focus()
            }, 0)
            return
        }
    }
    closeSlashMenu()
}

function closeSlashMenu() {
    slashMenu.visible = false
    slashMenu.filter = ''
    slashMenu.selected = 0
}

function onContentKeydown(e) {
    if (!slashMenu.visible) return

    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault()
        const items = filteredSlashItems.value
        if (!items.length) return
        if (e.key === 'ArrowDown') {
            slashMenu.selected = (slashMenu.selected + 1) % items.length
        } else {
            slashMenu.selected = (slashMenu.selected - 1 + items.length) % items.length
        }
    } else if (e.key === 'Enter' || e.key === 'Tab') {
        e.preventDefault()
        const items = filteredSlashItems.value
        if (items.length > 0 && items[slashMenu.selected]) {
            insertSlashItem(items[slashMenu.selected])
        }
    } else if (e.key === 'Escape') {
        e.preventDefault()
        closeSlashMenu()
    }
}

function onSlashKeydown(e) {
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault()
        const items = filteredSlashItems.value
        if (!items.length) return
        if (e.key === 'ArrowDown') {
            slashMenu.selected = (slashMenu.selected + 1) % items.length
        } else {
            slashMenu.selected = (slashMenu.selected - 1 + items.length) % items.length
        }
    } else if (e.key === 'Enter') {
        e.preventDefault()
        const items = filteredSlashItems.value
        if (items.length > 0 && items[slashMenu.selected]) {
            insertSlashItem(items[slashMenu.selected])
        }
    } else if (e.key === 'Escape') {
        e.preventDefault()
        closeSlashMenu()
        contentInput.value?.focus()
    }
}

function insertSlashItem(item) {
    const textarea = contentInput.value
    if (!textarea) return

    // 处理上传类项目
    if (item.insert === '__upload_image__') {
        pendingUploadType = 'image'
        closeSlashMenu()
        uploadInput.value.click()
        return
    }
    if (item.insert === '__upload_file__') {
        pendingUploadType = 'file'
        closeSlashMenu()
        uploadInput.value.click()
        return
    }
    if (item.insert === '__upload_video__') {
        pendingUploadType = 'video'
        closeSlashMenu()
        uploadInput.value.click()
        return
    }

    // 使用记录的插入位置（/ 被移除后的光标位置）
    const pos = slashInsertPos
    slashInsertPos = -1

    if (pos === -1) {
        closeSlashMenu()
        return
    }

    const val = textarea.value
    const before = val.substring(0, pos)
    const after = val.substring(pos)

    let insert = item.insert
    // 对于块级元素，在开头加换行
    if (['# ', '## ', '### ', '- ', '1. ', '> ', '```\n\n```', '\n---\n', '- [ ] '].includes(insert)) {
        if (before.length > 0 && !before.endsWith('\n')) {
            insert = '\n' + insert
        }
    }

    const newVal = before + insert + after
    form.content = newVal

    // 计算新光标位置
    let newCursor = before.length + insert.length
    // 对于代码块，把光标放在中间
    if (item.insert === '```\n\n```') {
        newCursor = before.length + insert.length - 3
    }

    closeSlashMenu()

    // 聚焦并设置光标
    textarea.focus()
    requestAnimationFrame(() => {
        textarea.setSelectionRange(newCursor, newCursor)
    })
}

async function onUploadSelected(e) {
    const file = e.target.files[0]
    if (!file) return

    const type = pendingUploadType
    pendingUploadType = null

    try {
        const result = await adminApi.uploadFile(file)
        const url = result.url

        const textarea = contentInput.value
        if (!textarea) return

        const cursorPos = textarea.selectionStart
        const before = form.content.substring(0, cursorPos)
        const after = form.content.substring(cursorPos)

        let insert = ''
        if (type === 'image') {
            insert = `![${file.name}](${url})`
        } else if (type === 'video') {
            insert = `<video src="${url}" controls></video>`
        } else {
            insert = `[${file.name}](${url})`
        }

        form.content = before + insert + after
        textarea.focus()
        requestAnimationFrame(() => {
            textarea.setSelectionRange(before.length + insert.length, before.length + insert.length)
        })
    } catch (e) {
        toast('上传失败: ' + e.message, 'error')
    }

    // 重置 input 以便重复选择同一文件
    e.target.value = ''
}

// 从 localStorage 恢复草稿
function loadDraft() {
    try {
        const saved = localStorage.getItem(DRAFT_KEY)
        if (saved) {
            const data = JSON.parse(saved)
            form.title = data.title || ''
            form.content = data.content || ''
        }
    } catch (e) {
        // ignore
    }
}

// 清空本地草稿
function clearDraft() {
    try {
        localStorage.removeItem(DRAFT_KEY)
    } catch (e) {
        // ignore
    }
}

// 保存草稿到 localStorage
function saveDraft() {
    // 编辑已有文章时不覆盖本地草稿
    if (editingId.value) return
    try {
        localStorage.setItem(DRAFT_KEY, JSON.stringify({
            title: form.title,
            content: form.content,
        }))
    } catch (e) {
        // ignore
    }
}

// 监听标题和内容变化，自动保存到本地（仅新建文章时）
watch(() => form.title, saveDraft)
watch(() => form.content, saveDraft)

onMounted(async () => {
    const id = route.query.id
    if (id) {
        editingId.value = id
        try {
            const post = await adminApi.getPost(id)
            if (post) {
                form.title = post.title || ''
                form.category = post.category || ''
                form.tag = post.tag || ''
                form.cover_url = post.cover_url || ''
                form.summary = post.summary || ''
                form.content = post.content || ''
            }
        } catch (e) {
            toast('加载文章失败: ' + e.message, 'error')
        }
    } else {
        // 没有编辑已有文章时，从本地恢复草稿
        loadDraft()
    }

    // 加载书籍列表（用于读书笔记建议）
    try {
        const res = await adminApi.getBooks()
        if (res && res.items) {
            books.value = res.items
        }
    } catch (e) {
        // 静默失败，不影响编辑器使用
    }

    // 点击其他地方关闭书籍建议
    document.addEventListener('click', closeSuggestions)
})

onUnmounted(() => {
    document.removeEventListener('click', closeSuggestions)
})

const renderedContent = computed(() => {
    // 构建文章头部（标题 + 元信息），与真实文章详情保持一致
    let header = ''
    if (form.title) {
        header += `<div class="post-header"><h1 class="post-title">${escapeHtml(form.title)}</h1>`
        header += `<div class="post-meta">`
        if (form.category) {
            header += `<span class="meta-category">${escapeHtml(form.category)}</span>`
        }
        header += `<span class="meta-date">刚刚</span>`
        header += `</div></div>`
    }
    if (!form.content) {
        return header || '<p style="color:rgba(255,255,255,0.08)">暂无内容</p>'
    }
    return header + marked.parse(form.content, { breaks: true, gfm: true })
})

function autoResize(e) {
    e.target.style.height = 'auto'
    e.target.style.height = e.target.scrollHeight + 'px'
}

async function handleSave() {
    if (!form.title.trim()) {
        toast('请输入文章标题', 'error')
        return
    }
    if (!form.content.trim()) {
        toast('请输入文章内容', 'error')
        return
    }

    saving.value = true
    try {
        const data = {
            title: form.title.trim(),
            category: form.category || '',
            tag: form.tag || '',
            cover_url: form.cover_url || '',
            summary: form.summary || '',
            content: form.content,
            is_published: true,
        }

        if (editingId.value) {
            await adminApi.updatePost(editingId.value, data)
            toast('文章已更新', 'success')
        } else {
            await adminApi.createPost(data)
            toast('文章已发布', 'success')
        }
        clearDraft()
        router.push('/admin/articles')
    } catch (e) {
        toast('操作失败: ' + e.message, 'error')
    } finally {
        saving.value = false
    }
}

async function handleSaveDraft() {
    if (!form.title.trim()) {
        toast('请输入文章标题', 'error')
        return
    }

    saving.value = true
    try {
        const data = {
            title: form.title.trim(),
            category: form.category || '',
            tag: form.tag || '',
            cover_url: form.cover_url || '',
            summary: form.summary || '',
            content: form.content,
            is_published: false,
        }

        if (editingId.value) {
            await adminApi.updatePost(editingId.value, data)
            toast('草稿已保存', 'success')
        } else {
            await adminApi.createPost(data)
            toast('草稿已保存', 'success')
        }
        router.push('/admin/articles')
    } catch (e) {
        toast('操作失败: ' + e.message, 'error')
    } finally {
        saving.value = false
    }
}
</script>

<style scoped>
.admin-editor {
    max-width: 800px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

/* ===== 步骤内容 ===== */
.step-content {
    flex: 1;
    min-height: 0;
}

/* ===== 顶部栏 ===== */
.editor-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 0;
    margin-bottom: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    flex-shrink: 0;
}

.topbar-tabs {
    display: flex;
    gap: 4px;
    padding: 4px;
    background: rgba(255, 255, 255, 0.02);
    border-radius: 10px;
}

.tab-btn {
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

.tab-btn i {
    font-size: 11px;
}

.tab-btn:hover {
    color: rgba(255, 255, 255, 0.5);
    background: rgba(255, 255, 255, 0.03);
}

.tab-btn.active {
    color: #FFFFFF;
    background: rgba(255, 255, 255, 0.06);
}

/* ===== 专注模式 ===== */
.focus-mode {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    padding: 24px 32px;
}

.focus-input {
    flex: 1;
    width: 100%;
    border: none;
    outline: none;
    background: transparent;
    color: rgba(255, 255, 255, 0.75);
    font-size: 15px;
    font-family: inherit;
    line-height: 1.8;
    resize: none;
    padding: 0;
    overflow-y: auto;
}

.focus-input::placeholder {
    color: rgba(255, 255, 255, 0.08);
}

.focus-exit {
    position: fixed;
    top: 20px;
    right: 24px;
    width: 36px;
    height: 36px;
    border-radius: 8px;
    border: none;
    background: transparent;
    color: rgba(255, 255, 255, 0.3);
    font-size: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
}

.focus-exit:hover {
    color: #00F2C0;
}

.topbar-right {
    display: flex;
    align-items: center;
    gap: 8px;
}

.focus-btn {
    width: 32px;
    height: 32px;
    border-radius: 6px;
    border: none;
    background: transparent;
    color: rgba(255, 255, 255, 0.2);
    font-size: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
}

.focus-btn:hover {
    color: #00F2C0;
}

/* ===== 步骤 1：编辑器 ===== */
.editor-write {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
}

.title-input {
    width: 100%;
    border: none;
    background: transparent;
    color: #FFFFFF;
    font-size: 32px;
    font-weight: 700;
    font-family: inherit;
    outline: none;
    padding: 0;
    margin-bottom: 20px;
    letter-spacing: -0.5px;
}

.title-input::placeholder {
    color: rgba(255, 255, 255, 0.08);
}

.content-area {
    flex: 1;
    overflow-y: auto;
}

.content-area.split {
    width: 50%;
    float: left;
    padding-right: 12px;
    border-right: 1px solid rgba(255, 255, 255, 0.04);
}

.content-input {
    width: 100%;
    min-height: calc(100vh - 200px);
    border: none;
    outline: none;
    background: transparent;
    color: rgba(255, 255, 255, 0.75);
    font-size: 15px;
    font-family: inherit;
    line-height: 1.8;
    resize: vertical;
    padding: 0;
}

.content-input::placeholder {
    color: rgba(255, 255, 255, 0.08);
}

/* ===== 预览区 ===== */
.preview-area {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
}

.preview-area.full {
    flex: 1;
    min-height: 0;
}

.preview-area.split {
    width: 50%;
    float: right;
    padding-left: 12px;
    min-height: 0;
}

/* ===== 预览区文章头部样式（与真实文章详情保持一致） ===== */
.preview-area :deep(.post-header) {
    margin-bottom: 32px;
    padding-bottom: 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.preview-area :deep(.post-title) {
    font-size: 28px;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1.3;
    margin-bottom: 12px;
    letter-spacing: -0.3px;
}

.preview-area :deep(.post-meta) {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.3);
    flex-wrap: wrap;
}

.preview-area :deep(.meta-category) {
    padding: 2px 10px;
    border-radius: 10px;
    font-size: 11px;
    color: #00F2C0;
    background: rgba(0, 242, 192, 0.1);
    border: 1px solid rgba(0, 242, 192, 0.2);
}

.preview-area :deep(.meta-date) {
    color: rgba(255, 255, 255, 0.2);
}

/* ===== 预览区使用全局 post.css 的 .markdown-body 样式 ===== */

/* ===== 步骤指示器 ===== */
.step-indicator {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 32px;
    padding: 16px 0;
}

.step-item {
    display: flex;
    align-items: center;
    gap: 8px;
}

.step-num {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 600;
    background: rgba(255, 255, 255, 0.04);
    color: rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
}

.step-item.active .step-num {
    background: rgba(0, 242, 192, 0.15);
    color: #00F2C0;
}

.step-item.done .step-num {
    background: rgba(0, 242, 192, 0.1);
    color: #00F2C0;
}

.step-label {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.2);
    transition: color 0.3s ease;
}

.step-item.active .step-label {
    color: #FFFFFF;
}

.step-item.done .step-label {
    color: rgba(255, 255, 255, 0.5);
}

.step-line {
    width: 60px;
    height: 1px;
    background: rgba(255, 255, 255, 0.06);
    margin: 0 16px;
    transition: background 0.3s ease;
}

.step-line.active {
    background: rgba(0, 242, 192, 0.3);
}

/* ===== 详细信息表单 ===== */
.detail-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
}

.detail-section {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.detail-section.full {
    grid-column: 1 / -1;
}

.detail-title {
    font-size: 13px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.3);
    margin: 0;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.form-group label {
    font-size: 12px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.25);
}

.form-input,
.form-select,
.form-textarea {
    padding: 10px 14px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    background: rgba(255, 255, 255, 0.02);
    color: #EFF3F8;
    font-size: 14px;
    font-family: inherit;
    outline: none;
    transition: all 0.2s ease;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
    border-color: rgba(0, 242, 192, 0.2);
    background: rgba(255, 255, 255, 0.04);
}

.form-input::placeholder,
.form-textarea::placeholder {
    color: rgba(255, 255, 255, 0.15);
}

.form-select {
    cursor: pointer;
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='rgba(255,255,255,0.2)'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 12px center;
    padding-right: 32px;
}

.form-select option {
    background: #1a1d23;
    color: #EFF3F8;
}

.form-textarea {
    resize: vertical;
    min-height: 100px;
    line-height: 1.6;
}

/* ===== 标签输入（含书籍建议） ===== */
.tag-input-wrap {
    position: relative;
}

.book-hint {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 6px;
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 12px;
    color: rgba(0, 242, 192, 0.7);
    background: rgba(0, 242, 192, 0.06);
    border: 1px solid rgba(0, 242, 192, 0.1);
}

.book-hint i {
    font-size: 11px;
}

.book-hint strong {
    color: #00F2C0;
    font-weight: 600;
}

.book-suggestions {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    z-index: 50;
    margin-top: 4px;
    background: rgba(24, 28, 34, 0.96);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}

.suggestion-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    cursor: pointer;
    transition: all 0.15s ease;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
}

.suggestion-item:hover {
    background: rgba(0, 242, 192, 0.08);
    color: #FFFFFF;
}

.suggestion-icon {
    width: 28px;
    height: 28px;
    border-radius: 6px;
    background: rgba(0, 242, 192, 0.08);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.suggestion-icon i {
    font-size: 12px;
    color: #00F2C0;
}

.suggestion-name {
    font-weight: 500;
}

/* ===== 步骤导航 ===== */
.step-nav {
    display: flex;
    justify-content: flex-end;
    padding: 24px 0;
    margin-top: auto;
}

.nav-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 20px;
    border-radius: 8px;
    border: none;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: inherit;
}

.nav-btn i {
    font-size: 12px;
}

.nav-btn.next {
    background: rgba(0, 242, 192, 0.1);
    color: #00F2C0;
}

.nav-btn.next:hover {
    background: rgba(0, 242, 192, 0.18);
}

.nav-btn.prev {
    background: rgba(255, 255, 255, 0.04);
    color: rgba(255, 255, 255, 0.4);
}

.nav-btn.prev:hover {
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.6);
}

/* ===== 底部操作栏 ===== */
.bottom-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 24px 0;
    margin-top: auto;
}

.bottom-actions {
    display: flex;
    gap: 8px;
}

.action-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 20px;
    border-radius: 8px;
    border: none;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: inherit;
}

.action-btn i {
    font-size: 12px;
}

.action-btn.publish {
    background: rgba(0, 242, 192, 0.1);
    color: #00F2C0;
}

.action-btn.publish:hover:not(:disabled) {
    background: rgba(0, 242, 192, 0.18);
}

.action-btn.publish:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

.action-btn.draft {
    background: rgba(255, 255, 255, 0.04);
    color: rgba(255, 255, 255, 0.4);
}

.action-btn.draft:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.6);
}

.action-btn.draft:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

/* ===== 斜杠菜单（类 settings-card 风格） ===== */
.slash-menu {
    position: absolute;
    z-index: 100;
    width: 280px;
    max-height: 320px;
    background: rgba(24, 28, 34, 0.96);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 8px 40px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.04);
    transition: all 0.2s ease;
}

.slash-menu::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0, 242, 192, 0.08), transparent);
    opacity: 0.6;
    pointer-events: none;
}

.slash-menu::after {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 50% 0%, rgba(0, 242, 192, 0.03), transparent 60%);
    pointer-events: none;
}

.slash-search {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 14px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    position: relative;
    z-index: 1;
}

.slash-search i {
    color: rgba(255, 255, 255, 0.2);
    font-size: 12px;
}

.slash-search input {
    flex: 1;
    border: none;
    outline: none;
    background: transparent;
    color: rgba(255, 255, 255, 0.7);
    font-size: 13px;
    font-family: inherit;
}

.slash-search input::placeholder {
    color: rgba(255, 255, 255, 0.15);
}

.slash-items {
    overflow-y: auto;
    max-height: 260px;
    padding: 4px;
    position: relative;
    z-index: 1;
}

.slash-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.15s ease;
}

.slash-item.selected {
    background: rgba(0, 242, 192, 0.08);
}

.slash-item:hover {
    background: rgba(255, 255, 255, 0.04);
}

.slash-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.04);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    border: 1px solid rgba(255, 255, 255, 0.04);
    transition: all 0.2s ease;
}

.slash-icon i {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.5);
}

.slash-item.selected .slash-icon {
    background: rgba(0, 242, 192, 0.12);
    border-color: rgba(0, 242, 192, 0.15);
}

.slash-item.selected .slash-icon i {
    color: #00F2C0;
}

.slash-info {
    flex: 1;
    min-width: 0;
}

.slash-name {
    font-size: 13px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.7);
}

.slash-desc {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.2);
    margin-top: 1px;
}

.slash-empty {
    text-align: center;
    padding: 20px;
    color: rgba(255, 255, 255, 0.15);
    font-size: 13px;
}

/* ===== 响应式 ===== */
@media (max-width: 600px) {
    .detail-grid {
        grid-template-columns: 1fr;
    }

    .title-input {
        font-size: 24px;
    }

    .bottom-bar {
        flex-direction: column;
        gap: 12px;
    }
}
</style>
