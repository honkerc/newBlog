<template>

    <!-- 底部播放栏：左右两侧使用通用图标，中间使用标准媒体控件（上一首/播放/下一首） -->
    <div class="player-bar">
        <div class="player-progress-track">
            <div class="player-progress-fill"></div>
        </div>

        <!-- 左侧组：消息、网格、星标（无音乐含义） -->
        <div class="left-actions">
            <i class="far fa-comment-dots action-icon"></i>
            <i class="fas fa-th-large action-icon"></i>
            <i class="far fa-star action-icon"></i>
        </div>

        <!-- 中间组：原来的播放控件（step-backward / play / step-forward）不是箭头 -->
        <div class="center-playback">
            <i class="fas fa-step-backward ctrl-btn"></i>
            <div class="ctrl-btn play-btn"><i class="fas fa-play"></i></div>
            <i class="fas fa-step-forward ctrl-btn"></i>
        </div>

        <!-- 右侧组：循环、音量、列表 -->
        <div class="right-actions">
            <i class="fas fa-arrows-spin action-icon"></i>
            <div class="volume-control">
                <i class="fas fa-speaker action-icon"></i>
                <div class="volume-slider">
                    <div class="volume-fill"></div>
                </div>
            </div>
            <i class="fas fa-list-ul action-icon"></i>
        </div>
    </div>
</template>

<style scoped>
.player-bar {
    position: relative;
    background: #3F4F5C;
    backdrop-filter: blur(32px) saturate(200%);
    -webkit-backdrop-filter: blur(32px) saturate(200%);
    border-top: none;
    padding: 15px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 10;
}

/* 进度条轨道（顶部border效果） */
.player-progress-track {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: rgba(155, 184, 200, 0.3);
    pointer-events: none;
    z-index: 11;
}

.player-progress-fill {
    position: relative;
    width: 46%;
    height: 100%;
    background: rgb(155, 184, 200);
    border-radius: 0 2px 2px 0;
    box-shadow: 0 0 3px rgba(155, 184, 200, 0.5);
}

/* 白色圆点 */
.player-progress-fill::after {
    content: '';
    position: absolute;
    right: 0;
    top: 50%;
    transform: translate(50%, -50%);
    width: 10px;
    height: 10px;
    background: white;
    border-radius: 50%;
    box-shadow: 0 0 4px rgba(255, 255, 255, 0.8);
    pointer-events: none;
}

/* 左右对称控件组 ———— 严格避免无关音乐图标，但播放核心使用标准媒体控件 */
.left-actions {
    display: flex;
    align-items: center;
    gap: 24px;
    flex: 1;
}

.action-icon {
    font-size: 20px;
    color: #E0E9FF;
    cursor: default;
    transition: 0.1s;
}

.action-icon:hover {
    color: #00F2C0;
    text-shadow: 0 0 5px rgba(0, 242, 192, 0.5);
    transform: scale(1.02);
}

.center-playback {
    display: flex;
    align-items: center;
    gap: 28px;
    justify-content: center;
    flex: 1;
}

.ctrl-btn {
    background: transparent;
    border: none;
    color: #F0F5FF;
    font-size: 22px;
    cursor: default;
    transition: 0.1s;
}

.play-btn {
    background: rgb(63 79 92);
    width: 46px;
    height: 46px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
}

.play-btn:hover {
    transform: scale(1.02);
    background: #00e6b5;
}

.play-btn .fas {
    position: relative;
    left: -1px;
}

.right-actions {
    display: flex;
    align-items: center;
    gap: 24px;
    justify-content: flex-end;
    flex: 1;
}

.volume-control {
    display: flex;
    align-items: center;
    gap: 10px;
}

.volume-slider {
    width: 70px;
    height: 4px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
    position: relative;
    cursor: default;
}

.volume-fill {
    width: 65%;
    height: 100%;
    background: #00F2C0;
    border-radius: 4px;
}

@media (max-width: 900px) {
    .volume-slider {
        width: 50px;
    }

    .left-actions {
        gap: 16px;
    }

    .right-actions {
        gap: 16px;
    }
}
</style>
