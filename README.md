Шаг 1: Настройка виртуальной среды

Обновите систему:
bashsudo apt update && sudo apt upgrade -y

Установите Python и pip:
Если Python 3.11 отсутствует, добавьте репозиторий и установите:
bashsudo apt install -y python3.11 python3.11-dev python3.11-venv python3-pip

Создайте виртуальную среду:
Выберите директорию для проекта (например, /opt/failure_predictor):
bashsudo mkdir -p /opt/failure_predictor
cd /opt/failure_predictor
python3.11 -m venv failure_predictor_env

Активируйте виртуальную среду:
bashsource failure_predictor_env/bin/activate



Шаг 2: Установка зависимостей

Установите зависимости:
bashpip install -r requirements.txt

Проверьте установки:
Убедитесь, что все пакеты установлены без ошибок:
bashpip list

Шаг 3: Настройка базы данных и конфигурации

Инициализация базы данных:

Файл users.db будет создан автоматически при первом запуске database.py, но вы можете создать его вручную:
bashsqlite3 users.db
Выполните SQL-команды:
sqlCREATE TABLE users (username TEXT PRIMARY KEY, password TEXT, role TEXT);
INSERT INTO users VALUES ('admin', ?, 'admin'); -- Пароль будет зашифрован при первом входе
.exit
(Замените ? на хэш пароля, сгенерированный через bcrypt.hash("admin123") в Python, если нужно).


Создайте директории для логов и ключей:
bashmkdir -p data/remote_logs keys
chmod 755 data keys

Создайте config.json (опционально):
Если вы хотите преднастроить конфигурацию, создайте файл config.json:
bashnano config.json
Вставьте минимальную конфигурацию:
json{
    "failure_threshold": 0.7,
    "n_estimators": 100,
    "model_type": "RandomForest",
    "chunk_size": 10000,
    "auto_fetch_interval": 5,
    "ssh_servers": [],
    "auto_fetch_enabled": false,
    "telegram_token": "",
    "telegram_chat_id": "",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_login": "",
    "smtp_password": "",
    "smtp_receiver": "",
    "webhook_url": ""
}
Сохраните и закройте.



Шаг 4: Запуск приложения

Активируйте виртуальную среду:
bashsource failure_predictor_env/bin/activate

Запустите Streamlit:
bashstreamlit run app.py

Доступ к приложению:

Откройте браузер и перейдите по одному из URL-адресов, указанных в выводе (например, http://localhost:8501 или http://192.168.26.77:8501).
Войдите с учетными данными (по умолчанию: admin/admin123, если база данных настроена).




Шаг 5: Использование приложения

Аутентификация:

Войдите с логином и паролем, заданными в users.db.


Настройка серверов:

Перейдите в раздел "Servers".
Добавьте сервер, указав адрес, порт, пути к логам и учетные данные (SSH-ключ или пароль).
Сохраните настройки.


Загрузка логов:

В разделе "Logs" выберите сервер и нажмите "Fetch Logs" или загрузите локальный файл/папку.
Убедитесь, что логи парсятся корректно (появится сообщение об обработанных записях).


Анализ:

Перейдите в "Analysis".
Нажмите "Train Model" для обучения модели на загруженных данных.
Нажмите "Run Prediction" для получения предсказаний и отображения графиков.


Настройки:

В разделе "Settings" настройте пороги сбоев, интервал автофетча и уведомления (Telegram, Email, Webhook).


Автофетч:

Включите опцию "Auto Fetch Logs" в разделе "Logs" и укажите интервал в настройках.


Дополнительные советы

Безопасность: Храните encryption.key и SSH-ключи в защищенном месте.
Резервное копирование: Регулярно сохраняйте config.json, users.db и папку keys.
Тестирование: Перед развертыванием на продакшене протестируйте на тестовой VM.

Если у вас возникнут проблемы или потребуется помощь с конкретной частью (например, настройка SSH или парсинг логов), предоставьте детали, и я помогу!
