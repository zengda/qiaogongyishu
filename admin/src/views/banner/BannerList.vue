<template>
  <div class="banner-list">
    <div class="page-header">
      <h1>Banner管理</h1>
      <el-button type="primary" @click="goToAdd">
        <el-icon><Plus /></el-icon>
        添加Banner
      </el-button>
    </div>
    
    <el-table :data="banners" border v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column label="图片" width="150">
        <template #default="scope">
          <img :src="scope.row.image_url" class="banner-thumb" />
        </template>
      </el-table-column>
      <el-table-column prop="link_type" label="链接类型">
        <template #default="scope">
          <span>{{ getLinkTypeText(scope.row.link_type) }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="link_value" label="链接值" />
      <el-table-column prop="sort_order" label="排序" />
      <el-table-column prop="is_active" label="状态">
        <template #default="scope">
          <el-switch :model-value="scope.row.is_active" @change="toggleStatus(scope.row.id, $event)" />
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
import { useRouter } from 'vue-router'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { bannerApi } from '../../api'

const router = useRouter()
const loading = ref(false)
const banners = ref([])

const getLinkTypeText = (linkType) => {
  const map = {
    'none': '无链接',
    'product': '产品链接',
    'external': '外部链接'
  }
  return map[linkType] || linkType
}

const loadBanners = async () => {
  loading.value = true
  try {
    const result = await bannerApi.list()
    banners.value = result || []
  } catch (error) {
    console.error('加载Banner失败:', error)
    const errorMsg = error?.response?.data?.message || error?.message || '加载Banner失败'
    ElMessage.error(errorMsg)
  } finally {
    loading.value = false
  }
}

const goToAdd = () => {
  router.push('/banners/add')
}

const editBanner = (id) => {
  router.push(`/banners/${id}/edit`)
}

const deleteBanner = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该Banner吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await bannerApi.delete(id)
    ElMessage.success('删除成功')
    loadBanners()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除Banner失败:', error)
      const errorMsg = error?.response?.data?.message || error?.message || '删除失败'
      ElMessage.error(errorMsg)
    }
  }
}

const toggleStatus = async (id, value) => {
  try {
    await bannerApi.update(id, { is_active: value })
    ElMessage.success(value ? '已启用' : '已禁用')
    loadBanners()
  } catch (error) {
    console.error('更新状态失败:', error)
    ElMessage.error('更新状态失败')
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