<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <div class="logo">
          <span class="logo-icon">🏠</span>
          <span class="logo-text">巧工艺墅管理后台</span>
        </div>
        <p class="login-desc">欢迎登录管理后台</p>
      </div>
      
      <el-form :model="form" ref="formRef" :rules="rules" class="login-form">
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            size="large"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleLogin" size="large" class="login-btn">
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import { authApi } from '../../api'

const router = useRouter()
const store = useStore()

const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    const response = await authApi.login(form)
    const res = response.data
    
    if (res.code !== 200 || !res.data || !res.data.token) {
      throw new Error(res.message || '登录失败')
    }
    
    await store.dispatch('login', {
      token: res.data.token,
      user: res.data.user
    })
    
    window.location.href = '/dashboard'
  } catch (error) {
    console.error('登录失败:', error)
    if (error.response && error.response.status === 401) {
      ElMessage.error('用户名或密码错误')
    } else {
      ElMessage.error(error.message || '登录失败，请重试')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1A6D5C 0%, #2D3748 100%);
}

.login-box {
  width: 400px;
  padding: 40px;
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-icon {
  font-size: 40px;
}

.logo-text {
  margin-left: 12px;
  font-size: 24px;
  font-weight: 600;
  color: #333;
}

.login-desc {
  margin-top: 12px;
  color: #999;
  font-size: 14px;
}

.login-form {
  .el-form-item {
    margin-bottom: 24px;
  }
}

.login-btn {
  width: 100%;
  background-color: #1A6D5C;
  border-color: #1A6D5C;
  
  &:hover {
    background-color: #155A4B;
    border-color: #155A4B;
  }
}
</style>