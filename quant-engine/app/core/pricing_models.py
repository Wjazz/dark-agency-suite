import numpy as np
from scipy.stats import norm
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import os

class BlackScholesMath:
    @staticmethod
    def d1(S, K, T, r, sigma):
        # Evitar division por cero
        if sigma <= 0 or T <= 0:
            return 0
        return (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))

    @staticmethod
    def d2(S, K, T, r, sigma):
        if sigma <= 0 or T <= 0:
            return 0
        return BlackScholesMath.d1(S, K, T, r, sigma) - sigma*np.sqrt(T)

    @staticmethod
    def call_price(S, K, T, r, sigma):
        """Fórmula clásica matemática (Benchmark)"""
        if T <= 0: return max(0, S - K)
        d1 = BlackScholesMath.d1(S, K, T, r, sigma)
        d2 = BlackScholesMath.d2(S, K, T, r, sigma)
        return S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)

class NeuralPricer:
    def __init__(self):
        # Perceptrón Multicapa (Simulación de lo aprendido en Semana 11)
        self.model = MLPRegressor(
            hidden_layer_sizes=(64, 64), 
            activation='relu', 
            solver='adam', 
            max_iter=1000,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False

    def train_dummy(self):
        """
        Genera datos sintéticos (Montecarlo) para entrenar la red 
        sin depender de archivos CSV externos por ahora.
        """
        print("Generando datos sintéticos de mercado...")
        n_samples = 10000
        S = np.random.uniform(50, 150, n_samples)
        K = np.random.uniform(50, 150, n_samples)
        T = np.random.uniform(0.1, 2.0, n_samples)
        r = np.random.uniform(0.01, 0.05, n_samples)
        sigma = np.random.uniform(0.1, 0.5, n_samples)

        # Matriz de características
        X = np.column_stack((S, K, T, r, sigma))
        
        # El "Target" es el precio real calculado con la fórmula
        y = np.array([BlackScholesMath.call_price(s, k, t, r_, sig) for s, k, t, r_, sig in zip(S, K, T, r, sigma)])

        print("Entrenando Red Neuronal...")
        self.model.fit(X, y)
        self.is_trained = True
        print("Entrenamiento completado.")

    def predict(self, S, K, T, r, sigma):
        if not self.is_trained:
            self.train_dummy()
        
        input_data = np.array([[S, K, T, r, sigma]])
        price = self.model.predict(input_data)[0]
        return max(0.0, price)
