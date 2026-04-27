import request from '../utils/request'

export const authApi = {
  login(data) {
    return request.post('/admin/login', data)
  },
  getProfile() {
    return request.get('/admin/profile')
  }
}

export const productApi = {
  list(params) {
    return request.get('/products', { params })
  },
  get(id) {
    return request.get(`/products/${id}`)
  },
  create(data) {
    return request.post('/products', data)
  },
  update(id, data) {
    return request.put(`/products/${id}`, data)
  },
  delete(id) {
    return request.delete(`/products/${id}`)
  }
}

export const categoryApi = {
  list() {
    return request.get('/categories')
  },
  get(id) {
    return request.get(`/categories/${id}`)
  },
  create(data) {
    return request.post('/categories', data)
  },
  update(id, data) {
    return request.put(`/categories/${id}`, data)
  },
  delete(id) {
    return request.delete(`/categories/${id}`)
  }
}

export const tagApi = {
  list() {
    return request.get('/tags')
  },
  get(id) {
    return request.get(`/tags/${id}`)
  },
  create(data) {
    return request.post('/tags', data)
  },
  update(id, data) {
    return request.put(`/tags/${id}`, data)
  },
  delete(id) {
    return request.delete(`/tags/${id}`)
  }
}

export const bannerApi = {
  list() {
    return request.get('/banners')
  },
  get(id) {
    return request.get(`/banners/${id}`)
  },
  create(data) {
    return request.post('/banners', data)
  },
  update(id, data) {
    return request.put(`/banners/${id}`, data)
  },
  delete(id) {
    return request.delete(`/banners/${id}`)
  }
}

export const customerApi = {
  list(params) {
    return request.get('/customers', { params })
  },
  get(id) {
    return request.get(`/customers/${id}`)
  },
  update(id, data) {
    return request.put(`/customers/${id}`, data)
  },
  delete(id) {
    return request.delete(`/customers/${id}`)
  },
  export() {
    return request.get('/customers/export', { responseType: 'blob' })
  }
}

export const uploadApi = {
  upload(file) {
    const formData = new FormData()
    formData.append('file', file)
    return request.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}

export const dashboardApi = {
  stats() {
    return request.get('/dashboard/stats')
  }
}