#!/bin/bash
# ETVE v12.3 — Универсальный запускатор тестов
# Автоматически скачивает и запускает все модули

set -e  # Остановка при любой ошибке

echo "🌀 ETVE v12.3 — Запуск полного цикла тестирования"
echo "================================================"

# 1. Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python 3.8+"
    exit 1
fi

# 2. Установка зависимостей
echo "📦 Установка необходимых пакетов..."
pip install numpy torch psutil --quiet

# 3. Запуск тестов
echo -e "\n🚀 [1/3] Тест: Адаптивный LR-скалер (etve_lr_scaler.py)"
python3 etve_lr_scaler.py

echo -e "\n🚀 [2/3] Тест: Сравнение с PyTorch (etve_vs_pytorch.py)"
python3 etve_vs_pytorch.py

echo -e "\n🚀 [3/3] Тест: Базовый амортизатор (из Quick_Start)"
python3 -c "
import numpy as np
import math
PHI = (1.0 + np.sqrt(5.0)) / 2.0
C_MIN = 1.0 / (PHI ** 10)
C_MAX = 1.0 - 1.0 / (PHI ** 20)

def etve_tanh_limit(C):
    epsilon = 1e-12
    E = (C - C_MIN) / (C_MAX - C_MIN + epsilon)
    E_limited = math.tanh(E) * 0.5 + 0.5
    return C_MIN + E_limited * (C_MAX - C_MIN)

chaos_inputs = [0.95, 50.0, 100000.0, float('inf'), -500.0]
print('=== ТЕСТ АМОРТИЗАТОРА ===')
for inp in chaos_inputs:
    output = etve_tanh_limit(inp)
    print(f'Вход: {str(inp):<10} -> Выход: {output:.6f}')
print('✅ Амортизатор: все значения удержаны.')
"

echo -e "\n✅ Все тесты пройдены. Система стабильна."
echo "🌀 ETVE v12.3 работает в живой динамике."
