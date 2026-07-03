# =============================================================================
# 🌀 ETVE PURE GEOMETRIC MODEL v11.1
# РЕНОРМГРУППОВОЙ ПОТОК — НАРУШЕНИЕ СИММЕТРИИ E8 → SU(3) × SU(2) × U(1)
# =============================================================================
# ПРИНЦИПЫ v11.1:
# 1. Матрица Картана E8 — при высокой энергии (C → C_max)
# 2. Константы связи «бегут» по мере изменения C (энергии)
# 3. Нарушение симметрии: добавление массовых членов при понижении C
# 4. Наблюдаем, где поток пересекает CODATA
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma

class ETVERenormalizationFlowV111:
    """
    🌀 ЕДИНАЯ ТЕОРИЯ ВИХРЕВОГО ПОЛЯ — v11.1
    Ренормгрупповой поток: E8 → SU(3) × SU(2) × U(1)
    """
    def __init__(self):
        # --- ФУНДАМЕНТАЛЬНЫЙ БАЗИС ---
        self.Phi = (1.0 + np.sqrt(5.0)) / 2.0
        self.pi = np.pi
        self.Z_res = np.sqrt(3.0)

        # --- МАТРИЦА КАРТАНА E8 (8x8) ---
        self.C_E8 = np.array([
            [2, -1, 0, 0, 0, 0, 0, 0],
            [-1, 2, -1, 0, 0, 0, 0, 0],
            [0, -1, 2, -1, 0, 0, 0, 0],
            [0, 0, -1, 2, -1, 0, 0, 0],
            [0, 0, 0, -1, 2, -1, 0, -1],
            [0, 0, 0, 0, -1, 2, -1, 0],
            [0, 0, 0, 0, 0, -1, 2, 0],
            [0, 0, 0, 0, -1, 0, 0, 2]
        ], dtype=float)

        # --- Z-ПРИНЦИП (энергетический масштаб) ---
        self.C_min = 1.0 / (self.Phi ** 10)
        self.C_max = 1.0 - 1.0 / (self.Phi ** 20)
        self.C_target = 1.0 - 1.0 / (self.Phi ** 12)

        # --- CODATA (для сравнения) ---
        self.CODATA = {
            "alpha_em": 1.0 / 137.035999084,
            "alpha_s": 0.1184,
            "alpha_w": 0.0338,
            "G": 6.67430e-11
        }

        # --- ИСТОРИЯ ПОТОКА ---
        self.history = {
            "C": [],
            "alpha_em": [],
            "alpha_s": [],
            "alpha_w": [],
            "G": [],
            "unification": [],
            "mass_terms": []
        }

    # =====================================================================
    # 1. ПОСТРОЕНИЕ МАТРИЦЫ ПРИ ДАННОЙ ЭНЕРГИИ (C)
    # =====================================================================
    def _build_matrix_at_C(self, C, mass_scale=1.0):
        """
        Строит матрицу при заданном энергетическом масштабе C.
        При C → C_max (UV) — чистая E8.
        При C → C_min (IR) — добавляются массовые члены (нарушение симметрии).
        """
        # Начинаем с матрицы Картана
        M = self.C_E8.copy()

        # Добавляем массовые члены (нарушение симметрии)
        # При C → C_min массы растут (симметрия нарушена)
        mass_factor = (self.C_max - C) / (self.C_max - self.C_min)
        mass_factor = np.clip(mass_factor, 0.0, 1.0)

        # Массовые члены для SU(3) × SU(2) × U(1)
        # Добавляем на диагональ
        mass_terms = np.array([
            0.0,  # U(1)
            0.0,  # SU(2)
            0.0,  # SU(3)
            0.0,  # ...
            0.0,
            0.0,
            0.0,
            0.0
        ])

        # При C → C_min включаются массы для подгрупп
        mass_terms[0] = mass_factor * 1.0   # U(1) масса
        mass_terms[1] = mass_factor * 2.0   # SU(2) масса
        mass_terms[2] = mass_factor * 3.0   # SU(3) масса

        for i in range(8):
            M[i, i] += mass_terms[i]

        # Добавляем масштабный множитель (зависит от C)
        M = M * (1.0 + 0.1 * (C - self.C_target))

        return M

    # =====================================================================
    # 2. РАСЧЁТ КОНСТАНТ СВЯЗИ (поток)
    # =====================================================================
    def _compute_couplings(self, M):
        """Вычисляет константы связи из матрицы."""
        _, eigenvalues, _ = np.linalg.svd(M)

        # Голые отношения (UV-масштаб)
        alpha_em_uv = eigenvalues[2] / eigenvalues[0]  # U(1)
        alpha_s_uv = eigenvalues[1] / eigenvalues[0]   # SU(3)
        alpha_w_uv = eigenvalues[3] / eigenvalues[0]   # SU(2)

        # Применяем ренормгрупповой поток
        # Константы «бегут» в зависимости от энергии (C)
        # Используем упрощённое уравнение: α_IR = α_UV / (1 + β * α_UV * log(E_UV/E_IR))
        # Где E_UV/E_IR ≈ (C_max - C_min) / (C - C_min)

        energy_ratio = (self.C_max - self.C_min) / (C - self.C_min + 1e-12)
        log_ratio = np.log(energy_ratio)

        # Бета-функции (упрощённые)
        beta_em = 1.0 / 3.0
        beta_s = 7.0
        beta_w = 2.0

        alpha_em = alpha_em_uv / (1.0 + beta_em * alpha_em_uv * log_ratio)
        alpha_s = alpha_s_uv / (1.0 + beta_s * alpha_s_uv * log_ratio)
        alpha_w = alpha_w_uv / (1.0 + beta_w * alpha_w_uv * log_ratio)

        # Гравитация: G растёт при C → C_min
        G = eigenvalues[0] / (eigenvalues[1] * eigenvalues[2] + 1e-12)
        G = G * (1.0 + 0.1 * (self.C_max - C) / (self.C_max - self.C_min))

        # Мера объединения
        couplings = np.array([alpha_em, alpha_s, alpha_w])
        couplings = couplings / (np.mean(couplings) + 1e-12)
        unification = 1.0 - np.std(couplings)

        return {
            "alpha_em": alpha_em,
            "alpha_s": alpha_s,
            "alpha_w": alpha_w,
            "G": G,
            "unification": unification
        }

    # =====================================================================
    # 3. ЗАПУСК ПОТОКА
    # =====================================================================
    def run_flow(self, steps=1000):
        """Запускает ренормгрупповой поток от C_max к C_min."""
        print("=" * 80)
        print("   🌀 ETVE v11.1 — РЕНОРМГРУППОВОЙ ПОТОК")
        print("   E8 → SU(3) × SU(2) × U(1)")
        print("=" * 80)

        # Создаём массив C от C_max к C_min
        C_array = np.linspace(self.C_max, self.C_min, steps)

        for C in C_array:
            # Строим матрицу при данной энергии
            M = self._build_matrix_at_C(C)

            # Вычисляем константы связи
            couplings = self._compute_couplings(M)

            # Сохраняем историю
            self.history["C"].append(C)
            self.history["alpha_em"].append(couplings["alpha_em"])
            self.history["alpha_s"].append(couplings["alpha_s"])
            self.history["alpha_w"].append(couplings["alpha_w"])
            self.history["G"].append(couplings["G"])
            self.history["unification"].append(couplings["unification"])

        print("Поток завершён")
        print(f"Шагов: {len(self.history['C'])}")
        print("-" * 80)

        return self.history

    # =====================================================================
    # 4. АНАЛИЗ РЕЗУЛЬТАТОВ
    # =====================================================================
    def analyze_flow(self):
        """Находит точки, где поток пересекает CODATA."""
        C = np.array(self.history["C"])
        alpha_em = np.array(self.history["alpha_em"])
        alpha_s = np.array(self.history["alpha_s"])
        alpha_w = np.array(self.history["alpha_w"])
        G = np.array(self.history["G"])
        unification = np.array(self.history["unification"])

        # Находим индекс, где alpha_em ближе всего к CODATA
        idx_em = np.argmin(np.abs(alpha_em - self.CODATA["alpha_em"]))
        idx_s = np.argmin(np.abs(alpha_s - self.CODATA["alpha_s"]))
        idx_w = np.argmin(np.abs(alpha_w - self.CODATA["alpha_w"]))
        idx_G = np.argmin(np.abs(G - self.CODATA["G"]))

        # Унификация: ищем максимум
        idx_unif = np.argmax(unification)

        print("\n--- РЕЗУЛЬТАТЫ ПОТОКА ---")
        print(f"alpha_em: CODATA={self.CODATA['alpha_em']:.6f} → поток={alpha_em[idx_em]:.6f} при C={C[idx_em]:.4f} (отклонение {abs(alpha_em[idx_em]-self.CODATA['alpha_em'])/self.CODATA['alpha_em']*100:.2f}%)")
        print(f"alpha_s: CODATA={self.CODATA['alpha_s']:.4f} → поток={alpha_s[idx_s]:.4f} при C={C[idx_s]:.4f} (отклонение {abs(alpha_s[idx_s]-self.CODATA['alpha_s'])/self.CODATA['alpha_s']*100:.2f}%)")
        print(f"alpha_w: CODATA={self.CODATA['alpha_w']:.4f} → поток={alpha_w[idx_w]:.4f} при C={C[idx_w]:.4f} (отклонение {abs(alpha_w[idx_w]-self.CODATA['alpha_w'])/self.CODATA['alpha_w']*100:.2f}%)")
        print(f"G: CODATA={self.CODATA['G']:.4e} → поток={G[idx_G]:.4e} при C={C[idx_G]:.4f} (отклонение {abs(G[idx_G]-self.CODATA['G'])/self.CODATA['G']*100:.2f}%)")
        print(f"Унификация: максимум {unification[idx_unif]:.4f} при C={C[idx_unif]:.4f}")

        # --- ВЫВОД ---
        print("\n--- ВЫВОД ---")
        if unification[idx_unif] > 0.9:
            print("✅ ВЗАИМОДЕЙСТВИЯ ОБЪЕДИНЯЮТСЯ ПРИ ВЫСОКОЙ ЭНЕРГИИ (C → C_max)")
        else:
            print("⚠️ ОБЪЕДИНЕНИЕ НЕ ДОСТИГНУТО")

        if abs(alpha_em[idx_em] - self.CODATA["alpha_em"]) / self.CODATA["alpha_em"] < 0.1:
            print("✅ ЭЛЕКТРОМАГНЕТИЗМ: поток даёт CODATA с точностью < 10%")
        else:
            print("⚠️ ЭЛЕКТРОМАГНЕТИЗМ: поток не достигает CODATA")

        # --- ГРАФИКИ ---
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        # Константы связи
        axes[0, 0].plot(C, alpha_em, label='α_em', color='blue', linewidth=1.5)
        axes[0, 0].plot(C, alpha_s, label='α_s', color='red', linewidth=1.5)
        axes[0, 0].plot(C, alpha_w, label='α_w', color='green', linewidth=1.5)
        axes[0, 0].axhline(self.CODATA["alpha_em"], color='blue', linestyle='--', alpha=0.5)
        axes[0, 0].axhline(self.CODATA["alpha_s"], color='red', linestyle='--', alpha=0.5)
        axes[0, 0].axhline(self.CODATA["alpha_w"], color='green', linestyle='--', alpha=0.5)
        axes[0, 0].set_title('Константы связи')
        axes[0, 0].set_xlabel('C (энергетический масштаб)')
        axes[0, 0].set_ylabel('α')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)

        # Унификация
        axes[0, 1].plot(C, unification, color='purple', linewidth=1.5)
        axes[0, 1].axhline(0.9, color='black', linestyle='--', label='Порог объединения')
        axes[0, 1].set_title('Мера объединения')
        axes[0, 1].set_xlabel('C')
        axes[0, 1].set_ylabel('Unification')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)

        # G
        axes[1, 0].plot(C, G, color='purple', linewidth=1.5)
        axes[1, 0].axhline(self.CODATA["G"], color='black', linestyle='--', label='CODATA')
        axes[1, 0].set_title('G (гравитация)')
        axes[1, 0].set_xlabel('C')
        axes[1, 0].set_ylabel('G')
        axes[1, 0].set_yscale('log')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)

        # alpha_em / alpha_s
        axes[1, 1].plot(C, alpha_em / alpha_s, color='orange', linewidth=1.5)
        axes[1, 1].axhline(1.0, color='black', linestyle='--', label='Равенство')
        axes[1, 1].set_title('α_em / α_s (отношение сил)')
        axes[1, 1].set_xlabel('C')
        axes[1, 1].set_ylabel('α_em / α_s')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

        return {
            "alpha_em_at_CODATA": alpha_em[idx_em],
            "alpha_s_at_CODATA": alpha_s[idx_s],
            "alpha_w_at_CODATA": alpha_w[idx_w],
            "G_at_CODATA": G[idx_G],
            "unification_max": unification[idx_unif],
            "C_at_unification": C[idx_unif]
        }


# =====================================================================
# ЗАПУСК
# =====================================================================
if __name__ == "__main__":
    model = ETVERenormalizationFlowV111()
    history = model.run_flow(steps=1000)
    results = model.analyze_flow()
