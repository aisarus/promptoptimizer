# Prompt Optimizer SaaS - DEV VERSION

**⚠️ DEVELOPMENT VERSION - Uses ports 8001/8081**

This is the development copy for safe experimentation.
- **DEV Backend:** http://localhost:8001
- **DEV Frontend:** http://localhost:8081
- **Production version** (original) uses ports 8000/8080

---

## Архитектура проекта

```
prompt-optimizer-saas/
├── backend/                    # FastAPI бэкенд
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # Главный файл FastAPI
│   │   ├── config.py          # Конфигурация
│   │   ├── models/            # Pydantic модели
│   │   ├── services/          # Бизнес-логика
│   │   ├── api/               # API endpoints
│   │   └── utils/             # Утилиты
│   ├── requirements.txt
│   └── .env.example
├── frontend/                   # HTML/JS/CSS фронтенд
│   ├── index.html             # Главная страница
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── assets/
│   └── components/            # Модульные компоненты
├── start_backend.bat          # Запуск FastAPI
├── start_frontend.bat         # Запуск frontend сервера
└── README.md
```

## Запуск проекта

### Вариант 1: Быстрый запуск (Windows)
Двойной клик на **`start_all.bat`** - запустит Backend + Frontend одновременно

### Вариант 2: Раздельный запуск
- **Backend**: Двойной клик `start_backend.bat` → Swagger UI откроется автоматически
- **Frontend**: Двойной клик `start_frontend.bat` → UI откроется автоматически

### Вариант 3: Ручной запуск
```bash
# Backend
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
# Swagger UI: http://localhost:8000/docs

# Frontend
cd frontend
python -m http.server 8080
# UI: http://localhost:8080
```

## API Endpoints

- `POST /api/optimize` - Оптимизация промпта
- `GET /api/history` - История оптимизаций
- `GET /api/health` - Healthcheck
