// Базовые настройки
const API_BASE = '/api'; // nginx проксирует /api/* -> http://api:8000

const els = {
  health: document.getElementById('health'),
  authStatus: document.getElementById('authStatus'),
  loginCard: document.getElementById('loginCard'),
  adminCard: document.getElementById('adminCard'),
  btnReady: document.getElementById('btnReady'),
  btnLive: document.getElementById('btnLive'),
  btnLogin: document.getElementById('btnLogin'),
  btnLogout: document.getElementById('btnLogout'),
  btnImport1: document.getElementById('btnImport1'),
  btnImport2: document.getElementById('btnImport2'),
  importStatus: document.getElementById('importStatus'),
  username: document.getElementById('username'),
  password: document.getElementById('password'),
};

function getToken() { return localStorage.getItem('ailogs_token') || ''; }
function setToken(t) {
  if (t) localStorage.setItem('ailogs_token', t);
  else localStorage.removeItem('ailogs_token');
  renderAuth();
}

function parseJwt(token) {
  try {
    const [, payload] = token.split('.');
    return JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')));
  } catch { return null; }
}

async function api(path, { method='GET', body, headers={} } = {}) {
  const token = getToken();
  const h = { 'Content-Type': 'application/json', ...headers };
  if (token) h['Authorization'] = `Bearer ${token}`;
  const res = await fetch(API_BASE + path, { method, headers: h, body: body ? JSON.stringify(body) : undefined });
  const text = await res.text();
  let data;
  try { data = JSON.parse(text); } catch { data = text; }
  if (!res.ok) {
    const msg = (data && data.detail) ? data.detail : res.status + ' ' + res.statusText;
    throw new Error(msg);
  }
  return data;
}

async function ping(path, label) {
  try {
    const data = await api(path);
    els.health.textContent = `${label}: ${typeof data === 'string' ? data : JSON.stringify(data)}`;
    els.health.className = 'ok';
  } catch (e) {
    els.health.textContent = `${label}: ошибка — ${e.message}`;
    els.health.className = 'err';
  }
}

async function login() {
  els.authStatus.textContent = 'вход...';
  try {
    const data = await api('/auth/login', {
      method: 'POST',
      body: {
        username: els.username.value.trim(),
        password: els.password.value
      }
    });
    if (data && data.access_token) {
      setToken(data.access_token);
      els.authStatus.textContent = 'вход выполнен';
    } else {
      throw new Error('Сервер не вернул access_token');
    }
  } catch (e) {
    els.authStatus.textContent = 'ошибка входа: ' + e.message;
    els.authStatus.className = 'err';
  }
}

function logout() { setToken(''); }

async function importDemoVariant1() {
  els.importStatus.textContent = 'импорт...';
  els.importStatus.className = 'muted';
  try {
    // На разных версиях бэка названия расходятся — попробуем по очереди
    const tryPaths = ['/examples/seed', '/examples/import', '/admin/examples/seed'];
    let ok = false, lastErr = '';
    for (const p of tryPaths) {
      try { await api(p, { method: 'POST' }); ok = true; break; }
      catch (e) { lastErr = e.message; }
    }
    if (!ok) throw new Error(lastErr || 'эндпоинт не найден');
    els.importStatus.textContent = 'импорт завершён';
    els.importStatus.className = 'ok';
  } catch (e) {
    els.importStatus.textContent = 'ошибка импорта: ' + e.message + ' (нужны права admin и валидный вход)';
    els.importStatus.className = 'err';
  }
}

async function importDemoVariant2() {
  // Вдруг где-то нужен GET — попробуем альтернативно
  els.importStatus.textContent = 'импорт...';
  els.importStatus.className = 'muted';
  try {
    await api('/examples/import', { method: 'GET' });
    els.importStatus.textContent = 'импорт завершён';
    els.importStatus.className = 'ok';
  } catch (e) {
    els.importStatus.textContent = 'ошибка импорта: ' + e.message;
    els.importStatus.className = 'err';
  }
}

function renderAuth() {
  const token = getToken();
  if (!token) {
    els.btnLogin.classList.remove('hidden');
    els.btnLogout.classList.add('hidden');
    els.adminCard.classList.add('hidden');
    els.authStatus.textContent = 'не авторизован';
    els.authStatus.className = 'muted';
    return;
  }
  els.btnLogin.classList.add('hidden');
  els.btnLogout.classList.remove('hidden');

  const payload = parseJwt(token) || {};
  const role = payload.role || payload.roles || 'unknown';
  els.authStatus.textContent = `авторизован, роль: ${JSON.stringify(role)}`;
  els.authStatus.className = 'ok';

  // простая логика: показываем админ-карточку, если есть "admin" в payload
  const isAdmin = (role === 'admin') || (Array.isArray(role) && role.includes('admin'));
  if (isAdmin) els.adminCard.classList.remove('hidden');
  else els.adminCard.classList.add('hidden');
}

// события
els.btnReady.addEventListener('click', () => ping('/ready', '/ready'));
els.btnLive.addEventListener('click', () => ping('/live', '/live'));
els.btnLogin.addEventListener('click', login);
els.btnLogout.addEventListener('click', logout);
els.btnImport1.addEventListener('click', importDemoVariant1);
els.btnImport2.addEventListener('click', importDemoVariant2);

// Инициализация
renderAuth();
