#!/usr/bin/env python3
"""
Скрипт для генерации .env.example файла
"""
import os
import sys

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from config.env.example import generate_env_example
    
    # Генерируем содержимое
    content = generate_env_example()
    
    # Записываем в файл
    output_file = os.path.join(os.path.dirname(__file__), '..', '.env.example')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ .env.example успешно сгенерирован: {output_file}")
    
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Убедитесь, что config/env/validator.py доступен")
    sys.exit(1)
except Exception as e:
    print(f"❌ Ошибка генерации: {e}")
    sys.exit(1)
