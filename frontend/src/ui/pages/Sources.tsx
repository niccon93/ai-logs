import React, { useEffect, useState } from 'react'
import { api } from '../lib/api'

export default function Sources() {
  const [accs, setAccs] = useState<any[]>([])
  const [sources, setSources] = useState<any[]>([])
  const [acc, setAcc] = useState({ name:'svc-1', username:'svc', public_key:'', description:'' })
  const [src, setSrc] = useState({ server_account_id:0, path_glob:'/var/log/*.log', interval_minutes:5, enabled:true })

  async function reload() {
    const a = await api.get('/server-accounts')
    setAccs(a.data || [])
    if (a.data?.length) setSrc(s=>({...s, server_account_id:a.data[0].id}))
    const s = await api.get('/sources')
    setSources(s.data || [])
  }

  useEffect(()=>{ reload() }, [])

  async function addAcc(e: React.FormEvent) {
    e.preventDefault()
    await api.post('/server-accounts', acc)
    await reload()
  }

  async function addSrc(e: React.FormEvent) {
    e.preventDefault()
    await api.post('/sources', src)
    await reload()
  }

  return (
    <div style={{display:'grid', gap:16}}>
      <h2>Источники логов</h2>
      <div style={{display:'grid', gap:8, maxWidth:600}}>
        <h3>Сервисная учётка</h3>
        <form onSubmit={addAcc} style={{display:'grid', gap:8}}>
          <input placeholder="Название" value={acc.name} onChange={e=>setAcc({...acc, name:e.target.value})}/>
          <input placeholder="Логин" value={acc.username} onChange={e=>setAcc({...acc, username:e.target.value})}/>
          <textarea placeholder="id_rsa.pub" value={acc.public_key} onChange={e=>setAcc({...acc, public_key:e.target.value})}/>
          <textarea placeholder="Описание" value={acc.description} onChange={e=>setAcc({...acc, description:e.target.value})}/>
          <button>Добавить учётку</button>
        </form>
      </div>

      <div style={{display:'grid', gap:8, maxWidth:600}}>
        <h3>Путь логов</h3>
        <form onSubmit={addSrc} style={{display:'grid', gap:8}}>
          <select value={src.server_account_id} onChange={e=>setSrc({...src, server_account_id:parseInt(e.target.value)})}>
            {accs.map(a=><option key={a.id} value={a.id}>{a.name}</option>)}
          </select>
          <input placeholder="/var/log/*.log" value={src.path_glob} onChange={e=>setSrc({...src, path_glob:e.target.value})}/>
          <input type="number" placeholder="Интервал (мин)" value={src.interval_minutes} onChange={e=>setSrc({...src, interval_minutes:parseInt(e.target.value)})}/>
          <label><input type="checkbox" checked={src.enabled} onChange={e=>setSrc({...src, enabled:e.target.checked})}/> Включено</label>
          <button>Добавить источник</button>
        </form>
      </div>

      <div>
        <h3>Текущие источники</h3>
        <pre style={{background:'#f5f5f5', padding:12}}>{JSON.stringify(sources, null, 2)}</pre>
      </div>
    </div>
  )
}
