<template>
    <div class="heatmap">
        <!-- 统计概览 - 只显示三个核心数据 -->
        <div class="heatmap-mvp">
            <div class="heatmap-mvp__item">
                <h5>{{ stats.days }}</h5>
                <span>DAYS</span>
            </div>
            <div class="heatmap-mvp__item">
                <h5>{{ stats.posts }}</h5>
                <span>POSTS</span>
            </div>
            <div class="heatmap-mvp__item">
                <h5>{{ stats.moments }}</h5>
                <span>MOMENTS</span>
            </div>
        </div>

        <!-- 热力图网格 - 多行显示 -->
        <div class="heatmap-map">
            <div v-for="(day, i) in heatmapDays" :key="i" class="heatmap-map__item tooltip" :data-date="day.date"
                :data-posts="day.posts" :data-moments="day.moments" :data-comments="day.comments">
                <div class="heatmap-map__item-block">
                    <div class="heatmap-map__item-inner" :class="getIntensityClass(day)"></div>
                </div>
            </div>
        </div>

        <!-- 图例 -->
        <div class="heatmap-legend">
            <span class="legend-label">少</span>
            <span class="legend-block low"></span>
            <span class="legend-block mid"></span>
            <span class="legend-block high"></span>
            <span class="legend-block peak"></span>
            <span class="legend-label">多</span>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { adminApi } from '@/utils/api'

const props = defineProps({
    days: { type: [Number, String], default: 60 },
})

const rawData = ref([])
const stats = ref({
    days: 0,
    posts: 0,
    moments: 0,
})

// 计算每天的总活动量，用于颜色强度
function getActivityScore(day) {
    return (day.posts || 0) + (day.moments || 0) + (day.comments || 0)
}

// 获取颜色强度 class
function getIntensityClass(day) {
    const score = getActivityScore(day)
    if (score === 0) return ''
    if (score <= 1) return 'low'
    if (score <= 3) return 'mid'
    if (score <= 6) return 'high'
    return 'peak'
}

// 生成最近 N 天的热力图数据
const heatmapDays = computed(() => {
    if (rawData.value.length) {
        return rawData.value.map(d => ({
            date: d.date,
            posts: d.posts || 0,
            moments: d.moments || 0,
            comments: d.comments || 0,
        }))
    }

    // 无数据时生成占位
    const days = []
    const now = new Date()
    for (let i = 59; i >= 0; i--) {
        const d = new Date(now)
        d.setDate(d.getDate() - i)
        const dateStr = d.toISOString().split('T')[0]
        days.push({
            date: dateStr,
            posts: 0,
            moments: 0,
            comments: 0,
        })
    }
    return days
})

onMounted(async () => {
    try {
        const res = await adminApi.getHeatmap(60)
        rawData.value = res.items || []
        if (res.stats) {
            stats.value = {
                days: res.stats.days ?? 0,
                posts: res.stats.posts ?? 0,
                moments: res.stats.moments ?? 0,
            }
        }
    } catch (e) {
        console.error('加载热力图数据失败:', e)
    }
})
</script>

<style scoped>
.heatmap {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 16px;
}

/* ===== 统计概览 ===== */
.heatmap-mvp {
    display: flex;
    justify-content: space-between;
    margin-bottom: 16px;
    padding-bottom: 14px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.heatmap-mvp__item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1px;
}

.heatmap-mvp__item h5 {
    font-size: 16px;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0;
    letter-spacing: -0.2px;
}

.heatmap-mvp__item span {
    font-size: 9px;
    color: rgba(255, 255, 255, 0.3);
    letter-spacing: 0.5px;
    font-weight: 500;
}

/* ===== 热力图网格 - 多行 ===== */
.heatmap-map {
    display: flex;
    flex-wrap: wrap;
    gap: 3px;
}

.heatmap-map__item {
    position: relative;
}

.heatmap-map__item-block {
    width: 10px;
    height: 10px;
    border-radius: 2px;
    background: rgba(255, 255, 255, 0.04);
    overflow: hidden;
}

.heatmap-map__item-inner {
    width: 100%;
    height: 100%;
    border-radius: 2px;
    transition: all 0.2s ease;
}

/* 颜色强度 */
.heatmap-map__item-inner.low {
    background: rgba(0, 242, 192, 0.15);
}

.heatmap-map__item-inner.mid {
    background: rgba(0, 242, 192, 0.35);
}

.heatmap-map__item-inner.high {
    background: rgba(0, 242, 192, 0.55);
}

.heatmap-map__item-inner.peak {
    background: rgba(0, 242, 192, 0.85);
    box-shadow: 0 0 4px rgba(0, 242, 192, 0.3);
}

.heatmap-map__item:hover .heatmap-map__item-inner {
    transform: scale(1.4);
}

/* ===== 图例 ===== */
.heatmap-legend {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 4px;
    margin-top: 12px;
    padding-top: 10px;
    border-top: 1px solid rgba(255, 255, 255, 0.04);
}

.legend-label {
    font-size: 10px;
    color: rgba(255, 255, 255, 0.2);
    margin: 0 2px;
}

.legend-block {
    width: 10px;
    height: 10px;
    border-radius: 2px;
}

.legend-block.low {
    background: rgba(0, 242, 192, 0.15);
}

.legend-block.mid {
    background: rgba(0, 242, 192, 0.35);
}

.legend-block.high {
    background: rgba(0, 242, 192, 0.55);
}

.legend-block.peak {
    background: rgba(0, 242, 192, 0.85);
}

/* ===== Tooltip ===== */
.tooltip {
    position: relative;
}

.tooltip::after {
    content: attr(data-date) " 📝" attr(data-posts) " 📸" attr(data-moments) " 💬" attr(data-comments);
    position: absolute;
    bottom: calc(100% + 6px);
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0, 0, 0, 0.85);
    color: #FFFFFF;
    font-size: 11px;
    padding: 5px 9px;
    border-radius: 6px;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.15s ease;
    z-index: 10;
    text-align: center;
    line-height: 1.4;
    letter-spacing: 0.3px;
}

.tooltip:hover::after {
    opacity: 1;
}
</style>
