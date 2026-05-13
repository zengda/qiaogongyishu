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
    },
    tags: {
      type: Array,
      default: []
    },
    activeTag: {
      type: Number,
      default: 0
    }
  },
  
  methods: {
    onCategoryTap(e) {
      const categoryId = e.currentTarget.dataset.id
      this.triggerEvent('change', categoryId)
    },
    
    onStyleTap() {
      console.log('styleTap triggered')
      this.triggerEvent('styleTap')
    },
    
    onTagTap(e) {
      const tagId = e.currentTarget.dataset.id
      this.triggerEvent('tagChange', tagId)
    }
  }
})