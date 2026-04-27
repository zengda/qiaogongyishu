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
          <div class="stat-label">客户数量</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon view-icon">👁</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.viewCount || 0 }}</div>
          <div class="stat-label">总浏览量</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon banner-icon">🎯</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.bannerCount || 0 }}</div>
          <div class="stat-label">Banner数量</div>
        </div>
      </div>
    </div>
    
    <div class="charts-section">
      <div class="chart-card">
        <h3>客户趋势</h3>
        <div ref="customerChart" class="chart-container"></div>
      </div>
      <div class="chart-card">
        <h3>产品分类统计</h3>
        <div ref="categoryChart" class="chart-container"></div>
      </div>
    </div>
    
    <div class="recent-customers">
      <h3>最近客户</h3>
      <el-table :data="recentCustomers" border>
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="phone" label="手机号" />
        <el-table-column prop="created_at" label="创建时间" />
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">{{ getStatusText(scope.row.status) }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import { dashboardApi, customerApi } from '../../api'

const stats = ref({})
const recentCustomers = ref([])
const customerChart = ref(null)
const categoryChart = ref(null)

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
    stats.value = await dashboardApi.stats()
    initCharts()
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

const loadRecentCustomers = async () => {
  try {
    const result = await customerApi.list({ page: 1, per_page: 5 })
    recentCustomers.value = result.items || []
  } catch (error) {
    console.error('加载客户列表失败:', error)
  }
}

const initCharts = () => {
  if (customerChart.value) {
    const chart = echarts.init(customerChart.value)
    chart.setOption({
      xAxis: {
        type: 'category',
        data: ['1月', '2月', '3月', '4月', '5月', '6月']
      },
      yAxis: {
        type: 'value'
      },
      series: [{
        data: [120, 200, 150, 250, 180, 300],
        type: 'line',
        smooth: true,
        areaStyle: {
          color: 'rgba(26, 109, 92, 0.1)'
        },
        lineStyle: {
          color: '#1A6D5C'
        }
      }]
    })
  }
  
  if (categoryChart.value) {
    const chart = echarts.init(categoryChart.value)
    chart.setOption({
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        data: [
          { value: 30, name: '一层' },
          { value: 25, name: '二层' },
          { value: 20, name: '三层' },
          { value: 15, name: '多层' },
          { value: 10, name: '双拼' }
        ],
        color: ['#1A6D5C', '#2D3748', '#F5A623', '#E53E3E', '#63B3ED']
      }]
    })
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
  margin-bottom: 24px;
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
  &.view-icon { background: rgba(245, 166, 35, 0.1); }
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

.charts-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.chart-card {
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

.chart-container {
  height: 300px;
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
</style>