import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/post.css'
import './assets/themes.css'
import 'highlight.js/styles/atom-one-dark.css'

// 初始化主题
const savedTheme = localStorage.getItem('blog_theme') || 'jade'
document.documentElement.setAttribute('data-theme', savedTheme)

createApp(App).use(router).mount('#app')
