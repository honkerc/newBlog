<template>
    <div class="about-page">
        <!-- ===== 第一部分：头像 + 歌词 ===== -->
        <section class="hero-section">
            <div class="hero-inner">
                <div class="hero-left">
                    <div class="avatar-frame">
                        <img src="https://picsum.photos/id/64/300/300" alt="avatar" />
                    </div>
                    <div class="avatar-info">
                        <h1 class="name">Clay</h1>
                        <p class="tagline">高敏天赋者 · 终身学习者 · 寻找自我中</p>
                        <div class="social-links">
                            <a href="#" class="social-btn"><i class="fab fa-github"></i></a>
                            <a href="#" class="social-btn"><i class="fab fa-twitter"></i></a>
                            <a href="#" class="social-btn"><i class="fab fa-codepen"></i></a>
                            <a href="#" class="social-btn"><i class="fas fa-envelope"></i></a>
                        </div>
                    </div>
                </div>

                <div class="hero-divider"></div>

                <div class="hero-right">
                    <div class="lyrics-card">
                        <div class="lyrics-line" v-for="(line, i) in lyrics" :key="i"
                            :class="{ active: activeLyric === i }" @click="activeLyric = i">
                            <span class="lyric-text">{{ line.text }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ===== 第二部分：更多简介 ===== -->
        <section class="bio-section">
            <div class="bio-grid">
                <div class="bio-card">
                    <div class="bio-icon"><i class="fas fa-code"></i></div>
                    <h3>技术栈</h3>
                    <p>Vue · React · Node.js · Python · TypeScript · Tailwind · Docker</p>
                </div>
                <div class="bio-card">
                    <div class="bio-icon"><i class="fas fa-paint-brush"></i></div>
                    <h3>设计</h3>
                    <p>UI/UX 设计 · 玻璃拟态 · 深色主题 · 响应式布局 · Figma</p>
                </div>
                <div class="bio-card">
                    <div class="bio-icon"><i class="fas fa-music"></i></div>
                    <h3>爱好</h3>
                    <p>独立音乐 · 摄影 · 写作 · 咖啡 · 旅行 · 科幻小说</p>
                </div>
                <div class="bio-card">
                    <div class="bio-icon"><i class="fas fa-graduation-cap"></i></div>
                    <h3>经历</h3>
                    <p>5 年全栈开发 · 3 年开源贡献 · 前大厂工程师 · 现独立创作者</p>
                </div>
            </div>

            <div class="timeline">
                <h2 class="section-label">📅 时间线</h2>
                <div class="timeline-item" v-for="(item, i) in timeline" :key="i">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <span class="timeline-year">{{ item.year }}</span>
                        <h4>{{ item.title }}</h4>
                        <p>{{ item.desc }}</p>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const activeLyric = ref(0)

const lyrics = [

    { text: '无休止的朝着心中所爱' },
    { text: '不断的自我革新' },
    { text: '以求更接近自己的目标' },
    // { text: '从构思到实现' },
    // { text: '每一次重构都是成长' },
    // { text: '不止于代码' },
    // { text: '更关于创造与分享' },
]

const timeline = [
    { year: '2021', title: '毕业 · 加入大厂', desc: '计算机科学学士，入职某互联网公司前端团队' },
    { year: '2022', title: '开源贡献', desc: '开始参与 Vue 生态开源项目，累计 500+ PR' },
    { year: '2023', title: '独立创作', desc: '离开大厂，成为独立开发者，开始做自己的产品' },
    { year: '2024', title: '汽水平台', desc: '创立汽水平台，探索设计与技术的边界' },
    { year: '2025', title: '持续进化', desc: '不断学习，持续输出，做有意义的产品' },
]
</script>

<style scoped>
.about-page {
    max-width: 1000px;
    margin: 0 auto;
    padding: 0 20px 60px;
}

/* ===== Hero 区域 ===== */
.hero-section {
    display: flex;
    justify-content: center;
    padding: 60px 0 56px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.hero-inner {
    display: flex;
    gap: 56px;
    align-items: center;
    justify-content: center;
}

.hero-left {
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 240px;
}

.avatar-frame {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid rgba(0, 242, 192, 0.4);
    box-shadow: 0 0 40px rgba(0, 242, 192, 0.15), 0 8px 40px rgba(0, 0, 0, 0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.avatar-frame:hover {
    transform: scale(1.02);
    box-shadow: 0 0 56px rgba(0, 242, 192, 0.25), 0 8px 48px rgba(0, 0, 0, 0.4);
}

.avatar-frame img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar-info {
    text-align: center;
    margin-top: 20px;
}

.name {
    font-size: 30px;
    font-weight: 800;
    background: linear-gradient(135deg, #FFFFFF, #A6FFE0);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    letter-spacing: -0.5px;
}

.tagline {
    font-size: 14px;
    color: #CBD5F0;
    margin-top: 6px;
    opacity: 0.85;
}

.social-links {
    display: flex;
    gap: 12px;
    margin-top: 16px;
    justify-content: center;
}

.social-btn {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #CBD5F0;
    font-size: 16px;
    text-decoration: none;
    transition: all 0.2s ease;
}

.social-btn:hover {
    background: rgba(0, 242, 192, 0.15);
    border-color: rgba(0, 242, 192, 0.4);
    color: #00F2C0;
    transform: translateY(-2px);
}

/* ===== 分割线 ===== */
.hero-divider {
    width: 1px;
    height: 260px;
    background: linear-gradient(to bottom, transparent, rgba(255, 255, 255, 0.15), transparent);
    flex-shrink: 0;
}

/* ===== 歌词 ===== */
.hero-right {
    flex: 1;
    min-width: 0;
    max-width: 460px;
}

.lyrics-card {
    padding: 0;
}

.lyrics-line {
    padding: 8px 20px;
    border-radius: 10px;
    transition: all 0.4s ease;
    color: rgba(255, 255, 255, 0.3);
}

.lyrics-line.active {
    color: #FFFFFF;
}

.lyrics-line:not(.active):hover {
    color: rgba(255, 255, 255, 0.65);
}

.lyric-text {
    font-size: 17px;
    font-weight: 400;
    letter-spacing: 0.8px;
    transition: color 0.3s ease;
}

.lyrics-line.active .lyric-text {
    font-weight: 500;
}

/* ===== Bio 区域 ===== */
.bio-section {
    padding-top: 56px;
}

.bio-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
}

.bio-card {
    background: rgba(11, 14, 20, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    padding: 28px 32px;
    transition: all 0.25s ease;
    backdrop-filter: blur(8px);
}

.bio-card:hover {
    background: rgba(11, 14, 20, 0.6);
    border-color: rgba(0, 242, 192, 0.2);
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.bio-icon {
    width: 48px;
    height: 48px;
    border-radius: 16px;
    background: rgba(0, 242, 192, 0.12);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    color: #00F2C0;
    margin-bottom: 18px;
}

.bio-card h3 {
    font-size: 20px;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 10px;
}

.bio-card p {
    font-size: 14px;
    color: #CBD5F0;
    line-height: 1.7;
    opacity: 0.9;
}

/* ===== 时间线 ===== */
.timeline {
    margin-top: 56px;
}

.section-label {
    font-size: 22px;
    font-weight: 700;
    color: #00F2C0;
    margin-bottom: 28px;
}

.timeline-item {
    display: flex;
    gap: 24px;
    padding-bottom: 32px;
    position: relative;
    padding-left: 32px;
}

.timeline-item::before {
    content: '';
    position: absolute;
    left: 9px;
    top: 24px;
    bottom: 10px;
    width: 2px;
    background: linear-gradient(to bottom, #00F2C0, rgba(0, 242, 192, 0.1));
    border-radius: 2px;
}

.timeline-item:last-child::before {
    display: none;
}

.timeline-dot {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #0B0E14;
    border: 3px solid #00F2C0;
    flex-shrink: 0;
    margin-top: 3px;
    position: relative;
    z-index: 1;
    box-shadow: 0 0 0 5px rgba(0, 242, 192, 0.12), 0 0 20px rgba(0, 242, 192, 0.15);
    transition: all 0.3s ease;
}

.timeline-item:hover .timeline-dot {
    background: #00F2C0;
    box-shadow: 0 0 0 7px rgba(0, 242, 192, 0.2), 0 0 28px rgba(0, 242, 192, 0.3);
    transform: scale(1.1);
}

.timeline-content {
    flex: 1;
    background: rgba(11, 14, 20, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 18px;
    padding: 20px 24px;
    transition: all 0.25s ease;
}

.timeline-content:hover {
    background: rgba(11, 14, 20, 0.5);
    border-color: rgba(0, 242, 192, 0.15);
    transform: translateX(4px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.timeline-year {
    font-family: 'JetBrains Mono', 'Noto Sans Mono', monospace;
    font-size: 13px;
    color: #00F2C0;
    font-weight: 600;
    letter-spacing: 1px;
}

.timeline-content h4 {
    font-size: 17px;
    font-weight: 600;
    color: #FFFFFF;
    margin: 6px 0 8px;
}

.timeline-content p {
    font-size: 14px;
    color: #CBD5F0;
    opacity: 0.85;
    line-height: 1.6;
}

/* ===== 响应式 ===== */
@media (max-width: 800px) {
    .hero-section {
        padding: 40px 0 40px;
    }

    .hero-inner {
        flex-direction: column;
        gap: 28px;
    }

    .hero-divider {
        width: 80%;
        height: 1px;
        background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.12), transparent);
    }

    .hero-left {
        width: 100%;
    }

    .avatar-frame {
        width: 140px;
        height: 140px;
    }

    .hero-right {
        max-width: 100%;
    }

    .bio-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 500px) {
    .about-page {
        padding: 0 12px 40px;
    }

    .name {
        font-size: 24px;
    }

    .lyric-text {
        font-size: 15px;
    }
}
</style>
