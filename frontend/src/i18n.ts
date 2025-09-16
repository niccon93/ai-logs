
import i18n from 'i18next'; import { initReactI18next } from 'react-i18next';
const resources = {
  en: { translation: { dashboard: 'Dashboard', sources: 'Sources', accounts:'Accounts', anomalies:'Anomalies', run:'Run', train:'Train', infer:'Detect', settings:'Settings', jobs:'Jobs', charts:'Charts', findings:'Findings', login:'Login', otp:'OTP (if enabled)' }},
  ru: { translation: { dashboard: 'Дашборд', sources: 'Источники', accounts:'Учётные записи', anomalies:'Аномалии', run:'Запустить', train:'Обучить', infer:'Детект', settings:'Настройки', jobs:'Задачи', charts:'Графики', findings:'Находки', login:'Войти', otp:'OTP (если включено)' }},
};
i18n.use(initReactI18next).init({ resources, lng: 'ru', fallbackLng: 'en', interpolation: { escapeValue: false } });
export default i18n;
