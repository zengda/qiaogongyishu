const app = getApp()
const baseUrl = app.globalData.apiBaseUrl

const request = (options) => {
  return new Promise((resolve, reject) => {
    wx.request({
      url: baseUrl + options.url,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'Content-Type': 'application/json',
        ...options.header
      },
      success: (res) => {
        if (res.statusCode === 200) {
          if (res.data.code === 200) {
            resolve(res.data.data)
          } else {
            reject(res.data.message)
          }
        } else {
          reject('网络请求失败')
        }
      },
      fail: (err) => {
        reject(err.errMsg)
      }
    })
  })
}

const get = (url, data = {}, header = {}) => {
  return request({ url, method: 'GET', data, header })
}

const post = (url, data = {}, header = {}) => {
  return request({ url, method: 'POST', data, header })
}

const put = (url, data = {}, header = {}) => {
  return request({ url, method: 'PUT', data, header })
}

const del = (url, data = {}, header = {}) => {
  return request({ url, method: 'DELETE', data, header })
}

module.exports = {
  request,
  get,
  post,
  put,
  del
}