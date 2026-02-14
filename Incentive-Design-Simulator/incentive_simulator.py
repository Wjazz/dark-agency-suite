"""
Simulador de Incentivos Comerciales
Permite diseñar y testear esquemas de incentivos con múltiples escenarios

Uso:
    python incentive_simulator.py

Autor: James - Portfolio People Analytics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, List, Tuple
import seaborn as sns

@dataclass
class KPIConfig:
    """Configuración de un KPI en el esquema de incentivos"""
    name: str
    weight: float  # Peso en % (0-1)
    threshold: float  # Mínimo para pagar (%)
    target: float  # Meta (100%)
    cap: float  # Máximo (%)
    accelerator: float = 1.0  # Multiplicador sobre target
    
    def calculate_payout(self, achievement: float) -> float:
        """
        Calcula el pago % basado en el logro
        
        Args:
            achievement: % de logro del KPI
            
        Returns:
            % de pago para este KPI
        """
        if achievement < self.threshold:
            return 0.0
        
        if achievement <= self.target:
            # Pago lineal desde threshold hasta target
            payout = ((achievement - self.threshold) / 
                     (self.target - self.threshold)) * 100
        else:
            # Sobre target: aplicar acelerador
            if achievement > self.cap:
                achievement = self.cap
            
            over_target = achievement - self.target
            payout = 100 + (over_target * self.accelerator)
        
        return min(payout, (self.cap - self.threshold) / 
                   (self.target - self.threshold) * 100)


class IncentiveScheme:
    """Esquema completo de incentivos con múltiples KPIs"""
    
    def __init__(self, name: str, oti_annual: float):
        """
        Args:
            name: Nombre del esquema
            oti_annual: On-Target Incentive anual en moneda local
        """
        self.name = name
        self.oti_annual = oti_annual
        self.kpis: List[KPIConfig] = []
    
    def add_kpi(self, kpi: KPIConfig):
        """Agregar KPI al esquema"""
        self.kpis.append(kpi)
    
    def validate(self) -> Tuple[bool, str]:
        """Validar que la configuración sea correcta"""
        total_weight = sum(kpi.weight for kpi in self.kpis)
        
        if not np.isclose(total_weight, 1.0, atol=0.01):
            return False, f"Pesos no suman 100%: {total_weight*100:.1f}%"
        
        return True, "Esquema válido"
    
    def calculate_total_payout(self, achievements: Dict[str, float]) -> Dict:
        """
        Calcula el pago total basado en logros de KPIs
        
        Args:
            achievements: Dict con {nombre_kpi: % logro}
            
        Returns:
            Dict con breakdown del cálculo
        """
        results = {
            'kpi_details': [],
            'total_payout_pct': 0,
            'incentive_amount': 0
        }
        
        for kpi in self.kpis:
            achievement = achievements.get(kpi.name, 0)
            payout_pct = kpi.calculate_payout(achievement)
            contribution = payout_pct * kpi.weight
            
            results['kpi_details'].append({
                'kpi': kpi.name,
                'achievement': achievement,
                'payout': payout_pct,
                'weight': kpi.weight * 100,
                'contribution': contribution
            })
            
            results['total_payout_pct'] += contribution
        
        results['incentive_amount'] = (self.oti_annual * 
                                      results['total_payout_pct'] / 100)
        
        return results
    
    def simulate_scenarios(self, n_scenarios: int = 1000) -> pd.DataFrame:
        """
        Simula múltiples escenarios aleatorios de cumplimiento
        
        Args:
            n_scenarios: Número de escenarios a simular
            
        Returns:
            DataFrame con resultados de simulación
        """
        scenarios = []
        
        for i in range(n_scenarios):
            # Generar logros aleatorios (distribución normal)
            achievements = {}
            for kpi in self.kpis:
                # Media = target, std dev = 15%
                achievement = np.random.normal(kpi.target, 15)
                achievement = max(0, min(achievement, kpi.cap + 10))
                achievements[kpi.name] = achievement
            
            result = self.calculate_total_payout(achievements)
            
            scenario = {
                'scenario_id': i + 1,
                'total_payout_pct': result['total_payout_pct'],
                'incentive_amount': result['incentive_amount']
            }
            
            # Agregar logros de cada KPI
            for kpi_detail in result['kpi_details']:
                scenario[f"{kpi_detail['kpi']}_achievement"] = kpi_detail['achievement']
                scenario[f"{kpi_detail['kpi']}_payout"] = kpi_detail['payout']
            
            scenarios.append(scenario)
        
        return pd.DataFrame(scenarios)


def create_sodimac_sales_scheme() -> IncentiveScheme:
    """
    Crea un esquema de incentivos para vendedor Sodimac
    Basado en las necesidades del puesto
    """
    # Salario anual promedio vendedor: S/. 36,000
    # OTI: 30% = S/. 10,800
    scheme = IncentiveScheme("Vendedor Sodimac", oti_annual=10800)
    
    # KPI 1: Ventas netas (50% peso)
    scheme.add_kpi(KPIConfig(
        name="Ventas",
        weight=0.50,
        threshold=85,
        target=100,
        cap=130,
        accelerator=1.5  # 1.5x sobre 100%
    ))
    
    # KPI 2: Margen bruto (30% peso)
    scheme.add_kpi(KPIConfig(
        name="Margen",
        weight=0.30,
        threshold=90,
        target=100,
        cap=120,
        accelerator=1.2
    ))
    
    # KPI 3: NPS (20% peso)
    scheme.add_kpi(KPIConfig(
        name="NPS",
        weight=0.20,
        threshold=80,
        target=100,
        cap=110,
        accelerator=1.0  # Lineal
    ))
    
    return scheme


def visualize_payout_curve(kpi: KPIConfig):
    """Visualiza la curva de pago de un KPI"""
    achievements = np.linspace(kpi.threshold - 10, kpi.cap + 10, 100)
    payouts = [kpi.calculate_payout(a) for a in achievements]
    
    plt.figure(figsize=(10, 6))
    plt.plot(achievements, payouts, linewidth=2)
    
    # Marcar puntos clave
    plt.axvline(kpi.threshold, color='red', linestyle='--', 
                label=f'Threshold ({kpi.threshold}%)', alpha=0.7)
    plt.axvline(kpi.target, color='green', linestyle='--', 
                label=f'Target ({kpi.target}%)', alpha=0.7)
    plt.axvline(kpi.cap, color='orange', linestyle='--', 
                label=f'Cap ({kpi.cap}%)', alpha=0.7)
    
    plt.xlabel('Achievement (%)', fontsize=12)
    plt.ylabel('Payout (%)', fontsize=12)
    plt.title(f'Curva de Pago - {kpi.name}', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'payout_curve_{kpi.name}.png', dpi=300, bbox_inches='tight')
    print(f"✓ Curva guardada: payout_curve_{kpi.name}.png")


def visualize_simulation_results(df: pd.DataFrame, scheme: IncentiveScheme):
    """Visualiza los resultados de la simulación"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Distribución de pagos
    axes[0, 0].hist(df['total_payout_pct'], bins=50, edgecolor='black', alpha=0.7)
    axes[0, 0].axvline(df['total_payout_pct'].mean(), color='red', 
                       linestyle='--', label=f'Media: {df["total_payout_pct"].mean():.1f}%')
    axes[0, 0].set_xlabel('Payout Total (%)')
    axes[0, 0].set_ylabel('Frecuencia')
    axes[0, 0].set_title('Distribución de Pagos Simulados')
    axes[0, 0].legend()
    axes[0, 0].grid(alpha=0.3)
    
    # 2. Distribución de montos
    axes[0, 1].hist(df['incentive_amount'], bins=50, edgecolor='black', 
                    alpha=0.7, color='green')
    axes[0, 1].axvline(df['incentive_amount'].mean(), color='red', 
                       linestyle='--', 
                       label=f'Media: S/. {df["incentive_amount"].mean():.0f}')
    axes[0, 1].set_xlabel('Monto Incentivo (S/.)')
    axes[0, 1].set_ylabel('Frecuencia')
    axes[0, 1].set_title('Distribución de Montos de Incentivo')
    axes[0, 1].legend()
    axes[0, 1].grid(alpha=0.3)
    
    # 3. Logros por KPI
    kpi_achievements = [col for col in df.columns if '_achievement' in col]
    data_to_plot = [df[col] for col in kpi_achievements]
    labels = [col.replace('_achievement', '') for col in kpi_achievements]
    
    axes[1, 0].boxplot(data_to_plot, labels=labels)
    axes[1, 0].axhline(100, color='red', linestyle='--', alpha=0.5, label='Target')
    axes[1, 0].set_ylabel('Achievement (%)')
    axes[1, 0].set_title('Distribución de Logros por KPI')
    axes[1, 0].legend()
    axes[1, 0].grid(alpha=0.3)
    
    # 4. Estadísticas resumen
    axes[1, 1].axis('off')
    stats_text = f"""
    ESTADÍSTICAS DE SIMULACIÓN
    {'='*40}
    
    Escenarios simulados: {len(df):,}
    
    Payout Total:
      • Media: {df['total_payout_pct'].mean():.1f}%
      • Mediana: {df['total_payout_pct'].median():.1f}%
      • Desv. Est.: {df['total_payout_pct'].std():.1f}%
      • Min: {df['total_payout_pct'].min():.1f}%
      • Max: {df['total_payout_pct'].max():.1f}%
    
    Monto Incentivo:
      • Media: S/. {df['incentive_amount'].mean():,.0f}
      • Mediana: S/. {df['incentive_amount'].median():,.0f}
      • Total simulado: S/. {df['incentive_amount'].sum():,.0f}
    
    Distribución de Pagos:
      • Sin pago (0%): {(df['total_payout_pct'] == 0).sum()} ({(df['total_payout_pct'] == 0).sum()/len(df)*100:.1f}%)
      • Parcial (<100%): {((df['total_payout_pct'] > 0) & (df['total_payout_pct'] < 100)).sum()} ({((df['total_payout_pct'] > 0) & (df['total_payout_pct'] < 100)).sum()/len(df)*100:.1f}%)
      • Target (100%±5%): {((df['total_payout_pct'] >= 95) & (df['total_payout_pct'] <= 105)).sum()} ({((df['total_payout_pct'] >= 95) & (df['total_payout_pct'] <= 105)).sum()/len(df)*100:.1f}%)
      • Sobre target (>105%): {(df['total_payout_pct'] > 105).sum()} ({(df['total_payout_pct'] > 105).sum()/len(df)*100:.1f}%)
    """
    axes[1, 1].text(0.1, 0.9, stats_text, transform=axes[1, 1].transAxes,
                    fontsize=10, verticalalignment='top', fontfamily='monospace')
    
    plt.tight_layout()
    plt.savefig('simulation_results.png', dpi=300, bbox_inches='tight')
    print(f"✓ Resultados guardados: simulation_results.png")


def main():
    """Función principal de demostración"""
    print("="*60)
    print("SIMULADOR DE INCENTIVOS COMERCIALES")
    print("Portfolio: People Analytics & Compensation")
    print("="*60)
    
    # Crear esquema Sodimac
    print("\n📊 Creando esquema: Vendedor Sodimac")
    scheme = create_sodimac_sales_scheme()
    
    # Validar
    is_valid, message = scheme.validate()
    print(f"✓ Validación: {message}")
    
    if not is_valid:
        print("❌ Error en configuración")
        return
    
    # Visualizar curvas de pago
    print("\n📈 Generando curvas de pago por KPI...")
    for kpi in scheme.kpis:
        visualize_payout_curve(kpi)
    
    # Ejemplo de cálculo individual
    print("\n🧮 Ejemplo de cálculo individual:")
    print("-" * 60)
    achievements = {
        "Ventas": 112,
        "Margen": 95,
        "NPS": 105
    }
    
    result = scheme.calculate_total_payout(achievements)
    
    print(f"\nLogros:")
    for kpi_detail in result['kpi_details']:
        print(f"  • {kpi_detail['kpi']}: {kpi_detail['achievement']:.0f}% "
              f"→ Payout: {kpi_detail['payout']:.1f}% "
              f"→ Contribución: {kpi_detail['contribution']:.1f}%")
    
    print(f"\nResultado Final:")
    print(f"  • Payout Total: {result['total_payout_pct']:.1f}%")
    print(f"  • Monto Incentivo: S/. {result['incentive_amount']:,.2f}")
    
    # Simulación de escenarios
    print("\n🎲 Ejecutando simulación de 10,000 escenarios...")
    df_simulation = scheme.simulate_scenarios(n_scenarios=10000)
    
    # Guardar resultados
    df_simulation.to_csv('simulation_results.csv', index=False)
    print(f"✓ Resultados guardados: simulation_results.csv")
    
    # Visualizar
    print("\n📊 Generando visualizaciones...")
    visualize_simulation_results(df_simulation, scheme)
    
    # Análisis de costo para empresa
    print("\n💰 ANÁLISIS DE COSTO (50 vendedores):")
    print("-" * 60)
    n_employees = 50
    mean_payout = df_simulation['incentive_amount'].mean()
    total_cost = mean_payout * n_employees
    
    print(f"  • Empleados: {n_employees}")
    print(f"  • Payout promedio: S/. {mean_payout:,.0f}")
    print(f"  • Costo total anual: S/. {total_cost:,.0f}")
    print(f"  • Percentil 10: S/. {df_simulation['incentive_amount'].quantile(0.1):,.0f}")
    print(f"  • Percentil 50: S/. {df_simulation['incentive_amount'].quantile(0.5):,.0f}")
    print(f"  • Percentil 90: S/. {df_simulation['incentive_amount'].quantile(0.9):,.0f}")
    
    print("\n" + "="*60)
    print("✅ Simulación completada exitosamente")
    print("="*60)


if __name__ == "__main__":
    # Configurar estilo de gráficos
    sns.set_style("whitegrid")
    plt.rcParams['figure.facecolor'] = 'white'
    
    main()
