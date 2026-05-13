<template>
  <div class="discover">
    <!-- 骨架屏 -->
    <div class="skeleton-home" v-if="loading">
      <div class="skeleton-hero">
        <Skeleton type="circle" width="64px" height="64px" borderRadius="50%" />
        <div class="skeleton-hero-info">
          <Skeleton type="title" width="180px" />
          <Skeleton type="text" width="260px" />
        </div>
      </div>
      <div class="skeleton-section">
        <Skeleton type="title" width="120px" height="18px" />
        <div class="skeleton-categories">
          <div v-for="n in 4" :key="n" class="skeleton-cat-item">
            <Skeleton type="circle" width="32px" height="32px" borderRadius="50%" />
            <Skeleton type="text" width="60px" height="12px" />
            <Skeleton type="text" width="40px" height="10px" />
          </div>
        </div>
      </div>
      <div class="skeleton-section">
        <Skeleton type="title" width="120px" height="18px" />
        <div class="skeleton-articles">
          <div v-for="n in 4" :key="n" class="skeleton-article-card">
            <Skeleton type="image" height="140px" />
            <div class="skeleton-article-body">
              <Skeleton type="title" />
              <Skeleton type="text" width="90%" />
              <Skeleton type="text" width="60%" />
            </div>
          </div>
        </div>
      </div>
      <div class="skeleton-section">
        <Skeleton type="title" width="120px" height="18px" />
        <div class="skeleton-moments">
          <div v-for="n in 3" :key="n" class="skeleton-moment-card">
            <Skeleton type="image" height="120px" />
            <Skeleton type="text" width="80%" />
            <Skeleton type="text" width="50%" height="10px" />
          </div>
        </div>
      </div>
    </div>

    <template v-if="!loading">

      <AboutHero />

      <!-- ===== 黑客打字机 ===== -->
      <div class="hacker-box">
        <div class="hacker-bar">
          <div class="hacker-dots">
            <span class="hacker-dot red"></span>
            <span class="hacker-dot yellow"></span>
            <span class="hacker-dot green"></span>
          </div>
        </div>
        <div class="hacker-content">
          <div class="hacker-line" v-for="(line, i) in typewriterLines" :key="i">
            <span class="hacker-prompt">$</span>
            <span class="hacker-text">{{ typewriterDisplay[i] }}<span class="hacker-cursor"
                v-if="typewriterCurrentLine === i && !typewriterDone">▌</span></span>
          </div>
        </div>
      </div>

      <!-- ===== 最新文章 ===== -->
      <div class="section-header">
        <h3 class="section-title"><i class="fas fa-newspaper"></i> 最新文章</h3>
        <router-link to="/articles" class="section-more">
          查看全部 <i class="fas fa-chevron-right"></i>
        </router-link>
      </div>
      <div class="mini-list" v-if="latestPosts.length">
        <router-link v-for="post in latestPosts" :key="post.id" :to="`/post/${post.id}`" class="mini-item">
          <div class="mini-dot"></div>
          <div class="mini-body">
            <span class="mini-title">{{ post.title }}</span>
            <span class="mini-meta">
              <span v-if="post.category" class="mini-tag">{{ post.category }}</span>
              <span>{{ formatDate(post.published_at || post.created_at) }}</span>
            </span>
          </div>
          <span class="mini-stats">
            <i class="fas fa-heart"></i> {{ post.like_count || 0 }}
          </span>
        </router-link>
      </div>
      <div class="empty-section" v-else>
        <i class="fas fa-file-alt"></i>
        <span>暂无文章</span>
      </div>

      <!-- ===== 最新动态 ===== -->
      <div class="section-header">
        <h3 class="section-title"><i class="fas fa-camera"></i> 最新动态</h3>
        <router-link to="/moments" class="section-more">
          查看全部 <i class="fas fa-chevron-right"></i>
        </router-link>
      </div>
      <div class="feed-list" v-if="latestMoments.length">
        <div v-for="moment in latestMoments" :key="moment.id" class="feed-card"
          @click="$router.push(`/moments?id=${moment.id}`)">
          <div class="card-left">
            <div class="card-avatar">
              <img src="https://picsum.photos/id/64/100/100" alt="" />
            </div>
          </div>
          <div class="card-body">
            <div class="card-top">
              <span class="card-name">克莱·C</span>
              <span class="card-date">{{ formatDate(moment.created_at) }}</span>
            </div>
            <div class="card-content">{{ moment.content }}</div>
            <div class="card-images" v-if="moment.imagesList && moment.imagesList.length">
              <div class="card-img-item" v-for="(img, j) in moment.imagesList.slice(0, 4)" :key="j">
                <img :src="resolveThumbUrl(img)" alt="" />
              </div>
            </div>
            <div class="card-footer">
              <div class="card-actions">
                <span class="action-btn">
                  <i class="far fa-heart"></i>
                  <span v-if="moment.like_count">{{ moment.like_count }}</span>
                </span>
                <span class="action-btn">
                  <i class="far fa-comment"></i>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="empty-section" v-else>
        <i class="fas fa-camera-retro"></i>
        <span>暂无动态</span>
      </div>

      <!-- ===== 最近读书（已隐藏） ===== -->
      <!--
      <div class="section-header">
        <h3 class="section-title"><i class="fas fa-book"></i> 最近读书</h3>
        <router-link to="/reading" class="section-more">
          查看全部 <i class="fas fa-chevron-right"></i>
        </router-link>
      </div>
      <div class="books-grid" v-if="latestBooks.length">
        <router-link v-for="book in latestBooks" :key="book.id" :to="`/book/${book.id}`" class="book-card">
          <div class="book-cover" v-if="book.cover_url">
            <img :src="resolveThumbUrl(book.cover_url)" :alt="book.title" />
          </div>
          <div class="book-cover book-cover-placeholder" v-else>
            <i class="fas fa-book-open"></i>
          </div>
          <div class="book-info">
            <h4 class="book-title">{{ book.title }}</h4>
            <p class="book-author" v-if="book.author">{{ book.author }}</p>
            <p class="book-desc" v-if="book.description">{{ book.description }}</p>
          </div>
        </router-link>
      </div>
      <div class="empty-section" v-else>
        <i class="fas fa-book"></i>
        <span>暂无读书</span>
      </div>
      -->

      <!-- ===== 关于我 - 更多信息（已隐藏） ===== -->
      <!--
      <div class="about-more-section">
        <div class="about-grid">
          <div class="about-card">
            <div class="about-card-icon"><i class="fas fa-code"></i></div>
            <h3>技术栈</h3>
            <p>Vue · React · Node.js · Python · TypeScript · Tailwind · Docker</p>
          </div>
          <div class="about-card">
            <div class="about-card-icon"><i class="fas fa-paint-brush"></i></div>
            <h3>设计</h3>
            <p>UI/UX 设计 · 玻璃拟态 · 深色主题 · 响应式布局 · Figma</p>
          </div>
          <div class="about-card">
            <div class="about-card-icon"><i class="fas fa-music"></i></div>
            <h3>爱好</h3>
            <p>独立音乐 · 摄影 · 写作 · 咖啡 · 旅行 · 科幻小说</p>
          </div>
          <div class="about-card">
            <div class="about-card-icon"><i class="fas fa-graduation-cap"></i></div>
            <h3>经历</h3>
            <p>5 年全栈开发 · 3 年开源贡献 · 前大厂工程师 · 现独立创作者</p>
          </div>
        </div>

        <div class="about-timeline">
          <h3 class="timeline-title">📅 时间线</h3>
          <div class="timeline-item" v-for="(item, i) in timeline" :key="i">
            <div class="timeline-dot"></div>
            <div class="timeline-content">
              <span class="timeline-year">{{ item.year }}</span>
              <h4>{{ item.title }}</h4>
              <p>{{ item.desc }}</p>
            </div>
          </div>
        </div>
      </div>
      -->
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { publicApi, resolveThumbUrl } from '@/utils/api'
import Skeleton from '@/components/Skeleton.vue'
import AboutHero from '@/components/AboutHero.vue'

const loading = ref(true)
const latestPosts = ref([])
const latestMoments = ref([])
const latestBooks = ref([])

const timeline = [
  { year: '2021', title: '毕业 · 加入大厂', desc: '计算机科学学士，入职某互联网公司前端团队' },
  { year: '2022', title: '开源贡献', desc: '开始参与 Vue 生态开源项目，累计 500+ PR' },
  { year: '2023', title: '独立创作', desc: '离开大厂，成为独立开发者，开始做自己的产品' },
  { year: '2024', title: '汽水平台', desc: '创立汽水平台，探索设计与技术的边界' },
  { year: '2025', title: '持续进化', desc: '不断学习，持续输出，做有意义的产品' },
]

// ===== 打字机效果 =====
const typewriterLines = [
  '欢迎来到我的世界',
  '不管你见到的是如何的我',
  '或开朗 或小气 或情绪化 ',
  '或阴险 或克制 或自律 或向上',
  '或是一滩扶不上墙的烂泥',
  '你看到的都是真实的我',
  '如果你看见这样的我',
  '还愿意继续认识我',
  '我很感恩你的到来',
]
const typewriterCurrentLine = ref(0)
const typewriterDone = ref(false)
const typewriterDisplay = ref(typewriterLines.map(() => ''))
let typewriterTimer = null

function startTypewriter() {
  let lineIdx = 0
  let charIdx = 0

  function typeNextChar() {
    const line = typewriterLines[lineIdx]
    if (charIdx < line.length) {
      typewriterCurrentLine.value = lineIdx
      const display = [...typewriterDisplay.value]
      display[lineIdx] = line.substring(0, charIdx + 1)
      typewriterDisplay.value = display
      charIdx++
      const delay = 30 + Math.random() * 50
      typewriterTimer = setTimeout(typeNextChar, delay)
    } else {
      lineIdx++
      charIdx = 0
      if (lineIdx < typewriterLines.length) {
        const delay = 200 + Math.random() * 200
        typewriterTimer = setTimeout(typeNextChar, delay)
      } else {
        typewriterDone.value = true
      }
    }
  }

  typewriterTimer = setTimeout(typeNextChar, 500)
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  const now = new Date()
  const diff = now - d
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days} 天前`
  return `${d.getMonth() + 1}/${d.getDate()}`
}

onMounted(async () => {
  try {
    const [postsRes, momentsRes, booksRes] = await Promise.allSettled([
      publicApi.getLatestPosts(),
      publicApi.getLatestMoments(),
      publicApi.getBooks(),
    ])

    if (postsRes.status === 'fulfilled') {
      latestPosts.value = postsRes.value.items || []
    }
    if (momentsRes.status === 'fulfilled') {
      latestMoments.value = (momentsRes.value.items || []).map(item => ({
        ...item,
        imagesList: item.images ? item.images.split(',').filter(Boolean).map(s => s.trim()) : [],
      }))
    }
    if (booksRes.status === 'fulfilled') {
      latestBooks.value = (booksRes.value.items || []).slice(0, 4)
    }
  } catch (e) {
    console.error('加载首页数据失败:', e)
  } finally {
    loading.value = false
    startTypewriter()
  }
})
</script>

<style scoped>
.discover {
  padding-bottom: 40px;
  position: relative;
}

/* ===== 骨架屏 ===== */
.skeleton-home {
  padding: 32px 0 40px;
}

.skeleton-hero {
  display: flex;
  align-items: center;
  gap: 20px;
  padding-bottom: 28px;
  margin-bottom: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

.skeleton-hero-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skeleton-section {
  margin: 32px 0 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.skeleton-categories {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 10px;
}

.skeleton-cat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 18px 12px 14px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 14px;
}

.skeleton-articles {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.skeleton-article-card {
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(255, 255, 255, 0.02);
}

.skeleton-article-body {
  padding: 14px 16px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skeleton-moments {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 12px;
}

.skeleton-moment-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 14px;
  overflow: hidden;
  padding: 0 0 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skeleton-moment-card :deep(.skeleton) {
  border-radius: 0;
}

.skeleton-moment-card :deep(.skeleton:first-child) {
  border-radius: 0;
}

/* ===== 黑客打字机盒子 ===== */
.hacker-box {
  margin: 20px 0 24px;
  border-radius: 14px;
  background: rgba(0, 0, 0, 0.55);
  border: 1px solid rgba(0, 242, 192, 0.1);
  box-shadow: 0 0 40px rgba(0, 242, 192, 0.03), inset 0 0 80px rgba(0, 242, 192, 0.015);
  backdrop-filter: blur(6px);
  position: relative;
  overflow: hidden;
}

.hacker-bar {
  display: flex;
  align-items: center;
  padding: 10px 16px;
  background: rgba(0, 0, 0, 0.3);
  border-bottom: 1px solid rgba(0, 242, 192, 0.06);
}

.hacker-dots {
  display: flex;
  gap: 7px;
}

.hacker-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.hacker-dot.red {
  background: #ff5f56;
}

.hacker-dot.yellow {
  background: #ffbd2e;
}

.hacker-dot.green {
  background: #27c93f;
}

.hacker-content {
  padding: 16px 24px 20px;
  position: relative;
  z-index: 1;
  font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
  font-size: 13px;
  line-height: 1.9;
}

.hacker-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: repeating-linear-gradient(0deg,
      transparent,
      transparent 2px,
      rgba(0, 242, 192, 0.015) 2px,
      rgba(0, 242, 192, 0.015) 4px);
  pointer-events: none;
  z-index: 0;
}

.hacker-box::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(ellipse at 30% 20%, rgba(0, 242, 192, 0.04), transparent 50%);
  pointer-events: none;
  z-index: 0;
}

.hacker-line {
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 24px;
}

.hacker-prompt {
  color: #00F2C0;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
  user-select: none;
}

.hacker-text {
  color: rgba(255, 255, 255, 0.7);
  word-break: break-all;
}

.hacker-cursor {
  color: #00F2C0;
  font-size: 14px;
  animation: blink 0.8s step-end infinite;
  font-weight: 300;
  margin-left: -1px;
}

@keyframes blink {

  0%,
  100% {
    opacity: 1;
  }

  50% {
    opacity: 0;
  }
}

/* ===== 通用区块 ===== */
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 32px 0 16px;
}

.section-title {
  font-size: 17px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-title i {
  font-size: 14px;
  color: #00F2C0;
}

.section-more {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.3);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: color 0.2s;
}

.section-more:hover {
  color: #00F2C0;
}

.section-more i {
  font-size: 10px;
}

/* ===== 紧凑文章列表 ===== */
.mini-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.mini-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.mini-item:hover {
  background: rgba(255, 255, 255, 0.04);
}

.mini-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #00F2C0;
  flex-shrink: 0;
  opacity: 0.5;
}

.mini-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.mini-title {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.7);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4;
  transition: color 0.2s;
}

.mini-item:hover .mini-title {
  color: #00F2C0;
}

.mini-meta {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  gap: 6px;
}

.mini-tag {
  font-size: 10px;
  color: #00F2C0;
  background: rgba(0, 242, 192, 0.08);
  padding: 1px 7px;
  border-radius: 10px;
}

.mini-stats {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.15);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 3px;
  transition: color 0.2s;
}

.mini-item:hover .mini-stats {
  color: #ff6b6b;
}

.mini-stats i {
  font-size: 10px;
}

/* ===== 动态卡片（朋友圈样式） ===== */
.feed-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.feed-card {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 14px 16px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 14px;
  border: 1px solid transparent;
  transition: all 0.2s ease;
  cursor: pointer;
}

.feed-card:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.06);
}

.card-left {
  flex-shrink: 0;
}

.card-avatar {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  overflow: hidden;
  flex-shrink: 0;
}

.card-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-body {
  flex: 1;
  min-width: 0;
}

.card-top {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.card-name {
  font-size: 13px;
  font-weight: 600;
  color: #00F2C0;
}

.card-date {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.2);
}

.card-content {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.55);
  line-height: 1.6;
  white-space: pre-wrap;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-images {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 3px;
  margin-top: 8px;
  max-width: 300px;
}

.card-images:has(.card-img-item:only-child) {
  grid-template-columns: 1fr;
  max-width: 160px;
}

.card-images:has(.card-img-item:first-child:nth-last-child(2),
  .card-img-item:first-child:nth-last-child(2) ~ .card-img-item) {
  grid-template-columns: 1fr 1fr;
  max-width: 220px;
}

.card-images:has(.card-img-item:first-child:nth-last-child(3),
  .card-img-item:first-child:nth-last-child(3) ~ .card-img-item) {
  grid-template-columns: repeat(3, 1fr);
  max-width: 260px;
}

.card-img-item {
  aspect-ratio: 1;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 5px;
}

.card-images:has(.card-img-item:only-child) .card-img-item {
  aspect-ratio: 16 / 9;
  border-radius: 6px;
}

.card-img-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.feed-card:hover .card-img-item img {
  transform: scale(1.06);
}

.card-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 6px;
}

.card-actions {
  display: flex;
  gap: 14px;
}

.action-btn {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  gap: 4px;
  transition: color 0.2s;
}

.action-btn:hover {
  color: #ff6b6b;
}

.action-btn i {
  font-size: 13px;
}

/* ===== 读书网格 ===== */
.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 14px;
}

.book-card {
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 14px;
  overflow: hidden;
  text-decoration: none;
  transition: all 0.25s ease;
}

.book-card:hover {
  background: rgba(0, 242, 192, 0.04);
  border-color: rgba(0, 242, 192, 0.15);
  transform: translateY(-3px);
}

.book-cover {
  aspect-ratio: 3/4;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.2);
}

.book-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.book-card:hover .book-cover img {
  transform: scale(1.05);
}

.book-cover-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  color: rgba(255, 255, 255, 0.08);
}

.book-info {
  padding: 12px 14px 14px;
}

.book-title {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.book-author {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.3);
  margin: 4px 0 0;
}

.book-desc {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.35);
  margin: 6px 0 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
}

/* ===== 空状态 ===== */
.empty-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 32px 0;
  color: rgba(255, 255, 255, 0.12);
  font-size: 14px;
}

.empty-section i {
  font-size: 28px;
  opacity: 0.5;
}

/* ===== 关于我 - 更多信息 ===== */
.about-more-section {
  margin-top: 48px;
  padding-top: 32px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.about-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.about-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 16px;
  padding: 20px 24px;
  transition: all 0.25s ease;
}

.about-card:hover {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(0, 242, 192, 0.15);
  transform: translateY(-2px);
}

.about-card-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: rgba(0, 242, 192, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: #00F2C0;
  margin-bottom: 14px;
}

.about-card h3 {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  margin: 0 0 6px;
}

.about-card p {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.4);
  line-height: 1.6;
  margin: 0;
}

.about-timeline {
  margin-top: 40px;
}

.timeline-title {
  font-size: 18px;
  font-weight: 600;
  color: #00F2C0;
  margin-bottom: 24px;
}

.timeline-item {
  display: flex;
  gap: 20px;
  padding-bottom: 24px;
  position: relative;
  padding-left: 28px;
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: 8px;
  top: 20px;
  bottom: 8px;
  width: 2px;
  background: linear-gradient(to bottom, #00F2C0, rgba(0, 242, 192, 0.05));
  border-radius: 2px;
}

.timeline-item:last-child::before {
  display: none;
}

.timeline-dot {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: transparent;
  border: 3px solid #00F2C0;
  flex-shrink: 0;
  margin-top: 2px;
  position: relative;
  z-index: 1;
  box-shadow: 0 0 0 4px rgba(0, 242, 192, 0.1);
  transition: all 0.3s ease;
}

.timeline-item:hover .timeline-dot {
  background: #00F2C0;
  box-shadow: 0 0 0 6px rgba(0, 242, 192, 0.15);
}

.timeline-content {
  flex: 1;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.04);
  border-radius: 14px;
  padding: 16px 20px;
  transition: all 0.25s ease;
}

.timeline-content:hover {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(0, 242, 192, 0.12);
  transform: translateX(4px);
}

.timeline-year {
  font-family: 'JetBrains Mono', 'Noto Sans Mono', monospace;
  font-size: 12px;
  color: #00F2C0;
  font-weight: 600;
  letter-spacing: 1px;
}

.timeline-content h4 {
  font-size: 15px;
  font-weight: 600;
  color: #fff;
  margin: 4px 0 6px;
}

.timeline-content p {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.4);
  line-height: 1.5;
  margin: 0;
}

/* ===== 响应式 ===== */
@media (max-width: 900px) {
  .hacker-content {
    padding: 14px 18px 18px;
    font-size: 12px;
  }
}

@media (max-width: 640px) {
  .books-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }

  .about-grid {
    grid-template-columns: 1fr;
  }

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
  }

  .hacker-content {
    padding: 12px 14px 16px;
    font-size: 11px;
    line-height: 1.8;
  }

  .hacker-line {
    gap: 6px;
    min-height: 20px;
  }

  .hacker-prompt {
    font-size: 12px;
  }

  .hacker-text {
    word-break: break-word;
  }
}
</style>
