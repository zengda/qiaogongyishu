const { get } = require('../../utils/request')

Page({
  data: {
    keyword: '',
    historyList: [],
    hotList: ['别墅设计', '三层别墅', '新中式', '欧式风格', '农村自建房'],
    products: [],
    total: 0,
    showResult: false
  },

  onLoad() {
    this.loadHistory()
  },

  loadHistory() {
    const history = wx.getStorageSync('searchHistory') || []
    this.setData({ historyList: history.slice(0, 10) })
  },

  saveHistory(keyword) {
    let history = wx.getStorageSync('searchHistory') || []
    history = history.filter(item => item !== keyword)
    history.unshift(keyword)
    history = history.slice(0, 10)
    wx.setStorageSync('searchHistory', history)
    this.setData({ historyList: history })
  },

  onKeywordInput(e) {
    this.setData({ keyword: e.detail.value })
  },

  async onSearch() {
    const keyword = this.data.keyword.trim()
    if (!keyword) return
    
    this.saveHistory(keyword)
    await this.searchProducts(keyword)
  },

  onHistoryTap(e) {
    const keyword = e.currentTarget.textContent
    this.setData({ keyword })
    this.onSearch()
  },

  onHotTap(e) {
    const keyword = e.currentTarget.textContent
    this.setData({ keyword })
    this.onSearch()
  },

  async searchProducts(keyword) {
    try {
      const result = await get('/search', { keyword, page: 1, per_page: 20 })
      this.setData({
        products: result.items,
        total: result.total,
        showResult: true
      })
    } catch (err) {
      console.error('搜索失败:', err)
      this.setData({ products: [], total: 0, showResult: true })
    }
  },

  onProductClick(e) {
    const productId = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/detail/detail?id=${productId}`
    })
  },

  clearHistory() {
    wx.removeStorageSync('searchHistory')
    this.setData({ historyList: [] })
  },

  goBack() {
    wx.navigateBack()
  }
})