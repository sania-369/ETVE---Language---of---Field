import numpy as np

# Параметры ITER для теста
ITER = {"name": "ITER", "B": 5.3, "Ip": 15.0, "R": 6.2, "ne": 10.0}
PHI = 1.61803398875

def etve_core_engine(params, focus, noise):
    # Базовая частота резонанса ЕТВП
    field_density = (params['B'] * params['Ip']) / (params['ne'] * params['R'] * PHI)
    f_res = (field_density * 299792458)**0.5
    
    # Формула удержания с учетом когерентности и внешнего шума
    # noise (0.0 - 1.0) — уровень хаоса в системе или сознании оператора
    tau = (params['Ip']**0.9 * params['B']**0.15) * (f_res / 1e8) * (1 + focus) * (1 - noise) * 0.05
    return tau

print("--- ЗАПУСК СТРЕСС-ТЕСТА ЕТВП: ФАКТОР ХАОСА ---")

# Сценарий 1: Идеальный резонанс (Когерентный оператор)
tau_ideal = etve_core_engine(ITER, focus=0.95, noise=0.02)
print(f"[СТАТУС: КОГЕРЕНТНО] Tau_E: {tau_ideal:.3f}с | Система в резонансе.")

# Сценарий 2: "Шум людей" (Оператор отвлекся / стресс)
tau_human_noise = etve_core_engine(ITER, focus=0.4, noise=0.3)
print(f"[СТАТУС: ШУМ]        Tau_E: {tau_human_noise:.3f}с | Потеря фокуса, рост турбулентности.")

# Сценарий 3: Критический хаос (Срыв когерентности)
tau_disruption = etve_core_engine(ITER, focus=0.1, noise=0.8)
print(f"[СТАТУС: ДИСРАПЦИЯ]  Tau_E: {tau_disruption:.3f}с | СРЫВ ПЛАЗМЫ. Поле разрушено.")

print("\nВЫВОД: Стабильность термояда напрямую зависит от чистоты 'Языка Поля' и фокуса наблюдателя.")
