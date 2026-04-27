Component({
  properties: {
    tags: {
      type: Array,
      default: []
    },
    activeTag: {
      type: Number,
      default: 0
    },
    visible: {
      type: Boolean,
      default: false
    }
  },
  
  methods: {
    onTagTap(e) {
      const tagId = e.currentTarget.dataset.id
      this.triggerEvent('change', tagId)
    }
  }
})