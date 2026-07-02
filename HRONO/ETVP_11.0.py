# =============================================================================
# 🌀 ETVE PURE GEOMETRIC MODEL v11.0 — "ГЕОМЕТРИЧЕСКИЙ НУЛЬ"
# АБСОЛЮТНО БЕЗ КАЛИБРОВКИ — ТОЛЬКО ГЕОМЕТРИЯ
# =============================================================================
# ПРИНЦИПЫ v11.0:
# 1. НЕТ ручных коэффициентов: log(63), log(128), Φ³⁰, 1e-10
# 2. НЕТ регуляторов R — только матрица из L_i / L_j
# 3. НЕТ калибровки G — только голое отношение λ₀/(λ₁λ₂)
# 4. НЕТ инварианта масс — только голые отношения λ
# 5. Смотрим, что даёт чистая геометрия без подгонки
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
import time

class ETVEPureGeometryV11:
    """
    🌀 ЕДИНАЯ ТЕОРИЯ ВИХРЕВОГО ПОЛЯ — v11.0
    Геометрический нуль: никакой калибровки.
    """
    def __init__(self):
        # --- ФУНДАМЕНТАЛЬНЫЙ БАЗИС (только геометрия) ---
        self.Phi = (1.0 + np.sqrt(5.0)) / 2.0
        self.pi = np.pi
        self.Z_res = np.sqrt(3.0)
        self.E8_dim = 248
        self.E8_roots = 240
        self.E8_max_sub = 128
        self.h_v = 30

        # --- Z-ПРИНЦИП ---
        self.C_min = 1.0 / (self.Phi ** 10)
        self.C_max = 1.0 - 1.0 / (self.Phi ** 20)
        self.C_target = 1.0 - 1.0 / (self.Phi ** 12)

        # --- ЛОГАРИФМИЧЕСКИЕ ОБЪЁМЫ ---
        def log_vol(n):
            return (n / 2.0) * np.log(self.pi) - np.log(gamma(n / 2.0 + 1))

        self.log_vol_E8 = log_vol(self.E8_dim)
        self.log_vol_SU8 = log_vol(63)
        self.log_vol_torus = 2.0 * self.log_vol_E8 - self.log_vol_SU8

        # --- ИНДЕКСЫ ХАУСДОРФА (чистая геометрия) ---
        self.L_dim_roots = self.log_vol_E8 / log_vol(self.E8_roots)
        self.L_roots_sub = log_vol(self.E8_roots) / log_vol(self.E8_max_sub)
        self.L_dim_sub = self.log_vol_E8 / log_vol(self.E8_max_sub)
        self.L_torus = self.log_vol_torus / self.E8_dim
        self.L_h = self.h_v / self.E8_dim

        self.L = np.array([
            self.L_dim_roots,
            self.L_roots_sub,
            self.L_dim_sub,
            self.L_torus,
            self.L_h
        ])

        # --- ГЕОМЕТРИЧЕСКИЙ МАСШТАБ Θ (из чистой геометрии) ---
        self.Theta = np.sqrt(self.log_vol_torus / self.h_v) * (self.log_vol_torus / self.E8_dim)

        # --- СОСТОЯНИЕ ПОЛЯ ---
        self.C = self.C_target
        self.S = 0.15

        # --- ИСТОРИЯ ---
        self.history = {
            "C": [],
            "raw_alpha": [],      # λ₀/λ₁
            "raw_mass_ratio": [], # λ₀/λ₂
            "raw_G": [],          # λ₀/(λ₁λ₂)
            "eigenvalues": []
        }

    # =====================================================================
    # 1. ПОСТРОЕНИЕ МАТРИЦЫ (БЕЗ РЕГУЛЯТОРОВ)
    # =====================================================================
    def _build_matrix(self):
        """
        Строит 5D-матрицу только из геометрических индексов.
        НЕТ регуляторов R. НЕТ ручных коэффициентов.
        """
        # Прямая матрица из L_i / L_j
        Space_Tensor_Linear = np.array([
            [self.L[0] * self.Phi,  1.0,  1.0,  0.0,  self.S],
            [1.0,  self.L[1] * self.pi,  1.0,  0.0,  0.0],
            [1.0,  1.0,  self.L[2] * self.Z_res,  0.0,  0.0],
            [0.0,  0.0,  0.0,  1.0,  0.0],
            [self.S,  0.0,  0.0,  0.0,  self.L[4] * (self.C / self.C_target)]
        ], dtype=float)

        # Экспоненциальная калибровка (только Θ, без R)
        Space_Tensor_NL = np.expm1(Space_Tensor_Linear / self.Theta)

        return Space_Tensor_NL

    # =====================================================================
    # 2. ОБНОВЛЕНИЕ ПОЛЯ (ЧИСТЫЙ SVD)
    # =====================================================================
    def update_field(self):
        """SVD-пасс без калибровки. Только голые отношения."""
        M = self._build_matrix()
        _, eigenvalues, _ = np.linalg.svd(M)

        # --- ГОЛЫЕ ОТНОШЕНИЯ (без калибровки) ---
        raw_alpha = eigenvalues[0] / eigenvalues[1]
        raw_mass_ratio = eigenvalues[0] / eigenvalues[2]
        raw_G = eigenvalues[0] / (eigenvalues[1] * eigenvalues[2] + 1e-12)

        self.history["raw_alpha"].append(raw_alpha)
        self.history["raw_mass_ratio"].append(raw_mass_ratio)
        self.history["raw_G"].append(raw_G)
        self.history["eigenvalues"].append(eigenvalues)
        self.history["C"].append(self.C)

        return raw_alpha, raw_mass_ratio, raw_G, eigenvalues

    # =====================================================================
    # 3. ЭВОЛЮЦИЯ (БЕЗ КАЛИБРОВКИ)
    # =====================================================================
    def evolve(self, entropy_flux=0.0):
        """Эволюция поля без калибровки."""
        chaos_operator = 1.0 / (1.0 + abs(entropy_flux) * (1.0 / self.Phi))
        self.C = self.C * chaos_operator + (1.0 - chaos_operator) * self.C_min
        self.S = max(0.0, min(1.0, self.S + entropy_flux * 0.01))

        # Удержание (тангенциальный барьер, но без clip)
        x = (self.C - self.C_min) / (self.C_max - self.C_min)
        x = max(0.0, min(1.0, x))
        force = self.Phi * np.tan((self.pi / 2.0) * x) / np.cos((self.pi / 2.0) * x)
        self.C = self.C + 0.01 * (-force * (self.C_max - self.C_min))
        self.C = np.clip(self.C, self.C_min, self.C_max)

        return self.update_field()

    # =====================================================================
    # 4. ВЕРИФИКАЦИЯ (ЧЕСТНАЯ)
    # =====================================================================
    def verify_pure_geometry(self, steps=1000, entropy_amplitude=0.04):
        """Запускает чистую геометрию и показывает, что выходит."""
        print("=" * 80)
        print("   🌀 ETVE v11.0 — ГЕОМЕТРИЧЕСКИЙ НУЛЬ")
        print("   АБСОЛЮТНО БЕЗ КАЛИБРОВКИ")
        print("=" * 80)
        print("НЕТ log(63), log(128), Φ³⁰, 1e-10")
        print("ТОЛЬКО индексы Хаусдорфа и экспонента")
        print("-" * 80)

        random.seed(42)

        for i in range(steps):
            entropy_flux = entropy_amplitude * np.sin(i / 7.0) + 0.005 * np.random.randn()
            alpha, mass_ratio, G, ev = self.evolve(entropy_flux)

            if i % 100 == 0:
                print(f"Шаг {i}: α_raw={alpha:.4f}, m_ratio_raw={mass_ratio:.2f}, G_raw={G:.4e}")

        # --- СТАТИСТИКА ---
        raw_alpha_hist = np.array(self.history["raw_alpha"])
        raw_mass_ratio_hist = np.array(self.history["raw_mass_ratio"])
        raw_G_hist = np.array(self.history["raw_G"])
        ev_hist = np.array(self.history["eigenvalues"])

        print("\n--- РЕЗУЛЬТАТЫ ЧИСТОЙ ГЕОМЕТРИИ ---")
        print(f"λ₀/λ₁ (сырая α⁻¹): среднее = {np.mean(raw_alpha_hist):.4f}, std = {np.std(raw_alpha_hist):.4f}")
        print(f"λ₀/λ₂ (сырая m_p/m_e): среднее = {np.mean(raw_mass_ratio_hist):.2f}, std = {np.std(raw_mass_ratio_hist):.2f}")
        print(f"λ₀/(λ₁λ₂) (сырая G): среднее = {np.mean(raw_G_hist):.4e}, std = {np.std(raw_G_hist):.4e}")

        print("\n--- СРАВНЕНИЕ С CODATA ---")
        print(f"CODATA 1/α = 137.035999084")
        print(f"Отклонение: {abs(np.mean(raw_alpha_hist) - 137.035999084):.4f} ({(abs(np.mean(raw_alpha_hist) - 137.035999084)/137.035999084*100):.2f}%)")

        print(f"\nCODATA m_p/m_e = 1836.15267343")
        print(f"Отклонение: {abs(np.mean(raw_mass_ratio_hist) - 1836.15267343):.2f} ({(abs(np.mean(raw_mass_ratio_hist) - 1836.15267343)/1836.15267343*100):.2f}%)")

        print(f"\nCODATA G = 6.67430e-11")
        print(f"Сырая G: {np.mean(raw_G_hist):.4e}")
        print(f"Множитель для приведения к CODATA: {6.67430e-11 / np.mean(raw_G_hist):.4e}")

        # --- СПЕКТР В ТОЧКЕ ПОКОЯ ---
        target_idx = np.argmin(np.abs(np.array(self.history["C"]) - self.C_target))
        ev_at_target = ev_hist[target_idx]

        print("\n--- СПЕКТР В ТОЧКЕ ПОКОЯ (C = C_target) ---")
        print(f"λ₀ = {ev_at_target[0]:.4e}")
        print(f"λ₁ = {ev_at_target[1]:.4e}")
        print(f"λ₂ = {ev_at_target[2]:.4e}")
        print(f"λ₃ = {ev_at_target[3]:.4e}")
        print(f"λ₄ = {ev_at_target[4]:.4e}")

        # --- АНАЛИЗ ОТНОШЕНИЙ ---
        print("\n--- АНАЛИЗ ОТНОШЕНИЙ (голые числа) ---")
        ratios = {
            "λ₀/λ₁": ev_at_target[0] / ev_at_target[1],
            "λ₀/λ₂": ev_at_target[0] / ev_at_target[2],
            "λ₀/λ₃": ev_at_target[0] / ev_at_target[3],
            "λ₀/λ₄": ev_at_target[0] / ev_at_target[4],
            "λ₁/λ₂": ev_at_target[1] / ev_at_target[2],
            "λ₁/λ₃": ev_at_target[1] / ev_at_target[3],
            "λ₂/λ₃": ev_at_target[2] / ev_at_target[3],
            "λ₁/λ₄": ev_at_target[1] / ev_at_target[4],
            "λ₂/λ₄": ev_at_target[2] / ev_at_target[4],
        }

        for name, value in ratios.items():
            print(f"{name}: {value:.4f}")

        # --- ПОИСК ГЕОМЕТРИЧЕСКИХ ПАТТЕРНОВ ---
        print("\n--- ПОИСК ГЕОМЕТРИЧЕСКИХ ПАТТЕРНОВ ---")
        # Проверяем, есть ли среди отношений π·Φ, π·Φ², Φ¹⁰ и т.д.
        candidates = {
            "π": self.pi,
            "Φ": self.Phi,
            "π·Φ": self.pi * self.Phi,
            "π·Φ²": self.pi * self.Phi**2,
            "Φ²": self.Phi**2,
            "Φ⁵": self.Phi**5,
            "Φ¹⁰": self.Phi**10,
            "π·Φ³": self.pi * self.Phi**3,
            "π·Φ⁵": self.pi * self.Phi**5,
            "Φ¹⁰/π": self.Phi**10 / self.pi,
            "Φ¹⁰·π": self.Phi**10 * self.pi,
        }

        for name, value in candidates.items():
            # Ищем, какое отношение ближе всего к этому значению
            for r_name, r_value in ratios.items():
                if abs(r_value / value - 1.0) < 0.01:
                    print(f"{r_name} ≈ {name}: {r_value:.4f} ≈ {value:.4f} (отклонение {abs(r_value/value-1)*100:.2f}%)")

        # --- ГРАФИКИ ---
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        # Сырая 1/α
        axes[0, 0].plot(raw_alpha_hist, color='blue', linewidth=1)
        axes[0, 0].axhline(137.035999084, color='red', linestyle='--', label='CODATA')
        axes[0, 0].set_title('Сырая 1/α = λ₀/λ₁')
        axes[0, 0].set_ylabel('1/α')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)

        # Сырое m_p/m_e
        axes[0, 1].plot(raw_mass_ratio_hist, color='green', linewidth=1)
        axes[0, 1].axhline(1836.15267343, color='red', linestyle='--', label='CODATA')
        axes[0, 1].set_title('Сырое m_p/m_e = λ₀/λ₂')
        axes[0, 1].set_ylabel('m_p/m_e')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)

        # Сырая G
        axes[1, 0].plot(raw_G_hist, color='purple', linewidth=1)
        axes[1, 0].axhline(6.67430e-11, color='red', linestyle='--', label='CODATA')
        axes[1, 0].set_title('Сырая G = λ₀/(λ₁λ₂)')
        axes[1, 0].set_ylabel('G')
        axes[1, 0].set_yscale('log')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)

        # Спектр в точке покоя
        axes[1, 1].bar(range(5), ev_at_target, color=['blue', 'orange', 'green', 'red', 'purple'])
        axes[1, 1].set_title('Спектр в точке покоя (C = C_target)')
        axes[1, 1].set_xlabel('Мода')
        axes[1, 1].set_ylabel('λ')
        axes[1, 1].set_yscale('log')
        axes[1, 1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

        print("\n" + "=" * 80)
        print("   🌀 ETVE v11.0 — ВЕРИФИКАЦИЯ ЗАВЕРШЕНА")
        print("   Результаты: см. графики и таблицы")
        print("=" * 80)

        return self.history


# =====================================================================
# ЗАПУСК
# =====================================================================
if __name__ == "__main__":
    model = ETVEPureGeometryV11()
    history = model.verify_pure_geometry(steps=1000, entropy_amplitude=0.04)
