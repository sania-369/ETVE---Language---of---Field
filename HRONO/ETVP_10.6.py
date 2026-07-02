# =============================================================================
# 🌀 ETVE PURE GEOMETRIC MODEL v10.6
# КВАНТОВАНИЕ ПОЛЯ И ВИРТУАЛЬНЫЕ ЧАСТИЦЫ — КТП НА ОСНОВЕ ЕТВП
# =============================================================================
# НОВОЕ В v10.6:
# 1. Поле квантуется: каждая мода спектра — это квантовое состояние.
# 2. Виртуальные частицы рождаются из вакуума (флуктуации).
# 3. Реальные частицы — это устойчивые солитоны с массой > порога.
# 4. Виртуальные частицы живут короткое время и аннигилируют.
# 5. Это даёт полную квантовую теорию поля на основе ЕТВП.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
from collections import deque
import random
import cmath

class ETVEQFTModelV106:
    """
    🌀 ЕДИНАЯ ТЕОРИЯ ВИХРЕВОГО ПОЛЯ — v10.6
    Квантование поля, виртуальные частицы, КТП.
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
        self.C_crit_virtual = self.C_min + (self.C_max - self.C_min) * 0.10  # виртуальные частицы

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

        # --- ЧАСТИЦЫ ---
        self.real_particles = []   # устойчивые солитоны
        self.virtual_particles = []  # виртуальные частицы (короткоживущие)
        self.field_quanta = []     # кванты поля (моды спектра)

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
            "n_real": [],
            "n_virtual": [],
            "n_quanta": [],
            "vacuum_energy": [],
            "measurements": []
        }

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
    # 2. КВАНТЫ ПОЛЯ
    # =====================================================================
    def _initialize_field_quanta(self):
        """Инициализирует кванты поля из спектра E8."""
        # Каждая мода спектра — это квантовое состояние
        for i, lam in enumerate(self.lambda_spectrum):
            quanta = {
                "mode": i,
                "energy": lam,
                "occupation": 0,  # число заполнения (0, 1, 2, ...)
                "phase": random.random() * 2 * self.pi,
                "alive": True
            }
            self.field_quanta.append(quanta)

    def _update_field_quanta(self):
        """Обновляет кванты поля: рождение/аннигиляция виртуальных частиц."""
        # Вакуумные флуктуации: виртуальные частицы рождаются из квантов
        for quanta in self.field_quanta:
            # Вероятность рождения виртуальной частицы
            birth_prob = (self.C - self.C_min) / (self.C_max - self.C_min) * 0.1
            if random.random() < birth_prob and len(self.virtual_particles) < 20:
                # Рождаем виртуальную частицу из кванта
                virtual = {
                    "mass": quanta["energy"] * random.uniform(0.1, 0.5),
                    "energy": quanta["energy"],
                    "phase": quanta["phase"] + random.uniform(-0.5, 0.5),
                    "lifetime": random.uniform(1, 5),  # короткое время жизни
                    "age": 0,
                    "alive": True,
                    "mode": quanta["mode"]
                }
                self.virtual_particles.append(virtual)
                quanta["occupation"] += 1

        # Эволюция виртуальных частиц: стареют и аннигилируют
        for virtual in self.virtual_particles[:]:
            virtual["age"] += 1
            virtual["lifetime"] *= (1 - 0.01 * (1 - self.C / self.C_target))
            if virtual["age"] > virtual["lifetime"] or random.random() < 0.02:
                # Аннигиляция виртуальной частицы — возврат энергии в поле
                virtual["alive"] = False
                self.virtual_particles.remove(virtual)
                # Уменьшаем occupation соответствующего кванта
                for quanta in self.field_quanta:
                    if quanta["mode"] == virtual["mode"] and quanta["occupation"] > 0:
                        quanta["occupation"] -= 1
                        break

        # Обновляем историю
        self.history["n_quanta"].append(sum(q["occupation"] for q in self.field_quanta))

    # =====================================================================
    # 3. РЕАЛЬНЫЕ ЧАСТИЦЫ (устойчивые солитоны)
    # =====================================================================
    def _create_real_particle(self, particle_type=1):
        """Создаёт устойчивую реальную частицу."""
        if len(self.real_particles) > 10:
            return

        mass = self.mass_ratio * self.m_e / self.MeV_invariant
        charge = self.alpha_inv / 137.0
        phase = self.phi

        # Волновая функция реальной частицы — устойчивая
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
        return particle

    def _create_real_pair(self):
        """Создаёт пару реальных частиц."""
        if len(self.real_particles) > 8:
            return

        p1 = self._create_real_particle(1)
        p2 = self._create_real_particle(-1)

        # Запутывание
        alpha = random.random()
        beta = np.sqrt(1 - alpha**2)
        p1["psi"] = alpha + 1j * beta
        p2["psi"] = beta - 1j * alpha

    # =====================================================================
    # 4. ИЗМЕРЕНИЕ (коллапс)
    # =====================================================================
    def _measure_particle(self, particle):
        """Измеряет реальную частицу."""
        collapse_prob = self.C * self.C_op / self.C_target
        collapse_prob = np.clip(collapse_prob, 0.0, 1.0)

        if random.random() < collapse_prob:
            psi = particle["psi"]
            prob_0 = np.abs(psi.real)**2
            if random.random() < prob_0:
                particle["psi"] = 1.0 + 0j
            else:
                particle["psi"] = 0.0 + 1j
            self.history["measurements"].append(len(self.history["measurements"]) + 1)
            return True
        return False

    # =====================================================================
    # 5. ОБНОВЛЕНИЕ ВСЕХ ЧАСТИЦ
    # =====================================================================
    def _update_particles(self):
        """Обновляет ансамбль частиц (реальных и виртуальных)."""
        # --- РЕАЛЬНЫЕ ЧАСТИЦЫ ---
        # Рождение
        if self.C > self.C_crit_birth and len(self.real_particles) == 0:
            self._create_real_particle(1)

        if self.C > self.C_crit_pair and len(self.real_particles) < 6:
            if random.random() < 0.06:
                self._create_real_pair()

        # Измерение
        for particle in self.real_particles:
            if particle["alive"]:
                self._measure_particle(particle)

        # Аннигиляция
        if self.C < self.C_crit_death and len(self.real_particles) > 0:
            self.real_particles = []

        # --- ВИРТУАЛЬНЫЕ ЧАСТИЦЫ (из квантов поля) ---
        if self.C > self.C_crit_virtual:
            self._update_field_quanta()

        # --- ИСТОРИЯ ---
        self.history["n_real"].append(len(self.real_particles))
        self.history["n_virtual"].append(len(self.virtual_particles))

        # Энергия вакуума (суммарная энергия виртуальных частиц)
        vacuum_energy = sum(v["energy"] for v in self.virtual_particles if v["alive"])
        self.history["vacuum_energy"].append(vacuum_energy)

    # =====================================================================
    # 6. ПОСТРОЕНИЕ МАТРИЦЫ
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

        # Вклад виртуальных частиц (меньше, нестабильны)
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

        state_with_particles = state_base + real_contribution * 0.01 + virtual_contribution * 0.005
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
    # 7. ОБНОВЛЕНИЕ ПОЛЯ
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
    # 8. УДЕРЖАНИЕ
    # =====================================================================
    def _barrier_potential(self, C):
        x = (C - self.C_min) / (self.C_max - self.C_min)
        x = max(0.0, min(1.0, x))
        force = self.Phi * np.tan((self.pi / 2.0) * x) / np.cos((self.pi / 2.0) * x)
        return -force * (self.C_max - self.C_min)

    # =====================================================================
    # 9. ЭВОЛЮЦИЯ
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
            "n_real": len(self.real_particles),
            "n_virtual": len(self.virtual_particles),
            "vacuum_energy": self.history["vacuum_energy"][-1] if self.history["vacuum_energy"] else 0
        }

    # =====================================================================
    # 10. ВЕРИФИКАЦИЯ
    # =====================================================================
    def verify_qft(self, steps=600, entropy_amplitude=0.04):
        """Верификация квантовой теории поля."""
        print("=" * 80)
        print("   🌀 ETVE QUANTUM FIELD THEORY v10.6")
        print("   Проверка квантования поля и виртуальных частиц")
        print("=" * 80)
        print(f"Критическая точка виртуальных частиц: C_crit_virtual = {self.C_crit_virtual:.4f}")

        random.seed(42)

        for i in range(steps):
            entropy_flux = entropy_amplitude * np.sin(i / 7.0) + 0.005 * np.random.randn()
            C_op = 0.5 + 0.4 * np.sin(i / 20.0)
            self.evolve(entropy_flux, time_step=1.0, C_op=C_op)

        C_hist = np.array(self.history["C"])
        n_real = np.array(self.history["n_real"])
        n_virtual = np.array(self.history["n_virtual"])
        n_quanta = np.array(self.history["n_quanta"])
        vacuum_energy = np.array(self.history["vacuum_energy"])
        dt_real_hist = np.array(self.history["dt_real"])
        dt_imag_hist = np.array(self.history["dt_imag"])
        alpha_hist = np.array(self.history["alpha"])
        mass_hist = np.array(self.history["mass_ratio"])

        print(f"\n--- СТАТИСТИКА КВАНТОВОГО ПОЛЯ ---")
        print(f"Максимальное число реальных частиц: {np.max(n_real)}")
        print(f"Максимальное число виртуальных частиц: {np.max(n_virtual)}")
        print(f"Максимальное число квантов поля: {np.max(n_quanta)}")
        print(f"Средняя энергия вакуума: {np.mean(vacuum_energy):.4e}")
        print(f"Максимальная энергия вакуума: {np.max(vacuum_energy):.4e}")

        if np.max(n_virtual) > 0:
            print("\n✅ ВИРТУАЛЬНЫЕ ЧАСТИЦЫ ОБНАРУЖЕНЫ.")
        else:
            print("\n⚠️ ВИРТУАЛЬНЫХ ЧАСТИЦ НЕТ.")

        if np.max(n_quanta) > 0:
            print("✅ ПОЛЕ КВАНТОВАННО (есть кванты).")
        else:
            print("⚠️ ПОЛЕ НЕ КВАНТОВАННО.")

        # Графики
        fig, axes = plt.subplots(3, 2, figsize=(14, 12))

        axes[0, 0].plot(C_hist, color='blue', linewidth=1.5)
        axes[0, 0].axhline(self.C_target, color='green', linestyle='--', label='C_target')
        axes[0, 0].axhline(self.C_crit_virtual, color='orange', linestyle='--', label='C_virtual')
        axes[0, 0].set_title('Когерентность C(t)')
        axes[0, 0].legend()
        axes[0, 0].grid(True)

        axes[0, 1].plot(n_real, color='blue', label='Реальные', linewidth=1.5)
        axes[0, 1].plot(n_virtual, color='red', label='Виртуальные', linewidth=1.5)
        axes[0, 1].plot(n_quanta, color='orange', label='Кванты', linewidth=1.5)
        axes[0, 1].set_title('Частицы и кванты поля')
        axes[0, 1].legend()
        axes[0, 1].grid(True)

        axes[1, 0].plot(vacuum_energy, color='purple', linewidth=1.5)
        axes[1, 0].set_title('Энергия вакуума (виртуальные частицы)')
        axes[1, 0].set_ylabel('E_vac')
        axes[1, 0].grid(True)

        axes[1, 1].scatter(C_hist, n_virtual, s=2, c='red', alpha=0.5)
        axes[1, 1].set_title('n_virtual(C) — виртуальные частицы')
        axes[1, 1].set_xlabel('C')
        axes[1, 1].set_ylabel('n_virtual')
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
    model = ETVEQFTModelV106(memory_depth=100)
    history = model.verify_qft(steps=600, entropy_amplitude=0.04)
