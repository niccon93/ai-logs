
import { useEffect, useState } from 'react';
import DataTable from '../components/DataTable';
type Finding = { id:number; dataset_id:number; model_id:number|null; severity:string|null; ts:string|null; host:string|null; app:string|null; template_id:string|null; message:string|null; }
export default function FindingsTable(){
  const [rows,setRows]=useState<Finding[]>([]); const [page,setPage]=useState(1); const [size,setSize]=useState(50); const [total,setTotal]=useState(0);
  const [search,setSearch]=useState(localStorage.getItem('flt_search')||''); const [severity,setSeverity]=useState(localStorage.getItem('flt_sev')||'');
  async function load(p=page){ localStorage.setItem('flt_search', search); localStorage.setItem('flt_sev', severity);
    const params = new URLSearchParams({page:String(p), size:String(size)}); if(search) params.set('search', search); if(severity) params.set('severity', severity);
    const r = await fetch(`http://${location.hostname}:8000/findings?${params.toString()}`); const d = await r.json(); setRows(d.items); setTotal(d.total); setPage(d.page);
  }
  useEffect(()=>{ load(1); }, [size, severity]);
  return (<div className="container"><h2>Findings</h2>
    <div className="card" style={{marginBottom:12}}>
      <input className="input" placeholder="Найти текст / Search message..." value={search} onChange={e=>setSearch(e.target.value)} />{' '}
      <select className="input" value={severity} onChange={e=>setSeverity(e.target.value)}>
        <option value="">All severities</option><option>info</option><option>low</option><option>medium</option><option>high</option><option>critical</option>
      </select>{' '}<button className="button" onClick={()=>load(1)}>Apply</button><span style={{marginLeft:8, opacity:.6}}>Total: {total}</span>
    </div>
    <div className="card"><DataTable rows={rows} pageSize={size} columns={[
      {key:'ts',label:'Time'}, {key:'severity',label:'Severity'}, {key:'host',label:'Host'}, {key:'app',label:'App'}, {key:'message',label:'Message'}
    ]}/>
      <div style={{display:'flex', gap:8, marginTop:8}}>
        <button className="button" onClick={()=>{ if(page>1){ const p=page-1; setPage(p); load(p);} }} disabled={page<=1}>Prev</button>
        <span className="text-sm">{page}</span>
        <button className="button" onClick={()=>{ const p=page+1; setPage(p); load(p); }} disabled={rows.length < size}>Next</button>
        <select className="input" value={size} onChange={e=>setSize(Number(e.target.value))}><option value={20}>20</option><option value={50}>50</option><option value={100}>100</option></select>
      </div>
    </div>
  </div>);
}
