"""
Módulo de visualización para el simulador de motor síncrono

Implementa gráficos y curvas para:
- Curva par-ángulo (T_e vs δ)
- Evolución temporal de variables
- Gráfico de factor de potencia vs excitación
- Otras visualizaciones relevantes
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from typing import Dict, List, Tuple, Optional, Any
import matplotlib.patches as patches
from motor_model import SynchronousMotorModel
from simulation_engine import SimulationEngine


class MotorPlots:
    """
    Generador de gráficos para análisis del motor síncrono
    """

    def __init__(self, motor_model: SynchronousMotorModel):
        self.motor = motor_model
        self.engine = SimulationEngine(motor_model)

        # Configuración de estilo
        plt.style.use('default')
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'accent': '#2ca02c',
            'warning': '#d62728',
            'neutral': '#7f7f7f'
        }

    def create_torque_angle_curve(self, delta_range: Tuple[float, float] = (-np.pi/2, np.pi/2),
                                 num_points: int = 200, figsize: Tuple[float, float] = (10, 6)) -> Figure:
        """
        Crea la curva característica par-ángulo (T_e vs δ)

        Muestra la relación entre par electromagnético y ángulo de carga,
        incluyendo el punto de operación actual.
        """
        fig, ax = plt.subplots(figsize=figsize)

        # Generar datos de la curva
        stability_data = self.engine.stability_analysis(delta_range, num_points)

        deltas_deg = np.degrees(stability_data['delta'])
        T_e = stability_data['T_e']

        # Graficar curva completa
        ax.plot(deltas_deg, T_e, 'b-', linewidth=2, label='Curva T_e(δ)')

        # Resaltar región estable (pendiente negativa)
        stable_mask = stability_data['stable_region']
        if np.any(stable_mask):
            ax.fill_between(deltas_deg[stable_mask], T_e[stable_mask],
                          alpha=0.3, color='green', label='Región estable')

        # Marcar punto de operación actual
        current_results = self.motor.steady_state_analysis()
        current_delta_deg = current_results['delta_deg']
        current_T_e = current_results['T_e']

        ax.plot(current_delta_deg, current_T_e, 'ro', markersize=8,
               label=f'Punto operación (δ={current_delta_deg:.1f}°, T_e={current_T_e:.1f} N·m)')

        # Marcar par máximo
        T_max = stability_data['T_max']
        delta_max_deg = np.degrees(stability_data['delta_max'])
        ax.plot(delta_max_deg, T_max, 'k*', markersize=10,
               label=f'Par máximo (δ={delta_max_deg:.1f}°, T_max={T_max:.1f} N·m)')

        # Configurar gráfico
        ax.set_xlabel('Ángulo de carga δ [°]')
        ax.set_ylabel('Par electromagnético T_e [N·m]')
        ax.set_title('Curva Característica Par-Ángulo del Motor Síncrono')
        ax.grid(True, alpha=0.3)
        ax.legend()

        # Añadir líneas de referencia
        ax.axhline(y=0, color='k', linestyle='--', alpha=0.5)
        ax.axvline(x=0, color='k', linestyle='--', alpha=0.5)

        plt.tight_layout()
        return fig

    def create_transient_plots(self, transient_data: Dict[str, np.ndarray],
                             figsize: Tuple[float, float] = (12, 8)) -> Figure:
        """
        Crea gráficos de evolución temporal para simulación transitoria

        Incluye velocidad, ángulo de carga, pares y potencias.
        """
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle('Evolución Temporal - Simulación Transitoria', fontsize=14)

        t = transient_data.get('time', np.array([]))
        if len(t) == 0:
            return fig

        # Gráfico 1: Velocidad
        ax1 = axes[0, 0]
        omega_m = transient_data.get('omega_m', np.zeros_like(t))
        omega_s = self.motor.synchronous_speed()
        n_m = omega_m * 60 / (2 * np.pi)  # RPM
        n_s = omega_s * 60 / (2 * np.pi)  # RPM síncrona

        ax1.plot(t, n_m, 'b-', linewidth=2, label='Velocidad mecánica')
        ax1.plot(t, np.full_like(t, n_s), 'r--', linewidth=1, label=f'Velocidad síncrona ({n_s:.1f} RPM)')
        ax1.set_ylabel('Velocidad [RPM]')
        ax1.set_title('Velocidad del Motor')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Gráfico 2: Ángulo de carga
        ax2 = axes[0, 1]
        delta_deg = transient_data.get('delta_deg', np.zeros_like(t))
        ax2.plot(t, delta_deg, 'g-', linewidth=2, label='Ángulo de carga')
        ax2.set_ylabel('Ángulo δ [°]')
        ax2.set_title('Ángulo de Carga Eléctrico')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        # Gráfico 3: Pares
        ax3 = axes[1, 0]
        T_e = transient_data.get('T_e', np.zeros_like(t))
        T_load = transient_data.get('T_load', np.zeros_like(t))

        ax3.plot(t, T_e, 'b-', linewidth=2, label='Par electromagnético')
        ax3.plot(t, T_load, 'r-', linewidth=2, label='Par de carga')
        ax3.set_xlabel('Tiempo [s]')
        ax3.set_ylabel('Par [N·m]')
        ax3.set_title('Pares Electromagnético y de Carga')
        ax3.grid(True, alpha=0.3)
        ax3.legend()

        # Gráfico 4: Potencias
        ax4 = axes[1, 1]
        P = transient_data.get('P', np.zeros_like(t))
        Q = transient_data.get('Q', np.zeros_like(t))

        ax4.plot(t, P/1000, 'b-', linewidth=2, label='Potencia activa')
        ax4.plot(t, Q/1000, 'orange', linewidth=2, label='Potencia reactiva')
        ax4.set_xlabel('Tiempo [s]')
        ax4.set_ylabel('Potencia [kW/kVAR]')
        ax4.set_title('Potencias Activa y Reactiva')
        ax4.grid(True, alpha=0.3)
        ax4.legend()

        plt.tight_layout()
        return fig

    def create_power_factor_plot(self, If_range: Tuple[float, float] = (0.1, 5.0),
                                num_points: int = 50, figsize: Tuple[float, float] = (10, 6)) -> Figure:
        """
        Crea gráfico de factor de potencia vs corriente de excitación

        Muestra cómo cambia el factor de potencia al variar la excitación,
        indicando regiones subexcitada y sobreexcitada.
        """
        fig, ax = plt.subplots(figsize=figsize)

        # Generar datos
        If_values, pf_values, pf_types = self.motor.power_factor_vs_excitation(If_range, num_points)

        # Separar por tipo de factor de potencia
        inductive_mask = np.array([t == 'inductivo' for t in pf_types])
        capacitive_mask = np.array([t == 'capacitivo' for t in pf_types])

        # Graficar
        ax.plot(If_values[inductive_mask], pf_values[inductive_mask],
               'b-', linewidth=2, label='Factor inductivo')
        ax.plot(If_values[capacitive_mask], pf_values[capacitive_mask],
               'r-', linewidth=2, label='Factor capacitivo')

        # Marcar punto de operación actual
        ax.plot(self.motor.If, self.motor.steady_state_analysis()['pf'],
               'ko', markersize=8, label='Punto actual')

        # Líneas de referencia
        ax.axhline(y=1.0, color='k', linestyle='--', alpha=0.5, label='Factor unidad')
        ax.axvline(x=self.motor.If, color='k', linestyle=':', alpha=0.5)

        # Región subexcitada (izquierda del punto unidad)
        unity_pf_If = If_values[np.argmin(np.abs(pf_values - 1.0))]
        ax.axvspan(If_range[0], unity_pf_If, alpha=0.2, color='blue',
                  label='Región subexcitada')

        # Región sobreexcitada (derecha del punto unidad)
        ax.axvspan(unity_pf_If, If_range[1], alpha=0.2, color='red',
                  label='Región sobreexcitada')

        # Configurar gráfico
        ax.set_xlabel('Corriente de excitación I_f [A]')
        ax.set_ylabel('Factor de potencia')
        ax.set_title('Factor de Potencia vs Corriente de Excitación')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_ylim(0.8, 1.05)

        plt.tight_layout()
        return fig

    def create_parameter_sweep_plot(self, parameter: str, value_range: Tuple[float, float],
                                   target_variable: str, num_points: int = 20,
                                   figsize: Tuple[float, float] = (10, 6)) -> Figure:
        """
        Crea gráfico de barrido de parámetros

        Muestra cómo cambia una variable objetivo al variar un parámetro.
        """
        fig, ax = plt.subplots(figsize=figsize)

        # Realizar barrido
        sweep_results = self.engine.parameter_sweep(parameter, value_range, num_points)

        # Extraer datos
        param_values = [r[f'parameter_{parameter}'] for r in sweep_results]
        target_values = [r[target_variable] for r in sweep_results]

        # Graficar
        ax.plot(param_values, target_values, 'b-o', linewidth=2, markersize=4)

        # Marcar punto actual
        current_value = getattr(self.motor, parameter)
        current_results = self.motor.steady_state_analysis()
        current_target = current_results[target_variable]

        ax.plot(current_value, current_target, 'ro', markersize=8,
               label=f'Punto actual ({parameter}={current_value:.2f}, {target_variable}={current_target:.2f})')

        # Configurar gráfico
        param_label = self._get_parameter_label(parameter)
        target_label = self._get_variable_label(target_variable)

        ax.set_xlabel(f'{param_label}')
        ax.set_ylabel(f'{target_label}')
        ax.set_title(f'{target_label} vs {param_label}')
        ax.grid(True, alpha=0.3)
        ax.legend()

        plt.tight_layout()
        return fig

    def create_comparison_plot(self, results_list: List[Dict[str, Any]],
                              variables: List[str], labels: List[str],
                              figsize: Tuple[float, float] = (12, 8)) -> Figure:
        """
        Crea gráfico comparativo de múltiples simulaciones

        Útil para comparar diferentes escenarios o configuraciones.
        """
        if len(results_list) != len(labels):
            raise ValueError("El número de resultados debe coincidir con el número de etiquetas")

        num_vars = len(variables)
        fig, axes = plt.subplots((num_vars + 1) // 2, 2, figsize=figsize)
        if num_vars == 1:
            axes = [axes]
        axes = axes.flatten()

        colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown']

        for i, var in enumerate(variables):
            ax = axes[i]

            for j, results in enumerate(results_list):
                if var in results and 'time' in results:
                    color = colors[j % len(colors)]
                    ax.plot(results['time'], results[var], color=color,
                           linewidth=2, label=labels[j])

            var_label = self._get_variable_label(var)
            ax.set_ylabel(var_label)
            ax.set_title(f'{var_label} vs Tiempo')
            ax.grid(True, alpha=0.3)
            ax.legend()

        # Ocultar ejes no utilizados
        for i in range(num_vars, len(axes)):
            axes[i].set_visible(False)

        plt.tight_layout()
        return fig

    def create_motor_status_display(self, results: Dict[str, float],
                                   figsize: Tuple[float, float] = (10, 6)) -> Figure:
        """
        Crea un display de estado del motor con valores actuales

        Muestra las variables más importantes en un formato fácil de leer.
        """
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')

        # Título
        ax.text(5, 9.5, 'Estado Actual del Motor Síncrono', ha='center',
               fontsize=14, fontweight='bold')

        # Variables eléctricas
        y_pos = 8.5
        ax.text(1, y_pos, 'Variables Eléctricas:', fontsize=12, fontweight='bold')

        electrical_vars = [
            ('V_line', 'Tensión de línea', 'V'),
            ('f', 'Frecuencia', 'Hz'),
            ('If', 'Corriente de excitación', 'A'),
            ('I_magnitude', 'Corriente de línea', 'A'),
            ('P', 'Potencia activa', 'W'),
            ('Q', 'Potencia reactiva', 'VAR'),
            ('S', 'Potencia aparente', 'VA'),
            ('pf', 'Factor de potencia', ''),
        ]

        for var, label, unit in electrical_vars:
            y_pos -= 0.5
            value = results.get(var, 0)
            if var == 'pf':
                text = f'{label}: {value:.3f}'
            elif var in ['P', 'Q', 'S']:
                text = f'{label}: {value/1000:.1f} k{unit}'
            else:
                text = f'{label}: {value:.1f} {unit}'
            ax.text(1.5, y_pos, text, fontsize=10)

        # Variables mecánicas
        y_pos = 8.5
        ax.text(6, y_pos, 'Variables Mecánicas:', fontsize=12, fontweight='bold')

        mechanical_vars = [
            ('omega_s', 'Velocidad síncrona', 'rad/s'),
            ('n_s', 'Velocidad síncrona', 'RPM'),
            ('delta_deg', 'Ángulo de carga', '°'),
            ('T_e', 'Par electromagnético', 'N·m'),
            ('T_load', 'Par de carga', 'N·m'),
        ]

        for var, label, unit in mechanical_vars:
            y_pos -= 0.5
            value = results.get(var, 0)
            text = f'{label}: {value:.1f} {unit}'
            ax.text(6.5, y_pos, text, fontsize=10)

        # Información adicional
        y_pos -= 1
        pf_type = results.get('pf_type', 'desconocido')
        ax.text(1, y_pos, f'Tipo de factor de potencia: {pf_type}', fontsize=10)

        y_pos -= 0.5
        connection = self.motor.connection
        ax.text(1, y_pos, f'Conexión: {connection}', fontsize=10)

        return fig

    def _create_motor_status_display_on_axes(self, ax, results: Dict[str, float]) -> None:
        """
        Crea el display de estado en ejes existentes (para evitar fugas de memoria)
        """
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')

        # Título
        ax.text(5, 9.5, 'Estado Actual del Motor Síncrono', ha='center',
               fontsize=14, fontweight='bold')

        # Variables eléctricas
        y_pos = 8.5
        ax.text(1, y_pos, 'Variables Eléctricas:', fontsize=12, fontweight='bold')

        electrical_vars = [
            ('V_line', 'Tensión de línea', 'V'),
            ('f', 'Frecuencia', 'Hz'),
            ('If', 'Corriente de excitación', 'A'),
            ('I_magnitude', 'Corriente de línea', 'A'),
            ('P', 'Potencia activa', 'W'),
            ('Q', 'Potencia reactiva', 'VAR'),
            ('S', 'Potencia aparente', 'VA'),
            ('pf', 'Factor de potencia', ''),
        ]

        for var, label, unit in electrical_vars:
            y_pos -= 0.5
            value = results.get(var, 0)
            if var == 'pf':
                text = f'{label}: {value:.3f}'
            elif var in ['P', 'Q', 'S']:
                text = f'{label}: {value/1000:.1f} k{unit}'
            else:
                text = f'{label}: {value:.1f} {unit}'
            ax.text(1.5, y_pos, text, fontsize=10)

        # Variables mecánicas
        y_pos = 8.5
        ax.text(6, y_pos, 'Variables Mecánicas:', fontsize=12, fontweight='bold')

        mechanical_vars = [
            ('omega_s', 'Velocidad síncrona', 'rad/s'),
            ('n_s', 'Velocidad síncrona', 'RPM'),
            ('delta_deg', 'Ángulo de carga', '°'),
            ('T_e', 'Par electromagnético', 'N·m'),
            ('T_load', 'Par de carga', 'N·m'),
        ]

        for var, label, unit in mechanical_vars:
            y_pos -= 0.5
            value = results.get(var, 0)
            text = f'{label}: {value:.1f} {unit}'
            ax.text(6.5, y_pos, text, fontsize=10)

        # Información adicional
        y_pos -= 1
        pf_type = results.get('pf_type', 'desconocido')
        ax.text(1, y_pos, f'Tipo de factor de potencia: {pf_type}', fontsize=10)

        y_pos -= 0.5
        connection = self.motor.connection
        ax.text(1, y_pos, f'Conexión: {connection}', fontsize=10)

    def _get_parameter_label(self, parameter: str) -> str:
        """Retorna etiqueta descriptiva para parámetros"""
        labels = {
            'V_line': 'Tensión de línea [V]',
            'f': 'Frecuencia [Hz]',
            'If': 'Corriente de excitación [A]',
            'T_load': 'Par de carga [N·m]',
            'Rs': 'Resistencia estator [Ω]',
            'Xd': 'Reactancia síncrona d [Ω]',
            'Xq': 'Reactancia síncrona q [Ω]',
            'J': 'Momento de inercia [kg·m²]',
            'B': 'Coeficiente de amortiguamiento [N·m·s/rad]'
        }
        return labels.get(parameter, parameter)

    def _get_variable_label(self, variable: str) -> str:
        """Retorna etiqueta descriptiva para variables"""
        labels = {
            'omega_m': 'Velocidad mecánica [rad/s]',
            'delta': 'Ángulo de carga [rad]',
            'delta_deg': 'Ángulo de carga [°]',
            'T_e': 'Par electromagnético [N·m]',
            'T_load': 'Par de carga [N·m]',
            'P': 'Potencia activa [W]',
            'Q': 'Potencia reactiva [VAR]',
            'S': 'Potencia aparente [VA]',
            'pf': 'Factor de potencia',
            'I_magnitude': 'Corriente de línea [A]',
            'V_line': 'Tensión de línea [V]',
            'f': 'Frecuencia [Hz]',
            'If': 'Corriente de excitación [A]'
        }
        return labels.get(variable, variable)

    def _create_torque_angle_curve_on_axes(self, ax) -> None:
        """
        Crea la curva par-ángulo en ejes existentes
        """
        # Generar datos de la curva
        stability_data = self.engine.stability_analysis()

        deltas_deg = np.degrees(stability_data['delta'])
        T_e = stability_data['T_e']

        # Graficar curva completa
        ax.plot(deltas_deg, T_e, 'b-', linewidth=2, label='Curva T_e(δ)')

        # Resaltar región estable (pendiente negativa)
        stable_mask = stability_data['stable_region']
        if np.any(stable_mask):
            ax.fill_between(deltas_deg[stable_mask], T_e[stable_mask],
                          alpha=0.3, color='green', label='Región estable')

        # Marcar punto de operación actual
        current_results = self.motor.steady_state_analysis()
        current_delta_deg = current_results['delta_deg']
        current_T_e = current_results['T_e']

        ax.plot(current_delta_deg, current_T_e, 'ro', markersize=8,
               label=f'Punto operación (δ={current_delta_deg:.1f}°, T_e={current_T_e:.1f} N·m)')

        # Marcar par máximo
        T_max = stability_data['T_max']
        delta_max_deg = np.degrees(stability_data['delta_max'])
        ax.plot(delta_max_deg, T_max, 'k*', markersize=10,
               label=f'Par máximo (δ={delta_max_deg:.1f}°, T_max={T_max:.1f} N·m)')

        # Configurar gráfico
        ax.set_xlabel('Ángulo de carga δ [°]')
        ax.set_ylabel('Par electromagnético T_e [N·m]')
        ax.set_title('Curva Característica Par-Ángulo del Motor Síncrono')
        ax.grid(True, alpha=0.3)
        ax.legend()

        # Añadir líneas de referencia
        ax.axhline(y=0, color='k', linestyle='--', alpha=0.5)
        ax.axvline(x=0, color='k', linestyle='--', alpha=0.5)

    def _create_power_factor_plot_on_axes(self, ax) -> None:
        """
        Crea el gráfico de factor de potencia vs excitación en ejes existentes
        """
        # Generar datos
        If_values, pf_values, pf_types = self.motor.power_factor_vs_excitation()

        # Separar por tipo de factor de potencia
        inductive_mask = np.array([t == 'inductivo' for t in pf_types])
        capacitive_mask = np.array([t == 'capacitivo' for t in pf_types])

        # Graficar
        ax.plot(If_values[inductive_mask], pf_values[inductive_mask],
               'b-', linewidth=2, label='Factor inductivo')
        ax.plot(If_values[capacitive_mask], pf_values[capacitive_mask],
               'r-', linewidth=2, label='Factor capacitivo')

        # Marcar punto de operación actual
        ax.plot(self.motor.If, self.motor.steady_state_analysis()['pf'],
               'ko', markersize=8, label='Punto actual')

        # Líneas de referencia
        ax.axhline(y=1.0, color='k', linestyle='--', alpha=0.5, label='Factor unidad')
        ax.axvline(x=self.motor.If, color='k', linestyle=':', alpha=0.5)

        # Región subexcitada (izquierda del punto unidad)
        unity_pf_If = If_values[np.argmin(np.abs(pf_values - 1.0))]
        ax.axvspan(If_values[0], unity_pf_If, alpha=0.2, color='blue',
                  label='Región subexcitada')

        # Región sobreexcitada (derecha del punto unidad)
        ax.axvspan(unity_pf_If, If_values[-1], alpha=0.2, color='red',
                  label='Región sobreexcitada')

        # Configurar gráfico
        ax.set_xlabel('Corriente de excitación I_f [A]')
        ax.set_ylabel('Factor de potencia')
        ax.set_title('Factor de Potencia vs Corriente de Excitación')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_ylim(0.8, 1.05)

    def _create_parameter_sweep_plot_on_axes(self, ax, parameter: str,
                                           value_range: Tuple[float, float],
                                           target_variable: str) -> None:
        """
        Crea gráfico de barrido de parámetros en ejes existentes
        """
        # Realizar barrido
        sweep_results = self.engine.parameter_sweep(parameter, value_range, num_points=20)

        # Extraer datos
        param_values = [r[f'parameter_{parameter}'] for r in sweep_results]
        target_values = [r[target_variable] for r in sweep_results]

        # Graficar
        ax.plot(param_values, target_values, 'b-o', linewidth=2, markersize=4)

        # Marcar punto actual
        current_value = getattr(self.motor, parameter)
        current_results = self.motor.steady_state_analysis()
        current_target = current_results[target_variable]

        ax.plot(current_value, current_target, 'ro', markersize=8,
               label=f'Punto actual ({parameter}={current_value:.2f}, {target_variable}={current_target:.2f})')

        # Configurar gráfico
        param_label = self._get_parameter_label(parameter)
        target_label = self._get_variable_label(target_variable)

        ax.set_xlabel(f'{param_label}')
        ax.set_ylabel(f'{target_label}')
        ax.set_title(f'{target_label} vs {param_label}')
        ax.grid(True, alpha=0.3)
        ax.legend()
