import numpy as np

class AuctionStrategist:
    """
    Implementa estrategias de Equilibrio de Nash Bayesiano para subastas.
    Basado en modelos de Teoría de Juegos (Vickrey / Primer Precio).
    """
    
    @staticmethod
    def optimal_bid_first_price(valuation: float, n_competitors: int, risk_aversion: float = 0.0):
        """
        Calcula la oferta óptima en una subasta de sobre cerrado de primer precio.
        
        Formula Teórica: b(v) = v * ((n-1) / (n - 1 + risk_param))
        Donde:
        - v: Valoración propia del objeto (Privada)
        - n: Número total de licitadores
        - risk_param: 1.0 (Neutral), <1 (Amante del riesgo), >1 (Averso)
        """
        if n_competitors < 2:
            return 0.0 # Si no hay competencia, oferta el mínimo (o cero teóricamente)
            
        # Ajuste por aversión al riesgo (Risk Neutral = 1.0 en el denominador base)
        # En tu PDF: Utilidad U(x) = x^(1-rho). Aquí simplificamos el factor.
        risk_factor = 1.0 + risk_aversion
        
        numerator = n_competitors - 1
        denominator = n_competitors - 1 + risk_factor
        
        optimal_bid = valuation * (numerator / denominator)
        
        expected_profit = (valuation - optimal_bid) * (optimal_bid / valuation)**(n_competitors-1)
        
        return {
            "optimal_bid": round(optimal_bid, 2),
            "implied_margin": round(valuation - optimal_bid, 2),
            "win_probability_estimate": round((optimal_bid / valuation)**(n_competitors-1), 4),
            "expected_utility": round(expected_profit, 4)
        }

    @staticmethod
    def prisoners_dilemma_payoff(strategy_a: str, strategy_b: str):
        """
        Matriz de pagos clásica (Cooperar vs Traicionar).
        Útil para simulación de precios entre duopolios.
        """
        matrix = {
            ("cooperate", "cooperate"): (3, 3),
            ("cooperate", "defect"): (0, 5),
            ("defect", "cooperate"): (5, 0),
            ("defect", "defect"): (1, 1),
        }
        return matrix.get((strategy_a, strategy_b), (0,0))
