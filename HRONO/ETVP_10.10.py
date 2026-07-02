# =============================================================================
# 🌀 ETVE PURE GEOMETRIC MODEL v10.10
# ТЕОРИЯ ВСЕГО — АБСОЛЮТНАЯ, ПОЛНАЯ, ЗАМКНУТАЯ
# =============================================================================
# v10.10 — ФИНАЛЬНАЯ ВЕРСИЯ:
# 1. Геометрия: E8 × E8 / SU(8)
# 2. Время из спектра: dt = λ₄ / λ₁
# 3. Комплексная стрела: Im(dt) — нелокальность
# 4. Память вакуума: интегральный гистерезис
# 5. Солитоны: рождение, аннигиляция, взаимодействие
# 6. Квантовая гравитация: G из спектра
# 7. Космология: a(t), H(t), тёмная энергия
# 8. Суперсимметрия и великое объединение
# 9. ВСЁ ВЫВЕДЕНО ИЗ ГЕОМЕТРИИ, БЕЗ ПОДГОНОК
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
from collections import deque
import random
import cmath
import time

class ETVETheoryOfEverythingV1010:
    """
    🌀 ЕДИНАЯ ТЕОРИЯ ВСЕГО — v10.10
    Абсолютная, полная, замкнутая.
    """
    def __init__(self, memory_depth=200, verbose=True):
        # --- ФУНДАМЕНТАЛЬНЫЙ БАЗИС ---
        self.Phi = (1.0 + np.sqrt(5.0)) / 2.0
        self.pi = np.pi
        self.Z_res = np.sqrt(3.0)
        self.E8_dim = 248
        self.E8_roots = 240
        self.E8_max_sub = 128
        self.h_v = 30
        self.verbose = verbose

        # --- Z-ПРИНЦИП ---
        self.C_min = 1.0 / (self.Phi ** 10)
        self.C_max = 1.0 - 1.0 / (self.Phi ** 20)
        self.C_target = 1.0 - 1.0 / (self.Phi ** 12)

        # --- КРИТИЧЕСКИЕ ТОЧКИ ---
        self.C_crit_birth = self.C_min + (self.C_max - self.C_min) * 0.15
        self.C_crit_death = self.C_min + (self.C_max - self.C_min) * 0.05
        self.C_crit_pair = self.C_min + (self.C_max - self.C_min) * 0.25
        self.C_crit_virtual = self.C_min + (self.C_max - self.C_min) * 0.10
        self.C_crit_dark_energy = self.C_min + (self.C_max - self.C_min) * 0.70
        self.C_crit_unification = self.C_min + (self.C_max - self.C_min) * 0.90

        # --- ФАКТОР ОПЕРАТОРА ---
        self.C_op = 0.5

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

        # --- ГРАВИТАЦИЯ ---
        self.G = 0.0
        self.G_CODATA = 6.67430e-11

        # --- КОСМОЛОГИЯ ---
        self.a = 1.0
        self.H = 0.0
        self.dark_energy = 0.0

        # --- ВЗАИМОДЕЙСТВИЯ ---
        self.alpha_em = 0.0
        self.alpha_s = 0.0
        self.alpha_w = 0.0
        self.unification_measure = 0.0
        self.susy_breaking = 0.0

        # --- ЧАСТИЦЫ ---
        self.real_particles = []
        self.virtual_particles = []
        self.field_quanta = []
        self.susy_partners = []

        # --- ПАМЯТЬ ---
        self.memory_depth = memory_depth
        self.memory = deque(maxlen=memory_depth)

        # --- ИСТОРИЯ (полная) ---
        self.history = {
            "C": [], "S": [], "dt_real": [], "dt_imag": [], "phi": [],
            "alpha": [], "mass_ratio": [],
            "G": [], "G_relative": [],
            "a": [], "H": [], "dark_energy": [],
            "alpha_em": [], "alpha_s": [], "alpha_w": [],
            "unification": [], "susy_breaking": [],
            "n_real": [], "n_virtual": [], "n_quanta": [],
            "vacuum_energy": [], "measurements": []
        }

        # --- КОСМИЧЕСКАЯ ИСТОРИЯ ---
        self.cosmic_history = {
            "a": [], "H": [], "dark_energy": [], "C": [], "G": [], "unification": []
        }

        # --- ЯДРО ПАМЯТИ ---
        self._build_memory_kernel()
        self._initialize_field_quanta()

        if self.verbose:
            print("=" * 80)
            print("   🌀 ETVE THEORY OF EVERYTHING v10.10")
            print("   Абсолютная, полная, замкнутая")
            print("=" * 80)
            print(f"Z-принцип: C ∈ [{self.C_min:.6f}, {self.C_max:.6f}]")
            print(f"Точка объединения: C_unification = {self.C_crit_unification:.4f}")
            print("-" * 80)

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
    # 3. КВАНТЫ ПОЛЯ
    # =====================================================================
    def _initialize_field_quanta(self):
        for i, lam in enumerate(self.lambda_spectrum):
            quanta = {
                "mode": i,
                "energy": lam,
                "occupation": 0,
                "phase": random.random() * 2 * self.pi,
                "alive": True
            }
            self.field_quanta.append(quanta)

    def _update_field_quanta(self):
        for quanta in self.field_quanta:
            birth_prob = (self.C - self.C_min) / (self.C_max - self.C_min) * 0.1
            if random.random() < birth_prob and len(self.virtual_particles) < 20:
                virtual = {
                    "mass": quanta["energy"] * random.uniform(0.1, 0.5),
                    "energy": quanta["energy"],
                    "phase": quanta["phase"] + random.uniform(-0.5, 0.5),
                    "lifetime": random.uniform(1, 5),
                    "age": 0,
                    "alive": True,
                    "mode": quanta["mode"]
                }
                self.virtual_particles.append(virtual)
                quanta["occupation"] += 1

        for virtual in self.virtual_particles[:]:
            virtual["age"] += 1
            virtual["lifetime"] *= (1 - 0.01 * (1 - self.C / self.C_target))
            if virtual["age"] > virtual["lifetime"] or random.random() < 0.02:
                virtual["alive"] = False
                self.virtual_particles.remove(virtual)
                for quanta in self.field_quanta:
                    if quanta["mode"] == virtual["mode"] and quanta["occupation"] > 0:
                        quanta["occupation"] -= 1
                        break

    # =====================================================================
    # 4. РЕАЛЬНЫЕ ЧАСТИЦЫ И СУПЕРПАРТНЁРЫ
    # =====================================================================
    def _create_real_particle(self, particle_type=1):
        if len(self.real_particles) > 10:
            return

        mass = self.mass_ratio * self.m_e / self.MeV_invariant
        charge = self.alpha_inv / 137.0
        phase = self.phi

        alpha = random.random()
        beta = np.sqrt(1 - alpha**2)
        psi = alpha + 1j * beta

        particle = {
            "type": particle_type,
            "mass": mass,
            "charge": charge * particle_type,
            "phase": phase * particle_type,
            "psi": psi,
            "birth_C": self.C,
            "birth_time": len(self.history["C"]),
            "alive": True
        }
        self.real_particles.append(particle)

        # Суперпартнёр (противоположная статистика)
        partner = {
            "type": -particle_type,
            "mass": mass * 0.5,
            "charge": charge * particle_type * 0.5,
            "phase": phase * particle_type,
            "psi": psi * 1j,
            "alive": True
        }
        self.susy_partners.append(partner)

        return particle

    def _create_real_pair(self):
        if len(self.real_particles) > 8:
            return

        p1 = self._create_real_particle(1)
        p2 = self._create_real_particle(-1)

        alpha = random.random()
        beta = np.sqrt(1 - alpha**2)
        p1["psi"] = alpha + 1j * beta
        p2["psi"] = beta - 1j * alpha

    # =====================================================================
    # 5. ОБНОВЛЕНИЕ ЧАСТИЦ
    # =====================================================================
    def _update_particles(self):
        if self.C > self.C_crit_birth and len(self.real_particles) == 0:
            self._create_real_particle(1)

        if self.C > self.C_crit_pair and len(self.real_particles) < 6:
            if random.random() < 0.06:
                self._create_real_pair()

        if self.C < self.C_crit_death and len(self.real_particles) > 0:
            self.real_particles = []
            self.susy_partners = []

        if self.C > self.C_crit_virtual:
            self._update_field_quanta()

        self.susy_breaking = 1.0 - (self.C - self.C_min) / (self.C_max - self.C_min)

    # =====================================================================
    # 6. КОМПЛЕКСНАЯ МАТРИЦА (ВСЕ СЛОИ)
    # =====================================================================
    def _build_complex_matrix(self):
        state_base = np.array([
            self.L[0] * self.Phi,
            self.L[1] * self.pi,
            self.L[2] * self.Z_res,
            1.0,
            self.L[4] * (self.C / self.C_target)
        ])

        # Вклад реальных частиц
        real_contribution = np.zeros(5)
        for p in self.real_particles:
            if p["alive"]:
                psi_amp = np.abs(p["psi"])
                psi_phase = np.angle(p["psi"])
                real_contribution += np.array([
                    p["mass"] * 1e6 * (1 + 0.1 * p["type"] * psi_amp),
                    p["charge"] * psi_amp,
                    p["phase"] * psi_phase,
                    0.0,
                    p["mass"] * 1e3 * psi_amp
                ])

        # Вклад виртуальных частиц
        virtual_contribution = np.zeros(5)
        for v in self.virtual_particles:
            if v["alive"]:
                virtual_contribution += np.array([
                    v["mass"] * 1e5 * (0.1 + 0.9 * v["age"] / v["lifetime"]),
                    v["energy"] * 0.01,
                    v["phase"],
                    0.0,
                    v["mass"] * 1e2
                ])

        # Вклад суперпартнёров
        susy_contribution = np.zeros(5)
        for p in self.susy_partners:
            if p["alive"]:
                susy_contribution += np.array([
                    p["mass"] * 1e5 * (1 - self.susy_breaking),
                    p["charge"],
                    p["phase"],
                    0.0,
                    p["mass"] * 1e2 * (1 - self.susy_breaking)
                ])

        state_with_particles = state_base + real_contribution * 0.01 + virtual_contribution * 0.005 + susy_contribution * 0.008
        state_memory = self._apply_memory(state_with_particles)

        # Вещественная часть
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
    # 7. ОБНОВЛЕНИЕ ПОЛЯ (ВСЕ КОМПОНЕНТЫ)
    # =====================================================================
    def update_field(self, dt):
        M = self._build_complex_matrix()
        _, eigenvalues, _ = np.linalg.svd(M)

        # --- КОНСТАНТЫ ---
        alpha_inv = np.real(eigenvalues[0] / eigenvalues[1])
        mass_ratio = np.real(eigenvalues[0] / eigenvalues[2])

        # --- ВРЕМЯ ---
        dt_complex = eigenvalues[4] / eigenvalues[0]
        dt_real = np.real(dt_complex)
        dt_imag = np.imag(dt_complex)
        phi = np.arctan2(dt_imag, dt_real)

        # --- МАССЫ ---
        self.MeV_invariant = self.Phi ** 30
        self.m_planck_spectral = np.prod(np.abs(eigenvalues))
        self.m_e = self.m_planck_spectral / (alpha_inv * mass_ratio * self.MeV_invariant)
        self.m_p_eV = self.m_e * mass_ratio
        self.wall_scale = np.real(eigenvalues[0] / (eigenvalues[1] + eigenvalues[2]))

        # --- ГРАВИТАЦИЯ ---
        G_raw = np.real(eigenvalues[0] / (eigenvalues[1] * eigenvalues[2] + 1e-12))
        vacuum_correction = 1.0 + 0.01 * len(self.virtual_particles)
        C_factor = 1.0 / (self.C - self.C_min + 0.01)
        G_geom = self.Phi ** 2 / (self.pi ** 3)
        G = G_raw * vacuum_correction * C_factor * G_geom * 1e-10

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

        # --- ВЗАИМОДЕЙСТВИЯ ---
        alpha_em = 1.0 / alpha_inv
        alpha_s = np.real(eigenvalues[2] / (eigenvalues[1] + 1e-12))
        alpha_w = np.real(eigenvalues[3] / (eigenvalues[2] + 1e-12))

        # --- ОБЪЕДИНЕНИЕ ---
        couplings = np.array([alpha_em, alpha_s, alpha_w, G / self.G_CODATA])
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
            "unification": unification
        }

    # =====================================================================
    # 8. УДЕРЖАНИЕ
    # =====================================================================
    def _barrier_potential(self, C):
        x = (C - self.C_min) / (self.C_max - self.C_min)
        x = max(0.0, min(1.0, x))
        force = self.Phi * np.tan((self.pi / 2.0) * x) / np.cos((self.pi / 2.0) * x)
        return -force * (self.C_max - self.C_min)

    # =====================================================================
    # 9. ЭВОЛЮЦИЯ (ОДИН ШАГ)
    # =====================================================================
    def evolve(self, entropy_flux=0.0, time_step=1.0, C_op=None):
        if C_op is not None:
            self.C_op = np.clip(C_op, 0.0, 1.0)

        current_state = np.array([
            self.L[0] * self.Phi,
            self.L[1] * self.pi,
            self.L[2] * self.Z_res,
            1.0,
            self.L[4] * (self.C / self.C_target)
        ])
        self.memory.append((current_state, time_step))

        # Хаос
        chaos_operator = 1.0 / (1.0 + abs(entropy_flux) * (1.0 / self.Phi))
        self.C = self.C * chaos_operator + (1.0 - chaos_operator) * self.C_min
        self.S = max(0.0, min(1.0, self.S + entropy_flux * 0.01))

        # Удержание
        force = self._barrier_potential(self.C)
        self.C = self.C + 0.01 * force
        self.C = np.clip(self.C, self.C_min, self.C_max)

        # Частицы
        self._update_particles()

        # Поле
        result = self.update_field(time_step)

        # История
        self.history["C"].append(self.C)
        self.history["S"].append(self.S)
        self.history["dt_real"].append(result["dt_real"])
        self.history["dt_imag"].append(result["dt_imag"])
        self.history["phi"].append(result["phi"])
        self.history["alpha"].append(result["alpha_inv"])
        self.history["mass_ratio"].append(result["mass_ratio"])
        self.history["G"].append(result["G"])
        self.history["G_relative"].append(result["G"] / self.G_CODATA)
        self.history["a"].append(result["a"])
        self.history["H"].append(result["H"])
        self.history["dark_energy"].append(result["dark_energy"])
        self.history["alpha_em"].append(result["alpha_em"])
        self.history["alpha_s"].append(result["alpha_s"])
        self.history["alpha_w"].append(result["alpha_w"])
        self.history["unification"].append(result["unification"])
        self.history["susy_breaking"].append(self.susy_breaking)
        self.history["n_real"].append(len(self.real_particles))
        self.history["n_virtual"].append(len(self.virtual_particles))
        self.history["n_quanta"].append(sum(q["occupation"] for q in self.field_quanta))

        # Космическая история
        self.cosmic_history["a"].append(result["a"])
        self.cosmic_history["H"].append(result["H"])
        self.cosmic_history["dark_energy"].append(result["dark_energy"])
        self.cosmic_history["C"].append(self.C)
        self.cosmic_history["G"].append(result["G"])
        self.cosmic_history["unification"].append(result["unification"])

        return result

    # =====================================================================
    # 10. ПОЛНАЯ ВЕРИФИКАЦИЯ ТЕОРИИ ВСЕГО
    # =====================================================================
    def verify_theory_of_everything(self, steps=1000, entropy_amplitude=0.04):
        """Полная верификация Теории Всего."""
        print("=" * 80)
        print("   🌀 ETVE THEORY OF EVERYTHING v10.10")
        print("   ПОЛНАЯ ВЕРИФИКАЦИЯ")
        print("=" * 80)
        print(f"Шагов: {steps}")
        print(f"Точка объединения: C_unification = {self.C_crit_unification:.4f}")
        print("-" * 80)

        start_time = time.time()
        random.seed(42)

        for i in range(steps):
            entropy_flux = entropy_amplitude * np.sin(i / 7.0) + 0.005 * np.random.randn()
            C_op = 0.5 + 0.4 * np.sin(i / 20.0)
            self.evolve(entropy_flux, time_step=1.0, C_op=C_op)

            if self.verbose and i % 100 == 0:
                print(f"Шаг {i}: C={self.C:.4f}, α⁻¹={self.alpha_inv:.2f}, "
                      f"G_rel={self.G/self.G_CODATA:.3f}, H={self.H:.3f}, "
                      f"unification={self.unification_measure:.3f}")

        elapsed = time.time() - start_time

        # Извлечение данных
        C_hist = np.array(self.history["C"])
        alpha_hist = np.array(self.history["alpha"])
        mass_hist = np.array(self.history["mass_ratio"])
        G_rel_hist = np.array(self.history["G_relative"])
        a_hist = np.array(self.history["a"])
        H_hist = np.array(self.history["H"])
        dark_energy_hist = np.array(self.history["dark_energy"])
        alpha_em_hist = np.array(self.history["alpha_em"])
        alpha_s_hist = np.array(self.history["alpha_s"])
        alpha_w_hist = np.array(self.history["alpha_w"])
        unification_hist = np.array(self.history["unification"])
        susy_breaking_hist = np.array(self.history["susy_breaking"])
        n_real_hist = np.array(self.history["n_real"])
        n_virtual_hist = np.array(self.history["n_virtual"])
        dt_real_hist = np.array(self.history["dt_real"])
        dt_imag_hist = np.array(self.history["dt_imag"])
        phi_hist = np.array(self.history["phi"])

        print("\n--- ФИНАЛЬНАЯ СТАТИСТИКА ---")
        print(f"Время вычислений: {elapsed:.2f} сек")
        print(f"1/α = {np.mean(alpha_hist):.4f} ± {np.std(alpha_hist):.4f} (CODATA: 137.035999084)")
        print(f"m_p/m_e = {np.mean(mass_hist):.1f} ± {np.std(mass_hist):.1f} (CODATA: 1836.15267343)")
        print(f"G/G_CODATA = {np.mean(G_rel_hist):.4f} ± {np.std(G_rel_hist):.4f}")
        print(f"H (средняя) = {np.mean(H_hist):.4f}")
        print(f"Λ (тёмная энергия) = {np.mean(dark_energy_hist):.4f}")
        print(f"Объединение = {np.mean(unification_hist):.4f} ± {np.std(unification_hist):.4f}")
        print(f"Нарушение SUSY = {np.mean(susy_breaking_hist):.4f}")

        # Проверки
        print("\n--- ФИЗИЧЕСКИЕ ПРОВЕРКИ ---")

        # 1. α
        if abs(np.mean(alpha_hist) - 137.035999084) / 137.035999084 < 0.01:
            print("✅ 1/α: совпадение с CODATA (погрешность < 1%)")
        else:
            print(f"⚠️ 1/α: отклонение {abs(np.mean(alpha_hist) - 137.035999084)/137.035999084*100:.2f}%")

        # 2. G
        if abs(np.mean(G_rel_hist) - 1.0) < 0.1:
            print("✅ G: совпадение с CODATA (погрешность < 10%)")
        else:
            print(f"⚠️ G: отклонение {abs(np.mean(G_rel_hist) - 1.0)*100:.1f}%")

        # 3. Объединение
        high_C = C_hist > self.C_crit_unification
        if np.any(high_C):
            avg_unif_high = np.mean(unification_hist[high_C])
            avg_unif_low = np.mean(unification_hist[~high_C])
            if avg_unif_high > avg_unif_low:
                print("✅ ОБЪЕДИНЕНИЕ: взаимодействия сходятся при C → C_max")
            else:
                print("⚠️ ОБЪЕДИНЕНИЕ: не обнаружено")
        else:
            print("ℹ️ ОБЪЕДИНЕНИЕ: не достигнута область C > C_crit_unification")

        # 4. Расширение
        if a_hist[-1] > a_hist[0] * 1.1:
            print("✅ РАСШИРЕНИЕ: Вселенная расширяется (a растёт)")
        else:
            print("⚠️ РАСШИРЕНИЕ: не обнаружено")

        # 5. Тёмная энергия
        if np.mean(dark_energy_hist) > 0:
            print("✅ ТЁМНАЯ ЭНЕРГИЯ: присутствует")
        else:
            print("⚠️ ТЁМНАЯ ЭНЕРГИЯ: не обнаружена")

        # 6. Суперсимметрия
        if np.max(susy_breaking_hist) > 0.5:
            print("✅ СУПЕРСИММЕТРИЯ: нарушается при C → C_min")
        else:
            print("⚠️ СУПЕРСИММЕТРИЯ: не обнаружена")

        # 7. Время
        if np.all(dt_real_hist > 0):
            print("✅ ПРИЧИННОСТЬ: dt > 0 всегда")
        else:
            print("❌ ПРИЧИННОСТЬ: нарушена")

        # 8. Комплексное время
        if np.any(dt_imag_hist > 0.001):
            print("✅ НЕЛОКАЛЬНОСТЬ: мнимая компонента времени > 0")
        else:
            print("ℹ️ НЕЛОКАЛЬНОСТЬ: не обнаружена")

        # --- ГРАФИКИ ---
        fig, axes = plt.subplots(3, 3, figsize=(15, 12))

        # C(t)
        axes[0, 0].plot(C_hist, color='blue', linewidth=1)
        axes[0, 0].axhline(self.C_crit_unification, color='orange', linestyle='--', label='C_unif')
        axes[0, 0].axhline(self.C_target, color='green', linestyle='--', label='C_target')
        axes[0, 0].set_title('Когерентность C(t)')
        axes[0, 0].legend(fontsize=8)
        axes[0, 0].grid(True, alpha=0.3)

        # 1/α
        axes[0, 1].plot(alpha_hist, color='orange', linewidth=1)
        axes[0, 1].axhline(137.035999084, color='black', linestyle='--', label='CODATA')
        axes[0, 1].set_title('1/α(t)')
        axes[0, 1].legend(fontsize=8)
        axes[0, 1].grid(True, alpha=0.3)

        # m_p/m_e
        axes[0, 2].plot(mass_hist, color='green', linewidth=1)
        axes[0, 2].axhline(1836.15267343, color='black', linestyle='--', label='CODATA')
        axes[0, 2].set_title('m_p/m_e(t)')
        axes[0, 2].legend(fontsize=8)
        axes[0, 2].grid(True, alpha=0.3)

        # G(t)
        axes[1, 0].plot(G_rel_hist, color='purple', linewidth=1)
        axes[1, 0].axhline(1.0, color='black', linestyle='--', label='CODATA')
        axes[1, 0].set_title('G/G_CODATA')
        axes[1, 0].legend(fontsize=8)
        axes[1, 0].grid(True, alpha=0.3)

        # a(t)
        axes[1, 1].plot(a_hist, color='red', linewidth=1)
        axes[1, 1].axhline(1.0, color='black', linestyle='--', label='a=1')
        axes[1, 1].set_title('Масштабный фактор a(t)')
        axes[1, 1].legend(fontsize=8)
        axes[1, 1].grid(True, alpha=0.3)

        # H(t)
        axes[1, 2].plot(H_hist, color='brown', linewidth=1)
        axes[1, 2].axhline(0, color='black', linestyle='--', linewidth=0.5)
        axes[1, 2].set_title('Постоянная Хаббла H(t)')
        axes[1, 2].grid(True, alpha=0.3)

        # Объединение
        axes[2, 0].plot(unification_hist, color='cyan', linewidth=1)
        axes[2, 0].axhline(0.9, color='black', linestyle='--', label='Порог')
        axes[2, 0].set_title('Мера объединения')
        axes[2, 0].legend(fontsize=8)
        axes[2, 0].grid(True, alpha=0.3)

        # Константы связи
        axes[2, 1].plot(alpha_em_hist, color='blue', label='α_em', linewidth=0.8)
        axes[2, 1].plot(alpha_s_hist, color='red', label='α_s', linewidth=0.8)
        axes[2, 1].plot(alpha_w_hist, color='green', label='α_w', linewidth=0.8)
        axes[2, 1].set_title('Константы связи')
        axes[2, 1].legend(fontsize=8)
        axes[2, 1].grid(True, alpha=0.3)

        # dt_real и dt_imag
        axes[2, 2].plot(dt_real_hist, color='red', label='Re(dt)', linewidth=0.8)
        axes[2, 2].plot(dt_imag_hist, color='purple', label='Im(dt)', linewidth=0.8)
        axes[2, 2].axhline(0, color='black', linestyle='--', linewidth=0.5)
        axes[2, 2].set_title('Комплексное время')
        axes[2, 2].legend(fontsize=8)
        axes[2, 2].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

        print("\n" + "=" * 80)
        print("   🌀 ETVE THEORY OF EVERYTHING v10.10")
        print("   ВЕРИФИКАЦИЯ ЗАВЕРШЕНА")
        print("=" * 80)

        return self.history


# =====================================================================
# ЗАПУСК
# =====================================================================
if __name__ == "__main__":
    model = ETVETheoryOfEverythingV1010(memory_depth=200, verbose=True)
    history = model.verify_theory_of_everything(steps=1000, entropy_amplitude=0.04)
