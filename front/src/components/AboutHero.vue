<template>
    <section class="about-hero-section">
        <div class="about-hero-inner">
            <div class="about-hero-left">
                <div class="about-avatar-frame">
                    <img v-if="profile.avatar" :src="resolveImageUrl(profile.avatar)" alt="avatar" />
                    <div v-else class="about-avatar-placeholder">
                        <i class="fas fa-user"></i>
                    </div>
                </div>
                <div class="about-avatar-info">
                    <h1 class="about-name">{{ profile.nickname || 'Clay' }}</h1>
                    <p class="about-tagline">{{ profile.bio || '高敏天赋者 · 终身学习者 · 重构自我中' }}</p>
                    <div class="about-social-links" v-if="hasSocialLinks">
                        <a v-if="profile.github" :href="profile.github" target="_blank" class="about-social-btn"><i
                                class="fab fa-github"></i></a>
                        <a v-if="profile.twitter" :href="profile.twitter" target="_blank" class="about-social-btn"><i
                                class="fab fa-twitter"></i></a>
                        <a v-if="profile.codepen" :href="profile.codepen" target="_blank" class="about-social-btn"><i
                                class="fab fa-codepen"></i></a>
                    </div>
                </div>
            </div>

            <div class="about-hero-divider"></div>

            <div class="about-hero-right">
                <div class="about-lyrics-card">
                    <div class="about-lyrics-line" v-for="(line, i) in lyrics" :key="i"
                        :class="{ active: activeLyric === i }" @click="selectLyric(i)">
                        <span class="about-lyric-text">{{ line.text }}</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { publicApi, resolveImageUrl } from '@/utils/api'

const STORAGE_KEY = 'about_selected_lyric'

// 从 localStorage 恢复上次选中的歌词，默认 0
const savedIndex = parseInt(localStorage.getItem(STORAGE_KEY)) || 0
const activeLyric = ref(savedIndex >= 0 && savedIndex < 8 ? savedIndex : 0)

// 点击歌词时保存到 localStorage
function selectLyric(index) {
    activeLyric.value = index
    localStorage.setItem(STORAGE_KEY, index)
}

const profile = reactive({
    avatar: '',
    nickname: '',
    bio: '',
    github: '',
    twitter: '',
    codepen: '',
})

const hasSocialLinks = computed(() => {
    return profile.github || profile.twitter || profile.codepen
})

const lyrics = [
    { text: '痴迷学习和成长' },
    { text: '实力大于名声' },
    { text: '无休止的朝着心中所爱' },
    { text: '不断的自我革新' },
    { text: '以求更接近自己的目标' },
    { text: '一个人最核心的能力' },
    { text: '不是外在的技巧或资源' },
    { text: '而是内在系统的持续进化' },
]

onMounted(async () => {
    try {
        const res = await publicApi.getProfile()
        if (res) {
            profile.avatar = res.avatar || ''
            profile.nickname = res.nickname || ''
            profile.bio = res.bio || ''
            profile.github = res.github || ''
            profile.twitter = res.twitter || ''
            profile.codepen = res.codepen || ''
        }
    } catch (e) {
        console.error('加载用户信息失败:', e)
    }
})
</script>

<style scoped>
.about-hero-section {
    display: flex;
    justify-content: center;
    padding: 40px 0 36px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    margin-bottom: 24px;
}

.about-hero-inner {
    display: flex;
    gap: 48px;
    align-items: center;
    justify-content: center;
    width: 100%;
}

.about-hero-left {
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 220px;
}

.about-avatar-frame {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid rgba(0, 242, 192, 0.35);
    box-shadow: 0 0 32px rgba(0, 242, 192, 0.12), 0 8px 32px rgba(0, 0, 0, 0.25);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    background: rgba(255, 255, 255, 0.03);
}

.about-avatar-frame:hover {
    transform: scale(1.02);
    box-shadow: 0 0 48px rgba(0, 242, 192, 0.2), 0 8px 40px rgba(0, 0, 0, 0.35);
}

.about-avatar-frame img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.about-avatar-placeholder {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 48px;
    color: rgba(255, 255, 255, 0.1);
}

.about-avatar-info {
    text-align: center;
    margin-top: 16px;
}

.about-name {
    font-size: 26px;
    font-weight: 800;
    background: linear-gradient(135deg, #FFFFFF, #A6FFE0);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    letter-spacing: -0.5px;
    margin: 0;
}

.about-tagline {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.4);
    margin: 6px 0 14px;
}

.about-social-links {
    display: flex;
    gap: 10px;
    justify-content: center;
}

.about-social-btn {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255, 255, 255, 0.3);
    font-size: 14px;
    text-decoration: none;
    transition: all 0.2s ease;
}

.about-social-btn:hover {
    background: rgba(0, 242, 192, 0.12);
    border-color: rgba(0, 242, 192, 0.35);
    color: #00F2C0;
    transform: translateY(-2px);
}

.about-hero-divider {
    width: 1px;
    height: 220px;
    background: linear-gradient(to bottom, transparent, rgba(255, 255, 255, 0.12), transparent);
    flex-shrink: 0;
}

.about-hero-right {
    flex: 1;
    min-width: 0;
    max-width: 420px;
}

.about-lyrics-card {
    padding: 0;
}

.about-lyrics-line {
    padding: 7px 18px;
    border-radius: 8px;
    transition: all 0.35s ease;
    color: rgba(255, 255, 255, 0.2);
    cursor: pointer;
}

.about-lyrics-line.active {
    color: #fff;
}

.about-lyrics-line:not(.active):hover {
    color: rgba(255, 255, 255, 0.5);
}

.about-lyric-text {
    font-size: 16px;
    letter-spacing: 0.6px;
    transition: color 0.3s ease;
}

.about-lyrics-line.active .about-lyric-text {
    font-weight: 500;
}

@media (max-width: 640px) {
    .about-hero-inner {
        flex-direction: column;
        gap: 24px;
    }

    .about-hero-divider {
        width: 80%;
        height: 1px;
        background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.1), transparent);
    }

    .about-hero-left {
        width: 100%;
    }

    .about-avatar-frame {
        width: 120px;
        height: 120px;
    }

    .about-hero-right {
        max-width: 100%;
        text-align: center;
    }
}
</style>
