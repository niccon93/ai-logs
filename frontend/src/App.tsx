
import { useTranslation } from 'react-i18next';
import { Link, Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import JobsStream from './pages/JobsStream';
import FindingsTable from './pages/FindingsTable';
import Login from './pages/Login';
import Admin from './pages/Admin';
import { useEffect, useState } from 'react';
import { api } from './lib/api';
export default function App(){
  const { t, i18n } = useTranslation(); const [theme,setTheme]=useState('light'); const [me,setMe]=useState<any>(null); useEffect(()=>{ document.documentElement.setAttribute('data-theme', theme==='dark'?'dark':''); try{ api('/users/me').then(setMe).catch(()=>{});}catch{} },[theme]);
  function logout(){ localStorage.removeItem('token'); location.href='/login'; }
  return (<>
    <header className="header"><Link to="/">AI-Logs</Link>
      <nav className="nav"><Link to="/findings">{t('findings')}</Link><Link to="/jobs">{t('jobs')}</Link>{me?.role==='admin' && <Link to="/admin">Admin</Link>}</nav>
      <div style={{marginLeft:'auto', display:'flex', gap:8}}>
        <button className="button" onClick={()=>i18n.changeLanguage('ru')}>RU</button>
        <button className="button" onClick={()=>i18n.changeLanguage('en')}>EN</button>
        <Link className="button" to="/login">{t('login')}</Link>
        <button className="button" onClick={logout}>Logout</button>
      </div>
    <div className="button" onClick={()=>setTheme(theme==='dark'?'light':'dark')}>{theme==='dark'?'Light':'Dark'}</div></header>
    <main><Routes><Route path="/" element={<Dashboard/>} /><Route path="/jobs" element={<JobsStream/>} />
      <Route path="/findings" element={<FindingsTable/>} /><Route path="/login" element={<Login/>} />
      <Route path="/admin" element={<Admin/>} /></Routes></main>
  </>);
}
