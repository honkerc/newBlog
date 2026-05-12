<template>
    <div class="admin-settings">
        <div class="page-header">
            <div class="header-left">
                <h2>偏好设置</h2>
                <span class="header-desc">管理界面显示偏好</span>
            </div>
        </div>

        <div class="settings-card">
            <div class="card-glow"></div>
            <div class="settings-body">
                <div class="settings-section">
                    <h3 class="section-title"><i class="fas fa-palette"></i> 显示</h3>
                    <div class="setting-row">
                        <div class="setting-info">
                            <span class="setting-label">深色模式</span>
                            <span class="setting-desc">使用深色主题显示</span>
                        </div>
                        <label class="toggle-switch">
                            <input type="checkbox" v-model="darkMode" @change="toggleDarkMode" />
                            <span class="toggle-slider"></span>
                        </label>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const darkMode = ref(true)

function toggleDarkMode() {
    document.documentElement.classList.toggle('light-mode', !darkMode.value)
}
</script>

<style scoped>
.admin-settings {
    max-width: 780px;
    margin: 0 auto;
}

/* ===== 页头 ===== */
.page-header {
    margin-bottom: 24px;
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
}

.header-desc {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.2);
}

/* ===== 设置卡片 ===== */
.settings-card {
    position: relative;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 14px;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.settings-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.06), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.settings-card:hover {
    background: rgba(255, 255, 255, 0.04);
    border-color: rgba(255, 255, 255, 0.1);
}

.settings-card:hover::before {
    opacity: 1;
}

.card-glow {
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 50% 0%, rgba(0, 242, 192, 0.03), transparent 60%);
    opacity: 0;
    transition: opacity 0.4s ease;
    pointer-events: none;
}

.settings-card:hover .card-glow {
    opacity: 1;
}

.settings-body {
    position: relative;
    padding: 28px 32px;
    display: flex;
    flex-direction: column;
    gap: 28px;
}

/* ===== 分区 ===== */
.settings-section {
    display: flex;
    flex-direction: column;
    gap: 18px;
}

.section-title {
    font-size: 16px;
    font-weight: 600;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-title i {
    color: #00F2C0;
    font-size: 16px;
}

/* ===== 设置行 ===== */
.setting-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 0;
}

.setting-label {
    font-size: 14px;
    font-weight: 500;
    color: #EFF3F8;
    display: block;
}

.setting-desc {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.3);
    margin-top: 2px;
    display: block;
}

/* ===== Toggle Switch ===== */
.toggle-switch {
    position: relative;
    display: inline-block;
    width: 44px;
    height: 24px;
    flex-shrink: 0;
}

.toggle-switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.toggle-slider {
    position: absolute;
    cursor: pointer;
    inset: 0;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 24px;
    transition: all 0.3s ease;
}

.toggle-slider::before {
    content: '';
    position: absolute;
    width: 18px;
    height: 18px;
    left: 3px;
    bottom: 3px;
    background: #FFFFFF;
    border-radius: 50%;
    transition: all 0.3s ease;
}

.toggle-switch input:checked+.toggle-slider {
    background: #00F2C0;
}

.toggle-switch input:checked+.toggle-slider::before {
    transform: translateX(20px);
}

/* ===== 响应式 ===== */
@media (max-width: 600px) {
    .settings-body {
        padding: 20px;
    }
}
</style>
