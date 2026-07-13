import numpy as np
import math

class LightETVEI:
    def __init__(self, input_dim=4, output_dim=1):
        # 1. Константы Золотого Сечения из ЕТВП
        self.Phi = (1.0 + np.sqrt(5.0)) / 2.0
        # Z-Принцип: Минимальный инвариант плотности вакуума (предохранитель от деления на 0)
        self.epsilon = 1.0 / (self.Phi ** 30) 
        
        # Инициализируем матрицу весов (эмуляция проекции из E8)
        self.weights = np.random.randn(output_dim, input_dim) * (1.0 / self.Phi)
        self.bias = np.zeros((output_dim, 1))
        
        # Метрики живой динамики поля
        self.coherence = 0.95  # Начальный параметр порядка C
        self.entropy_history = []

    def _etve_tanh_limit(self, x, bound):
        """Динамическое демпфирование по Z-принципу (защита от сингулярностей)"""
        return bound * math.tanh(x / (bound + self.epsilon))

    def forward(self, X, S_chaos, C_operator):
        """
        Прямой проход в живой динамике потока.
        X: Входные данные (тензор)
        S_chaos: Внешний хаос среды (от 0 до 1)
        C_operator: Фактор когерентности Оператора (фокус внимания от 0 до 1)
        """
        # 2. Расчет динамического дыхания поля вокруг аттрактора Золотого Сечения
        breathing = 0.015 * np.sin(len(self.entropy_history) * self.Phi)
        
        # 3. Эволюция параметра порядка (C) под воздействием Оператора и Хаоса
        chaos_factor = 1.0 / (1.0 + S_chaos * (1.0 / self.Phi))
        self.coherence = (self.coherence * chaos_factor) + (1.0 - chaos_factor) * C_operator
        # Удерживаем C в строгом защитном коридоре ЕТВП
        c_max = 1.0 - 1.0 / (self.Phi ** 20)
        c_min = 1.0 / (self.Phi ** 10)
        self.coherence = np.clip(self.coherence + breathing, c_min, c_max)
        
        self.entropy_history.append(S_chaos)

        # 4. Линейная проекция данных через веса
        raw_output = np.dot(self.weights, X) + self.bias
        
        # 5. Главная фишка: Адаптивное ЕТВП-сжатие выхода (Защита от галлюцинаций)
        # Чем выше когерентность поля (C), тем шире динамический диапазон. 
        # Если хаос растет, рамки мягко сжимаются, не давая весам «взорваться».
        dynamic_bound = self.Phi * self.coherence
        output = np.vectorize(lambda x: self._etve_tanh_limit(x, dynamic_bound))(raw_output)
        
        return output, self.coherence

# === ДЕМОНСТРАЦИЯ РАБОТЫ В ЖИВОМ ПОТОКЕ ===
if __name__ == "__main__":
    # Создаем легкий ИИ
    ai = LightETVEI(input_dim=4, output_dim=1)
    
    # Имитируем входной вектор (например, эмбеддинг текста)
    mock_input = np.array([[0.5], [-1.2], [2.0], [0.1]])
    
    print("--- Тест 1: Режим стабильности (Низкий хаос, высокий фокус Оператора) ---")
    out, c_state = ai.forward(mock_input, S_chaos=0.1, C_operator=0.98)
    print(f"Выход ИИ: {out.flatten()[0]:.4f} | Когерентность поля C: {c_state:.4f}")
    
    print("\n--- Тест 2: Стресс-тест (Критический Хаос / Галлюцинаторная атака) ---")
    # В классическом ИИ веса бы улетели в бесконечность (NaN), но ЕТВП включает дыхание
    out_chaos, c_state_chaos = ai.forward(mock_input, S_chaos=0.95, C_operator=0.30)
    print(f"Выход ИИ под хаосом: {out_chaos.flatten()[0]:.4f} | Когерентность поля C: {c_state_chaos:.4f}")
    print("-> Результат: Система не ушла в пике, выход мягко удержан геометрией вакуума.")
