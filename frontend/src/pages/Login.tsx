
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
export default function Login(){
  const { t } = useTranslation();
  const [username,setU]=useState('admin'); const [password,setP]=useState('admin123'); const [otp,setOTP]=useState(''); const [msg,setMsg]=useState('');
  async function submit(){
    try{
      const apiBase = (location.port==='8080') ? `${location.protocol}//${location.hostname}:8000` : '';
      const res = await fetch(`${apiBase}/auth/login`, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({username, password, otp: otp||undefined})});
      if(!res.ok) throw new Error('Login error');
      const d = await res.json(); localStorage.setItem('token', d.access_token); location.href='/';
    }catch(e:any){ setMsg('Ошибка входа / Login error'); }
  }
  return (<div className="container"><h2>Вход / Login</h2><div className="card" style={{maxWidth:420}}>
      <label>Username</label>
      <input className="input" value={username} onChange={e=>setU(e.target.value)} placeholder="Username" /><br/><br/>
      <label>Password</label>
      <input className="input" value={password} onChange={e=>setP(e.target.value)} type="password" placeholder="Password" /><br/><br/>
      <label>{t('otp')}</label>
      <input className="input" value={otp} onChange={e=>setOTP(e.target.value)} placeholder={t('otp')||'OTP'} /><br/><br/>
      <button className="button primary" onClick={submit}>Войти / Login</button>
      <div style={{color:'#b91c1c', marginTop:8}}>{msg}</div>
      <div style={{marginTop:8}}><a href="/auth/oidc/login">SSO (если настроено)</a></div>
  </div></div>);
}
