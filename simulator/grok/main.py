#!/usr/bin/env python3
"""
Punto de entrada principal del Simulador de Motor Síncrono Trifásico

Este simulador educativo permite estudiar el comportamiento de motores
síncronos trifásicos tanto en régimen permanente como dinámico.
"""

import sys
import argparse
from pathlib import Path

# Añadir el directorio actual al path para importar módulos locales
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Simulador de Motor Síncrono Trifásico',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Ejecutar interfaz gráfica
  python main.py

  # Ejecutar con modo verbose
  python main.py --verbose

  # Mostrar información del sistema
  python main.py --info
        """
    )

    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Modo verbose con más información')
    parser.add_argument('--info', action='store_true',
                       help='Mostrar información del sistema y salir')

    args = parser.parse_args()

    if args.info:
        show_system_info()
        return

    if args.verbose:
        print("Iniciando Simulador de Motor Síncrono Trifásico...")
        print("Cargando módulos...")

    try:
        # Importar y ejecutar la interfaz gráfica
        from gui import main as gui_main

        if args.verbose:
            print("Interfaz gráfica cargada correctamente")
            print("Iniciando aplicación...")

        gui_main()

    except ImportError as e:
        print(f"Error importando módulos: {e}")
        print("Asegúrese de que todas las dependencias estén instaladas:")
        print("  pip install -r requirements.txt")
        sys.exit(1)

    except Exception as e:
        print(f"Error iniciando aplicación: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def show_system_info():
    """Muestra información del sistema"""
    print("=== Información del Sistema ===")
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")

    # Verificar dependencias
    print("\n=== Verificación de Dependencias ===")

    dependencies = [
        ('PyQt6', 'PyQt6.QtWidgets'),
        ('numpy', 'numpy'),
        ('matplotlib', 'matplotlib'),
        ('scipy', 'scipy')
    ]

    for name, module in dependencies:
        try:
            __import__(module)
            print(f"✓ {name}: OK")
        except ImportError:
            print(f"✗ {name}: NO ENCONTRADO")

    print("\n=== Información del Simulador ===")
    print("Simulador de Motor Síncrono Trifásico v1.0")
    print("Desarrollado para fines educativos")
    print("Soporta análisis en régimen permanente y dinámico")


if __name__ == '__main__':
    main()
