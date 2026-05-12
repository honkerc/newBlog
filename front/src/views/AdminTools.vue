<template>
    <div class="admin-tools">
        <div class="page-header">
            <h1><i class="fas fa-tools"></i> 管理工具</h1>
            <p>数据导入导出、系统维护</p>
        </div>

        <!-- 导入导出 -->
        <div class="tool-card">
            <div class="tool-card-header">
                <i class="fas fa-database"></i>
                <span>数据导入导出</span>
            </div>
            <div class="tool-card-body">
                <div class="tool-row">
                    <div class="tool-info">
                        <h3>导出数据</h3>
                        <p>导出所有数据（数据库 + 上传文件）为 ZIP 包</p>
                    </div>
                    <button class="btn btn-primary" @click="handleExport" :disabled="exporting">
                        <i class="fas fa-download"></i>
                        {{ exporting ? '导出中...' : '导出' }}
                    </button>
                </div>
                <div class="tool-divider"></div>
                <div class="tool-row">
                    <div class="tool-info">
                        <h3>导入数据</h3>
                        <p>上传 ZIP 包恢复数据（会覆盖现有数据！）</p>
                    </div>
                    <div class="import-area">
                        <input type="file" ref="importInput" accept=".zip" @change="handleImport"
                            style="display:none" />
                        <button class="btn btn-warning" @click="$refs.importInput.click()" :disabled="importing">
                            <i class="fas fa-upload"></i>
                            {{ importing ? '导入中...' : '导入' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- 未引用文件管理 -->
        <div class="tool-card">
            <div class="tool-card-header">
                <i class="fas fa-trash-alt"></i>
                <span>未引用文件管理</span>
            </div>
            <div class="tool-card-body">
                <div class="tool-row">
                    <div class="tool-info">
                        <h3>扫描未引用文件</h3>
                        <p>找出上传目录中未被任何文章、动态等引用的文件</p>
                    </div>
                    <button class="btn btn-primary" @click="scanOrphanFiles" :disabled="scanning">
                        <i class="fas fa-search"></i>
                        {{ scanning ? '扫描中...' : '扫描' }}
                    </button>
                </div>

                <!-- 扫描结果 -->
                <div v-if="orphanResult" class="orphan-result">
                    <div class="orphan-summary">
                        <span>找到 <strong>{{ orphanResult.count }}</strong> 个未引用文件</span>
                        <span>共 <strong>{{ orphanResult.total_size_display }}</strong></span>
                    </div>

                    <div v-if="orphanResult.files.length" class="orphan-actions">
                        <div class="orphan-action-row">
                            <input v-model="moveTargetDir" placeholder="目标目录名（如: unused）" class="form-input" />
                            <button class="btn btn-sm" @click="moveOrphanFiles" :disabled="!selectedOrphans.length">
                                <i class="fas fa-folder-open"></i> 移动到目录
                            </button>
                        </div>
                        <button class="btn btn-sm btn-danger" @click="deleteOrphanFiles"
                            :disabled="!selectedOrphans.length">
                            <i class="fas fa-trash"></i> 删除选中 ({{ selectedOrphans.length }})
                        </button>
                    </div>

                    <div class="orphan-list">
                        <label v-for="f in orphanResult.files" :key="f.filename" class="orphan-item"
                            :class="{ selected: selectedOrphans.includes(f.filename) }">
                            <input type="checkbox" :value="f.filename" v-model="selectedOrphans" />
                            <span class="orphan-icon">
                                <i v-if="f.is_thumb" class="fas fa-image" style="color:#888"></i>
                                <i v-else class="fas fa-file"></i>
                            </span>
                            <span class="orphan-name">{{ f.filename }}</span>
                            <span class="orphan-size">{{ f.size_display }}</span>
                            <span class="orphan-date">{{ formatDate(f.modified) }}</span>
                        </label>
                    </div>
                    <div v-if="!orphanResult.files.length" class="orphan-empty">
                        <i class="fas fa-check-circle"></i> 没有未引用的文件
                    </div>
                </div>
            </div>
        </div>

        <!-- Toast -->
        <div v-if="toast" class="toast" :class="toast.type">{{ toast.message }}</div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuth } from '@/stores/auth'

const { getToken } = useAuth()

// 使用与 api.js 相同的 API_BASE 逻辑
const isDev = window.location.port === '8080' || window.location.port === '3001'
const API_BASE = isDev ? `http://${window.location.hostname}:8000` : ''

const exporting = ref(false)
const importing = ref(false)
const scanning = ref(false)
const importInput = ref(null)
const toast = ref(null)

// 未引用文件
const orphanResult = ref(null)
const selectedOrphans = ref([])
const moveTargetDir = ref('unused')

function showToast(message, type = 'success') {
    toast.value = { message, type }
    setTimeout(() => { toast.value = null }, 3000)
}

function getHeaders() {
    return {
        'Authorization': `Bearer ${getToken()}`,
    }
}

// 导出
async function handleExport() {
    exporting.value = true
    try {
        const res = await fetch(`${API_BASE}/api/admin/export`, {
            headers: getHeaders(),
        })
        if (!res.ok) throw new Error('导出失败')

        const blob = await res.blob()
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `blog-export-${new Date().toISOString().slice(0, 10)}.zip`
        a.click()
        URL.revokeObjectURL(url)
        showToast('导出成功')
    } catch (e) {
        showToast(e.message || '导出失败', 'error')
    } finally {
        exporting.value = false
    }
}

// 导入
async function handleImport(e) {
    const file = e.target.files[0]
    if (!file) return

    if (!confirm('导入将覆盖现有数据，确定继续吗？')) {
        e.target.value = ''
        return
    }

    importing.value = true
    try {
        const formData = new FormData()
        formData.append('file', file)

        const res = await fetch(`${API_BASE}/api/admin/import`, {
            method: 'POST',
            headers: getHeaders(),
            body: formData,
        })
        if (!res.ok) {
            const err = await res.json()
            throw new Error(err.detail || '导入失败')
        }
        showToast('导入成功，建议重启服务')
    } catch (e) {
        showToast(e.message || '导入失败', 'error')
    } finally {
        importing.value = false
        e.target.value = ''
    }
}

// 扫描未引用文件
async function scanOrphanFiles() {
    scanning.value = true
    selectedOrphans.value = []
    try {
        const res = await fetch(`${API_BASE}/api/admin/orphan-files`, {
            headers: getHeaders(),
        })
        if (!res.ok) throw new Error('扫描失败')
        orphanResult.value = await res.json()
        showToast(`扫描完成，找到 ${orphanResult.value.count} 个未引用文件`)
    } catch (e) {
        showToast(e.message || '扫描失败', 'error')
    } finally {
        scanning.value = false
    }
}

// 移动未引用文件
async function moveOrphanFiles() {
    if (!selectedOrphans.value.length) return
    if (!moveTargetDir.value.trim()) {
        showToast('请输入目标目录名', 'error')
        return
    }

    try {
        const params = new URLSearchParams()
        params.append('target_dir', moveTargetDir.value.trim())
        selectedOrphans.value.forEach(f => params.append('filenames', f))

        const res = await fetch(`${API_BASE}/api/admin/orphan-files/move?${params}`, {
            method: 'POST',
            headers: getHeaders(),
        })
        if (!res.ok) throw new Error('移动失败')
        const result = await res.json()
        showToast(result.message)
        // 重新扫描
        await scanOrphanFiles()
    } catch (e) {
        showToast(e.message || '移动失败', 'error')
    }
}

// 删除未引用文件
async function deleteOrphanFiles() {
    if (!selectedOrphans.value.length) return
    if (!confirm(`确定删除选中的 ${selectedOrphans.value.length} 个文件吗？`)) return

    try {
        const params = new URLSearchParams()
        selectedOrphans.value.forEach(f => params.append('filenames', f))

        const res = await fetch(`${API_BASE}/api/admin/orphan-files/delete?${params}`, {
            method: 'POST',
            headers: getHeaders(),
        })
        if (!res.ok) throw new Error('删除失败')
        const result = await res.json()
        showToast(result.message)
        await scanOrphanFiles()
    } catch (e) {
        showToast(e.message || '删除失败', 'error')
    }
}

function formatDate(dateStr) {
    if (!dateStr) return ''
    const d = new Date(dateStr)
    return `${d.getMonth() + 1}/${d.getDate()} ${d.getHours()}:${String(d.getMinutes()).padStart(2, '0')}`
}
</script>

<style scoped>
.admin-tools {
    padding: 32px;
    max-width: 800px;
    margin: 0 auto;
}

.page-header {
    margin-bottom: 32px;
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

.tool-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 20px;
}

.tool-card-header {
    padding: 16px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    font-size: 15px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.7);
    display: flex;
    align-items: center;
    gap: 8px;
}

.tool-card-header i {
    color: var(--theme);
    font-size: 16px;
}

.tool-card-body {
    padding: 20px;
}

.tool-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
}

.tool-info h3 {
    font-size: 15px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: 4px;
}

.tool-info p {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.35);
}

.tool-divider {
    height: 1px;
    background: rgba(255, 255, 255, 0.04);
    margin: 16px 0;
}

.btn {
    padding: 10px 20px;
    border-radius: 10px;
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
    white-space: nowrap;
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

.btn-warning {
    background: rgba(255, 193, 7, 0.1);
    border-color: rgba(255, 193, 7, 0.2);
    color: #ffc107;
}

.btn-warning:hover:not(:disabled) {
    background: rgba(255, 193, 7, 0.18);
}

.btn-danger {
    background: rgba(255, 107, 107, 0.1);
    border-color: rgba(255, 107, 107, 0.2);
    color: #ff6b6b;
}

.btn-danger:hover:not(:disabled) {
    background: rgba(255, 107, 107, 0.18);
}

.btn-sm {
    padding: 8px 14px;
    font-size: 12px;
}

/* 未引用文件 */
.orphan-result {
    margin-top: 16px;
    border-top: 1px solid rgba(255, 255, 255, 0.04);
    padding-top: 16px;
}

.orphan-summary {
    display: flex;
    gap: 20px;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.5);
    margin-bottom: 12px;
}

.orphan-summary strong {
    color: rgba(255, 255, 255, 0.8);
}

.orphan-actions {
    display: flex;
    gap: 10px;
    align-items: center;
    margin-bottom: 12px;
    flex-wrap: wrap;
}

.orphan-action-row {
    display: flex;
    gap: 8px;
    align-items: center;
    flex: 1;
}

.form-input {
    padding: 8px 12px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.04);
    color: rgba(255, 255, 255, 0.7);
    font-size: 13px;
    font-family: inherit;
    outline: none;
    flex: 1;
    min-width: 120px;
}

.form-input:focus {
    border-color: var(--theme);
}

.orphan-list {
    max-height: 400px;
    overflow-y: auto;
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 10px;
}

.orphan-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 12px;
    cursor: pointer;
    transition: background 0.15s;
    font-size: 13px;
}

.orphan-item:hover {
    background: rgba(255, 255, 255, 0.03);
}

.orphan-item.selected {
    background: rgba(0, 242, 192, 0.04);
}

.orphan-item+.orphan-item {
    border-top: 1px solid rgba(255, 255, 255, 0.02);
}

.orphan-item input[type="checkbox"] {
    accent-color: var(--theme);
}

.orphan-icon {
    width: 20px;
    text-align: center;
    color: rgba(255, 255, 255, 0.3);
}

.orphan-name {
    flex: 1;
    color: rgba(255, 255, 255, 0.7);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.orphan-size {
    color: rgba(255, 255, 255, 0.3);
    font-size: 12px;
    width: 60px;
    text-align: right;
}

.orphan-date {
    color: rgba(255, 255, 255, 0.2);
    font-size: 12px;
    width: 80px;
    text-align: right;
}

.orphan-empty {
    text-align: center;
    padding: 24px;
    color: rgba(255, 255, 255, 0.3);
    font-size: 14px;
}

.orphan-empty i {
    font-size: 24px;
    color: var(--theme);
    margin-bottom: 8px;
    display: block;
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
