import pandas as pd
import numpy as np
import logging
import json
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import os
from datetime import datetime
import re

# Настройка логирования
logging.basicConfig(level=logging.INFO, filename='model.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

class FailurePredictor:
    def __init__(self):
        # Инициализация параметров и состояния
        self.model = None
        self.lstm_model = None
        self.scaler = StandardScaler()
        self.config = self.load_config()
        self.log_formats = {
            'default': r'(?P<date>\d{4}-\d{2}-\d{2})\s(?P<time>\d{2}:\d{2}:\d{2})\s(?P<level>\w+)\s(?P<message>.*)',
            'linux_audit': r'type=(?P<type>\w+)\smsg=audit\((?P<date>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d+)\):.*(?P<message>.*)'
        }

    def load_config(self):
        # Загрузка конфигурации из файла, если существует
        default_config = {
            'failure_threshold': 0.7,
            'n_estimators': 100,
            'model_type': 'RandomForest',
            'chunk_size': 10000,
            'auto_fetch_interval': 5,
            'ssh_servers': [],
            'auto_fetch_enabled': False,
            'telegram_token': '',
            'telegram_chat_id': '',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_login': '',
            'smtp_password': '',
            'smtp_receiver': '',
            'webhook_url': ''
        }
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r') as f:
                    config = json.load(f)
                return {**default_config, **config}
            else:
                self.save_config(default_config)
                return default_config
        except Exception as e:
            logging.error(f"Failed to load config: {e}")
            return default_config

    def save_config(self, config):
        # Сохранение конфигурации в файл
        try:
            with open('config.json', 'w') as f:
                json.dump(config, f)
            logging.info("Config saved")
        except Exception as e:
            logging.error(f"Failed to save config: {e}")

    def parse_logs(self, log_paths, custom_regex=None):
        # Парсинг логов из файлов
        all_data = []
        for path in log_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    regex = custom_regex if custom_regex else self.log_formats.get('default', self.log_formats['linux_audit'])
                    entries = re.finditer(regex, content, re.MULTILINE)
                    for entry in entries:
                        data = entry.groupdict()
                        data['source'] = path
                        all_data.append(data)
            except Exception as e:
                logging.error(f"Failed to parse {path}: {e}")
        return pd.DataFrame(all_data) if all_data else pd.DataFrame()

    def feature_engineering(self, df_raw):
        # Генерация признаков из сырых данных
        if df_raw is None or df_raw.empty:
            return pd.DataFrame()
        df = df_raw.copy()
        df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], errors='coerce')
        df['hour'] = df['datetime'].dt.hour
        df['error_count'] = df['level'].str.lower().eq('error').astype(int)
        df['warning_count'] = df['level'].str.lower().eq('warning').astype(int)
        df['fail_keywords'] = df['message'].str.contains('fail|error|crash', case=False, na=False).astype(int)
        df['audit_count'] = df['message'].str.contains('audit', case=False, na=False).astype(int)
        return df.dropna()

    def train(self, df):
        # Обучение модели на основе данных
        if df is None or (isinstance(df, pd.DataFrame) and df.empty):
            raise ValueError("No data provided for training.")
        features = ['error_count', 'warning_count', 'fail_keywords', 'audit_count']
        X = df[features]
        y = (df['fail_keywords'] > 0).astype(int)  # Простая целевая переменная

        X_scaled = self.scaler.fit_transform(X)
        model_type = self.config['model_type']
        if model_type == 'RandomForest':
            self.model = RandomForestClassifier(n_estimators=self.config['n_estimators'], random_state=42)
        elif model_type == 'LogisticRegression':
            self.model = LogisticRegression(random_state=42)
        elif model_type == 'IsolationForest':
            self.model = IsolationForest(n_estimators=self.config['n_estimators'], random_state=42)
        elif model_type == 'LOF':
            self.model = LocalOutlierFactor(novelty=True)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

        if model_type in ['IsolationForest', 'LOF']:
            self.model.fit(X_scaled)
            y_pred = self.model.predict(X_scaled)
            acc = np.mean(y_pred == -1)  # Для аномалий -1 означает сбой
            f1 = 0  # F1 не применим для unsupervised моделей напрямую
        else:
            self.model.fit(X_scaled, y)
            y_pred = self.model.predict(X_scaled)
            acc = np.mean(y_pred == y)
            f1 = 2 * (np.mean(y_pred[y == 1] == 1) * acc) / (np.mean(y_pred[y == 1] == 1) + acc) if acc > 0 else 0

        logging.info(f"Model trained with {model_type}, accuracy: {acc:.2f}, F1: {f1:.2f}")
        return acc, f1

    def predict(self, df):
        # Предсказание с использованием обученной модели
        if df is None or (isinstance(df, pd.DataFrame) and df.empty):
            raise ValueError("No valid data provided for prediction.")
        if not self.model and not self.lstm_model:
            raise ValueError("No model trained or loaded.")
        features = ['error_count', 'warning_count', 'fail_keywords', 'audit_count']
        if not all(feature in df.columns for feature in features):
            raise ValueError(f"Missing features in dataframe: {features}")
        X = df[features]
        X_scaled = self.scaler.transform(X)

        if self.lstm_model:
            X_reshaped = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))
            y_pred = self.lstm_model.predict(X_reshaped, verbose=0)
        else:
            y_pred = self.model.predict_proba(X_scaled)[:, 1]  # Вероятность сбоя

        df_pred = df.copy()
        df_pred['failure_prob'] = y_pred
        alerts = df_pred[df_pred['failure_prob'] > self.config['failure_threshold']].copy()
        return df_pred, alerts

    def train_lstm(self, df):
        # Обучение LSTM модели (опционально)
        if df is None or (isinstance(df, pd.DataFrame) and df.empty):
            raise ValueError("No data provided for LSTM training.")
        features = ['error_count', 'warning_count', 'fail_keywords', 'audit_count']
        X = df[features].values
        y = (df['fail_keywords'] > 0).astype(int).values

        X_scaled = self.scaler.fit_transform(X)
        X_reshaped = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))

        self.lstm_model = Sequential()
        self.lstm_model.add(LSTM(50, return_sequences=True, input_shape=(1, len(features))))
        self.lstm_model.add(LSTM(50))
        self.lstm_model.add(Dense(1, activation='sigmoid'))
        self.lstm_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        self.lstm_model.fit(X_reshaped, y, epochs=10, batch_size=32, verbose=0)
        logging.info("LSTM model trained")
        return self.lstm_model

# Пример использования (можно удалить, если не нужен)
if __name__ == "__main__":
    predictor = FailurePredictor()
    # Здесь можно добавить тестовые данные для отладки