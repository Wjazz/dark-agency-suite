"""
Synthetic Psychometric Data Generator.

Generates realistic datasets for Dark Tetrad, Big Five, PsyCap, EIB, and CWB
with theoretically-informed correlations based on thesis hypotheses.

Author: James Alvarado
Based on: Master's Thesis - Dark Agency in Institutional Voids
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PsychometricDataGenerator:
    """
    Generates synthetic psychometric data with realistic correlations.
    
    Theoretical assumptions (from thesis):
    - S_Agencia (N + M) correlates positively with EIB (r ≈ 0.35)
    - G (P + S) correlates negatively with EIB (r ≈ -0.25)
    - S_Agencia correlates positively with CWB-O (r ≈ 0.30)
    - G correlates strongly with CWB-I (r ≈ 0.45)
    - PsyCap moderates S_Agencia → EIB relationship
    - POPS moderates S_Agencia → VEE relationship
    """
    
    def __init__(self, n_samples: int = 1000, random_state: int = 42):
        """
        Initialize generator.
        
        Args:
            n_samples: Number of synthetic employees to generate
            random_state: Random seed for reproducibility
        """
        self.n_samples = n_samples
        self.rng = np.random.RandomState(random_state)
        
    def generate_dark_tetrad(self) -> pd.DataFrame:
        """
        Generate SD4 (Short Dark Tetrad) scores.
        
        28 items, 7 per trait (Narcissism, Machiavellianism, Psychopathy, Sadism)
        Likert 1-7 scale
        
        Returns:
            DataFrame with 28 item columns + 4 trait means
        """
        logger.info("Generating Dark Tetrad data...")
        
        # Define correlations between traits (from literature meta-analyses)
        # Correlation matrix for 4 traits: N, M, P, S
        corr_matrix = np.array([
            [1.00, 0.25, 0.30, 0.20],  # Narcissism
            [0.25, 1.00, 0.45, 0.35],  # Machiavellianism
            [0.30, 0.45, 1.00, 0.50],  # Psychopathy
            [0.20, 0.35, 0.50, 1.00]   # Sadism
        ])
        
        # Generate correlated trait scores
        mean_scores = self.rng.multivariate_normal(
            mean=[3.5, 3.2, 2.8, 2.5],  # Population means from literature
            cov=self._corr_to_cov(corr_matrix, [0.8, 0.9, 1.0, 1.1]),
            size=self.n_samples
        )
        
        # Clip to valid range [1, 7]
        mean_scores = np.clip(mean_scores, 1, 7)
        
        df = pd.DataFrame({
            'narcissism': mean_scores[:, 0],
            'machiavellianism': mean_scores[:, 1],
            'psychopathy': mean_scores[:, 2],
            'sadism': mean_scores[:, 3]
        })
        
        # Generate individual items with noise around trait means
        for trait_idx, trait in enumerate(['narcissism', 'machiavellianism', 'psychopathy', 'sadism']):
            for item in range(1, 8):  # 7 items per trait
                item_col = f'{trait}_item{item}'
                # Add item-specific noise
                df[item_col] = df[trait] + self.rng.normal(0, 0.5, self.n_samples)
                df[item_col] = np.clip(np.round(df[item_col]), 1, 7)
        
        logger.info(f"Generated {self.n_samples} Dark Tetrad profiles")
        return df
    
    def generate_big_five(self) -> pd.DataFrame:
        """
        Generate Big Five personality scores (OCEAN).
        
        5-point Likert scale (1-5)
        
        Returns:
            DataFrame with 5 trait columns
        """
        logger.info("Generating Big Five data...")
        
        # Correlation with Dark Tetrad (from literature)
        # Antagonism (low Agreeableness) is core of Dark Factor
        corr_matrix = np.array([
            [1.00, 0.10, 0.15, 0.05, -0.10],  # Openness
            [0.10, 1.00, 0.20, 0.30, -0.15],  # Conscientiousness
            [0.15, 0.20, 1.00, 0.10, -0.25],  # Extraversion
            [0.05, 0.30, 0.10, 1.00, -0.40],  # Agreeableness (key: negatively related to Dark)
            [-0.10, -0.15, -0.25, -0.40, 1.00]   # Neuroticism
        ])
        
        mean_scores = self.rng.multivariate_normal(
            mean=[3.5, 3.7, 3.3, 3.6, 2.9],
            cov=self._corr_to_cov(corr_matrix, [0.6, 0.6, 0.7, 0.6, 0.8]),
            size=self.n_samples
        )
        
        mean_scores = np.clip(mean_scores, 1, 5)
        
        df = pd.DataFrame({
            'openness': mean_scores[:, 0],
            'conscientiousness': mean_scores[:, 1],
            'extraversion': mean_scores[:, 2],
            'agreeableness': mean_scores[:, 3],
            'neuroticism': mean_scores[:, 4]
        })
        
        logger.info("Big Five generated")
        return df
    
    def generate_psycap(self) -> pd.DataFrame:
        """
        Generate Psychological Capital (PsyCap) scores.
        
        4 dimensions: Hope, Efficacy, Resilience, Optimism
        6-point Likert scale (1-6)
        
        Returns:
            DataFrame with 4 dimension columns + composite
        """
        logger.info("Generating PsyCap data...")
        
        # High internal consistency (dimensions highly correlated)
        corr_matrix = np.array([
            [1.00, 0.60, 0.55, 0.50],  # Hope
            [0.60, 1.00, 0.50, 0.45],  # Efficacy
            [0.55, 0.50, 1.00, 0.55],  # Resilience
            [0.50, 0.45, 0.55, 1.00]   # Optimism
        ])
        
        mean_scores = self.rng.multivariate_normal(
            mean=[4.2, 4.5, 4.0, 4.3],
            cov=self._corr_to_cov(corr_matrix, [0.7, 0.6, 0.8, 0.7]),
            size=self.n_samples
        )
        
        mean_scores = np.clip(mean_scores, 1, 6)
        
        df = pd.DataFrame({
            'hope': mean_scores[:, 0],
            'efficacy': mean_scores[:, 1],
            'resilience': mean_scores[:, 2],
            'optimism': mean_scores[:, 3]
        })
        
        # Composite PsyCap
        df['psycap_composite'] = df[['hope', 'efficacy', 'resilience', 'optimism']].mean(axis=1)
        
        logger.info("PsyCap generated")
        return df
    
    def generate_outcomes(self, 
                         dark_tetrad: pd.DataFrame,
                         big_five: pd.DataFrame,
                         psycap: pd.DataFrame) -> pd.DataFrame:
        """
        Generate outcome variables (EIB, CWB-O, CWB-I, POPS, VEE).
        
        Based on theoretical model from thesis.
        
        Args:
            dark_tetrad: Dark Tetrad scores
            big_five: Big Five scores
            psycap: PsyCap scores
            
        Returns:
            DataFrame with outcome variables
        """
        logger.info("Generating outcome variables based on theoretical model...")
        
        # Create latent factors
        # G (General Antagonism) = Psychopathy + Sadism
        G = (dark_tetrad['psychopathy'] + dark_tetrad['sadism']) / 2
        
        # S_Agencia (Dark Agency) = Narcissism + Machiavellianism (residual to G)
        # Simplified: just the mean, residualization happens in modeling
        S_Agencia = (dark_tetrad['narcissism'] + dark_tetrad['machiavellianism']) / 2
        
        # POPS (Perceived Organizational Politics) - context variable
        # Weakly related to neuroticism
        POPS = (
            3.0 +  # baseline
            0.3 * stats.zscore(big_five['neuroticism']) +
            self.rng.normal(0, 0.8, self.n_samples)
        )
        POPS = np.clip(POPS, 1, 5)
        
        # VEE (Strategic Environmental Scanning)
        # Predicted by S_Agencia, moderated by POPS
        VEE = (
            3.0 +
            0.35 * stats.zscore(S_Agencia) +
            0.25 * stats.zscore(POPS) +
            0.20 * stats.zscore(S_Agencia) * stats.zscore(POPS) +  # interaction
            self.rng.normal(0, 0.6, self.n_samples)
        )
        VEE = np.clip(VEE, 1, 5)
        
        # EIB (Employee Intrapreneurship Behavior)
        # Hypothesis: S_Agencia → VEE → EIB (mediation)
        # PsyCap moderates S_Agencia → EIB
        EIB = (
            3.0 +
            0.30 * stats.zscore(S_Agencia) +
            -0.20 * stats.zscore(G) +  # negative effect of antagonism
            0.35 * stats.zscore(VEE) +  # mediation path
            0.25 * stats.zscore(psycap['psycap_composite']) +
            0.15 * stats.zscore(S_Agencia) * stats.zscore(psycap['psycap_composite']) +  # moderation
            0.20 * stats.zscore(big_five['openness']) +
            0.15 * stats.zscore(big_five['conscientiousness']) +
            self.rng.normal(0, 0.5, self.n_samples)
        )
        EIB = np.clip(EIB, 1, 5)
        
        # CWB-O (Counterproductive Work Behavior - Organizational)
        # Predicted by S_Agencia (instrumental norm-breaking)
        CWB_O = (
            2.0 +  # lower baseline (less frequent)
            0.28 * stats.zscore(S_Agencia) +
            0.15 * stats.zscore(G) +
            -0.20 * stats.zscore(big_five['conscientiousness']) +
            self.rng.normal(0, 0.6, self.n_samples)
        )
        CWB_O = np.clip(CWB_O, 1, 5)
        
        # CWB-I (Counterproductive Work Behavior - Interpersonal)
        # Strongly predicted by G (antagonism), not S_Agencia
        CWB_I = (
            1.8 +  # even lower baseline
            0.45 * stats.zscore(G) +  # strong effect
            0.05 * stats.zscore(S_Agencia) +  # weak/null effect
            -0.35 * stats.zscore(big_five['agreeableness']) +
            0.20 * stats.zscore(big_five['neuroticism']) +
            self.rng.normal(0, 0.5, self.n_samples)
        )
        CWB_I = np.clip(CWB_I, 1, 5)
        
        df = pd.DataFrame({
            'G_latent': G,
            'S_Agencia_latent': S_Agencia,
            'POPS': POPS,
            'VEE': VEE,
            'EIB': EIB,
            'CWB_O': CWB_O,
            'CWB_I': CWB_I
        })
        
        logger.info("Outcome variables generated with theoretical correlations")
        return df
    
    def generate_demographics(self) -> pd.DataFrame:
        """
        Generate demographic variables.
        
        Returns:
            DataFrame with employee_id, age, gender, sector, tenure
        """
        logger.info("Generating demographics...")
        
        df = pd.DataFrame({
            'employee_id': range(1, self.n_samples + 1),
            'age': self.rng.normal(32, 8, self.n_samples).astype(int).clip(22, 60),
            'gender': self.rng.choice(['M', 'F'], self.n_samples, p=[0.52, 0.48]),
            'sector': self.rng.choice(
                ['Finanzas', 'Telecomunicaciones', 'Consultoría', 'Seguros', 'Servicios Empresariales'],
                self.n_samples,
                p=[0.25, 0.20, 0.20, 0.15, 0.20]
            ),
            'tenure_months': self.rng.exponential(24, self.n_samples).astype(int).clip(1, 120)
        })
        
        logger.info("Demographics generated")
        return df
    
    def generate_full_dataset(self) -> pd.DataFrame:
        """
        Generate complete synthetic dataset.
        
        Returns:
            DataFrame with all variables
        """
        logger.info(f"Generating complete dataset for {self.n_samples} employees...")
        
        # Generate each component
        demographics = self.generate_demographics()
        dark_tetrad = self.generate_dark_tetrad()
        big_five = self.generate_big_five()
        psycap = self.generate_psycap()
        outcomes = self.generate_outcomes(dark_tetrad, big_five, psycap)
        
        # Merge all
        df = pd.concat([demographics, dark_tetrad, big_five, psycap, outcomes], axis=1)
        
        logger.info(f"Complete dataset generated: {df.shape[0]} rows × {df.shape[1]} columns")
        return df
    
    @staticmethod
    def _corr_to_cov(corr_matrix: np.ndarray, std_devs: list) -> np.ndarray:
        """
        Convert correlation matrix to covariance matrix.
        
        Args:
            corr_matrix: Correlation matrix
            std_devs: Standard deviations for each variable
            
        Returns:
            Covariance matrix
        """
        D = np.diag(std_devs)
        return D @ corr_matrix @ D


if __name__ == "__main__":
    # Example usage
    generator = PsychometricDataGenerator(n_samples=1000, random_state=42)
    
    # Generate full dataset
    df = generator.generate_full_dataset()
    
    # Save to CSV
    output_path = "../../data/synthetic/psychometric_dataset_n1000.csv"
    df.to_csv(output_path, index=False)
    print(f"\n✅ Dataset saved to: {output_path}")
    
    # Display summary statistics
    print("\n📊 Summary Statistics:")
    print(df[['narcissism', 'machiavellianism', 'psychopathy', 'sadism', 
              'EIB', 'CWB_O', 'CWB_I', 'psycap_composite']].describe())
    
    # Display correlations (theoretical validation)
    print("\n🔗 Key Correlations:")
    print(f"S_Agencia × EIB: {df['S_Agencia_latent'].corr(df['EIB']):.3f} (expected: ~0.30)")
    print(f"G × CWB-I: {df['G_latent'].corr(df['CWB_I']):.3f} (expected: ~0.45)")
    print(f"S_Agencia × CWB-O: {df['S_Agencia_latent'].corr(df['CWB_O']):.3f} (expected: ~0.28)")
    print(f"G × EIB: {df['G_latent'].corr(df['EIB']):.3f} (expected: ~-0.20)")
