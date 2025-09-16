import { useMemo } from 'react';
import { LineSeries, BarSeries } from '../components/Charts';
export default function Dashboard(){
  const data = useMemo(()=> Array.from({length:50}, (_,i)=>({t:i, value: Math.round(Math.sin(i/5)*50+50)})), []);
  return (<div className="container"><h2>Дашборд / Dashboard</h2>
    <div className="card"><LineSeries data={data} xKey="t" yKey="value"/></div>
    <div className="card" style={{marginTop:12}}><BarSeries data={data} xKey="t" yKey="value"/></div>

    <div className="card" style={{marginTop:12}}>
      <button className="button" onClick={async ()=>{
        try{
          const token = localStorage.getItem('token');
          const apiBase = (location.port==='8080') ? `${location.protocol}//${location.hostname}:8000` : '';
          const res = await fetch(`${apiBase}/examples/import`, { method: 'POST', headers: {'Authorization': `Bearer ${token||''}`} });
          if(!res.ok) throw new Error('err');
          alert('Импорт примера выполнен');
        }catch{ alert('Ошибка импорта (нужны права admin и вход)'); }
      }}>Импортировать пример</button>
    </div>
  </div>);
}
