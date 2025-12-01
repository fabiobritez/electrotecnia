#!/usr/bin/env python3
"""
Ejemplo de uso del Simulador de Motor Síncrono Trifásico

Este archivo demuestra cómo usar las clases del simulador
de forma programática (sin interfaz gráfica).
"""

import numpy as np
import matplotlib.pyplot as plt
from motor_model import SynchronousMotorModel
from simulation_engine import SimulationEngine
from scenarios import SimulationScenarios
from plots import MotorPlots
from phasor_diagram import PhasorDiagram


def ejemplo_analisis_basico():
    """Ejemplo básico: análisis en régimen permanente"""
    print("=== Análisis Básico en Régimen Permanente ===")

    # Crear modelo del motor
    motor = SynchronousMotorModel()

    # Configurar parámetros
    motor.V_line = 400  # V
    motor.f = 50  # Hz
    motor.If = 2.0  # A
    motor.T_load = 15.0  # N·m
    motor.Xd = 4.0  # ohm
    motor.Xq = 3.0  # ohm

    # Realizar análisis
    results = motor.steady_state_analysis()

    # Mostrar resultados
    print(f"Tensión de línea: {results['V_line']} V")
    print(f"Corriente de excitación: {results['If']} A")
    print(f"Velocidad síncrona: {results['n_s']:.1f} RPM")
    print(f"Ángulo de carga: {results['delta_deg']:.2f}°")
    print(f"Corriente de línea: {results['I_magnitude']:.2f} A")
    print(f"Potencia activa: {results['P']/1000:.1f} kW")
    print(f"Potencia reactiva: {results['Q']/1000:.1f} kVAR")
    print(f"Factor de potencia: {results['pf']:.3f} ({results['pf_type']})")
    print(f"Par electromagnético: {results['T_e']:.1f} N·m")

    return results


def ejemplo_curva_par_angulo():
    """Ejemplo: generar curva característica par-ángulo"""
    print("\n=== Curva Característica Par-Ángulo ===")

    motor = SynchronousMotorModel()
    plots = MotorPlots(motor)

    # Crear gráfico
    fig = plots.create_torque_angle_curve()
    plt.savefig('curva_par_angulo.png', dpi=150, bbox_inches='tight')
    print("Gráfico guardado como 'curva_par_angulo.png'")

    return fig


def ejemplo_factor_potencia_vs_excitacion():
    """Ejemplo: curva de factor de potencia vs corriente de excitación"""
    print("\n=== Factor de Potencia vs Excitación ===")

    motor = SynchronousMotorModel()
    plots = MotorPlots(motor)

    # Crear gráfico
    fig = plots.create_power_factor_plot()
    plt.savefig('factor_potencia_vs_if.png', dpi=150, bbox_inches='tight')
    print("Gráfico guardado como 'factor_potencia_vs_if.png'")

    return fig


def ejemplo_simulacion_arranque():
    """Ejemplo: simulación de arranque del motor"""
    print("\n=== Simulación de Arranque ===")

    motor = SynchronousMotorModel()
    scenarios = SimulationScenarios(motor)

    # Ejecutar escenario de arranque
    results = scenarios.run_scenario('startup_ideal', t_final=2.0)

    print(f"Tiempo de simulación: {results['t_final']:.1f} s")
    print(f"Velocidad inicial: {results['omega_m'][0]:.2f} rad/s")
    print(f"Velocidad final: {results['omega_m'][-1]:.2f} rad/s")
    print(f"Velocidad síncrona: {motor.synchronous_speed():.2f} rad/s")

    # Crear gráfico temporal
    plots = MotorPlots(motor)
    fig = plots.create_transient_plots(results)
    plt.savefig('simulacion_arranque.png', dpi=150, bbox_inches='tight')
    print("Gráfico guardado como 'simulacion_arranque.png'")

    return results


def ejemplo_diagrama_fasorial():
    """Ejemplo: diagrama fasorial"""
    print("\n=== Diagrama Fasorial ===")

    motor = SynchronousMotorModel()
    phasor_diagram = PhasorDiagram(motor)

    # Guardar diagrama fasorial
    phasor_diagram.save_phasor_diagram('diagrama_fasorial.png')
    print("Diagrama guardado como 'diagrama_fasorial.png'")

    # Crear diagrama explicativo
    fig = phasor_diagram.create_phasor_explanation()
    plt.savefig('explicacion_fasorial.png', dpi=150, bbox_inches='tight')
    print("Explicación guardada como 'explicacion_fasorial.png'")


def ejemplo_barrido_parametros():
    """Ejemplo: barrido de parámetros"""
    print("\n=== Barrido de Parámetros ===")

    motor = SynchronousMotorModel()
    engine = SimulationEngine(motor)
    plots = MotorPlots(motor)

    # Barrer corriente de excitación
    sweep_results = engine.parameter_sweep('If', (0.5, 4.0), num_points=20)

    print("Resultados del barrido de If:")
    for i, result in enumerate(sweep_results[::3]):  # Mostrar cada 3 puntos
        If = result['parameter_If']
        pf = result['pf']
        P = result['P']
        print(".1f")

    # Crear gráfico del barrido
    fig = plots.create_parameter_sweep_plot('If', (0.5, 4.0), 'P')
    plt.savefig('barrido_potencia_vs_if.png', dpi=150, bbox_inches='tight')
    print("Gráfico guardado como 'barrido_potencia_vs_if.png'")

    return sweep_results


def ejemplo_analisis_estabilidad():
    """Ejemplo: análisis de estabilidad"""
    print("\n=== Análisis de Estabilidad ===")

    motor = SynchronousMotorModel()
    engine = SimulationEngine(motor)

    # Análisis de estabilidad
    stability_data = engine.stability_analysis()

    print("Análisis de estabilidad:")
    print(f"Par máximo: {stability_data['T_max']:.2f} N·m")
    print(f"Ángulo del par máximo: {np.degrees(stability_data['delta_max']):.1f}°")
    print(f"Región estable: |δ| < {np.degrees(stability_data['delta_max']):.1f}°")

    # Verificar estabilidad con carga actual
    results = motor.steady_state_analysis()
    current_delta = results['delta']
    is_stable = abs(current_delta) < stability_data['delta_max']

    print(f"Carga actual estable: {is_stable}")
    print(f"Ángulo actual: {np.degrees(current_delta):.1f}°")

    return stability_data


def main():
    """Función principal con todos los ejemplos"""
    print("Simulador de Motor Síncrono Trifásico - Ejemplos de Uso")
    print("=" * 60)

    try:
        # Ejecutar ejemplos
        results_basico = ejemplo_analisis_basico()
        fig_par_angulo = ejemplo_curva_par_angulo()
        fig_pf_if = ejemplo_factor_potencia_vs_excitacion()
        results_arranque = ejemplo_simulacion_arranque()
        ejemplo_diagrama_fasorial()
        sweep_results = ejemplo_barrido_parametros()
        stability_data = ejemplo_analisis_estabilidad()

        print("\n=== Resumen ===")
        print("Todos los ejemplos se ejecutaron correctamente.")
        print("Se generaron los siguientes archivos:")
        print("- curva_par_angulo.png")
        print("- factor_potencia_vs_if.png")
        print("- simulacion_arranque.png")
        print("- diagrama_fasorial.png")
        print("- explicacion_fasorial.png")
        print("- barrido_potencia_vs_if.png")

        print("\nPara ejecutar la interfaz gráfica completa:")
        print("python main.py")

    except Exception as e:
        print(f"Error ejecutando ejemplos: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Cerrar todas las figuras de matplotlib
        plt.close('all')


if __name__ == '__main__':
    main()
