# =============================================================================
# 🌀 ETVE PURE GEOMETRIC MODEL v10.1
# КОМПЛЕКСНАЯ СТРЕЛА ВРЕМЕНИ — НЕЛОКАЛЬНОСТЬ И ЗАПУТАННОСТЬ
# =============================================================================
# НОВОЕ В v10.1:
# 1. Матрица переведена в комплексное поле ℂ.
# 2. Мнимая часть времени: dt_imag = Im(λ₄ / λ₁) — мера нелокальности.
# 3. Фаза φ = arctan(Im(dt) / Re(dt)) — степень квантовой запутанности.
# 4. При C → C_min фаза → π/2 (максимальная нелокальность).
# 5. При C → C_max фаза → 0 (классический предел).
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma

class ETVEComplexChronoModelV101:
    """
    🌀 ЕДИНАЯ ТЕОРИЯ ВИХРЕВОГО ПОЛЯ — v10.1
    Комплексное время, нелокальность, запутанность.
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

        # --- ИНДЕКСЫ ХАУСДОРФА ---
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
        self.phi = 0.0  # фаза (мера нелокальности)

        # --- ИСТОРИЯ ---
        self.history = {
            "C": [],
            "S": [],
            "dt_real": [],
            "dt_imag": [],
            "phi": [],
            "alpha": [],
            "mass_ratio": []
        }

    # =====================================================================
    # 1. ПОСТРОЕНИЕ КОМПЛЕКСНОЙ МАТРИЦЫ
    # =====================================================================
    def _build_complex_matrix(self):
        """Строит 5D-комплексную матрицу с мнимой частью времени."""
        # Вещественная часть (как в v10.0)
        Space_Tensor_Real = np.array([
            [self.L[0] * self.Phi, 1.0, 1.0, 0.0, self.S],
            [1.0, self.L[1] * self.pi, 1.0, 0.0, 0.0],
            [1.0, 1.0, self.L[2] * self.Z_res, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0],
            [self.S, 0.0, 0.0, 0.0, self.L[4] * (self.C / self.C_target)]
        ], dtype=float)

        # Мнимая часть (нелокальность через фазу)
        # При C → C_min, imag → max (π/2), при C → C_max, imag → 0
        phi = (self.pi / 2.0) * (1.0 - (self.C - self.C_min) / (self.C_max - self.C_min))
        self.phi = phi

        # Мнимая компонента: фаза модулирует все элементы
        Space_Tensor_Imag = Space_Tensor_Real * np.tan(phi)

        # Комплексная матрица
        Space_Tensor_Complex = Space_Tensor_Real + 1j * Space_Tensor_Imag

        # Экспоненциальная калибровка (комплексная)
        Theta_norm = self.Theta * self.R
        Space_Tensor_NL = np.expm1(Space_Tensor_Complex / Theta_norm)

        return Space_Tensor_NL

    # =====================================================================
    # 2. ОБНОВЛЕНИЕ ПОЛЯ (комплексный SVD)
    # =====================================================================
    def update_field(self):
        """Один комплексный SVD-пасс — рождение времени и фазы."""
        M = self._build_complex_matrix()
        _, eigenvalues, _ = np.linalg.svd(M)

        # Константы — вещественные части отношений
        alpha_inv = np.real(eigenvalues[0] / eigenvalues[1])
        mass_ratio = np.real(eigenvalues[0] / eigenvalues[2])

        # Комплексное время
        dt_complex = eigenvalues[4] / eigenvalues[0]
        dt_real = np.real(dt_complex)
        dt_imag = np.imag(dt_complex)

        # Фаза (мера нелокальности)
        phi = np.arctan2(dt_imag, dt_real)

        # Массы
        self.MeV_invariant = self.Phi ** 30
        self.m_planck_spectral = np.prod(np.abs(eigenvalues))
        self.m_e = self.m_planck_spectral / (alpha_inv * mass_ratio * self.MeV_invariant)
        self.m_p_eV = self.m_e * mass_ratio

        # Стенка Паули
        self.wall_scale = np.real(eigenvalues[0] / (eigenvalues[1] + eigenvalues[2]))

        # Сохраняем
        self.alpha_inv = alpha_inv
        self.mass_ratio = mass_ratio
        self.dt_real = dt_real
        self.dt_imag = dt_imag
        self.phi = phi
        self.Eigenvalues = eigenvalues

        return alpha_inv, mass_ratio, dt_real, dt_imag, phi

    # =====================================================================
    # 3. ЕСТЕСТВЕННОЕ УДЕРЖАНИЕ
    # =====================================================================
    def _barrier_potential(self, C):
        x = (C - self.C_min) / (self.C_max - self.C_min)
        x = max(0.0, min(1.0, x))
        force = self.Phi * np.tan((self.pi / 2.0) * x) / np.cos((self.pi / 2.0) * x)
        return -force * (self.C_max - self.C_min)

    # =====================================================================
    # 4. ЭВОЛЮЦИЯ ПОЛЯ
    # =====================================================================
    def evolve(self, entropy_flux=0.0):
        """Один шаг эволюции с комплексным временем."""
        chaos_operator = 1.0 / (1.0 + abs(entropy_flux) * (1.0 / self.Phi))
        self.C = self.C * chaos_operator + (1.0 - chaos_operator) * self.C_min
        self.S = max(0.0, min(1.0, self.S + entropy_flux * 0.01))

        force = self._barrier_potential(self.C)
        self.C = self.C + 0.01 * force
        self.C = np.clip(self.C, self.C_min, self.C_max)

        alpha, mass_ratio, dt_real, dt_imag, phi = self.update_field()

        self.history["C"].append(self.C)
        self.history["S"].append(self.S)
        self.history["dt_real"].append(dt_real)
        self.history["dt_imag"].append(dt_imag)
        self.history["phi"].append(phi)
        self.history["alpha"].append(alpha)
        self.history["mass_ratio"].append(mass_ratio)

        return {
            "C": self.C,
            "S": self.S,
            "dt_real": dt_real,
            "dt_imag": dt_imag,
            "phi": phi,
            "1/alpha": alpha,
            "m_p/m_e": mass_ratio
        }

    # =====================================================================
    # 5. ВЕРИФИКАЦИЯ
    # =====================================================================
    def verify_complex_time(self, steps=200, entropy_amplitude=0.03):
        """Запускает симуляцию и проверяет комплексное время."""
        print("=" * 80)
        print("   🌀 ETVE COMPLEX CHRONO VERIFICATION v10.1")
        print("   Проверка нелокальности и мнимой стрелы времени")
        print("=" * 80)

        for i in range(steps):
            entropy_flux = entropy_amplitude * np.sin(i / 5.0)
            self.evolve(entropy_flux)

        C_hist = np.array(self.history["C"])
        dt_real_hist = np.array(self.history["dt_real"])
        dt_imag_hist = np.array(self.history["dt_imag"])
        phi_hist = np.array(self.history["phi"])
        alpha_hist = np.array(self.history["alpha"])
        mass_hist = np.array(self.history["mass_ratio"])

        print(f"\n--- СТАТИСТИКА КОМПЛЕКСНОГО ВРЕМЕНИ ---")
        print(f"C: min={C_hist.min():.6f}, max={C_hist.max():.6f}")
        print(f"dt_real: min={dt_real_hist.min():.6f}, max={dt_real_hist.max():.6f}")
        print(f"dt_imag: min={dt_imag_hist.min():.6f}, max={dt_imag_hist.max():.6f}")
        print(f"phi: min={phi_hist.min():.4f}, max={phi_hist.max():.4f}")

        # Проверка нелокальности
        if np.any(dt_imag_hist > 0.001):
            print("\n✅ НЕЛОКАЛЬНОСТЬ ОБНАРУЖЕНА: мнимая компонента времени > 0.")
        else:
            print("\n⚠️ НЕЛОКАЛЬНОСТЬ НЕ ЗНАЧИМА: dt_imag близка к нулю.")

        # Проверка фазы
        if np.max(phi_hist) > 0.1:
            print(f"✅ КВАНТОВАЯ ЗАПУТАННОСТЬ АКТИВНА: максимальная фаза = {np.max(phi_hist):.4f} рад.")
        else:
            print("ℹ️ ФАЗА В КЛАССИЧЕСКОМ ПРЕДЕЛЕ: система локальна.")

        # Графики
        fig, axes = plt.subplots(3, 2, figsize=(14, 12))

        # C(t)
        axes[0, 0].plot(C_hist, color='blue', linewidth=1.5)
        axes[0, 0].axhline(self.C_target, color='green', linestyle='--', label='C_target')
        axes[0, 0].set_title('Когерентность C(t)')
        axes[0, 0].legend()
        axes[0, 0].grid(True)

        # dt_real и dt_imag
        axes[0, 1].plot(dt_real_hist, color='red', label='Re(dt)', linewidth=1.5)
        axes[0, 1].plot(dt_imag_hist, color='purple', label='Im(dt)', linewidth=1.5)
        axes[0, 1].axhline(0, color='black', linestyle='--', linewidth=0.5)
        axes[0, 1].set_title('Комплексное время')
        axes[0, 1].legend()
        axes[0, 1].grid(True)

        # Фаза
        axes[1, 0].plot(phi_hist, color='orange', linewidth=1.5)
        axes[1, 0].axhline(0, color='black', linestyle='--', linewidth=0.5)
        axes[1, 0].set_title('Фаза φ(t) — мера нелокальности')
        axes[1, 0].set_ylabel('φ (рад)')
        axes[1, 0].grid(True)

        # dt_imag(C) — фазовая диаграмма нелокальности
        axes[1, 1].scatter(C_hist, dt_imag_hist, s=2, color='purple', alpha=0.5)
        axes[1, 1].axhline(0, color='black', linestyle='--', linewidth=0.5)
        axes[1, 1].set_title('dt_imag(C) — нелокальность vs когерентность')
        axes[1, 1].set_xlabel('C')
        axes[1, 1].set_ylabel('Im(dt)')
        axes[1, 1].grid(True)

        # 1/α(t)
        axes[2, 0].plot(alpha_hist, color='orange', linewidth=1.5)
        axes[2, 0].axhline(137.035999084, color='black', linestyle='--', label='CODATA')
        axes[2, 0].set_title('Тонкая структура 1/α(t)')
        axes[2, 0].legend()
        axes[2, 0].grid(True)

        # m_p/m_e(t)
        axes[2, 1].plot(mass_hist, color='green', linewidth=1.5)
        axes[2, 1].axhline(1836.15267343, color='black', linestyle='--', label='CODATA')
        axes[2, 1].set_title('Отношение масс m_p/m_e(t)')
        axes[2, 1].legend()
        axes[2, 1].grid(True)

        plt.tight_layout()
        plt.show()

        return self.history


# =====================================================================
# ЗАПУСК ВЕРИФИКАЦИИ
# =====================================================================
if __name__ == "__main__":
    model = ETVEComplexChronoModelV101()
    history = model.verify_complex_time(steps=200, entropy_amplitude=0.03)
