import { useMemo, useState } from 'react';
type Row = Record<string, any>;
export default function DataTable({rows, columns, pageSize=20}:{rows:Row[], columns:{key:string,label:string}[], pageSize?:number}){
  const [page,setPage]=useState(1); const [q,setQ]=useState('');
  const filtered=useMemo(()=>{ if(!q)return rows; const s=q.toLowerCase();
    return rows.filter(r=>Object.values(r).some(v=>String(v??'').toLowerCase().includes(s))); },[rows,q]);
  const total=filtered.length; const pages=Math.max(1,Math.ceil(total/pageSize));
  const start=(page-1)*pageSize; const slice=filtered.slice(start,start+pageSize);
  return (<div className="w-full">
    <div className="flex gap-2 mb-2"><input className="input" placeholder="Фильтр / Filter..." value={q} onChange={e=>{setPage(1);setQ(e.target.value)}}/>
    <div className="ml-auto text-sm" style={{opacity:.6}}>{start+1}-{Math.min(start+pageSize,total)} / {total}</div></div>
    <div className="card"><table className="table">
      <thead><tr>{columns.map(c=><th key={c.key}>{c.label}</th>)}</tr></thead>
      <tbody>{slice.map((r,i)=>(<tr key={i}>{columns.map(c=><td key={c.key}>{String(r[c.key]??'')}</td>)}</tr>))}
      {slice.length===0 && <tr><td colSpan={columns.length} style={{opacity:.6, padding:'12px'}}>Нет данных / No data</td></tr>}</tbody></table></div>
    <div className="flex gap-2 mt-2"><button className="button" onClick={()=>setPage(p=>Math.max(1,p-1))} disabled={page<=1}>Prev</button>
    <span className="text-sm">{page} / {pages}</span>
    <button className="button" onClick={()=>setPage(p=>Math.min(pages,p+1))} disabled={page>=pages}>Next</button></div>
  </div>);
}
