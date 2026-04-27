Component({
  properties: {
    categories: {
      type: Array,
      default: []
    },
    activeCategory: {
      type: Number,
      default: 0
    },
    showStyleFilter: {
      type: Boolean,
      default: false
    }
  },
  
  methods: {
    onCategoryTap(e) {
      const categoryId = e.currentTarget.dataset.id
      this.triggerEvent('change', categoryId)
    },
    
    onStyleTap() {
      this.triggerEvent('styleTap')
    }
  }
})