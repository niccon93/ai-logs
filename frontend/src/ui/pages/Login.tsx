import React, { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { login } from '../lib/api'

export default function Login() {
  const [username, setU] = useState('admin')
  const [password, setP] = useState('admin123')
  const [err, setErr] = useState<string|null>(null)
  const nav = useNavigate()
  const loc = useLocation() as any
  const from = loc.state?.from?.pathname || '/'

  async function handle(e: React.FormEvent) {
    e.preventDefault()
    setErr(null)
    try {
      await login(username, password)
      nav(from, { replace:true })
    } catch (e:any) {
      setErr(e?.response?.data?.detail || 'Ошибка входа')
    }
  }

  return (
    <form onSubmit={handle} style={{maxWidth:360, margin:'48px auto', display:'grid', gap:8}}>
      <h2>Вход</h2>
      <label>Логин
        <input value={username} onChange={e=>setU(e.target.value)} />
      </label>
      <label>Пароль
        <input type="password" value={password} onChange={e=>setP(e.target.value)} />
      </label>
      {err && <div style={{color:'crimson'}}>{err}</div>}
      <button type="submit">Войти</button>
    </form>
  )
}
