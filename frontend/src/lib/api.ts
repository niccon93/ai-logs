const API_BASE = (location.port === '8080') ? `${location.protocol}//${location.hostname}:8000` : '';
export async function api(path: string, opts: RequestInit = {}){
  const token = localStorage.getItem('token') || '';
  const headers = new Headers(opts.headers || {});
  if(token) headers.set('Authorization', `Bearer ${token}`);
  headers.set('Content-Type','application/json');
  const res = await fetch(`${API_BASE}${path}`, { ...opts, headers });
  if(!res.ok) throw new Error(`API error ${res.status}`);
  return res.json();
}
