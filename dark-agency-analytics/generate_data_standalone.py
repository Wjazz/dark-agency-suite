"""
Quick Synthetic Data Generator - Standalone Version
Generates dataset for Dark Agency Analytics Platform demonstration.
"""

import sys
import os
import numpy as np
import pandas as pd
from scipy import stats

# Ensure output directory exists
output_dir = "../../data/synthetic"
os.makedirs(output_dir, exist_ok=True)

print("🔬 Generating synthetic psychometric dataset...")
print(f"Output directory: {os.path.abspath(output_dir)}")

# Set random seed
np.random.seed(42)
n_samples = 1000

# 1. Generate Dark Tetrad (simplified)
print("\n📊 Generating Dark Tetrad traits...")
G_base = np.random.normal(2.5, 1.0, n_samples).clip(1, 7)
S_Agencia_base = np.random.normal(3.5, 0.9, n_samples).clip(1, 7)

narcissism = S_Agencia_base + np.random.normal(0, 0.3, n_samples)
machiavellianism = S_Agencia_base + np.random.normal(0, 0.3, n_samples)
psychopathy = G_base + np.random.normal(0, 0.4, n_samples)
sadism = G_base + np.random.normal(0, 0.4, n_samples)

narcissism = narcissism.clip(1, 7)
machiavellianism = machiavellianism.clip(1, 7)
psychopathy = psychopathy.clip(1, 7)
sadism = sadism.clip(1, 7)

# 2. Generate Big Five
print("📊 Generating Big Five...")
openness = np.random.normal(3.5, 0.6, n_samples).clip(1, 5)
conscientiousness = np.random.normal(3.7, 0.6, n_samples).clip(1, 5)
extraversion = np.random.normal(3.3, 0.7, n_samples).clip(1, 5)
agreeableness = (3.6 - 0.3 * stats.zscore(G_base) + np.random.normal(0, 0.4, n_samples)).clip(1, 5)
neuroticism = np.random.normal(2.9, 0.8, n_samples).clip(1, 5)

# 3. Generate PsyCap
print("📊 Generating PsyCap...")
hope = np.random.normal(4.2, 0.7, n_samples).clip(1, 6)
efficacy = np.random.normal(4.5, 0.6, n_samples).clip(1, 6)
resilience = np.random.normal(4.0, 0.8, n_samples).clip(1, 6)
optimism = np.random.normal(4.3, 0.7, n_samples).clip(1, 6)
psycap_composite = (hope + efficacy + resilience + optimism) / 4

# 4. Generate POPS
print("📊 Generating POPS...")
POPS = (3.0 + 0.3 * stats.zscore(neuroticism) + np.random.normal(0, 0.8, n_samples)).clip(1, 5)

# 5. Generate VEE (Strategic Scanning)
print("📊 Generating VEE...")
VEE = (
    3.0 +
    0.35 * stats.zscore(S_Agencia_base) +
    0.25 * stats.zscore(POPS) +
    0.20 * stats.zscore(S_Agencia_base) * stats.zscore(POPS) +
    np.random.normal(0, 0.6, n_samples)
).clip(1, 5)

# 6. Generate EIB (Intrapreneurship)
print("📊 Generating EIB...")
EIB = (
    3.0 +
    0.30 * stats.zscore(S_Agencia_base) +
    -0.20 * stats.zscore(G_base) +
    0.35 * stats.zscore(VEE) +
    0.25 * stats.zscore(psycap_composite) +
    0.15 * stats.zscore(S_Agencia_base) * stats.zscore(psycap_composite) +
    0.20 * stats.zscore(openness) +
    np.random.normal(0, 0.5, n_samples)
).clip(1, 5)

# 7. Generate CWB-O and CWB-I
print("📊 Generating CWB outcomes...")
CWB_O = (
    2.0 +
    0.28 * stats.zscore(S_Agencia_base) +
    0.15 * stats.zscore(G_base) +
    -0.20 * stats.zscore(conscientiousness) +
    np.random.normal(0, 0.6, n_samples)
).clip(1, 5)

CWB_I = (
    1.8 +
    0.45 * stats.zscore(G_base) +
    0.05 * stats.zscore(S_Agencia_base) +
    -0.35 * stats.zscore(agreeableness) +
    np.random.normal(0, 0.5, n_samples)
).clip(1, 5)

# 8. Demographics
print("📊 Generating demographics...")
employee_id = np.arange(1, n_samples + 1)
age = np.random.normal(32, 8, n_samples).astype(int).clip(22, 60)
gender = np.random.choice(['M', 'F'], n_samples, p=[0.52, 0.48])
sector = np.random.choice(
    ['Finanzas', 'Telecomunicaciones', 'Consultoría', 'Seguros', 'Servicios Empresariales'],
    n_samples,
    p=[0.25, 0.20, 0.20, 0.15, 0.20]
)
tenure_months = np.random.exponential(24, n_samples).astype(int).clip(1, 120)

# Create DataFrame
print("\n📦 Creating final dataset...")
df = pd.DataFrame({
    'employee_id': employee_id,
    'age': age,
    'gender': gender,
    'sector': sector,
    'tenure_months': tenure_months,
    'narcissism': narcissism,
    'machiavellianism': machiavellianism,
    'psychopathy': psychopathy,
    'sadism': sadism,
    'G_latent': G_base,
    'S_Agencia_latent': S_Agencia_base,
    'openness': openness,
    'conscientiousness': conscientiousness,
    'extraversion': extraversion,
    'agreeableness': agreeableness,
    'neuroticism': neuroticism,
    'hope': hope,
    'efficacy': efficacy,
    'resilience': resilience,
    'optimism': optimism,
    'psycap_composite': psycap_composite,
    'POPS': POPS,
    'VEE': VEE,
    'EIB': EIB,
    'CWB_O': CWB_O,
    'CWB_I': CWB_I
})

# Save
output_path = os.path.join(output_dir, "psychometric_dataset_n1000.csv")
df.to_csv(output_path, index=False)
print(f"\n✅ Dataset saved to: {os.path.abspath(output_path)}")
print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")

# Summary statistics
print("\n📊 Summary Statistics:")
summary_cols = ['narcissism', 'machiavellianism', 'psychopathy', 'sadism',
                'EIB', 'CWB_O', 'CWB_I', 'psycap_composite']
print(df[summary_cols].describe().round(2))

# Theoretical validations
print("\n🔗 Key Correlations (Theoretical Validation):")
print(f"   S_Agencia × EIB:   {df['S_Agencia_latent'].corr(df['EIB']):.3f}  (expected: ~0.30)")
print(f"   G × CWB-I:         {df['G_latent'].corr(df['CWB_I']):.3f}  (expected: ~0.45)")
print(f"   S_Agencia × CWB-O: {df['S_Agencia_latent'].corr(df['CWB_O']):.3f}  (expected: ~0.28)")
print(f"   G × EIB:           {df['G_latent'].corr(df['EIB']):.3f}  (expected: ~-0.20)")

print("\n🎉 Data generation complete!")
