# =============================================================================
# 🌀 ETVE PURE GEOMETRIC MODEL v10.4
# ВЗАИМОДЕЙСТВИЕ СОЛИТОНОВ — СТОЛКНОВЕНИЯ, РАССЕЯНИЕ, РОЖДЕНИЕ ПАР
# =============================================================================
# НОВОЕ В v10.4:
# 1. Введены типы солитонов: +1 (частица) и -1 (античастица).
# 2. При столкновении частицы и античастицы — аннигиляция с излучением.
# 3. При столкновении одинаковых частиц — рассеяние с обменом фазой.
# 4. При высокой энергии — рождение пар (частица + античастица).
# 5. Взаимодействие управляется спектром поля (без внешних правил).
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma
from collections import deque
import random

class ETVEInteractionModelV104:
    """
    🌀 ЕДИНАЯ ТЕОРИЯ ВИХРЕВОГО ПОЛЯ — v10.4
    Взаимодействие солитонов: столкновения, рассеяние, рождение пар.
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
        self.C_crit_pair = self.C_min + (self.C_max - self.C_min) * 0.25  # рождение пар

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

        # --- СОЛИТОНЫ (теперь с типом) ---
        self.solitons = []  # [{"type": +1/-1, "mass": ..., "charge": ..., "phase": ...}]
        self.soliton_history = []
        self.interaction_log = []

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
            "interactions": []
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
    # 3. ВЗАИМОДЕЙСТВИЕ СОЛИТОНОВ
    # =====================================================================
    def _interact_solitons(self):
        """Обрабатывает взаимодействия между солитонами."""
        if len(self.solitons) < 2:
            return

        # Случайно выбираем пару для взаимодействия
        idx1 = random.randint(0, len(self.solitons) - 1)
        idx2 = random.randint(0, len(self.solitons) - 1)
        if idx1 == idx2:
            return

        s1 = self.solitons[idx1]
        s2 = self.solitons[idx2]

        # Типы взаимодействий
        if s1["type"] == 1 and s2["type"] == -1:
            # Частица + Античастица → Аннигиляция
            self._annihilate_pair(idx1, idx2)
        elif s1["type"] == s2["type"]:
            # Одинаковые частицы → Рассеяние с обменом фазой
            self._scatter_pair(idx1, idx2)
        else:
            # Разные типы (уже обработано выше)
            pass

    def _annihilate_pair(self, idx1, idx2):
        """Аннигиляция частицы и античастицы."""
        s1 = self.solitons[idx1]
        s2 = self.solitons[idx2]

        # Излучение (энергия переходит в поле)
        energy_released = s1["mass"] + s2["mass"]
        self.C = min(self.C + energy_released * 0.001, self.C_max)

        # Удаляем оба солитона
        self.solitons.pop(max(idx1, idx2))
        self.solitons.pop(min(idx1, idx2))

        self.interaction_log.append({
            "type": "annihilation",
            "energy": energy_released,
            "time": len(self.history["C"])
        })
        print(f"💥 АННИГИЛЯЦИЯ: энергия = {energy_released:.4e}")

        # Возможно рождение пары при высокой энергии
        if energy_released > 0.5 and random.random() < 0.3:
            self._create_pair()

    def _scatter_pair(self, idx1, idx2):
        """Рассеяние одинаковых частиц с обменом фазой."""
        s1 = self.solitons[idx1]
        s2 = self.solitons[idx2]

        # Обмен фазами
        s1["phase"], s2["phase"] = s2["phase"], s1["phase"]

        # Обмен импульсами (упрощённо)
        momentum_exchange = random.uniform(0.8, 1.2)
        s1["mass"], s2["mass"] = s2["mass"] * momentum_exchange, s1["mass"] / momentum_exchange

        self.interaction_log.append({
            "type": "scattering",
            "time": len(self.history["C"])
        })
        print(f"🔄 РАССЕЯНИЕ: обмен фазой и импульсом")

    def _create_pair(self):
        """Рождение пары частица + античастица."""
        if len(self.solitons) > 10:  # ограничение
            return

        mass = self.mass_ratio * self.m_e / self.MeV_invariant * random.uniform(0.5, 1.5)
        charge = self.alpha_inv / 137.0 * random.uniform(0.8, 1.2)
        phase = self.phi

        # Частица
        self.solitons.append({
            "type": 1,
            "mass": mass,
            "charge": charge,
            "phase": phase,
            "birth_C": self.C,
            "birth_time": len(self.history["C"]),
            "alive": True
        })

        # Античастица
        self.solitons.append({
            "type": -1,
            "mass": mass * 0.9,
            "charge": -charge,
            "phase": -phase,
            "birth_C": self.C,
            "birth_time": len(self.history["C"]),
            "alive": True
        })

        self.interaction_log.append({
            "type": "pair_creation",
            "time": len(self.history["C"])
        })
        print(f"✨ РОЖДЕНИЕ ПАРЫ: масса = {mass:.4e}")

    # =====================================================================
    # 4. ОБНОВЛЕНИЕ СОЛИТОНОВ
    # =====================================================================
    def _update_solitons(self):
        """Обновляет ансамбль солитонов и обрабатывает взаимодействия."""
        # Рождение одиночного солитона
        if self.C > self.C_crit_birth and len(self.solitons) == 0:
            mass = self.mass_ratio * self.m_e / self.MeV_invariant
            charge = self.alpha_inv / 137.0
            phase = self.phi

            self.solitons.append({
                "type": 1,
                "mass": mass,
                "charge": charge,
                "phase": phase,
                "birth_C": self.C,
                "birth_time": len(self.history["C"]),
                "alive": True
            })
            print(f"🎯 СОЛИТОН РОЖДЁН: C={self.C:.4f}")

        # Рождение пары при высокой когерентности
        if self.C > self.C_crit_pair and len(self.solitons) < 8:
            if random.random() < 0.1:
                self._create_pair()

        # Аннигиляция при низкой когерентности
        if self.C < self.C_crit_death and len(self.solitons) > 0:
            # Аннигилируем все солитоны
            for soliton in self.solitons:
                soliton["alive"] = False
            self.solitons = []
            print(f"💥 ВСЕ СОЛИТОНЫ АННИГИЛИРОВАНЫ: C={self.C:.4f}")

        # Взаимодействие между солитонами
        if len(self.solitons) >= 2 and random.random() < 0.05:
            self._interact_solitons()

        # Обновляем историю
        self.history["n_solitons"].append(len(self.solitons))
        self.history["n_particles"].append(sum(1 for s in self.solitons if s["type"] == 1))
        self.history["n_antiparticles"].append(sum(1 for s in self.solitons if s["type"] == -1))
        self.history["interactions"].append(len(self.interaction_log))

    # =====================================================================
    # 5. ПОСТРОЕНИЕ МАТРИЦЫ
    # =====================================================================
    def _build_complex_matrix(self):
        state_base = np.array([
            self.L[0] * self.Phi,
            self.L[1] * self.pi,
            self.L[2] * self.Z_res,
            1.0,
            self.L[4] * (self.C / self.C_target)
        ])

        # Вклад солитонов
        soliton_contribution = np.zeros(5)
        for soliton in self.solitons:
            if soliton["alive"]:
                # Солитон вносит добавку в спектр
                soliton_contribution += np.array([
                    soliton["mass"] * 1e6 * (1 + 0.1 * soliton["type"]),
                    soliton["charge"],
                    soliton["phase"] * soliton["type"],
                    0.0,
                    soliton["mass"] * 1e3
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
    # 6. ОБНОВЛЕНИЕ ПОЛЯ
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
            "n_antiparticles": sum(1 for s in self.solitons if s["type"] == -1)
        }

    # =====================================================================
    # 9. ВЕРИФИКАЦИЯ
    # =====================================================================
    def verify_interactions(self, steps=500, entropy_amplitude=0.04):
        print("=" * 80)
        print("   🌀 ETVE INTERACTION VERIFICATION v10.4")
        print("   Проверка взаимодействия солитонов")
        print("=" * 80)
        print(f"Рождение: C > {self.C_crit_birth:.4f}")
        print(f"Рождение пар: C > {self.C_crit_pair:.4f}")
        print(f"Аннигиляция: C < {self.C_crit_death:.4f}")

        random.seed(42)

        for i in range(steps):
            entropy_flux = entropy_amplitude * np.sin(i / 7.0) + 0.005 * np.random.randn()
            self.evolve(entropy_flux, time_step=1.0)

        C_hist = np.array(self.history["C"])
        n_solitons = np.array(self.history["n_solitons"])
        n_particles = np.array(self.history["n_particles"])
        n_antiparticles = np.array(self.history["n_antiparticles"])
        dt_real_hist = np.array(self.history["dt_real"])
        dt_imag_hist = np.array(self.history["dt_imag"])
        alpha_hist = np.array(self.history["alpha"])
        mass_hist = np.array(self.history["mass_ratio"])

        print(f"\n--- СТАТИСТИКА ВЗАИМОДЕЙСТВИЙ ---")
        print(f"Всего взаимодействий: {len(self.interaction_log)}")
        annihilations = sum(1 for e in self.interaction_log if e["type"] == "annihilation")
        scatterings = sum(1 for e in self.interaction_log if e["type"] == "scattering")
        pairs = sum(1 for e in self.interaction_log if e["type"] == "pair_creation")
        print(f"Аннигиляций: {annihilations}")
        print(f"Рассеяний: {scatterings}")
        print(f"Рождений пар: {pairs}")
        print(f"Максимальное число солитонов: {np.max(n_solitons)}")
        print(f"Среднее число солитонов: {np.mean(n_solitons):.2f}")

        if len(self.interaction_log) > 0:
            print("\n✅ ВЗАИМОДЕЙСТВИЯ ОБНАРУЖЕНЫ.")
        else:
            print("\n⚠️ ВЗАИМОДЕЙСТВИЙ НЕ ОБНАРУЖЕНО.")

        # Графики
        fig, axes = plt.subplots(3, 2, figsize=(14, 12))

        axes[0, 0].plot(C_hist, color='blue', linewidth=1.5)
        axes[0, 0].axhline(self.C_target, color='green', linestyle='--', label='C_target')
        axes[0, 0].axhline(self.C_crit_birth, color='orange', linestyle='--', label='C_birth')
        axes[0, 0].axhline(self.C_crit_death, color='red', linestyle='--', label='C_death')
        axes[0, 0].axhline(self.C_crit_pair, color='purple', linestyle='--', label='C_pair')
        axes[0, 0].set_title('Когерентность C(t)')
        axes[0, 0].legend()
        axes[0, 0].grid(True)

        axes[0, 1].plot(n_solitons, color='purple', label='Все', linewidth=1.5)
        axes[0, 1].plot(n_particles, color='blue', label='Частицы', linewidth=1.5)
        axes[0, 1].plot(n_antiparticles, color='red', label='Античастицы', linewidth=1.5)
        axes[0, 1].set_title('Число солитонов n(t)')
        axes[0, 1].legend()
        axes[0, 1].grid(True)

        axes[1, 0].plot(dt_real_hist, color='red', label='Re(dt)', linewidth=1.5)
        axes[1, 0].plot(dt_imag_hist, color='purple', label='Im(dt)', linewidth=1.5)
        axes[1, 0].set_title('Комплексное время')
        axes[1, 0].legend()
        axes[1, 0].grid(True)

        axes[1, 1].scatter(C_hist, n_solitons, s=2, c='purple', alpha=0.5)
        axes[1, 1].axhline(0, color='black', linestyle='--', linewidth=0.5)
        axes[1, 1].set_title('n(C) — фазовая диаграмма')
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
    model = ETVEInteractionModelV104(memory_depth=100)
    history = model.verify_interactions(steps=500, entropy_amplitude=0.04)
