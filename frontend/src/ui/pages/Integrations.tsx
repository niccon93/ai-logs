import React from 'react'
export default function Integrations(){
  return (<div><h2>Интеграции</h2><ul>
    <li>Telegram: будет добавлен webhook + настройка чатов.</li>
    <li>S3/MinIO: используется для хранения артефактов; настройки в .env.</li>
    <li>OpenSearch: опционально docker-compose.opensearch.yml.</li>
  </ul></div>)
}
