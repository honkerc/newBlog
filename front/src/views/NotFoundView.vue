<template>
    <div class="not-found">
        <div class="nf-content">
            <h1 class="nf-code">404</h1>
            <p class="nf-text">页面不存在</p>
            <router-link to="/" class="nf-link">
                <i class="fas fa-arrow-left"></i>
                <span>返回首页</span>
            </router-link>
        </div>
    </div>
</template>

<style scoped>
.not-found {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 70vh;
    padding: 20px;
}

.nf-content {
    text-align: center;
}

.nf-code {
    font-size: 96px;
    font-weight: 800;
    background: linear-gradient(135deg, var(--theme), rgba(var(--theme-rgb), 0.4));
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    letter-spacing: -4px;
    line-height: 1;
}

.nf-text {
    font-size: 18px;
    color: var(--text-muted);
    margin-top: 12px;
    margin-bottom: 32px;
}

.nf-link {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 28px;
    border-radius: 12px;
    background: var(--theme-light);
    color: var(--theme);
    border: 1px solid var(--theme-border);
    text-decoration: none;
    font-size: 14px;
    font-weight: 600;
    transition: all var(--transition);
}

.nf-link:hover {
    background: rgba(var(--theme-rgb), 0.25);
    transform: translateY(-1px);
}
</style>
