const { post } = require('../../utils/request')

Page({
  data: {
    form: {
      name: '',
      phone: '',
      wechat: '',
      province: '',
      city: '',
      buildingAreaBudget: ''
    },
    productId: '',
    productTitle: '',
    submitting: false,
    showSuccess: false
  },

  onLoad(options) {
    this.setData({
      productId: options.product_id || '',
      productTitle: decodeURIComponent(options.product_title || '')
    })
  },

  onNameInput(e) {
    this.setData({ 'form.name': e.detail.value })
  },

  onPhoneInput(e) {
    this.setData({ 'form.phone': e.detail.value })
  },

  onWechatInput(e) {
    this.setData({ 'form.wechat': e.detail.value })
  },

  onBudgetInput(e) {
    this.setData({ 'form.buildingAreaBudget': e.detail.value })
  },

  onRegionPick() {
    wx.chooseRegion({
      success: (res) => {
        this.setData({
          'form.province': res.province,
          'form.city': res.city
        })
      }
    })
  },

  async onSubmit() {
    const { form, productId, productTitle } = this.data
    
    if (!form.name.trim()) {
      wx.showToast({ title: '请输入姓名', icon: 'none' })
      return
    }
    
    if (!form.phone.trim()) {
      wx.showToast({ title: '请输入手机号', icon: 'none' })
      return
    }
    
    if (!/^1[3-9]\d{9}$/.test(form.phone)) {
      wx.showToast({ title: '请输入正确的手机号', icon: 'none' })
      return
    }
    
    this.setData({ submitting: true })
    
    try {
      await post('/customers', {
        name: form.name,
        phone: form.phone,
        wechat: form.wechat,
        province: form.province,
        city: form.city,
        building_area_budget: form.buildingAreaBudget,
        product_id: productId,
        product_title: productTitle
      })
      
      this.setData({ showSuccess: true })
    } catch (err) {
      wx.showToast({ title: err || '提交失败', icon: 'none' })
    } finally {
      this.setData({ submitting: false })
    }
  },

  goHome() {
    wx.navigateBack({
      delta: 99
    })
  }
})