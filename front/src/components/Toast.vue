<template>
    <Teleport to="body">
        <div class="toast-container">
            <TransitionGroup name="toast">
                <div v-for="t in toasts" :key="t.id" class="toast-item" :class="t.type">
                    <i v-if="t.type === 'success'" class="fas fa-check-circle"></i>
                    <i v-else-if="t.type === 'error'" class="fas fa-exclamation-circle"></i>
                    <i v-else class="fas fa-info-circle"></i>
                    <span>{{ t.message }}</span>
                </div>
            </TransitionGroup>
        </div>
    </Teleport>
</template>

<script setup>
import { ref, provide } from 'vue'

const TOAST_KEY = Symbol('toast')

const toasts = ref([])
let id = 0

function toast(message, type = 'info', duration = 2500) {
    const tid = ++id
    toasts.value.push({ id: tid, message, type })
    setTimeout(() => {
        toasts.value = toasts.value.filter(t => t.id !== tid)
    }, duration)
}

provide(TOAST_KEY, toast)

defineExpose({ toast })
</script>

<style scoped>
.toast-container {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 99999;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    pointer-events: none;
}

.toast-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 500;
    backdrop-filter: blur(16px);
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
    pointer-events: auto;
    white-space: nowrap;
}

.toast-item.info {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.8);
}

.toast-item.success {
    background: rgba(0, 242, 192, 0.1);
    border: 1px solid rgba(0, 242, 192, 0.15);
    color: #00F2C0;
}

.toast-item.error {
    background: rgba(255, 107, 107, 0.1);
    border: 1px solid rgba(255, 107, 107, 0.15);
    color: #ff6b6b;
}

.toast-item i {
    font-size: 15px;
}

/* ===== 动画 ===== */
.toast-enter-active {
    transition: all 0.25s ease;
}

.toast-leave-active {
    transition: all 0.2s ease;
}

.toast-enter-from {
    opacity: 0;
    transform: translateY(-12px) scale(0.95);
}

.toast-leave-to {
    opacity: 0;
    transform: translateY(-8px) scale(0.95);
}
</style>
