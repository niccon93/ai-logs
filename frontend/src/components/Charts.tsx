import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, BarChart, Bar, Legend } from 'recharts';
export function LineSeries({data,xKey,yKey}:{data:any[],xKey:string,yKey:string}){
  return (<div style={{width:'100%',height:300}}>
    <ResponsiveContainer><LineChart data={data}>
      <CartesianGrid strokeDasharray="3 3"/><XAxis dataKey={xKey}/><YAxis/><Tooltip/><Legend/>
      <Line type="monotone" dataKey={yKey} dot={false}/>
    </LineChart></ResponsiveContainer></div>);
}
export function BarSeries({data,xKey,yKey}:{data:any[],xKey:string,yKey:string}){
  return (<div style={{width:'100%',height:300}}>
    <ResponsiveContainer><BarChart data={data}>
      <CartesianGrid strokeDasharray="3 3"/><XAxis dataKey={xKey}/><YAxis/><Tooltip/><Legend/><Bar dataKey={yKey}/>
    </BarChart></ResponsiveContainer></div>);
}
