
# УСТАНОВКА AI-Logs НА ДЕBIAN 11 (максимально подробно)

## Краткая версия
1) Распакуйте архив в `~/ai-logs`  
2) Выполните:
```bash
cd ~/ai-logs
chmod +x install.sh
./install.sh
```
3) Откройте `http://<ваш_адрес>:8080`

## Подробная версия (для новичков)
### Что поставится
- **Docker** и **Docker Compose** — чтобы легко запускать все части системы.
- **PostgreSQL** (база данных), **RabbitMQ** (очередь задач), **Redis** (уведомления), **MinIO** (файлы).
- **API (FastAPI)** и **Веб‑интерфейс (React)**.

### Шаги
1. **Скопируйте архив** на сервер (через WinSCP/SFTP/ssh).
2. **Распакуйте** в папку (например, `~/ai-logs`).
3. Откройте терминал и выполните:
   ```bash
   cd ~/ai-logs
   chmod +x install.sh
   ./install.sh
   ```
4. Установщик задаст вопросы:
   - адрес сервера (обычно IP или `localhost`),
   - логин/пароль администратора,
   - параметры хранилища (MinIO по умолчанию),
   - по желанию SSO (OIDC).
5. По окончании установщик **сам запустит** все службы.

### Как проверить
Откройте в браузере:
- Web UI: `http://<адрес>:8080`
- API: `http://<адрес>:8000`
- MinIO: `http://<адрес>:9001` (лог/пароль в `deploy/.env`)
- RabbitMQ: `http://<адрес>:15672` (guest/guest)

### Частые проблемы
- **Нет прав на Docker** → выйдите и зайдите заново или `newgrp docker`.
- **Порт занят** → измените порт в `deploy/docker-compose.yml`.
- **Postgres не успел подняться** → подождите и повторите `docker compose up -d`.

### Перезапуск и остановка
```bash
cd ~/ai-logs/deploy
docker compose --env-file .env up -d --build   # запустить/перезапустить
docker compose --env-file .env down            # остановить
docker compose down -v                         # удалить с данными (необратимо)
```


## Опционально: включение полнотекстового поиска (OpenSearch)
Если хотите искать по текстам находок:
1. Во время `./install.sh` ответьте «y» на вопрос «Включить OpenSearch?».
2. После первого запуска индекс создастся автоматически при первом индексировании.
3. Для уже существующих записей можно пересоздать индекс курлом (по необходимости) — напишите, добавлю скрипт.

## Импорт примера (демо-данные)
1. Откройте Web UI, войдите как admin.
2. На странице «Dashboard» нажмите «Импортировать пример».
3. Перейдите в «Findings» — появятся демонстрационные записи.



## Полная установка с нуля (Debian 11)
1) Скопируйте архив на сервер, распакуйте:
```bash
scp ai-logs-full-debian11-v9.zip user@SERVER:/home/user/
unzip ai-logs-full-debian11-v9.zip -d ~/ai-logs
cd ~/ai-logs
```
2) Запустите установку:
```bash
chmod +x install.sh
./install.sh
```
3) Откройте:
- UI: `http://<IP>:8080`
- API: `http://<IP>:8000/health`
- RabbitMQ: `http://<IP>:15672`
- Flower: `http://<IP>:5555`
- MinIO: `http://<IP>:9001` (логин/пароль в `deploy/.env`)

### Что вписывать и где взять
- **IP/домен** — `hostname -I` или ваш провайдер/админ дал адрес.
- **S3 (если внешний)** — получите endpoint/access/secret в панели вашего облака (Яндекс Облако, AWS, Selectel и т.п.).
- **OIDC/SSO (опционально)** — Client ID/Secret, Discovery URL — в панели вашего провайдера SSO (Keycloak/Okta/Azure AD).

### Проверка и устранение неполадок
- Логи контейнеров:
```bash
cd ~/ai-logs/deploy
docker compose logs -f api
docker compose logs -f worker_parse
docker compose logs -f worker_ml
```
- Пересборка/перезапуск:
```bash
docker compose --env-file .env build api beat worker_parse worker_ml web
docker compose --env-file .env up -d
```
