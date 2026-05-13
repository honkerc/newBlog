<template>
    <div class="page">
        <div class="page-header">
            <div class="header-top">
                <div class="header-title-group">
                    <h1>今日</h1>
                    <p class="header-desc">{{ dateStr }}</p>
                </div>
                <div class="header-icon">
                    <i class="fas fa-calendar-day"></i>
                </div>
            </div>
        </div>

        <!-- 加载中 -->
        <div class="loading" v-if="!todayData">
            <i class="fas fa-spinner fa-spin"></i>
            <span>加载中...</span>
        </div>

        <!-- 空状态 -->
        <div class="empty-state"
            v-if="todayData && !todayData.checkins.length && !todayData.mottos.length && !todayData.posts.length">
            <i class="fas fa-inbox"></i>
            <p>今天还没有记录</p>
        </div>

        <!-- 打卡 -->
        <div class="section" v-if="todayData && todayData.checkins.length">
            <div class="section-header">
                <div class="section-label">
                    <i class="fas fa-check-circle"></i>
                    <span>打卡</span>
                </div>
                <span class="section-count">{{ todayData.checkins.length }} 条</span>
            </div>
            <div class="card" v-for="item in todayData.checkins" :key="'c' + item.id">
                <div class="card-left">
                    <div class="card-icon" :class="item.category">
                        <i :class="getCatIcon(item.category)"></i>
                    </div>
                </div>
                <div class="card-body">
                    <div class="card-text">{{ item.content }}</div>
                </div>
                <div class="card-actions">
                    <button class="action-btn like-btn" :class="{ liked: item.liked }" @click="toggleLike(item)"
                        title="点赞">
                        <i class="far fa-heart"></i>
                        <span v-if="item.like_count">{{ item.like_count }}</span>
                    </button>
                    <button class="action-btn danger" @click="delCheckIn(item.id)" title="删除">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
            </div>
        </div>

        <!-- 一句话 -->
        <div class="section" v-if="todayData && todayData.mottos.length">
            <div class="section-header">
                <div class="section-label">
                    <i class="fas fa-quote-right"></i>
                    <span>一言</span>
                </div>
                <span class="section-count">{{ todayData.mottos.length }} 条</span>
            </div>
            <div class="card" v-for="item in todayData.mottos" :key="'m' + item.id">
                <div class="card-left">
                    <div class="card-icon motto-icon">
                        <i class="fas fa-quote-right"></i>
                    </div>
                </div>
                <div class="card-body">
                    <div class="card-text motto-text">"{{ item.content }}"</div>
                </div>
                <div class="card-actions">
                    <button class="action-btn danger" @click="delMotto(item.id)" title="删除">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
            </div>
        </div>

        <!-- 日精进 / 读书笔记 -->
        <div class="section" v-if="todayData && todayData.posts.length">
            <div class="section-header">
                <div class="section-label">
                    <i class="fas fa-file-alt"></i>
                    <span>精进 / 读书</span>
                </div>
                <span class="section-count">{{ todayData.posts.length }} 条</span>
            </div>
            <div class="card" v-for="item in todayData.posts" :key="'p' + item.id">
                <div class="card-left">
                    <div class="card-icon post-icon">
                        <i class="fas fa-file-lines"></i>
                    </div>
                </div>
                <div class="card-body">
                    <div class="card-title">{{ item.title }}</div>
                    <div class="card-text" v-if="item.content">{{ item.content.substring(0, 60) }}{{
                        item.content.length > 60 ? '...' : '' }}</div>
                </div>
                <div class="card-actions">
                    <button class="action-btn danger" @click="delPost(item.id)" title="删除">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
            </div>
        </div>

        <!-- Toast -->
        <div class="toast success" v-if="toastMsg">{{ toastMsg }}</div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/utils/api'

const todayData = ref(null)
const toastMsg = ref('')

const now = new Date()
const dateStr = now.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' })

const catIcons = {
    moment: 'fas fa-camera',
    sports: 'fas fa-running',
    daily: 'fas fa-sun',
    study: 'fas fa-graduation-cap',
}

function getCatLabel(val) {
    const map = { moment: '朋友圈', sports: '运动', daily: '日常', study: '学习' }
    return map[val] || val
}

function getCatIcon(val) {
    return catIcons[val] || 'fas fa-check'
}

async function loadData() {
    try {
        todayData.value = await api.getTodaySummary()
    } catch (e) {
        console.error('加载今日记录失败:', e)
    }
}

onMounted(loadData)

async function delCheckIn(id) {
    try {
        await api.deleteCheckIn(id)
        todayData.value.checkins = todayData.value.checkins.filter(i => i.id !== id)
        toastMsg.value = '已删除 🗑️'
        setTimeout(() => toastMsg.value = '', 2000)
    } catch (e) {
        toastMsg.value = '删除失败: ' + e.message
        setTimeout(() => toastMsg.value = '', 3000)
    }
}

async function delMotto(id) {
    try {
        await api.deleteMotto(id)
        todayData.value.mottos = todayData.value.mottos.filter(i => i.id !== id)
        toastMsg.value = '已删除 🗑️'
        setTimeout(() => toastMsg.value = '', 2000)
    } catch (e) {
        toastMsg.value = '删除失败: ' + e.message
        setTimeout(() => toastMsg.value = '', 3000)
    }
}

async function delPost(id) {
    try {
        await api.deletePost(id)
        todayData.value.posts = todayData.value.posts.filter(i => i.id !== id)
        toastMsg.value = '已删除 🗑️'
        setTimeout(() => toastMsg.value = '', 2000)
    } catch (e) {
        toastMsg.value = '删除失败: ' + e.message
        setTimeout(() => toastMsg.value = '', 3000)
    }
}

async function toggleLike(item) {
    try {
        const res = await api.toggleLike(item.id)
        item.liked = res.liked
        item.like_count = res.like_count
    } catch (e) {
        console.error('点赞失败:', e)
    }
}
</script>

<style scoped>
.page {
    padding-top: 4px;
}

/* ===== 页头 ===== */
.page-header {
    padding: 20px 0 24px;
    text-align: left;
}

.header-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.header-title-group h1 {
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.3px;
}

.header-desc {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.3);
    margin-top: 2px;
}

.header-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: rgba(var(--theme-rgb), 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    color: var(--accent);
}

/* ===== 加载 ===== */
.loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    padding: 60px 0;
    color: var(--text-dim);
    font-size: 14px;
}

.loading i {
    font-size: 24px;
}

/* ===== 空状态 ===== */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    padding: 60px 0;
    color: var(--text-dim);
}

.empty-state i {
    font-size: 36px;
    opacity: 0.3;
}

.empty-state p {
    font-size: 14px;
}

/* ===== 区块 ===== */
.section {
    margin-bottom: 24px;
}

.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
    padding: 0 2px;
}

.section-label {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 6px;
}

.section-label i {
    font-size: 12px;
    color: var(--accent);
}

.section-count {
    font-size: 11px;
    color: var(--text-dim);
    font-family: 'JetBrains Mono', monospace;
}

/* ===== 卡片（admin 风格） ===== */
.card {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 14px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.04);
    transition: all 0.2s ease;
    margin-bottom: 6px;
}

.card:last-child {
    margin-bottom: 0;
}

.card:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.08);
}

/* ===== 左侧图标 ===== */
.card-left {
    flex-shrink: 0;
}

.card-icon {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
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
    background: rgba(255, 217, 61, 0.12);
    color: #FFD93D;
}

.card-icon.daily {
    background: rgba(0, 242, 192, 0.12);
    color: #00F2C0;
}

.card-icon.motto-icon {
    background: rgba(0, 242, 192, 0.1);
    color: #00F2C0;
}

.card-icon.post-icon {
    background: rgba(162, 155, 254, 0.12);
    color: #a29bfe;
}

/* ===== 中间内容 ===== */
.card-body {
    flex: 1;
    min-width: 0;
}

.card-title {
    font-size: 13px;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 2px;
}

.card-text {
    font-size: 13px;
    color: var(--text-tertiary);
    line-height: 1.5;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.card-text.motto-text {
    font-style: italic;
    color: var(--text-secondary);
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
    color: rgba(255, 255, 255, 0.12);
    font-size: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    cursor: pointer;
    opacity: 0;
}

.card:hover .action-btn {
    opacity: 1;
}

.action-btn.danger:hover {
    background: rgba(255, 107, 107, 0.1);
    color: #ff6b6b;
}

.action-btn.like-btn {
    width: auto;
    padding: 0 6px;
    gap: 3px;
    font-size: 12px;
}

.action-btn.like-btn.liked {
    color: #ff6b6b;
    opacity: 1;
}

.action-btn.like-btn.liked i {
    font-weight: 900;
}

.action-btn.like-btn:hover {
    color: #ff6b6b;
    opacity: 1;
}
</style>
