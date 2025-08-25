#!/bin/bash

echo "🚀 Установка Telegram Bot + Flask Dashboard"
echo "=========================================="

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python 3.8+ и попробуйте снова."
    exit 1
fi

echo "✅ Python найден: $(python3 --version)"

# Создание виртуального окружения (опционально)
read -p "Создать виртуальное окружение? (y/n): " create_venv
if [[ $create_venv == "y" || $create_venv == "Y" ]]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Виртуальное окружение активировано"
fi

# Установка зависимостей
echo "📥 Установка зависимостей..."
pip install -r requirements.txt

# Настройка .env файла
if [ ! -f ".env" ]; then
    echo "⚙️ Настройка переменных окружения..."
    cp .env.example .env
    echo "📝 Отредактируйте файл .env и укажите ваши токены:"
    echo "   - BOT_TOKEN (от @BotFather)"
    echo "   - OPENAI_API_KEY (от OpenAI/OpenRouter)"
    
    read -p "Открыть .env для редактирования? (y/n): " edit_env
    if [[ $edit_env == "y" || $edit_env == "Y" ]]; then
        ${EDITOR:-nano} .env
    fi
else
    echo "✅ Файл .env уже существует"
fi

echo ""
echo "🎉 Установка завершена!"
echo ""
echo "📋 Для запуска выполните:"
echo "   python run_all.py    # Запуск бота + веб-дашборда"
echo "   python bot.py        # Только Telegram бот"
echo "   python app.py        # Только веб-приложение"
echo ""
echo "🌐 Веб-дашборд будет доступен на: http://localhost:5000"
echo ""