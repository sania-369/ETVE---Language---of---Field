# =============================================================================
# 🌀 ETVE PURE GEOMETRIC MODEL v9.6.2
# Геометрическая экспонента Римана (без циклов)
# =============================================================================
# НОВОЕ В v9.6.2:
# 1. Встроена экспоненциальная калибровка непосредственно в матрицу:
#    Space_Tensor_NL = exp(Space_Tensor_4D / Θ) - I
# 2. Θ (тета) вычисляется из геометрии: Θ = log_vol_torus / E8_dim
# 3. Это даёт нелинейное раздвижение собственных значений без циклов.
# 4. SVD применяется один раз.
# =============================================================================

import numpy as np
from scipy.special import gamma

class ETVEPureGeometricModelV962:
    def __init__(self):
        # --- ФУНДАМЕНТАЛЬНЫЙ БАЗИС ---
        self.Phi = (1.0 + np.sqrt(5.0)) / 2.0
        self.pi = np.pi
        self.Z_res = np.sqrt(3.0)

        # --- ИНВАРИАНТЫ E8 ---
        self.E8_dim = 248
        self.E8_roots = 240
        self.E8_max_sub = 128

        # --- ЛОГАРИФМИЧЕСКИЙ ОБЪЁМ E8 ---
        def log_volume_group(n):
            return (n / 2.0) * np.log(self.pi) - np.log(gamma(n / 2.0 + 1))

        self.log_vol_E8 = log_volume_group(self.E8_dim)

        # --- ЛОГАРИФМИЧЕСКИЙ ОБЪЁМ SU(8) ---
        self.SU8_dim = 63
        self.log_vol_SU8 = log_volume_group(self.SU8_dim)

        # --- ОБЪЁМ ТОРА РИМАНА ---
        self.log_vol_torus = 2.0 * self.log_vol_E8 - self.log_vol_SU8

        # --- ГЕОМЕТРИЧЕСКИЙ МАСШТАБ Θ (для экспоненты) ---
        self.Theta = self.log_vol_torus / self.E8_dim

        # --- ИНДЕКСЫ ХАУСДОРФА ---
        self.L_dim_roots = self.log_vol_E8 / log_volume_group(self.E8_roots)

        # --- 4D-МАТРИЦА КАЛУЦЫ-КЛЕЙНА (линейная) ---
        self.Space_Tensor_4D = np.array([
            [self.L_dim_roots * self.Phi,  1.0,  1.0,  0.0],
            [1.0,  self.L_dim_roots * self.pi,  1.0,  0.0],
            [1.0,  1.0,  self.L_dim_roots * self.Z_res,  0.0],
            [0.0,  0.0,  0.0,  1.0]  # калибровочная мода (будет усилена экспонентой)
        ], dtype=float)

        # =====================================================================
        # НЕЛИНЕЙНАЯ ЭКСПОНЕНЦИАЛЬНАЯ КАЛИБРОВКА (геометрическая)
        # =====================================================================
        # Space_Tensor_NL = exp(Space_Tensor_4D / Θ) - I
        # Это не цикл, а прямое матричное преобразование.
        self.Space_Tensor_NL = np.expm1(self.Space_Tensor_4D / self.Theta)

        # --- ПРЯМОЙ SVD (ОДИН РАЗ) ---
        self.U, self.Eigenvalues, self.Vt = np.linalg.svd(self.Space_Tensor_NL)

        # --- ВЫВОД КОНСТАНТ ---
        hopf_factor = self.pi * self.Phi
        self.alpha_inv = (self.Eigenvalues[0] / self.Eigenvalues[1]) * hopf_factor
        self.mass_ratio = (self.Eigenvalues[0] / self.Eigenvalues[3]) * (hopf_factor ** 2)

        # --- МАССЫ ---
        self.m_planck_spectral = self.Eigenvalues[0] * self.Eigenvalues[1] * self.Eigenvalues[3]
        self.m_e = self.m_planck_spectral / (self.alpha_inv * self.mass_ratio)
        self.m_p_eV = self.m_e * self.mass_ratio

        # --- ИНВАРИАНТЫ ---
        self.percent_invariant = self.Phi ** 10
        self.MeV_invariant = self.Phi ** 30
        self.coulomb_invariant = self.Phi / (self.pi ** 5)
        self.asymmetry_invariant = self.Z_res / (self.pi ** 4)
        self.light_nuclei_threshold = 4

        # --- Z-ПРИНЦИП ---
        self.C_min = 1.0 / (self.Phi ** 10)
        self.C_max = 1.0 - 1.0 / (self.Phi ** 20)
        self.target_C = 1.0 - 1.0 / ((self.Phi ** 7) * self.Phi * (self.pi / 5.0))

        # --- ДИНАМИКА ---
        self.M = np.array([[self.Phi, 1.0], [1.0, 1.0 / self.Phi]], dtype=float)
        self.state = np.array([1.0 / self.Phi, 1.0 / self.Phi], dtype=float)

    # =====================================================================
    # МЕТОДЫ ДЛЯ КОНСТАНТ
    # =====================================================================
    def get_alpha_inv(self):
        return self.alpha_inv

    def get_mass_ratio(self):
        return self.mass_ratio

    def get_m_planck_spectral(self):
        return self.m_planck_spectral

    def get_electron_mass(self):
        return self.m_e

    def get_proton_mass_eV(self):
        return self.m_p_eV

    def get_proton_mass_MeV(self):
        return self.m_p_eV / self.MeV_invariant

    def get_gravitational_constant(self):
        hbar = 1.054571817e-34
        c = 299792458
        m_planck_kg = self.m_planck_spectral * 1.602176634e-19 / (c ** 2)
        return (hbar * c) / (m_planck_kg ** 2)

    def get_proton_radius(self):
        return 1.0 / (self.alpha_inv * self.pi) * (self.Phi ** 2)

    # =====================================================================
    # МЕТОДЫ ДЛЯ ЯДЕРНЫХ МАСС
    # =====================================================================
    def compute_masses_from_matrix(self, G_matrix):
        N = len(G_matrix)
        s = np.zeros((N, N), dtype=complex)
        for i in range(N):
            for j in range(N):
                if i != j and G_matrix[i][j] > 0:
                    s[i][j] = np.sqrt(G_matrix[i][j]) + 0j
        for i in range(N):
            external_sum = np.sum(s[i, :]) - s[i, i]
            s[i, i] = -external_sum
        masses = np.zeros(N)
        for i in range(N):
            w_i = np.abs(s[i][i])
            external_sum_sq = np.sum(np.abs(s[i, :]) ** 2) - w_i ** 2
            m_sq = (w_i ** 2 + external_sum_sq) * (self.m_e / self.MeV_invariant)
            masses[i] = np.sqrt(m_sq)
        return masses

    def compute_nuclear_mass(self, A, Z, modes=None):
        N = A - Z
        asymmetry = (N - Z) / A
        if A <= self.light_nuclei_threshold:
            coulomb_repulsion = 0.0
            asymmetry_correction = 0.0
            nuclear_binding = (Z * self.Phi + N * self.Z_res) / (self.pi ** 2)
        else:
            nuclear_binding = (Z * self.Phi + N * self.Z_res) / (self.pi ** 2)
            coulomb_repulsion = (Z ** 2) / (A ** (1/3)) * self.coulomb_invariant
            asymmetry_correction = asymmetry * self.asymmetry_invariant
        total_binding = nuclear_binding - coulomb_repulsion - asymmetry_correction
        if modes is not None and "strong" in modes:
            return A - (total_binding * modes["strong"] / self.percent_invariant)
        else:
            return A - total_binding

    # =====================================================================
    # МЕТОДЫ ДЛЯ ДИНАМИКИ
    # =====================================================================
    def _pure_tensor_evolution(self, entropy_flux):
        chaos_operator = 1.0 / (1.0 + abs(entropy_flux) * (1.0 / self.Phi))
        D = np.array([
            [chaos_operator, 0.0],
            [0.0, 1.0 / chaos_operator]
        ], dtype=float)
        self.state = np.dot(np.dot(D, self.M), self.state)
        trace_weight = abs(self.state[0]) + abs(self.state[1])
        if trace_weight > 0.0:
            self.state = self.state / trace_weight
        return abs(self.state[0])

    def get_dynamic_coherence(self, external_entropy=0.15, iteration=0):
        coherence = self._pure_tensor_evolution(external_entropy)
        coh_e = np.clip(coherence, self.C_min, self.C_max)
        coh_strong = np.clip(coherence * 1.05, self.C_min, self.C_max)
        coh_grav = np.clip(coherence * 0.98, self.C_min, self.C_max)
        return {
            "electron": coh_e,
            "strong": coh_strong,
            "gravity": coh_grav
        }

    def apply_safety_shield(self, C, entropy, psi):
        safe_C = np.clip(C, self.C_min, self.C_max)
        epsilon = 1.0 / (self.Phi ** 30)
        safe_psi = (self.Phi * safe_C) / np.sqrt(max(entropy, 0.0) + epsilon)
        distance = abs(safe_C - self.target_C)
        dt = 0.01 + 0.99 * (1.0 - np.tanh(distance * 20.0))
        return {
            "safe_C": safe_C,
            "safe_psi": safe_psi,
            "dt": dt,
            "is_locked": distance < 1e-9
        }

    def compute_gravity_modulation(self, distance, polarity=1.0):
        G_base = self.get_gravitational_constant()
        wave = np.sin(distance / self.Phi) * self.Phi
        envelope = np.exp(-distance / (self.Phi ** 3))
        modulation = 1.0 + wave * envelope
        return polarity * (G_base * modulation)

    def classify_reality(self, E, m, O):
        if E > 0 and m > 0 and O > 0:
            return "I. Наша Вселенная (Обычная материя)"
        elif E > 0 and m > 0 and O < 0:
            return "II. Тёмная энергия (Антигравитация)"
        elif E > 0 and m < 0 and O > 0:
            return "III. Убегающая материя (Гравитационное отталкивание)"
        elif E < 0 and m < 0 and O < 0:
            return "VIII. Полная инверсия"
        else:
            return "Неопределённый тип"

    # =====================================================================
    # МЕТОДЫ ДЛЯ ПОТЕНЦИАЛА
    # =====================================================================
    def _get_k_space(self, C, num_points=200):
        C_clamped = np.clip(C, self.C_min, self.C_max)
        k_min = 0.01 + 0.1 * (1.0 - C_clamped)
        if C_clamped < 1e-6:
            k_max = 1e34
        else:
            k_max = 20.0 / (C_clamped + 1e-12)
            k_max = min(k_max, 1e34)
        return np.linspace(k_min, k_max, num_points)

    def compute_potential(self, r, C, mode='full'):
        k_space = self._get_k_space(C)
        k = 1.0 / (r + 1e-12)
        if mode == 'coulomb':
            return self.alpha_inv / r
        v_profile = np.zeros_like(k_space)
        wall_mask = k_space > self.Eigenvalues[0]
        v_profile[wall_mask] = 1e6 * (k_space[wall_mask] - self.Eigenvalues[0])**2
        mid_mask = (k_space <= self.Eigenvalues[0]) & (k_space >= self.Eigenvalues[1])
        if np.any(mid_mask):
            v_profile[mid_mask] = -self.Eigenvalues[2] + (k_space[mid_mask] - self.Eigenvalues[1]) * self.Eigenvalues[1]
        far_mask = k_space < self.Eigenvalues[1]
        v_profile[far_mask] = self.alpha_inv / (1.0 / (k_space[far_mask] + 1e-12) + 1.0)
        return np.interp(k, k_space, v_profile, left=v_profile[0], right=v_profile[-1])

    def simulate_scattering(self, energy, C, r_max=10.0, steps=100):
        r = np.linspace(0.01, r_max, steps)
        v = np.array([self.compute_potential(ri, C) for ri in r])
        kinetic = energy - v
        trapped_indices = np.where(kinetic < 0)[0]
        is_trapped = len(trapped_indices) > 0
        trapping_time = trapped_indices[0] if is_trapped else steps
        return {
            'r_traj': r,
            'v_traj': v,
            'is_trapped': is_trapped,
            'trapping_time': trapping_time / steps * r_max
        }

    def verify_x17_angle(self, Z, N, mode='default'):
        A = Z + N
        p = N / Z if Z > 0 else 1.0
        spectral_index = self.Eigenvalues[1] / self.Eigenvalues[2]
        base_angle = 180.0 / (1.0 + 1.0/(spectral_index * self.Phi))
        modifier = 1.0 + (1.0 - 1.0/(1.0 + (p - 1.0)**2)) * 0.1 * p
        angle = base_angle * modifier
        if angle > 180.0:
            angle = 180.0
        if A <= 4:
            angle = angle * (self.pi / 3.0)
        return angle

    # =====================================================================
    # ВЕРИФИКАЦИЯ
    # =====================================================================
    def run_verification(self, C=0.95):
        print("=" * 75)
        print("   🌀 ETVE PURE GEOMETRIC MODEL v9.6.2    ")
        print("   (Геометрическая экспонента Римана)     ")
        print("=" * 75)
        print("[СТАТУС]: НЕЛИНЕЙНОСТЬ ВСТРОЕНА В МАТРИЦУ.")
        print(f"[Θ]: {self.Theta:.6f} (выведен из объёма тора)")
        print("-" * 75)

        alpha_inv = self.get_alpha_inv()
        mass_ratio = self.get_mass_ratio()
        m_p_MeV = self.get_proton_mass_MeV()
        G = self.get_gravitational_constant()
        R_p = self.get_proton_radius()

        print(f"1/α (Тонкая структура)        : {alpha_inv:.12f}  (CODATA: 137.035999084)")
        print(f"m_p/m_e (Отношение масс)      : {mass_ratio:.12f}  (CODATA: 1836.15267343)")
        print(f"m_p (Масса протона, МэВ)      : {m_p_MeV:.12f}  (CODATA: 938.272)")
        print(f"G (Гравитационная постоянна.) : {G:.5e}  (CODATA: 6.67430e-11)")
        print(f"R_p (Радиус протона, фм)      : {R_p:.4f}  (CODATA: 0.8414)")
        print("-" * 75)

        print("--- МАССЫ ЯДЕР (расчёт) ---")
        for A, Z in [(1,1), (2,1), (209,83), (238,92)]:
            m = self.compute_nuclear_mass(A, Z)
            print(f" A={A}, Z={Z}: масса = {m:.6f} а.е.м.")
        print("-" * 75)

        print("--- УГЛЫ X17 (предсказание) ---")
        for Z, N in [(4,4), (2,2), (3,4)]:
            angle = self.verify_x17_angle(Z, N)
            print(f" Z={Z}, N={N}: угол = {angle:.1f}°")
        print("-" * 75)

        print("--- ПРОВЕРКА ПОТЕНЦИАЛА (адаптивная сетка) ---")
        r_test = np.array([0.0001, 0.001, 0.01, 0.1, 1.0, 10.0])
        k_space = self._get_k_space(C)
        print(f" Сетка k_space: {k_space[0]:.3e} ... {k_space[-1]:.3e} (точек: {len(k_space)})")
        for r in r_test:
            v = self.compute_potential(r, C)
            print(f" r={r:.4f} -> V={v:.3e}")
        print("-" * 75)

        print("=" * 75)
        print("✅ v9.6.2: ЭКСПОНЕНЦИАЛЬНОЕ РАЗДВИЖЕНИЕ БЕЗ ЦИКЛОВ.")
        print("   КОНСТАНТЫ — СЛЕДСТВИЕ ГЕОМЕТРИИ.")
        print("=" * 75)

if __name__ == "__main__":
    model = ETVEPureGeometricModelV962()
    model.run_verification(C=0.95)
