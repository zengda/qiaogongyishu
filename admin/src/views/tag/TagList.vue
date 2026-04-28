<template>
  <div class="tag-list">
    <div class="page-header">
      <h1>标签管理</h1>
      <el-button type="primary" @click="$router.push('/tags/add')">
        <el-icon><Plus /></el-icon>
        添加标签
      </el-button>
    </div>
    
    <el-table :data="tags" border>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="标签名称" />
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
          <el-button type="text" @click="editTag(scope.row.id)">编辑</el-button>
          <el-button type="text" @click="deleteTag(scope.row.id)" style="color: #E53E3E">删除</el-button>
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
import { tagApi } from '../../api'

const router = useRouter()
const tags = ref([])

const loadTags = async () => {
  try {
    tags.value = await tagApi.list()
  } catch (error) {
    console.error('加载标签失败:', error)
    ElMessage.error('加载标签失败')
  }
}

const editTag = (id) => {
  router.push(`/tags/${id}/edit`)
}

const deleteTag = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该标签吗？', '提示', {
      type: 'warning'
    })
    await tagApi.delete(id)
    ElMessage.success('删除成功')
    loadTags()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除标签失败:', error)
      ElMessage.error('删除标签失败')
    }
  }
}

const toggleStatus = async (id, value) => {
  try {
    await tagApi.update(id, { is_active: value })
    ElMessage.success(value ? '已启用' : '已禁用')
  } catch (error) {
    console.error('更新状态失败:', error)
    ElMessage.error('更新状态失败')
    loadTags()
  }
}

onMounted(() => {
  loadTags()
})
</script>

<style lang="scss" scoped>
.tag-list {
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