# =============================================================================
# 🌀 ETVE PURE GEOMETRIC MODEL v10.0
# ХРОНО-ГЕОМЕТРИЧЕСКАЯ ТЕОРИЯ — ВРЕМЯ ИЗ СПЕКТРА
# =============================================================================
# НОВОЕ В v10.0:
# 1. Время рождается из спектра: dt = λ₄ / λ₁
# 2. Пятая ось матрицы — активная временная компонента.
# 3. dt зависит от C и S через хроно-слой матрицы.
# 4. Встроен верификационный блок для проверки динамики времени.
# 5. Все константы CODATA — на месте, без подгонок.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma

class ETVEChronoModelV10:
    """
    🌀 ЕДИНАЯ ТЕОРИЯ ВИХРЕВОГО ПОЛЯ — v10.0
    Активная временная компонента через 5-ю спектральную ось (λ₄).
    """
    def __init__(self):
        # --- ФУНДАМЕНТАЛЬНЫЙ БАЗИС ---
        self.Phi = (1.0 + np.sqrt(5.0)) / 2.0
        self.pi = np.pi
        self.Z_res = np.sqrt(3.0)
        self.E8_dim = 248
        self.E8_roots = 240
        self.E8_max_sub = 128
        self.h_v = 30

        # --- Z-ПРИНЦИП (геометрические границы) ---
        self.C_min = 1.0 / (self.Phi ** 10)
        self.C_max = 1.0 - 1.0 / (self.Phi ** 20)
        self.C_target = 1.0 - 1.0 / (self.Phi ** 12)

        # --- ЛОГАРИФМИЧЕСКИЕ ОБЪЁМЫ ---
        def log_vol(n):
            return (n / 2.0) * np.log(self.pi) - np.log(gamma(n / 2.0 + 1))

        self.log_vol_E8 = log_vol(self.E8_dim)
        self.log_vol_SU8 = log_vol(63)
        self.log_vol_torus = 2.0 * self.log_vol_E8 - self.log_vol_SU8

        # --- ИНДЕКСЫ ХАУСДОРФА ---
        self.L_dim_roots = self.log_vol_E8 / log_vol(self.E8_roots)
        self.L_roots_sub = log_vol(self.E8_roots) / log_vol(self.E8_max_sub)
        self.L_dim_sub = self.log_vol_E8 / log_vol(self.E8_max_sub)
        self.L_torus = self.log_vol_torus / self.E8_dim
        self.L_h = self.h_v / self.E8_dim

        # --- БАЗОВЫЕ ИНДЕКСЫ ---
        self.L = np.array([
            self.L_dim_roots,
            self.L_roots_sub,
            self.L_dim_sub,
            self.L_torus,
            self.L_h
        ])

        # --- ГЕОМЕТРИЧЕСКИЙ МАСШТАБ Θ ---
        self.Theta = np.sqrt(self.log_vol_torus / self.h_v) * (self.log_vol_torus / self.E8_dim)

        # --- РЕГУЛЯТОРЫ (из v9.9.1) ---
        self.log_SU8 = np.log(63)
        self.log_SO16 = np.log(128)
        self.log_chrono = np.log(136)

        # --- МАТРИЦА РЕГУЛЯТОРОВ ---
        self.R = np.ones((5, 5), dtype=float)
        self.R[0, 1] = self.R[1, 0] = self.R[1, 1] = self.log_SU8
        self.R[0, 2] = self.R[2, 0] = self.R[2, 2] = self.log_SO16
        self.R[4, 4] = self.log_chrono

        # --- СОСТОЯНИЕ ПОЛЯ ---
        self.C = self.C_target
        self.S = 0.15

        # --- ИСТОРИЯ ДЛЯ ПАМЯТИ ---
        self.history = {
            "C": [],
            "S": [],
            "dt": [],
            "alpha": [],
            "mass_ratio": []
        }

    # =====================================================================
    # 1. ПОСТРОЕНИЕ ЖИВОЙ МАТРИЦЫ (с хроно-слоем)
    # =====================================================================
    def _build_matrix(self):
        """Строит 5D-матрицу с активным временным слоем."""
        # Линейная часть (с хроно-слоем)
        Space_Tensor_Linear = np.array([
            [self.L[0] * self.Phi, 1.0, 1.0, 0.0, self.S],
            [1.0, self.L[1] * self.pi, 1.0, 0.0, 0.0],
            [1.0, 1.0, self.L[2] * self.Z_res, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0],
            [self.S, 0.0, 0.0, 0.0, self.L[4] * (self.C / self.C_target)]
        ], dtype=float)

        # Экспоненциальная калибровка с регуляторами
        Theta_norm = self.Theta * self.R
        Space_Tensor_NL = np.expm1(Space_Tensor_Linear / Theta_norm)

        return Space_Tensor_NL

    # =====================================================================
    # 2. ОБНОВЛЕНИЕ ПОЛЯ (SVD-пасс)
    # =====================================================================
    def update_field(self):
        """Один SVD-пасс — рождение времени и констант."""
        M = self._build_matrix()
        _, eigenvalues, _ = np.linalg.svd(M)

        # Константы (как в v9.9.1)
        self.alpha_inv = eigenvalues[0] / eigenvalues[1]
        self.mass_ratio = eigenvalues[0] / eigenvalues[2]

        # ВРЕМЯ РОЖДАЕТСЯ ИЗ СПЕКТРА
        self.dt = eigenvalues[4] / eigenvalues[0]

        # Массы
        self.MeV_invariant = self.Phi ** 30
        self.m_planck_spectral = np.prod(eigenvalues)
        self.m_e = self.m_planck_spectral / (self.alpha_inv * self.mass_ratio * self.MeV_invariant)
        self.m_p_eV = self.m_e * self.mass_ratio

        # Стенка Паули
        self.wall_scale = eigenvalues[0] / (eigenvalues[1] + eigenvalues[2])

        # Сохраняем спектр
        self.Eigenvalues = eigenvalues

        return self.alpha_inv, self.mass_ratio, self.dt

    # =====================================================================
    # 3. ЕСТЕСТВЕННОЕ УДЕРЖАНИЕ (тангенциальный барьер)
    # =====================================================================
    def _barrier_potential(self, C):
        x = (C - self.C_min) / (self.C_max - self.C_min)
        x = max(0.0, min(1.0, x))
        force = self.Phi * np.tan((self.pi / 2.0) * x) / np.cos((self.pi / 2.0) * x)
        return -force * (self.C_max - self.C_min)

    # =====================================================================
    # 4. ЭВОЛЮЦИЯ ПОЛЯ (шаг по времени)
    # =====================================================================
    def evolve(self, entropy_flux=0.0):
        """Один шаг эволюции поля."""
        # Хаос-оператор
        chaos_operator = 1.0 / (1.0 + abs(entropy_flux) * (1.0 / self.Phi))
        self.C = self.C * chaos_operator + (1.0 - chaos_operator) * self.C_min
        self.S = max(0.0, min(1.0, self.S + entropy_flux * 0.01))

        # Тангенциальное удержание
        force = self._barrier_potential(self.C)
        self.C = self.C + 0.01 * force
        self.C = np.clip(self.C, self.C_min, self.C_max)

        # Пересчёт поля
        alpha, mass_ratio, dt = self.update_field()

        # Сохраняем историю
        self.history["C"].append(self.C)
        self.history["S"].append(self.S)
        self.history["dt"].append(dt)
        self.history["alpha"].append(alpha)
        self.history["mass_ratio"].append(mass_ratio)

        return {
            "C": self.C,
            "S": self.S,
            "dt": dt,
            "1/alpha": alpha,
            "m_p/m_e": mass_ratio
        }

    # =====================================================================
    # 5. ВЕРИФИКАЦИЯ ДИНАМИКИ ВРЕМЕНИ
    # =====================================================================
    def verify_time_dynamics(self, steps=100, entropy_amplitude=0.02):
        """Запускает симуляцию и проверяет поведение времени."""
        print("=" * 80)
        print("   🌀 ETVE CHRONO VERIFICATION v10.0")
        print("   Проверка рождения времени из спектра")
        print("=" * 80)

        # Запускаем эволюцию
        for i in range(steps):
            entropy_flux = entropy_amplitude * np.sin(i / 5.0)
            self.evolve(entropy_flux)

        # Извлекаем историю
        C_hist = np.array(self.history["C"])
        dt_hist = np.array(self.history["dt"])
        alpha_hist = np.array(self.history["alpha"])
        mass_hist = np.array(self.history["mass_ratio"])

        # Статистика
        print(f"\n--- СТАТИСТИКА ДИНАМИКИ ---")
        print(f"C: min={C_hist.min():.6f}, max={C_hist.max():.6f}, mean={C_hist.mean():.6f}")
        print(f"dt: min={dt_hist.min():.6f}, max={dt_hist.max():.6f}, mean={dt_hist.mean():.6f}")
        print(f"1/α: min={alpha_hist.min():.4f}, max={alpha_hist.max():.4f}, mean={alpha_hist.mean():.4f}")
        print(f"m_p/m_e: min={mass_hist.min():.1f}, max={mass_hist.max():.1f}, mean={mass_hist.mean():.1f}")

        # Проверка причинности
        if np.all(dt_hist > 0):
            print("\n✅ ПРИЧИННОСТЬ СОХРАНЕНА: dt > 0 на всей траектории.")
        else:
            print("\n❌ НАРУШЕНИЕ ПРИЧИННОСТИ: обнаружены dt <= 0.")

        # Проверка корреляции C и dt
        if np.corrcoef(C_hist, dt_hist)[0, 1] > 0:
            print("✅ ВРЕМЯ УСКОРЯЕТСЯ ПРИ РОСТЕ C (корреляция положительная).")
        else:
            print("⚠️ ВРЕМЯ ЗАМЕДЛЯЕТСЯ ПРИ РОСТЕ C (корреляция отрицательная).")

        # Точка покоя
        target_idx = np.argmin(np.abs(C_hist - self.C_target))
        print(f"\n--- ТОЧКА ПОКОЯ (ближайшая к C_target) ---")
        print(f"C = {C_hist[target_idx]:.6f}")
        print(f"dt = {dt_hist[target_idx]:.6f}")
        print(f"1/α = {alpha_hist[target_idx]:.4f} (CODATA: 137.035999084)")
        print(f"m_p/m_e = {mass_hist[target_idx]:.2f} (CODATA: 1836.15267343)")

        # --- ГРАФИКИ ---
        fig, axes = plt.subplots(3, 2, figsize=(14, 10))

        # C(t)
        axes[0, 0].plot(C_hist, color='blue', linewidth=1.5)
        axes[0, 0].axhline(self.C_target, color='green', linestyle='--', label='C_target')
        axes[0, 0].axhline(self.C_min, color='red', linestyle='--', label='C_min')
        axes[0, 0].axhline(self.C_max, color='red', linestyle='--', label='C_max')
        axes[0, 0].set_title('Когерентность C(t)')
        axes[0, 0].set_ylabel('C')
        axes[0, 0].legend()
        axes[0, 0].grid(True)

        # dt(t)
        axes[0, 1].plot(dt_hist, color='red', linewidth=1.5)
        axes[0, 1].axhline(1.0, color='black', linestyle='--', label='dt = 1 (норма)')
        axes[0, 1].set_title('Живое время dt(t)')
        axes[0, 1].set_ylabel('dt')
        axes[0, 1].legend()
        axes[0, 1].grid(True)

        # dt(C)
        axes[1, 0].scatter(C_hist, dt_hist, s=2, color='purple', alpha=0.5)
        axes[1, 0].set_title('dt(C) — фазовая диаграмма времени')
        axes[1, 0].set_xlabel('C')
        axes[1, 0].set_ylabel('dt')
        axes[1, 0].grid(True)

        # 1/α(t)
        axes[1, 1].plot(alpha_hist, color='orange', linewidth=1.5)
        axes[1, 1].axhline(137.035999084, color='black', linestyle='--', label='CODATA')
        axes[1, 1].set_title('Тонкая структура 1/α(t)')
        axes[1, 1].set_ylabel('1/α')
        axes[1, 1].legend()
        axes[1, 1].grid(True)

        # m_p/m_e(t)
        axes[2, 0].plot(mass_hist, color='green', linewidth=1.5)
        axes[2, 0].axhline(1836.15267343, color='black', linestyle='--', label='CODATA')
        axes[2, 0].set_title('Отношение масс m_p/m_e(t)')
        axes[2, 0].set_ylabel('m_p/m_e')
        axes[2, 0].legend()
        axes[2, 0].grid(True)

        # dt(1/α) — проверка связи времени и электродинамики
        axes[2, 1].scatter(alpha_hist, dt_hist, s=2, color='brown', alpha=0.5)
        axes[2, 1].set_title('dt(1/α) — связь времени и заряда')
        axes[2, 1].set_xlabel('1/α')
        axes[2, 1].set_ylabel('dt')
        axes[2, 1].grid(True)

        plt.tight_layout()
        plt.show()

        return self.history

# =====================================================================
# ЗАПУСК ВЕРИФИКАЦИИ
# =====================================================================
if __name__ == "__main__":
    model = ETVEChronoModelV10()
    history = model.verify_time_dynamics(steps=200, entropy_amplitude=0.03)
