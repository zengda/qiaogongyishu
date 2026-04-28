<template>
  <div class="storage-config">
    <div class="page-header">
      <h1>存储配置</h1>
      <p class="page-desc">配置系统文件存储方式，支持本地存储和阿里云OSS</p>
    </div>
    
    <el-form :model="form" :rules="rules" ref="formRef" label-width="140px" class="config-form">
      <el-form-item label="存储方式">
        <el-radio-group v-model="form.storage_type">
          <el-radio label="local">本地存储</el-radio>
          <el-radio label="oss">阿里云 OSS</el-radio>
        </el-radio-group>
      </el-form-item>
      
      <template v-if="form.storage_type === 'oss'">
        <el-divider content-position="left">阿里云OSS配置</el-divider>
        
        <el-form-item label="Endpoint" prop="oss_endpoint">
          <el-input v-model="form.oss_endpoint" placeholder="oss-cn-hangzhou.aliyuncs.com" />
          <div class="form-tip">阿里云OSS地域节点，如：oss-cn-hangzhou.aliyuncs.com</div>
        </el-form-item>
        
        <el-form-item label="Access Key ID" prop="oss_access_key_id">
          <el-input v-model="form.oss_access_key_id" placeholder="请输入阿里云 AccessKey ID" />
        </el-form-item>
        
        <el-form-item label="Access Key Secret" prop="oss_access_key_secret">
          <el-input v-model="form.oss_access_key_secret" type="password" placeholder="请输入阿里云 AccessKey Secret" show-password />
        </el-form-item>
        
        <el-form-item label="Bucket 名称" prop="oss_bucket_name">
          <el-input v-model="form.oss_bucket_name" placeholder="请输入 OSS Bucket 名称" />
        </el-form-item>
        
        <el-form-item label="Bucket域名(外网)">
          <el-input v-model="form.oss_bucket_domain" placeholder="oss-cn-shenzhen.aliyuncs.com" />
          <div class="form-tip">请不要携带 http:// 或 https:// 前缀</div>
        </el-form-item>
        
        <el-form-item label="是否开启HTTPS">
          <el-switch
            v-model="form.oss_https_enabled"
            active-text="开启"
            inactive-text="关闭"
          />
          <div class="form-tip">如果您的站点开启了 HTTPS，请开启此选项</div>
        </el-form-item>
        
        <el-form-item label="自定义域名">
          <el-input v-model="form.oss_custom_domain" placeholder="cdn.example.com（可选）" />
          <div class="form-tip">使用自定义CDN域名时填写，如已配置Bucket域名则无需填写</div>
        </el-form-item>
      </template>
      
      <template v-if="form.storage_type === 'local'">
        <el-divider content-position="left">本地存储配置</el-divider>
        <el-alert type="info" :closable="false" show-icon>
          <template #title>
            当前使用本地存储，所有上传文件将保存在服务器本地目录
          </template>
        </el-alert>
      </template>
      
      <el-form-item>
        <el-button type="primary" @click="handleSubmit" :loading="saving">保存配置</el-button>
        <el-button v-if="form.storage_type === 'oss'" type="success" :loading="testing" @click="handleTestConnection">测试连接</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const formRef = ref(null)
const testing = ref(false)
const saving = ref(false)

const form = reactive({
  storage_type: 'local',
  oss_endpoint: '',
  oss_access_key_id: '',
  oss_access_key_secret: '',
  oss_bucket_name: '',
  oss_bucket_domain: '',
  oss_https_enabled: false,
  oss_custom_domain: ''
})

const rules = {
  oss_endpoint: [
    { required: true, message: '请输入 Endpoint', trigger: 'blur' }
  ],
  oss_access_key_id: [
    { required: true, message: '请输入 Access Key ID', trigger: 'blur' }
  ],
  oss_access_key_secret: [
    { required: true, message: '请输入 Access Key Secret', trigger: 'blur' }
  ],
  oss_bucket_name: [
    { required: true, message: '请输入 Bucket 名称', trigger: 'blur' }
  ]
}

const loadConfig = async () => {
  try {
    const response = await fetch('/api/v1/admin/storage/config', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('admin_token')}`
      }
    })
    const data = await response.json()
    if (data.code === 200) {
      form.storage_type = data.data.storage_type || 'local'
      if (data.data.storage_config) {
        Object.assign(form, data.data.storage_config)
      }
    }
  } catch (error) {
    console.error('加载配置失败:', error)
    ElMessage.error('加载配置失败')
  }
}

const handleTestConnection = async () => {
  try {
    await formRef.value.validateField(['oss_endpoint', 'oss_access_key_id', 'oss_access_key_secret', 'oss_bucket_name'])
    
    testing.value = true
    try {
      const response = await fetch('/api/v1/admin/storage/test-oss', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('admin_token')}`
        },
        body: JSON.stringify({
          endpoint: form.oss_endpoint,
          access_key_id: form.oss_access_key_id,
          access_key_secret: form.oss_access_key_secret,
          bucket_name: form.oss_bucket_name,
          bucket_domain: form.oss_bucket_domain,
          https_enabled: form.oss_https_enabled
        })
      })
      const data = await response.json()
      if (data.code === 200) {
        ElMessage.success(`连接成功！Bucket: ${data.data.bucket_name}`)
      } else {
        ElMessage.error(data.message || '连接失败，请检查配置')
      }
    } catch (error) {
      console.error('测试连接失败:', error)
      ElMessage.error('测试连接失败，请检查网络连接')
    } finally {
      testing.value = false
    }
  } catch (error) {
    console.warn('表单验证失败')
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    
    if (form.storage_type === 'oss') {
      const confirmed = await ElMessageBox.confirm(
        '确认保存OSS配置？保存后将使用新配置进行文件上传。',
        '确认保存',
        { type: 'warning' }
      )
    }
    
    saving.value = true
    try {
      const response = await fetch('/api/v1/admin/storage/config', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('admin_token')}`
        },
        body: JSON.stringify({
          storage_type: form.storage_type,
          oss_config: form.storage_type === 'oss' ? {
            endpoint: form.oss_endpoint,
            access_key_id: form.oss_access_key_id,
            access_key_secret: form.oss_access_key_secret,
            bucket_name: form.oss_bucket_name,
            bucket_domain: form.oss_bucket_domain,
            https_enabled: form.oss_https_enabled,
            custom_domain: form.oss_custom_domain
          } : null
        })
      })
      const data = await response.json()
      if (data.code === 200) {
        ElMessage.success('保存成功')
      } else {
        ElMessage.error(data.message || '保存失败')
      }
    } catch (error) {
      console.error('保存失败:', error)
      ElMessage.error('保存失败，请检查网络连接')
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
.storage-config {
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

:deep(.el-divider--horizontal) {
  margin: 24px 0 16px;
}

:deep(.el-alert) {
  margin-bottom: 24px;
}

:deep(.el-form-item:last-child) {
  margin-top: 16px;
}
</style>
