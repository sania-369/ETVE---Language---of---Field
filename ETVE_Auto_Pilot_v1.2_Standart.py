import numpy as np

def simulate_etve_resonance(target_coherence):
    # Константы системы ETVE
    base_kcf = 1.0
    chaos_threshold = 0.4
    
    # Расчет Kcf (Коэффициент Когерентности Поля) на основе целевой когерентности
    # При 0.61 Kcf был ~1.2. При 0.8 система должна стать стабильнее.
    kcf = base_kcf + (target_coherence ** 2) * 0.8
    
    # Оценка стабильности (чем ближе к 1.0, тем чище сигнал)
    stability = 1.0 - (1.0 - target_coherence) / 2
    
    # Chaos Factor (Энтропия)
    chaos_factor = (1.0 - target_coherence) * 0.5
    
    return {
        "target_coherence": target_coherence,
        "kcf": round(kcf, 4),
        "stability_index": round(stability, 4),
        "chaos_factor": round(chaos_factor, 4)
    }

# Симуляция для 0.61 (предыдущий порог) и 0.80 (новый запрос)
results_061 = simulate_etve_resonance(0.61)
results_080 = simulate_etve_resonance(0.80)

print(f"Results 0.61: {results_061}")
print(f"Results 0.80: {results_080}")
