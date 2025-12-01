"""
Interfaz gráfica principal para el simulador de motor síncrono

Implementa una interfaz completa con:
- Controles para ajustar parámetros
- Visualización en tiempo real
- Gráficos interactivos
- Escenarios preconfigurados
"""

import sys
import numpy as np
from typing import Dict, List, Optional, Any
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QSlider, QDoubleSpinBox, QPushButton,
    QComboBox, QGroupBox, QTabWidget, QTextEdit, QSplitter,
    QProgressBar, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QPalette, QColor

# Importaciones de matplotlib para embeber gráficos
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# Importaciones del simulador
from motor_model import SynchronousMotorModel
from simulation_engine import SimulationEngine
from scenarios import SimulationScenarios
from plots import MotorPlots
from phasor_diagram import PhasorDiagram


class MotorSimulatorGUI(QMainWindow):
    """
    Interfaz gráfica principal del simulador de motor síncrono
    """

    def __init__(self):
        super().__init__()

        # Inicializar componentes del simulador
        self.motor = SynchronousMotorModel()
        self.engine = SimulationEngine(self.motor)
        self.scenarios = SimulationScenarios(self.motor)
        self.plots = MotorPlots(self.motor)
        self.phasor_diagram = PhasorDiagram(self.motor)

        # Estado de la interfaz
        self.current_scenario = None
        self.is_simulating = False

        # Configurar interfaz
        self.init_ui()
        self.connect_signals()
        self.update_display()

    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle('Simulador de Motor Síncrono Trifásico')
        self.setGeometry(100, 100, 1400, 900)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QHBoxLayout(central_widget)

        # Splitter para dividir la interfaz
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Panel izquierdo: controles
        self.control_panel = self.create_control_panel()
        splitter.addWidget(self.control_panel)

        # Panel derecho: visualizaciones
        self.visualization_panel = self.create_visualization_panel()
        splitter.addWidget(self.visualization_panel)

        # Ajustar proporciones
        splitter.setSizes([400, 1000])

        main_layout.addWidget(splitter)

        # Barra de estado
        self.statusBar().showMessage('Listo')

        # Timer para actualizaciones en tiempo real
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(500)  # Actualizar cada 500ms

    def create_control_panel(self) -> QWidget:
        """Crea el panel de controles"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Título
        title = QLabel('Controles del Simulador')
        title.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        layout.addWidget(title)

        # Tabs para organizar controles
        tabs = QTabWidget()

        # Tab 1: Parámetros del motor
        motor_tab = self.create_motor_parameters_tab()
        tabs.addTab(motor_tab, 'Parámetros')

        # Tab 2: Variables de operación
        operation_tab = self.create_operation_parameters_tab()
        tabs.addTab(operation_tab, 'Operación')

        # Tab 3: Escenarios
        scenarios_tab = self.create_scenarios_tab()
        tabs.addTab(scenarios_tab, 'Escenarios')

        layout.addWidget(tabs)

        # Botón de reset
        reset_btn = QPushButton('Reset a Valores por Defecto')
        reset_btn.clicked.connect(self.reset_parameters)
        layout.addWidget(reset_btn)

        return panel

    def create_motor_parameters_tab(self) -> QWidget:
        """Crea la pestaña de parámetros del motor"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Grupo: Parámetros eléctricos
        electrical_group = QGroupBox('Parámetros Eléctricos')
        electrical_layout = QGridLayout(electrical_group)

        # Rs
        electrical_layout.addWidget(QLabel('Rs [Ω]:'), 0, 0)
        self.rs_spin = QDoubleSpinBox()
        self.rs_spin.setRange(0.01, 10.0)
        self.rs_spin.setValue(self.motor.Rs)
        self.rs_spin.setSingleStep(0.1)
        electrical_layout.addWidget(self.rs_spin, 0, 1)

        # Xd
        electrical_layout.addWidget(QLabel('Xd [Ω]:'), 1, 0)
        self.xd_spin = QDoubleSpinBox()
        self.xd_spin.setRange(0.1, 50.0)
        self.xd_spin.setValue(self.motor.Xd)
        self.xd_spin.setSingleStep(0.5)
        electrical_layout.addWidget(self.xd_spin, 1, 1)

        # Xq
        electrical_layout.addWidget(QLabel('Xq [Ω]:'), 2, 0)
        self.xq_spin = QDoubleSpinBox()
        self.xq_spin.setRange(0.1, 50.0)
        self.xq_spin.setValue(self.motor.Xq)
        self.xq_spin.setSingleStep(0.5)
        electrical_layout.addWidget(self.xq_spin, 2, 1)

        layout.addWidget(electrical_group)

        # Grupo: Parámetros mecánicos
        mechanical_group = QGroupBox('Parámetros Mecánicos')
        mechanical_layout = QGridLayout(mechanical_group)

        # J
        mechanical_layout.addWidget(QLabel('J [kg·m²]:'), 0, 0)
        self.j_spin = QDoubleSpinBox()
        self.j_spin.setRange(0.01, 10.0)
        self.j_spin.setValue(self.motor.J)
        self.j_spin.setSingleStep(0.1)
        mechanical_layout.addWidget(self.j_spin, 0, 1)

        # B
        mechanical_layout.addWidget(QLabel('B [N·m·s/rad]:'), 1, 0)
        self.b_spin = QDoubleSpinBox()
        self.b_spin.setRange(0.0, 1.0)
        self.b_spin.setValue(self.motor.B)
        self.b_spin.setSingleStep(0.01)
        mechanical_layout.addWidget(self.b_spin, 1, 1)

        # p
        mechanical_layout.addWidget(QLabel('Polos (p):'), 2, 0)
        self.p_combo = QComboBox()
        self.p_combo.addItems(['2', '4', '6', '8', '10'])
        self.p_combo.setCurrentText(str(self.motor.p))
        mechanical_layout.addWidget(self.p_combo, 2, 1)

        layout.addWidget(mechanical_group)

        layout.addStretch()
        return tab

    def create_operation_parameters_tab(self) -> QWidget:
        """Crea la pestaña de parámetros de operación"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Grupo: Variables de entrada
        input_group = QGroupBox('Variables de Operación')
        input_layout = QGridLayout(input_group)

        # V_line
        input_layout.addWidget(QLabel('V_line [V]:'), 0, 0)
        self.v_line_spin = QDoubleSpinBox()
        self.v_line_spin.setRange(100, 1000)
        self.v_line_spin.setValue(self.motor.V_line)
        self.v_line_spin.setSingleStep(10)
        input_layout.addWidget(self.v_line_spin, 0, 1)

        # f
        input_layout.addWidget(QLabel('f [Hz]:'), 1, 0)
        self.f_spin = QDoubleSpinBox()
        self.f_spin.setRange(25, 100)
        self.f_spin.setValue(self.motor.f)
        self.f_spin.setSingleStep(1)
        input_layout.addWidget(self.f_spin, 1, 1)

        # If
        input_layout.addWidget(QLabel('I_f [A]:'), 2, 0)
        self.if_slider = QSlider(Qt.Orientation.Horizontal)
        self.if_slider.setRange(0, 1000)  # 0-10 A con 2 decimales
        self.if_slider.setValue(int(self.motor.If * 100))
        input_layout.addWidget(self.if_slider, 2, 1)

        self.if_spin = QDoubleSpinBox()
        self.if_spin.setRange(0.0, 10.0)
        self.if_spin.setValue(self.motor.If)
        self.if_spin.setSingleStep(0.1)
        input_layout.addWidget(self.if_spin, 2, 2)

        # T_load
        input_layout.addWidget(QLabel('T_load [N·m]:'), 3, 0)
        self.t_load_slider = QSlider(Qt.Orientation.Horizontal)
        self.t_load_slider.setRange(0, 200)  # 0-20 N·m con 1 decimal
        self.t_load_slider.setValue(int(self.motor.T_load * 10))
        input_layout.addWidget(self.t_load_slider, 3, 1)

        self.t_load_spin = QDoubleSpinBox()
        self.t_load_spin.setRange(0.0, 20.0)
        self.t_load_spin.setValue(self.motor.T_load)
        self.t_load_spin.setSingleStep(0.1)
        input_layout.addWidget(self.t_load_spin, 3, 2)

        # Conexión
        input_layout.addWidget(QLabel('Conexión:'), 4, 0)
        self.connection_combo = QComboBox()
        self.connection_combo.addItems(['star', 'delta'])
        self.connection_combo.setCurrentText(self.motor.connection)
        input_layout.addWidget(self.connection_combo, 4, 1)

        layout.addWidget(input_group)

        # Grupo: Información calculada
        output_group = QGroupBox('Variables Calculadas')
        output_layout = QGridLayout(output_group)

        # Labels para mostrar resultados
        self.labels = {}
        variables = [
            ('omega_s', 'ω_s [rad/s]'),
            ('n_s', 'n_s [RPM]'),
            ('delta_deg', 'δ [°]'),
            ('I_magnitude', 'I [A]'),
            ('P', 'P [W]'),
            ('Q', 'Q [VAR]'),
            ('S', 'S [VA]'),
            ('pf', 'cosφ'),
            ('pf_type', 'Tipo FP'),
            ('T_e', 'T_e [N·m]')
        ]

        for i, (var, label) in enumerate(variables):
            output_layout.addWidget(QLabel(f'{label}:'), i, 0)
            self.labels[var] = QLabel('0.00')
            self.labels[var].setFont(QFont('Courier', 10))
            output_layout.addWidget(self.labels[var], i, 1)

        layout.addWidget(output_group)

        layout.addStretch()
        return tab

    def create_scenarios_tab(self) -> QWidget:
        """Crea la pestaña de escenarios preconfigurados"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Selector de escenario
        scenario_group = QGroupBox('Escenarios Preconfigurados')
        scenario_layout = QVBoxLayout(scenario_group)

        self.scenario_combo = QComboBox()
        self.scenario_combo.addItems(self.scenarios.get_available_scenarios())
        scenario_layout.addWidget(self.scenario_combo)

        # Descripción del escenario
        self.scenario_description = QTextEdit()
        self.scenario_description.setMaximumHeight(100)
        self.scenario_description.setReadOnly(True)
        scenario_layout.addWidget(self.scenario_description)

        # Botón ejecutar escenario
        self.run_scenario_btn = QPushButton('Ejecutar Escenario')
        self.run_scenario_btn.clicked.connect(self.run_selected_scenario)
        scenario_layout.addWidget(self.run_scenario_btn)

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        scenario_layout.addWidget(self.progress_bar)

        layout.addWidget(scenario_group)

        # Grupo: Información del escenario actual
        current_group = QGroupBox('Escenario Actual')
        current_layout = QVBoxLayout(current_group)

        self.current_scenario_label = QLabel('Ninguno')
        current_layout.addWidget(self.current_scenario_label)

        layout.addWidget(current_group)

        layout.addStretch()
        return tab

    def create_visualization_panel(self) -> QWidget:
        """Crea el panel de visualizaciones"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Tabs para diferentes visualizaciones
        self.viz_tabs = QTabWidget()

        # Tab 1: Estado actual
        status_tab = self.create_status_tab()
        self.viz_tabs.addTab(status_tab, 'Estado')

        # Tab 2: Diagrama fasorial
        phasor_tab = self.create_phasor_tab()
        self.viz_tabs.addTab(phasor_tab, 'Fasores')

        # Tab 3: Curvas características
        curves_tab = self.create_curves_tab()
        self.viz_tabs.addTab(curves_tab, 'Curvas')

        # Tab 4: Simulación temporal
        temporal_tab = self.create_temporal_tab()
        self.viz_tabs.addTab(temporal_tab, 'Temporal')

        layout.addWidget(self.viz_tabs)

        return panel

    def create_status_tab(self) -> QWidget:
        """Crea la pestaña de estado actual"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Canvas para matplotlib
        self.status_canvas = FigureCanvas(Figure(figsize=(8, 6)))
        layout.addWidget(self.status_canvas)

        # Toolbar
        toolbar = NavigationToolbar(self.status_canvas, tab)
        layout.addWidget(toolbar)

        return tab

    def create_phasor_tab(self) -> QWidget:
        """Crea la pestaña del diagrama fasorial"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Canvas para el diagrama fasorial
        self.phasor_canvas = FigureCanvas(Figure(figsize=(8, 8)))
        layout.addWidget(self.phasor_canvas)

        # Toolbar
        toolbar = NavigationToolbar(self.phasor_canvas, tab)
        layout.addWidget(toolbar)

        # Controles específicos del fasor
        controls_layout = QHBoxLayout()

        self.animate_phasor_btn = QPushButton('Animar If')
        self.animate_phasor_btn.clicked.connect(self.animate_phasor_diagram)
        controls_layout.addWidget(self.animate_phasor_btn)

        layout.addLayout(controls_layout)

        return tab

    def create_curves_tab(self) -> QWidget:
        """Crea la pestaña de curvas características"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Canvas para curvas
        self.curves_canvas = FigureCanvas(Figure(figsize=(8, 6)))
        layout.addWidget(self.curves_canvas)

        # Toolbar
        toolbar = NavigationToolbar(self.curves_canvas, tab)
        layout.addWidget(toolbar)

        # Selector de curva
        controls_layout = QHBoxLayout()

        controls_layout.addWidget(QLabel('Tipo de curva:'))
        self.curve_type_combo = QComboBox()
        self.curve_type_combo.addItems([
            'Par-Ángulo',
            'Factor de Potencia vs If',
            'P vs If',
            'Eficiencia vs Carga'
        ])
        self.curve_type_combo.currentTextChanged.connect(self.update_curves_plot)
        controls_layout.addWidget(self.curve_type_combo)

        layout.addLayout(controls_layout)

        return tab

    def create_temporal_tab(self) -> QWidget:
        """Crea la pestaña de simulación temporal"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Canvas para gráficos temporales
        self.temporal_canvas = FigureCanvas(Figure(figsize=(8, 6)))
        layout.addWidget(self.temporal_canvas)

        # Toolbar
        toolbar = NavigationToolbar(self.temporal_canvas, tab)
        layout.addWidget(toolbar)

        return tab

    def connect_signals(self):
        """Conecta las señales de los controles"""
        # Parámetros eléctricos
        self.rs_spin.valueChanged.connect(lambda: self.update_parameter('Rs', self.rs_spin.value()))
        self.xd_spin.valueChanged.connect(lambda: self.update_parameter('Xd', self.xd_spin.value()))
        self.xq_spin.valueChanged.connect(lambda: self.update_parameter('Xq', self.xq_spin.value()))

        # Parámetros mecánicos
        self.j_spin.valueChanged.connect(lambda: self.update_parameter('J', self.j_spin.value()))
        self.b_spin.valueChanged.connect(lambda: self.update_parameter('B', self.b_spin.value()))
        self.p_combo.currentTextChanged.connect(lambda: self.update_parameter('p', int(self.p_combo.currentText())))

        # Variables de operación
        self.v_line_spin.valueChanged.connect(lambda: self.update_parameter('V_line', self.v_line_spin.value()))
        self.f_spin.valueChanged.connect(lambda: self.update_parameter('f', self.f_spin.value()))

        # Sliders con spins
        self.if_slider.valueChanged.connect(lambda: self.if_spin.setValue(self.if_slider.value() / 100))
        self.if_spin.valueChanged.connect(self.update_if_from_spin)

        self.t_load_slider.valueChanged.connect(lambda: self.t_load_spin.setValue(self.t_load_slider.value() / 10))
        self.t_load_spin.valueChanged.connect(self.update_t_load_from_spin)

        self.connection_combo.currentTextChanged.connect(lambda: self.update_parameter('connection', self.connection_combo.currentText()))

        # Escenarios
        self.scenario_combo.currentTextChanged.connect(self.update_scenario_description)

    def update_parameter(self, param: str, value: Any):
        """Actualiza un parámetro del motor"""
        setattr(self.motor, param, value)
        self.update_display()

    def update_if_from_spin(self):
        """Actualiza el slider de If desde el spin box"""
        self.if_slider.blockSignals(True)
        self.if_slider.setValue(int(self.if_spin.value() * 100))
        self.if_slider.blockSignals(False)
        self.update_parameter('If', self.if_spin.value())

    def update_t_load_from_spin(self):
        """Actualiza el slider de T_load desde el spin box"""
        self.t_load_slider.blockSignals(True)
        self.t_load_slider.setValue(int(self.t_load_spin.value() * 10))
        self.t_load_slider.blockSignals(False)
        self.update_parameter('T_load', self.t_load_spin.value())

    def update_display(self):
        """Actualiza todas las visualizaciones"""
        try:
            # Calcular estado actual
            results = self.motor.steady_state_analysis()

            # Actualizar labels numéricos
            for var, label in self.labels.items():
                value = results.get(var, 0)
                if var in ['P', 'Q', 'S']:
                    label.setText('.1f')
                elif var == 'pf':
                    label.setText('.3f')
                elif var == 'pf_type':
                    label.setText(str(value))
                else:
                    label.setText('.2f')

            # Actualizar gráficos
            self.update_status_plot()
            self.update_phasor_plot()
            self.update_curves_plot()

        except Exception as e:
            print(f"Error actualizando display: {e}")

    def update_status_plot(self):
        """Actualiza el gráfico de estado"""
        self.status_canvas.figure.clear()
        ax = self.status_canvas.figure.add_subplot(111)
        results = self.motor.steady_state_analysis()
        # Create the plot directly on the existing axes instead of creating a new figure
        self.plots._create_motor_status_display_on_axes(ax, results)
        self.status_canvas.draw()

    def update_phasor_plot(self):
        """Actualiza el diagrama fasorial"""
        self.phasor_canvas.figure.clear()
        ax = self.phasor_canvas.figure.add_subplot(111)
        # Create the phasor diagram on existing axes instead of creating new figure
        self.phasor_diagram._create_phasor_diagram_on_axes(ax)
        self.phasor_diagram._plot_phasors_on_axes(ax)
        self.phasor_canvas.draw()

    def update_curves_plot(self):
        """Actualiza las curvas características"""
        self.curves_canvas.figure.clear()
        ax = self.curves_canvas.figure.add_subplot(111)

        curve_type = self.curve_type_combo.currentText()

        if curve_type == 'Par-Ángulo':
            self.plots._create_torque_angle_curve_on_axes(ax)
        elif curve_type == 'Factor de Potencia vs If':
            self.plots._create_power_factor_plot_on_axes(ax)
        elif curve_type == 'P vs If':
            self.plots._create_parameter_sweep_plot_on_axes(ax, 'If', (0.1, 5.0), 'P')
        elif curve_type == 'Eficiencia vs Carga':
            # Placeholder - implementar eficiencia
            ax.text(0.5, 0.5, 'Gráfico de eficiencia\n(no implementado aún)',
                   ha='center', va='center', transform=ax.transAxes)

        self.curves_canvas.draw()

    def update_scenario_description(self):
        """Actualiza la descripción del escenario seleccionado"""
        scenario = self.scenario_combo.currentText()
        description = self.scenarios.get_scenario_description(scenario)
        self.scenario_description.setText(description)

    def run_selected_scenario(self):
        """Ejecuta el escenario seleccionado"""
        scenario_name = self.scenario_combo.currentText()

        try:
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminado
            self.run_scenario_btn.setEnabled(False)
            self.statusBar().showMessage(f'Ejecutando escenario: {scenario_name}')

            # Ejecutar escenario
            results = self.scenarios.run_scenario(scenario_name)

            # Mostrar resultados
            if 'time' in results:
                self.display_temporal_results(results)
            else:
                self.display_scenario_results(results)

            self.current_scenario = scenario_name
            self.current_scenario_label.setText(scenario_name)
            self.statusBar().showMessage(f'Escenario {scenario_name} completado')

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error ejecutando escenario:\n{str(e)}')
        finally:
            self.progress_bar.setVisible(False)
            self.run_scenario_btn.setEnabled(True)

    def display_temporal_results(self, results: Dict[str, Any]):
        """Muestra resultados de simulación temporal"""
        self.temporal_canvas.figure.clear()
        self.plots.create_transient_plots(results, figsize=(8, 6))
        self.temporal_canvas.draw()
        self.viz_tabs.setCurrentIndex(3)  # Ir a pestaña temporal

    def display_scenario_results(self, results: Dict[str, Any]):
        """Muestra resultados de escenario no temporal"""
        # Mostrar en la pestaña de estado
        self.viz_tabs.setCurrentIndex(0)

    def animate_phasor_diagram(self):
        """Anima el diagrama fasorial"""
        try:
            # Crear animación
            anim = self.phasor_diagram.create_animated_diagram(
                'If', (0.5, 4.0), num_frames=20, interval=300
            )

            # Mostrar animación (esto requiere guardar como gif o similar)
            QMessageBox.information(self, 'Animación',
                                  'La animación se ha creado. Para ver la animación completa,\n'
                                  'use el método save() del objeto de animación.')

        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error creando animación:\n{str(e)}')

    def reset_parameters(self):
        """Resetea todos los parámetros a valores por defecto"""
        reply = QMessageBox.question(self, 'Confirmar Reset',
                                   '¿Desea resetear todos los parámetros a valores por defecto?',
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            # Recrear modelo con valores por defecto
            self.motor = SynchronousMotorModel()
            self.engine = SimulationEngine(self.motor)
            self.scenarios = SimulationScenarios(self.motor)
            self.plots = MotorPlots(self.motor)
            self.phasor_diagram = PhasorDiagram(self.motor)

            # Actualizar controles
            self.update_controls_from_model()
            self.update_display()
            self.statusBar().showMessage('Parámetros reseteados')

    def update_controls_from_model(self):
        """Actualiza todos los controles con los valores del modelo"""
        # Parámetros eléctricos
        self.rs_spin.setValue(self.motor.Rs)
        self.xd_spin.setValue(self.motor.Xd)
        self.xq_spin.setValue(self.motor.Xq)

        # Parámetros mecánicos
        self.j_spin.setValue(self.motor.J)
        self.b_spin.setValue(self.motor.B)
        self.p_combo.setCurrentText(str(self.motor.p))

        # Variables de operación
        self.v_line_spin.setValue(self.motor.V_line)
        self.f_spin.setValue(self.motor.f)
        self.if_spin.setValue(self.motor.If)
        self.t_load_spin.setValue(self.motor.T_load)
        self.connection_combo.setCurrentText(self.motor.connection)

    def closeEvent(self, event):
        """Evento de cierre de la aplicación"""
        self.update_timer.stop()
        event.accept()


def main():
    """Función principal para ejecutar la aplicación"""
    app = QApplication(sys.argv)

    # Estilo de la aplicación
    app.setStyle('Fusion')

    # Paleta oscura opcional
    # palette = QPalette()
    # palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    # palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    # app.setPalette(palette)

    # Crear y mostrar ventana principal
    window = MotorSimulatorGUI()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
