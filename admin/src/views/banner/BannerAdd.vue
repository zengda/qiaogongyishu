<template>
  <div class="banner-add">
    <div class="page-header">
      <h1>添加Banner</h1>
      <el-button @click="$router.back()">返回</el-button>
    </div>
    
    <el-form :model="form" class="banner-form">
      <el-form-item label="Banner图片">
        <div class="upload-area" @click="triggerUpload">
          <img v-if="form.image_url" :src="form.image_url" class="preview-image" />
          <div v-else class="upload-placeholder">
            <el-icon><Upload /></el-icon>
            <span>点击上传Banner图片</span>
          </div>
        </div>
      </el-form-item>
      
      <el-form-item label="链接类型" prop="link_type">
        <el-radio-group v-model="form.link_type">
          <el-radio label="none">无链接</el-radio>
          <el-radio label="product">产品链接</el-radio>
          <el-radio label="external">外部链接</el-radio>
        </el-radio-group>
      </el-form-item>
      
      <el-form-item label="链接值" v-if="form.link_type !== 'none'">
        <template v-if="form.link_type === 'product'">
          <el-select v-model="form.link_value" placeholder="请选择产品">
            <el-option v-for="product in products" :key="product.id" :label="product.title" :value="product.id.toString()" />
          </el-select>
        </template>
        <template v-else>
          <el-input v-model="form.link_value" placeholder="请输入外部链接地址" />
        </template>
      </el-form-item>
      
      <el-form-item label="排序">
        <el-input-number v-model="form.sort_order" :min="0" :max="100" />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="handleSubmit">保存</el-button>
        <el-button @click="$router.back()">取消</el-button>
      </el-form-item>
    </el-form>
    
    <input ref="fileInput" type="file" accept="image/*" class="hidden-input" @change="handleFileChange" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Upload } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { bannerApi, productApi, uploadApi } from '../../api'

const router = useRouter()

const fileInput = ref(null)

const products = ref([])

const form = reactive({
  image_url: '',
  link_type: 'none',
  link_value: '',
  sort_order: 0
})

const loadProducts = async () => {
  try {
    const result = await productApi.list({ per_page: 100 })
    products.value = result.items || []
  } catch (error) {
    console.error('加载产品失败:', error)
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
    form.image_url = result.url
    e.target.value = ''
  } catch (error) {
    console.error('上传失败:', error)
    ElMessage.error('上传失败')
  }
}

const handleSubmit = async () => {
  if (!form.image_url) {
    ElMessage.error('请上传Banner图片')
    return
  }
  
  try {
    await bannerApi.create(form)
    ElMessage.success('保存成功')
    router.push('/banners')
  } catch (error) {
    console.error('保存失败:', error)
    const errorMsg = error?.response?.data?.message || error?.message || '保存失败'
    ElMessage.error(errorMsg)
  }
}

onMounted(() => {
  loadProducts()
})
</script>

<style lang="scss" scoped>
.banner-add {
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

.banner-form {
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

.preview-image {
  max-width: 300px;
  max-height: 180px;
  border-radius: 8px;
}

.hidden-input {
  display: none;
}
</style>