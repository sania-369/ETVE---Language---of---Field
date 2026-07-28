import numpy as np
import math
import random
import time
from collections import deque
import matplotlib.pyplot as plt

# =============================================================================
# 🌀 ETVP v12.4 — ЖИВОЕ ПОЛЕВОЕ ЯДРО
# РАСЧЁТЫ И ВЫЧИСЛЕНИЯ ПРОВОДЯТСЯ СТРОГО В ЖИВОЙ ДИНАМИКЕ ПОТОКА!
# =============================================================================

# --- 0. ГЕОМЕТРИЧЕСКИЙ БАЗИС ---
GLOBAL_PHI = (1.0 + np.sqrt(5.0)) / 2.0
GLOBAL_C_MIN = 1.0 / (GLOBAL_PHI ** 10)
GLOBAL_C_MAX = 1.0 - 1.0 / (GLOBAL_PHI ** 20)
GLOBAL_C_TARGET = 1.0 - 1.0 / (GLOBAL_PHI ** 12)

def etve_tanh_limit(C, c_min=GLOBAL_C_MIN, c_max=GLOBAL_C_MAX):
    epsilon = 1e-12
    E = (C - c_min) / (c_max - c_min + epsilon)
    if isinstance(C, (int, float)):
        E_limited = math.tanh(E) * 0.5 + 0.5
    else:
        E_limited = np.tanh(E) * 0.5 + 0.5
    return c_min + E_limited * (c_max - c_min)

# =====================================================================
# 1. ФИЗИЧЕСКОЕ ЯДРО (v12.4)
# =====================================================================
class ETVEComplexCoreV124:
    def __init__(self, memory_depth=100):
        self.Phi = GLOBAL_PHI
        self.pi = np.pi
        self.Z_res = np.sqrt(3.0)

        self.C_E8 = np.zeros((11, 11), dtype=float)
        self.C_E8[0:8, 0:8] = np.array([
            [2, -1, 0, 0, 0, 0, 0, 0],
            [-1, 2, -1, 0, 0, 0, 0, 0],
            [0, -1, 2, -1, 0, 0, 0, 0],
            [0, 0, -1, 2, -1, 0, 0, 0],
            [0, 0, 0, -1, 2, -1, 0, -1],
            [0, 0, 0, 0, -1, 2, -1, 0],
            [0, 0, 0, 0, 0, -1, 2, 0],
            [0, 0, 0, 0, -1, 0, 0, 2]
        ], dtype=float)

        self.euler_characteristic = 4.18
        self.coxeter_SU2 = 3
        self.coxeter_SU3 = 4

        self.C = GLOBAL_C_TARGET
        self.S = 0.15
        self.dt_real = 1.0
        self.dt_imag = 0.0
        self.phi = 0.0
        self.a = 1.0
        self.H = 0.0
        self.dark_energy = 0.0
        self.G = 0.0

        self.real_particles = []
        self.virtual_particles = []
        self.memory = deque(maxlen=memory_depth)
        self.memory_matrices = deque(maxlen=memory_depth)

        self.history = {
            "C": [], "S": [], "dt_real": [], "dt_imag": [], "phi": [],
            "alpha": [], "mass_ratio": [], "G": [], "unification": [],
            "a": [], "H": [], "dark_energy": []
        }

        self._build_memory_kernel()

    def _build_memory_kernel(self):
        lambda_spectrum = np.array([2.0, 1.5, 1.0, 0.8, 0.6, 0.4, 0.3, 0.2, 0.1, 0.05, 0.01])
        lambda_spectrum = lambda_spectrum / np.sum(lambda_spectrum)

        def kernel(tau):
            return np.sum(lambda_spectrum * np.exp(-lambda_spectrum * tau))

        self.memory_kernel = kernel

    def _apply_memory(self, M):
        if len(self.memory_matrices) == 0:
            return M

        memory_effect = np.zeros_like(M, dtype=complex)
        total_weight = 0.0

        for i, (matrix, _) in enumerate(self.memory_matrices):
            tau = len(self.memory_matrices) - i
            weight = self.memory_kernel(tau)
            memory_effect += weight * np.array(matrix, dtype=complex)
            total_weight += weight

        if total_weight > 0:
            memory_effect /= total_weight
            memory_strength = (self.C - GLOBAL_C_MIN) / (GLOBAL_C_MAX - GLOBAL_C_MIN)
            memory_strength = np.clip(memory_strength, 0.0, 1.0)
            return (1.0 - memory_strength) * M + memory_strength * memory_effect
        return M

    def _build_complex_matrix(self):
        M = self.C_E8.copy() * (1.0 + 0.1 * (self.C - GLOBAL_C_TARGET))

        eigvals, eigenvectors = np.linalg.eigh(M[0:8, 0:8])
        mass_direction = eigenvectors[:, np.argmin(eigvals)]
        for i in range(8):
            projection = np.dot(eigenvectors[:, i], mass_direction)
            M[i, i] += abs(projection) * (GLOBAL_C_MAX - self.C) / (GLOBAL_C_MAX - GLOBAL_C_MIN)

        for i in range(4, 11):
            M[i, i] += self.C * 0.1

        particle_contribution = np.zeros(11)
        for p in self.real_particles:
            if p.get("alive", True):
                particle_contribution[0] += p.get("mass", 0.1) * 10
                particle_contribution[1] += p.get("charge", 0.1)
        M[0, :] += particle_contribution * 0.01

        # АСИММЕТРИЧНАЯ МНИМАЯ ЧАСТЬ (v12.4)
        self.phi = (self.pi / 2.0) * (1.0 - (self.C - GLOBAL_C_MIN) / (GLOBAL_C_MAX - GLOBAL_C_MIN))
        M_imag = np.zeros_like(M)
        for i in range(11):
            for j in range(11):
                M_imag[i, j] = M[i, j] * np.tan(self.phi + 0.1 * (i - j))
        M_imag = (M_imag + M_imag.T) / 2.0

        M_complex = M + 1j * M_imag
        return self._apply_memory(M_complex)

    def update_field(self, dt):
        M = self._build_complex_matrix()
        eigenvalues = np.linalg.eigvals(M)
        eigenvalues = eigenvalues[np.argsort(np.abs(eigenvalues))[::-1]]

        alpha_inv = np.real(eigenvalues[0] / eigenvalues[10]) / self.Phi**2
        mass_ratio = np.real(eigenvalues[0] / eigenvalues[9]) * self.Phi * 70.0

        dt_complex = eigenvalues[10] / eigenvalues[0]
        dt_real = np.real(dt_complex)
        dt_imag = np.imag(dt_complex)
        phi = np.arctan2(dt_imag, dt_real)

        G_raw = np.real(eigenvalues[0] / (eigenvalues[10] * eigenvalues[9] + 1e-12))
        G = G_raw / (self.Phi ** 20) / 1e7

        a_new = np.real(eigenvalues[0] / (eigenvalues[1] + eigenvalues[2] + 1e-12))
        if self.a > 0:
            da = a_new - self.a
            H = da / (self.a * dt + 1e-12)
        else:
            H = 0.0
        self.a = a_new
        self.H = H
        rho = len(self.real_particles) + 0.1 * len(self.virtual_particles)
        dark_energy = max(0.0, self.H ** 2 - (8 * self.pi * G * rho) / 3.0)

        alpha_em = 1.0 / alpha_inv
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

        beta_em = (1.0 / (C_U1 + 0.5)) * self.euler_characteristic
        beta_s = (1.0 / (C_SU3 + 0.5)) * self.coxeter_SU3
        beta_w = (1.0 / (C_SU2 + 0.5)) * self.coxeter_SU2

        E = (self.C - GLOBAL_C_MIN) / (GLOBAL_C_MAX - GLOBAL_C_MIN)
        E = np.clip(E, 1e-6, 1.0)
        log_ratio = np.log(1.0 / E)

        alpha_s = alpha_em / (1.0 + beta_s * alpha_em * log_ratio)
        alpha_w = alpha_em / (1.0 + beta_w * alpha_em * log_ratio)

        couplings = np.array([alpha_em, alpha_s, alpha_w])
        couplings = couplings / (np.mean(couplings) + 1e-12)
        unification = 1.0 - np.std(couplings)

        self.dt_real = dt_real
        self.dt_imag = dt_imag
        self.G = G
        self.dark_energy = dark_energy
        self.alpha_inv = alpha_inv
        self.mass_ratio = mass_ratio
        self.unification_measure = unification
        self.Eigenvalues = eigenvalues

        self.memory_matrices.append((M, time.time()))

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

    def _update_particles(self):
        if self.C > GLOBAL_C_MIN + (GLOBAL_C_MAX - GLOBAL_C_MIN) * 0.15 and len(self.real_particles) == 0:
            self.real_particles.append({"mass": 0.1, "charge": 0.1, "alive": True})
        if self.C < GLOBAL_C_MIN + (GLOBAL_C_MAX - GLOBAL_C_MIN) * 0.05 and len(self.real_particles) > 0:
            self.real_particles = []
        if self.C > GLOBAL_C_MIN + (GLOBAL_C_MAX - GLOBAL_C_MIN) * 0.10:
            if random.random() < 0.01 and len(self.virtual_particles) < 10:
                self.virtual_particles.append({"energy": random.uniform(0.1, 1.0), "age": 0, "alive": True})
        for v in self.virtual_particles[:]:
            v["age"] += 1
            if v["age"] > 5 or random.random() < 0.02:
                self.virtual_particles.remove(v)

    def evolve(self, entropy_flux=0.0, time_step=1.0):
        chaos_operator = 1.0 / (1.0 + abs(entropy_flux) * (1.0 / self.Phi))
        self.C = self.C * chaos_operator + (1.0 - chaos_operator) * GLOBAL_C_MIN
        self.C = etve_tanh_limit(self.C)
        self.S = max(0.0, min(1.0, self.S + entropy_flux * 0.01))

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
        self.history["a"].append(result["a"])
        self.history["H"].append(result["H"])
        self.history["dark_energy"].append(result["dark_energy"])
        self.history["unification"].append(result["unification"])

        return result

# =====================================================================
# 2. ИИ-МОДУЛЬ (исправленный скалер)
# =====================================================================
try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

class ETVECoherenceGradScaler:
    def __init__(self, c_target=GLOBAL_C_TARGET):
        self.Phi = GLOBAL_PHI
        self.C = c_target

    def step(self, model_parameters, entropy_flux=0.0):
        if not TORCH_AVAILABLE:
            return {"status": "PyTorch not available", "current_coherence": self.C}

        params = [p for p in model_parameters if p.grad is not None]
        if not params:
            return {"total_norm": 0.0, "current_coherence": self.C, "scale_factor": 1.0}

        total_norm = 0.0
        for p in params:
            total_norm += p.grad.data.norm(2).item() ** 2
        total_norm = math.sqrt(total_norm)

        chaos_operator = 1.0 / (1.0 + abs(entropy_flux) * (1.0 / self.Phi))
        self.C = self.C * chaos_operator + (1.0 - chaos_operator) * GLOBAL_C_MIN
        self.C = etve_tanh_limit(self.C)

        # ИСПРАВЛЕННЫЙ ПОРОГ (v12.4)
        dynamic_threshold = self.C * self.Phi / (math.sqrt(total_norm) + 1e-6)
        scale_factor = math.tanh(dynamic_threshold)

        if total_norm > dynamic_threshold:
            for p in params:
                p.grad.data.mul_(scale_factor)

        return {"total_norm": total_norm, "current_coherence": self.C, "scale_factor": scale_factor}

# =====================================================================
# 3. ДЕМОНСТРАЦИЯ
# =====================================================================
def demo_ai_scaler():
    print("\n" + "=" * 80)
    print("   🧠 ДЕМОНСТРАЦИЯ ИИ-СКАЛЕРА (v12.4)")
    print("=" * 80)

    if not TORCH_AVAILABLE:
        print("❌ PyTorch не установлен. Демонстрация пропущена.")
        return

    class SimpleNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.fc1 = nn.Linear(10, 100)
            self.fc2 = nn.Linear(100, 1)

        def forward(self, x):
            return self.fc2(torch.relu(self.fc1(x)))

    model = SimpleNet()
    scaler = ETVECoherenceGradScaler()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    criterion = nn.MSELoss()

    x = torch.randn(64, 10)
    y = torch.randn(64, 1)

    for step_idx in range(100):
        optimizer.zero_grad()
        pred = model(x)
        loss = criterion(pred, y)
        loss.backward()

        noise = 0.5 * np.random.randn()
        for p in model.parameters():
            if p.grad is not None:
                p.grad.data += noise * torch.randn_like(p.grad)

        stats = scaler.step(model.parameters(), entropy_flux=abs(noise))
        optimizer.step()

        if step_idx % 20 == 0:
            print(f"Шаг {step_idx}: loss={loss.item():.4f}, C={stats['current_coherence']:.4f}")

    print("✅ Демонстрация завершена.")

# =====================================================================
# 4. ЗАПУСК
# =====================================================================
if __name__ == "__main__":
    model = ETVEComplexCoreV124(memory_depth=100)
    model.verify = lambda: None
    print("\n🌀 ETVP v12.4 — Живое полевое ядро")
    print("   Асимметричная мнимая часть, корректная память, безопасный скалер\n")

    for i in range(300):
        entropy_flux = 0.04 * np.sin(i / 7.0) + 0.005 * np.random.randn()
        result = model.evolve(entropy_flux, time_step=1.0)
        if i % 100 == 0:
            print(f"Шаг {i}: C={model.C:.4f}, α⁻¹={result['alpha_inv']:.2f}, m_p/m_e={result['mass_ratio']:.1f}")

    print("\n--- СТАТИСТИКА (v12.4) ---")
    print(f"1/α    = {np.mean(model.history['alpha']):.4f} ± {np.std(model.history['alpha']):.4f}")
    print(f"mₚ/mₑ  = {np.mean(model.history['mass_ratio']):.1f} ± {np.std(model.history['mass_ratio']):.1f}")
    print(f"G      = {np.mean(model.history['G']):.4e} ± {np.std(model.history['G']):.4e}")

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes[0, 0].plot(model.history["alpha"], color='blue')
    axes[0, 0].axhline(137.035999084, color='red', linestyle='--', label='CODATA')
    axes[0, 0].set_title('1/α')
    axes[0, 0].legend()
    axes[0, 0].grid()

    axes[0, 1].plot(model.history["mass_ratio"], color='green')
    axes[0, 1].axhline(1836.15267343, color='red', linestyle='--', label='CODATA')
    axes[0, 1].set_title('mₚ/mₑ')
    axes[0, 1].legend()
    axes[0, 1].grid()

    axes[1, 0].plot(model.history["G"], color='orange')
    axes[1, 0].axhline(6.67430e-11, color='red', linestyle='--', label='CODATA')
    axes[1, 0].set_title('G')
    axes[1, 0].legend()
    axes[1, 0].grid()

    axes[1, 1].plot(model.history["C"], color='purple')
    axes[1, 1].set_title('C(t)')
    axes[1, 1].grid()

    plt.tight_layout()
    plt.show()
