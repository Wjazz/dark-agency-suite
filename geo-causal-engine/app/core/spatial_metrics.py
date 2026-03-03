class SpatialStressCalculator:
    @staticmethod
    def calculate_environmental_stress(ndvi: float, lst: float) -> float:
        """
        Convierte variables de teledetección continua en un vector de estrés discreto.
        Bajo NDVI (poca vegetación/agua) + Alta Temperatura (LST) = Alto Estrés Ambiental.
        """
        # Normalizamos la temperatura asumiendo un máximo hostil de 45°C
        norm_temp = min(lst / 45.0, 1.0)
        
        # El estrés es inversamente proporcional al NDVI (recursos) y directamente a la temperatura
        resource_scarcity = 1.0 - max(ndvi, 0.0)
        
        environmental_stress = (resource_scarcity * 0.6) + (norm_temp * 0.4)
        return round(environmental_stress, 4)
