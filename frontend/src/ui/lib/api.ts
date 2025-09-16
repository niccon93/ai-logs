import axios from 'axios'
import { getToken, setRole } from './auth'

const API_URL = (import.meta as any).env?.VITE_API_URL || (window as any).__API_URL__ || '' || (document?.querySelector('meta[name=api-url]') as any)?.content || '/'
const instance = axios.create({ baseURL: API_URL })

instance.interceptors.request.use((config) => {
  const t = getToken()
  if (t) config.headers = { ...(config.headers||{}), Authorization: `Bearer ${t}` }
  return config
})

instance.interceptors.response.use(res => res, async (err) => {
  if (err?.response?.status === 401) {
    // token invalid; drop
    localStorage.removeItem('token')
    localStorage.removeItem('role')
    location.href = '/login'
  }
  return Promise.reject(err)
})

export async function login(username: string, password: string) {
  const r = await instance.post('/auth/login', { username, password })
  const token = r.data?.access_token
  if (token) {
    localStorage.setItem('token', token)
    // fetch role
    const me = await instance.get('/auth/me')
    setRole(me.data?.role || 'user')
  }
}

export const api = instance
