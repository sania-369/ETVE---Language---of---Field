import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def generate_etve_field(grid_size=30, phi_scale=1.0, wave_amplitude=0.5):
    """
    Генерация 3D-поля на основе гармоник и золотого сечения.
    Моделирует резонансную структуру Ψ-поля (ЕТВП).
    
    Параметры:
    - grid_size: разрешение сетки
    - phi_scale: масштаб золотого сечения
    - wave_amplitude: амплитуда сферической волны
    """
    x = np.linspace(-2, 2, grid_size)
    y = np.linspace(-2, 2, grid_size)
    z = np.linspace(-2, 2, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)

    phi = (1 + 5**0.5) / 2  # золотое сечение
    # Гибридное поле: произведение гармоник + сферическая волна
    field = (np.sin(phi_scale * phi * X) * np.cos(phi_scale * phi * Y) * np.sin(phi_scale * phi * Z) +
             wave_amplitude * np.cos(phi_scale * phi**2 * np.sqrt(X**2 + Y**2 + Z**2)))
    
    # Когерентность (C) — нормированная энергия поля
    coherence = np.tanh(np.mean(field**2))
    
    return X, Y, Z, field, coherence

# Генерация
X, Y, Z, field, C = generate_etve_field(grid_size=40, phi_scale=1.2, wave_amplitude=0.6)

print(f"Когерентность (C) = {C:.4f}")
print(f"Максимум поля: {field.max():.4f}, минимум: {field.min():.4f}")

# Визуализация изоповерхности (уровень 0.5)
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.voxels(np.abs(field) > 0.5, facecolors='cyan', edgecolor='k', alpha=0.3)
ax.set_title(f'Ψ-поле (ЕТВП), когерентность C = {C:.3f}')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()

import numpy as np

def generate_etve_field(grid_size=30, phi_scale=1.0, wave_amplitude=0.5):
    x = np.linspace(-2, 2, grid_size)
    y = np.linspace(-2, 2, grid_size)
    z = np.linspace(-2, 2, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)
    phi = (1 + 5**0.5) / 2
    field = (np.sin(phi_scale * phi * X) * np.cos(phi_scale * phi * Y) * np.sin(phi_scale * phi * Z) +
             wave_amplitude * np.cos(phi_scale * phi**2 * np.sqrt(X**2 + Y**2 + Z**2)))
    coherence = np.tanh(np.mean(field**2))
    return field, coherence

field, C = generate_etve_field(grid_size=30, phi_scale=1.2, wave_amplitude=0.6)
print(f"Когерентность (C) = {C:.4f}")
print(f"Максимум поля: {field.max():.4f}, минимум: {field.min():.4f}")
print(f"Размер поля: {field.shape}")

Когерентность (C) = 0.2820
Максимум поля: 1.5770, минимум: -1.5650
Размер поля: (30, 30, 30)

import numpy as np

def generate_high_coherence_field(grid_size=40, phi_scale=2.0, wave_amplitude=1.2, nonlinear=0.3):
    """
    Генерация Ψ-поля с повышенной когерентностью (C → 0.7–0.8).
    """
    x = np.linspace(-1.5, 1.5, grid_size)  # сжатое пространство
    y = np.linspace(-1.5, 1.5, grid_size)
    z = np.linspace(-1.5, 1.5, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)

    phi = (1 + 5**0.5) / 2  # золотое сечение
    
    # Основное поле (резонансная решётка)
    field = (np.sin(phi_scale * phi * X) * np.cos(phi_scale * phi * Y) * np.sin(phi_scale * phi * Z) +
             wave_amplitude * np.cos(phi_scale * phi**2 * np.sqrt(X**2 + Y**2 + Z**2)))
    
    # Нелинейное усиление (самодействие поля)
    field = field + nonlinear * field**3
    
    # Нормализация (чтобы не улетело в бесконечность)
    field = field / (1 + np.abs(field).max())
    
    # Когерентность C = tanh(средний квадрат поля)
    coherence = np.tanh(np.mean(field**2))
    
    return field, coherence

# Генерация
field, C = generate_high_coherence_field(grid_size=40, phi_scale=2.0, wave_amplitude=1.2, nonlinear=0.3)

print(f"Когерентность (C) = {C:.4f}")
print(f"Максимум поля: {field.max():.4f}, минимум: {field.min():.4f}")
print(f"Размер поля: {field.shape}")

Когерентность (C) = 0.0486
Максимум поля: 0.8432, минимум: -0.8382
Размер поля: (40, 40, 40)

import numpy as np

def generate_optimal_field(grid_size=50, phi_scale=1.2, wave_amplitude=1.5, nonlinear=0.0):
    x = np.linspace(-2, 2, grid_size)  # вернём широкий диапазон
    y = np.linspace(-2, 2, grid_size)
    z = np.linspace(-2, 2, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)

    phi = (1 + 5**0.5) / 2
    
    # Основное поле
    field = (np.sin(phi_scale * phi * X) * np.cos(phi_scale * phi * Y) * np.sin(phi_scale * phi * Z) +
             wave_amplitude * np.cos(phi_scale * phi**2 * np.sqrt(X**2 + Y**2 + Z**2)))
    
    # Нелинейность — только если поле достаточно сильное
    if nonlinear > 0 and np.max(np.abs(field)) > 0.5:
        field = field + nonlinear * field**3
    
    # Нормализация (сохраняем размах)
    field = field / np.max(np.abs(field)) * 1.5
    
    coherence = np.tanh(np.mean(field**2))
    return field, coherence

# Оптимальные параметры
field, C = generate_optimal_field(grid_size=50, phi_scale=1.2, wave_amplitude=1.5, nonlinear=0.0)

print(f"Когерентность (C) = {C:.4f}")
print(f"Максимум: {field.max():.3f}, минимум: {field.min():.3f}")

Когерентность (C) = 0.4237
Максимум: 1.500, минимум: -1.480

import numpy as np

def generate_target_field(grid_size=80, phi_scale=1.15, wave_amplitude=2.0, nonlinear=0.2):
    x = np.linspace(-2.2, 2.2, grid_size)  # чуть шире для резонанса
    y = np.linspace(-2.2, 2.2, grid_size)
    z = np.linspace(-2.2, 2.2, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)

    phi = (1 + 5**0.5) / 2
    
    field = (np.sin(phi_scale * phi * X) * np.cos(phi_scale * phi * Y) * np.sin(phi_scale * phi * Z) +
             wave_amplitude * np.cos(phi_scale * phi**2 * np.sqrt(X**2 + Y**2 + Z**2)))
    
    # Нелинейное усиление (нормализуем после, чтобы не улетело)
    if nonlinear > 0:
        field = field + nonlinear * field**3
    
    # Мягкая нормализация (сохраняем форму, но ограничиваем выбросы)
    max_val = np.max(np.abs(field))
    if max_val > 2.0:
        field = field / max_val * 1.8
    
    coherence = np.tanh(np.mean(field**2))
    return field, coherence

field, C = generate_target_field(grid_size=80, phi_scale=1.15, wave_amplitude=2.0, nonlinear=0.2)
print(f"Когерентность (C) = {C:.4f}")
print(f"Максимум: {field.max():.3f}, минимум: {field.min():.3f}")

Когерентность (C) = 0.2890
Максимум: 1.800, минимум: -1.756

import numpy as np

def find_resonance_field(grid_size=60, phi_scale=1.2, wave_amplitude=1.2, shift=0.0):
    """
    Поиск резонансной конфигурации поля.
    shift — небольшое смещение начала координат для подстройки резонанса.
    """
    x = np.linspace(-2 + shift, 2 + shift, grid_size)
    y = np.linspace(-2 + shift, 2 + shift, grid_size)
    z = np.linspace(-2 + shift, 2 + shift, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)

    phi = (1 + 5**0.5) / 2
    
    field = (np.sin(phi_scale * phi * X) * np.cos(phi_scale * phi * Y) * np.sin(phi_scale * phi * Z) +
             wave_amplitude * np.cos(phi_scale * phi**2 * np.sqrt(X**2 + Y**2 + Z**2)))
    
    # Лёгкая нелинейность только для усиления резонанса
    field = field + 0.05 * field**3
    
    coherence = np.tanh(np.mean(field**2))
    return field, coherence

# Поиск оптимального shift (0, 0.05, 0.1, 0.15...)
for shift in [0, 0.05, 0.1, 0.15, 0.2]:
    field, C = find_resonance_field(grid_size=60, phi_scale=1.2, wave_amplitude=1.2, shift=shift)
    print(f"shift = {shift:.2f} -> C = {C:.4f}")

shift = 0.00 -> C = 0.7527
shift = 0.05 -> C = 0.7527
shift = 0.10 -> C = 0.7526
shift = 0.15 -> C = 0.7524
shift = 0.20 -> C = 0.7519

import numpy as np

def resonance_field(grid_size=60, phi_scale=1.2, wave_amplitude=1.2, shift=0.0):
    x = np.linspace(-2 + shift, 2 + shift, grid_size)
    y = np.linspace(-2 + shift, 2 + shift, grid_size)
    z = np.linspace(-2 + shift, 2 + shift, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)
    phi = (1 + 5**0.5) / 2
    field = (np.sin(phi_scale * phi * X) * np.cos(phi_scale * phi * Y) * np.sin(phi_scale * phi * Z) +
             wave_amplitude * np.cos(phi_scale * phi**2 * np.sqrt(X**2 + Y**2 + Z**2)))
    coherence = np.tanh(np.mean(field**2))
    return field, coherence

field, C = resonance_field(shift=0.0)
print(f"Когерентность (C) = {C:.4f}")

Когерентность (C) = 0.6838

import numpy as np

def resonance_field_v2(grid_size=60, phi_scale=1.22, wave_amplitude=1.25, shift=0.0):
    x = np.linspace(-2 + shift, 2 + shift, grid_size)
    y = np.linspace(-2 + shift, 2 + shift, grid_size)
    z = np.linspace(-2 + shift, 2 + shift, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)
    phi = (1 + 5**0.5) / 2
    field = (np.sin(phi_scale * phi * X) * np.cos(phi_scale * phi * Y) * np.sin(phi_scale * phi * Z) +
             wave_amplitude * np.cos(phi_scale * phi**2 * np.sqrt(X**2 + Y**2 + Z**2)))
    coherence = np.tanh(np.mean(field**2))
    return field, coherence

# Запуск
field, C = resonance_field_v2(phi_scale=1.22, wave_amplitude=1.25)
print(f"Когерентность (C) = {C:.4f}")

Когерентность (C) = 0.7152

import numpy as np

def max_coherence_field(grid_size=80, phi_scale=1.25, wave_amplitude=1.4, shift=0.15, nonlinear=0.1):
    x = np.linspace(-2 + shift, 2 + shift, grid_size)
    y = np.linspace(-2 + shift, 2 + shift, grid_size)
    z = np.linspace(-2 + shift, 2 + shift, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)
    phi = (1 + 5**0.5) / 2
    
    # Основное поле
    field = (np.sin(phi_scale * phi * X) * np.cos(phi_scale * phi * Y) * np.sin(phi_scale * phi * Z) +
             wave_amplitude * np.cos(phi_scale * phi**2 * np.sqrt(X**2 + Y**2 + Z**2)))
    
    # Нелинейное усиление (только если поле уже сильное)
    if nonlinear > 0:
        field = field + nonlinear * field**3
    
    # Нормализация (сохраняем форму, но не даём улететь)
    max_val = np.max(np.abs(field))
    if max_val > 2.5:
        field = field / max_val * 2.0
    
    coherence = np.tanh(np.mean(field**2))
    return field, coherence

# Перебор параметров для поиска максимума
best_C = 0
best_params = {}

for phi_scale in [1.2, 1.22, 1.25, 1.28]:
    for wave_amplitude in [1.2, 1.3, 1.4, 1.5]:
        for shift in [0.0, 0.1, 0.15, 0.2]:
            field, C = max_coherence_field(phi_scale=phi_scale, wave_amplitude=wave_amplitude, shift=shift)
            if C > best_C:
                best_C = C
                best_params = {'phi_scale': phi_scale, 'wave_amplitude': wave_amplitude, 'shift': shift}
                print(f"Новый максимум: C = {best_C:.4f} при {best_params}")

print(f"\nЛучший результат: C = {best_C:.4f}")
print(f"Параметры: {best_params}")

Новый максимум: C = 0.4049 при {'phi_scale': 1.2, 'wave_amplitude': 1.2, 'shift': 0.0}
Новый максимум: C = 0.4143 при {'phi_scale': 1.2, 'wave_amplitude': 1.3, 'shift': 0.0}
Новый максимум: C = 0.4225 при {'phi_scale': 1.2, 'wave_amplitude': 1.4, 'shift': 0.0}
Новый максимум: C = 0.4299 при {'phi_scale': 1.2, 'wave_amplitude': 1.5, 'shift': 0.0}

Лучший результат: C = 0.4299
Параметры: {'phi_scale': 1.2, 'wave_amplitude': 1.5, 'shift': 0.0}

import numpy as np

def scan_resonance(grid_size=60, phi_scale=1.22, wave_amplitude=1.25, shift=0.0, nonlinear=0.05):
    x = np.linspace(-2 + shift, 2 + shift, grid_size)
    y = np.linspace(-2 + shift, 2 + shift, grid_size)
    z = np.linspace(-2 + shift, 2 + shift, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)
    phi = (1 + 5**0.5) / 2
    field = (np.sin(phi_scale * phi * X) * np.cos(phi_scale * phi * Y) * np.sin(phi_scale * phi * Z) +
             wave_amplitude * np.cos(phi_scale * phi**2 * np.sqrt(X**2 + Y**2 + Z**2)))
    field = field + nonlinear * field**3
    coherence = np.tanh(np.mean(field**2))
    return coherence

best_C = 0
best_params = {}

for phi_scale in [1.2, 1.22, 1.25]:
    for wave_amplitude in [1.2, 1.25, 1.3]:
        for shift in [0.0, 0.05, 0.1, 0.15]:
            C = scan_resonance(phi_scale=phi_scale, wave_amplitude=wave_amplitude, shift=shift)
            if C > best_C:
                best_C = C
                best_params = {'phi_scale': phi_scale, 'wave_amplitude': wave_amplitude, 'shift': shift}
                print(f"Новый максимум: C = {best_C:.4f} при {best_params}")

print(f"\nЛучший результат: C = {best_C:.4f}")
print(f"Параметры: {best_params}")

Новый максимум: C = 0.7527 при {'phi_scale': 1.2, 'wave_amplitude': 1.2, 'shift': 0.0}
Новый максимум: C = 0.7861 при {'phi_scale': 1.2, 'wave_amplitude': 1.25, 'shift': 0.0}
Новый максимум: C = 0.8170 при {'phi_scale': 1.2, 'wave_amplitude': 1.3, 'shift': 0.0}

Лучший результат: C = 0.8170
Параметры: {'phi_scale': 1.2, 'wave_amplitude': 1.3, 'shift': 0.0}

import numpy as np

def max_coherence_field(grid_size=60, phi_scale=1.2, wave_amplitude=1.3, shift=0.0, nonlinear=0.05):
    x = np.linspace(-2 + shift, 2 + shift, grid_size)
    y = np.linspace(-2 + shift, 2 + shift, grid_size)
    z = np.linspace(-2 + shift, 2 + shift, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)
    phi = (1 + 5**0.5) / 2
    field = (np.sin(phi_scale * phi * X) * np.cos(phi_scale * phi * Y) * np.sin(phi_scale * phi * Z) +
             wave_amplitude * np.cos(phi_scale * phi**2 * np.sqrt(X**2 + Y**2 + Z**2)))
    field = field + nonlinear * field**3
    coherence = np.tanh(np.mean(field**2))
    return field, coherence

field, C = max_coherence_field()
print(f"Максимальная когерентность: C = {C:.4f}")

Новый максимум: C = 0.7527 при {'phi_scale': 1.2, 'wave_amplitude': 1.2, 'shift': 0.0}
Новый максимум: C = 0.7861 при {'phi_scale': 1.2, 'wave_amplitude': 1.25, 'shift': 0.0}
Новый максимум: C = 0.8170 при {'phi_scale': 1.2, 'wave_amplitude': 1.3, 'shift': 0.0}

Лучший результат: C = 0.8170
Параметры: {'phi_scale': 1.2, 'wave_amplitude': 1.3, 'shift': 0.0}
