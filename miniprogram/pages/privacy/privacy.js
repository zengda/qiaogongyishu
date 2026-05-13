const AGREEMENT_KEY = 'privacy_agreement'

Page({
  data: {},

  onLoad() {
    
  },

  onOverlayTap() {
    // 点击遮罩层不做任何操作，弹窗不关闭
  },

  onModalTap() {
    // 点击弹窗内部不做任何操作
  },

  onOpenPrivacyContract() {
    // 调用微信官方 API 打开隐私协议页面
    wx.openPrivacyContract({
      success: () => {
        console.log('隐私协议页面打开成功')
      },
      fail: (err) => {
        console.error('隐私协议页面打开失败:', err)
        // 如果微信版本不支持，显示提示
        wx.showToast({
          title: '请更新微信版本',
          icon: 'none'
        })
      }
    })
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