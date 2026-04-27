<template>
  <div class="tag-add">
    <div class="page-header">
      <h1>添加标签</h1>
      <el-button @click="$router.back()">返回</el-button>
    </div>
    
    <el-form :model="form" ref="formRef" :rules="rules" class="tag-form">
      <el-form-item label="标签名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入标签名称" />
      </el-form-item>
      
      <el-form-item label="排序">
        <el-input-number v-model="form.sort_order" :min="0" :max="100" />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="handleSubmit">保存</el-button>
        <el-button @click="$router.back()">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { tagApi } from '../../api'

const formRef = ref(null)

const form = reactive({
  name: '',
  sort_order: 0
})

const rules = {
  name: [{ required: true, message: '请输入标签名称', trigger: 'blur' }]
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    await tagApi.create(form)
    window.location.href = '/tags'
  } catch (error) {
    console.error('保存失败:', error)
  }
}
</script>

<style lang="scss" scoped>
.tag-add {
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

.tag-form {
  max-width: 400px;
}
</style>