<template>
    <div class="admin-profile">
        <div class="page-header">
            <div class="header-left">
                <h2>个人设置</h2>
                <span class="header-desc">管理你的个人资料、站点信息和账号安全</span>
            </div>
        </div>

        <!-- ===== 板块一：个人资料（头像 + 信息整合） ===== -->
        <div class="settings-card profile-card">
            <div class="card-glow"></div>
            <div class="card-body">
                <!-- 左侧头像 + 右侧资料 横向布局 -->
                <div class="profile-layout">
                    <!-- 左侧：固定方正的图片上传区 -->
                    <div class="profile-avatar">
                        <div class="avatar-frame">
                            <ImageUploader v-model="form.avatar" />
                        </div>
                    </div>

                    <!-- 右侧：资料表单 -->
                    <div class="profile-info">
                        <div class="form-row">
                            <div class="form-group">
                                <label><i class="fas fa-user"></i> 昵称</label>
                                <input type="text" v-model="form.nickname" placeholder="你的昵称" class="form-input" />
                            </div>
                            <div class="form-group">
                                <label><i class="fas fa-envelope"></i> 邮箱</label>
                                <input type="email" v-model="form.email" placeholder="your@email.com"
                                    class="form-input" />
                            </div>
                        </div>
                        <div class="form-group">
                            <label><i class="fas fa-quote-right"></i> 简介</label>
                            <textarea v-model="form.bio" placeholder="一句话介绍自己..." rows="2"
                                class="form-textarea"></textarea>
                        </div>
                    </div>
                </div>

                <!-- 分隔线 -->
                <div class="section-divider"></div>

                <!-- 社交链接 -->
                <div class="social-section">
                    <label class="social-label"><i class="fas fa-link"></i> 社交链接</label>
                    <div class="social-grid">
                        <div class="social-item">
                            <div class="social-icon github">
                                <i class="fab fa-github"></i>
                            </div>
                            <input type="text" v-model="form.github" placeholder="GitHub 链接" class="form-input" />
                        </div>
                        <div class="social-item">
                            <div class="social-icon twitter">
                                <i class="fab fa-twitter"></i>
                            </div>
                            <input type="text" v-model="form.twitter" placeholder="Twitter 链接" class="form-input" />
                        </div>
                        <div class="social-item">
                            <div class="social-icon codepen">
                                <i class="fab fa-codepen"></i>
                            </div>
                            <input type="text" v-model="form.codepen" placeholder="CodePen 链接" class="form-input" />
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ===== 板块二：站点设置 ===== -->
        <div class="settings-card">
            <div class="card-glow"></div>
            <div class="card-body">
                <h3 class="section-title"><i class="fas fa-globe"></i> 站点设置</h3>
                <div class="form-group">
                    <label>站点名称</label>
                    <input type="text" v-model="form.site_name" placeholder="魂牵梦绕" class="form-input" />
                </div>
                <div class="form-group">
                    <label>站点描述</label>
                    <textarea v-model="form.site_description" placeholder="个人博客" rows="2"
                        class="form-textarea"></textarea>
                </div>
            </div>
        </div>

        <!-- ===== 板块三：修改密码 ===== -->
        <div class="settings-card">
            <div class="card-glow"></div>
            <div class="card-body">
                <h3 class="section-title"><i class="fas fa-lock"></i> 修改密码</h3>
                <div class="form-group">
                    <label>当前密码</label>
                    <input type="password" v-model="passwordForm.old_password" placeholder="输入当前密码"
                        class="form-input" />
                </div>
                <div class="form-group">
                    <label>新密码</label>
                    <input type="password" v-model="passwordForm.new_password" placeholder="输入新密码" class="form-input" />
                </div>
                <div class="form-group">
                    <label>确认新密码</label>
                    <input type="password" v-model="passwordForm.confirm_password" placeholder="再次输入新密码"
                        class="form-input" />
                </div>
                <button class="btn-save btn-password" @click="handleChangePassword" :disabled="changingPassword">
                    <i class="fas fa-check"></i>
                    <span>{{ changingPassword ? '修改中...' : '修改密码' }}</span>
                </button>
            </div>
        </div>

        <!-- ===== 保存按钮 ===== -->
        <div class="save-bar">
            <button class="btn-save btn-primary" @click="handleSave" :disabled="saving">
                <i class="fas fa-check"></i>
                <span>{{ saving ? '保存中...' : '保存全部' }}</span>
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { adminApi } from '@/utils/api'
import { useToast } from '@/utils/toast'
import ImageUploader from '@/components/ImageUploader.vue'

const { toast } = useToast()
const saving = ref(false)
const changingPassword = ref(false)

const form = reactive({
    avatar: '',
    nickname: '',
    bio: '',
    email: '',
    github: '',
    twitter: '',
    codepen: '',
    site_name: '',
    site_description: '',
})

const passwordForm = reactive({
    old_password: '',
    new_password: '',
    confirm_password: '',
})

onMounted(async () => {
    try {
        const res = await adminApi.getProfile()
        if (res) {
            form.avatar = res.avatar || ''
            form.nickname = res.nickname || ''
            form.bio = res.bio || ''
            form.email = res.email || ''
            form.github = res.github || ''
            form.twitter = res.twitter || ''
            form.codepen = res.codepen || ''
            form.site_name = res.site_name || '魂牵梦绕'
            form.site_description = res.site_description || '个人博客'
        }
    } catch (e) {
        console.error('加载个人资料失败:', e)
    }
})

async function handleSave() {
    saving.value = true
    try {
        await adminApi.updateProfile({
            avatar: form.avatar,
            nickname: form.nickname,
            bio: form.bio,
            email: form.email,
            github: form.github,
            twitter: form.twitter,
            codepen: form.codepen,
            site_name: form.site_name,
            site_description: form.site_description,
        })
        toast('个人资料已更新', 'success')
    } catch (e) {
        toast('保存失败: ' + e.message, 'error')
    } finally {
        saving.value = false
    }
}

async function handleChangePassword() {
    const { old_password, new_password, confirm_password } = passwordForm

    if (!old_password || !new_password || !confirm_password) {
        toast('请填写所有密码字段', 'error')
        return
    }
    if (new_password !== confirm_password) {
        toast('两次输入的新密码不一致', 'error')
        return
    }
    if (new_password.length < 6) {
        toast('新密码至少 6 位', 'error')
        return
    }

    changingPassword.value = true
    try {
        await adminApi.changePassword({
            old_password,
            new_password,
        })
        toast('密码修改成功', 'success')
        passwordForm.old_password = ''
        passwordForm.new_password = ''
        passwordForm.confirm_password = ''
    } catch (e) {
        toast('修改失败: ' + e.message, 'error')
    } finally {
        changingPassword.value = false
    }
}
</script>

<style scoped>
.admin-profile {
    max-width: 780px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 24px;
}

/* ===== 页头 ===== */
.page-header {
    margin-bottom: 4px;
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

.card-body {
    position: relative;
    padding: 32px 36px;
    display: flex;
    flex-direction: column;
    gap: 22px;
}

/* ===== 分区标题 ===== */
.section-title {
    font-size: 16px;
    font-weight: 600;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 0;
}

.section-title i {
    color: #00F2C0;
    font-size: 16px;
}

/* =============================================
   个人资料卡片（头像 + 信息整合）
   ============================================= */

/* --- 左侧头像 + 右侧资料 横向布局 --- */
.profile-layout {
    display: flex;
    align-items: stretch;
    gap: 32px;
}

/* --- 左侧：固定方正头像 --- */
.profile-avatar {
    flex-shrink: 0;
    display: flex;
    align-items: center;
}

.avatar-frame {
    width: 140px;
    height: 140px;
    border-radius: 16px;
    overflow: hidden;
    border: 2px dashed rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.02);
    transition: all 0.2s ease;
    cursor: pointer;
    position: relative;
}

.avatar-frame:hover {
    border-color: rgba(0, 242, 192, 0.3);
    background: rgba(255, 255, 255, 0.04);
}

.avatar-frame .image-uploader {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
}

.avatar-frame .upload-area {
    width: 100% !important;
    height: 100% !important;
    min-height: 140px !important;
    max-height: 140px !important;
    border: none !important;
    border-radius: 0 !important;
    background: transparent !important;
    display: flex;
    align-items: center;
    justify-content: center;
}

.avatar-frame .upload-area.has-image {
    border: none !important;
    border-radius: 0 !important;
}

.avatar-frame .preview {
    width: 100% !important;
    height: 100% !important;
    max-height: 140px !important;
    min-height: 140px !important;
    aspect-ratio: unset !important;
    border-radius: 0 !important;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}

.avatar-frame .preview img {
    width: 100% !important;
    height: auto !important;
    min-height: 140px !important;
    object-fit: cover;
    border-radius: 0 !important;
    display: block;
    flex-shrink: 0;
}

.avatar-frame .placeholder {
    width: 100%;
    height: 100%;
    padding: 0;
    border-radius: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
}

.avatar-frame .placeholder i {
    font-size: 32px;
    color: rgba(255, 255, 255, 0.15);
}

.avatar-frame .placeholder span {
    display: block;
    font-size: 11px;
    color: rgba(255, 255, 255, 0.12);
}

.avatar-frame .placeholder .hint {
    display: none;
}

.avatar-frame .preview-overlay {
    border-radius: 0;
}

/* --- 右侧资料表单 --- */
.profile-info {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 14px;
    justify-content: center;
}

/* --- 分隔线 --- */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, rgba(255, 255, 255, 0.04), rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04));
    margin: 2px 0;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}

/* ===== 表单 ===== */
.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-group label {
    font-size: 13px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.45);
    letter-spacing: 0.3px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.form-group label i {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.2);
}

.form-input,
.form-textarea {
    padding: 10px 14px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    background: rgba(255, 255, 255, 0.03);
    color: #EFF3F8;
    font-size: 14px;
    font-family: inherit;
    outline: none;
    transition: all 0.2s ease;
}

.form-input:focus,
.form-textarea:focus {
    border-color: rgba(0, 242, 192, 0.2);
    background: rgba(255, 255, 255, 0.05);
}

.form-input::placeholder,
.form-textarea::placeholder {
    color: rgba(255, 255, 255, 0.15);
}

.form-textarea {
    resize: vertical;
    min-height: 60px;
    line-height: 1.6;
}

/* ===== 社交链接 ===== */
.social-section {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding-top: 4px;
}

.social-label {
    font-size: 13px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.45);
    letter-spacing: 0.3px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.social-label i {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.2);
}

.social-grid {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.social-item {
    display: flex;
    align-items: center;
    gap: 10px;
}

.social-icon {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 17px;
    flex-shrink: 0;
    transition: all 0.25s ease;
    position: relative;
}

.social-icon.github {
    background: linear-gradient(135deg, rgba(110, 84, 148, 0.2), rgba(110, 84, 148, 0.1));
    color: #b088e0;
    border: 1px solid rgba(110, 84, 148, 0.15);
}

.social-icon.github:hover {
    background: linear-gradient(135deg, rgba(110, 84, 148, 0.35), rgba(110, 84, 148, 0.2));
    border-color: rgba(110, 84, 148, 0.3);
    transform: translateY(-1px);
}

.social-icon.twitter {
    background: linear-gradient(135deg, rgba(29, 161, 242, 0.2), rgba(29, 161, 242, 0.1));
    color: #5fc3ff;
    border: 1px solid rgba(29, 161, 242, 0.15);
}

.social-icon.twitter:hover {
    background: linear-gradient(135deg, rgba(29, 161, 242, 0.35), rgba(29, 161, 242, 0.2));
    border-color: rgba(29, 161, 242, 0.3);
    transform: translateY(-1px);
}

.social-icon.codepen {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.03));
    color: #cccccc;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.social-icon.codepen:hover {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.08));
    border-color: rgba(255, 255, 255, 0.15);
    transform: translateY(-1px);
}

.social-item .form-input {
    flex: 1;
}

/* ===== 保存栏 ===== */
.save-bar {
    display: flex;
    justify-content: flex-end;
    padding-top: 4px;
}

.btn-save {
    padding: 8px 24px;
    border-radius: 8px;
    border: none;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    font-family: inherit;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.btn-save i {
    font-size: 12px;
}

.btn-primary {
    background: rgba(0, 242, 192, 0.1);
    color: #00F2C0;
}

.btn-primary:hover:not(:disabled) {
    background: rgba(0, 242, 192, 0.18);
}

.btn-primary:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

.btn-password {
    align-self: flex-start;
    background: rgba(0, 242, 192, 0.1);
    color: #00F2C0;
}

.btn-password:hover:not(:disabled) {
    background: rgba(0, 242, 192, 0.18);
}

.btn-password:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

/* ===== 响应式 ===== */
@media (max-width: 600px) {
    .card-body {
        padding: 20px;
    }

    .profile-layout {
        flex-direction: column;
        align-items: center;
    }

    .profile-avatar {
        margin-top: 0;
    }

    .profile-info {
        width: 100%;
    }

    .form-row {
        grid-template-columns: 1fr;
    }
}
</style>
