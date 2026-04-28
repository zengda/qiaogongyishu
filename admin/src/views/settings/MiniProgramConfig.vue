<template>
  <div class="miniprogram-config">
    <div class="page-header">
      <h1>小程序设置</h1>
      <p class="page-desc">配置微信小程序相关参数，支持手动绑定小程序</p>
    </div>
    
    <el-form :model="form" :rules="rules" ref="formRef" label-width="140px" class="config-form">
      <el-form-item label="授权方式">
        <el-radio-group v-model="form.auth_type">
          <el-radio label="manual">手动绑定</el-radio>
        </el-radio-group>
        <div class="form-tip">当前仅支持手动绑定方式，需手动输入小程序AppId和AppSecret</div>
      </el-form-item>
      
      <el-divider content-position="left">小程序配置</el-divider>
      
      <el-form-item label="小程序 AppId" prop="app_id">
        <el-input v-model="form.app_id" placeholder="请输入小程序 AppId" />
        <div class="form-tip">登录微信公众平台 -> 设置 -> 开发设置 中获取</div>
      </el-form-item>
      
      <el-form-item label="小程序 AppSecret" prop="app_secret">
        <el-input 
          v-model="form.app_secret" 
          :type="showPassword ? 'text' : 'password'" 
          placeholder="请输入小程序 AppSecret" 
          @blur="handleSecretBlur"
        />
        <div class="form-actions">
          <el-button type="text" @click="showPassword = !showPassword" size="small">
            {{ showPassword ? '隐藏' : '显示' }}
          </el-button>
          <span v-if="isMasked" class="mask-hint">（已脱敏显示）</span>
        </div>
        <div class="form-tip">登录微信公众平台 -> 设置 -> 开发设置 中获取，点击重置可生成新的AppSecret</div>
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="handleSubmit(false)" :loading="saving">保存配置</el-button>
        <el-button type="info" @click="handleSubmit(true)" :loading="saving">保存并同步到小程序</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const formRef = ref(null)
const saving = ref(false)
const showPassword = ref(false)
const isMasked = ref(false)
const originalSecret = ref('')

const form = reactive({
  auth_type: 'manual',
  app_id: '',
  app_secret: ''
})

const rules = {
  app_id: [
    { required: true, message: '请输入小程序 AppId', trigger: 'blur' },
    { min: 18, max: 18, message: 'AppId长度必须为18位', trigger: 'blur' }
  ],
  app_secret: [
    { required: true, message: '请输入小程序 AppSecret', trigger: 'blur' }
  ]
}

const loadConfig = async () => {
  try {
    const response = await fetch('/api/v1/admin/settings/miniprogram', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('admin_token')}`
      }
    })
    const data = await response.json()
    if (data.code === 200 && data.data) {
      form.auth_type = data.data.auth_type || 'manual'
      form.app_id = data.data.app_id || ''
      form.app_secret = data.data.app_secret || ''
      originalSecret.value = data.data.app_secret || ''
      // 判断是否为脱敏数据
      isMasked.value = (data.data.app_secret || '').startsWith('*')
    }
  } catch (error) {
    console.error('加载配置失败:', error)
    ElMessage.error('加载配置失败')
  }
}

const handleSecretBlur = () => {
  // 如果用户修改了脱敏显示的密码，取消脱敏标记
  if (isMasked.value && form.app_secret !== originalSecret.value) {
    isMasked.value = false
  }
}

const handleSubmit = async (syncToFile = false) => {
  try {
    await formRef.value.validate()
    
    saving.value = true
    const endpoint = syncToFile 
      ? '/api/v1/admin/settings/miniprogram/sync' 
      : '/api/v1/admin/settings/miniprogram'
    const method = syncToFile ? 'POST' : 'PUT'
    const successMsg = syncToFile ? '保存并同步成功' : '保存成功'
    const failMsg = syncToFile ? '同步失败' : '保存失败'
    
    try {
      const response = await fetch(endpoint, {
        method,
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('admin_token')}`
        },
        body: JSON.stringify({
          auth_type: form.auth_type,
          app_id: form.app_id,
          app_secret: form.app_secret
        })
      })
      const data = await response.json()
      if (data.code === 200) {
        ElMessage.success(successMsg)
        // 重新加载配置（获取脱敏后的密码）
        loadConfig()
      } else {
        ElMessage.error(data.message || failMsg)
      }
    } catch (error) {
      console.error('操作失败:', error)
      ElMessage.error(`操作失败，请检查网络连接`)
    } finally {
      saving.value = false
    }
  } catch (error) {
    console.warn('表单验证失败')
  }
}

onMounted(() => {
  loadConfig()
})
</script>

<style lang="scss" scoped>
.miniprogram-config {
  .page-header {
    margin-bottom: 24px;
    
    h1 {
      font-size: 24px;
      font-weight: 600;
      color: #333;
      margin-bottom: 8px;
    }
    
    .page-desc {
      color: #666;
      font-size: 14px;
    }
  }
}

.config-form {
  max-width: 700px;
  background: #fff;
  padding: 24px;
  border-radius: 8px;
}

.form-tip {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
  line-height: 1.4;
}

.form-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  
  .mask-hint {
    font-size: 12px;
    color: #67c23a;
  }
}

:deep(.el-divider--horizontal) {
  margin: 24px 0 16px;
}

:deep(.el-form-item:last-child) {
  margin-top: 16px;
}
</style>