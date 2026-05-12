<template>
    <div class="image-uploader">
        <!-- 隐藏的文件输入 -->
        <input type="file" ref="fileInput" accept="image/*" @change="onFileSelect" style="display:none" />

        <!-- 上传区域 -->
        <div class="upload-area" @click="triggerUpload" @drop.prevent="onDrop" @dragover.prevent
            :class="{ dragging: isDragging, 'has-image': modelValue }">
            <!-- 已有图片预览 -->
            <div class="preview" v-if="modelValue">
                <img :src="imageUrl" alt="preview" @error="onImageError" />
                <div class="preview-overlay">
                    <button class="overlay-btn change" @click.stop="triggerUpload" title="更换图片">
                        <i class="fas fa-sync-alt"></i>
                    </button>
                    <button class="overlay-btn remove" @click.stop="$emit('update:modelValue', '')" title="移除">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
            <!-- 空状态 -->
            <div class="placeholder" v-else>
                <i class="fas fa-cloud-upload-alt"></i>
                <span>点击或拖拽上传图片</span>
                <span class="hint">支持 JPG / PNG / GIF</span>
            </div>
        </div>

        <!-- 上传进度 -->
        <div class="upload-progress" v-if="uploading">
            <div class="progress-bar">
                <div class="progress-fill" :style="{ width: progress + '%' }"></div>
            </div>
            <span class="progress-text">{{ progress }}%</span>
        </div>

        <!-- 错误提示 -->
        <div class="upload-error" v-if="error">{{ error }}</div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { adminApi, resolveImageUrl } from '@/utils/api'

const props = defineProps({
    modelValue: { type: String, default: '' },
})

const emit = defineEmits(['update:modelValue'])

const fileInput = ref(null)
const uploading = ref(false)
const progress = ref(0)
const error = ref('')
const isDragging = ref(false)

const imageUrl = computed(() => resolveImageUrl(props.modelValue))

function triggerUpload() {
    fileInput.value?.click()
}

function onDrop(e) {
    isDragging.value = false
    const file = e.dataTransfer.files[0]
    if (file) uploadFile(file)
}

function onFileSelect(e) {
    const file = e.target.files[0]
    if (file) uploadFile(file)
    // 重置 input 以便重复选择同一文件
    e.target.value = ''
}

function onImageError() {
    error.value = '图片加载失败'
}

async function uploadFile(file) {
    // 验证文件类型
    if (!file.type.startsWith('image/')) {
        error.value = '请选择图片文件'
        return
    }

    error.value = ''
    uploading.value = true
    progress.value = 0

    try {
        // 模拟进度
        const progressTimer = setInterval(() => {
            progress.value = Math.min(progress.value + 10, 90)
        }, 200)

        const result = await adminApi.uploadFile(file)

        clearInterval(progressTimer)
        progress.value = 100

        // 返回相对路径
        setTimeout(() => {
            emit('update:modelValue', result.url)
            uploading.value = false
            progress.value = 0
        }, 300)
    } catch (e) {
        error.value = '上传失败: ' + (e.message || '未知错误')
        uploading.value = false
        progress.value = 0
    }
}
</script>

<style scoped>
.image-uploader {
    width: 100%;
}

.upload-area {
    width: 100%;
    min-height: 120px;
    border-radius: 10px;
    border: 1px dashed rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.02);
    cursor: pointer;
    transition: all 0.2s ease;
    overflow: hidden;
    position: relative;
}

.upload-area:hover {
    border-color: rgba(0, 242, 192, 0.2);
    background: rgba(255, 255, 255, 0.04);
}

.upload-area.dragging {
    border-color: #00F2C0;
    background: rgba(0, 242, 192, 0.06);
}

.upload-area.has-image {
    border-style: solid;
    border-color: rgba(255, 255, 255, 0.06);
    min-height: auto;
}

/* ===== 预览 ===== */
.preview {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 9;
    max-height: 200px;
}

.preview img {
    width: 100%;
    /* height: 100%; */
    object-fit: cover;
    display: block;
}

.preview-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    opacity: 0;
    transition: opacity 0.2s ease;
}

.preview:hover .preview-overlay {
    opacity: 1;
}

.overlay-btn {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    border: none;
    background: rgba(255, 255, 255, 0.15);
    color: #FFFFFF;
    font-size: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
    backdrop-filter: blur(4px);
}

.overlay-btn:hover {
    background: rgba(255, 255, 255, 0.25);
}

.overlay-btn.remove:hover {
    background: rgba(255, 107, 107, 0.6);
}

/* ===== 空状态 ===== */
.placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 32px 20px;
    color: rgba(255, 255, 255, 0.15);
}

.placeholder i {
    font-size: 28px;
    margin-bottom: 4px;
}

.placeholder span {
    font-size: 13px;
}

.placeholder .hint {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.08);
}

/* ===== 进度条 ===== */
.upload-progress {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 8px;
}

.progress-bar {
    flex: 1;
    height: 4px;
    border-radius: 2px;
    background: rgba(255, 255, 255, 0.04);
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: #00F2C0;
    border-radius: 2px;
    transition: width 0.3s ease;
}

.progress-text {
    font-size: 11px;
    color: rgba(255, 255, 255, 0.2);
    min-width: 32px;
    text-align: right;
}

/* ===== 错误 ===== */
.upload-error {
    margin-top: 6px;
    font-size: 12px;
    color: #ff6b6b;
}
</style>
