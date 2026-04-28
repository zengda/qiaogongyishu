<template>
  <div class="category-list">
    <div class="page-header">
      <h1>分类管理</h1>
      <el-button type="primary" @click="$router.push('/categories/add')">
        <el-icon><Plus /></el-icon>
        添加分类
      </el-button>
    </div>
    
    <el-table :data="categories" border>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="分类名称" />
      <el-table-column prop="sort_order" label="排序" />
      <el-table-column prop="is_active" label="状态">
        <template #default="scope">
          <el-tag :type="scope.row.is_active ? 'success' : 'info'">
            {{ scope.row.is_active ? '启用' : '禁用' }}
          </el-tag>
          <el-switch 
            v-model="scope.row.is_active" 
            style="margin-left: 8px"
            @change="toggleStatus(scope.row.id, $event)" 
          />
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button type="text" @click="editCategory(scope.row.id)">编辑</el-button>
          <el-button type="text" @click="deleteCategory(scope.row.id)" style="color: #E53E3E">删除</el-button>
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
import { categoryApi } from '../../api'

const router = useRouter()
const categories = ref([])

const loadCategories = async () => {
  try {
    categories.value = await categoryApi.list()
  } catch (error) {
    console.error('加载分类失败:', error)
    ElMessage.error('加载分类失败')
  }
}

const editCategory = (id) => {
  router.push(`/categories/${id}/edit`)
}

const deleteCategory = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该分类吗？', '提示', {
      type: 'warning'
    })
    await categoryApi.delete(id)
    ElMessage.success('删除成功')
    loadCategories()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除分类失败:', error)
      ElMessage.error('删除分类失败')
    }
  }
}

const toggleStatus = async (id, value) => {
  try {
    await categoryApi.update(id, { is_active: value })
    ElMessage.success(value ? '已启用' : '已禁用')
  } catch (error) {
    console.error('更新状态失败:', error)
    ElMessage.error('更新状态失败')
    loadCategories()
  }
}

onMounted(() => {
  loadCategories()
})
</script>

<style lang="scss" scoped>
.category-list {
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
</style>