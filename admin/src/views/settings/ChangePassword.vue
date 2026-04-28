<template>
  <div class="change-password">
    <div class="page-header">
      <h1>修改密码</h1>
    </div>
    
    <el-form :model="form" :rules="rules" ref="formRef" label-width="120px" class="password-form">
      <el-form-item label="当前密码" prop="old_password">
        <el-input v-model="form.old_password" type="password" placeholder="请输入当前密码" />
      </el-form-item>
      
      <el-form-item label="新密码" prop="new_password">
        <el-input v-model="form.new_password" type="password" placeholder="请输入新密码" />
      </el-form-item>
      
      <el-form-item label="确认密码" prop="confirm_password">
        <el-input v-model="form.confirm_password" type="password" placeholder="请再次输入新密码" />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="handleSubmit">确认修改</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const formRef = ref(null)

const form = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== form.new_password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  old_password: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 位', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    
    const response = await fetch('/api/v1/admin/profile/password', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('admin_token')}`
      },
      body: JSON.stringify({
        old_password: form.old_password,
        new_password: form.new_password
      })
    })
    
    const data = await response.json()
    if (data.code === 200) {
      ElMessage.success('密码修改成功，请重新登录')
      form.old_password = ''
      form.new_password = ''
      form.confirm_password = ''
      setTimeout(() => {
        localStorage.removeItem('admin_token')
        localStorage.removeItem('admin_user')
        window.location.href = '/login'
      }, 1500)
    } else {
      ElMessage.error(data.message || '密码修改失败')
    }
  } catch (error) {
    console.error('密码修改失败:', error)
    ElMessage.error('密码修改失败')
  }
}
</script>

<style lang="scss" scoped>
.change-password {
  .page-header {
    margin-bottom: 24px;
  }
  
  h1 {
    font-size: 24px;
    font-weight: 600;
    color: #333;
  }
}

.password-form {
  max-width: 500px;
}
</style>
