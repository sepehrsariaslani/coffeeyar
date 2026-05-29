import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import {
  HomePage,
  CategoryPage,
  ProductPage,
  AboutPage,
  ShowroomPage,
  CheckoutPage,
  PaymentCallbackPage,
  BlogListPage,
  BlogPostPage,
} from './pages'
import './styles.css'

if (typeof document !== 'undefined') {
  document.documentElement.setAttribute('lang', 'fa')
  document.documentElement.setAttribute('dir', 'rtl')
}

const routes = [
  { path: '/', component: HomePage },
  { path: '/all-products', component: CategoryPage, props: { categorySlug: '' } },
  { path: '/category/:categorySlug', component: CategoryPage, props: true },
  { path: '/about-us', component: AboutPage },
  { path: '/showroom', component: ShowroomPage },
  { path: '/blog', component: BlogListPage },
  { path: '/blog/:slug', component: BlogPostPage, props: true },
  { path: '/checkout', component: CheckoutPage },
  { path: '/payment/callback', component: PaymentCallbackPage },
  { path: '/product/:slug', component: ProductPage, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

createApp(App).use(router).mount('#app')
