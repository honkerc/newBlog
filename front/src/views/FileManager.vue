<template>
    <div class="file-manager">
        <div class="page-header">
            <h1><i class="fas fa-folder-open"></i> 文件管理</h1>
            <p>浏览和管理服务器文件</p>
        </div>

        <!-- 文件管理器 -->
        <div class="file-browser">
            <!-- 工具栏 -->
            <div class="toolbar">
                <div class="breadcrumb">
                    <span class="breadcrumb-item" @click="navigateTo('')">根目录</span>
                    <span v-for="(seg, i) in breadcrumbs" :key="i" class="breadcrumb-sep">/</span>
                    <span v-for="(seg, i) in breadcrumbs" :key="'b' + i" class="breadcrumb-item"
                        :class="{ active: i === breadcrumbs.length - 1 }"
                        @click="navigateTo(breadcrumbs.slice(0, i + 1).join('/'))">
                        {{ seg }}
                    </span>
                </div>
                <div class="toolbar-actions">
                    <button class="btn btn-sm" @click="showUpload = true" title="上传文件">
                        <i class="fas fa-upload"></i>
                    </button>
                    <button class="btn btn-sm" @click="showMkdir = true" title="新建目录">
                        <i class="fas fa-folder-plus"></i>
                    </button>
                    <button class="btn btn-sm" @click="refresh" title="刷新">
                        <i class="fas fa-sync-alt"></i>
                    </button>
                </div>
            </div>

            <!-- 上传区域 -->
            <div v-if="showUpload" class="upload-area">
                <input type="file" ref="fileInput" multiple @change="handleUpload" style="display:none" />
                <div class="upload-dropzone" @click="$refs.fileInput.click()" @dragover.prevent
                    @drop.prevent="handleDrop">
                    <i class="fas fa-cloud-upload-alt"></i>
                    <span>点击或拖拽文件到此处上传</span>
                </div>
                <div v-if="uploading" class="upload-progress">
                    <span>上传中...</span>
                    <div class="progress-bar">
                        <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
                    </div>
                </div>
            </div>

            <!-- 新建目录 -->
            <div v-if="showMkdir" class="mkdir-area">
                <input v-model="newDirName" class="form-input" placeholder="目录名" @keyup.enter="createDirectory" />
                <button class="btn btn-sm btn-primary" @click="createDirectory">创建</button>
                <button class="btn btn-sm" @click="showMkdir = false; newDirName = ''">取消</button>
            </div>

            <!-- 文件列表 -->
            <div class="file-list">
                <div v-if="loading" class="file-list-loading">
                    <i class="fas fa-spinner fa-spin"></i> 加载中...
                </div>
                <div v-else-if="!items.length" class="file-list-empty">
                    <i class="fas fa-folder-open"></i>
                    <span>空目录</span>
                </div>
                <div v-else v-for="item in items" :key="item.path" class="file-item"
                    :class="{ selected: selectedPath === item.path }" @click="selectItem(item)"
                    @dblclick="openItem(item)">
                    <span class="file-icon">
                        <i v-if="item.is_dir" class="fas fa-folder" style="color: #ffc107"></i>
                        <i v-else-if="item.is_image" class="fas fa-file-image" style="color: #00bcd4"></i>
                        <i v-else-if="item.is_video" class="fas fa-file-video" style="color: #e91e63"></i>
                        <i v-else-if="item.is_audio" class="fas fa-file-audio" style="color: #9c27b0"></i>
                        <i v-else-if="item.is_archive" class="fas fa-file-archive" style="color: #ff9800"></i>
                        <i v-else-if="item.is_code || item.is_text" class="fas fa-file-code" style="color: #4caf50"></i>
                        <i v-else class="fas fa-file" style="color: #888"></i>
                    </span>
                    <span class="file-name">{{ item.name }}</span>
                    <span class="file-size">{{ item.size_display }}</span>
                    <span class="file-date">{{ formatDate(item.modified) }}</span>
                    <span class="file-actions" @click.stop>
                        <button class="btn-icon" @click="downloadItem(item)" title="下载">
                            <i class="fas fa-download"></i>
                        </button>
                        <button class="btn-icon" @click="renameItem(item)" title="重命名">
                            <i class="fas fa-pen"></i>
                        </button>
                        <button class="btn-icon btn-icon-danger" @click="deleteItem(item)" title="删除">
                            <i class="fas fa-trash"></i>
                        </button>
                    </span>
                </div>
            </div>
        </div>

        <!-- Toast -->
        <div v-if="toast" class="toast" :class="toast.type">{{ toast.message }}</div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuth } from '@/stores/auth'

const { API_BASE, getToken } = useAuth()

const currentPath = ref('')
const items = ref([])
const loading = ref(false)
const selectedPath = ref('')

const showUpload = ref(false)
const showMkdir = ref(false)
const newDirName = ref('')
const uploading = ref(false)
const uploadProgress = ref(0)
const fileInput = ref(null)

const toast = ref(null)

const breadcrumbs = computed(() => {
    if (!currentPath.value) return []
    return currentPath.value.split('/').filter(Boolean)
})

function showToast(message, type = 'success') {
    toast.value = { message, type }
    setTimeout(() => { toast.value = null }, 3000)
}

function authHeaders() {
    const token = getToken()
    return token ? { 'Authorization': `Bearer ${token}` } : {}
}

async function refresh() {
    await loadFiles(currentPath.value)
}

async function loadFiles(path) {
    loading.value = true
    try {
        const pathParam = path ? `&path=${encodeURIComponent(path)}` : ''
        const res = await fetch(`${API_BASE}/api/files/list?t=${Date.now()}${pathParam}`, {
            headers: { ...authHeaders() }
        })
        if (!res.ok) throw new Error('加载失败')
        const data = await res.json()
        items.value = data.items
        currentPath.value = path
    } catch (e) {
        showToast(e.message || '加载失败', 'error')
    } finally {
        loading.value = false
    }
}

function navigateTo(path) {
    loadFiles(path)
}

function selectItem(item) {
    selectedPath.value = item.path === selectedPath.value ? '' : item.path
}

function openItem(item) {
    if (item.is_dir) {
        loadFiles(item.path)
    } else {
        downloadItem(item)
    }
}

async function downloadItem(item) {
    try {
        const res = await fetch(`${API_BASE}/api/files/download?path=${encodeURIComponent(item.path)}`, {
            headers: { ...authHeaders() }
        })
        if (!res.ok) throw new Error('下载失败')
        const blob = await res.blob()
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = item.name
        a.click()
        URL.revokeObjectURL(url)
    } catch (e) {
        showToast(e.message || '下载失败', 'error')
    }
}

async function handleUpload(e) {
    const files = e.target.files
    if (!files.length) return
    await uploadFiles(files)
    e.target.value = ''
}

async function handleDrop(e) {
    const files = e.dataTransfer.files
    if (!files.length) return
    await uploadFiles(files)
}

async function uploadFiles(files) {
    uploading.value = true
    uploadProgress.value = 0
    try {
        const pathParam = currentPath.value ? `&path=${encodeURIComponent(currentPath.value)}` : ''

        for (let i = 0; i < files.length; i++) {
            const formData = new FormData()
            formData.append('file', files[i])

            const res = await fetch(`${API_BASE}/api/files/upload?t=${Date.now()}${pathParam}`, {
                method: 'POST',
                headers: { ...authHeaders() },
                body: formData,
            })
            if (!res.ok) {
                const err = await res.json()
                throw new Error(err.detail || `上传 ${files[i].name} 失败`)
            }
            uploadProgress.value = Math.round(((i + 1) / files.length) * 100)
        }
        showToast(`成功上传 ${files.length} 个文件`)
        await loadFiles(currentPath.value)
        showUpload.value = false
    } catch (e) {
        showToast(e.message || '上传失败', 'error')
    } finally {
        uploading.value = false
    }
}

async function createDirectory() {
    if (!newDirName.value.trim()) return
    try {
        const pathParam = currentPath.value ? `&path=${encodeURIComponent(currentPath.value)}` : ''
        const res = await fetch(`${API_BASE}/api/files/mkdir?t=${Date.now()}${pathParam}&name=${encodeURIComponent(newDirName.value.trim())}`, {
            method: 'POST',
            headers: { ...authHeaders() },
        })
        if (!res.ok) throw new Error('创建失败')
        showToast('目录创建成功')
        showMkdir.value = false
        newDirName.value = ''
        await loadFiles(currentPath.value)
    } catch (e) {
        showToast(e.message || '创建失败', 'error')
    }
}

async function deleteItem(item) {
    if (!confirm(`确定删除 "${item.name}" 吗？`)) return
    try {
        const res = await fetch(`${API_BASE}/api/files/delete?t=${Date.now()}&path=${encodeURIComponent(item.path)}`, {
            method: 'DELETE',
            headers: { ...authHeaders() },
        })
        if (!res.ok) throw new Error('删除失败')
        showToast('删除成功')
        await loadFiles(currentPath.value)
    } catch (e) {
        showToast(e.message || '删除失败', 'error')
    }
}

async function renameItem(item) {
    const newName = prompt('请输入新名称：', item.name)
    if (!newName || newName === item.name) return
    try {
        const res = await fetch(`${API_BASE}/api/files/rename?t=${Date.now()}&path=${encodeURIComponent(item.path)}&new_name=${encodeURIComponent(newName)}`, {
            method: 'POST',
            headers: { ...authHeaders() },
        })
        if (!res.ok) throw new Error('重命名失败')
        showToast('重命名成功')
        await loadFiles(currentPath.value)
    } catch (e) {
        showToast(e.message || '重命名失败', 'error')
    }
}

function formatDate(dateStr) {
    if (!dateStr) return ''
    const d = new Date(dateStr)
    return `${d.getMonth() + 1}/${d.getDate()} ${d.getHours()}:${String(d.getMinutes()).padStart(2, '0')}`
}

onMounted(() => {
    loadFiles('')
})
</script>

<style scoped>
.file-manager {
    padding: 32px;
    max-width: 1000px;
    margin: 0 auto;
}

.page-header {
    margin-bottom: 24px;
}

.page-header h1 {
    font-size: 24px;
    font-weight: 700;
    color: #fff;
    display: flex;
    align-items: center;
    gap: 10px;
}

.page-header h1 i {
    color: var(--theme);
}

.page-header p {
    color: rgba(255, 255, 255, 0.4);
    font-size: 14px;
    margin-top: 4px;
}

/* 工具栏 */
.toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 16px;
    padding: 12px 16px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 12px;
}

.breadcrumb {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 2px;
    font-size: 13px;
    flex: 1;
    min-width: 0;
}

.breadcrumb-item {
    color: rgba(255, 255, 255, 0.4);
    cursor: pointer;
    padding: 2px 4px;
    border-radius: 4px;
    transition: color 0.15s;
}

.breadcrumb-item:hover {
    color: var(--theme);
}

.breadcrumb-item.active {
    color: rgba(255, 255, 255, 0.7);
}

.breadcrumb-sep {
    color: rgba(255, 255, 255, 0.15);
    margin: 0 2px;
}

.toolbar-actions {
    display: flex;
    gap: 6px;
}

/* 上传区域 */
.upload-area {
    margin-bottom: 12px;
}

.upload-dropzone {
    border: 2px dashed rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    color: rgba(255, 255, 255, 0.3);
}

.upload-dropzone:hover {
    border-color: var(--theme);
    background: rgba(0, 242, 192, 0.03);
    color: var(--theme);
}

.upload-dropzone i {
    font-size: 28px;
    display: block;
    margin-bottom: 8px;
}

.upload-progress {
    margin-top: 8px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.4);
}

.progress-bar {
    height: 4px;
    background: rgba(255, 255, 255, 0.06);
    border-radius: 2px;
    margin-top: 4px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: var(--theme);
    border-radius: 2px;
    transition: width 0.3s;
}

/* 新建目录 */
.mkdir-area {
    display: flex;
    gap: 8px;
    margin-bottom: 12px;
    padding: 12px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 10px;
}

.mkdir-area .form-input {
    flex: 1;
}

/* 文件列表 */
.file-list {
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 12px;
    overflow: hidden;
}

.file-list-loading,
.file-list-empty {
    text-align: center;
    padding: 40px;
    color: rgba(255, 255, 255, 0.3);
}

.file-list-loading i {
    margin-right: 8px;
}

.file-list-empty i {
    font-size: 32px;
    display: block;
    margin-bottom: 8px;
}

.file-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 16px;
    cursor: pointer;
    transition: background 0.15s;
    font-size: 13px;
}

.file-item:hover {
    background: rgba(255, 255, 255, 0.03);
}

.file-item.selected {
    background: rgba(0, 242, 192, 0.04);
}

.file-item+.file-item {
    border-top: 1px solid rgba(255, 255, 255, 0.02);
}

.file-icon {
    width: 24px;
    text-align: center;
    font-size: 16px;
    flex-shrink: 0;
}

.file-name {
    flex: 1;
    color: rgba(255, 255, 255, 0.7);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.file-size {
    width: 70px;
    text-align: right;
    color: rgba(255, 255, 255, 0.3);
    font-size: 12px;
    flex-shrink: 0;
}

.file-date {
    width: 90px;
    text-align: right;
    color: rgba(255, 255, 255, 0.2);
    font-size: 12px;
    flex-shrink: 0;
}

.file-actions {
    display: none;
    gap: 4px;
    flex-shrink: 0;
}

.file-item:hover .file-actions {
    display: flex;
}

.btn-icon {
    width: 28px;
    height: 28px;
    border-radius: 6px;
    border: none;
    background: transparent;
    color: rgba(255, 255, 255, 0.3);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.15s;
    font-size: 12px;
}

.btn-icon:hover {
    background: rgba(255, 255, 255, 0.06);
    color: rgba(255, 255, 255, 0.7);
}

.btn-icon-danger:hover {
    background: rgba(255, 107, 107, 0.1);
    color: #ff6b6b;
}

/* 通用 */
.form-input {
    padding: 8px 12px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.04);
    color: rgba(255, 255, 255, 0.7);
    font-size: 13px;
    font-family: inherit;
    outline: none;
}

.form-input:focus {
    border-color: var(--theme);
}

.btn {
    padding: 8px 16px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.04);
    color: rgba(255, 255, 255, 0.7);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 6px;
    font-family: inherit;
}

.btn:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.08);
    color: #fff;
}

.btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

.btn-primary {
    background: rgba(0, 242, 192, 0.1);
    border-color: rgba(0, 242, 192, 0.2);
    color: var(--theme);
}

.btn-primary:hover:not(:disabled) {
    background: rgba(0, 242, 192, 0.18);
}

.btn-sm {
    padding: 6px 12px;
    font-size: 12px;
}

/* Toast */
.toast {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    padding: 10px 20px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 500;
    z-index: 9999;
    animation: toastIn 0.3s ease;
}

.toast.success {
    background: rgba(0, 242, 192, 0.12);
    color: var(--theme);
    border: 1px solid rgba(0, 242, 192, 0.2);
}

.toast.error {
    background: rgba(255, 107, 107, 0.12);
    color: #ff6b6b;
    border: 1px solid rgba(255, 107, 107, 0.2);
}

@keyframes toastIn {
    from {
        opacity: 0;
        transform: translateX(-50%) translateY(-10px);
    }

    to {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }
}
</style>
