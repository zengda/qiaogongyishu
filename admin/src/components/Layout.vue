<template>
  <div class="layout-container">
    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="sidebar-header">
        <div class="logo" v-if="!sidebarCollapsed">
          <span class="logo-icon">🏠</span>
          <span class="logo-text">巧工艺墅</span>
        </div>
        <div class="logo collapsed-logo" v-else>
          <span class="logo-icon">🏠</span>
        </div>
      </div>
      <nav class="sidebar-nav">
        <el-menu
          :default-active="activeMenu"
          :router="true"
          mode="vertical"
          background-color="#2D3748"
          text-color="#CBD5E0"
          active-text-color="#fff"
        >
          <el-menu-item index="/dashboard">
            <el-icon><component :is="icons.Dashboard" /></el-icon>
            <span>{{ sidebarCollapsed ? '' : '仪表盘' }}</span>
          </el-menu-item>
          <el-sub-menu index="/products">
            <template #title>
              <el-icon><component :is="icons.Box" /></el-icon>
              <span>{{ sidebarCollapsed ? '' : '产品管理' }}</span>
            </template>
            <el-menu-item index="/products">{{ sidebarCollapsed ? '' : '产品列表' }}</el-menu-item>
            <el-menu-item index="/products/add">{{ sidebarCollapsed ? '' : '添加产品' }}</el-menu-item>
          </el-sub-menu>
          <el-sub-menu index="/categories">
            <template #title>
              <el-icon><component :is="icons.List" /></el-icon>
              <span>{{ sidebarCollapsed ? '' : '分类管理' }}</span>
            </template>
            <el-menu-item index="/categories">{{ sidebarCollapsed ? '' : '分类列表' }}</el-menu-item>
            <el-menu-item index="/categories/add">{{ sidebarCollapsed ? '' : '添加分类' }}</el-menu-item>
          </el-sub-menu>
          <el-sub-menu index="/tags">
            <template #title>
              <el-icon><component :is="icons.Tag" /></el-icon>
              <span>{{ sidebarCollapsed ? '' : '标签管理' }}</span>
            </template>
            <el-menu-item index="/tags">{{ sidebarCollapsed ? '' : '标签列表' }}</el-menu-item>
            <el-menu-item index="/tags/add">{{ sidebarCollapsed ? '' : '添加标签' }}</el-menu-item>
          </el-sub-menu>
          <el-sub-menu index="/banners">
            <template #title>
              <el-icon><component :is="icons.Image" /></el-icon>
              <span>{{ sidebarCollapsed ? '' : 'Banner管理' }}</span>
            </template>
            <el-menu-item index="/banners">{{ sidebarCollapsed ? '' : 'Banner列表' }}</el-menu-item>
            <el-menu-item index="/banners/add">{{ sidebarCollapsed ? '' : '添加Banner' }}</el-menu-item>
          </el-sub-menu>
          <el-menu-item index="/customers">
            <el-icon><component :is="icons.User" /></el-icon>
            <span>{{ sidebarCollapsed ? '' : '客户管理' }}</span>
          </el-menu-item>
          <el-sub-menu index="/settings">
            <template #title>
              <el-icon><component :is="icons.Setting" /></el-icon>
              <span>{{ sidebarCollapsed ? '' : '系统设置' }}</span>
            </template>
            <el-menu-item index="/settings/storage">{{ sidebarCollapsed ? '' : '存储配置' }}</el-menu-item>
            <el-menu-item index="/settings/customer-service">{{ sidebarCollapsed ? '' : '客服二维码设置' }}</el-menu-item>
            <el-menu-item index="/settings/change-password">{{ sidebarCollapsed ? '' : '修改密码' }}</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </nav>
    </aside>
    <main class="main-content">
      <header class="top-bar">
        <button class="toggle-btn" @click="toggleSidebar">
          <el-icon><component :is="icons.Menu" /></el-icon>
        </button>
        <div class="top-bar-right">
          <span class="welcome-text">欢迎, {{ user?.username || '管理员' }}</span>
          <button class="logout-btn" @click="handleLogout">
            <el-icon><component :is="icons.Logout" /></el-icon>
            <span>退出</span>
          </button>
        </div>
      </header>
      <div class="content-wrapper">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { Grid, Box, List, PriceTag, Picture, User, Setting, Menu, Close } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const store = useStore()

const icons = { Dashboard: Grid, Box, List, Tag: PriceTag, Image: Picture, User, Setting, Menu, Logout: Close }

const activeMenu = computed(() => {
  return route.path
})

const sidebarCollapsed = computed(() => store.getters.sidebarCollapsed)
const user = computed(() => store.getters.user)

const toggleSidebar = () => {
  store.dispatch('toggleSidebar')
}

const handleLogout = () => {
  store.dispatch('logout')
  router.push('/login')
}
</script>

<style lang="scss" scoped>
.layout-container {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 220px;
  background-color: #2D3748;
  color: #fff;
  transition: width 0.3s;
  
  &.collapsed {
    width: 64px;
  }
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #4A5568;
}

.logo {
  display: flex;
  align-items: center;
  
  &.collapsed-logo {
    justify-content: center;
  }
}

.logo-icon {
  font-size: 28px;
}

.logo-text {
  margin-left: 12px;
  font-size: 18px;
  font-weight: 600;
}

.sidebar-nav {
  padding-top: 20px;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.toggle-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  
  &:hover {
    background-color: #f5f7fa;
  }
}

.top-bar-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.welcome-text {
  font-size: 14px;
  color: #666;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background-color: #fff;
  border: 1px solid #E53E3E;
  color: #E53E3E;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  
  &:hover {
    background-color: #FEF2F2;
  }
}

.content-wrapper {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  background-color: #f5f7fa;
}
</style>