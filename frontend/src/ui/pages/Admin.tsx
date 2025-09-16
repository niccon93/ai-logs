import React, { useState } from 'react'
import { api } from '../lib/api'

export default function Admin() {
  const [u, setU] = useState('test'); const [p, setP] = useState('test123'); const [role, setR] = useState<'admin'|'user'>('user')
  const [email, setE] = useState('user@example.com')
  const [msg, setMsg] = useState<string| null>(null)

  async function createUser(e: React.FormEvent) {
    e.preventDefault(); setMsg(null)
    try {
      await api.post('/users', { username:u, password:p, role, email })
      setMsg('Пользователь создан')
    } catch (e:any) {
      setMsg(e?.response?.data?.detail || 'Ошибка')
    }
  }

  async function importDemo() {
    setMsg(null)
    try {
      await api.post('/examples/import')
      setMsg('Импорт выполнен')
    } catch (e:any) {
      setMsg(e?.response?.data?.detail || 'Ошибка импорта')
    }
  }

  return (
    <div>
      <h2>Администрирование</h2>
      <button onClick={importDemo}>Импортировать пример</button>
      {msg && <div style={{marginTop:8}}>{msg}</div>}

      <h3 style={{marginTop:24}}>Создать пользователя</h3>
      <form onSubmit={createUser} style={{display:'grid', gap:8, maxWidth:360}}>
        <input placeholder="username" value={u} onChange={e=>setU(e.target.value)}/>
        <input placeholder="email" value={email} onChange={e=>setE(e.target.value)}/>
        <input placeholder="password" value={p} onChange={e=>setP(e.target.value)} type="password" />
        <select value={role} onChange={e=>setR(e.target.value as any)}>
          <option value="user">user</option>
          <option value="admin">admin</option>
        </select>
        <button type="submit">Создать</button>
      </form>
    </div>
  )
}
