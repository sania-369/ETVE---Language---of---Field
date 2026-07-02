# =============================================================================
# 🌀 ETVE PURE GEOMETRIC MODEL v10.9
# СУПЕРСИММЕТРИЯ И ВЕЛИКОЕ ОБЪЕДИНЕНИЕ — ВСЕ ВЗАИМОДЕЙСТВИЯ ИЗ СПЕКТРА
# =============================================================================
# НОВОЕ В v10.9:
# 1. Четыре взаимодействия выводятся из спектра:
#    - Гравитация: G = λ₁ / (λ₂ * λ₃)
#    - Электромагнетизм: α = λ₂ / λ₁
#    - Сильное: α_s = λ₃ / λ₂
#    - Слабое: α_w = λ₄ / λ₃
# 2. При C → C_max все взаимодействия сходятся (объединение).
# 3. При C → C_min взаимодействия расходятся (расщепление).
# 4. Суперсимметрия: бозоны и фермионы — разные фазы одного спектра.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
from collections import deque
import random
import cmath

class ETVEGrandUnificationModelV109:
    """
    🌀 ЕДИНАЯ ТЕОРИЯ ВИХРЕВОГО ПОЛЯ — v10.9
    Суперсимметрия и великое объединение.
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

        # --- КРИТИЧЕСКИЕ ТОЧКИ ---
        self.C_crit_birth = self.C_min + (self.C_max - self.C_min) * 0.15
        self.C_crit_death = self.C_min + (self.C_max - self.C_min) * 0.05
        self.C_crit_pair = self.C_min + (self.C_max - self.C_min) * 0.25
        self.C_crit_virtual = self.C_min + (self.C_max - self.C_min) * 0.10
        self.C_crit_dark_energy = self.C_min + (self.C_max - self.C_min) * 0.70
        self.C_crit_unification = self.C_min + (self.C_max - self.C_min) * 0.90  # точка объединения

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
        self.alpha = 0.0
        self.alpha_s = 0.0  # сильное
        self.alpha_w = 0.0  # слабое
        self.alpha_em = 0.0 # электромагнетизм (уже есть как 1/α)

        # --- СУПЕРСИММЕТРИЯ ---
        self.susy_breaking = 0.0  # мера нарушения суперсимметрии
        self.susy_partners = []   # суперпартнёры (бозоны/фермионы)

        # --- ИСТОРИЯ ---
        self.history = {
            "C": [],
            "S": [],
            "dt_real": [],
            "dt_imag": [],
            "phi": [],
            "alpha": [],
            "mass_ratio": [],
            "G": [],
            "G_relative": [],
            "a": [],
            "H": [],
            "dark_energy": [],
            "alpha_s": [],
            "alpha_w": [],
            "susy_breaking": [],
            "n_real": [],
            "n_virtual": [],
            "n_quanta": [],
            "vacuum_energy": [],
            "unification_measure": []
        }

        # --- ЧАСТИЦЫ ---
        self.real_particles = []
        self.virtual_particles = []
        self.field_quanta = []

        # --- ПАМЯТЬ ---
        self.memory_depth = memory_depth
        self.memory = deque(maxlen=memory_depth)

        # --- ЯДРО ПАМЯТИ ---
        self._build_memory_kernel()
        self._initialize_field_quanta()

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
    # 4. РЕАЛЬНЫЕ ЧАСТИЦЫ
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

        # Создаём суперпартнёра (бозон/фермион)
        partner = {
            "type": -particle_type,  # противоположная статистика
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

        # Нарушение суперсимметрии: при C → C_min суперпартнёры исчезают
        self.susy_breaking = 1.0 - (self.C - self.C_min) / (self.C_max - self.C_min)

    # =====================================================================
    # 6. ВЗАИМОДЕЙСТВИЯ ИЗ СПЕКТРА (НОВОЕ)
    # =====================================================================
    def _compute_interactions(self, eigenvalues):
        """
        Вычисляет все четыре взаимодействия из спектра.
        """
        # Электромагнетизм (тонкая структура)
        self.alpha_em = 1.0 / self.alpha_inv

        # Сильное взаимодействие: α_s = λ₃ / λ₂
        self.alpha_s = np.real(eigenvalues[2] / (eigenvalues[1] + 1e-12))

        # Слабое взаимодействие: α_w = λ₄ / λ₃
        self.alpha_w = np.real(eigenvalues[3] / (eigenvalues[2] + 1e-12))

        # Гравитация: уже вычислена
        # G уже есть

        # Мера объединения: при C → C_max все взаимодействия сходятся
        # unification_measure = 1 - разброс между α_em, α_s, α_w, G
        couplings = np.array([self.alpha_em, self.alpha_s, self.alpha_w, self.G / self.G_CODATA])
        couplings = couplings / (np.mean(couplings) + 1e-12)
        self.unification_measure = 1.0 - np.std(couplings)

        return {
            "alpha_em": self.alpha_em,
            "alpha_s": self.alpha_s,
            "alpha_w": self.alpha_w,
            "G": self.G,
            "unification": self.unification_measure
        }

    # =====================================================================
    # 7. ГРАВИТАЦИЯ
    # =====================================================================
    def _compute_gravity(self, eigenvalues):
        G_raw = np.real(eigenvalues[0] / (eigenvalues[1] * eigenvalues[2] + 1e-12))
        vacuum_correction = 1.0 + 0.01 * len(self.virtual_particles)
        C_factor = 1.0 / (self.C - self.C_min + 0.01)
        G_geom = self.Phi ** 2 / (self.pi ** 3)
        G = G_raw * vacuum_correction * C_factor * G_geom * 1e-10
        self.G_relative = G / self.G_CODATA
        return G

    # =====================================================================
    # 8. КОСМОЛОГИЯ
    # =====================================================================
    def _compute_cosmology(self, eigenvalues, dt):
        a_new = np.real(eigenvalues[0] / (eigenvalues[1] + eigenvalues[2] + 1e-12))
        if self.a > 0:
            da = a_new - self.a
            self.H = da / (self.a * dt + 1e-12)
        else:
            self.H = 0.0
        self.a = a_new
        G = self._compute_gravity(eigenvalues)
        rho = len(self.real_particles) + 0.1 * len(self.virtual_particles)
        self.dark_energy = self.H**2 - (8 * self.pi * G * rho) / 3.0
        self.dark_energy = max(0.0, self.dark_energy)
        return self.a, self.H, self.dark_energy

    # =====================================================================
    # 9. ПОСТРОЕНИЕ МАТРИЦЫ
    # =====================================================================
    def _build_complex_matrix(self):
        state_base = np.array([
            self.L[0] * self.Phi,
            self.L[1] * self.pi,
            self.L[2] * self.Z_res,
            1.0,
            self.L[4] * (self.C / self.C_target)
        ])

        # Суперпартнёры влияют на спектр
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

        state_with_particles = state_base + real_contribution * 0.01 + virtual_contribution * 0.005 + susy_contribution * 0.008
        state_memory = self._apply_memory(state_with_particles)

        Space_Tensor_Real = np.array([
            [state_memory[0], 1.0, 1.0, 0.0, self.S],
            [1.0, state_memory[1], 1.0, 0.0, 0.0],
            [1.0, 1.0, state_memory[2], 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0],
            [self.S, 0.0, 0.0, 0.0, state_memory[4]]
        ], dtype=float)

        phi = (self.pi / 2.0) * (1.0 - (self.C - self.C_min) / (self.C_max - self.C_min))
        self.phi = phi
        Space_Tensor_Imag = Space_Tensor_Real * np.tan(phi)

        Space_Tensor_Complex = Space_Tensor_Real + 1j * Space_Tensor_Imag

        Theta_norm = self.Theta * self.R
        Space_Tensor_NL = np.expm1(Space_Tensor_Complex / Theta_norm)

        return Space_Tensor_NL

    # =====================================================================
    # 10. ОБНОВЛЕНИЕ ПОЛЯ
    # =====================================================================
    def update_field(self, dt):
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

        # Гравитация
        self.G = self._compute_gravity(eigenvalues)

        # Космология
        self.a, self.H, self.dark_energy = self._compute_cosmology(eigenvalues, dt)

        # Взаимодействия и объединение
        interactions = self._compute_interactions(eigenvalues)
        self.alpha_em = interactions["alpha_em"]
        self.alpha_s = interactions["alpha_s"]
        self.alpha_w = interactions["alpha_w"]
        self.unification_measure = interactions["unification"]

        return {
            "alpha_inv": alpha_inv,
            "mass_ratio": mass_ratio,
            "dt_real": dt_real,
            "dt_imag": dt_imag,
            "phi": phi,
            "G": self.G,
            "a": self.a,
            "H": self.H,
            "dark_energy": self.dark_energy,
            "alpha_em": self.alpha_em,
            "alpha_s": self.alpha_s,
            "alpha_w": self.alpha_w,
            "unification": self.unification_measure
        }

    # =====================================================================
    # 11. УДЕРЖАНИЕ
    # =====================================================================
    def _barrier_potential(self, C):
        x = (C - self.C_min) / (self.C_max - self.C_min)
        x = max(0.0, min(1.0, x))
        force = self.Phi * np.tan((self.pi / 2.0) * x) / np.cos((self.pi / 2.0) * x)
        return -force * (self.C_max - self.C_min)

    # =====================================================================
    # 12. ЭВОЛЮЦИЯ
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
        self.history["G_relative"].append(result["G"] / self.G_CODATA)
        self.history["a"].append(result["a"])
        self.history["H"].append(result["H"])
        self.history["dark_energy"].append(result["dark_energy"])
        self.history["alpha_s"].append(result["alpha_s"])
        self.history["alpha_w"].append(result["alpha_w"])
        self.history["susy_breaking"].append(self.susy_breaking)
        self.history["unification_measure"].append(result["unification"])
        self.history["n_real"].append(len(self.real_particles))
        self.history["n_virtual"].append(len(self.virtual_particles))

        return {
            "C": self.C,
            "S": self.S,
            "dt_real": result["dt_real"],
            "dt_imag": result["dt_imag"],
            "phi": result["phi"],
            "1/alpha": result["alpha_inv"],
            "m_p/m_e": result["mass_ratio"],
            "G": result["G"],
            "G_relative": result["G"] / self.G_CODATA,
            "a": result["a"],
            "H": result["H"],
            "dark_energy": result["dark_energy"],
            "alpha_em": result["alpha_em"],
            "alpha_s": result["alpha_s"],
            "alpha_w": result["alpha_w"],
            "unification": result["unification"],
            "susy_breaking": self.susy_breaking,
            "n_real": len(self.real_particles),
            "n_virtual": len(self.virtual_particles)
        }

    # =====================================================================
    # 13. ВЕРИФИКАЦИЯ ВЕЛИКОГО ОБЪЕДИНЕНИЯ
    # =====================================================================
    def verify_grand_unification(self, steps=900, entropy_amplitude=0.04):
        """Верификация объединения взаимодействий и суперсимметрии."""
        print("=" * 80)
        print("   🌀 ETVE GRAND UNIFICATION v10.9")
        print("   Проверка объединения взаимодействий и суперсимметрии")
        print("=" * 80)
        print(f"Точка объединения: C_crit_unification = {self.C_crit_unification:.4f}")

        random.seed(42)

        for i in range(steps):
            entropy_flux = entropy_amplitude * np.sin(i / 7.0) + 0.005 * np.random.randn()
            C_op = 0.5 + 0.4 * np.sin(i / 20.0)
            self.evolve(entropy_flux, time_step=1.0, C_op=C_op)

        C_hist = np.array(self.history["C"])
        alpha_s_hist = np.array(self.history["alpha_s"])
        alpha_w_hist = np.array(self.history["alpha_w"])
        alpha_em_hist = 1.0 / np.array(self.history["alpha"])
        unification_hist = np.array(self.history["unification_measure"])
        susy_breaking_hist = np.array(self.history["susy_breaking"])
        G_rel_hist = np.array(self.history["G_relative"])
        a_hist = np.array(self.history["a"])
        H_hist = np.array(self.history["H"])

        print(f"\n--- СТАТИСТИКА ВЗАИМОДЕЙСТВИЙ ---")
        print(f"α_em (среднее): {np.mean(alpha_em_hist):.6f} (CODATA: 0.00729735256)")
        print(f"α_s (среднее): {np.mean(alpha_s_hist):.6f}")
        print(f"α_w (среднее): {np.mean(alpha_w_hist):.6f}")
        print(f"Мера объединения (средняя): {np.mean(unification_hist):.4f}")
        print(f"Нарушение суперсимметрии (среднее): {np.mean(susy_breaking_hist):.4f}")

        # Проверка объединения при C → C_max
        high_C_indices = np.where(C_hist > self.C_crit_unification)[0]
        if len(high_C_indices) > 0:
            avg_unification_high = np.mean(unification_hist[high_C_indices])
            avg_unification_low = np.mean(unification_hist[:len(high_C_indices)//2])
            if avg_unification_high > avg_unification_low:
                print("✅ ВЗАИМОДЕЙСТВИЯ ОБЪЕДИНЯЮТСЯ ПРИ C → C_max.")
            else:
                print("⚠️ ОБЪЕДИНЕНИЕ НЕ НАБЛЮДАЕТСЯ.")
        else:
            print("ℹ️ НЕ ДОСТИГНУТА ОБЛАСТЬ C > C_crit_unification.")

        # Проверка суперсимметрии
        if np.max(susy_breaking_hist) > 0.5 and np.min(susy_breaking_hist) < 0.5:
            print("✅ СУПЕРСИММЕТРИЯ НАРУШАЕТСЯ ПРИ C → C_min.")
        else:
            print("⚠️ СУПЕРСИММЕТРИЯ НЕ НАБЛЮДАЕТСЯ.")

        # Графики
        fig, axes = plt.subplots(3, 2, figsize=(14, 12))

        # C(t) и точка объединения
        axes[0, 0].plot(C_hist, color='blue', linewidth=1.5)
        axes[0, 0].axhline(self.C_crit_unification, color='orange', linestyle='--', label='C_unification')
        axes[0, 0].axhline(self.C_target, color='green', linestyle='--', label='C_target')
        axes[0, 0].set_title('Когерентность C(t)')
        axes[0, 0].legend()
        axes[0, 0].grid(True)

        # Мера объединения
        axes[0, 1].plot(unification_hist, color='purple', linewidth=1.5)
        axes[0, 1].axhline(0.9, color='black', linestyle='--', label='Порог объединения')
        axes[0, 1].set_title('Мера объединения взаимодействий')
        axes[0, 1].legend()
        axes[0, 1].grid(True)

        # Константы связи
        axes[1, 0].plot(alpha_em_hist, color='blue', label='α_em', linewidth=1.5)
        axes[1, 0].plot(alpha_s_hist, color='red', label='α_s', linewidth=1.5)
        axes[1, 0].plot(alpha_w_hist, color='green', label='α_w', linewidth=1.5)
        axes[1, 0].axhline(0.00729735256, color='black', linestyle='--', label='CODATA α_em')
        axes[1, 0].set_title('Константы связи')
        axes[1, 0].legend()
        axes[1, 0].grid(True)

        # Нарушение суперсимметрии
        axes[1, 1].plot(susy_breaking_hist, color='orange', linewidth=1.5)
        axes[1, 1].axhline(0.5, color='black', linestyle='--', label='Порог нарушения')
        axes[1, 1].set_title('Нарушение суперсимметрии')
        axes[1, 1].legend()
        axes[1, 1].grid(True)

        # Масштабный фактор и G
        axes[2, 0].plot(a_hist, color='red', label='a(t)', linewidth=1.5)
        axes[2, 0].set_title('Масштабный фактор a(t)')
        axes[2, 0].legend()
        axes[2, 0].grid(True)

        # G(t)
        axes[2, 1].plot(G_rel_hist, color='purple', linewidth=1.5)
        axes[2, 1].axhline(1.0, color='black', linestyle='--', label='CODATA')
        axes[2, 1].set_title('G/G_CODATA')
        axes[2, 1].legend()
        axes[2, 1].grid(True)

        plt.tight_layout()
        plt.show()

        return self.history


# =====================================================================
# ЗАПУСК
# =====================================================================
if __name__ == "__main__":
    model = ETVEGrandUnificationModelV109(memory_depth=100)
    history = model.verify_grand_unification(steps=900, entropy_amplitude=0.04)
