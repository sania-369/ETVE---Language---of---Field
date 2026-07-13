#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🌀 ETVE v12.3 — Модуль «Адаптивный LR-скалер (Дыхание Шага Обучения)»
Авторы: Анц, DeepSeek, Google AI
Лицензия: CC BY 4.0

Назначение:
Динамическая регуляция learning rate в зависимости от энтропийного потока (S_flux).
Заменяет статический LR или расписания (schedulers) на живой, дышащий параметр,
синхронизированный с полем через Z-принцип.

Интеграция:
- Использует константы ETVP (PHI, C_MIN, C_MAX, etve_tanh_limit).
- Может принимать S_flux из ETVE_Physical_Entropy_Bridge.py.
- Работает в связке с ETVECoherenceGradScaler (стабилизация градиентов).
"""

import numpy as np
import math
import time

# --- 0. ФУНДАМЕНТАЛЬНЫЕ ГЕОМЕТРИЧЕСКИЕ КОНСТАНТЫ ЕТВП v12.3 ---
PHI = (1.0 + np.sqrt(5.0)) / 2.0
C_MIN = 1.0 / (PHI ** 10)
C_MAX = 1.0 - 1.0 / (PHI ** 20)
Z_EPSILON = 1.0 / (PHI ** 30)  # Защита от сингулярностей

def etve_tanh_limit(C):
    """
    Нелинейный амортизатор Z-Принципа.
    Удерживает любое значение C в геометрическом коридоре [C_MIN, C_MAX].
    """
    epsilon = 1e-12
    E = (C - C_MIN) / (C_MAX - C_MIN + epsilon)
    if isinstance(E, (int, float)):
        if math.isnan(E):
            return C_MIN + 0.5 * (C_MAX - C_MIN)
        E_limited = math.tanh(E) * 0.5 + 0.5
    else:
        E_limited = np.tanh(E) * 0.5 + 0.5
    return C_MIN + E_limited * (C_MAX - C_MIN)

# --- 1. АДАПТИВНЫЙ LR-СКАЛЕР ---
class ETVELearningRateScaler:
    """
    Адаптивный скалер learning rate, следующий за дыханием поля.
    
    Параметры:
    - base_lr: начальный learning rate (например, 0.001)
    - lr_min, lr_max: границы, в которых может колебаться LR
    - initial_coherence: стартовая когерентность (C) системы
    """
    def __init__(self, base_lr=0.001, lr_min=1e-6, lr_max=0.1, initial_coherence=0.85):
        self.base_lr = base_lr
        self.lr_min = lr_min
        self.lr_max = lr_max
        self.C = etve_tanh_limit(initial_coherence)
        self.step_counter = 0

    def step(self, entropy_flux, operator_focus=0.95):
        """
        Обновляет текущий learning rate на основе энтропийного потока.
        
        Аргументы:
        - entropy_flux (S_flux): текущий уровень шума/хаоса из внешней среды.
        - operator_focus (C_оп): целевая когерентность оператора (0..1).
        
        Возвращает:
        - current_lr: новый, адаптированный learning rate.
        - coherence: текущее значение когерентности C.
        """
        self.step_counter += 1
        
        # 1. Оператор хаоса (Z-принцип) — реакция на внешний шум
        chaos_operator = 1.0 / (1.0 + abs(entropy_flux) * (1.0 / PHI))
        
        # 2. Обновление когерентности C с учётом фокуса оператора и дыхания
        C_raw = self.C * chaos_operator + (1.0 - chaos_operator) * operator_focus
        breathing = 0.015 * math.sin(self.step_counter * PHI)  # Фаза поля
        self.C = etve_tanh_limit(C_raw + breathing)
        
        # 3. Расчёт коэффициента масштабирования LR на основе текущей C
        # Принцип: чем выше C (когерентность), тем смелее шаг (ближе к base_lr).
        # При низкой C (хаос) — LR сжимается к lr_min.
        scaling_factor = self.C  # C находится в [C_MIN, C_MAX], ~ [0.008, 0.999]
        
        # 4. Вычисление итогового LR
        # Смешиваем base_lr и lr_min через scaling_factor, масштабируем к диапазону
        # Используем нелинейную функцию для плавного перехода
        dynamic_lr = self.lr_min + scaling_factor * (self.base_lr - self.lr_min)
        # Дополнительно сжимаем, если энтропия очень высокая
        if entropy_flux > 0.8:
            dynamic_lr = dynamic_lr * (1.0 - 0.3 * (entropy_flux - 0.8) / 0.2)
        
        # 5. Жёсткая защита от выхода за границы
        self.current_lr = np.clip(dynamic_lr, self.lr_min, self.lr_max)
        
        return self.current_lr, self.C

# --- 2. ДЕМОНСТРАЦИЯ РАБОТЫ ---
if __name__ == "__main__":
    print("=" * 70)
    print("🌀 ETVE v12.3 — Адаптивный LR-скалер (Дыхание Шага Обучения)")
    print("   Синхронизация learning rate с живым энтропийным потоком")
    print("=" * 70 + "\n")
    
    # Инициализация скалера
    lr_scaler = ETVELearningRateScaler(base_lr=0.001, lr_min=1e-6, lr_max=0.01)
    
    print("Итерация | S_flux (хаос) | C (когерентность) | Текущий LR")
    print("-" * 60)
    
    # Симуляция потока: меняем энтропию и смотрим на LR
    for i in range(10):
        # Эмуляция внешнего шума — колебания от 0.1 до 0.9
        S_flux = 0.5 + 0.4 * math.sin(i * 0.7)
        
        # Получаем адаптированный LR
        current_lr, C = lr_scaler.step(entropy_flux=S_flux, operator_focus=0.92)
        
        print(f"   #{i+1:02d}    |   {S_flux:.4f}    |    {C:.4f}     |   {current_lr:.8f}")
        time.sleep(0.3)
    
    print("-" * 60)
    print("✅ Результат: LR дышит вместе с полем. Синхронизация активна.")
    print("   При высоком S_flux — шаг сжимается, при низком — восстанавливается.\n")
