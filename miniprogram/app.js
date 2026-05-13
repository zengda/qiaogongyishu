const config = require('./utils/config')

const PRIVACY_AGREEMENT_KEY = 'privacy_agreement'

App({
  onLaunch() {
    console.log('巧工艺墅小程序启动')
    console.log('API Base URL:', config.apiBaseUrl)
    
    this.checkPrivacyAgreement()
  },
  
  onShow() {
    console.log('小程序显示')
  },
  
  onHide() {
    console.log('小程序隐藏')
  },
  
  checkPrivacyAgreement() {
    try {
      const agreed = wx.getStorageSync(PRIVACY_AGREEMENT_KEY)
      if (!agreed) {
        setTimeout(() => {
          wx.navigateTo({
            url: '/pages/privacy/privacy'
          })
        }, 100)
      }
    } catch (e) {
      console.error('检查隐私协议状态失败:', e)
    }
  },
  
  globalData: {
    userInfo: null,
    apiBaseUrl: config.apiBaseUrl
  }
})