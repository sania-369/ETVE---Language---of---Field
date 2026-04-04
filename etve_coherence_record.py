import numpy as np

def coherence_record(grid_size=120, phi_scale=1.2, wave_amplitude=1.33, shift=0.0, nonlinear=0.07):
    x = np.linspace(-2.2 + shift, 2.2 + shift, grid_size)
    y = np.linspace(-2.2 + shift, 2.2 + shift, grid_size)
    z = np.linspace(-2.2 + shift, 2.2 + shift, grid_size)
    X, Y, Z = np.meshgrid(x, y, z)
    phi = (1 + 5**0.5) / 2
    field = (np.sin(phi_scale * phi * X) * np.cos(phi_scale * phi * Y) * np.sin(phi_scale * phi * Z) +
             wave_amplitude * np.cos(phi_scale * phi**2 * np.sqrt(X**2 + Y**2 + Z**2)))
    field = field + nonlinear * field**3
    coherence = np.tanh(np.mean(field**2))
    return coherence

C = coherence_record()
print(f"Рекордная когерентность Ψ-поля: C = {C:.4f}")
