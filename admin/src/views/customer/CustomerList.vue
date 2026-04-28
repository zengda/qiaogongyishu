<template>
  <div class="customer-list">
    <div class="page-header">
      <h1>客户管理</h1>
      <el-button type="primary" @click="handleExport">
        <el-icon><Download /></el-icon>
        导出客户
      </el-button>
    </div>
    
    <div class="search-bar">
      <el-input v-model="searchForm.keyword" placeholder="搜索客户姓名或手机号" class="search-input">
        <template #append>
          <el-button @click="handleSearch"><el-icon><Search /></el-icon></el-button>
        </template>
      </el-input>
      <el-select v-model="searchForm.status" placeholder="选择状态" class="search-select">
        <el-option label="全部" :value="''" />
        <el-option label="新客户" :value="'new'" />
        <el-option label="已联系" :value="'contacted'" />
        <el-option label="跟进中" :value="'followed'" />
        <el-option label="已成交" :value="'closed'" />
      </el-select>
      <el-button @click="resetSearch">重置</el-button>
    </div>
    
    <el-table :data="customers" border>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="phone" label="手机号" />
      <el-table-column prop="wechat" label="微信号" />
      <el-table-column prop="province" label="省份" />
      <el-table-column prop="city" label="城市" />
      <el-table-column prop="building_area_budget" label="建房面积预算" />
      <el-table-column prop="product_title" label="意向产品" />
      <el-table-column prop="status" label="状态">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)">{{ getStatusText(scope.row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" />
      <el-table-column label="操作" width="180">
        <template #default="scope">
          <el-button type="text" @click="viewCustomer(scope.row.id)">查看</el-button>
          <el-button type="text" @click="deleteCustomer(scope.row.id)" style="color: #E53E3E">删除</el-button>
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
import { Search, Download } from '@element-plus/icons-vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { customerApi } from '../../api'

const router = useRouter()
const customers = ref([])
const pagination = reactive({
  page: 1,
  per_page: 10,
  total: 0
})

const searchForm = reactive({
  keyword: '',
  status: ''
})

const statusMap = {
  new: { text: '新客户', type: 'primary' },
  contacted: { text: '已联系', type: 'success' },
  followed: { text: '跟进中', type: 'warning' },
  closed: { text: '已成交', type: 'info' }
}

const getStatusText = (status) => statusMap[status]?.text || status
const getStatusType = (status) => statusMap[status]?.type || 'default'

const loadCustomers = async () => {
  try {
    const params = {
      page: pagination.page,
      per_page: pagination.per_page,
      keyword: searchForm.keyword || undefined,
      status: searchForm.status || undefined
    }
    const result = await customerApi.list(params)
    customers.value = result.items || []
    pagination.total = result.total
    pagination.page = result.page
  } catch (error) {
    console.error('加载客户列表失败:', error)
    ElMessage.error('加载客户列表失败')
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadCustomers()
}

const resetSearch = () => {
  searchForm.keyword = ''
  searchForm.status = ''
  pagination.page = 1
  loadCustomers()
}

const handlePageChange = (page) => {
  pagination.page = page
  loadCustomers()
}

const viewCustomer = (id) => {
  router.push(`/customers/${id}`)
}

const deleteCustomer = async (id) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除该客户吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await customerApi.delete(id)
    ElMessage.success('删除成功')
    loadCustomers()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除客户失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

const handleExport = async () => {
  try {
    const response = await customerApi.export()
    const blob = new Blob([response], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = '客户列表.xlsx'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败')
  }
}

onMounted(() => {
  loadCustomers()
})
</script>

<style lang="scss" scoped>
.customer-list {
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
