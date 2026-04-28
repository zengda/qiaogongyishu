const { get } = require('../../utils/request')

Page({
  data: {
    banners: [],
    categories: [],
    tags: [],
    products: [],
    activeCategory: 1,
    activeTag: 0,
    showStyleFilter: false,
    page: 1,
    hasMore: true,
    loading: false
  },

  async onLoad() {
    await this.loadData()
  },

  async loadData() {
    try {
      const [banners, categories, tags] = await Promise.all([
        get('/banners'),
        get('/categories'),
        get('/tags')
      ])
      
      this.setData({
        banners,
        categories,
        tags: [{ id: 0, name: '全部' }, ...tags]
      })
      
      await this.loadProducts()
    } catch (err) {
      console.error('加载数据失败:', err)
    }
  },

  async loadProducts(isLoadMore = false) {
    if (this.data.loading) return
    
    this.setData({ loading: true })
    
    try {
      const params = {
        page: isLoadMore ? this.data.page + 1 : 1,
        per_page: 10
      }
      
      if (this.data.activeCategory > 0) {
        params.category_id = this.data.activeCategory
      }
      
      if (this.data.activeTag > 0) {
        params.tag_id = this.data.activeTag
      }
      
      const result = await get('/products', params)
      
      const newProducts = isLoadMore ? [...this.data.products, ...result.items] : result.items
      
      this.setData({
        products: newProducts,
        page: result.page,
        hasMore: result.page < result.pages,
        loading: false
      })
    } catch (err) {
      console.error('加载产品失败:', err)
      this.setData({ loading: false })
    }
  },

  onBannerClick(e) {
    const banner = e.detail
    if (banner.link_type === 'product') {
      wx.navigateTo({
        url: `/pages/detail/detail?id=${banner.link_value}`
      })
    }
  },

  onSearchClick() {
    wx.navigateTo({
      url: '/pages/search/search'
    })
  },

  onCategoryChange(e) {
    const categoryId = e.detail
    this.setData({
      activeCategory: categoryId,
      showStyleFilter: false
    })
    this.loadProducts()
  },

  onStyleTap() {
    this.setData({
      showStyleFilter: !this.data.showStyleFilter
    })
  },

  onTagChange(e) {
    const tagId = e.detail
    this.setData({ activeTag: tagId })
    this.loadProducts()
  },

  onProductClick(e) {
    const productId = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/detail/detail?id=${productId}`
    })
  },

  onReachBottom() {
    if (this.data.hasMore && !this.data.loading) {
      this.loadProducts(true)
    }
  },

  onPullDownRefresh() {
    this.setData({ page: 1, hasMore: true })
    this.loadData().then(() => {
      wx.stopPullDownRefresh()
    })
  }
})