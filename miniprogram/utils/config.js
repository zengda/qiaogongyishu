const DEV_API_BASE_URL = 'http://localhost:5001/api/v1'
const PROD_API_BASE_URL = 'https://qgys.rongyun.online/api/v1'

function getApiBaseUrl() {
  try {
    const accountInfo = wx.getAccountInfoSync()
    const env = accountInfo.miniProgram.envVersion
    if (env === 'release' || env === 'trial') {
      return PROD_API_BASE_URL
    }
  } catch (e) {}
  return PROD_API_BASE_URL
}

module.exports = {
  apiBaseUrl: getApiBaseUrl(),
  
  categoryNames: ['一层', '二层', '三层', '多层', '双拼'],
  
  tagNames: ['全部', '新中式', '欧式', '现代', '中式'],
  
  statusMap: {
    new: '新客户',
    contacted: '已联系',
    followed: '跟进中',
    closed: '已成交'
  }
}