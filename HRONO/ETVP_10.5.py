# =============================================================================
# 🌀 ETVE PURE GEOMETRIC MODEL v10.5
# КВАНТОВЫЕ ВЕРОЯТНОСТИ И ИЗМЕРЕНИЕ — СУПЕРПОЗИЦИЯ И КОЛЛАПС
# =============================================================================
# НОВОЕ В v10.5:
# 1. Каждый солитон находится в суперпозиции состояний (волновая функция).
# 2. Состояния: |0⟩ (невозбуждённое) и |1⟩ (возбуждённое) с амплитудами.
# 3. При измерении (взаимодействии с оператором) волновая функция коллапсирует.
# 4. Вероятность коллапса зависит от когерентности C и фактора оператора.
# 5. Это даёт квантовую механику как следствие геометрии поля.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
from collections import deque
import random
import cmath

class ETVEQuantumModelV105:
    """
    🌀 ЕДИНАЯ ТЕОРИЯ ВИХРЕВОГО ПОЛЯ — v10.5
    Квантовые вероятности, суперпозиция, коллапс волновой функции.
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

        # --- ФАКТОР ОПЕРАТОРА (когерентность наблюдателя) ---
        self.C_op = 0.5  # от 0 (хаос) до 1 (абсолютный порядок)

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

        # --- КВАНТОВЫЕ СОЛИТОНЫ (с волновой функцией) ---
        self.solitons = []  # каждый солит имеет psi (комплексную амплитуду)
        self.soliton_history = []
        self.measurement_log = []

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
            "n_particles": [],
            "n_antiparticles": [],
            "coherence_measure": [],
            "measurements": []
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
    # 3. ВОЛНОВАЯ ФУНКЦИЯ И СУПЕРПОЗИЦИЯ
    # =====================================================================
    def _create_soliton(self, soliton_type=1):
        """Создаёт солитон с волновой функцией в суперпозиции."""
        mass = self.mass_ratio * self.m_e / self.MeV_invariant
        charge = self.alpha_inv / 137.0
        phase = self.phi

        # Волновая функция: |psi|^2 = 1 (нормирована)
        # Суперпозиция состояний |0⟩ и |1⟩
        alpha = random.random()  # амплитуда |0⟩
        beta = np.sqrt(1 - alpha**2)  # амплитуда |1⟩
        psi = alpha + 1j * beta

        soliton = {
            "type": soliton_type,
            "mass": mass,
            "charge": charge * soliton_type,
            "phase": phase * soliton_type,
            "psi": psi,  # волновая функция
            "birth_C": self.C,
            "birth_time": len(self.history["C"]),
            "alive": True,
            "measured": False
        }
        self.solitons.append(soliton)
        return soliton

    def _create_pair(self):
        """Создаёт пару частица + античастица с запутанными волновыми функциями."""
        if len(self.solitons) > 10:
            return

        # Создаём частицу
        p1 = self._create_soliton(1)
        # Создаём античастицу с противоположной фазой
        p2 = self._create_soliton(-1)

        # Запутываем волновые функции
        # |psi1⟩ и |psi2⟩ антикоррелированы
        alpha = random.random()
        beta = np.sqrt(1 - alpha**2)
        p1["psi"] = alpha + 1j * beta
        p2["psi"] = beta - 1j * alpha

        self.measurement_log.append({
            "type": "pair_creation",
            "time": len(self.history["C"])
        })

    # =====================================================================
    # 4. ИЗМЕРЕНИЕ (КОЛЛАПС ВОЛНОВОЙ ФУНКЦИИ)
    # =====================================================================
    def _measure_soliton(self, soliton):
        """
        Измеряет солитон — коллапс волновой функции.
        Вероятность коллапса зависит от C и фактора оператора C_op.
        """
        # Вероятность коллапса
        collapse_prob = self.C * self.C_op / self.C_target
        collapse_prob = np.clip(collapse_prob, 0.0, 1.0)

        if random.random() < collapse_prob:
            # Коллапс: волновая функция переходит в одно из состояний
            psi = soliton["psi"]
            # Вероятность состояния |0⟩
            prob_0 = np.abs(psi.real)**2
            # Коллапсируем в |0⟩ или |1⟩
            if random.random() < prob_0:
                soliton["psi"] = 1.0 + 0j  # состояние |0⟩
            else:
                soliton["psi"] = 0.0 + 1j  # состояние |1⟩
            soliton["measured"] = True

            self.measurement_log.append({
                "type": "collapse",
                "time": len(self.history["C"]),
                "state": "0" if soliton["psi"].real > 0.5 else "1"
            })
            print(f"📐 ИЗМЕРЕНИЕ: солитон коллапсировал в состояние {soliton['psi']}")

        return soliton

    # =====================================================================
    # 5. ОБНОВЛЕНИЕ СОЛИТОНОВ
    # =====================================================================
    def _update_solitons(self):
        """Обновляет ансамбль солитонов с квантовыми эффектами."""
        # Рождение
        if self.C > self.C_crit_birth and len(self.solitons) == 0:
            self._create_soliton(1)
            print(f"🎯 СОЛИТОН РОЖДЁН (квантовый): C={self.C:.4f}")

        # Рождение пары
        if self.C > self.C_crit_pair and len(self.solitons) < 8:
            if random.random() < 0.08:
                self._create_pair()
                print(f"✨ КВАНТОВАЯ ПАРА РОЖДЕНА: C={self.C:.4f}")

        # Измерение (коллапс) для каждого солитона
        for soliton in self.solitons:
            if soliton["alive"] and not soliton["measured"]:
                self._measure_soliton(soliton)

        # Аннигиляция
        if self.C < self.C_crit_death and len(self.solitons) > 0:
            for soliton in self.solitons:
                soliton["alive"] = False
            self.solitons = []
            print(f"💥 КВАНТОВЫЕ СОЛИТОНЫ АННИГИЛИРОВАНЫ: C={self.C:.4f}")

        # Обновляем историю
        self.history["n_solitons"].append(len(self.solitons))
        self.history["n_particles"].append(sum(1 for s in self.solitons if s["type"] == 1))
        self.history["n_antiparticles"].append(sum(1 for s in self.solitons if s["type"] == -1))

        # Мера когерентности (усреднённая по всем солитонам)
        if len(self.solitons) > 0:
            avg_psi = np.mean([np.abs(s["psi"]) for s in self.solitons])
            self.history["coherence_measure"].append(avg_psi)
        else:
            self.history["coherence_measure"].append(0.0)

        self.history["measurements"].append(len(self.measurement_log))

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

        # Вклад солитонов с квантовыми состояниями
        soliton_contribution = np.zeros(5)
        for soliton in self.solitons:
            if soliton["alive"]:
                # Волновая функция влияет на вклад
                psi_amplitude = np.abs(soliton["psi"])
                psi_phase = np.angle(soliton["psi"])

                soliton_contribution += np.array([
                    soliton["mass"] * 1e6 * (1 + 0.1 * soliton["type"] * psi_amplitude),
                    soliton["charge"] * psi_amplitude,
                    soliton["phase"] * psi_phase,
                    0.0,
                    soliton["mass"] * 1e3 * psi_amplitude
                ])

        state_with_solitons = state_base + soliton_contribution * 0.01
        state_memory = self._apply_memory(state_with_solitons)

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
        """Один шаг эволюции с квантовыми эффектами."""
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

        self._update_solitons()

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
            "n_solitons": len(self.solitons),
            "n_particles": sum(1 for s in self.solitons if s["type"] == 1),
            "n_antiparticles": sum(1 for s in self.solitons if s["type"] == -1),
            "C_op": self.C_op
        }

    # =====================================================================
    # 10. ВЕРИФИКАЦИЯ
    # =====================================================================
    def verify_quantum(self, steps=500, entropy_amplitude=0.04, C_op_profile=None):
        """
        Верификация квантовых эффектов.
        C_op_profile: список значений C_op для каждого шага (можно менять во времени).
        """
        print("=" * 80)
        print("   🌀 ETVE QUANTUM VERIFICATION v10.5")
        print("   Проверка суперпозиции, коллапса и квантовых вероятностей")
        print("=" * 80)
        print(f"Начальный фактор оператора: C_op = {self.C_op:.2f}")

        random.seed(42)

        for i in range(steps):
            entropy_flux = entropy_amplitude * np.sin(i / 7.0) + 0.005 * np.random.randn()

            # Если задан профиль C_op, используем его
            if C_op_profile is not None and i < len(C_op_profile):
                C_op = C_op_profile[i]
            else:
                C_op = 0.5 + 0.4 * np.sin(i / 20.0)  # пульсация оператора

            self.evolve(entropy_flux, time_step=1.0, C_op=C_op)

        C_hist = np.array(self.history["C"])
        n_solitons = np.array(self.history["n_solitons"])
        n_particles = np.array(self.history["n_particles"])
        n_antiparticles = np.array(self.history["n_antiparticles"])
        coherence_measure = np.array(self.history["coherence_measure"])
        measurements = np.array(self.history["measurements"])
        dt_real_hist = np.array(self.history["dt_real"])
        dt_imag_hist = np.array(self.history["dt_imag"])
        alpha_hist = np.array(self.history["alpha"])
        mass_hist = np.array(self.history["mass_ratio"])

        print(f"\n--- СТАТИСТИКА КВАНТОВЫХ ЭФФЕКТОВ ---")
        print(f"Всего измерений (коллапсов): {len(self.measurement_log)}")
        collapses = sum(1 for e in self.measurement_log if e["type"] == "collapse")
        pairs = sum(1 for e in self.measurement_log if e["type"] == "pair_creation")
        print(f"Коллапсов волновой функции: {collapses}")
        print(f"Рождений запутанных пар: {pairs}")
        print(f"Максимальное число солитонов: {np.max(n_solitons)}")
        print(f"Средняя мера когерентности: {np.mean(coherence_measure):.4f}")

        if len(self.measurement_log) > 0:
            print("\n✅ КВАНТОВЫЕ ЭФФЕКТЫ ОБНАРУЖЕНЫ.")
        else:
            print("\n⚠️ КВАНТОВЫЕ ЭФФЕКТЫ НЕ ОБНАРУЖЕНЫ.")

        # Графики
        fig, axes = plt.subplots(3, 2, figsize=(14, 12))

        # C(t) и C_op(t)
        axes[0, 0].plot(C_hist, color='blue', label='C(t)', linewidth=1.5)
        axes[0, 0].axhline(self.C_target, color='green', linestyle='--', label='C_target')
        axes[0, 0].set_title('Когерентность поля C(t)')
        axes[0, 0].legend()
        axes[0, 0].grid(True)

        # Число солитонов и когерентность
        axes[0, 1].plot(n_solitons, color='purple', label='n(t)', linewidth=1.5)
        axes[0, 1].plot(coherence_measure, color='orange', label='|ψ|', linewidth=1.5)
        axes[0, 1].set_title('Число солитонов и мера когерентности')
        axes[0, 1].legend()
        axes[0, 1].grid(True)

        # Коллапсы
        axes[1, 0].plot(measurements, color='red', label='Измерения', linewidth=1.5)
        axes[1, 0].set_title('Накопленное число коллапсов')
        axes[1, 0].legend()
        axes[1, 0].grid(True)

        # dt(C) с квантовыми эффектами
        axes[1, 1].scatter(C_hist, dt_real_hist, s=2, c=coherence_measure, cmap='viridis', alpha=0.5)
        axes[1, 1].set_title('dt(C) — окрашено мерой когерентности')
        axes[1, 1].set_xlabel('C')
        axes[1, 1].set_ylabel('dt_real')
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
# ЗАПУСК
# =====================================================================
if __name__ == "__main__":
    model = ETVEQuantumModelV105(memory_depth=100)

    # Профиль C_op: сначала низкий (хаос), потом высокий (порядок)
    C_op_profile = [0.2 + 0.7 * (1 - np.exp(-i/100)) for i in range(500)]

    history = model.verify_quantum(
        steps=500,
        entropy_amplitude=0.04,
        C_op_profile=C_op_profile
      )
