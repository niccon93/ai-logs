import { useEffect, useState } from 'react';
import { subscribeWS } from '../lib/ws';
import DataTable from '../components/DataTable';
export default function JobsStream(){
  const [rows,setRows]=useState<any[]>([]);
  useEffect(()=>{
    const ws=subscribeWS(['jobs:all']);
    ws.onmessage=(e:any)=>{ try{ const m=JSON.parse(e.data); setRows(prev=>[m.data||m,...prev].slice(0,500)); }catch{} };
    return ()=>ws.close();
  },[]);
  return (<div className="container"><h2>Jobs stream</h2>
    <div className="card"><DataTable rows={rows} columns={[{key:'task_id',label:'Task'},{key:'stage',label:'Stage'},{key:'progress',label:'%'}]}/></div></div>);
}
