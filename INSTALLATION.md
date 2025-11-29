# 🚀 Prompt Optimizer SaaS - Инструкция по запуску

## 📦 Установка

1. **Распакуйте архив** `prompt-optimizer-saas.tar.gz`

2. **Установите Python 3.10+** (если еще не установлен)
   - Скачайте с https://www.python.org/downloads/

3. **Установите зависимости backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

## 🔑 Настройка API ключей

### Вариант 1: Через UI (рекомендуется)
Просто введите ваши API ключи в веб-интерфейсе при запуске

### Вариант 2: Через .env файл
1. Скопируйте `backend/.env.example` в `backend/.env`
2. Добавьте ваши ключи:
   ```
   GEMINI_API_KEY=your_gemini_key_here
   XAI_API_KEY=your_xai_key_here
   ```

### Получение API ключей:
- **Gemini**: https://makersuite.google.com/app/apikey
- **Grok (xAI)**: https://console.x.ai/

## 🚀 Быстрый запуск

### Windows:

1. **Запустите backend:**
   - Двойной клик на `start_backend.bat`
   - ИЛИ в командной строке:
     ```bash
     start_backend.bat
     ```
   - Backend запустится на http://localhost:8000
   - Swagger UI: http://localhost:8000/docs

2. **Запустите frontend:**
   - Двойной клик на `start_frontend.bat`
   - ИЛИ в командной строке:
     ```bash
     start_frontend.bat
     ```
   - Frontend откроется на http://localhost:8080

### Linux/Mac:

1. **Backend:**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Frontend:**
   ```bash
   cd frontend
   python -m http.server 8080
   ```
   Затем откройте http://localhost:8080

## 📖 Использование

1. Откройте http://localhost:8080 в браузере
2. Выберите LLM backend (Gemini или Grok)
3. Введите API ключ для выбранного провайдера
4. Настройте параметры (опционально):
   - Max D/S Iterations (1-6)
   - Convergence Threshold (0.01-0.20)
5. Введите промпт для оптимизации
6. Нажмите "Optimize Prompt"
7. Изучите результаты:
   - Smart Queue Analysis
   - PCV (Proposer-Critic-Verifier)
   - D/S Cycle iterations
   - Final optimized prompt
   - Quality evaluation
   - Metrics

## 🔧 Структура проекта

```
prompt-optimizer-saas/
├── backend/                    # FastAPI бэкенд
│   ├── app/
│   │   ├── main.py            # Главный файл FastAPI
│   │   ├── config.py          # Конфигурация
│   │   ├── models/            # Pydantic схемы
│   │   ├── services/          # Бизнес-логика
│   │   │   ├── llm_provider.py    # LLM провайдеры
│   │   │   └── optimizer.py       # Оптимизация промптов
│   │   ├── api/               # API endpoints
│   │   └── utils/             # Утилиты
│   └── requirements.txt
├── frontend/                   # HTML/JS фронтенд
│   ├── index.html             # Главная страница
│   ├── components/            # Модульные компоненты
│   │   ├── smart-queue.js
│   │   ├── pcv-display.js
│   │   ├── ds-display.js
│   │   ├── evaluation-display.js
│   │   └── metrics-display.js
│   └── static/
│       ├── css/
│       │   ├── main.css
│       │   └── components.css
│       └── js/
│           ├── api-client.js
│           └── app.js
├── start_backend.bat          # Запуск backend (Windows)
├── start_frontend.bat         # Запуск frontend (Windows)
└── README.md
```

## 🎯 API Endpoints

### Health Check
```
GET http://localhost:8000/api/health
```

### Optimize Prompt
```
POST http://localhost:8000/api/optimize
Content-Type: application/json

{
  "prompt": "Your prompt here",
  "backend": "gemini",
  "gemini_api_key": "your_key",
  "max_iterations": 3,
  "convergence_threshold": 0.05,
  "force_optimization": true
}
```

Swagger UI со всей документацией: http://localhost:8000/docs

## 🔍 Как работает пайплайн

1. **Smart Queue** - Анализирует промпт и решает, нужна ли оптимизация
   - Оценивает clarity, structure, constraints (0-1)
   - Рекомендует оптимизацию или нет

2. **Proposer-Critic-Verifier (PCV)**
   - **Proposer**: Переписывает промпт с улучшенной структурой
   - **Critic**: Анализирует предложение и дает критику
   - **Verifier**: Создает финальную версию с учетом критики

3. **D/S Cycle** (Diversification/Stabilization)
   - **D-Block**: Расширяет промпт деталями
   - **S-Block**: Стабилизирует и удаляет избыточность
   - Повторяется до конвергенции или max_iterations

4. **Pairwise Evaluation**
   - Сравнивает исходный и финальный промпт
   - Оценивает улучшения по 4 осям

## ⚙️ Продвинутые настройки

### Backend конфигурация (backend/.env):
```env
# Models
GEMINI_MODEL=gemini-2.5-flash  # или gemini-2.5-pro
GROK_MODEL=grok-4

# Timeouts
CONNECT_TIMEOUT=10
READ_TIMEOUT=120

# D/S Cycle defaults
MAX_DS_ITERATIONS=3
CONVERGENCE_THRESHOLD=0.05
```

### Изменение порта backend:
В `backend/app/config.py` измените:
```python
PORT: int = 8000  # ваш порт
```

### CORS настройки:
В `backend/app/main.py` измените:
```python
allow_origins=["http://localhost:8080"]  # ваш origin
```

## 🐛 Troubleshooting

### Backend не запускается:
- Проверьте, установлен ли Python 3.10+
- Проверьте, установлены ли зависимости: `pip install -r backend/requirements.txt`
- Проверьте, свободен ли порт 8000

### Frontend не подключается к backend:
- Убедитесь, что backend запущен на http://localhost:8000
- Проверьте CORS настройки в backend
- Откройте консоль браузера (F12) для ошибок

### API ключи не работают:
- Проверьте правильность ключа
- Убедитесь, что выбран правильный backend (Gemini/Grok)
- Проверьте квоты API

### Ошибка "Module not found":
```bash
cd backend
pip install -r requirements.txt --force-reinstall
```

## 📝 TODO для продакшена

- [ ] Database для истории оптимизаций
- [ ] User authentication
- [ ] Rate limiting
- [ ] Кеширование результатов
- [ ] WebSocket для real-time обновлений
- [ ] Более продвинутые метрики (semantic similarity)
- [ ] A/B тестирование промптов
- [ ] Export в разные форматы
- [ ] Batch processing
- [ ] API key management UI

## 📞 Поддержка

Для вопросов и багов создайте issue или обратитесь к документации API в Swagger UI.

---

**Версия**: 1.0.0  
**Дата**: 2024
