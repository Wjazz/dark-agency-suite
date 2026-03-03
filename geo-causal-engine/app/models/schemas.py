from pydantic import BaseModel, Field

class GeoPsychometricInput(BaseModel):
    # Variables Espaciales (Teledetección - Obtenidas por ej. de Google Earth Engine)
    ndvi_mean: float = Field(..., description="Índice de Vegetación de Diferencia Normalizada promedio (Abundancia de recursos)", ge=-1.0, le=1.0)
    lst_mean_celsius: float = Field(..., description="Land Surface Temperature (Estrés térmico)")

    # Variables Psicométricas (Provenientes de tu people-analytics-etl)
    extraversion_agg: float = Field(..., description="Agregado poblacional de Extraversión (Hedonismo/Gregarismo)", ge=0, le=1)
    conscientiousness_agg: float = Field(..., description="Agregado poblacional de Responsabilidad (Planificación)", ge=0, le=1)
