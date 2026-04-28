<template>
  <div class="product-add">
    <div class="page-header">
      <h1>添加产品</h1>
      <el-button @click="$router.back()">返回</el-button>
    </div>
    
    <el-form :model="form" ref="formRef" :rules="rules" class="product-form">
      <el-form-item label="产品名称" prop="title">
        <el-input v-model="form.title" placeholder="请输入产品名称" />
      </el-form-item>
      
      <el-form-item label="产品型号" prop="model_number">
        <el-input v-model="form.model_number" placeholder="请输入产品型号" />
      </el-form-item>
      
      <el-form-item label="分类" prop="category_id">
        <el-select v-model="form.category_id" placeholder="请选择分类">
          <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="标签">
        <el-select v-model="form.tag_ids" multiple placeholder="请选择标签">
          <el-option v-for="tag in tags" :key="tag.id" :label="tag.name" :value="tag.id" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="建筑面积">
        <el-input v-model="form.floor_area" placeholder="请输入建筑面积（如：200㎡）" />
      </el-form-item>
      
      <el-form-item label="占地面积">
        <el-input v-model="form.building_area" placeholder="请输入占地面积（如：150㎡）" />
      </el-form-item>
      
      <el-form-item label="户型">
        <el-input v-model="form.rooms" placeholder="请输入户型（如：5室3厅3卫）" />
      </el-form-item>
      
      <el-form-item label="封面图片" prop="cover_image">
        <div class="upload-area" @click="triggerUpload('cover')">
          <img v-if="form.cover_image" :src="form.cover_image" class="preview-image" />
          <div v-else class="upload-placeholder">
            <el-icon><Upload /></el-icon>
            <span>点击上传封面图片</span>
          </div>
        </div>
      </el-form-item>
      
      <el-form-item label="Banner图片">
        <div class="banner-list">
          <div 
            class="banner-item" 
            v-for="(img, index) in form.banner_images" 
            :key="index"
          >
            <img :src="img.image_url || img" class="banner-image" />
            <el-button type="text" @click="removeBanner(index)" style="color: #E53E3E">删除</el-button>
          </div>
          <div class="upload-area small" @click="triggerUpload('banner')">
            <div class="upload-placeholder">
              <el-icon><Plus /></el-icon>
              <span>添加图片</span>
            </div>
          </div>
        </div>
      </el-form-item>
      
      <el-form-item label="详情图片">
        <div class="detail-list">
          <div 
            class="detail-item" 
            v-for="(img, index) in form.detail_images" 
            :key="index"
          >
            <img :src="img.image_url || img" class="detail-image" />
            <el-button type="text" @click="removeDetail(index)" style="color: #E53E3E">删除</el-button>
          </div>
          <div class="upload-area small" @click="triggerUpload('detail')">
            <div class="upload-placeholder">
              <el-icon><Plus /></el-icon>
              <span>添加图片</span>
            </div>
          </div>
        </div>
      </el-form-item>
      
      <el-form-item label="描述">
        <el-input type="textarea" v-model="form.description" placeholder="请输入产品描述" :rows="4" />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">保存</el-button>
        <el-button @click="$router.back()">取消</el-button>
      </el-form-item>
    </el-form>
    
    <input ref="fileInput" type="file" accept="image/*" class="hidden-input" @change="handleFileChange" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Upload, Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { productApi, categoryApi, tagApi, uploadApi } from '../../api'

const router = useRouter()
const formRef = ref(null)
const fileInput = ref(null)
const uploadType = ref('')
const submitting = ref(false)

const categories = ref([])
const tags = ref([])

const form = reactive({
  title: '',
  model_number: '',
  category_id: '',
  tag_ids: [],
  floor_area: '',
  building_area: '',
  rooms: '',
  cover_image: '',
  banner_images: [],
  detail_images: [],
  description: ''
})

const rules = {
  title: [{ required: true, message: '请输入产品名称', trigger: 'blur' }],
  model_number: [{ required: true, message: '请输入产品型号', trigger: 'blur' }],
  category_id: [{ required: true, message: '请选择分类', trigger: 'blur' }],
  cover_image: [{ required: true, message: '请上传封面图片', trigger: 'blur' }]
}

const loadCategories = async () => {
  categories.value = await categoryApi.list()
}

const loadTags = async () => {
  tags.value = await tagApi.list()
}

const triggerUpload = (type) => {
  uploadType.value = type
  fileInput.value?.click()
}

const handleFileChange = async (e) => {
  const file = e.target.files?.[0]
  if (!file) return
  
  try {
    const result = await uploadApi.upload(file)
    
    if (uploadType.value === 'cover') {
      form.cover_image = result.url
    } else if (uploadType.value === 'banner') {
      form.banner_images.push(result.url)
    } else if (uploadType.value === 'detail') {
      form.detail_images.push(result.url)
    }
    
    e.target.value = ''
  } catch (error) {
    console.error('上传失败:', error)
    ElMessage.error('上传失败')
  }
}

const removeBanner = (index) => {
  form.banner_images.splice(index, 1)
}

const removeDetail = (index) => {
  form.detail_images.splice(index, 1)
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    submitting.value = true
    
    const data = {
      title: form.title,
      model_number: form.model_number,
      category_id: form.category_id,
      tags: form.tag_ids,
      floor_area: form.floor_area,
      building_area: form.building_area,
      rooms: form.rooms,
      cover_image: form.cover_image,
      banner_images: form.banner_images,
      detail_images: form.detail_images,
      description: form.description
    }
    
    await productApi.create(data)
    ElMessage.success('添加成功')
    router.push('/products')
  } catch (error) {
    console.error('保存失败:', error)
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadCategories()
  loadTags()
})
</script>

<style lang="scss" scoped>
.product-add {
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

.product-form {
  max-width: 800px;
}

.upload-area {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  
  &.small {
    padding: 20px;
    width: 120px;
    height: 120px;
  }
  
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
  max-width: 200px;
  max-height: 200px;
  border-radius: 8px;
}

.banner-list, .detail-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.banner-item, .detail-item {
  position: relative;
}

.banner-image {
  width: 200px;
  height: 120px;
  object-fit: cover;
  border-radius: 8px;
}

.detail-image {
  width: 150px;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
}

.hidden-input {
  display: none;
}
</style>