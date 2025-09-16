export function subscribeWS(channels: string[], opts?: {onOpen?: ()=>void,onClose?:()=>void,onError?:(e:any)=>void}) {
  const qs = new URLSearchParams(); channels.forEach(c=>qs.append('channels', c));
  const proto = location.protocol==='https:'?'wss':'ws';
  const host = (location.port==='8080') ? `${location.hostname}:8000` : location.host;
  const url = `${proto}://${host}/ws/subscribe?${qs.toString()}`;
  let ws: WebSocket; let attempts=0; const maxDelay=15000;
  function connect(){
    ws = new WebSocket(url);
    ws.onopen = () => { attempts=0; opts?.onOpen?.(); };
    ws.onclose = () => { opts?.onClose?.(); const delay = Math.min(maxDelay, 500*Math.pow(2, attempts++)); setTimeout(connect, delay); };
    ws.onerror = (e) => { opts?.onError?.(e); };
  }
  connect();
  return new Proxy({} as WebSocket, { get(_, prop){ /* @ts-ignore */ return ws[prop]; }, set(_, prop, value){ /* @ts-ignore */ ws[prop] = value; return true; } });
}
