
# ИСПОЛЬЗОВАНИЕ (подробно, с примерами)

## Вход
1) Перейдите на `http://<адрес>:8080` → «Войти».  
2) Введите логин/пароль администратора.  
3) Если включён SSO, нажмите «SSO (если настроено)».

### Включение 2FA (TOTP)
- Получить токен входа:
```bash
curl -s -X POST http://<адрес>:8000/auth/login -H 'Content-Type: application/json' -d '{"username":"admin","password":"admin123"}'
```
- В ответе найдите `access_token` и подставьте:
```bash
TOKEN=<вставьте_тут_токен>
curl -s http://<адрес>:8000/mfa/setup -H "Authorization: Bearer $TOKEN"
```
- Добавьте секрет в приложение‑авторизатор, затем:
```bash
curl -s -X POST http://<адрес>:8000/mfa/enable -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"code":"123456"}'
```
- Теперь при входе вводите OTP.

## Разделы
- **Dashboard** — базовые графики.
- **Findings** — таблица событий: фильтр по тексту, важности, постранично.
- **Jobs** — лента статусов задач в реальном времени (Redis pub/sub + Streams).

## Добавление серверной учётки и источника
1) Войти и получить токен:
```bash
curl -s -X POST http://<адрес>:8000/auth/login -H 'Content-Type: application/json' -d '{"username":"admin","password":"admin123"}'
TOKEN=<вставьте сюда>
```
2) Добавить SSH‑учётку:
```bash
curl -s -X POST http://<адрес>:8000/server-accounts/   -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json"   -d '{"name":"prod01","host":"10.0.0.10","port":22,"username":"root","auth_type":"password","password":"SecretPass!"}'
```
3) Добавить источник логов:
```bash
curl -s -X POST http://<адрес>:8000/sources   -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json"   -d '{"type":"local","path":"/var/log/nginx/","tags":{"env":"prod","app":"nginx"}}'
```

## Просмотр находок
Перейдите в **Findings**, используйте поиск/фильтры. Для больших объёмов — переключайте размер страницы (20/50/100).

## Хранилище S3/MinIO
По умолчанию — MinIO (`http://<адрес>:9001`). Параметры — в `deploy/.env`.  
Чтобы использовать внешнее S3 — замените `S3_ENDPOINT`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_BUCKET`, `S3_REGION` и перезапустите.

## Диагностика
```bash
cd deploy
docker compose ps               # какие контейнеры запущены
docker compose logs -f api      # логи API
docker compose logs -f worker   # логи worker
docker compose logs -f web      # логи фронтенда
```


## Импорт логов из локального каталога (простая проверка)
Команда отправляет путь на сервер API (контейнер), где читаются файлы:
```bash
TOKEN=<ваш токен>
curl -s -X POST http://<адрес>:8000/ingest/local   -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json"   -d '{"path":"/var/log","parser_hint":"auto"}'
```
> Примечание: для NGINX/Apache в примере добавлен простой разбор строк и «находки» для ответов **5xx**.

## Поиск и индексация в OpenSearch (если включён)
- Переменная окружения `ENABLE_OPENSEARCH=1` включает индексирование новых находок в индекс `findings`.
- Параметры подключения: `OPENSEARCH_HOST`, `OPENSEARCH_PORT` (см. `deploy/docker-compose.opensearch.yml`).

## Тёмная тема и сохранённые фильтры
- Переключатель «Dark/Light» в шапке.
- Фильтры в разделе «Findings» запоминаются между сессиями (LocalStorage).

## Экраны по ролям (RBAC)
- Пункт меню «Admin» виден только роли `admin`.
- Эндпоинт `/users` доступен только администраторам.


## Использование: очереди задач и сценарии
- `worker_parse` обрабатывает задачи `parse.*` и содержит `drain3` (без LogAI).
- `worker_ml` обрабатывает задачи `ml.*` и содержит LogAI/Loglizer (без drain3).

### Пример: демо-парсинг
Через Flower (`http://<IP>:5555` → Tasks) отправьте `parse.run` с аргументами:
```json
{"dataset_id": 1, "lines": ["error line one", "warning line two"]}
```

### Пример: тренировка и инференс
Отправьте `ml.train`:
```json
{"dataset_id": 1, "backend": "logai", "params": {}}
```
и затем `ml.infer`:
```json
{"dataset_id": 1, "model_id": 1, "backend": "logai", "params": {}}
```

## S3/MinIO хранение
По умолчанию запущен MinIO (локально). Для внешнего S3 — меняйте `deploy/.env` и перезапускайте `docker compose`.
