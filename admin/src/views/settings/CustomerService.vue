<template>
  <div class="customer-service">
    <div class="page-header">
      <h1>客服二维码设置</h1>
    </div>
    
    <el-form :model="form" class="settings-form">
      <el-form-item label="客服二维码">
        <div class="upload-area" :class="{ 'has-image': form.customer_service_qrcode }">
          <template v-if="form.customer_service_qrcode">
            <div class="image-wrapper">
              <el-image 
                :src="form.customer_service_qrcode" 
                :preview-src-list="[form.customer_service_qrcode]"
                fit="contain"
                class="qrcode-image"
              />
              <div class="image-actions">
                <el-button type="primary" size="small" @click.stop="triggerUpload">
                  <el-icon><Refresh /></el-icon>
                  重新上传
                </el-button>
                <el-button type="danger" size="small" @click.stop="handleRemove">
                  <el-icon><Delete /></el-icon>
                  移除
                </el-button>
              </div>
            </div>
          </template>
          <div v-else class="upload-placeholder" @click="triggerUpload">
            <el-icon><Upload /></el-icon>
            <span>点击上传客服二维码</span>
          </div>
        </div>
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="handleSubmit" :loading="saving">保存设置</el-button>
      </el-form-item>
    </el-form>
    
    <input ref="fileInput" type="file" accept="image/*" class="hidden-input" @change="handleFileChange" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Upload, Refresh, Delete } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { uploadApi } from '../../api'

const fileInput = ref(null)
const saving = ref(false)

const form = reactive({
  customer_service_qrcode: ''
})

const loadSettings = async () => {
  try {
    const response = await fetch('/api/v1/admin/settings/customer_service_qrcode', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('admin_token')}`
      }
    })
    const data = await response.json()
    if (data.code === 200) {
      form.customer_service_qrcode = data.data.value || ''
    }
  } catch (error) {
    console.error('加载设置失败:', error)
  }
}

const triggerUpload = () => {
  fileInput.value?.click()
}

const handleFileChange = async (e) => {
  const file = e.target.files?.[0]
  if (!file) return
  
  try {
    const result = await uploadApi.upload(file)
    form.customer_service_qrcode = result.url
    e.target.value = ''
  } catch (error) {
    console.error('上传失败:', error)
    ElMessage.error('上传失败')
  }
}

const handleRemove = () => {
  form.customer_service_qrcode = ''
}

const handleSubmit = async () => {
  saving.value = true
  try {
    const response = await fetch('/api/v1/admin/settings', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('admin_token')}`
      },
      body: JSON.stringify({ customer_service_qrcode: form.customer_service_qrcode })
    })
    const data = await response.json()
    if (data.code === 200) {
      ElMessage.success('保存成功')
    } else {
      ElMessage.error(data.message || '保存失败')
    }
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadSettings()
})
</script>

<style lang="scss" scoped>
.customer-service {
  .page-header {
    margin-bottom: 24px;
  }
  
  h1 {
    font-size: 24px;
    font-weight: 600;
    color: #333;
  }
}

.settings-form {
  max-width: 500px;
}

.upload-area {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  
  &:hover {
    border-color: #1A6D5C;
  }
  
  &.has-image {
    border-style: solid;
    background: #fafafa;
  }
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  
  span {
    font-size: 14px;
    color: #999;
  }
}

.image-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.qrcode-image {
  max-width: 200px;
  max-height: 200px;
  border-radius: 8px;
  background: #fff;
}

.image-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.hidden-input {
  display: none;
}
</style>
