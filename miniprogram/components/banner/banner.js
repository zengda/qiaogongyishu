Component({
  properties: {
    banners: {
      type: Array,
      default: []
    }
  },
  
  methods: {
    onBannerTap(e) {
      const currentIndex = e.detail.current
      const banner = this.properties.banners[currentIndex]
      this.triggerEvent('click', banner)
    }
  }
})