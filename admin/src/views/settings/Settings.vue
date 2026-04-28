<template>
  <div class="settings">
    <div class="page-header">
      <h1>系统设置</h1>
    </div>
    
    <el-form :model="form" class="settings-form" v-loading="loading">
      <el-form-item label="客服二维码">
        <div class="upload-area" @click="triggerUpload">
          <img v-if="form.customer_service_qrcode" :src="form.customer_service_qrcode" class="qrcode-image" />
          <div v-else class="upload-placeholder">
            <el-icon><Upload /></el-icon>
            <span>点击上传客服二维码</span>
          </div>
        </div>
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">保存设置</el-button>
      </el-form-item>
    </el-form>
  </div>
  
  <input ref="fileInput" type="file" accept="image/*" class="hidden-input" @change="handleFileChange" />
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Upload } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { uploadApi, settingsApi } from '../../api'

const fileInput = ref(null)
const loading = ref(false)
const submitting = ref(false)

const form = reactive({
  customer_service_qrcode: ''
})

const loadSettings = async () => {
  loading.value = true
  try {
    const result = await settingsApi.get('customer_service_qrcode')
    form.customer_service_qrcode = result?.value || ''
  } catch (error) {
    console.error('加载设置失败:', error)
    ElMessage.error('加载设置失败')
  } finally {
    loading.value = false
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
    ElMessage.success('上传成功')
  } catch (error) {
    console.error('上传失败:', error)
    ElMessage.error('上传失败')
  }
}

const handleSubmit = async () => {
  submitting.value = true
  try {
    await settingsApi.update({ customer_service_qrcode: form.customer_service_qrcode })
    ElMessage.success('保存成功')
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadSettings()
})
</script>

<style lang="scss" scoped>
.settings {
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
  padding: 40px;
  text-align: center;
  cursor: pointer;
  
  &:hover {
    border-color: #1A6D5C;
  }
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  
  span {
    font-size: 14px;
    color: #999;
  }
}

.qrcode-image {
  max-width: 200px;
  max-height: 200px;
  border-radius: 8px;
}

.hidden-input {
  display: none;
}
</style>