<template>
  <div class="miniprogram-config">
    <div class="page-header">
      <h1>小程序配置</h1>
      <p class="page-desc">配置微信小程序 AppID 和上传密钥，通过 miniprogram-ci 实现代码预览与上传</p>
    </div>

    <el-tabs v-model="activeTab" type="border-card">
      <el-tab-pane label="基本配置" name="config">
        <el-form :model="form" label-width="140px" class="config-form" v-loading="loading">
          <el-form-item label="小程序 AppID">
            <el-input v-model="form.appid" placeholder="请输入小程序 AppID" />
            <div class="form-tip">在微信公众平台 - 开发管理 - 开发设置 中查看</div>
          </el-form-item>

          <el-form-item label="项目类型">
            <el-select v-model="form.type" placeholder="请选择项目类型">
              <el-option label="小程序" value="miniProgram" />
              <el-option label="小游戏" value="miniGame" />
              <el-option label="小程序插件" value="miniProgramPlugin" />
              <el-option label="小游戏插件" value="miniGamePlugin" />
            </el-select>
          </el-form-item>

          <el-form-item label="代码上传密钥">
            <el-input
              v-model="form.private_key"
              type="textarea"
              :rows="6"
              placeholder="请粘贴从微信公众平台下载的代码上传密钥（.key 文件内容）"
            />
            <div class="form-tip">
              在微信公众平台 - 开发管理 - 开发设置 - 小程序代码上传 中生成并下载密钥文件，
              将文件内容粘贴到此。密钥不会明文存储在微信平台，遗失必须重置。
            </div>
          </el-form-item>

          <el-form-item label="项目路径">
            <el-input v-model="form.project_path" placeholder="服务器上小程序项目根目录路径" />
            <div class="form-tip">小程序项目所在目录的绝对路径，即 project.config.json 所在目录</div>
          </el-form-item>

          <el-form-item label="CI 机器人编号">
            <el-input-number v-model="form.robot" :min="1" :max="30" />
            <div class="form-tip">可选 1 ~ 30，对应微信开发者工具中的 CI 机器人编号</div>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="handleSaveConfig" :loading="saving">保存配置</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <el-tab-pane label="预览" name="preview">
        <el-form :model="previewForm" label-width="140px" class="config-form">
          <el-form-item label="备注说明">
            <el-input v-model="previewForm.desc" placeholder="预览版本的备注描述" />
          </el-form-item>

          <el-form-item label="预览页面">
            <el-input v-model="previewForm.page_path" placeholder="pages/index/index" />
            <div class="form-tip">扫码后直接进入的页面路径</div>
          </el-form-item>

          <el-form-item label="启动参数">
            <el-input v-model="previewForm.search_query" placeholder="如: id=123&from=admin" />
            <div class="form-tip">页面启动时携带的 query 参数，选填</div>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="handlePreview" :loading="previewing">
              {{ previewing ? '编译中...' : '生成预览二维码' }}
            </el-button>
          </el-form-item>

          <el-form-item v-if="qrcodeUrl" label="预览二维码">
            <div class="qrcode-area">
              <el-image
                :src="qrcodeUrl"
                :preview-src-list="[qrcodeUrl]"
                fit="contain"
                class="qrcode-image"
              />
              <p class="qrcode-tip">请用微信扫描二维码进行预览</p>
            </div>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <el-tab-pane label="上传代码" name="upload">
        <el-form :model="uploadForm" label-width="140px" class="config-form">
          <el-alert
            title="上传说明"
            type="info"
            :closable="false"
            show-icon
            style="margin-bottom: 20px"
          >
            <template #default>
              <p>上传后代码将进入微信公众平台"版本管理"中的「开发版本」，可在微信开发者工具中设为体验版或提交审核。</p>
            </template>
          </el-alert>

          <el-form-item label="版本号" required>
            <el-input v-model="uploadForm.version" placeholder="如: 1.0.0" />
            <div class="form-tip">必填，每次上传必须递增版本号</div>
          </el-form-item>

          <el-form-item label="备注说明">
            <el-input
              v-model="uploadForm.desc"
              type="textarea"
              :rows="3"
              placeholder="此版本更新的内容描述"
            />
          </el-form-item>

          <el-form-item v-if="latestVersion" label="最近上传">
            <el-tag type="success">版本 {{ latestVersion }}</el-tag>
            <span v-if="latestDesc" class="latest-desc">{{ latestDesc }}</span>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="handleUpload" :loading="uploading">
              {{ uploading ? '上传中...' : '上传代码' }}
            </el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { miniprogramApi } from '../../api'

const activeTab = ref('config')
const loading = ref(false)
const saving = ref(false)
const previewing = ref(false)
const uploading = ref(false)
const qrcodeUrl = ref('')
const latestVersion = ref('')
const latestDesc = ref('')

const form = reactive({
  appid: '',
  type: 'miniProgram',
  private_key: '',
  project_path: '',
  robot: 1
})

const previewForm = reactive({
  desc: '从管理后台预览',
  page_path: 'pages/index/index',
  search_query: ''
})

const uploadForm = reactive({
  version: '',
  desc: ''
})

const loadConfig = async () => {
  loading.value = true
  try {
    const config = await miniprogramApi.getConfig()
    form.appid = config.appid || ''
    form.type = config.type || 'miniProgram'
    form.private_key = config.private_key || ''
    form.project_path = config.project_path || ''
    form.robot = parseInt(config.robot) || 1
    latestVersion.value = config.latest_version || ''
    latestDesc.value = config.latest_desc || ''
  } catch (error) {
    console.error('加载配置失败:', error)
    ElMessage.error('加载配置失败')
  } finally {
    loading.value = false
  }
}

const handleSaveConfig = async () => {
  if (!form.appid) {
    ElMessage.warning('请输入小程序 AppID')
    return
  }
  saving.value = true
  try {
    await miniprogramApi.saveConfig({
      appid: form.appid,
      type: form.type,
      private_key: form.private_key,
      project_path: form.project_path,
      robot: form.robot
    })
    ElMessage.success('配置保存成功')
  } catch (error) {
    console.error('保存配置失败:', error)
    ElMessage.error('保存配置失败')
  } finally {
    saving.value = false
  }
}

const handlePreview = async () => {
  previewing.value = true
  try {
    const result = await miniprogramApi.preview({
      desc: previewForm.desc,
      page_path: previewForm.page_path,
      search_query: previewForm.search_query
    })
    if (result.qrcode_url) {
      qrcodeUrl.value = result.qrcode_url
      ElMessage.success('预览二维码生成成功')
    }
  } catch (error) {
    console.error('预览失败:', error)
    ElMessage.error(error.message || '预览失败')
  } finally {
    previewing.value = false
  }
}

const handleUpload = async () => {
  if (!uploadForm.version) {
    ElMessage.warning('请输入版本号')
    return
  }
  try {
    await ElMessageBox.confirm(
      `确认上传版本 ${uploadForm.version} ？上传后将进入微信公众平台的"开发版本列表中"。`,
      '确认上传',
      { confirmButtonText: '确认上传', cancelButtonText: '取消', type: 'warning' }
    )
  } catch {
    return
  }
  uploading.value = true
  try {
    const result = await miniprogramApi.upload({
      version: uploadForm.version,
      desc: uploadForm.desc
    })
    ElMessage.success(result.message || '上传成功')
    latestVersion.value = uploadForm.version
    latestDesc.value = uploadForm.desc
    uploadForm.version = ''
    uploadForm.desc = ''
  } catch (error) {
    console.error('上传失败:', error)
    ElMessage.error(error.message || '上传失败')
  } finally {
    uploading.value = false
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
  }

  h1 {
    font-size: 24px;
    font-weight: 600;
    color: #333;
    margin: 0;
  }

  .page-desc {
    margin-top: 8px;
    color: #999;
    font-size: 14px;
  }

  .config-form {
    max-width: 680px;
    padding-top: 16px;
  }

  .form-tip {
    font-size: 12px;
    color: #999;
    margin-top: 4px;
    line-height: 1.6;
  }

  .qrcode-area {
    text-align: center;
    padding: 20px;
    background: #f9fafb;
    border-radius: 12px;
    border: 1px dashed #d9d9d9;
  }

  .qrcode-image {
    width: 200px;
    height: 200px;
    margin-bottom: 12px;
  }

  .qrcode-tip {
    color: #999;
    font-size: 13px;
    margin: 0;
  }

  .latest-desc {
    margin-left: 12px;
    color: #666;
    font-size: 13px;
  }
}
</style>
