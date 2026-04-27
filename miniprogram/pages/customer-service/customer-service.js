const { get } = require('../../utils/request')

Page({
  data: {
    qrcodeUrl: ''
  },

  async onLoad() {
    await this.loadQrcode()
  },

  async loadQrcode() {
    try {
      const result = await get('/settings/customer_service_qrcode')
      this.setData({ qrcodeUrl: result.value || '/images/default-qrcode.png' })
    } catch (err) {
      console.error('加载二维码失败:', err)
      this.setData({ qrcodeUrl: '/images/default-qrcode.png' })
    }
  }
})