import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/login/Login.vue')
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('../components/Layout.vue'),
    redirect: '/dashboard',
    children: [
      { path: '/dashboard', name: 'Dashboard', component: () => import('../views/dashboard/Dashboard.vue') },
      { path: '/products', name: 'ProductList', component: () => import('../views/product/ProductList.vue') },
      { path: '/products/add', name: 'ProductAdd', component: () => import('../views/product/ProductAdd.vue') },
      { path: '/products/:id/edit', name: 'ProductEdit', component: () => import('../views/product/ProductEdit.vue') },
      { path: '/categories', name: 'CategoryList', component: () => import('../views/category/CategoryList.vue') },
      { path: '/categories/add', name: 'CategoryAdd', component: () => import('../views/category/CategoryAdd.vue') },
      { path: '/categories/:id/edit', name: 'CategoryEdit', component: () => import('../views/category/CategoryEdit.vue') },
      { path: '/tags', name: 'TagList', component: () => import('../views/tag/TagList.vue') },
      { path: '/tags/add', name: 'TagAdd', component: () => import('../views/tag/TagAdd.vue') },
      { path: '/tags/:id/edit', name: 'TagEdit', component: () => import('../views/tag/TagEdit.vue') },
      { path: '/banners', name: 'BannerList', component: () => import('../views/banner/BannerList.vue') },
      { path: '/banners/add', name: 'BannerAdd', component: () => import('../views/banner/BannerAdd.vue') },
      { path: '/banners/:id/edit', name: 'BannerEdit', component: () => import('../views/banner/BannerEdit.vue') },
      { path: '/customers', name: 'CustomerList', component: () => import('../views/customer/CustomerList.vue') },
      { path: '/customers/add', name: 'CustomerAdd', component: () => import('../views/customer/CustomerAdd.vue') },
      { path: '/customers/:id', name: 'CustomerDetail', component: () => import('../views/customer/CustomerDetail.vue') },
      { path: '/settings/storage', name: 'StorageConfig', component: () => import('../views/settings/StorageConfig.vue') },
      { path: '/settings/customer-service', name: 'CustomerService', component: () => import('../views/settings/CustomerService.vue') },
      { path: '/settings/miniprogram', name: 'MiniprogramConfig', component: () => import('../views/settings/MiniProgramConfig.vue') },
      { path: '/settings/change-password', name: 'ChangePassword', component: () => import('../views/settings/ChangePassword.vue') }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, _from, next) => {
  if (to.path !== '/login') {
    const token = store.getters.token || localStorage.getItem('admin_token')
    if (!token) {
      next('/login')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router