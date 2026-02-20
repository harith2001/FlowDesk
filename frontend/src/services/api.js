import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token from localStorage on initialization
const token = localStorage.getItem('token')
if (token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

// Add organization header from localStorage
const orgSlug = localStorage.getItem('currentOrgSlug')
if (orgSlug) {
  api.defaults.headers.common['X-Organization-Slug'] = orgSlug
}

export default api
