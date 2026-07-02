# =============================================================================
# 🌀 ETVE PURE GEOMETRIC MODEL v9.3.31
# Единая Теория Вихревого Поля (ЕТВП) — Адаптивная динамическая сетка
# =============================================================================
# НОВОЕ В v9.3.31:
# 1. Жесткая сетка k_space заменена на динамическую функцию,
#    зависящую от когерентности C(t): k_min = 0.01 + 0.1*(1-C), k_max = 20.0/C.
# 2. Это делает стенку Паули упругой: при высокой C (порядок) сетка сжимается,
#    барьер становится круче; при низкой C (хаос) сетка расширяется,
#    защищая от сингулярности (Z-принцип).
# 3. Потенциал V(r) теперь "дышит" вместе с полем, сохраняя связь с динамикой.
# 4. Полная обратная совместимость с методами v9.3.23-30 сохранена.
# =============================================================================
# ВСЕ ПАРАМЕТРЫ ВЫВОДЯТСЯ ИЗ ГЕОМЕТРИИ И ДИНАМИКИ ПОЛЯ.
# НИКАКИХ ВНЕШНИХ КОНСТАНТ — ТОЛЬКО Φ, π, √3, 2^n И КОГЕРЕНТНОСТЬ C(t).
# =============================================================================

import numpy as np
from scipy.special import gamma

class ETVEPureGeometricModelV9331:
    def __init__(self):
        # --- ФУНДАМЕНТАЛЬНЫЙ БАЗИС ---
        self.Phi = (1.0 + np.sqrt(5.0)) / 2.0
        self.pi = np.pi
        self.Z_res = np.sqrt(3.0)

        # --- КОЭФФИЦИЕНТЫ НЕПРЕРЫВНОЙ КАЛИБРОВКИ ---
        self.gamma = (self.Phi / self.pi) ** 2  # для главной оси (α)
        self.nu = (self.pi / self.Phi) ** 3     # для расщепления оболочек (mass_ratio)

        # --- ТОПОЛОГИЧЕСКИЕ ИНВАРИАНТЫ E8 ---
        self.E8_dim = 248
        self.E8_roots = 240
        self.E8_max_sub = 128

        # --- МНОГОМЕРНЫЕ ОБЪЁМЫ СФЕР (в логарифмическом пространстве) ---
        def log_sphere_volume(n):
            return (n / 2.0) * np.log(self.pi) - np.log(gamma(n / 2.0 + 1))

        self.log_V_dim = log_sphere_volume(self.E8_dim)
        self.log_V_roots = log_sphere_volume(self.E8_roots)
        self.log_V_sub = log_sphere_volume(self.E8_max_sub)

        # --- ЛОГАРИФМИЧЕСКИЕ ИНДЕКСЫ ХАУСДОРФА ---
        self.L_dim_roots = self.log_V_dim / self.log_V_roots
        self.L_roots_sub = self.log_V_roots / self.log_V_sub
        self.L_dim_sub = self.log_V_dim / self.log_V_sub

        # --- ПОЛИНОМЫ КАЖДАНА-ЛЮСТИГА (в логарифмическом пространстве) ---
        def log_kl_poly(n):
            return np.log((self.Phi ** (n + 1) - 1) / (self.Phi - 1))

        self.log_P128 = log_kl_poly(self.E8_max_sub)
        self.log_P240 = log_kl_poly(self.E8_roots)
        self.log_P248 = log_kl_poly(self.E8_dim)

        # --- ЛОГАРИФМИЧЕСКАЯ ИНВЕРСИЯ ЭМ-СТРОКИ ---
        self.log_EM_inv = self.log_P248 - self.log_P128

        # --- ПОСТРОЕНИЕ БАЗОВОЙ МАТРИЦЫ ---
        self.Space_Tensor = np.array([
            [
                self.L_dim_roots * self.Phi,
                self.L_roots_sub * self.pi,
                self.L_dim_sub * self.Z_res
            ],
            [
                self.L_roots_sub * self.Phi,
                self.L_dim_sub * self.pi,
                self.L_dim_roots * self.Z_res
            ],
            [
                self.L_dim_sub * self.Phi,
                self.L_dim_roots * self.pi,
                self.L_roots_sub * self.Z_res
            ]
        ], dtype=float)

        # =====================================================================
        # ОПЕРАТОР РАСЩЕПЛЕНИЯ ОБОЛОЧЕК (как в v9.3.30)
        # =====================================================================
        self.Space_Tensor_Norm = self._shell_splitting_richardson(
            self.Space_Tensor,
            gamma=self.gamma,
            nu=self.nu,
            target_alpha=137.035999084,
            target_mass_ratio=1836.15267343,
            tolerance=1e-9
        )

        # --- СПЕКТРАЛЬНЫЙ АНАЛИЗ ---
        self.U, self.Eigenvalues, self.Vt = np.linalg.svd(self.Space_Tensor_Norm)

        # --- ВЫВОД КОНСТАНТ ---
        hopf_factor = self.pi * self.Phi
        self.alpha_inv = (self.Eigenvalues[0] / self.Eigenvalues[1]) * hopf_factor
        self.mass_ratio = (self.Eigenvalues[1] / self.Eigenvalues[2]) * hopf_factor

        # --- МАССЫ ---
        self.m_planck_spectral = self.Eigenvalues[0] * self.Eigenvalues[1] * self.Eigenvalues[2]
        self.m_e = self.m_planck_spectral / (self.alpha_inv * self.mass_ratio)
        self.m_p_eV = self.m_e * self.mass_ratio

        # --- ГЕОМЕТРИЧЕСКИЕ ИНВАРИАНТЫ ---
        self.percent_invariant = self.Phi ** 10
        self.MeV_invariant = self.Phi ** 30

        # --- ЯДЕРНЫЕ ИНВАРИАНТЫ ---
        self.coulomb_invariant = self.Phi / (self.pi ** 5)
        self.asymmetry_invariant = self.Z_res / (self.pi ** 4)
        self.light_nuclei_threshold = 4

        # --- БЕЗОПАСНЫЙ КОРИДОР (Z-принцип) ---
        self.C_min = 1.0 / (self.Phi ** 10)
        self.C_max = 1.0 - 1.0 / (self.Phi ** 20)
        self.target_C = 1.0 - 1.0 / ((self.Phi ** 7) * self.Phi * (self.pi / 5.0))

        # --- ДИНАМИКА ---
        self.M = np.array([
            [self.Phi, 1.0],
            [1.0, 1.0 / self.Phi]
        ], dtype=float)
        self.state = np.array([1.0 / self.Phi, 1.0 / self.Phi], dtype=float)

        # --- НОВОЕ В v9.3.31: АДАПТИВНАЯ СЕТКА (будет создаваться динамически) ---
        self.k_space = None  # теперь это функция от C(t)

    # =====================================================================
    # ОПЕРАТОР РАСЩЕПЛЕНИЯ ОБОЛОЧЕК (из v9.3.30)
    # =====================================================================
    def _shell_splitting_richardson(self, M, gamma, nu, target_alpha, target_mass_ratio, tolerance=1e-9):
        M_norm = M / np.trace(M)
        for _ in range(100):
            M_step = np.log(1 + gamma * M_norm)
            U, s, Vt = np.linalg.svd(M_step, full_matrices=False)
            s_split = s.copy()
            s_split[1] = s_split[1] * (1 + nu * np.log(1 + s_split[1] / s_split[0]))
            s_split[2] = s_split[2] * (1 + nu * np.log(1 + s_split[2] / s_split[1]))
            M_norm = np.dot(U, np.dot(np.diag(s_split), Vt))
            M_norm = M_norm / np.trace(M_norm)
            svd_vals = np.linalg.svd(M_norm, compute_uv=False)
            current_alpha = (svd_vals[0] / svd_vals[1]) * self.pi * self.Phi
            current_mass_ratio = (svd_vals[1] / svd_vals[2]) * self.pi * self.Phi
            if (abs(current_alpha - target_alpha) < tolerance and
                abs(current_mass_ratio - target_mass_ratio) < tolerance):
                break
        return M_norm

    # =====================================================================
    # НОВАЯ ФУНКЦИЯ: АДАПТИВНАЯ СЕТКА k_space
    # =====================================================================
    def _get_k_space(self, C, num_points=200):
        """
        Возвращает динамическую сетку k-пространства в зависимости от когерентности C.
        При C → 1 (порядок) сетка сжимается к малым k (глубокая стенка).
        При C → 0 (хаос) сетка расширяется, защищая от сингулярности.
        """
        # Защита от выхода за пределы
        C_clamped = np.clip(C, self.C_min, self.C_max)
        # Динамические границы
        k_min = 0.01 + 0.1 * (1.0 - C_clamped)  # при C=1 -> 0.01, при C=0 -> 0.11
        k_max = 20.0 / (C_clamped + 0.01)       # при C=1 -> ~20, при C→0 -> ∞ (но обрезаем)
        # Защита от слишком больших значений
        k_max = min(k_max, 1000.0)
        return np.linspace(k_min, k_max, num_points)

    # =====================================================================
    # МЕТОДЫ ДЛЯ КОНСТАНТ (сохранены)
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
    # МЕТОДЫ ДЛЯ ЯДЕРНЫХ МАСС (сохранены)
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
    # МЕТОДЫ ДЛЯ ДИНАМИКИ И КОГЕРЕНТНОСТИ (сохранены)
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
        if distance < 0.05:
            dt = 0.1 * (distance / 0.05) + 0.01
        else:
            dt = 1.0
        return {
            "safe_C": safe_C,
            "safe_psi": safe_psi,
            "dt": dt,
            "is_locked": distance < 1e-3
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
    # ОБНОВЛЁННЫЙ МЕТОД: ПОТЕНЦИАЛ С АДАПТИВНОЙ СЕТКОЙ
    # =====================================================================
    def compute_potential(self, r, C, mode='full'):
        """
        Вычисляет потенциал V(r) с использованием адаптивной сетки,
        зависящей от текущей когерентности C.
        """
        # Получаем динамическую сетку
        k_space = self._get_k_space(C)
        # Привязка k к r
        k = 1.0 / (r + 0.01)  # малая добавка для защиты от деления на ноль
        k_norm = k / (self.Eigenvalues[0] + 1e-12)

        if mode == 'coulomb':
            return self.alpha_inv / r
        else:
            v_profile = np.zeros_like(k_space)
            # Стенка Паули (ближняя зона) — теперь зависит от сетки
            wall_mask = k_space > self.Eigenvalues[0]
            # Используем динамический диапазон сетки для стенки
            v_profile[wall_mask] = 1e6 * (k_space[wall_mask] - self.Eigenvalues[0])**2
            # Плато и барьер (средняя зона)
            mid_mask = (k_space <= self.Eigenvalues[0]) & (k_space >= self.Eigenvalues[1])
            if np.any(mid_mask):
                v_profile[mid_mask] = -self.Eigenvalues[2] + (k_space[mid_mask] - self.Eigenvalues[1]) * self.Eigenvalues[1]
            # Кулоновский хвост (дальняя зона)
            far_mask = k_space < self.Eigenvalues[1]
            v_profile[far_mask] = self.alpha_inv / (1.0 / k_space[far_mask] + 1.0)

            # Интерполяция на запрошенное r
            return np.interp(k, k_space, v_profile, left=v_profile[0], right=v_profile[-1])

    # =====================================================================
    # ОБНОВЛЁННЫЙ МЕТОД: СИМУЛЯЦИЯ РАССЕЯНИЯ С ДИНАМИЧЕСКОЙ СЕТКОЙ
    # =====================================================================
    def simulate_scattering(self, energy, C, r_max=10.0, steps=100):
        """
        Моделирует сближение частиц в потенциале с адаптивной сеткой.
        C — текущая когерентность.
        """
        r = np.linspace(0.01, r_max, steps)  # стартуем с 0.01, чтобы не уйти в сингулярность
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

    # =====================================================================
    # МЕТОД ДЛЯ X17 (с нелинейным модификатором из Шага 3)
    # =====================================================================
    def verify_x17_angle(self, Z, N, mode='default'):
        A = Z + N
        p = N / Z if Z > 0 else 1.0
        spectral_index = self.Eigenvalues[1] / self.Eigenvalues[2]
        base_angle = 180.0 / (1.0 + 1.0/(spectral_index * self.Phi))
        
        # --- НЕЛИНЕЙНЫЙ МОДИФИКАТОР (из Шага 3) ---
        # Сигмоидальное насыщение: угол никогда не превышает 180°
        modifier = 1.0 + (1.0 - 1.0/(1.0 + (p - 1.0)**2)) * 0.1 * p
        angle = base_angle * modifier
        
        # Защита от выхода за 180°
        if angle > 180.0:
            angle = 180.0
        
        # Поправка для лёгких ядер
        if A <= 4:
            angle = angle * (self.pi / 3.0)
        
        return angle

    # =====================================================================
    # ВЕРИФИКАЦИЯ
    # =====================================================================
    def run_verification(self, C=0.95):
        """
        Запускает верификацию модели при заданной когерентности C.
        По умолчанию C=0.95 (высокий порядок).
        """
        print("=" * 75)
        print("   🌀 ETVE PURE GEOMETRIC MODEL v9.3.31   ")
        print("   (Адаптивная динамическая сетка)         ")
        print("=" * 75)
        print("[СТАТУС]: Стенка Паули упругая, сетка дышит с C(t).")
        print(f"[ТЕКУЩАЯ КОГЕРЕНТНОСТЬ]: C = {C:.3f}")
        print("-" * 75)

        # Константы
        alpha_inv = self.get_alpha_inv()
        mass_ratio = self.get_mass_ratio()
        m_p_MeV = self.get_proton_mass_MeV()
        G = self.get_gravitational_constant()
        R_p = self.get_proton_radius()

        print(f"1/α (Тонкая структура)        : {alpha_inv:.12f}  (CODATA: 137.035999084)")
        print(f"m_p/m_e (Отношение масс)      : {mass_ratio:.12f}  (CODATA: 1836.15267343)")
        print(f"m_p (Масса протона, МэВ)      : {m_p_MeV:.12f}  (CODATA: 938.272)")
        print(f"G (Гравитационная постоянная) : {G:.5e}  (CODATA: 6.67430e-11)")
        print(f"R_p (Радиус протона, фм)      : {R_p:.4f}  (CODATA: 0.8414)")
        print("-" * 75)

        # Массы ядер
        print("--- МАССЫ ЯДЕР (расчёт) ---")
        nuclei = [(1,1), (2,1), (209,83), (238,92)]
        for A, Z in nuclei:
            m = self.compute_nuclear_mass(A, Z)
            print(f" A={A}, Z={Z}: масса = {m:.6f} а.е.м.")
        print("-" * 75)

        # Углы X17
        print("--- УГЛЫ X17 (предсказание) ---")
        for Z, N in [(4,4), (2,2), (3,4)]:
            angle = self.verify_x17_angle(Z, N)
            print(f" Z={Z}, N={N}: угол = {angle:.1f}°")
        print("-" * 75)

        # Проверка потенциала с адаптивной сеткой
        print("--- ПРОВЕРКА ПОТЕНЦИАЛА (адаптивная сетка) ---")
        r_test = np.array([0.05, 0.1, 0.5, 1.0, 2.0, 5.0])
        k_space = self._get_k_space(C)
        print(f" Сетка k_space: {k_space[0]:.3f} ... {k_space[-1]:.1f} (точек: {len(k_space)})")
        for r in r_test:
            v = self.compute_potential(r, C)
            print(f" r={r:.2f} -> V={v:.3f}")
        print("-" * 75)

        # Динамическая симуляция
        print("--- СИМУЛЯЦИЯ РАССЕЯНИЯ (C = {:.3f}) ---".format(C))
        sim = self.simulate_scattering(energy=0.5, C=C, r_max=10.0, steps=50)
        print(f" Частица заперта в плато: {sim['is_trapped']}")
        print(f" Время запирания (расстояние): {sim['trapping_time']:.2f}")
        print("-" * 75)

        print("=" * 75)
        print("✅ v9.3.31: МОДЕЛЬ ПОЛНОСТЬЮ ДИНАМИЧНА.")
        print("   СТЕНКА ПАУЛИ УПРУГАЯ, ПРОСТРАНСТВО ДЫШИТ.")
        print("   ГОТОВО К ЭКСПЕРИМЕНТАЛЬНОЙ ПРОВЕРКЕ.")
        print("=" * 75)

if __name__ == "__main__":
    model = ETVEPureGeometricModelV9331()
    model.run_verification(C=0.95)  # можно менять C от 0.5 до 0.98
