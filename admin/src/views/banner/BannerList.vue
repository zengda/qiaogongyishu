<template>
  <div class="banner-list">
    <div class="page-header">
      <h1>Banner管理</h1>
      <el-button type="primary" @click="$router.push('/banners/add')">
        <el-icon><Plus /></el-icon>
        添加Banner
      </el-button>
    </div>
    
    <el-table :data="banners" border>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column label="图片" width="150">
        <template #default="scope">
          <img :src="scope.row.image_url" class="banner-thumb" />
        </template>
      </el-table-column>
      <el-table-column prop="link_type" label="链接类型">
        <template #default="scope">
          <span>{{ scope.row.link_type === 'product' ? '产品' : '外部链接' }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="link_value" label="链接值" />
      <el-table-column prop="sort_order" label="排序" />
      <el-table-column prop="status" label="状态">
        <template #default="scope">
          <el-switch :value="scope.row.status === 'active'" @change="toggleStatus(scope.row.id, $event)" />
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button type="text" @click="editBanner(scope.row.id)">编辑</el-button>
          <el-button type="text" @click="deleteBanner(scope.row.id)" style="color: #E53E3E">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { bannerApi } from '../../api'

const banners = ref([])

const loadBanners = async () => {
  try {
    banners.value = await bannerApi.list()
  } catch (error) {
    console.error('加载Banner失败:', error)
  }
}

const editBanner = (id) => {
  window.location.href = `/banners/${id}/edit`
}

const deleteBanner = async (id) => {
  try {
    await bannerApi.delete(id)
    loadBanners()
  } catch (error) {
    console.error('删除Banner失败:', error)
  }
}

const toggleStatus = async (id, value) => {
  try {
    await bannerApi.update(id, { status: value ? 'active' : 'inactive' })
  } catch (error) {
    console.error('更新状态失败:', error)
    loadBanners()
  }
}

onMounted(() => {
  loadBanners()
})
</script>

<style lang="scss" scoped>
.banner-list {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
  }
  
  h1 {
    font-size: 24px;
    font-weight: 600;
    color: #333;
  }
}

.banner-thumb {
  width: 100px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}
</style>