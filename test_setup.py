#!/usr/bin/env python3
"""
Скрипт для проверки настройки проекта
"""
import sys
import os
import importlib.util

def check_python_version():
    """Проверка версии Python"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - требуется Python 3.8+")
        return False

def check_dependencies():
    """Проверка установленных зависимостей"""
    required_packages = [
        'flask', 'flask_sqlalchemy', 'aiogram', 'openai', 
        'httpx', 'pydantic_settings', 'yookassa'
    ]
    
    missing = []
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing.append(package)
        else:
            print(f"✅ {package}")
    
    if missing:
        print(f"❌ Отсутствуют пакеты: {', '.join(missing)}")
        print("Выполните: pip install -r requirements.txt")
        return False
    
    return True

def check_env_file():
    """Проверка файла .env"""
    if os.path.exists('.env'):
        print("✅ Файл .env найден")
        
        # Проверка основных переменных
        with open('.env', 'r') as f:
            content = f.read()
            
        required_vars = ['BOT_TOKEN', 'OPENAI_API_KEY']
        missing_vars = []
        
        for var in required_vars:
            if var not in content or f"{var}=your_" in content:
                missing_vars.append(var)
        
        if missing_vars:
            print(f"⚠️ Не настроены переменные: {', '.join(missing_vars)}")
            return False
        else:
            print("✅ Основные переменные настроены")
            return True
    else:
        print("❌ Файл .env не найден")
        print("Скопируйте .env.example в .env и настройте переменные")
        return False

def check_files():
    """Проверка наличия основных файлов"""
    required_files = [
        'bot.py', 'app.py', 'run_all.py', 'handlers.py', 
        'models.py', 'routes.py', 'extensions.py', 'requirements.txt'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            missing.append(file)
    
    if missing:
        print(f"❌ Отсутствуют файлы: {', '.join(missing)}")
        return False
    
    return True

def main():
    print("🔍 Проверка настройки проекта Telegram Bot + Flask")
    print("=" * 50)
    
    all_good = True
    
    print("\n📦 Проверка Python:")
    all_good &= check_python_version()
    
    print("\n📚 Проверка файлов:")
    all_good &= check_files()
    
    print("\n🔧 Проверка зависимостей:")
    all_good &= check_dependencies()
    
    print("\n⚙️ Проверка конфигурации:")
    all_good &= check_env_file()
    
    print("\n" + "=" * 50)
    
    if all_good:
        print("🎉 Всё готово к запуску!")
        print("\nДля запуска выполните:")
        print("  python run_all.py")
    else:
        print("❌ Обнаружены проблемы. Устраните их перед запуском.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())