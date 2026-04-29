<template>
  <div class="storage-config">
    <div class="page-header">
      <h1>存储配置</h1>
      <p class="page-desc">配置系统文件存储方式，支持本地存储和阿里云OSS</p>
    </div>
    
    <el-form :model="form" :rules="rules" ref="formRef" label-width="140px" class="config-form" v-loading="loading">
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
        <el-form-item label="上传目录路径">
          <el-input v-model="form.local_upload_path" placeholder="uploads" />
          <div class="form-tip">服务器上文件存储目录的相对或绝对路径</div>
        </el-form-item>
        <el-form-item label="本地访问地址">
          <el-input v-model="form.local_base_url" placeholder="http://localhost:5001/uploads" />
          <div class="form-tip">本地文件对外访问的完整 URL 前缀</div>
        </el-form-item>
      </template>
      
      <el-form-item>
        <el-button type="primary" @click="handleSubmit" :loading="saving">保存配置</el-button>
        <el-button v-if="form.storage_type === 'oss'" type="success" :loading="testing" @click="handleTestConnection">测试连接</el-button>
      </el-form-item>
    </el-form>

    <div class="migrate-section" v-if="form.storage_type === 'oss' && configLoaded">
      <div class="section-title-wrap">
        <h3>本地文件迁移</h3>
        <p class="section-desc">将当前服务器 uploads 目录中的所有文件批量上传到阿里云 OSS 中</p>
      </div>
      <el-button 
        type="warning" 
        :loading="migrating" 
        @click="handleMigrate"
        :icon="Upload"
      >
        {{ migrating ? '迁移中...' : '迁移本地文件到 OSS' }}
      </el-button>
    </div>

    <el-dialog v-model="migrateResultVisible" title="迁移结果" width="560px">
      <div class="migrate-result" v-if="migrateResult">
        <el-alert 
          :type="migrateResult.failed === 0 ? 'success' : 'warning'"
          :closable="false"
          show-icon
        >
          <template #title>
            迁移完成：成功 {{ migrateResult.migrated }} 个，失败 {{ migrateResult.failed }} 个，共 {{ migrateResult.total }} 个文件
          </template>
        </el-alert>
        <div class="migrate-detail" v-if="migrateResult.failed_files && migrateResult.failed_files.length > 0">
          <h4>失败列表：</h4>
          <div v-for="item in migrateResult.failed_files" :key="item.filename" class="failed-item">
            <span class="failed-name">{{ item.filename }}</span>
            <span class="failed-error">{{ item.error }}</span>
          </div>
        </div>
        <div class="migrate-detail" v-if="migrateResult.migrated_files && migrateResult.migrated_files.length > 0">
          <h4>成功迁移 {{ migrateResult.migrated_files.length }} 个文件：</h4>
          <div v-for="item in migrateResult.migrated_files" :key="item.filename" class="success-item">
            <span class="success-name">{{ item.filename }}</span>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button type="primary" @click="migrateResultVisible = false">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Upload } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { storageApi } from '../../api'

const formRef = ref(null)
const testing = ref(false)
const saving = ref(false)
const loading = ref(false)
const migrating = ref(false)
const configLoaded = ref(false)
const migrateResultVisible = ref(false)
const migrateResult = ref(null)

const form = reactive({
  storage_type: 'local',
  oss_endpoint: '',
  oss_access_key_id: '',
  oss_access_key_secret: '',
  oss_bucket_name: '',
  oss_bucket_domain: '',
  oss_https_enabled: false,
  oss_custom_domain: '',
  local_upload_path: 'uploads',
  local_base_url: 'http://localhost:5001/uploads'
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
  loading.value = true
  try {
    const config = await storageApi.getConfig()
    form.storage_type = config.storage_type || 'local'
    form.oss_endpoint = config.oss_endpoint || ''
    form.oss_access_key_id = config.oss_access_key_id || ''
    form.oss_access_key_secret = config.oss_access_key_secret || ''
    form.oss_bucket_name = config.oss_bucket_name || ''
    form.oss_bucket_domain = config.oss_bucket_domain || ''
    form.oss_https_enabled = config.oss_https_enabled || false
    form.oss_custom_domain = config.oss_custom_domain || ''
    form.local_upload_path = config.local_upload_path || 'uploads'
    form.local_base_url = config.local_base_url || 'http://localhost:5001/uploads'
    configLoaded.value = true
  } catch (error) {
    console.error('加载配置失败:', error)
    ElMessage.error('加载配置失败')
  } finally {
    loading.value = false
  }
}

const handleTestConnection = async () => {
  try {
    await formRef.value.validateField(['oss_endpoint', 'oss_access_key_id', 'oss_access_key_secret', 'oss_bucket_name'])
    
    testing.value = true
    const result = await storageApi.testOss({
      endpoint: form.oss_endpoint,
      access_key_id: form.oss_access_key_id,
      access_key_secret: form.oss_access_key_secret,
      bucket_name: form.oss_bucket_name,
      bucket_domain: form.oss_bucket_domain,
      https_enabled: form.oss_https_enabled
    })
    ElMessage.success(`连接成功！Bucket: ${result.bucket_name}`)
  } catch (error) {
    if (error !== 'cancel') {
      console.error('测试连接失败:', error)
      ElMessage.error(error?.message || '测试连接失败，请检查网络连接')
    }
  } finally {
    testing.value = false
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    
    if (form.storage_type === 'oss') {
      await ElMessageBox.confirm(
        '确认保存OSS配置？保存后将使用新配置进行文件上传。',
        '确认保存',
        { type: 'warning' }
      )
    }
    
    saving.value = true
    
    await storageApi.saveConfig({
      storage_type: form.storage_type,
      local_upload_path: form.local_upload_path,
      local_base_url: form.local_base_url,
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
    ElMessage.success('保存成功')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('保存失败:', error)
      ElMessage.error(error?.message || '保存失败')
    }
  } finally {
    saving.value = false
  }
}

const handleMigrate = async () => {
  try {
    await ElMessageBox.confirm(
      '即将把本地 uploads 目录中的所有文件上传到阿里云 OSS。此操作不会删除本地文件，上传的文件将存储在 OSS 的 uploads/ 目录下。确认继续？',
      '确认迁移',
      { confirmButtonText: '确认迁移', cancelButtonText: '取消', type: 'warning' }
    )
  } catch {
    return
  }

  migrating.value = true
  try {
    migrateResult.value = await storageApi.migrateToOss()
    migrateResultVisible.value = true
  } catch (error) {
    console.error('迁移失败:', error)
    ElMessage.error(error?.message || '迁移失败')
  } finally {
    migrating.value = false
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

.migrate-section {
  max-width: 700px;
  background: #fff;
  padding: 24px;
  border-radius: 8px;
  margin-top: 20px;

  .section-title-wrap {
    margin-bottom: 16px;

    h3 {
      font-size: 18px;
      font-weight: 600;
      color: #333;
      margin: 0;
    }

    .section-desc {
      margin-top: 4px;
      color: #999;
      font-size: 13px;
    }
  }
}

.migrate-result {
  .el-alert {
    margin-bottom: 16px;
  }

  h4 {
    font-size: 14px;
    font-weight: 500;
    color: #333;
    margin: 12px 0 8px;
  }
}

.failed-item, .success-item {
  padding: 6px 0;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.failed-name {
  color: #E53E3E;
}

.failed-error {
  color: #999;
  font-size: 12px;
}

.success-name {
  color: #1A6D5C;
}

.migrate-detail {
  max-height: 300px;
  overflow-y: auto;
  margin-top: 12px;
}
</style>
