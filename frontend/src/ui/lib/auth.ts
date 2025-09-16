export function getToken(): string | null { return localStorage.getItem('token') }
export function getRole(): 'admin' | 'user' {
  return (localStorage.getItem('role') as any) || 'user'
}
export function setRole(r: 'admin'|'user') { localStorage.setItem('role', r) }
