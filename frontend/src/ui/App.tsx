import React from 'react'
import { Routes, Route, Link, Navigate, useLocation } from 'react-router-dom'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Admin from './pages/Admin'
import Sources from './pages/Sources'
import Alerts from './pages/Alerts'
import Integrations from './pages/Integrations'
import { getToken, getRole } from './lib/auth'

function Protected({ children, admin=false }: { children: React.ReactNode, admin?: boolean }) {
  const tok = getToken(); const role = getRole();
  const loc = useLocation();
  if (!tok) return <Navigate to="/login" state={{ from: loc }} replace />
  if (admin && role !== 'admin') return <Navigate to="/" replace />
  return <>{children}</>;
}

export default function App() {
  const token = getToken()
  const role = getRole()

  return (
    <div style={{fontFamily:'Inter, system-ui, sans-serif', padding:16}}>
      <nav style={{display:'flex', gap:12, marginBottom:16}}>
        <Link to="/">Главная</Link>
        <Link to="/sources">Источники</Link>
        <Link to="/alerts">Алерты</Link>
        <Link to="/integrations">Интеграции</Link>
        <Link to="/admin">Админ</Link>
        <span style={{marginLeft:'auto'}}>
          {token ? <span>Роль: {role} • <a href="/login">Выйти</a></span> : <Link to="/login">Войти</Link>}
        </span>
      </nav>
      <Routes>
        <Route path="/" element={<Protected><Dashboard/></Protected>} />
        <Route path="/sources" element={<Protected><Sources/></Protected>} />
        <Route path="/alerts" element={<Protected><Alerts/></Protected>} />
        <Route path="/integrations" element={<Protected><Integrations/></Protected>} />
        <Route path="/admin" element={<Protected admin><Admin/></Protected>} />
        <Route path="/login" element={<Login/>} />
        <Route path="*" element={<div>404</div>} />
      </Routes>
    </div>
  )
}
