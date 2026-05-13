const { get } = require('../../utils/request')

Page({
  data: {
    keyword: '',
    historyList: [],
    hotList: ['别墅设计', '三层别墅', '新中式', '欧式风格', '农村自建房'],
    products: [],
    total: 0,
    page: 1,
    perPage: 20,
    hasMore: false,
    showResult: false,
    searchLoading: false,
    loadingMore: false
  },

  _lastKeyword: '',
  _searchLock: false,

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
    if (this._searchLock) return
    if (keyword === this._lastKeyword) return

    this._lastKeyword = keyword
    this._searchLock = true
    this.saveHistory(keyword)

    this.setData({
      searchLoading: true,
      showResult: true,
      products: [],
      page: 1,
      hasMore: false
    })

    try {
      const result = await get('/search', { keyword, page: 1, per_page: this.data.perPage })
      this.setData({
        products: result.items || [],
        total: result.total,
        page: result.page,
        hasMore: result.page < result.pages,
        searchLoading: false
      })
    } catch (err) {
      console.error('搜索失败:', err)
      this.setData({
        searchLoading: false,
        showResult: false
      })
      wx.showToast({ title: '搜索失败，请重试', icon: 'none' })
    } finally {
      this._searchLock = false
    }
  },

  onHistoryTap(e) {
    const keyword = e.currentTarget.dataset.keyword
    if (!keyword) return
    this.setData({ keyword })
    this.onSearch()
  },

  onHotTap(e) {
    const keyword = e.currentTarget.dataset.keyword
    if (!keyword) return
    this.setData({ keyword })
    this.onSearch()
  },

  async onReachBottom() {
    if (this.data.loadingMore) return
    if (!this.data.hasMore) return
    if (this.data.searchLoading) return

    this.setData({ loadingMore: true })

    try {
      const nextPage = this.data.page + 1
      const result = await get('/search', {
        keyword: this._lastKeyword,
        page: nextPage,
        per_page: this.data.perPage
      })
      this.setData({
        products: [...this.data.products, ...result.items],
        page: result.page,
        hasMore: result.page < result.pages,
        loadingMore: false
      })
    } catch (err) {
      console.error('加载更多失败:', err)
      this.setData({ loadingMore: false })
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