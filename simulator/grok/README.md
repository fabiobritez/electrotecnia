# Simulador de Motor Síncrono Trifásico

Este simulador interactivo permite estudiar el comportamiento de un motor síncrono trifásico tanto en régimen permanente como dinámico, con énfasis en las interrelaciones entre variables eléctricas y mecánicas.

## Instalación

### Requisitos del sistema
- Python 3.8 o superior
- Sistema operativo Linux/Windows/macOS

### Instalación de dependencias

```bash
# Instalar dependencias de Python
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

## Características principales

### Modelo implementado
- Motor síncrono trifásico con rotor de polos salientes
- Modelo fasorial para régimen permanente
- Modelo dinámico simplificado en ejes d-q
- Análisis de estabilidad y comportamiento transitorio

### Variables controlables
- Tensión de línea (V_L)
- Frecuencia eléctrica (f)
- Número de polos (p)
- Corriente de excitación del rotor (I_f)
- Par de carga mecánica (T_L)
- Parámetros eléctricos: R_s, X_d, X_q
- Parámetros mecánicos: J, B

### Visualizaciones
- Diagrama fasorial interactivo
- Curva característica par-ángulo (T_e vs δ)
- Evolución temporal de variables durante transitorios
- Gráfico de factor de potencia vs corriente de excitación

### Escenarios preconfigurados
1. **Arranque ideal**: Simulación del enganche a velocidad síncrona
2. **Carga creciente**: Aumento gradual del par de carga
3. **Cambio de excitación**: De subexcitado a sobreexcitado
4. **Sobrecarga**: Análisis de pérdida de sincronismo

## Manual de uso

### Interfaz principal
La interfaz se divide en tres paneles principales:

1. **Panel de parámetros**: Controles deslizantes y campos de texto para ajustar variables
2. **Panel de visualización**: Gráficos y diagramas que se actualizan en tiempo real
3. **Panel de resultados**: Display numérico de variables calculadas

### Experimentos sugeridos

#### 1. Efecto de la excitación en el factor de potencia
- Mantén V_L, f, T_L constantes
- Varía I_f desde valores bajos (subexcitado) a altos (sobreexcitado)
- Observa cómo cambia el factor de potencia de inductivo a capacitivo

#### 2. Estabilidad con carga variable
- Configura parámetros nominales
- Aumenta gradualmente T_L
- Observa el crecimiento del ángulo δ hasta el límite de estabilidad

#### 3. Análisis fasorial
- Modifica diferentes parámetros
- Estudia cómo se reorganizan los fasores V, E, I en el diagrama
- Relaciona los cambios con las ecuaciones fasoriales

### Interpretación de resultados

#### Diagrama fasorial
- **V**: Tensión de fase aplicada
- **E**: Fuerza electromotriz interna (proporcional a I_f)
- **I**: Corriente de línea
- **jX_s I**: Caída reactiva de tensión

#### Curva par-ángulo
Muestra la relación entre par electromagnético y ángulo de carga δ.
El punto de operación debe estar en la región estable (pendiente negativa).

## Modelo matemático

### Régimen permanente (fasorial)
```
V = E + j X_s I + R_s I
T_e = (3 V E / ω_s X_s) sinδ
P = 3 V_fase I_fase cosφ
Q = 3 V_fase I_fase sinφ
```

### Modelo dinámico (ejes d-q)
```
dω_m/dt = (T_e - T_L - B ω_m) / J
```

Donde ω_s = 2πf (velocidad síncrona).

## Limitaciones del modelo
- Modelo simplificado sin saturación magnética
- Pérdidas en el cobre consideradas constantes
- Sin efectos de amortiguamiento del rotor
- Amortiguador de polos no modelado

## Estructura del código

```
simulator/grok/
├── main.py              # Punto de entrada principal
├── motor_model.py       # Modelo matemático del motor síncrono
├── simulation_engine.py # Motor de simulación numérica
├── gui.py              # Interfaz gráfica principal (PyQt6)
├── phasor_diagram.py   # Visualización de diagramas fasoriales
├── plots.py            # Generador de gráficos y curvas
├── scenarios.py        # Escenarios de simulación preconfigurados
├── utils.py            # Utilidades matemáticas y conversiones
├── example_usage.py    # Ejemplos de uso programático
├── test_basic.py       # Pruebas básicas de funcionamiento
├── requirements.txt    # Dependencias de Python
└── README.md           # Esta documentación
```

## Archivos adicionales

### `example_usage.py`
Contiene ejemplos completos de uso programático del simulador, incluyendo:
- Análisis básico en régimen permanente
- Generación de curvas características
- Simulaciones temporales
- Diagramas fasoriales
- Barridos de parámetros

### `test_basic.py`
Script de pruebas que verifica:
- Importación correcta de todos los módulos
- Funcionamiento básico del modelo
- Disponibilidad de dependencias
- Ejecución sin errores de funciones principales

## Uso programático

Además de la interfaz gráfica, el simulador puede usarse programáticamente:

```python
from motor_model import SynchronousMotorModel
from simulation_engine import SimulationEngine

# Crear motor
motor = SynchronousMotorModel()
motor.V_line = 400  # V
motor.If = 2.0      # A

# Análisis en régimen permanente
results = motor.steady_state_analysis()
print(f"Potencia: {results['P']:.1f} W")
print(f"Factor de potencia: {results['pf']:.3f}")

# Simulación dinámica
engine = SimulationEngine(motor)
transient_results = engine.simulate_transient_response((0, 2.0))
```

## Verificación del funcionamiento

Para verificar que todo funciona correctamente:

```bash
# Ejecutar pruebas básicas
python test_basic.py

# Ejecutar ejemplos
python example_usage.py

# Iniciar interfaz gráfica
python main.py
```
