import request from '../utils/request'
import axios from 'axios'
import store from '../store'

export const authApi = {
  login(data) {
    const instance = axios.create({
      timeout: 10000
    })
    return instance.post('/api/v1/admin/auth/login', data)
  }
}

export const productApi = {
  list(params) {
    return request.get('/admin/products', { params })
  },
  get(id) {
    return request.get(`/admin/products/${id}`)
  },
  create(data) {
    return request.post('/admin/products', data)
  },
  update(id, data) {
    return request.put(`/admin/products/${id}`, data)
  },
  delete(id) {
    return request.delete(`/admin/products/${id}`)
  }
}

export const categoryApi = {
  list() {
    return request.get('/admin/categories')
  },
  get(id) {
    return request.get(`/admin/categories/${id}`)
  },
  create(data) {
    return request.post('/admin/categories', data)
  },
  update(id, data) {
    return request.put(`/admin/categories/${id}`, data)
  },
  delete(id) {
    return request.delete(`/admin/categories/${id}`)
  }
}

export const tagApi = {
  list() {
    return request.get('/admin/tags')
  },
  get(id) {
    return request.get(`/admin/tags/${id}`)
  },
  create(data) {
    return request.post('/admin/tags', data)
  },
  update(id, data) {
    return request.put(`/admin/tags/${id}`, data)
  },
  delete(id) {
    return request.delete(`/admin/tags/${id}`)
  }
}

export const bannerApi = {
  list() {
    return request.get('/admin/banners')
  },
  get(id) {
    return request.get(`/admin/banners/${id}`)
  },
  create(data) {
    return request.post('/admin/banners', data)
  },
  update(id, data) {
    return request.put(`/admin/banners/${id}`, data)
  },
  delete(id) {
    return request.delete(`/admin/banners/${id}`)
  }
}

export const customerApi = {
  list(params) {
    return request.get('/admin/customers', { params })
  },
  get(id) {
    return request.get(`/admin/customers/${id}`)
  },
  create(data) {
    return request.post('/admin/customers', data)
  },
  updateStatus(id, status) {
    return request.patch(`/admin/customers/${id}/status`, { status })
  },
  updateRemark(id, remark) {
    return request.patch(`/admin/customers/${id}/remark`, { remark })
  },
  delete(id) {
    return request.delete(`/admin/customers/${id}`)
  },
  async export() {
    const token = store.getters.token
    const response = await axios.get('/api/v1/admin/customers/export', {
      headers: {
        Authorization: `Bearer ${token}`
      },
      responseType: 'blob'
    })
    return response.data
  }
}

export const uploadApi = {
  upload(file) {
    const formData = new FormData()
    formData.append('file', file)
    return request.post('/admin/upload/image', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}

export const dashboardApi = {
  stats() {
    return request.get('/admin/dashboard')
  }
}

export const settingsApi = {
  get(key) {
    return request.get(`/admin/settings/${key}`)
  },
  getAll() {
    return request.get('/admin/settings')
  },
  update(data) {
    return request.put('/admin/settings', data)
  }
}