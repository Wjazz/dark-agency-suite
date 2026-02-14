import numpy as np
from scipy.stats import norm

class DarkRiskEngine:
    def __init__(self, confidence_level=0.95):
        self.confidence_level = confidence_level

    def calculate_parametric_var(self, portfolio_value: float, volatility: float, z_score: float = None) -> float:
        """
        Calculates Parametric VaR.
        VaR = Position * Volatility * Z-Score
        """
        if z_score is None:
            z_score = norm.ppf(self.confidence_level)
        
        return portfolio_value * volatility * z_score

    def stress_test_climate_scenario(self, portfolio_value: float, current_volatility: float, shock_factor: float):
        """
        Simulates a climate scenario by applying a shock multiplier to volatility.
        """
        # 1. Calculate baseline risk
        base_z = norm.ppf(self.confidence_level)
        original_var = self.calculate_parametric_var(portfolio_value, current_volatility, base_z)
        
        # 2. Apply Shock (Climate Scenario)
        stressed_volatility = current_volatility * shock_factor
        stressed_var = self.calculate_parametric_var(portfolio_value, stressed_volatility, base_z)
        
        return {
            "scenario_shock_factor": shock_factor,
            "original_volatility": current_volatility,
            "stressed_volatility": stressed_volatility,
            "original_var": round(original_var, 2),
            "stressed_var": round(stressed_var, 2),
            "capital_loss_increase": round(stressed_var - original_var, 2),
            "percent_increase": round(((stressed_var - original_var) / original_var) * 100, 2)
        }
