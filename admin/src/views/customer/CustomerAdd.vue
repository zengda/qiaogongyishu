<template>
  <div class="customer-add">
    <div class="page-header">
      <h1>添加客户</h1>
      <el-button @click="$router.back()">返回</el-button>
    </div>
    
    <el-form :model="form" ref="formRef" :rules="rules" class="customer-form">
      <el-form-item label="姓名" prop="name">
        <el-input v-model="form.name" placeholder="请输入客户姓名" />
      </el-form-item>
      
      <el-form-item label="手机号" prop="phone">
        <el-input v-model="form.phone" placeholder="请输入手机号" maxlength="11" />
      </el-form-item>
      
      <el-form-item label="微信号">
        <el-input v-model="form.wechat" placeholder="请输入微信号（选填）" />
      </el-form-item>
      
      <el-form-item label="省份">
        <el-input v-model="form.province" placeholder="请输入省份" />
      </el-form-item>
      
      <el-form-item label="城市">
        <el-input v-model="form.city" placeholder="请输入城市" />
      </el-form-item>
      
      <el-form-item label="建房面积预算">
        <el-input v-model="form.building_area_budget" placeholder="请输入建房面积预算（如：200㎡）" />
      </el-form-item>
      
      <el-form-item label="意向产品">
        <el-select v-model="form.product_id" placeholder="请选择意向产品" clearable>
          <el-option v-for="product in products" :key="product.id" :label="product.title" :value="product.id" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="状态">
        <el-select v-model="form.status" placeholder="选择客户状态">
          <el-option label="新客户" value="new" />
          <el-option label="已联系" value="contacted" />
          <el-option label="跟进中" value="followed" />
          <el-option label="已成交" value="closed" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="备注">
        <el-input v-model="form.remark" type="textarea" :rows="4" placeholder="请输入备注信息（选填）" />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">保存</el-button>
        <el-button @click="$router.back()">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { customerApi, productApi } from '../../api'

const router = useRouter()
const formRef = ref(null)
const submitting = ref(false)

const products = ref([])

const form = reactive({
  name: '',
  phone: '',
  wechat: '',
  province: '',
  city: '',
  building_area_budget: '',
  product_id: '',
  product_title: '',
  status: 'new',
  remark: ''
})

const rules = {
  name: [{ required: true, message: '请输入客户姓名', trigger: 'blur' }],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
  ]
}

const loadProducts = async () => {
  try {
    const result = await productApi.list({ page: 1, per_page: 100 })
    products.value = result.items || []
  } catch (error) {
    console.error('加载产品列表失败:', error)
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    submitting.value = true
    
    const selectedProduct = products.value.find(p => p.id === form.product_id)
    
    const data = {
      name: form.name,
      phone: form.phone,
      wechat: form.wechat || undefined,
      province: form.province || undefined,
      city: form.city || undefined,
      building_area_budget: form.building_area_budget || undefined,
      product_id: form.product_id || undefined,
      product_title: selectedProduct?.title || undefined,
      status: form.status,
      remark: form.remark || undefined,
      source: '后台添加'
    }
    
    await customerApi.create(data)
    ElMessage.success('添加成功')
    router.push('/customers')
  } catch (error) {
    console.error('保存失败:', error)
    if (error !== false) {
      ElMessage.error('添加失败')
    }
  } finally {
    submitting.value = false
  }
}

loadProducts()
</script>

<style lang="scss" scoped>
.customer-add {
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

.customer-form {
  max-width: 600px;
  
  :deep(.el-textarea) {
    .el-textarea__inner {
      resize: vertical;
    }
  }
}
</style>