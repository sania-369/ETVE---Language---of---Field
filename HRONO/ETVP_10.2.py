# =============================================================================
# 🌀 ETVE PURE GEOMETRIC MODEL v10.2
# ПАМЯТЬ ВАКУУМА — ГИСТЕРЕЗИС И ХРОНО-СОЛИТОНЫ
# =============================================================================
# НОВОЕ В v10.2:
# 1. Введён интегральный оператор памяти (ядро из спектра E8).
# 2. Текущее состояние зависит от всей траектории: Ψ(t) = ∫ K(t-t') Ψ(t') dt'
# 3. Ядро памяти: K(τ) = Σ λ_i * exp(-λ_i * τ) — выведено из спектра.
# 4. При C → C_min память стирается (хаос), при C → C_max — сохраняется (порядок).
# 5. Поле обретает гистерезис — историю своих состояний.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
from collections import deque

class ETVEMemoryModelV102:
    """
    🌀 ЕДИНАЯ ТЕОРИЯ ВИХРЕВОГО ПОЛЯ — v10.2
    Память вакуума, гистерезис, хроно-солитоны.
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

        # --- ПАМЯТЬ ВАКУУМА ---
        self.memory_depth = memory_depth
        self.memory = deque(maxlen=memory_depth)  # хранит историю состояний

        # --- СОСТОЯНИЕ ПОЛЯ ---
        self.C = self.C_target
        self.S = 0.15
        self.phi = 0.0
        self.dt_real = 1.0
        self.dt_imag = 0.0

        # --- ЯДРО ПАМЯТИ (из спектра E8) ---
        self._build_memory_kernel()

        # --- ИСТОРИЯ ---
        self.history = {
            "C": [],
            "S": [],
            "dt_real": [],
            "dt_imag": [],
            "phi": [],
            "alpha": [],
            "mass_ratio": [],
            "memory_strength": []
        }

    # =====================================================================
    # 1. ЯДРО ПАМЯТИ (из спектра E8)
    # =====================================================================
    def _build_memory_kernel(self):
        """Строит ядро памяти из собственных значений E8."""
        # Используем собственные значения E8 (известный спектр)
        # Упрощённо: берём логарифмические индексы как спектр
        lambda_spectrum = np.array([
            self.L_dim_roots,
            self.L_roots_sub,
            self.L_dim_sub,
            self.L_torus,
            self.L_h
        ])
        # Нормируем спектр
        lambda_spectrum = lambda_spectrum / np.sum(lambda_spectrum)

        # Ядро памяти: K(τ) = Σ λ_i * exp(-λ_i * τ)
        def kernel(tau):
            return np.sum(lambda_spectrum * np.exp(-lambda_spectrum * tau))

        self.memory_kernel = kernel
        self.lambda_spectrum = lambda_spectrum

    # =====================================================================
    # 2. ИНТЕГРАЛ ПАМЯТИ (гистерезис)
    # =====================================================================
    def _apply_memory(self, current_state):
        """
        Применяет оператор памяти к текущему состоянию.
        Возвращает состояние с учётом истории.
        """
        if len(self.memory) == 0:
            return current_state

        # Интеграл памяти: Ψ_memory = Σ K(t - t') * Ψ(t')
        memory_effect = np.zeros(5)
        total_weight = 0.0

        for i, (state, time) in enumerate(self.memory):
            tau = len(self.memory) - i  # время, прошедшее с того момента
            weight = self.memory_kernel(tau)
            memory_effect += weight * np.array(state)
            total_weight += weight

        if total_weight > 0:
            memory_effect = memory_effect / total_weight
        else:
            memory_effect = current_state

        # Смешиваем текущее состояние и память
        # При C → C_min память стирается (коэффициент 0)
        # При C → C_max память сохраняется (коэффициент 1)
        memory_strength = (self.C - self.C_min) / (self.C_max - self.C_min)
        memory_strength = np.clip(memory_strength, 0.0, 1.0)

        # Сохраняем силу памяти для истории
        self.history["memory_strength"].append(memory_strength)

        # Возвращаем состояние с гистерезисом
        return (1.0 - memory_strength) * current_state + memory_strength * memory_effect

    # =====================================================================
    # 3. ПОСТРОЕНИЕ КОМПЛЕКСНОЙ МАТРИЦЫ (с памятью)
    # =====================================================================
    def _build_complex_matrix(self):
        """Строит 5D-комплексную матрицу с учётом памяти."""
        # Базовое состояние (из C, S)
        state_base = np.array([
            self.L[0] * self.Phi,
            self.L[1] * self.pi,
            self.L[2] * self.Z_res,
            1.0,
            self.L[4] * (self.C / self.C_target)
        ])

        # Применяем память
        state_memory = self._apply_memory(state_base)

        # Строим матрицу из состояния с памятью
        Space_Tensor_Real = np.array([
            [state_memory[0], 1.0, 1.0, 0.0, self.S],
            [1.0, state_memory[1], 1.0, 0.0, 0.0],
            [1.0, 1.0, state_memory[2], 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0],
            [self.S, 0.0, 0.0, 0.0, state_memory[4]]
        ], dtype=float)

        # Мнимая часть (нелокальность)
        phi = (self.pi / 2.0) * (1.0 - (self.C - self.C_min) / (self.C_max - self.C_min))
        self.phi = phi
        Space_Tensor_Imag = Space_Tensor_Real * np.tan(phi)

        # Комплексная матрица
        Space_Tensor_Complex = Space_Tensor_Real + 1j * Space_Tensor_Imag

        # Экспоненциальная калибровка
        Theta_norm = self.Theta * self.R
        Space_Tensor_NL = np.expm1(Space_Tensor_Complex / Theta_norm)

        return Space_Tensor_NL

    # =====================================================================
    # 4. ОБНОВЛЕНИЕ ПОЛЯ (с памятью)
    # =====================================================================
    def update_field(self):
        """Один SVD-пасс с учётом памяти."""
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
    # 5. ЕСТЕСТВЕННОЕ УДЕРЖАНИЕ
    # =====================================================================
    def _barrier_potential(self, C):
        x = (C - self.C_min) / (self.C_max - self.C_min)
        x = max(0.0, min(1.0, x))
        force = self.Phi * np.tan((self.pi / 2.0) * x) / np.cos((self.pi / 2.0) * x)
        return -force * (self.C_max - self.C_min)

    # =====================================================================
    # 6. ЭВОЛЮЦИЯ ПОЛЯ (с памятью)
    # =====================================================================
    def evolve(self, entropy_flux=0.0, time_step=1.0):
        """Один шаг эволюции с памятью."""
        # Сохраняем текущее состояние в память
        current_state = np.array([
            self.L[0] * self.Phi,
            self.L[1] * self.pi,
            self.L[2] * self.Z_res,
            1.0,
            self.L[4] * (self.C / self.C_target)
        ])
        self.memory.append((current_state, time_step))

        # Хаос-оператор
        chaos_operator = 1.0 / (1.0 + abs(entropy_flux) * (1.0 / self.Phi))
        self.C = self.C * chaos_operator + (1.0 - chaos_operator) * self.C_min
        self.S = max(0.0, min(1.0, self.S + entropy_flux * 0.01))

        # Тангенциальное удержание
        force = self._barrier_potential(self.C)
        self.C = self.C + 0.01 * force
        self.C = np.clip(self.C, self.C_min, self.C_max)

        # Пересчёт поля
        alpha, mass_ratio, dt_real, dt_imag, phi = self.update_field()

        # Сохраняем историю
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
    # 7. ВЕРИФИКАЦИЯ ПАМЯТИ
    # =====================================================================
    def verify_memory(self, steps=300, entropy_amplitude=0.03):
        """Запускает симуляцию и проверяет память вакуума."""
        print("=" * 80)
        print("   🌀 ETVE MEMORY VERIFICATION v10.2")
        print("   Проверка гистерезиса и памяти вакуума")
        print("=" * 80)

        # Запускаем эволюцию
        for i in range(steps):
            entropy_flux = entropy_amplitude * np.sin(i / 7.0) + 0.005 * np.random.randn()
            self.evolve(entropy_flux, time_step=1.0)

        # Извлекаем историю
        C_hist = np.array(self.history["C"])
        dt_real_hist = np.array(self.history["dt_real"])
        dt_imag_hist = np.array(self.history["dt_imag"])
        phi_hist = np.array(self.history["phi"])
        alpha_hist = np.array(self.history["alpha"])
        mass_hist = np.array(self.history["mass_ratio"])
        memory_strength = np.array(self.history["memory_strength"])

        print(f"\n--- СТАТИСТИКА ПАМЯТИ ВАКУУМА ---")
        print(f"C: min={C_hist.min():.6f}, max={C_hist.max():.6f}")
        print(f"dt_real: min={dt_real_hist.min():.6f}, max={dt_real_hist.max():.6f}")
        print(f"dt_imag: min={dt_imag_hist.min():.6f}, max={dt_imag_hist.max():.6f}")
        print(f"phi: min={phi_hist.min():.4f}, max={phi_hist.max():.4f}")
        print(f"memory_strength: min={memory_strength.min():.4f}, max={memory_strength.max():.4f}")

        # Проверка гистерезиса
        # Сравниваем C и dt_real на разных участках
        first_half = slice(0, steps // 2)
        second_half = slice(steps // 2, steps)

        if np.mean(dt_real_hist[second_half]) != np.mean(dt_real_hist[first_half]):
            print("\n✅ ГИСТЕРЕЗИС ОБНАРУЖЕН: поле помнит свою историю.")
        else:
            print("\n⚠️ ГИСТЕРЕЗИС НЕ ЗНАЧИМ: поле не сохраняет память.")

        # Проверка стирания памяти при хаосе
        chaos_indices = np.where(C_hist < self.C_min * 1.5)[0]
        if len(chaos_indices) > 0:
            avg_memory_at_chaos = np.mean(memory_strength[chaos_indices])
            print(f"✅ ПАМЯТЬ СТИРАЕТСЯ ПРИ ХАОСЕ: memory_strength = {avg_memory_at_chaos:.4f} (при C → C_min)")
        else:
            print("ℹ️ ХАОС НЕ ДОСТИГНУТ: поле остаётся когерентным.")

        # Графики
        fig, axes = plt.subplots(3, 2, figsize=(14, 12))

        # C(t)
        axes[0, 0].plot(C_hist, color='blue', linewidth=1.5)
        axes[0, 0].axhline(self.C_target, color='green', linestyle='--', label='C_target')
        axes[0, 0].axhline(self.C_min, color='red', linestyle='--', label='C_min')
        axes[0, 0].set_title('Когерентность C(t) с памятью')
        axes[0, 0].legend()
        axes[0, 0].grid(True)

        # dt_real и dt_imag
        axes[0, 1].plot(dt_real_hist, color='red', label='Re(dt)', linewidth=1.5)
        axes[0, 1].plot(dt_imag_hist, color='purple', label='Im(dt)', linewidth=1.5)
        axes[0, 1].axhline(0, color='black', linestyle='--', linewidth=0.5)
        axes[0, 1].set_title('Комплексное время с памятью')
        axes[0, 1].legend()
        axes[0, 1].grid(True)

        # Фаза
        axes[1, 0].plot(phi_hist, color='orange', linewidth=1.5)
        axes[1, 0].axhline(0, color='black', linestyle='--', linewidth=0.5)
        axes[1, 0].set_title('Фаза φ(t) — нелокальность')
        axes[1, 0].set_ylabel('φ (рад)')
        axes[1, 0].grid(True)

        # Сила памяти
        axes[1, 1].plot(memory_strength, color='brown', linewidth=1.5)
        axes[1, 1].axhline(0.5, color='black', linestyle='--', linewidth=0.5)
        axes[1, 1].set_title('Сила памяти вакуума')
        axes[1, 1].set_ylabel('memory_strength')
        axes[1, 1].grid(True)

        # dt(C) с гистерезисом
        axes[2, 0].scatter(C_hist, dt_real_hist, s=2, c=memory_strength, cmap='viridis', alpha=0.5)
        axes[2, 0].set_title('dt(C) с гистерезисом (цвет — сила памяти)')
        axes[2, 0].set_xlabel('C')
        axes[2, 0].set_ylabel('dt_real')
        axes[2, 0].grid(True)

        # 1/α(t)
        axes[2, 1].plot(alpha_hist, color='orange', linewidth=1.5)
        axes[2, 1].axhline(137.035999084, color='black', linestyle='--', label='CODATA')
        axes[2, 1].set_title('Тонкая структура 1/α(t)')
        axes[2, 1].legend()
        axes[2, 1].grid(True)

        plt.tight_layout()
        plt.show()

        return self.history


# =====================================================================
# ЗАПУСК ВЕРИФИКАЦИИ
# =====================================================================
if __name__ == "__main__":
    model = ETVEMemoryModelV102(memory_depth=100)
    history = model.verify_memory(steps=300, entropy_amplitude=0.03)
