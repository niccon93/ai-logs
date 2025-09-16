import React from 'react'
import { api } from '../lib/api'

export default function Dashboard() {
  const [status, setStatus] = React.useState<any>(null)
  React.useEffect(()=>{
    (async()=>{
      const r1 = await api.get('/ready'); const r2 = await api.get('/live')
      setStatus({ ready:r1.data, live:r2.data })
    })()
  },[])
  return (
    <div>
      <h2>Дашборд</h2>
      <pre style={{background:'#f5f5f5', padding:12}}>{JSON.stringify(status, null, 2)}</pre>
      <p>Это минимальная стартовая панель. Импорт демо-данных: раздел «Админ».</p>
    </div>
  )
}
