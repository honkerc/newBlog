<template>
    <div class="multi-image-uploader">
        <!-- 隐藏的文件输入 -->
        <input type="file" ref="fileInput" accept="image/*" multiple @change="onFileSelect" style="display:none" />

        <!-- 图片列表 -->
        <div class="image-grid">
            <div class="image-item" v-for="(img, i) in imageList" :key="i">
                <img :src="resolveImageUrl(img)" alt="" />
                <div class="item-overlay">
                    <button class="overlay-btn remove" @click="removeImage(i)" title="移除">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>

            <!-- 添加按钮 -->
            <div class="add-btn" @click="triggerUpload" :class="{ uploading }">
                <i class="fas fa-plus"></i>
                <span>添加图片</span>
            </div>
        </div>

        <!-- 上传进度 -->
        <div class="upload-progress" v-if="uploading">
            <div class="progress-bar">
                <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
            </div>
            <span class="progress-text">{{ uploadProgress }}%</span>
        </div>

        <!-- 错误提示 -->
        <div class="upload-error" v-if="error">{{ error }}</div>
    </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { adminApi, resolveImageUrl } from '@/utils/api'

const props = defineProps({
    modelValue: { type: String, default: '' },
})

const emit = defineEmits(['update:modelValue'])

const fileInput = ref(null)
const uploading = ref(false)
const uploadProgress = ref(0)
const error = ref('')

const imageList = computed({
    get: () => props.modelValue ? props.modelValue.split(',').filter(Boolean).map(s => s.trim()) : [],
    set: (val) => emit('update:modelValue', val.join(',')),
})

function triggerUpload() {
    if (uploading.value) return
    fileInput.value?.click()
}

async function onFileSelect(e) {
    const files = Array.from(e.target.files)
    if (!files.length) return

    error.value = ''
    uploading.value = true
    uploadProgress.value = 0

    const total = files.length
    let completed = 0
    const newUrls = []

    try {
        for (const file of files) {
            if (!file.type.startsWith('image/')) {
                error.value = `"${file.name}" 不是图片文件，已跳过`
                continue
            }

            const result = await adminApi.uploadFile(file)
            newUrls.push(result.url)
            completed++
            uploadProgress.value = Math.round((completed / total) * 100)
        }

        // 合并到现有列表
        const current = [...imageList.value]
        current.push(...newUrls)
        imageList.value = current

        setTimeout(() => {
            uploading.value = false
            uploadProgress.value = 0
        }, 300)
    } catch (e) {
        error.value = '上传失败: ' + (e.message || '未知错误')
        uploading.value = false
        uploadProgress.value = 0
    }

    // 重置 input 以便重复选择
    e.target.value = ''
}

function removeImage(index) {
    const current = [...imageList.value]
    current.splice(index, 1)
    imageList.value = current
}
</script>

<style scoped>
.multi-image-uploader {
    width: 100%;
}

.image-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 8px;
}

.image-item {
    position: relative;
    aspect-ratio: 1;
    border-radius: 10px;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.image-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.item-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.2s ease;
}

.image-item:hover .item-overlay {
    opacity: 1;
}

.overlay-btn {
    width: 28px;
    height: 28px;
    border-radius: 6px;
    border: none;
    background: rgba(255, 255, 255, 0.2);
    color: #FFFFFF;
    font-size: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
    backdrop-filter: blur(4px);
}

.overlay-btn.remove:hover {
    background: rgba(255, 107, 107, 0.7);
}

.add-btn {
    aspect-ratio: 1;
    border-radius: 10px;
    border: 1px dashed rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.02);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
    cursor: pointer;
    transition: all 0.2s ease;
    color: rgba(255, 255, 255, 0.15);
}

.add-btn:hover {
    border-color: rgba(0, 242, 192, 0.3);
    background: rgba(0, 242, 192, 0.04);
    color: rgba(0, 242, 192, 0.5);
}

.add-btn.uploading {
    opacity: 0.4;
    cursor: not-allowed;
    pointer-events: none;
}

.add-btn i {
    font-size: 20px;
}

.add-btn span {
    font-size: 11px;
}

/* ===== 进度条 ===== */
.upload-progress {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 10px;
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
