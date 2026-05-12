import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Post from '@/views/Post.vue'
import Moments from '@/views/MomentsView.vue'
import Articles from '@/views/ArticlesView.vue'
import Reading from '@/views/ReadingView.vue'
import BookDetail from '@/views/BookDetailView.vue'
import DailyProgress from '@/views/DailyProgressView.vue'
import Mottos from '@/views/MottosView.vue'
import Search from '@/views/SearchView.vue'
import NotFound from '@/views/NotFoundView.vue'
import Login from '@/views/LoginView.vue'
import AdminDashboard from '@/views/AdminDashboard.vue'
import AdminArticles from '@/views/AdminArticles.vue'
import AdminEditor from '@/views/AdminEditor.vue'
import AdminMoments from '@/views/AdminMoments.vue'
import AdminProfile from '@/views/AdminProfile.vue'
import AdminSettings from '@/views/AdminSettings.vue'
import AdminBooks from '@/views/AdminBooks.vue'
import AdminMottos from '@/views/AdminMottos.vue'
import AdminTools from '@/views/AdminTools.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  }, {
    path: '/post/:id',
    name: 'post',
    component: Post
  }, {
    path: '/moments',
    name: 'moments',
    component: Moments
  }, {
    path: '/articles',
    name: 'articles',
    component: Articles
  }, {
    path: '/reading',
    name: 'reading',
    component: Reading
  }, {
    path: '/reading/:tag',
    name: 'book-detail',
    component: BookDetail
  }, {
    path: '/daily',
    name: 'daily',
    component: DailyProgress
  }, {
    path: '/mottos',
    name: 'mottos',
    component: Mottos
  }, {
    path: '/search',
    name: 'search',
    component: Search
  }, {
    path: '/login',
    name: 'login',
    component: Login
  }, {
    path: '/admin',
    name: 'admin-dashboard',
    component: AdminDashboard
  }, {
    path: '/admin/articles',
    name: 'admin-articles',
    component: AdminArticles
  }, {
    path: '/admin/editor',
    name: 'admin-editor',
    component: AdminEditor
  }, {
    path: '/admin/moments',
    name: 'admin-moments',
    component: AdminMoments
  }, {
    path: '/admin/profile',
    name: 'admin-profile',
    component: AdminProfile
  }, {
    path: '/admin/books',
    name: 'admin-books',
    component: AdminBooks
  }, {
    path: '/admin/books/add',
    name: 'admin-books-add',
    component: AdminBooks
  }, {
    path: '/admin/mottos',
    name: 'admin-mottos',
    component: AdminMottos
  }, {
    path: '/admin/settings',
    name: 'admin-settings',
    component: AdminSettings
  }, {
    path: '/admin/tools',
    name: 'admin-tools',
    component: AdminTools
  }, {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFound
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
