# dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Título (Como el dashboard de la imagen)
st.title("🛡️ Maverick Hunter: Dashboard de Operaciones")

# 2. ETL (En lugar de Power Query)
@st.cache_data
def load_data():
    # Simulamos datos de tu tesis (Agencia Oscura vs Desempeño)
    df = pd.DataFrame({
        'Agente': [f'Agente {i}' for i in range(100)],
        'S_Agency': np.random.normal(0.5, 0.15, 100),
        'G_Factor': np.random.normal(0.4, 0.2, 100),
        'Desempeño': np.random.randint(50, 100, 100)
    })
    return df

df = load_data()

# 3. Métricas (KPIs como en la imagen de la clase)
col1, col2, col3 = st.columns(3)
col1.metric("Agentes Activos", "100")
col2.metric("Promedio Agencia Oscura", f"{df['S_Agency'].mean():.2f}")
col3.metric("Riesgo Detectado", "Alta", delta_color="inverse")

# 4. Visualización (En lugar de arrastrar gráficos)
fig = px.scatter(df, x='S_Agency', y='G_Factor', size='Desempeño', color='Desempeño',
                 title="Matriz de Riesgo: Agencia vs Antagonismo")
st.plotly_chart(fig)

# 5. Análisis Avanzado (Lo que Power BI no hace fácil)
if st.button('Correr Simulación de Estrés'):
    st.write("Ejecutando modelo Monte Carlo en backend C++...")
    st.progress(100)
    st.success("Simulación completada. El sistema resiste.")