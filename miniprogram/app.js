App({
  onLaunch() {
    console.log('巧工艺墅小程序启动')
  },
  
  onShow() {
    console.log('小程序显示')
  },
  
  onHide() {
    console.log('小程序隐藏')
  },
  
  globalData: {
    userInfo: null,
    apiBaseUrl: 'http://localhost:5001/api/v1'
  }
})