<template>
  <div class="dashboard">
    <div class="page-header">
      <h1>仪表盘</h1>
      <p>欢迎回来，这是您的数据概览</p>
    </div>
    
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon product-icon">📦</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.productCount || 0 }}</div>
          <div class="stat-label">产品总数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon customer-icon">👥</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.customerCount || 0 }}</div>
          <div class="stat-label">客户总量</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon new-customer-icon">🆕</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.customerToday || 0 }}</div>
          <div class="stat-label">今日新增</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon banner-icon">🎯</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.bannerCount || 0 }}</div>
          <div class="stat-label">活跃Banner</div>
        </div>
      </div>
    </div>
    
    <div class="stats-row">
      <div class="mini-stat-card">
        <div class="mini-stat-value">{{ stats.customerWeek || 0 }}</div>
        <div class="mini-stat-label">本周客户</div>
      </div>
      <div class="mini-stat-card">
        <div class="mini-stat-value">{{ stats.customerMonth || 0 }}</div>
        <div class="mini-stat-label">本月客户</div>
      </div>
    </div>
    
    <div class="recent-customers">
      <h3>最近客户</h3>
      <el-table :data="recentCustomers" border v-if="recentCustomers.length > 0">
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="phone" label="手机号" />
        <el-table-column prop="province" label="省份">
          <template #default="scope">
            {{ scope.row.province || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="product_title" label="意向产品">
          <template #default="scope">
            {{ scope.row.product_title || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="提交时间" />
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">{{ getStatusText(scope.row.status) }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
      <div v-else class="empty-state">
        <p>暂无客户数据</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { dashboardApi, customerApi } from '../../api'

const stats = ref({
  productCount: 0,
  customerCount: 0,
  customerToday: 0,
  customerWeek: 0,
  customerMonth: 0,
  viewCount: 0,
  bannerCount: 0
})
const recentCustomers = ref([])

const statusMap = {
  new: { text: '新客户', type: 'primary' },
  contacted: { text: '已联系', type: 'success' },
  followed: { text: '跟进中', type: 'warning' },
  closed: { text: '已成交', type: 'info' }
}

const getStatusText = (status) => statusMap[status]?.text || status
const getStatusType = (status) => statusMap[status]?.type || 'default'

const loadStats = async () => {
  try {
    const result = await dashboardApi.stats()
    stats.value = result || {}
  } catch (error) {
    console.error('加载统计数据失败:', error)
    const errorMsg = error?.response?.data?.message || error?.message || '加载统计数据失败'
    ElMessage.error(errorMsg)
  }
}

const loadRecentCustomers = async () => {
  try {
    const result = await customerApi.list({ page: 1, per_page: 10 })
    recentCustomers.value = result.items || []
  } catch (error) {
    console.error('加载客户列表失败:', error)
  }
}

onMounted(() => {
  loadStats()
  loadRecentCustomers()
})
</script>

<style lang="scss" scoped>
.dashboard {
  .page-header {
    margin-bottom: 24px;
  }
  
  h1 {
    font-size: 24px;
    font-weight: 600;
    color: #333;
  }
  
  p {
    color: #999;
    margin-top: 8px;
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  background: #fff;
  padding: 24px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  
  &.product-icon { background: rgba(26, 109, 92, 0.1); }
  &.customer-icon { background: rgba(99, 179, 237, 0.1); }
  &.new-customer-icon { background: rgba(72, 187, 120, 0.1); }
  &.banner-icon { background: rgba(229, 62, 62, 0.1); }
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 600;
  color: #333;
}

.stat-label {
  font-size: 14px;
  color: #999;
  margin-top: 4px;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.mini-stat-card {
  background: #fff;
  padding: 20px 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.mini-stat-value {
  font-size: 28px;
  font-weight: 600;
  color: #333;
}

.mini-stat-label {
  font-size: 14px;
  color: #999;
}

.recent-customers {
  background: #fff;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  
  h3 {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 20px;
    color: #333;
  }
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #999;
}
</style>