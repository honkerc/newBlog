<template>
    <div class="reading-page">
        <div class="page-head">
            <h1 class="head-title">书架</h1>
            <p class="head-desc">在文字里，遇见更大的世界</p>
        </div>

        <!-- 骨架屏 -->
        <div class="skeleton-bookcase" v-if="loading">
            <div class="skeleton-cornice"></div>
            <div class="skeleton-wall">
                <div class="skeleton-shelf" v-for="n in 5" :key="n">
                    <div class="skeleton-books">
                        <div class="skeleton-book" v-for="m in 12" :key="m"
                            :style="{ height: (60 + (m * 7 + n * 11) % 40) + 'px' }"></div>
                    </div>
                    <div class="skeleton-board"></div>
                </div>
            </div>
        </div>

        <div class="bookcase" v-if="!loading">
            <!-- 顶部楣板 -->
            <div class="top-cornice">
                <div class="cornice-ornament"></div>
                <div class="cornice-tassel-wrap">
                    <div class="cornice-tassel"></div>
                </div>
                <div class="cornice-ornament"></div>
            </div>

            <!-- 墙面+书架主体 -->
            <div class="wall">
                <div class="shelves-area">
                    <div class="shelf-row" v-for="(row, ri) in shelfRows" :key="ri">
                        <div class="shelf-bracket left"></div>
                        <div class="shelf-content">
                            <div class="books">
                                <!-- 装饰物 -->
                                <template v-for="(ornament, oi) in row.ornaments" :key="'o-' + ri + '-' + oi">
                                    <div class="ornament" v-if="ornament.type === 0">
                                        <div class="plant-leaves">
                                            <div class="leaf leaf1"></div>
                                            <div class="leaf leaf2"></div>
                                            <div class="leaf leaf3"></div>
                                        </div>
                                        <div class="plant-pot"></div>
                                    </div>
                                    <div class="ornament" v-else-if="ornament.type === 1">
                                        <div class="photo-frame">
                                            <div class="frame-inner"></div>
                                        </div>
                                    </div>
                                    <div class="ornament" v-else-if="ornament.type === 2">
                                        <div class="small-candle"></div>
                                    </div>
                                </template>
                                <!-- 书本 -->
                                <div class="book" v-for="(book, bi) in row.books" :key="book.id" @click="goToBook(book)"
                                    :class="getBookClasses(book, bi)" :style="getBookOuterStyle(book, bi)">
                                    <div class="book-body" :style="getBookBodyStyle(book, bi)">
                                        <template v-if="getDeco(book, bi).bands === 'double'">
                                            <div class="book-band top-band"></div>
                                            <div class="book-band top-band-2"></div>
                                            <div class="book-band bottom-band"></div>
                                            <div class="book-band bottom-band-2"></div>
                                        </template>
                                        <template v-else>
                                            <div class="book-band top-band"></div>
                                            <div class="book-band bottom-band"></div>
                                        </template>
                                        <div class="book-foil" v-if="getDeco(book, bi).foil"></div>
                                        <div class="book-ribbon"
                                            :class="['ribbon-' + getDeco(book, bi).bookmark, 'ribbon-' + getDeco(book, bi).bookmarkPos]"
                                            v-if="getDeco(book, bi).bookmark"></div>
                                        <div class="book-sticker" :class="getDeco(book, bi).stickerClass"
                                            v-if="getDeco(book, bi).sticker">{{
                                                getDeco(book, bi).stickerText }}</div>
                                        <div class="book-label" v-if="getDeco(book, bi).label">{{ getDeco(book,
                                            bi).label }}
                                        </div>
                                        <div class="book-wear" v-if="getDeco(book, bi).wear"></div>
                                        <div class="book-ridge" v-if="getDeco(book, bi).ridge"></div>
                                        <div class="book-pattern stripes"
                                            v-if="getDeco(book, bi).pattern === 'stripes'">
                                        </div>
                                        <div class="book-year" v-if="getDeco(book, bi).year">{{ getDeco(book, bi).year
                                        }}
                                        </div>
                                        <div class="book-author" v-if="getDeco(book, bi).author">{{ getDeco(book,
                                            bi).author
                                        }}</div>
                                        <div class="book-headpiece" v-if="getDeco(book, bi).headpiece"></div>
                                        <div class="book-publisher" v-if="getDeco(book, bi).publisher">{{ getDeco(book,
                                            bi).publisher }}</div>
                                        <div class="book-title">{{ getBookShortTitle(book) }}</div>
                                    </div>
                                </div>
                            </div>
                            <div class="shelf-board"></div>
                        </div>
                        <div class="shelf-bracket right"></div>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { publicApi } from '@/utils/api'

const router = useRouter()
const loading = ref(true)
const books = ref([])

// 颜色池 - 用于书本配色
const colorPool = [
    '#2c3e50', '#8e44ad', '#16a085', '#c0392b', '#d35400', '#2980b9', '#27ae60', '#7f8c8d',
    '#e74c3c', '#1abc9c', '#34495e', '#9b59b6', '#e67e22', '#2ecc71', '#3498db', '#f39c12',
    '#6c3483', '#1a5276', '#0e6655', '#7b241c', '#4a235a', '#a0522d', '#212f3d', '#7e5109',
    '#1b4f72', '#78281f', '#145a32', '#641e16', '#0b5345', '#1b2631', '#4d5656', '#6c3483',
]

// 将书籍分配到5层书架
const shelfRows = computed(() => {
    const rows = []
    const items = [...books.value]
    const perRow = Math.ceil(items.length / 5)

    for (let r = 0; r < 5; r++) {
        const rowBooks = items.slice(r * perRow, (r + 1) * perRow)
        // 生成装饰物
        const ornamentCount = Math.random() < 0.55 ? (Math.random() < 0.5 ? 1 : 2) : 0
        const ornPositions = new Set()
        while (ornPositions.size < ornamentCount) {
            ornPositions.add(Math.floor(Math.random() * (rowBooks.length + 2)))
        }
        const ornaments = []
        for (const pos of ornPositions) {
            ornaments.push({ type: Math.floor(Math.random() * 3), at: pos })
        }
        ornaments.sort((a, b) => a.at - b.at)

        rows.push({ books: rowBooks, ornaments })
    }
    return rows
})

// 获取简短书名（去掉《》和副标题）
function getBookShortTitle(book) {
    let title = book.title || ''
    title = title.replace(/[《》]/g, '')
    // 如果书名太长，截取前4个字
    if (title.length > 6) {
        title = title.slice(0, 6) + '…'
    }
    return title
}

function lighten(hex, pct) {
    const num = parseInt(hex.slice(1), 16)
    const r = Math.min(255, (num >> 16) + pct)
    const g = Math.min(255, ((num >> 8) & 0x00FF) + pct)
    const b = Math.min(255, (num & 0x0000FF) + pct)
    return `rgb(${r},${g},${b})`
}

function darken(hex, pct) {
    const num = parseInt(hex.slice(1), 16)
    const r = Math.max(0, (num >> 16) - pct)
    const g = Math.max(0, ((num >> 8) & 0x00FF) - pct)
    const b = Math.max(0, (num & 0x0000FF) - pct)
    return `rgb(${r},${g},${b})`
}

function getBookBodyStyle(book, idx) {
    const c = colorPool[(book.id * 7 + idx * 13) % colorPool.length]
    const h = 95 + (book.id * 3 + idx * 7) % 30
    return {
        background: `linear-gradient(180deg, ${lighten(c, 30)}, ${c} 15%, ${darken(c, 8)} 80%, ${darken(c, 18)})`,
        height: h + 'px',
    }
}

function getBookOuterStyle(book, idx) {
    const tilt = (book.id * 3 + idx) % 7
    if (tilt === 0) return { transform: 'rotate(-5deg) translateY(-3px)' }
    if (tilt === 1) return { transform: 'rotate(5deg) translateY(-3px)' }
    if (tilt === 2) return { transform: 'rotate(4deg) translateY(-2px)' }
    return {}
}

function getBookClasses(book, idx) {
    const tilt = (book.id * 3 + idx) % 7
    const classes = []
    if (tilt === 0) classes.push('tilted-left')
    else if (tilt === 1) classes.push('tilted-right')
    else if (tilt === 2) classes.push('leaning')
    else if (tilt === 3) classes.push('short-book')
    else if (tilt === 4) classes.push('gap-book')
    return classes
}

function getDeco(book, idx) {
    const r = (book.id * 13 + idx) % 37
    const d = {
        bands: 'single',
        foil: false,
        bookmark: null,
        bookmarkPos: 'bottom',
        sticker: false,
        stickerText: '',
        stickerClass: '',
        label: null,
        wear: false,
        ridge: false,
        pattern: null,
        year: null,
        author: null,
        headpiece: false,
        publisher: null,
    }
    if ((idx + 1) % 5 === 0) d.bands = 'double'
    if (r % 5 === 0) d.foil = true
    if (r % 11 === 0) {
        const cols = ['red', 'gold', 'blue', 'green', 'purple', 'teal']
        d.bookmark = cols[idx % cols.length]
        d.bookmarkPos = (idx % 2 === 0) ? 'bottom' : 'top'
    }
    if (r % 12 === 0) { d.sticker = true; d.stickerText = '新'; d.stickerClass = '' }
    if (r % 17 === 0) { d.sticker = true; d.stickerText = '★'; d.stickerClass = 'sticker-star' }
    if (r % 13 === 0) d.label = ['A', 'B', 'C'][idx % 3]
    if (r % 9 === 0) d.wear = true
    if (r % 8 === 0) d.ridge = true
    if (r % 10 === 0) d.pattern = 'stripes'
    if (r % 15 === 0) d.year = ['2024', '2023'][idx % 2]
    if (r % 16 === 0) d.author = ['村上', '余华'][idx % 2]
    if (r % 18 === 0) d.headpiece = true
    if (r % 19 === 0) d.publisher = '◎'
    return d
}

function goToBook(book) {
    router.push(`/reading/${encodeURIComponent(book.title)}`)
}

onMounted(async () => {
    try {
        const res = await publicApi.getBooks()
        books.value = res.items || []
    } catch (e) {
        console.error('加载书籍列表失败:', e)
    } finally {
        loading.value = false
    }
})
</script>

<style scoped>
.reading-page {
    width: 100%;
    padding: 0 20px 40px;
}

/* ===== 头部 ===== */
.page-head {
    padding: 48px 0 28px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 30px;
    position: relative;
}

.head-title {
    font-size: 42px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -1px;
    line-height: 1.15;
    margin: 0;
    background: linear-gradient(135deg, #FFFFFF 60%, rgba(255, 255, 255, 0.5));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.head-desc {
    font-size: 15px;
    color: rgba(255, 255, 255, 0.35);
    margin-top: 10px;
    font-weight: 400;
    letter-spacing: 0.3px;
}

/* ===== 骨架屏 ===== */
.skeleton-bookcase {
    background: rgba(30, 35, 40, 0.25);
    border-radius: 10px;
    padding: 0;
    overflow: hidden;
}

.skeleton-cornice {
    height: 28px;
    background: rgba(255, 255, 255, 0.04);
    border-radius: 8px 8px 0 0;
}

.skeleton-wall {
    padding: 25px 15px;
}

.skeleton-shelf {
    margin-bottom: 40px;
}

.skeleton-shelf:last-child {
    margin-bottom: 0;
}

.skeleton-books {
    display: flex;
    gap: 2px;
    align-items: flex-end;
    padding: 0 10px;
}

.skeleton-book {
    flex: 1;
    background: rgba(255, 255, 255, 0.04);
    border-radius: 2px 2px 0 0;
    animation: pulse 1.5s ease-in-out infinite;
}

.skeleton-board {
    height: 12px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 3px;
    margin-top: 0;
}

@keyframes pulse {

    0%,
    100% {
        opacity: 0.3;
    }

    50% {
        opacity: 0.6;
    }
}

/* ===== 书架外壳 ===== */
.bookcase {
    position: relative;
    background: rgba(30, 35, 40, 0.25);
    border-radius: 10px;
    box-shadow: inset 0 0 35px rgba(0, 0, 0, 0.2);
    padding: 0;
}

/* ===== 顶部楣板 ===== */
.top-cornice {
    height: 28px;
    background: linear-gradient(180deg, rgba(130, 150, 160, 0.6) 0%, rgba(90, 110, 120, 0.5) 40%, rgba(60, 80, 90, 0.45) 100%);
    border-radius: 8px 8px 0 0;
    margin: 0;
    position: relative;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(200, 210, 180, 0.3);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
}

.cornice-ornament {
    width: 40px;
    height: 6px;
    background: linear-gradient(90deg, transparent, rgba(200, 180, 140, 0.6), transparent);
    border-radius: 2px;
}

.cornice-tassel-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.cornice-tassel {
    width: 2px;
    height: 18px;
    background: #b0976a;
    position: relative;
}

.cornice-tassel::after {
    content: '';
    position: absolute;
    bottom: -6px;
    left: -4px;
    width: 10px;
    height: 8px;
    background: radial-gradient(circle, #c4a36a, #8b6d42);
    border-radius: 50%;
}

/* ===== 墙面 ===== */
.wall {
    position: relative;
    padding: 25px 15px 25px 15px;
    background:
        repeating-linear-gradient(0deg, transparent, transparent 80px, rgba(255, 255, 255, 0.02) 80px, rgba(255, 255, 255, 0.02) 81px),
        repeating-linear-gradient(90deg, transparent, transparent 100px, rgba(255, 255, 255, 0.015) 100px, rgba(255, 255, 255, 0.015) 101px);
    display: flex;
    gap: 0;
}

/* ===== 书架主体 ===== */
.shelves-area {
    flex: 1;
    display: flex;
    flex-direction: column;
}

/* ===== 搁板行 ===== */
.shelf-row {
    display: flex;
    align-items: flex-end;
    justify-content: center;
    margin-bottom: 40px;
    height: 180px;
    gap: 0;
}

.shelf-row:last-child {
    margin-bottom: 0;
}

/* ===== 支架 ===== */
.shelf-bracket {
    width: 7px;
    background: linear-gradient(180deg, rgba(45, 60, 70, 0.6), rgba(30, 45, 55, 0.55));
    border-radius: 2px;
    align-self: stretch;
    position: relative;
    z-index: 1;
    margin-top: auto;
    height: 20px;
}

.shelf-bracket::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -4px;
    right: -4px;
    height: 6px;
    background: rgba(150, 170, 180, 0.2);
    border-radius: 2px;
}

.shelf-bracket.left {
    margin-right: 3px;
}

.shelf-bracket.right {
    margin-left: 3px;
}

/* ===== 搁板内容区 ===== */
.shelf-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    position: relative;
}

/* ===== 书籍排列 ===== */
.books {
    display: flex;
    align-items: flex-end;
    gap: 0;
    padding: 0 1px;
    position: relative;
    z-index: 3;
}

/* ===== 书本 ===== */
.book {
    cursor: pointer;
    transition: all 0.25s ease;
    width: 100%;
    max-width: 34px;
    min-width: 10px;
    flex: 1 1 0;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    margin: 0 1px;
    position: relative;
}

.book:hover {
    transform: translateY(-8px) !important;
    z-index: 20;
    filter: brightness(1.15);
}

.book.tilted-left {
    transform-origin: bottom center;
}

.book.tilted-right {
    transform-origin: bottom center;
}

.book.leaning {
    transform-origin: bottom center;
}

.book.short-book .book-body {
    margin-top: 12px;
}

.book.gap-book {
    margin-left: 8px;
}

/* ===== 书体 ===== */
.book-body {
    width: 100%;
    border-radius: 1px 3px 0 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    box-shadow: 1px 0 4px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    transition: all 0.25s ease;
    overflow: hidden;
    padding: 6px 2px;
}

.book-body::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 30%;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.12), transparent);
    pointer-events: none;
    z-index: 1;
}

/* ===== 书脊装饰带 ===== */
.book-band {
    position: absolute;
    left: 2px;
    right: 2px;
    height: 2px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 1px;
    z-index: 2;
}

.top-band {
    top: 3px;
}

.bottom-band {
    bottom: 3px;
}

.top-band-2 {
    position: absolute;
    left: 2px;
    right: 2px;
    height: 1px;
    background: rgba(255, 255, 255, 0.08);
    top: 6px;
    z-index: 2;
}

.bottom-band-2 {
    position: absolute;
    left: 2px;
    right: 2px;
    height: 1px;
    background: rgba(255, 255, 255, 0.08);
    bottom: 6px;
    z-index: 2;
}

/* ===== 金色烫印 ===== */
.book-foil {
    position: absolute;
    left: 6px;
    right: 6px;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(180, 200, 160, 0.25), transparent);
    top: 50%;
    z-index: 2;
}

/* ===== 书签丝带 ===== */
.book-ribbon {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    width: 4px;
    height: 16px;
    z-index: 10;
    box-shadow: 1px 2px 4px rgba(0, 0, 0, 0.3);
}

.ribbon-bottom {
    bottom: -9px;
    border-radius: 0 0 3px 3px;
}

.ribbon-top {
    top: -9px;
    border-radius: 3px 3px 0 0;
}

.ribbon-red {
    background: linear-gradient(180deg, #e74c3c, #b03a2e);
}

.ribbon-gold {
    background: linear-gradient(180deg, #f1c40f, #b7950b);
}

.ribbon-blue {
    background: linear-gradient(180deg, #3498db, #2471a3);
}

.ribbon-green {
    background: linear-gradient(180deg, #2ecc71, #1e8449);
}

.ribbon-purple {
    background: linear-gradient(180deg, #9b59b6, #7d3c98);
}

.ribbon-teal {
    background: linear-gradient(180deg, #1abc9c, #148f77);
}

/* ===== 标签贴纸 ===== */
.book-sticker {
    position: absolute;
    top: 15%;
    left: 50%;
    transform: translateX(-50%);
    font-size: 5px;
    font-weight: 700;
    color: #fff;
    padding: 2px 4px;
    border-radius: 2px;
    background: rgba(231, 76, 60, 0.8);
    z-index: 5;
}

.book-sticker.sticker-star {
    background: rgba(241, 196, 15, 0.85);
}

/* ===== 编号标签 ===== */
.book-label {
    position: absolute;
    bottom: 15px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 5px;
    color: rgba(255, 255, 255, 0.4);
    background: rgba(0, 0, 0, 0.3);
    padding: 1px 3px;
    border-radius: 2px;
    z-index: 3;
}

/* ===== 磨损痕迹 ===== */
.book-wear {
    position: absolute;
    top: 30%;
    left: 0;
    right: 0;
    height: 5px;
    background: linear-gradient(180deg, transparent, rgba(0, 0, 0, 0.1), transparent);
    z-index: 2;
}

/* ===== 书脊凸起 ===== */
.book-ridge {
    position: absolute;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.08) 30%, rgba(255, 255, 255, 0.12) 50%, rgba(255, 255, 255, 0.08) 70%, transparent);
    top: 45%;
    z-index: 2;
}

/* ===== 图案 ===== */
.book-pattern.stripes {
    position: absolute;
    top: 20%;
    left: 3px;
    right: 3px;
    height: 15%;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255, 255, 255, 0.05) 2px, rgba(255, 255, 255, 0.05) 4px);
    z-index: 2;
}

/* ===== 年份 ===== */
.book-year {
    position: absolute;
    top: 5px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 5px;
    color: rgba(255, 255, 255, 0.3);
    z-index: 3;
}

/* ===== 作者 ===== */
.book-author {
    position: absolute;
    bottom: 22px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 5px;
    color: rgba(255, 255, 255, 0.2);
    z-index: 3;
}

/* ===== 顶部装饰 ===== */
.book-headpiece {
    position: absolute;
    top: 5px;
    left: 4px;
    right: 4px;
    height: 3px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.06) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.06) 75%, transparent);
    z-index: 2;
}

/* ===== 出版社标记 ===== */
.book-publisher {
    position: absolute;
    bottom: 4px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 6px;
    color: rgba(255, 255, 255, 0.15);
    z-index: 3;
}

/* ===== 书名 ===== */
.book-title {
    writing-mode: vertical-rl;
    text-orientation: upright;
    font-size: 11px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.95);
    letter-spacing: 3px;
    text-shadow: 0 1px 4px rgba(0, 0, 0, 0.6);
    transition: all 0.25s ease;
    user-select: none;
    flex-grow: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 4;
    margin: 6px 0;
    line-height: 1.1;
    white-space: nowrap;
}

.book:hover .book-title {
    color: #FFFFFF;
    letter-spacing: 3px;
    text-shadow: 0 0 14px rgba(0, 242, 192, 0.4);
}

/* ===== 隔板 ===== */
.shelf-board {
    height: 12px;
    background: linear-gradient(180deg,
            rgba(120, 140, 150, 0.45),
            rgba(90, 110, 120, 0.35) 45%,
            rgba(60, 80, 90, 0.4));
    border-radius: 3px;
    box-shadow: 0 5px 14px rgba(0, 0, 0, 0.28), inset 0 1px 0 rgba(190, 210, 190, 0.15);
    z-index: 2;
    position: relative;
}

.shelf-board::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: repeating-linear-gradient(90deg, transparent, transparent 18px, rgba(70, 90, 100, 0.15) 18px, rgba(70, 90, 100, 0.15) 19px);
    border-radius: 3px;
}

/* ===== 装饰物 ===== */
.ornament {
    flex-shrink: 0;
    align-self: flex-end;
    margin: 0 4px;
    z-index: 5;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.plant-pot {
    width: 20px;
    height: 28px;
    background: linear-gradient(180deg, #c49a6c, #8b5a3a);
    border-radius: 2px 2px 5px 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
    position: relative;
    margin-top: -8px;
}

.plant-leaves {
    position: relative;
    width: 26px;
    height: 30px;
}

.leaf {
    position: absolute;
    background: #4d6b3a;
    border-radius: 60% 5px 60% 5px;
    transform-origin: bottom center;
}

.leaf1 {
    width: 10px;
    height: 20px;
    bottom: 0;
    left: 8px;
    transform: rotate(-10deg);
    background: #557a3a;
}

.leaf2 {
    width: 8px;
    height: 18px;
    bottom: 0;
    left: 4px;
    transform: rotate(-25deg);
    background: #44632e;
}

.leaf3 {
    width: 9px;
    height: 22px;
    bottom: 0;
    left: 13px;
    transform: rotate(15deg);
    background: #4e6e34;
}

.photo-frame {
    width: 28px;
    height: 38px;
    background: #a58d6f;
    border: 3px solid #6b5a43;
    box-shadow: 1px 2px 5px rgba(0, 0, 0, 0.4);
    border-radius: 1px;
    display: flex;
    align-items: center;
    justify-content: center;
    transform: rotate(3deg);
    margin-bottom: 2px;
}

.frame-inner {
    width: 18px;
    height: 24px;
    background: linear-gradient(160deg, #d8c8a8, #b8a070);
    border-radius: 50%;
}

.small-candle {
    width: 14px;
    height: 20px;
    background: linear-gradient(180deg, #f5e6d3, #d4b68a);
    border-radius: 3px 3px 1px 1px;
    box-shadow: 0 2px 3px rgba(0, 0, 0, 0.3);
    position: relative;
}

.small-candle::after {
    content: '';
    position: absolute;
    top: -3px;
    left: 50%;
    transform: translateX(-50%);
    width: 3px;
    height: 5px;
    background: #f1c40f;
    border-radius: 1px;
}

.empty-text {
    text-align: center;
    padding: 60px;
    color: rgba(255, 255, 255, 0.15);
    font-size: 14px;
}

/* ===== 响应式 ===== */
@media (max-width: 768px) {
    .book {
        max-width: 28px;
    }

    .book-title {
        font-size: 7px;
    }

    .shelf-row {
        height: 140px;
        margin-bottom: 35px;
    }
}

@media (max-width: 480px) {
    .book {
        max-width: 22px;
    }

    .book-title {
        font-size: 6px;
    }

    .head-title {
        font-size: 26px;
    }

    .reading-page {
        padding: 0 12px 40px;
    }

    .shelf-row {
        height: 115px;
        margin-bottom: 30px;
    }
}
</style>
