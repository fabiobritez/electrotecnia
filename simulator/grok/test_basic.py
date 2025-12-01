#!/usr/bin/env python3
"""
Pruebas básicas del simulador de motor síncrono

Verifica que todos los módulos se importan correctamente
y que las funciones básicas funcionan.
"""

import sys
import traceback
from pathlib import Path

# Añadir el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))


def test_imports():
    """Prueba que todos los módulos se importan correctamente"""
    print("Probando importaciones...")

    try:
        from motor_model import SynchronousMotorModel
        print("✓ motor_model importado correctamente")

        from simulation_engine import SimulationEngine
        print("✓ simulation_engine importado correctamente")

        from scenarios import SimulationScenarios
        print("✓ scenarios importado correctamente")

        from plots import MotorPlots
        print("✓ plots importado correctamente")

        from phasor_diagram import PhasorDiagram
        print("✓ phasor_diagram importado correctamente")

        from utils import polar_to_rectangular, synchronous_speed_rpm
        print("✓ utils importado correctamente")

        return True
    except ImportError as e:
        print(f"✗ Error de importación: {e}")
        return False


def test_motor_model():
    """Prueba básica del modelo del motor"""
    print("\nProbando modelo del motor...")

    try:
        from motor_model import SynchronousMotorModel

        # Crear motor
        motor = SynchronousMotorModel()
        print("✓ Motor creado correctamente")

        # Probar cálculo básico
        omega_s = motor.synchronous_speed()
        print(".2f")

        # Probar análisis en régimen permanente
        results = motor.steady_state_analysis()
        print("✓ Análisis en régimen permanente completado")
        print(".1f")

        return True
    except Exception as e:
        print(f"✗ Error en modelo del motor: {e}")
        traceback.print_exc()
        return False


def test_simulation_engine():
    """Prueba básica del motor de simulación"""
    print("\nProbando motor de simulación...")

    try:
        from motor_model import SynchronousMotorModel
        from simulation_engine import SimulationEngine

        motor = SynchronousMotorModel()
        engine = SimulationEngine(motor)
        print("✓ Motor de simulación creado correctamente")

        # Probar resolución de estado estacionario
        results = engine.solve_steady_state()
        print("✓ Estado estacionario resuelto")
        print(".2f")

        return True
    except Exception as e:
        print(f"✗ Error en motor de simulación: {e}")
        traceback.print_exc()
        return False


def test_scenarios():
    """Prueba básica de escenarios"""
    print("\nProbando escenarios...")

    try:
        from motor_model import SynchronousMotorModel
        from scenarios import SimulationScenarios

        motor = SynchronousMotorModel()
        scenarios = SimulationScenarios(motor)
        print("✓ Gestor de escenarios creado correctamente")

        # Listar escenarios disponibles
        available = scenarios.get_available_scenarios()
        print(f"✓ Escenarios disponibles: {len(available)}")
        print(f"  - {', '.join(available[:3])}{'...' if len(available) > 3 else ''}")

        return True
    except Exception as e:
        print(f"✗ Error en escenarios: {e}")
        traceback.print_exc()
        return False


def test_plots():
    """Prueba básica de gráficos (sin mostrar ventanas)"""
    print("\nProbando gráficos...")

    try:
        import matplotlib
        matplotlib.use('Agg')  # Backend no interactivo

        from motor_model import SynchronousMotorModel
        from plots import MotorPlots

        motor = SynchronousMotorModel()
        plots = MotorPlots(motor)
        print("✓ Generador de gráficos creado correctamente")

        # Probar creación de figura (sin guardar)
        fig = plots.create_torque_angle_curve()
        print("✓ Curva par-ángulo creada correctamente")

        # Cerrar figura para liberar memoria
        import matplotlib.pyplot as plt
        plt.close(fig)

        return True
    except Exception as e:
        print(f"✗ Error en gráficos: {e}")
        traceback.print_exc()
        return False


def test_utils():
    """Prueba funciones de utilidad"""
    print("\nProbando utilidades...")

    try:
        from utils import polar_to_rectangular, synchronous_speed_rpm, calculate_power_factor

        # Probar conversión polar-rectangular
        z = polar_to_rectangular(5.0, 30.0)
        print(f"✓ Conversión polar-rectangular: 5∠30° = {z:.2f}")

        # Probar cálculo de velocidad síncrona
        n_s = synchronous_speed_rpm(50, 4)
        print(f"✓ Velocidad síncrona: {n_s:.1f} RPM (50 Hz, 4 polos)")

        # Probar cálculo de factor de potencia
        pf, pf_type = calculate_power_factor(1000, 1200)
        print(f"✓ Factor de potencia: {pf:.3f} ({pf_type})")

        return True
    except Exception as e:
        print(f"✗ Error en utilidades: {e}")
        traceback.print_exc()
        return False


def test_dependencies():
    """Prueba que las dependencias externas están disponibles"""
    print("\nProbando dependencias...")

    dependencies = [
        ('numpy', None),          # Solo verificar que se puede importar
        ('scipy', None),          # Solo verificar que se puede importar
        ('matplotlib', None),     # Solo verificar que se puede importar
    ]

    all_ok = True

    for module_name, attr in dependencies:
        try:
            __import__(module_name)
            print(f"✓ {module_name} disponible")
        except ImportError:
            print(f"✗ {module_name} NO disponible")
            all_ok = False

    # PyQt6 es opcional para pruebas básicas
    try:
        import PyQt6.QtWidgets
        print("✓ PyQt6 disponible")
    except ImportError:
        print("⚠ PyQt6 NO disponible (necesario solo para interfaz gráfica)")

    return all_ok


def main():
    """Función principal de pruebas"""
    print("Pruebas Básicas del Simulador de Motor Síncrono")
    print("=" * 50)

    tests = [
        ("Dependencias", test_dependencies),
        ("Importaciones", test_imports),
        ("Utilidades", test_utils),
        ("Modelo del motor", test_motor_model),
        ("Motor de simulación", test_simulation_engine),
        ("Escenarios", test_scenarios),
        ("Gráficos", test_plots)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Error inesperado en {test_name}: {e}")
            results.append((test_name, False))

    # Resumen
    print("\n" + "=" * 50)
    print("RESUMEN DE PRUEBAS")

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✓ PASÓ" if result else "✗ FALLÓ"
        print(f"{test_name}: {status}")
        if result:
            passed += 1

    print(f"\nPruebas pasadas: {passed}/{total}")

    if passed == total:
        print("🎉 Todas las pruebas pasaron correctamente!")
        print("\nPara ejecutar la interfaz gráfica:")
        print("python main.py")
        print("\nPara ver ejemplos de uso:")
        print("python example_usage.py")
        return 0
    else:
        print("❌ Algunas pruebas fallaron.")
        print("Verifique que todas las dependencias estén instaladas:")
        print("pip install -r requirements.txt")
        return 1


if __name__ == '__main__':
    sys.exit(main())
