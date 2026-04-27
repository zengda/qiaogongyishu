const TOKEN_KEY = 'wx_token'
const OPENID_KEY = 'wx_openid'

const setToken = (token) => {
  wx.setStorageSync(TOKEN_KEY, token)
}

const getToken = () => {
  return wx.getStorageSync(TOKEN_KEY) || ''
}

const setOpenid = (openid) => {
  wx.setStorageSync(OPENID_KEY, openid)
}

const getOpenid = () => {
  return wx.getStorageSync(OPENID_KEY) || ''
}

const clearAuth = () => {
  wx.removeStorageSync(TOKEN_KEY)
  wx.removeStorageSync(OPENID_KEY)
}

const login = async () => {
  return new Promise((resolve, reject) => {
    wx.login({
      success: async (res) => {
        if (res.code) {
          try {
            const result = await require('./request').post('/auth/wx-login', { code: res.code })
            setToken(result.token)
            setOpenid(result.openid)
            resolve(result)
          } catch (err) {
            reject(err)
          }
        } else {
          reject('登录失败')
        }
      },
      fail: (err) => {
        reject(err)
      }
    })
  })
}

module.exports = {
  setToken,
  getToken,
  setOpenid,
  getOpenid,
  clearAuth,
  login
}