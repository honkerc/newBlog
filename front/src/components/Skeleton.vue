<template>
    <div class="skeleton" :class="[type, size]" :style="customStyle">
        <div class="skeleton-shimmer"></div>
    </div>
</template>

<script setup>
const props = defineProps({
    type: {
        type: String,
        default: 'text',
        validator: v => ['text', 'title', 'avatar', 'image', 'card', 'circle', 'rect'].includes(v)
    },
    size: {
        type: String,
        default: 'md',
        validator: v => ['sm', 'md', 'lg', 'xl'].includes(v)
    },
    width: { type: String, default: '' },
    height: { type: String, default: '' },
    borderRadius: { type: String, default: '' },
})

const customStyle = {}
if (props.width) customStyle.width = props.width
if (props.height) customStyle.height = props.height
if (props.borderRadius) customStyle.borderRadius = props.borderRadius
</script>

<style scoped>
.skeleton {
    position: relative;
    background: rgba(255, 255, 255, 0.04);
    border-radius: 6px;
    overflow: hidden;
}

.skeleton-shimmer {
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg,
            transparent 0%,
            rgba(255, 255, 255, 0.04) 40%,
            rgba(255, 255, 255, 0.06) 50%,
            rgba(255, 255, 255, 0.04) 60%,
            transparent 100%);
    background-size: 200% 100%;
    animation: shimmer 1.8s ease-in-out infinite;
}

@keyframes shimmer {
    0% {
        background-position: 200% 0;
    }

    100% {
        background-position: -200% 0;
    }
}

/* ===== 类型 ===== */
.skeleton.text {
    height: 14px;
    border-radius: 4px;
}

.skeleton.title {
    height: 22px;
    border-radius: 5px;
}

.skeleton.avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
}

.skeleton.image {
    width: 100%;
    aspect-ratio: 16 / 10;
    border-radius: 10px;
}

.skeleton.card {
    width: 100%;
    height: 160px;
    border-radius: 14px;
}

.skeleton.circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
}

.skeleton.rect {
    border-radius: 8px;
}

/* ===== 尺寸 ===== */
.skeleton.sm {
    width: 60px;
}

.skeleton.md {
    width: 100%;
}

.skeleton.lg {
    width: 80%;
}

.skeleton.xl {
    width: 60%;
}
</style>
