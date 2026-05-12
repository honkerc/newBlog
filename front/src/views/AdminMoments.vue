<template>
    <div class="admin-moments">
        <div class="page-header">
            <div class="header-left">
                <h2>动态管理</h2>
                <span class="header-count">{{ items.length }} 条</span>
            </div>
            <div class="header-actions">
                <button class="create-btn" @click="openNew('moment')">
                    <i class="fas fa-camera"></i> 朋友圈
                </button>
                <button class="create-btn sports" @click="openNew('sports')">
                    <i class="fas fa-running"></i> 运动
                </button>
                <button class="create-btn daily" @click="openNew('daily')">
                    <i class="fas fa-sun"></i> 日常
                </button>
                <button class="create-btn study" @click="openNew('study')">
                    <i class="fas fa-graduation-cap"></i> 学习
                </button>
            </div>
        </div>

        <!-- 筛选栏 -->
        <div class="filter-bar">
            <button class="filter-btn" :class="{ active: activeCategory === '' }" @click="activeCategory = ''">
                <i class="fas fa-layer-group"></i> 全部
            </button>
            <button class="filter-btn" :class="{ active: activeCategory === 'moment' }"
                @click="activeCategory = 'moment'">
                <i class="fas fa-camera"></i> 朋友圈
            </button>
            <button class="filter-btn" :class="{ active: activeCategory === 'sports' }"
                @click="activeCategory = 'sports'">
                <i class="fas fa-running"></i> 运动
            </button>
            <button class="filter-btn" :class="{ active: activeCategory === 'daily' }"
                @click="activeCategory = 'daily'">
                <i class="fas fa-sun"></i> 日常
            </button>
            <button class="filter-btn" :class="{ active: activeCategory === 'study' }"
                @click="activeCategory = 'study'">
                <i class="fas fa-graduation-cap"></i> 学习
            </button>
        </div>

        <div class="loading-text" v-if="loading">加载中...</div>

        <div class="item-list" v-else>
            <div class="item-card" v-for="item in filteredItems" :key="item.id">
                <div class="card-left">
                    <div class="card-icon" :class="item.category">
                        <i :class="categoryIcon(item.category)"></i>
                    </div>
                </div>
                <div class="card-body">
                    <div class="card-top">
                        <span class="card-type" :class="item.category">
                            {{ categoryLabel(item.category) }}
                        </span>
                        <span class="card-date">{{ formatDate(item.created_at) }}</span>
                        <span class="card-status" v-if="!item.is_published">草稿</span>
                        <span class="card-status top" v-if="item.is_top">置顶</span>
                    </div>
                    <div class="card-content">{{ item.content }}</div>
                    <div class="card-meta" v-if="item.category === 'moment'">
                        <span><i class="far fa-heart"></i> {{ item.like_count || 0 }}</span>
                        <span v-if="item.images"><i class="fas fa-image"></i> 有图片</span>
                    </div>
                </div>
                <div class="card-actions">
                    <button class="action-btn edit" @click="openEdit(item)" title="编辑">
                        <i class="fas fa-pen"></i>
                    </button>
                    <button class="action-btn danger" @click="deleteItem(item)" title="删除">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>

            <div class="empty-text" v-if="!filteredItems.length">暂无内容</div>
        </div>

        <!-- 编辑弹窗 -->
        <div class="modal-overlay" v-if="editModal.visible" @click.self="closeEdit">
            <div class="modal-panel">
                <div class="modal-header">
                    <h3>{{ editModal.title }}</h3>
                    <button class="modal-close" @click="closeEdit"><i class="fas fa-times"></i></button>
                </div>
                <div class="modal-body">
                    <div class="form-group">
                        <label>类别</label>
                        <select v-model="editForm.category" class="form-input">
                            <option value="moment">朋友圈</option>
                            <option value="sports">运动</option>
                            <option value="daily">日常</option>
                            <option value="study">学习</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>内容</label>
                        <textarea v-model="editForm.content" placeholder="写点什么..." rows="6"
                            class="form-textarea"></textarea>
                    </div>
                    <div class="form-group">
                        <label>图片（可多选）</label>
                        <MultiImageUploader v-model="editForm.images" />
                    </div>
                    <div class="form-group">
                        <label class="checkbox-label">
                            <input type="checkbox" v-model="editForm.is_published" />
                            <span>已发布</span>
                        </label>
                    </div>
                    <div class="form-group">
                        <label class="checkbox-label">
                            <input type="checkbox" v-model="editForm.is_top" />
                            <span>置顶</span>
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
import { ref, reactive, computed, onMounted } from 'vue'
import { adminApi } from '@/utils/api'
import { useToast } from '@/utils/toast'
import MultiImageUploader from '@/components/MultiImageUploader.vue'

const { toast } = useToast()
const loading = ref(true)
const saving = ref(false)
const items = ref([])
const activeCategory = ref('')

const categoryLabels = {
    moment: '朋友圈',
    sports: '运动',
    daily: '日常',
    study: '学习',
}

const categoryIcons = {
    moment: 'fas fa-camera',
    sports: 'fas fa-running',
    daily: 'fas fa-sun',
    study: 'fas fa-graduation-cap',
}

function categoryLabel(cat) {
    return categoryLabels[cat] || cat
}

function categoryIcon(cat) {
    return categoryIcons[cat] || 'fas fa-check'
}

const filteredItems = computed(() => {
    if (!activeCategory.value) return items.value
    return items.value.filter(item => item.category === activeCategory.value)
})

const editModal = reactive({
    visible: false,
    title: '',
    editingId: null,
})

const editForm = reactive({
    category: 'moment',
    content: '',
    images: '',
    is_published: true,
    is_top: false,
})

function formatDate(dateStr) {
    if (!dateStr) return ''
    const d = new Date(dateStr)
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    const h = String(d.getHours()).padStart(2, '0')
    const min = String(d.getMinutes()).padStart(2, '0')
    return `${y}.${m}.${day} ${h}:${min}`
}

function openNew(category) {
    editModal.visible = true
    editModal.title = `新建${categoryLabel(category)}`
    editModal.editingId = null
    editForm.category = category
    editForm.content = ''
    editForm.images = ''
    editForm.is_published = true
    editForm.is_top = false
}

function openEdit(item) {
    editModal.visible = true
    editModal.title = '编辑动态'
    editModal.editingId = item.id
    editForm.category = item.category || 'moment'
    editForm.content = item.content || ''
    editForm.images = item.images || ''
    editForm.is_published = item.is_published !== false
    editForm.is_top = item.is_top || false
}

function closeEdit() {
    editModal.visible = false
    editModal.editingId = null
    editForm.category = 'moment'
    editForm.content = ''
    editForm.images = ''
    editForm.is_published = true
    editForm.is_top = false
}

async function saveEdit() {
    if (!editForm.content.trim()) {
        toast('请输入内容', 'error')
        return
    }

    saving.value = true
    try {
        const data = {
            category: editForm.category,
            content: editForm.content.trim(),
            images: editForm.images.trim(),
            is_published: editForm.is_published,
            is_top: editForm.is_top,
        }

        if (editModal.editingId) {
            await adminApi.updateMoment(editModal.editingId, data)
            toast('动态已更新', 'success')
        } else {
            await adminApi.createMoment(data)
            toast('动态已创建', 'success')
        }

        await loadData()
        closeEdit()
    } catch (e) {
        toast('保存失败: ' + e.message, 'error')
    } finally {
        saving.value = false
    }
}

async function deleteItem(item) {
    try {
        await adminApi.deleteMoment(item.id)
        toast('动态已删除', 'success')
        items.value = items.value.filter(i => i.id !== item.id)
    } catch (e) {
        toast('删除失败: ' + e.message, 'error')
    }
}

async function loadData() {
    try {
        const res = await adminApi.getMoments({ page: 1, page_size: 100 })
        items.value = res.items || []
    } catch (e) {
        console.error('加载数据失败:', e)
    } finally {
        loading.value = false
    }
}

onMounted(loadData)
</script>

<style scoped>
.admin-moments {
    max-width: 800px;
    margin: 0 auto;
}

.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    flex-wrap: wrap;
    gap: 12px;
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

.header-actions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
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

.create-btn.sports {
    background: rgba(255, 107, 107, 0.1);
    color: #ff6b6b;
}

.create-btn.sports:hover {
    background: rgba(255, 107, 107, 0.18);
}

.create-btn.study {
    background: rgba(162, 155, 254, 0.1);
    color: #a29bfe;
}

.create-btn.study:hover {
    background: rgba(162, 155, 254, 0.18);
}

.create-btn.daily {
    background: rgba(253, 203, 110, 0.1);
    color: #fdcb6e;
}

.create-btn.daily:hover {
    background: rgba(253, 203, 110, 0.18);
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
    align-items: center;
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

/* ===== 列表 ===== */
.item-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.item-card {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 14px 18px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 14px;
    border: 1px solid transparent;
    transition: all 0.2s ease;
}

.item-card:hover {
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
    font-size: 18px;
}

.card-icon.moment {
    background: rgba(0, 242, 192, 0.06);
    color: #00F2C0;
}

.card-icon.sports {
    background: rgba(255, 107, 107, 0.12);
    color: #ff6b6b;
}

.card-icon.study {
    background: rgba(255, 217, 61, 0.12);
    color: #FFD93D;
}

.card-icon.daily {
    background: rgba(0, 242, 192, 0.12);
    color: #00F2C0;
}

/* ===== 中间内容 ===== */
.card-body {
    flex: 1;
    min-width: 0;
}

.card-top {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 4px;
}

.card-type {
    font-size: 10px;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 500;
}

.card-type.moment {
    background: rgba(0, 242, 192, 0.1);
    color: #00F2C0;
}

.card-type.sports {
    background: rgba(255, 107, 107, 0.1);
    color: #ff6b6b;
}

.card-type.study {
    background: rgba(255, 217, 61, 0.1);
    color: #FFD93D;
}

.card-type.daily {
    background: rgba(0, 242, 192, 0.1);
    color: #00F2C0;
}

.card-date {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.2);
    font-family: 'JetBrains Mono', monospace;
}

.card-status {
    font-size: 10px;
    padding: 1px 6px;
    border-radius: 3px;
    background: rgba(255, 255, 255, 0.04);
    color: rgba(255, 255, 255, 0.2);
}

.card-status.top {
    background: rgba(255, 217, 61, 0.1);
    color: #FFD93D;
}

.card-content {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.7);
    line-height: 1.5;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.card-meta {
    display: flex;
    gap: 10px;
    margin-top: 4px;
    font-size: 11px;
    color: rgba(255, 255, 255, 0.25);
}

.card-meta i {
    margin-right: 3px;
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
    min-height: 120px;
    line-height: 1.6;
}

select.form-input {
    cursor: pointer;
    appearance: auto;
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
