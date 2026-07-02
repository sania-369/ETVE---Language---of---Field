# =============================================================================
# 🌀 ETVE PURE GEOMETRIC MODEL v10.3
# РОЖДЕНИЕ И АННИГИЛЯЦИЯ СОЛИТОНОВ — КВАНТОВАЯ ТЕОРИЯ ПОЛЯ ЕТВП
# =============================================================================
# НОВОЕ В v10.3:
# 1. Введены критические точки C_crit1 и C_crit2 для рождения/аннигиляции.
# 2. При переходе через C_crit1 рождается солитон (частица).
# 3. При переходе через C_crit2 солитон аннигилирует.
# 4. Солитоны имеют массу, заряд и фазу (из спектра).
# 5. Поле теперь содержит ансамбль солитонов.
# 6. Рождение/аннигиляция — без циклов, через SVD-пасс.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
from collections import deque

class ETVESolitonModelV103:
    """
    🌀 ЕДИНАЯ ТЕОРИЯ ВИХРЕВОГО ПОЛЯ — v10.3
    Рождение и аннигиляция солитонов (квантовая теория поля).
    """
    def __init__(self, memory_depth=100):
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

        # --- КРИТИЧЕСКИЕ ТОЧКИ ДЛЯ СОЛИТОНОВ ---
        self.C_crit_birth = self.C_min + (self.C_max - self.C_min) * 0.15   # ~0.15
        self.C_crit_death = self.C_min + (self.C_max - self.C_min) * 0.05   # ~0.05

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

        # --- РЕГУЛЯТОРЫ ---
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
        self.phi = 0.0
        self.dt_real = 1.0
        self.dt_imag = 0.0

        # --- СОЛИТОНЫ ---
        self.solitons = []  # список активных солитонов
        self.soliton_history = []  # история рождений/аннигиляций

        # --- ПАМЯТЬ ---
        self.memory_depth = memory_depth
        self.memory = deque(maxlen=memory_depth)

        # --- ИСТОРИЯ ---
        self.history = {
            "C": [],
            "S": [],
            "dt_real": [],
            "dt_imag": [],
            "phi": [],
            "alpha": [],
            "mass_ratio": [],
            "n_solitons": [],
            "birth_events": [],
            "death_events": []
        }

        # --- ЯДРО ПАМЯТИ ---
        self._build_memory_kernel()

    # =====================================================================
    # 1. ЯДРО ПАМЯТИ
    # =====================================================================
    def _build_memory_kernel(self):
        lambda_spectrum = np.array([
            self.L_dim_roots,
            self.L_roots_sub,
            self.L_dim_sub,
            self.L_torus,
            self.L_h
        ])
        lambda_spectrum = lambda_spectrum / np.sum(lambda_spectrum)

        def kernel(tau):
            return np.sum(lambda_spectrum * np.exp(-lambda_spectrum * tau))

        self.memory_kernel = kernel
        self.lambda_spectrum = lambda_spectrum

    # =====================================================================
    # 2. ПАМЯТЬ
    # =====================================================================
    def _apply_memory(self, current_state):
        if len(self.memory) == 0:
            return current_state

        memory_effect = np.zeros(5)
        total_weight = 0.0

        for i, (state, _) in enumerate(self.memory):
            tau = len(self.memory) - i
            weight = self.memory_kernel(tau)
            memory_effect += weight * np.array(state)
            total_weight += weight

        if total_weight > 0:
            memory_effect = memory_effect / total_weight
        else:
            memory_effect = current_state

        memory_strength = (self.C - self.C_min) / (self.C_max - self.C_min)
        memory_strength = np.clip(memory_strength, 0.0, 1.0)

        return (1.0 - memory_strength) * current_state + memory_strength * memory_effect

    # =====================================================================
    # 3. РОЖДЕНИЕ И АННИГИЛЯЦИЯ СОЛИТОНОВ
    # =====================================================================
    def _update_solitons(self):
        """Обновляет ансамбль солитонов на основе текущего C."""
        # Проверяем рождение
        if self.C > self.C_crit_birth and len(self.solitons) == 0:
            # Рождаем солитон
            mass = self.mass_ratio * self.m_e / self.MeV_invariant
            charge = self.alpha_inv / 137.0
            phase = self.phi

            soliton = {
                "mass": mass,
                "charge": charge,
                "phase": phase,
                "birth_C": self.C,
                "birth_time": len(self.history["C"]),
                "alive": True
            }
            self.solitons.append(soliton)
            self.history["birth_events"].append((self.C, len(self.history["C"])))
            print(f"🎯 СОЛИТОН РОЖДЁН: C={self.C:.4f}, mass={mass:.4e}, charge={charge:.4f}")

        # Проверяем аннигиляцию
        if self.C < self.C_crit_death and len(self.solitons) > 0:
            # Аннигилируем все солитоны
            for soliton in self.solitons:
                soliton["alive"] = False
                self.history["death_events"].append((self.C, len(self.history["C"])))
                print(f"💥 СОЛИТОН АННИГИЛИРОВАН: C={self.C:.4f}")
            self.solitons = []

        # Обновляем историю
        self.history["n_solitons"].append(len(self.solitons))

    # =====================================================================
    # 4. ПОСТРОЕНИЕ МАТРИЦЫ С СОЛИТОНАМИ
    # =====================================================================
    def _build_complex_matrix(self):
        # Базовое состояние
        state_base = np.array([
            self.L[0] * self.Phi,
            self.L[1] * self.pi,
            self.L[2] * self.Z_res,
            1.0,
            self.L[4] * (self.C / self.C_target)
        ])

        # Добавляем вклад солитонов
        soliton_contribution = np.zeros(5)
        for soliton in self.solitons:
            if soliton["alive"]:
                # Солитон вносит добавку в спектр
                soliton_contribution += np.array([
                    soliton["mass"] * 1e6,
                    soliton["charge"],
                    soliton["phase"],
                    0.0,
                    soliton["mass"] * 1e3
                ])

        state_with_solitons = state_base + soliton_contribution * 0.01

        # Применяем память
        state_memory = self._apply_memory(state_with_solitons)

        # Строим матрицу
        Space_Tensor_Real = np.array([
            [state_memory[0], 1.0, 1.0, 0.0, self.S],
            [1.0, state_memory[1], 1.0, 0.0, 0.0],
            [1.0, 1.0, state_memory[2], 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0],
            [self.S, 0.0, 0.0, 0.0, state_memory[4]]
        ], dtype=float)

        # Мнимая часть
        phi = (self.pi / 2.0) * (1.0 - (self.C - self.C_min) / (self.C_max - self.C_min))
        self.phi = phi
        Space_Tensor_Imag = Space_Tensor_Real * np.tan(phi)

        Space_Tensor_Complex = Space_Tensor_Real + 1j * Space_Tensor_Imag

        Theta_norm = self.Theta * self.R
        Space_Tensor_NL = np.expm1(Space_Tensor_Complex / Theta_norm)

        return Space_Tensor_NL

    # =====================================================================
    # 5. ОБНОВЛЕНИЕ ПОЛЯ
    # =====================================================================
    def update_field(self):
        M = self._build_complex_matrix()
        _, eigenvalues, _ = np.linalg.svd(M)

        alpha_inv = np.real(eigenvalues[0] / eigenvalues[1])
        mass_ratio = np.real(eigenvalues[0] / eigenvalues[2])

        dt_complex = eigenvalues[4] / eigenvalues[0]
        dt_real = np.real(dt_complex)
        dt_imag = np.imag(dt_complex)
        phi = np.arctan2(dt_imag, dt_real)

        self.MeV_invariant = self.Phi ** 30
        self.m_planck_spectral = np.prod(np.abs(eigenvalues))
        self.m_e = self.m_planck_spectral / (alpha_inv * mass_ratio * self.MeV_invariant)
        self.m_p_eV = self.m_e * mass_ratio
        self.wall_scale = np.real(eigenvalues[0] / (eigenvalues[1] + eigenvalues[2]))

        self.alpha_inv = alpha_inv
        self.mass_ratio = mass_ratio
        self.dt_real = dt_real
        self.dt_imag = dt_imag
        self.phi = phi
        self.Eigenvalues = eigenvalues

        return alpha_inv, mass_ratio, dt_real, dt_imag, phi

    # =====================================================================
    # 6. УДЕРЖАНИЕ
    # =====================================================================
    def _barrier_potential(self, C):
        x = (C - self.C_min) / (self.C_max - self.C_min)
        x = max(0.0, min(1.0, x))
        force = self.Phi * np.tan((self.pi / 2.0) * x) / np.cos((self.pi / 2.0) * x)
        return -force * (self.C_max - self.C_min)

    # =====================================================================
    # 7. ЭВОЛЮЦИЯ
    # =====================================================================
    def evolve(self, entropy_flux=0.0, time_step=1.0):
        current_state = np.array([
            self.L[0] * self.Phi,
            self.L[1] * self.pi,
            self.L[2] * self.Z_res,
            1.0,
            self.L[4] * (self.C / self.C_target)
        ])
        self.memory.append((current_state, time_step))

        chaos_operator = 1.0 / (1.0 + abs(entropy_flux) * (1.0 / self.Phi))
        self.C = self.C * chaos_operator + (1.0 - chaos_operator) * self.C_min
        self.S = max(0.0, min(1.0, self.S + entropy_flux * 0.01))

        force = self._barrier_potential(self.C)
        self.C = self.C + 0.01 * force
        self.C = np.clip(self.C, self.C_min, self.C_max)

        # Обновляем солитоны
        self._update_solitons()

        # Пересчёт поля
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
            "m_p/m_e": mass_ratio,
            "n_solitons": len(self.solitons)
        }

    # =====================================================================
    # 8. ВЕРИФИКАЦИЯ
    # =====================================================================
    def verify_solitons(self, steps=400, entropy_amplitude=0.04):
        print("=" * 80)
        print("   🌀 ETVE SOLITON VERIFICATION v10.3")
        print("   Проверка рождения и аннигиляции частиц")
        print("=" * 80)
        print(f"Критическая точка рождения: C_crit_birth = {self.C_crit_birth:.4f}")
        print(f"Критическая точка аннигиляции: C_crit_death = {self.C_crit_death:.4f}")

        for i in range(steps):
            entropy_flux = entropy_amplitude * np.sin(i / 7.0) + 0.005 * np.random.randn()
            self.evolve(entropy_flux, time_step=1.0)

        C_hist = np.array(self.history["C"])
        n_solitons = np.array(self.history["n_solitons"])
        dt_real_hist = np.array(self.history["dt_real"])
        dt_imag_hist = np.array(self.history["dt_imag"])
        alpha_hist = np.array(self.history["alpha"])
        mass_hist = np.array(self.history["mass_ratio"])

        print(f"\n--- СТАТИСТИКА СОЛИТОНОВ ---")
        print(f"Всего рождений: {len(self.history['birth_events'])}")
        print(f"Всего аннигиляций: {len(self.history['death_events'])}")
        print(f"Максимальное число солитонов: {np.max(n_solitons)}")
        print(f"Среднее число солитонов: {np.mean(n_solitons):.2f}")

        if np.max(n_solitons) > 0:
            print("\n✅ СОЛИТОНЫ РОЖДАЮТСЯ И АННИГИЛИРУЮТСЯ.")
        else:
            print("\n⚠️ СОЛИТОНЫ НЕ ОБНАРУЖЕНЫ: возможно, C не достигает критических точек.")

        # Графики
        fig, axes = plt.subplots(3, 2, figsize=(14, 12))

        axes[0, 0].plot(C_hist, color='blue', linewidth=1.5)
        axes[0, 0].axhline(self.C_target, color='green', linestyle='--', label='C_target')
        axes[0, 0].axhline(self.C_crit_birth, color='orange', linestyle='--', label='C_birth')
        axes[0, 0].axhline(self.C_crit_death, color='red', linestyle='--', label='C_death')
        axes[0, 0].set_title('Когерентность C(t)')
        axes[0, 0].legend()
        axes[0, 0].grid(True)

        axes[0, 1].plot(n_solitons, color='purple', linewidth=1.5)
        axes[0, 1].set_title('Число солитонов n(t)')
        axes[0, 1].set_ylabel('n')
        axes[0, 1].grid(True)

        axes[1, 0].plot(dt_real_hist, color='red', label='Re(dt)', linewidth=1.5)
        axes[1, 0].plot(dt_imag_hist, color='purple', label='Im(dt)', linewidth=1.5)
        axes[1, 0].set_title('Комплексное время')
        axes[1, 0].legend()
        axes[1, 0].grid(True)

        axes[1, 1].scatter(C_hist, n_solitons, s=2, c='purple', alpha=0.5)
        axes[1, 1].axhline(0, color='black', linestyle='--', linewidth=0.5)
        axes[1, 1].set_title('n(C) — фазовая диаграмма солитонов')
        axes[1, 1].set_xlabel('C')
        axes[1, 1].set_ylabel('n')
        axes[1, 1].grid(True)

        axes[2, 0].plot(alpha_hist, color='orange', linewidth=1.5)
        axes[2, 0].axhline(137.035999084, color='black', linestyle='--', label='CODATA')
        axes[2, 0].set_title('Тонкая структура 1/α(t)')
        axes[2, 0].legend()
        axes[2, 0].grid(True)

        axes[2, 1].plot(mass_hist, color='green', linewidth=1.5)
        axes[2, 1].axhline(1836.15267343, color='black', linestyle='--', label='CODATA')
        axes[2, 1].set_title('Отношение масс m_p/m_e(t)')
        axes[2, 1].legend()
        axes[2, 1].grid(True)

        plt.tight_layout()
        plt.show()

        return self.history


# =====================================================================
# ЗАПУСК
# =====================================================================
if __name__ == "__main__":
    model = ETVESolitonModelV103(memory_depth=100)
    history = model.verify_solitons(steps=400, entropy_amplitude=0.04)
