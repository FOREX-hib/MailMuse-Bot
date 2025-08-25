# Telegram Bot + Flask Web Dashboard

Интегрированное приложение, включающее Telegram бота для генерации email-рассылок и веб-дашборд для мониторинга.

## 🚀 Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка переменных окружения
Создайте файл `.env` или установите переменные окружения:
```bash
export BOT_TOKEN="your_telegram_bot_token"
export OPENAI_API_KEY="your_openai_api_key"
export DATABASE_URL="sqlite:///telegram_bot.db"  # опционально
export SESSION_SECRET="your_secret_key"  # опционально
```

### 3. Запуск приложения

#### Вариант 1: Запуск всего одной командой
```bash
python run_all.py
```

#### Вариант 2: Отдельный запуск
```bash
# В одном терминале - Telegram бот
python bot.py

# В другом терминале - Flask веб-приложение
python app.py
```

#### Вариант 3: Только Flask приложение
```bash
python app.py
```

## 📊 Веб-дашборд

После запуска откройте в браузере: http://localhost:5000

### Доступные эндпоинты:
- `/` - Главная страница с статистикой
- `/api/users` - Список пользователей
- `/api/messages` - Список сообщений
- `/api/stats` - Статистика бота
- `/health` - Проверка состояния

## 🗄️ База данных

Приложение использует SQLite базу данных с двумя таблицами:
- `users` - Пользователи Telegram
- `messages` - Сообщения от пользователей

База данных создается автоматически при первом запуске.

## 🔧 Структура проекта

```
├── app.py              # Flask веб-приложение
├── bot.py              # Telegram бот
├── run_all.py          # Запуск обоих приложений
├── extensions.py       # Конфигурация SQLAlchemy
├── models.py           # Модели базы данных
├── routes.py           # Flask маршруты
├── bot_integration.py  # Интеграция бота с БД
├── handlers.py         # Обработчики Telegram бота
├── keyboards.py        # Клавиатуры для бота
├── middleware.py       # Middleware для бота
├── config.py           # Конфигурация
├── utils.py            # Утилиты
└── requirements.txt    # Зависимости
```

## 🔗 API примеры

### Создание пользователя
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"telegram_id": 123456789, "username": "testuser", "first_name": "Test"}'
```

### Получение статистики
```bash
curl http://localhost:5000/api/stats
```

## 🐛 Отладка

Логи выводятся в консоль. Для увеличения детализации измените уровень логирования в файлах `app.py` и `bot.py`.

## 📝 Примечания

- При первом запуске база данных создается автоматически
- Все пользователи, взаимодействующие с ботом, автоматически сохраняются в БД
- Веб-дашборд обновляется в реальном времени при использовании бота