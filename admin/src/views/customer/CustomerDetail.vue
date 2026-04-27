<template>
  <div class="customer-detail">
    <div class="page-header">
      <h1>客户详情</h1>
      <el-button @click="$router.back()">返回</el-button>
    </div>
    
    <div class="detail-card" v-if="customer">
      <div class="detail-row">
        <span class="label">姓名</span>
        <span class="value">{{ customer.name }}</span>
      </div>
      <div class="detail-row">
        <span class="label">手机号</span>
        <span class="value">{{ customer.phone }}</span>
      </div>
      <div class="detail-row">
        <span class="label">微信号</span>
        <span class="value">{{ customer.wechat || '-' }}</span>
      </div>
      <div class="detail-row">
        <span class="label">省份</span>
        <span class="value">{{ customer.province || '-' }}</span>
      </div>
      <div class="detail-row">
        <span class="label">城市</span>
        <span class="value">{{ customer.city || '-' }}</span>
      </div>
      <div class="detail-row">
        <span class="label">建房面积预算</span>
        <span class="value">{{ customer.building_area_budget || '-' }}</span>
      </div>
      <div class="detail-row">
        <span class="label">意向产品</span>
        <span class="value">{{ customer.product_title || '-' }}</span>
      </div>
      <div class="detail-row">
        <span class="label">状态</span>
        <el-tag :type="getStatusType(customer.status)">{{ getStatusText(customer.status) }}</el-tag>
      </div>
      <div class="detail-row">
        <span class="label">创建时间</span>
        <span class="value">{{ customer.created_at }}</span>
      </div>
    </div>
    
    <div class="action-section">
      <el-select v-model="status" placeholder="选择状态">
        <el-option label="新客户" value="new" />
        <el-option label="已联系" value="contacted" />
        <el-option label="跟进中" value="followed" />
        <el-option label="已成交" value="closed" />
      </el-select>
      <el-button type="primary" @click="handleUpdateStatus">更新状态</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { customerApi } from '../../api'

const route = useRoute()
const customer = ref(null)
const status = ref('')

const statusMap = {
  new: { text: '新客户', type: 'primary' },
  contacted: { text: '已联系', type: 'success' },
  followed: { text: '跟进中', type: 'warning' },
  closed: { text: '已成交', type: 'info' }
}

const getStatusText = (status) => statusMap[status]?.text || status
const getStatusType = (status) => statusMap[status]?.type || 'default'

const loadCustomer = async () => {
  try {
    customer.value = await customerApi.get(route.params.id)
    status.value = customer.value.status
  } catch (error) {
    console.error('加载客户详情失败:', error)
  }
}

const handleUpdateStatus = async () => {
  try {
    await customerApi.update(route.params.id, { status: status.value })
    customer.value.status = status.value
  } catch (error) {
    console.error('更新状态失败:', error)
  }
}

onMounted(() => {
  loadCustomer()
})
</script>

<style lang="scss" scoped>
.customer-detail {
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

.detail-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.detail-row {
  display: flex;
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
  
  &:last-child {
    border-bottom: none;
  }
}

.label {
  width: 120px;
  color: #999;
  font-size: 14px;
}

.value {
  flex: 1;
  color: #333;
  font-size: 14px;
}

.action-section {
  margin-top: 24px;
  display: flex;
  gap: 16px;
  
  .el-select {
    width: 200px;
  }
}
</style>