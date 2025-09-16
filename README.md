# AI-Logs (Debian 11, Docker Compose)

Полностью офлайн-пакет для развертывания AI-Logs на Debian 11 (Bullseye). 
Состав:
- Backend (FastAPI + SQLAlchemy + Alembic + Celery + Redis + RabbitMQ)
- Frontend (Vite + React, сборка в nginx; SPA fallback)
- PostgreSQL, Redis, RabbitMQ
- Опционально: OpenSearch + Dashboards
- Скрипт установки `install.sh` с автоконфигом `.env` и запуском контейнеров

## Быстрый старт
1) Скопируйте архив на ВМ Debian 11 и распакуйте:
```bash
unzip ai-logs-full-debian11-v10.zip -d /mnt
cd /mnt/ai-logs-full-debian11-v10
chmod +x install.sh
./install.sh
```
2) Ответьте на вопросы установщика. Он:
   - Установит Docker и docker compose
   - Сгенерирует ключи `FERNET_KEYS` и `JWT_SECRET`
   - Подставит адреса в `.env` (API_URL/FRONTEND_URL/CORS)
   - Поднимет контейнеры; при выборе — подключит OpenSearch

3) Откройте:
- API (здоровье): `http://<IP>:8000/ready`
- Веб-интерфейс: `http://<IP>:8080`

## Учётные данные администратора
Задаются в `install.sh`. По умолчанию:
```
admin / admin123
```

## Траблшутинг
- Если в логах API видите проблемы с `KeysView`/`ValuesView`, это починено файлом `sitecustomize.py` (подмешивает классы из `collections.abc`).
- Если включаете OpenSearch на малой памяти, выставьте `OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m` и swappiness в хосте.
- Если фронт выдаёт 404 при переключении вкладок — включён SPA fallback в nginx (`deploy/nginx.conf`).

## Обновление
```bash
docker compose --env-file deploy/.env -f deploy/docker-compose.yml up -d --build
```
