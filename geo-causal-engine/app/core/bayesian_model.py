import numpy as np

class PoliticalInferenceEngine:
    """
    Motor de Inferencia Causal que cruza variables geográficas (estrés ambiental)
    con variables psicométricas (Big Five) para calcular invariantes políticos.
    """
    
    @staticmethod
    def calculate_synthesis(conscientiousness: float, extraversion: float, env_stress: float) -> dict:
        # Ecuación 1: La institucionalidad (Nación) requiere orden y manejo racional del estrés
        nation_score = (conscientiousness * 1.5) + (env_stress * 0.5) - extraversion
        
        # Ecuación 2: El caudillismo (Patria) se alimenta del gregarismo y reacciona emocionalmente al estrés
        patria_score = (extraversion * 1.5) + (env_stress * 0.8) - conscientiousness
        
        # Normalización matemática (Softmax)
        total = np.exp(nation_score) + np.exp(patria_score)
        prob_nation = np.exp(nation_score) / total
        prob_patria = np.exp(patria_score) / total
        
        if prob_nation > prob_patria:
            dominant_structure = "Nación (Institucional / Planificación)"
        else:
            dominant_structure = "Patria (Caudillista / Supervivencia Emocional)"
            
        return {
            "probability_nation": round(float(prob_nation), 4),
            "probability_patria": round(float(prob_patria), 4),
            "dominant_structure": dominant_structure
        }
