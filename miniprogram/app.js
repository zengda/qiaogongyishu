const config = require('./utils/config')

App({
  onLaunch() {
    console.log('巧工艺墅小程序启动')
    console.log('API Base URL:', config.apiBaseUrl)
  },
  
  onShow() {
    console.log('小程序显示')
  },
  
  onHide() {
    console.log('小程序隐藏')
  },
  
  globalData: {
    userInfo: null,
    apiBaseUrl: config.apiBaseUrl
  }
})