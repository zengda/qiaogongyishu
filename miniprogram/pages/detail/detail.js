const { get, post } = require('../../utils/request')

Page({
  data: {
    product: null,
    productId: null
  },

  async onLoad(options) {
    const id = options.id
    this.setData({ productId: id })
    await this.loadProduct(id)
  },

  async loadProduct(productId) {
    try {
      const product = await get(`/products/${productId}`)
      this.setData({ product })
      
      await post(`/products/${productId}/view`)
    } catch (err) {
      console.error('加载产品失败:', err)
      wx.showToast({ title: '加载失败', icon: 'none' })
    }
  },

  onImageTap(e) {
    const currentIndex = e.detail.current
    const urls = this.data.product.banner_images.map(img => img.image_url)
    wx.previewImage({
      current: urls[currentIndex],
      urls
    })
  },

  onDetailImageTap(e) {
    const index = e.currentTarget.dataset.index
    const urls = this.data.product.detail_images.map(img => img.image_url)
    wx.previewImage({
      current: urls[index],
      urls
    })
  },

  goToCustomerService() {
    wx.navigateTo({
      url: '/pages/customer-service/customer-service'
    })
  },

  goToForm() {
    const { productId, product } = this.data
    wx.navigateTo({
      url: `/pages/form/form?product_id=${productId}&product_title=${encodeURIComponent(product.title)}`
    })
  },

  onShareAppMessage() {
    const { product } = this.data
    return {
      title: product.title,
      path: `/pages/detail/detail?id=${product.id}`,
      imageUrl: product.banner_images[0]?.image_url
    }
  },

  onShareTimeline() {
    const { product } = this.data
    return {
      title: product.title,
      query: `id=${product.id}`,
      imageUrl: product.banner_images[0]?.image_url
    }
  }
})