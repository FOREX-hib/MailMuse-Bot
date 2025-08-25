# 🚀 Быстрый запуск проекта

## 1. Распаковка архива
```bash
# Распакуйте архив в папку проекта
unzip telegram_bot_project.zip -d telegram_bot_project/
cd telegram_bot_project/

# ИЛИ для .tar.gz:
# tar -xzf telegram_bot_project.tar.gz -C telegram_bot_project/
```

## 2. Настройка окружения
```bash
# Скопируйте файл с переменными окружения
cp .env.example .env

# Отредактируйте .env файл и укажите ваши токены:
nano .env
```

### Обязательные переменные:
- `BOT_TOKEN` - токен вашего Telegram бота (получить у @BotFather)
- `OPENAI_API_KEY` - API ключ OpenAI/OpenRouter

## 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

## 4. Запуск
```bash
# Запуск всего проекта (бот + веб-дашборд)
python run_all.py

# ИЛИ запуск только бота:
# python bot.py

# ИЛИ запуск только веб-приложения:
# python app.py
```

## 5. Проверка работы
- Напишите боту в Telegram: `/start`
- Откройте в браузере: http://localhost:5000
- Проверьте статистику и API

## 🔧 Troubleshooting

### Ошибка модулей:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Проблемы с базой данных:
```bash
# Удалите файл БД и перезапустите
rm telegram_bot.db
python run_all.py
```

### Проверка портов:
```bash
# Убедитесь что порт 5000 свободен
lsof -i :5000
```

## 📁 Структура файлов
- `bot.py` - Telegram бот
- `app.py` - Flask веб-приложение  
- `run_all.py` - Запуск всего проекта
- `handlers.py` - Обработчики бота
- `models.py` - Модели базы данных
- `routes.py` - Веб-маршруты
- `README.md` - Подробная документация