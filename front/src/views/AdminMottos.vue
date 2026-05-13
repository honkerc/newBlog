<template>
    <div class="admin-mottos">
        <div class="page-header">
            <div class="header-left">
                <h2>一言管理</h2>
                <span class="header-count">{{ mottos.length }} 条</span>
            </div>
            <button class="create-btn" @click="openNew">
                <i class="fas fa-plus"></i> 新建语录
            </button>
        </div>

        <div class="loading-text" v-if="loading">加载中...</div>

        <div class="motto-list" v-else>
            <div class="motto-card" v-for="motto in mottos" :key="motto.id">
                <div class="card-left">
                    <div class="card-icon">
                        <i class="fas fa-quote-right"></i>
                    </div>
                </div>
                <div class="card-body">
                    <div class="card-content">"{{ motto.content }}"</div>
                    <div class="card-meta">
                        <span class="meta-item" v-if="motto.location"><i class="fas fa-location-dot"></i> {{
                            motto.location }}</span>
                        <span class="meta-item">{{ formatDate(motto.created_at) }}</span>
                        <span class="meta-status" :class="{ published: motto.is_published }">
                            {{ motto.is_published ? '已发布' : '草稿' }}
                        </span>
                    </div>
                </div>
                <div class="card-actions">
                    <button class="action-btn edit" @click="openEdit(motto)" title="编辑">
                        <i class="fas fa-pen"></i>
                    </button>
                    <button class="action-btn danger" @click="deleteMotto(motto.id)" title="删除">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>

            <div class="empty-text" v-if="!mottos.length">暂无语录</div>
        </div>

        <!-- 编辑弹窗 -->
        <div class="modal-overlay" v-if="editModal.visible" @click.self="closeEdit">
            <div class="modal-panel">
                <div class="modal-header">
                    <h3>{{ editModal.isNew ? '新建语录' : '编辑语录' }}</h3>
                    <button class="modal-close" @click="closeEdit"><i class="fas fa-times"></i></button>
                </div>
                <div class="modal-body">
                    <div class="form-group">
                        <label>内容 <span class="required">*</span></label>
                        <textarea v-model="editForm.content" placeholder="写一句触动你的话..." rows="3"
                            class="form-textarea"></textarea>
                    </div>
                    <div class="form-group">
                        <label>出处/地点</label>
                        <input type="text" v-model="editForm.location" placeholder="例如：罗曼·罗兰、咖啡馆..."
                            class="form-input" />
                    </div>
                    <div class="form-group">
                        <label class="checkbox-label">
                            <input type="checkbox" v-model="editForm.is_published" />
                            <span>已发布</span>
                        </label>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="modal-btn cancel" @click="closeEdit">取消</button>
                    <button class="modal-btn save" @click="saveEdit" :disabled="saving">
                        {{ saving ? '保存中...' : '保存' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { adminApi } from '@/utils/api'
import { useToast } from '@/utils/toast'

const { toast } = useToast()
const loading = ref(true)
const saving = ref(false)
const mottos = ref([])

const editModal = reactive({
    visible: false,
    isNew: false,
    editingId: null,
})

const editForm = reactive({
    content: '',
    location: '',
    is_published: true,
})

function formatDate(dateStr) {
    if (!dateStr) return ''
    const d = new Date(dateStr)
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return `${y}.${m}.${day}`
}

function openNew() {
    editModal.visible = true
    editModal.isNew = true
    editModal.editingId = null
    editForm.content = ''
    editForm.location = ''
    editForm.is_published = true
}

function openEdit(motto) {
    editModal.visible = true
    editModal.isNew = false
    editModal.editingId = motto.id
    editForm.content = motto.content || ''
    editForm.location = motto.location || ''
    editForm.is_published = motto.is_published !== false
}

function closeEdit() {
    editModal.visible = false
    editModal.editingId = null
    editForm.content = ''
    editForm.location = ''
    editForm.is_published = true
}

async function saveEdit() {
    if (!editForm.content.trim()) {
        toast('请输入语录内容', 'error')
        return
    }

    saving.value = true
    try {
        const data = {
            content: editForm.content.trim(),
            location: editForm.location.trim(),
            is_published: editForm.is_published,
        }

        if (editModal.editingId) {
            await adminApi.updateMotto(editModal.editingId, data)
            toast('语录已更新', 'success')
        } else {
            await adminApi.createMotto(data)
            toast('语录已创建', 'success')
        }

        const res = await adminApi.getMottos({ page: 1, page_size: 100 })
        mottos.value = res.items || []
        closeEdit()
    } catch (e) {
        toast('保存失败: ' + e.message, 'error')
    } finally {
        saving.value = false
    }
}

async function deleteMotto(id) {
    try {
        await adminApi.deleteMotto(id)
        mottos.value = mottos.value.filter(m => m.id !== id)
        toast('语录已删除', 'success')
    } catch (e) {
        toast('删除失败: ' + e.message, 'error')
    }
}

onMounted(async () => {
    try {
        const res = await adminApi.getMottos({ page: 1, page_size: 100 })
        mottos.value = res.items || []
    } catch (e) {
        console.error('加载语录列表失败:', e)
    } finally {
        loading.value = false
    }
})
</script>

<style scoped>
.admin-mottos {
    max-width: 800px;
    margin: 0 auto;
}

.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 28px;
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
    margin: 0;
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
    padding: 8px 18px;
    border-radius: 8px;
    border: none;
    background: rgba(0, 242, 192, 0.1);
    color: #00F2C0;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: inherit;
}

.create-btn i {
    font-size: 12px;
}

.create-btn:hover {
    background: rgba(0, 242, 192, 0.18);
}

/* ===== 语录列表 ===== */
.motto-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.motto-card {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 14px 18px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 14px;
    border: 1px solid transparent;
    transition: all 0.2s ease;
}

.motto-card:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.06);
}

/* ===== 左侧图标 ===== */
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
    background: rgba(0, 242, 192, 0.1);
    color: #00F2C0;
    font-size: 18px;
}

/* ===== 中间内容 ===== */
.card-body {
    flex: 1;
    min-width: 0;
}

.card-content {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.6;
    font-style: italic;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-bottom: 4px;
}

.card-meta {
    display: flex;
    align-items: center;
    gap: 10px;
}

.meta-item {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.25);
}

.meta-item i {
    margin-right: 3px;
}

.meta-status {
    font-size: 10px;
    padding: 1px 8px;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.04);
    color: rgba(255, 255, 255, 0.2);
}

.meta-status.published {
    background: rgba(0, 242, 192, 0.1);
    color: #00F2C0;
}

/* ===== 操作按钮 ===== */
.card-actions {
    display: flex;
    gap: 4px;
    flex-shrink: 0;
}

.action-btn {
    width: 30px;
    height: 30px;
    border-radius: 8px;
    border: none;
    background: transparent;
    color: rgba(255, 255, 255, 0.15);
    font-size: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    cursor: pointer;
}

.action-btn.edit:hover {
    background: rgba(0, 242, 192, 0.1);
    color: #00F2C0;
}

.action-btn.danger:hover {
    background: rgba(255, 107, 107, 0.1);
    color: #ff6b6b;
}

/* ===== 编辑弹窗 ===== */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 20px;
}

.modal-panel {
    width: 100%;
    max-width: 520px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.5);
}

.modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 22px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

.modal-header h3 {
    font-size: 16px;
    font-weight: 600;
    color: #FFFFFF;
    margin: 0;
}

.modal-close {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    border: none;
    background: transparent;
    color: rgba(255, 255, 255, 0.2);
    font-size: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
}

.modal-close:hover {
    background: rgba(255, 255, 255, 0.04);
    color: rgba(255, 255, 255, 0.5);
}

.modal-body {
    padding: 22px;
    display: flex;
    flex-direction: column;
    gap: 16px;
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

.required {
    color: #ff5f56;
}

.form-input,
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
.form-textarea:focus {
    border-color: rgba(0, 242, 192, 0.2);
    background: rgba(255, 255, 255, 0.04);
}

.form-input::placeholder,
.form-textarea::placeholder {
    color: rgba(255, 255, 255, 0.15);
}

.form-textarea {
    resize: vertical;
    min-height: 80px;
    line-height: 1.6;
}

.checkbox-label {
    display: flex !important;
    flex-direction: row !important;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    font-size: 13px !important;
    color: rgba(255, 255, 255, 0.5) !important;
}

.checkbox-label input[type="checkbox"] {
    width: 16px;
    height: 16px;
    accent-color: #00F2C0;
    cursor: pointer;
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    padding: 16px 22px;
    border-top: 1px solid rgba(255, 255, 255, 0.04);
}

.modal-btn {
    padding: 8px 20px;
    border-radius: 8px;
    border: none;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: inherit;
}

.modal-btn.cancel {
    background: rgba(255, 255, 255, 0.04);
    color: rgba(255, 255, 255, 0.4);
}

.modal-btn.cancel:hover {
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.6);
}

.modal-btn.save {
    background: rgba(0, 242, 192, 0.1);
    color: #00F2C0;
}

.modal-btn.save:hover:not(:disabled) {
    background: rgba(0, 242, 192, 0.18);
}

.modal-btn.save:disabled {
    opacity: 0.4;
    cursor: not-allowed;
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
