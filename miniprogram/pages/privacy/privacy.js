const AGREEMENT_KEY = 'privacy_agreement'

Page({
  data: {},

  onLoad() {
    
  },

  onAgree() {
    try {
      wx.setStorageSync(AGREEMENT_KEY, 'true')
    } catch (e) {
      console.error('保存隐私协议状态失败:', e)
    }
    
    this.navigateBack()
  },

  onDisagree() {
    wx.showModal({
      title: '提示',
      content: '您需要同意隐私政策才能继续使用小程序',
      showCancel: false,
      confirmText: '我知道了'
    })
  },

  navigateBack() {
    const pages = getCurrentPages()
    if (pages.length > 1) {
      wx.navigateBack()
    } else {
      wx.reLaunch({
        url: '/pages/index/index'
      })
    }
  }
})