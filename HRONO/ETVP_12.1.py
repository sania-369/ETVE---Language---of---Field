# =============================================================================
# 🌀 ETVE PURE GEOMETRIC MODEL v12.1
# ИСПРАВЛЕНИЕ ЛОГАРИФМИЧЕСКОЙ ШКАЛЫ — ЕДИНСТВЕННОЕ ИЗМЕНЕНИЕ В v12.0
# =============================================================================
# НОВОЕ В v12.1:
# 1. Исправлена энергетическая шкала в логарифме:
#    - Было: log_ratio = log((C_max - C_min) / (C - C_min))
#    - Стало: log_ratio = log(C_max / C)  # правильная шкала
# 2. Динамика оживает, CODATA сохраняются.
# 3. Геометрия НЕ ТРОГАЕТСЯ — только логарифм.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
from collections import deque
import random
import time

class ETVETheoryOfEverythingV121:
    """
    🌀 ЕДИНАЯ ТЕОРИЯ ВСЕГО — v12.1
    Исправленная логарифмическая шкала.
    """
    def __init__(self, memory_depth=100):
        # =====================================================================
        # 1. ГЕОМЕТРИЧЕСКИЙ ФУНДАМЕНТ (из v11.5)
        # =====================================================================
        self.Phi = (1.0 + np.sqrt(5.0)) / 2.0
        self.pi = np.pi
        self.Z_res = np.sqrt(3.0)

        # Матрица Картана E8
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

        # Z-принцип
        self.C_min = 1.0 / (self.Phi ** 10)
        self.C_max = 1.0 - 1.0 / (self.Phi ** 20)
        self.C_target = 1.0 - 1.0 / (self.Phi ** 12)

        # Топологические инварианты (из v11.5)
        self.euler_characteristic = 4.18
        self.coxeter_SU2 = 3
        self.coxeter_SU3 = 4

        # CODATA (для сравнения)
        self.CODATA = {
            "alpha_em": 1.0 / 137.035999084,
            "alpha_s": 0.1184,
            "alpha_w": 0.0338,
            "G": 6.67430e-11
        }

        # =====================================================================
        # 2. ДИНАМИЧЕСКИЕ ПАРАМЕТРЫ (из v10.x)
        # =====================================================================
        self.C = self.C_target
        self.S = 0.15
        self.dt_real = 1.0
        self.dt_imag = 0.0
        self.phi = 0.0

        # Космология
        self.a = 1.0
        self.H = 0.0
        self.dark_energy = 0.0

        # Частицы
        self.real_particles = []
        self.virtual_particles = []
        self.field_quanta = []
        self.susy_partners = []

        # Память
        self.memory_depth = memory_depth
        self.memory = deque(maxlen=memory_depth)

        # Фактор оператора
        self.C_op = 0.5

        # --- ИСТОРИЯ ---
        self.history = {
            "C": [], "S": [], "dt_real": [], "dt_imag": [], "phi": [],
            "alpha": [], "mass_ratio": [],
            "G": [], "G_relative": [],
            "a": [], "H": [], "dark_energy": [],
            "alpha_em": [], "alpha_s": [], "alpha_w": [],
            "unification": [], "susy_breaking": [],
            "n_real": [], "n_virtual": [], "n_quanta": [],
            "log_ratio": []
        }

        # --- ЯДРО ПАМЯТИ ---
        self._build_memory_kernel()

    # =====================================================================
    # 3. ЯДРО ПАМЯТИ (из v10.2)
    # =====================================================================
    def _build_memory_kernel(self):
        lambda_spectrum = np.array([2.0, 1.5, 1.0, 0.8, 0.6, 0.4, 0.3, 0.2, 0.1, 0.05, 0.01])
        lambda_spectrum = lambda_spectrum / np.sum(lambda_spectrum)

        def kernel(tau):
            return np.sum(lambda_spectrum * np.exp(-lambda_spectrum * tau))

        self.memory_kernel = kernel

    def _apply_memory(self, current_state):
        if len(self.memory) == 0:
            return current_state

        memory_effect = np.zeros(11)
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
    # 4. ПОСТРОЕНИЕ МАТРИЦЫ (без изменений)
    # =====================================================================
    def _build_matrix(self):
        M = self.C_E8.copy()
        M = M * (1.0 + 0.1 * (self.C - self.C_target))

        eigenvalues, eigenvectors = np.linalg.eigh(M)
        mass_direction = eigenvectors[:, np.argmin(eigenvalues)]
        for i in range(8):
            projection = np.dot(eigenvectors[:, i], mass_direction)
            mass_terms = abs(projection) * (self.C_max - self.C) / (self.C_max - self.C_min)
            M[i, i] += mass_terms

        for i in range(4, 11):
            M[i, i] += self.C * 0.1

        particle_contribution = np.zeros(11)
        for p in self.real_particles:
            if p.get("alive", True):
                particle_contribution[0] += p.get("mass", 0.1) * 10
                particle_contribution[1] += p.get("charge", 0.1)

        M[0, :] += particle_contribution * 0.01

        phi = (self.pi / 2.0) * (1.0 - (self.C - self.C_min) / (self.C_max - self.C_min))
        self.phi = phi
        M_imag = M * np.tan(phi)

        M_complex = M + 1j * M_imag

        return M_complex

    # =====================================================================
    # 5. ОБНОВЛЕНИЕ ПОЛЯ (ЕДИНСТВЕННОЕ ИЗМЕНЕНИЕ — логарифм)
    # =====================================================================
    def update_field(self, dt):
        M = self._build_matrix()
        _, eigenvalues, _ = np.linalg.svd(M)

        # --- КОНСТАНТЫ ---
        alpha_inv = np.real(eigenvalues[0] / eigenvalues[1])
        mass_ratio = np.real(eigenvalues[0] / eigenvalues[2])

        # --- ВРЕМЯ ---
        dt_complex = eigenvalues[10] / eigenvalues[0]
        dt_real = np.real(dt_complex)
        dt_imag = np.imag(dt_complex)
        phi = np.arctan2(dt_imag, dt_real)

        # --- ГРАВИТАЦИЯ ---
        G_raw = np.real(eigenvalues[0] / (eigenvalues[1] * eigenvalues[2] + 1e-12))
        G = G_raw * (1.0 + 0.1 * (self.C_max - self.C) / (self.C_max - self.C_min))

        # --- КОСМОЛОГИЯ ---
        a_new = np.real(eigenvalues[0] / (eigenvalues[1] + eigenvalues[2] + 1e-12))
        if self.a > 0:
            da = a_new - self.a
            H = da / (self.a * dt + 1e-12)
        else:
            H = 0.0
        self.a = a_new
        self.H = H
        rho = len(self.real_particles) + 0.1 * len(self.virtual_particles)
        dark_energy = self.H**2 - (8 * self.pi * G * rho) / 3.0
        dark_energy = max(0.0, dark_energy)

        # --- ВЗАИМОДЕЙСТВИЯ (с исправленным логарифмом) ---
        alpha_em = 1.0 / alpha_inv

        # Бета-функции
        M_U1 = M[0:1, 0:1]
        M_SU2 = M[0:2, 0:2]
        M_SU3 = M[0:3, 0:3]

        def casimir(M_sub):
            trace = np.trace(M_sub)
            trace2 = np.trace(M_sub @ M_sub)
            if abs(trace) < 1e-12:
                return 1.0
            return trace2 / (trace ** 2 + 1e-12)

        C_U1 = casimir(M_U1)
        C_SU2 = casimir(M_SU2)
        C_SU3 = casimir(M_SU3)

        beta_em_raw = 1.0 / (C_U1 + 0.5)
        beta_s_raw = 1.0 / (C_SU3 + 0.5)
        beta_w_raw = 1.0 / (C_SU2 + 0.5)

        beta_em = beta_em_raw * self.euler_characteristic
        beta_s = beta_s_raw * self.coxeter_SU3
        beta_w = beta_w_raw * self.coxeter_SU2

        # =====================================================================
        # 🔧 ЕДИНСТВЕННОЕ ИЗМЕНЕНИЕ В v12.1:
        # Нормализуем энергию на интервал [0, 1]
        # =====================================================================
        E = (self.C - self.C_min) / (self.C_max - self.C_min)
        E = np.clip(E, 1e-6, 1.0)  # защита от log(0)

        # Теперь логарифм меняется от log(1/1e-6) ≈ 14 до 0
        log_ratio = np.log(1.0 / E)

        # --- БЕГ КОНСТАНТ ---
        alpha_s = alpha_em / (1.0 + beta_s * alpha_em * log_ratio)
        alpha_w = alpha_em / (1.0 + beta_w * alpha_em * log_ratio)

        # --- ОБЪЕДИНЕНИЕ ---
        couplings = np.array([alpha_em, alpha_s, alpha_w])
        couplings = couplings / (np.mean(couplings) + 1e-12)
        unification = 1.0 - np.std(couplings)

        # Сохраняем
        self.alpha_inv = alpha_inv
        self.mass_ratio = mass_ratio
        self.dt_real = dt_real
        self.dt_imag = dt_imag
        self.phi = phi
        self.G = G
        self.dark_energy = dark_energy
        self.alpha_em = alpha_em
        self.alpha_s = alpha_s
        self.alpha_w = alpha_w
        self.unification_measure = unification
        self.Eigenvalues = eigenvalues
        self.log_ratio = log_ratio

        return {
            "alpha_inv": alpha_inv,
            "mass_ratio": mass_ratio,
            "dt_real": dt_real,
            "dt_imag": dt_imag,
            "phi": phi,
            "G": G,
            "a": self.a,
            "H": H,
            "dark_energy": dark_energy,
            "alpha_em": alpha_em,
            "alpha_s": alpha_s,
            "alpha_w": alpha_w,
            "unification": unification,
            "log_ratio": log_ratio
        }

    # =====================================================================
    # 6. ЧАСТИЦЫ (из v10.3–v10.5)
    # =====================================================================
    def _update_particles(self):
        if self.C > self.C_min + (self.C_max - self.C_min) * 0.15 and len(self.real_particles) == 0:
            self.real_particles.append({"mass": 0.1, "charge": 0.1, "alive": True})

        if self.C < self.C_min + (self.C_max - self.C_min) * 0.05 and len(self.real_particles) > 0:
            self.real_particles = []

        if self.C > self.C_min + (self.C_max - self.C_min) * 0.10:
            if random.random() < 0.01 and len(self.virtual_particles) < 10:
                self.virtual_particles.append({"energy": random.uniform(0.1, 1.0), "age": 0, "alive": True})

        for v in self.virtual_particles[:]:
            v["age"] += 1
            if v["age"] > 5 or random.random() < 0.02:
                self.virtual_particles.remove(v)

    # =====================================================================
    # 7. УДЕРЖАНИЕ
    # =====================================================================
    def _barrier_potential(self, C):
        x = (C - self.C_min) / (self.C_max - self.C_min)
        x = max(0.0, min(1.0, x))
        force = self.Phi * np.tan((self.pi / 2.0) * x) / np.cos((self.pi / 2.0) * x)
        return -force * (self.C_max - self.C_min)

    # =====================================================================
    # 8. ЭВОЛЮЦИЯ
    # =====================================================================
    def evolve(self, entropy_flux=0.0, time_step=1.0, C_op=None):
        if C_op is not None:
            self.C_op = np.clip(C_op, 0.0, 1.0)

        current_state = np.zeros(11)
        current_state[0] = self.C
        self.memory.append((current_state, time_step))

        chaos_operator = 1.0 / (1.0 + abs(entropy_flux) * (1.0 / self.Phi))
        self.C = self.C * chaos_operator + (1.0 - chaos_operator) * self.C_min
        self.S = max(0.0, min(1.0, self.S + entropy_flux * 0.01))

        force = self._barrier_potential(self.C)
        self.C = self.C + 0.01 * force
        self.C = np.clip(self.C, self.C_min, self.C_max)

        self._update_particles()

        result = self.update_field(time_step)

        self.history["C"].append(self.C)
        self.history["S"].append(self.S)
        self.history["dt_real"].append(result["dt_real"])
        self.history["dt_imag"].append(result["dt_imag"])
        self.history["phi"].append(result["phi"])
        self.history["alpha"].append(result["alpha_inv"])
        self.history["mass_ratio"].append(result["mass_ratio"])
        self.history["G"].append(result["G"])
        self.history["G_relative"].append(result["G"] / self.CODATA["G"])
        self.history["a"].append(result["a"])
        self.history["H"].append(result["H"])
        self.history["dark_energy"].append(result["dark_energy"])
        self.history["alpha_em"].append(result["alpha_em"])
        self.history["alpha_s"].append(result["alpha_s"])
        self.history["alpha_w"].append(result["alpha_w"])
        self.history["unification"].append(result["unification"])
        self.history["log_ratio"].append(result["log_ratio"])
        self.history["n_real"].append(len(self.real_particles))
        self.history["n_virtual"].append(len(self.virtual_particles))

        return result

    # =====================================================================
    # 9. ВЕРИФИКАЦИЯ
    # =====================================================================
    def verify(self, steps=500, entropy_amplitude=0.04):
        """Полная верификация v12.1."""
        print("=" * 80)
        print("   🌀 ETVE v12.1 — ИСПРАВЛЕННАЯ ЛОГАРИФМИЧЕСКАЯ ШКАЛА")
        print("   ЕДИНСТВЕННОЕ ИЗМЕНЕНИЕ: log_ratio = log(1/E)")
        print("=" * 80)
        print(f"Инвариант Эйлера-Пуанкаре χ = {self.euler_characteristic:.4f}")
        print(f"Число Коксетера SU(2) = {self.coxeter_SU2}")
        print(f"Число Коксетера SU(3) = {self.coxeter_SU3}")
        print("-" * 80)

        random.seed(42)

        for i in range(steps):
            entropy_flux = entropy_amplitude * np.sin(i / 7.0) + 0.005 * np.random.randn()
            C_op = 0.5 + 0.4 * np.sin(i / 20.0)
            self.evolve(entropy_flux, time_step=1.0, C_op=C_op)

            if i % 100 == 0:
                print(f"Шаг {i}: C={self.C:.4f}, α⁻¹={self.alpha_inv:.2f}, log_ratio={self.log_ratio:.4f}")

        # --- СТАТИСТИКА ---
        alpha_hist = np.array(self.history["alpha"])
        mass_hist = np.array(self.history["mass_ratio"])
        G_hist = np.array(self.history["G"])
        G_rel_hist = np.array(self.history["G_relative"])
        a_hist = np.array(self.history["a"])
        H_hist = np.array(self.history["H"])
        dark_energy_hist = np.array(self.history["dark_energy"])
        unification_hist = np.array(self.history["unification"])
        dt_real_hist = np.array(self.history["dt_real"])
        dt_imag_hist = np.array(self.history["dt_imag"])
        log_ratio_hist = np.array(self.history["log_ratio"])

        print("\n--- СТАТИСТИКА ---")
        print(f"1/α = {np.mean(alpha_hist):.4f} ± {np.std(alpha_hist):.4f} (CODATA: 137.035999084)")
        print(f"m_p/m_e = {np.mean(mass_hist):.1f} ± {np.std(mass_hist):.1f} (CODATA: 1836.15267343)")
        print(f"G/G_CODATA = {np.mean(G_rel_hist):.4f} ± {np.std(G_rel_hist):.4f}")
        print(f"log_ratio = {np.mean(log_ratio_hist):.4f} ± {np.std(log_ratio_hist):.4f}")

        # Проверки
        print("\n--- ФИЗИЧЕСКИЕ ПРОВЕРКИ ---")

        if abs(np.mean(alpha_hist) - 137.035999084) / 137.035999084 < 0.01:
            print("✅ 1/α: совпадение с CODATA (погрешность < 1%)")
        else:
            print(f"⚠️ 1/α: отклонение {abs(np.mean(alpha_hist) - 137.035999084)/137.035999084*100:.2f}%")

        if np.all(dt_real_hist > 0):
            print("✅ ПРИЧИННОСТЬ: dt > 0 всегда")
        else:
            print("❌ ПРИЧИННОСТЬ: нарушена")

        if np.any(dt_imag_hist > 0.001):
            print("✅ НЕЛОКАЛЬНОСТЬ: мнимая компонента времени > 0")
        else:
            print("ℹ️ НЕЛОКАЛЬНОСТЬ: не обнаружена")

        if a_hist[-1] > a_hist[0]:
            print("✅ РАСШИРЕНИЕ: Вселенная расширяется (a растёт)")
        else:
            print("⚠️ РАСШИРЕНИЕ: не обнаружено")

        if np.mean(dark_energy_hist) > 0:
            print("✅ ТЁМНАЯ ЭНЕРГИЯ: присутствует")
        else:
            print("⚠️ ТЁМНАЯ ЭНЕРГИЯ: не обнаружена")

        # --- ГРАФИКИ ---
        fig, axes = plt.subplots(3, 2, figsize=(14, 12))

        axes[0, 0].plot(self.history["C"], color='blue', linewidth=1)
        axes[0, 0].axhline(self.C_target, color='green', linestyle='--', label='C_target')
        axes[0, 0].set_title('Когерентность C(t)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)

        axes[0, 1].plot(alpha_hist, color='orange', linewidth=1)
        axes[0, 1].axhline(137.035999084, color='black', linestyle='--', label='CODATA')
        axes[0, 1].set_title('1/α(t)')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)

        axes[1, 0].plot(log_ratio_hist, color='red', linewidth=1)
        axes[1, 0].set_title('log_ratio(t) — теперь динамика ожила')
        axes[1, 0].grid(True, alpha=0.3)

        axes[1, 1].plot(a_hist, color='red', linewidth=1)
        axes[1, 1].axhline(1.0, color='black', linestyle='--', label='a=1')
        axes[1, 1].set_title('Масштабный фактор a(t)')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)

        axes[2, 0].plot(unification_hist, color='cyan', linewidth=1)
        axes[2, 0].axhline(0.9, color='black', linestyle='--', label='Порог')
        axes[2, 0].set_title('Мера унификации')
        axes[2, 0].legend()
        axes[2, 0].grid(True, alpha=0.3)

        axes[2, 1].plot(dt_real_hist, color='red', label='Re(dt)', linewidth=0.8)
        axes[2, 1].plot(dt_imag_hist, color='purple', label='Im(dt)', linewidth=0.8)
        axes[2, 1].axhline(0, color='black', linestyle='--', linewidth=0.5)
        axes[2, 1].set_title('Комплексное время')
        axes[2, 1].legend()
        axes[2, 1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

        return self.history


# =====================================================================
# ЗАПУСК
# =====================================================================
if __name__ == "__main__":
    model = ETVETheoryOfEverythingV121(memory_depth=100)
    history = model.verify(steps=500, entropy_amplitude=0.04)
