<template>
  <div class="product-list">
    <div class="page-header">
      <h1>产品列表</h1>
      <el-button type="primary" @click="$router.push('/products/add')">
        <el-icon><Plus /></el-icon>
        添加产品
      </el-button>
    </div>
    
    <div class="search-bar">
      <el-input v-model="searchForm.keyword" placeholder="搜索产品名称或型号" class="search-input">
        <template #append>
          <el-button @click="handleSearch"><el-icon><Search /></el-icon></el-button>
        </template>
      </el-input>
      <el-select v-model="searchForm.category_id" placeholder="选择分类" class="search-select">
        <el-option label="全部" :value="0" />
        <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
      </el-select>
      <el-button @click="resetSearch">重置</el-button>
    </div>
    
    <el-table :data="products" border>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="title" label="产品名称" />
      <el-table-column prop="model_number" label="型号" />
      <el-table-column prop="floor_area" label="建筑面积" />
      <el-table-column prop="building_area" label="占地面积" />
      <el-table-column prop="category_name" label="分类" />
      <el-table-column prop="view_count" label="浏览量" />
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
          <el-button type="text" @click="editProduct(scope.row.id)">编辑</el-button>
          <el-button type="text" @click="deleteProduct(scope.row.id)" style="color: #E53E3E">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <el-pagination
      :current-page="pagination.page"
      :page-size="pagination.per_page"
      :total="pagination.total"
      @current-change="handlePageChange"
      layout="total, prev, pager, next, jumper"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, Search } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { productApi, categoryApi } from '../../api'

const router = useRouter()
const loading = ref(false)
const products = ref([])
const categories = ref([])
const pagination = reactive({
  page: 1,
  per_page: 10,
  total: 0
})

const searchForm = reactive({
  keyword: '',
  category_id: 0
})

const loadProducts = async () => {
  try {
    const params = {
      page: pagination.page,
      per_page: pagination.per_page,
      keyword: searchForm.keyword || undefined,
      category_id: searchForm.category_id > 0 ? searchForm.category_id : undefined
    }
    const result = await productApi.list(params)
    products.value = result.items || []
    pagination.total = result.total
    pagination.page = result.page
  } catch (error) {
    console.error('加载产品列表失败:', error)
    ElMessage.error('加载产品列表失败')
  }
}

const loadCategories = async () => {
  try {
    categories.value = await categoryApi.list()
  } catch (error) {
    console.error('加载分类失败:', error)
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadProducts()
}

const resetSearch = () => {
  searchForm.keyword = ''
  searchForm.category_id = 0
  pagination.page = 1
  loadProducts()
}

const handlePageChange = (page) => {
  pagination.page = page
  loadProducts()
}

const editProduct = (id) => {
  router.push(`/products/${id}/edit`)
}

const deleteProduct = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该产品吗？', '提示', {
      type: 'warning'
    })
    await productApi.delete(id)
    ElMessage.success('删除成功')
    loadProducts()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除产品失败:', error)
      ElMessage.error('删除产品失败')
    }
  }
}

const toggleStatus = async (id, value) => {
  try {
    await productApi.update(id, { is_active: value })
    ElMessage.success(value ? '已启用' : '已禁用')
  } catch (error) {
    console.error('更新状态失败:', error)
    ElMessage.error('更新状态失败')
    loadProducts()
  }
}

onMounted(() => {
  loadProducts()
  loadCategories()
})
</script>

<style lang="scss" scoped>
.product-list {
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

.search-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.search-input {
  width: 300px;
}

.search-select {
  width: 150px;
}

.el-pagination {
  margin-top: 24px;
  text-align: right;
}
</style>