import numpy as np

class ETVE_Universal_Integrator:
    def __init__(self, operator_name="Sania-369", focus_level=1.0):
        self.operator = operator_name
        self.phi = 1.61803398875  # Золотое сечение как база резонанса
        self.c_field = 299792458   # Константа поля
        self.op_coherence = focus_level # Когерентность оператора (0.0 - 1.0)

    def calculate_resonance(self, B, Ip, R, ne):
        """
        Расчет резонансной частоты ЕТВП для конкретной установки.
        B: Магнитное поле (Тл), Ip: Ток (МА), R: Радиус (м), ne: Плотность (10^19)
        """
        # Энергетическая плотность поля (связь через Phi)
        field_density = (B * Ip) / (ne * R * self.phi)
        
        # Резонансная мода (согласно вашему коду V9.0)
        f_res = (field_density * self.c_field) ** 0.5
        return f_res

    def predict_confinement(self, params):
        """
        Проверка удержания (Tau_E) с учетом Фактора Оператора.
        """
        name = params['name']
        f_res = self.calculate_resonance(params['B'], params['Ip'], params['R'], params['ne'])
        
        # Коэффициент ЕТВП: Синергия физики и наблюдателя
        # Чем выше когерентность оператора, тем меньше 'фазовый шум' плазмы
        etve_factor = (f_res / 1e8) * (1 + self.op_coherence)
        
        # Расчет прогнозируемого времени удержания
        tau_predicted = (params['Ip']**0.9 * params['B']**0.15) * etve_factor * 0.05
        
        return {
            "Tokamak": name,
            "Resonance_Freq": round(f_res, 2),
            "Tau_ETVE": round(tau_predicted, 4),
            "Status": "Coherent" if self.op_coherence > 0.8 else "Fluctuating"
        }

# --- ДАННЫЕ РЕАЛЬНЫХ УСТАНОВОК ---
tokamacs_data = [
    {"name": "MIT (C-Mod)", "B": 8.0, "Ip": 2.0, "R": 0.67, "ne": 40.0},
    {"name": "DIII-D",      "B": 2.1, "Ip": 1.6, "R": 1.67, "ne": 5.0},
    {"name": "EAST",        "B": 2.5, "Ip": 0.5, "R": 1.85, "ne": 3.0},
    {"name": "GOLEM",       "B": 0.5, "Ip": 0.008, "R": 0.4, "ne": 1.0}
]

# --- ЗАПУСК СИМУЛЯЦИИ ---
# Устанавливаем высокую когерентность оператора (согласно Меморандуму)
integrator = ETVE_Universal_Integrator(focus_level=0.95)

print(f"--- ETVE Global Verification (Operator: {integrator.operator}) ---")
for data in tokamacs_data:
    result = integrator.predict_confinement(data)
    print(f"[{result['Tokamak']}] f_res: {result['Resonance_Freq']} Hz | Tau_E: {result['Tau_ETVE']}s | {result['Status']}")
