<template>
    <div class="greeting">
        <h2>标准控件 · 左右对称 ✨</h2>
        <p>播放核心使用原有媒体图标，其他区域为通用符号</p>
    </div>
    <div class="section-title">
        <h3>推荐内容 · 精选卡片</h3><span>查看全部 <i class="fas fa-chevron-right"></i></span>
    </div>
    <div class="card-grid">
        <div class="music-card">
            <div class="card-img"><img src="https://picsum.photos/id/106/200/200" alt="cover"></div>
            <h4>活力节奏包</h4>
            <p>能量满满 · 唤醒一天</p>
        </div>
        <div class="music-card">
            <div class="card-img"><img src="https://picsum.photos/id/169/200/200" alt="cover"></div>
            <h4>氛围感选集</h4>
            <p>慵懒午后灵感</p>
        </div>
        <div class="music-card">
            <div class="card-img"><img src="https://picsum.photos/id/20/200/200" alt="cover"></div>
            <h4>夏日限定</h4>
            <p>清爽气泡感</p>
        </div>
        <div class="music-card">
            <div class="card-img"><img src="https://picsum.photos/id/145/200/200" alt="cover"></div>
            <h4>独立新声</h4>
            <p>宝藏原创精选</p>
        </div>
    </div>
    <div class="section-title">
        <h3>趋势榜 · 本周热门</h3><span><i class="fas fa-arrow-right"></i> 更多</span>
    </div>
    <div class="song-list">
        <div class="song-item">
            <div class="song-index">01</div>
            <div class="song-cover"><img src="https://picsum.photos/id/155/60/60" alt="thumb"></div>
            <div class="song-name">云端漫步</div>
            <div class="song-artist">橘子海</div>
            <div class="song-play"><i class="fas fa-play-circle"></i></div>
        </div>
        <div class="song-item">
            <div class="song-index">02</div>
            <div class="song-cover"><img src="https://picsum.photos/id/22/60/60" alt="thumb"></div>
            <div class="song-name">霓虹甜心</div>
            <div class="song-artist">马赛克</div>
            <div class="song-play"><i class="fas fa-play-circle"></i></div>
        </div>
        <div class="song-item">
            <div class="song-index">03</div>
            <div class="song-cover"><img src="https://picsum.photos/id/96/60/60" alt="thumb"></div>
            <div class="song-name">月光快车</div>
            <div class="song-artist">钱润玉</div>
            <div class="song-play"><i class="fas fa-play-circle"></i></div>
        </div>
        <div class="song-item">
            <div class="song-index">04</div>
            <div class="song-cover"><img src="https://picsum.photos/id/29/60/60" alt="thumb"></div>
            <div class="song-name">银河汽水</div>
            <div class="song-artist">告五人</div>
            <div class="song-play"><i class="fas fa-play-circle"></i></div>
        </div>
        <div class="song-item">
            <div class="song-index">05</div>
            <div class="song-cover"><img src="https://picsum.photos/id/107/60/60" alt="thumb"></div>
            <div class="song-name">蓝色浪潮</div>
            <div class="song-artist">夏日入侵</div>
            <div class="song-play"><i class="fas fa-play-circle"></i></div>
        </div>
    </div>
</template>

<style scoped>
.greeting h2 {
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.3px;
    text-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.greeting p {
    color: #F0F4FF;
    margin-top: 6px;
    font-size: 14px;
    opacity: 0.92;
}

.section-title {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin: 32px 0 18px 0;
}

.section-title h3 {
    font-size: 20px;
    font-weight: 700;
}

.section-title span {
    font-size: 13px;
    color: #C8FCEB;
    cursor: default;
    background: rgba(0, 0, 0, 0.25);
    padding: 4px 14px;
    border-radius: 40px;
    backdrop-filter: blur(4px);
}

.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 18px;
}

.music-card {
    background: rgba(20, 28, 40, 0.6);
    backdrop-filter: blur(4px);
    border-radius: 24px;
    padding: 16px 12px 14px;
    transition: 0.25s;
    border: 1px solid rgba(255, 255, 255, 0.15);
    cursor: default;
}

.music-card:hover {
    background: rgba(38, 48, 62, 0.85);
    transform: translateY(-5px);
    border-color: rgba(0, 242, 192, 0.5);
}

.card-img {
    width: 100%;
    aspect-ratio: 1;
    border-radius: 18px;
    background: #1C212F;
    overflow: hidden;
    box-shadow: 0 6px 12px -4px rgba(0, 0, 0, 0.3);
}

.card-img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.music-card h4 {
    margin-top: 14px;
    font-size: 15px;
    font-weight: 600;
}

.music-card p {
    font-size: 12px;
    color: #C8D4F0;
    margin-top: 4px;
}

.song-list {
    background: rgba(0, 0, 0, 0.25);
    backdrop-filter: blur(12px);
    border-radius: 28px;
    overflow: hidden;
    margin-top: 16px;
    border: 1px solid rgba(255, 255, 255, 0.12);
}

.song-item {
    display: grid;
    grid-template-columns: 40px 60px 1fr 1fr 50px;
    align-items: center;
    padding: 12px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    cursor: default;
}

.song-item:hover {
    background: rgba(0, 242, 192, 0.12);
}

.song-index {
    color: #D6E0FF;
    font-weight: 500;
}

.song-cover {
    width: 46px;
    height: 46px;
    border-radius: 12px;
    background: #2A2F3E;
    overflow: hidden;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.song-cover img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.song-name {
    font-weight: 600;
}

.song-artist {
    color: #D0DBF5;
    font-size: 13px;
}

.song-play i {
    color: #00F2C0;
    font-size: 20px;
    opacity: 0.9;
    transition: 0.1s;
}

.song-play i:hover {
    opacity: 1;
    transform: scale(1.03);
    cursor: default;
}
</style>
