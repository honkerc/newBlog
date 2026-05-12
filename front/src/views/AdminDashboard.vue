<template>
    <div class="admin-dashboard">
        <div class="page-header">
            <h2>概览</h2>
            <p class="page-desc">博客数据总览</p>
        </div>

        <!-- 统计卡片 -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-newspaper"></i></div>
                <div class="stat-info">
                    <span class="stat-value">{{ stats.posts }}</span>
                    <span class="stat-label">文章</span>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-camera"></i></div>
                <div class="stat-info">
                    <span class="stat-value">{{ stats.moments }}</span>
                    <span class="stat-label">动态</span>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-comment"></i></div>
                <div class="stat-info">
                    <span class="stat-value">{{ stats.comments }}</span>
                    <span class="stat-label">评论</span>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fas fa-heart"></i></div>
                <div class="stat-info">
                    <span class="stat-value">{{ stats.likes }}</span>
                    <span class="stat-label">总点赞</span>
                </div>
            </div>
        </div>

        <!-- 热力图 -->
        <div class="dashboard-section">
            <h3>活动热力图</h3>
            <HeatmapWidget />
        </div>

        <!-- 快捷操作 -->
        <div class="quick-actions">
            <h3>快捷操作</h3>
            <div class="actions-grid">
                <router-link to="/admin/editor" class="action-card">
                    <i class="fas fa-pen"></i>
                    <span>写文章</span>
                </router-link>
                <router-link to="/admin/moments" class="action-card">
                    <i class="fas fa-camera"></i>
                    <span>发动态</span>
                </router-link>
                <router-link to="/admin/profile" class="action-card">
                    <i class="fas fa-user-gear"></i>
                    <span>编辑资料</span>
                </router-link>
                <router-link to="/admin/settings" class="action-card">
                    <i class="fas fa-cog"></i>
                    <span>账号设置</span>
                </router-link>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/utils/api'
import HeatmapWidget from '@/components/HeatmapWidget.vue'

const stats = ref({
    posts: 0,
    moments: 0,
    comments: 0,
    likes: 0,
})

onMounted(async () => {
    try {
        const res = await adminApi.getStats()
        if (res) {
            stats.value = {
                posts: res.post_count || 0,
                moments: res.moment_count || 0,
                comments: res.comment_count || 0,
                likes: res.total_likes || 0,
            }
        }
    } catch (e) {
        console.error('加载统计数据失败:', e)
    }
})
</script>

<style scoped>
.admin-dashboard {
    max-width: 800px;
    margin: 0 auto;
}

.page-header {
    margin-bottom: 32px;
}

.page-header h2 {
    font-size: 24px;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.3px;
}

.page-desc {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.3);
    margin-top: 6px;
}

/* ===== 统计卡片 ===== */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 40px;
}

.stat-card {
    background: rgba(11, 14, 20, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 18px;
    padding: 24px;
    display: flex;
    align-items: center;
    gap: 16px;
    transition: all 0.25s ease;
}

.stat-card:hover {
    background: rgba(11, 14, 20, 0.5);
    border-color: rgba(0, 242, 192, 0.2);
    transform: translateY(-2px);
}

.stat-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: rgba(0, 242, 192, 0.12);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    color: #00F2C0;
    flex-shrink: 0;
}

.stat-info {
    display: flex;
    flex-direction: column;
}

.stat-value {
    font-size: 24px;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1;
}

.stat-label {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.3);
    margin-top: 4px;
}

/* ===== 区块 ===== */
.dashboard-section {
    margin-bottom: 40px;
}

.dashboard-section h3 {
    font-size: 17px;
    font-weight: 600;
    color: #FFFFFF;
    margin-bottom: 16px;
}

/* ===== 快捷操作 ===== */
.quick-actions h3 {
    font-size: 17px;
    font-weight: 600;
    color: #FFFFFF;
    margin-bottom: 16px;
}

.actions-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}

.action-card {
    background: rgba(11, 14, 20, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 18px;
    padding: 28px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    text-decoration: none;
    transition: all 0.25s ease;
}

.action-card:hover {
    background: rgba(11, 14, 20, 0.5);
    border-color: rgba(0, 242, 192, 0.2);
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.action-card i {
    font-size: 28px;
    color: #00F2C0;
}

.action-card span {
    font-size: 14px;
    font-weight: 500;
    color: #EFF3F8;
}

/* ===== 响应式 ===== */
@media (max-width: 700px) {
    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .actions-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 400px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }

    .actions-grid {
        grid-template-columns: 1fr;
    }
}
</style>
