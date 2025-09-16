
import { useEffect, useState } from 'react';
export default function Admin(){
  const [users,setUsers]=useState<any[]>([]);
  useEffect(()=>{ (async()=>{
    try{
      const token = localStorage.getItem('token'); const apiBase = (location.port==='8080') ? `${location.protocol}//${location.hostname}:8000` : '';
      const res = await fetch(`${apiBase}/users`, { headers: {'Authorization': `Bearer ${token||''}`}});
      if(res.ok){ setUsers(await res.json()); }
    }catch{}
  })(); },[]);
  return (<div className="container"><h2>Администрирование</h2>
    <div className="card"><table className="table"><thead><tr><th>ID</th><th>Логин</th><th>Роль</th><th>Email</th></tr></thead>
    <tbody>{users.map((u:any)=>(<tr key={u.id}><td>{u.id}</td><td>{u.username}</td><td>{u.role}</td><td>{u.email||''}</td></tr>))}</tbody></table></div>
  </div>);
}
