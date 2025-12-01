"""
Visualización de diagramas fasoriales para el motor síncrono

Implementa:
- Diagrama fasorial interactivo con fasores V, E, I
- Representación gráfica de caídas de tensión
- Animación de cambios en tiempo real
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.patches import Arc, FancyArrowPatch
from typing import Dict, Tuple, Optional, List
import matplotlib.animation as animation
from motor_model import SynchronousMotorModel
from utils import polar_to_rectangular, rectangular_to_polar


class PhasorDiagram:
    """
    Generador de diagramas fasoriales para análisis del motor síncrono
    """

    def __init__(self, motor_model: SynchronousMotorModel):
        self.motor = motor_model

        # Configuración visual
        self.scale_factor = 100  # Escala para visualizar los fasores
        self.arrow_width = 0.02
        self.arrow_head_width = 0.05
        self.arrow_head_length = 0.05

        # Colores para diferentes fasores
        self.colors = {
            'V': '#1f77b4',      # Azul: tensión
            'E': '#ff7f0e',      # Naranja: FEM interna
            'I': '#2ca02c',      # Verde: corriente
            'jXsI': '#d62728',   # Rojo: caída reactiva
            'RsI': '#9467bd',    # Morado: caída resistiva
            'reference': '#7f7f7f'  # Gris: referencia
        }

    def create_phasor_diagram(self, figsize: Tuple[float, float] = (8, 8)) -> Tuple[Figure, Axes]:
        """
        Crea un diagrama fasorial básico con los fasores principales
        """
        fig, ax = plt.subplots(figsize=figsize)

        # Configurar el gráfico como círculo unitario
        ax.set_aspect('equal')
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)

        # Dibujar círculo de referencia
        circle = plt.Circle((0, 0), 1, fill=False, color='lightgray', linestyle='--', alpha=0.5)
        ax.add_patch(circle)

        # Ejes coordenados
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)

        # Etiquetas de ángulos
        for angle in [0, 90, 180, 270]:
            rad_angle = np.radians(angle)
            x_text = 1.2 * np.cos(rad_angle)
            y_text = 1.2 * np.sin(rad_angle)
            ax.text(x_text, y_text, f'{angle}°', ha='center', va='center', fontsize=8)

        # Título
        ax.set_title('Diagrama Fasorial del Motor Síncrono', fontsize=12, pad=20)
        ax.set_xlabel('Parte Real')
        ax.set_ylabel('Parte Imaginaria')

        return fig, ax

    def plot_phasors(self, ax: Axes, results: Optional[Dict[str, float]] = None) -> None:
        """
        Dibuja los fasores principales en el diagrama

        Args:
            ax: Ejes donde dibujar
            results: Resultados del análisis (si None, calcula automáticamente)
        """
        if results is None:
            results = self.motor.steady_state_analysis()

        # Obtener magnitudes y ángulos
        V_magnitude = results.get('V_phase', self.motor.phase_voltage()) / self.scale_factor
        E_magnitude = results.get('E_magnitude', 0) / self.scale_factor
        I_magnitude = results.get('I_magnitude', 0) / self.scale_factor

        V_angle = 0  # Referencia
        I_angle = results.get('I_angle', 0)
        delta = results.get('delta', 0)

        # Crear fasores como números complejos normalizados
        V_phasor = polar_to_rectangular(V_magnitude, V_angle)
        E_phasor = polar_to_rectangular(E_magnitude, np.degrees(delta))
        I_phasor = polar_to_rectangular(I_magnitude, I_angle)

        # Limpiar fasores anteriores
        self._clear_phasors(ax)

        # Dibujar fasores
        self._draw_phasor(ax, V_phasor, 'V', self.colors['V'], label_text='Tensión V')
        self._draw_phasor(ax, E_phasor, 'E', self.colors['E'], label_text='FEM interna E')
        self._draw_phasor(ax, I_phasor, 'I', self.colors['I'], label_text='Corriente I')

        # Dibujar caídas de tensión (opcional)
        self._draw_voltage_drops(ax, V_phasor, E_phasor, I_phasor)

        # Añadir leyenda
        ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))

    def _draw_phasor(self, ax: Axes, phasor: complex, label: str,
                    color: str, label_text: str = None) -> None:
        """
        Dibuja un fasor individual en el diagrama
        """
        # Coordenadas del fasor
        x, y = phasor.real, phasor.imag

        # Dibujar flecha
        arrow = FancyArrowPatch((0, 0), (x, y),
                               arrowstyle='->',
                               color=color,
                               linewidth=2,
                               mutation_scale=15,
                               label=label_text or label)
        ax.add_patch(arrow)

        # Etiqueta del fasor
        # Posición de la etiqueta (ligeramente desplazada del extremo)
        label_offset = 0.1
        angle = np.angle(phasor)
        label_x = x + label_offset * np.cos(angle)
        label_y = y + label_offset * np.sin(angle)

        ax.text(label_x, label_y, label, fontsize=10, fontweight='bold',
               ha='center', va='center', color=color)

        # Mostrar magnitud y ángulo
        magnitude, angle_deg = rectangular_to_polar(phasor)
        info_text = '.1f'
        info_x = x * 0.7
        info_y = y * 0.7
        ax.text(info_x, info_y, info_text, fontsize=8, color=color,
               ha='center', va='center', bbox=dict(boxstyle='round,pad=0.2',
               facecolor='white', alpha=0.8))

    def _draw_voltage_drops(self, ax: Axes, V_phasor: complex,
                           E_phasor: complex, I_phasor: complex) -> None:
        """
        Dibuja las caídas de tensión en el diagrama fasorial

        V = E + Rs*I + j*Xs*I
        """
        # Calcular caídas
        Rs = self.motor.Rs
        Xs_avg = (self.motor.Xd + self.motor.Xq) / 2

        RsI = complex(Rs, 0) * I_phasor
        jXsI = complex(0, Xs_avg) * I_phasor

        # Escalar para visualización
        scale = 1 / self.scale_factor
        RsI_scaled = RsI * scale
        jXsI_scaled = jXsI * scale

        # Dibujar Rs*I (caída resistiva)
        if abs(RsI_scaled) > 0.01:
            start_point = E_phasor
            end_point = E_phasor + RsI_scaled
            self._draw_phasor_component(ax, start_point, end_point,
                                      'RsI', self.colors['RsI'], 'Rs·I')

        # Dibujar jXs*I (caída reactiva)
        if abs(jXsI_scaled) > 0.01:
            start_point = E_phasor + RsI_scaled
            end_point = V_phasor
            self._draw_phasor_component(ax, start_point, end_point,
                                      'jXsI', self.colors['jXsI'], 'j·Xs·I')

    def _draw_phasor_component(self, ax: Axes, start: complex, end: complex,
                              label: str, color: str, label_text: str) -> None:
        """
        Dibuja un componente del fasor (como Rs*I o jXs*I)
        """
        x_start, y_start = start.real, start.imag
        x_end, y_end = end.real, end.imag

        # Dibujar línea
        ax.plot([x_start, x_end], [y_start, y_end], color=color,
               linewidth=1.5, linestyle='--')

        # Dibujar flecha pequeña
        dx, dy = x_end - x_start, y_end - y_start
        arrow = FancyArrowPatch((x_start, y_start), (x_end, y_end),
                               arrowstyle='->',
                               color=color,
                               linewidth=1.5,
                               mutation_scale=10)
        ax.add_patch(arrow)

        # Etiqueta
        mid_x, mid_y = (x_start + x_end) / 2, (y_start + y_end) / 2
        ax.text(mid_x, mid_y, label_text, fontsize=8, color=color,
               ha='center', va='center',
               bbox=dict(boxstyle='round,pad=0.1', facecolor='white', alpha=0.8))

    def update_phasor_diagram(self, ax: Axes, parameter: str, value: float) -> None:
        """
        Actualiza el diagrama fasorial al cambiar un parámetro

        Args:
            ax: Ejes del diagrama
            parameter: Parámetro que cambió
            value: Nuevo valor del parámetro
        """
        # Actualizar el modelo
        setattr(self.motor, parameter, value)

        # Recalcular y redibujar
        self.plot_phasors(ax)

    def create_animated_diagram(self, parameter: str, value_range: Tuple[float, float],
                               num_frames: int = 30, interval: int = 200) -> animation.FuncAnimation:
        """
        Crea una animación del diagrama fasorial al variar un parámetro

        Args:
            parameter: Parámetro a variar
            value_range: Rango de valores (min, max)
            num_frames: Número de frames de la animación
            interval: Intervalo entre frames en ms

        Returns:
            Objeto de animación de matplotlib
        """
        fig, ax = self.create_phasor_diagram()

        # Valores para cada frame
        values = np.linspace(value_range[0], value_range[1], num_frames)

        def animate(frame):
            # Limpiar frame anterior
            ax.clear()
            self.create_phasor_diagram()
            ax.figure = fig

            # Actualizar parámetro y dibujar
            current_value = values[frame]
            self.update_phasor_diagram(ax, parameter, current_value)

            # Título con valor actual
            ax.set_title(f'Diagrama Fasorial - {parameter} = {current_value:.2f}')

            return ax

        # Crear animación
        anim = animation.FuncAnimation(fig, animate, frames=num_frames,
                                     interval=interval, blit=False)

        return anim

    def create_phasor_explanation(self, figsize: Tuple[float, float] = (10, 6)) -> Figure:
        """
        Crea un diagrama explicativo del significado de cada fasor
        """
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.axis('off')

        # Título
        ax.text(5, 7.5, 'Interpretación del Diagrama Fasorial', ha='center',
               fontsize=14, fontweight='bold')

        # Explicación de cada fasor
        explanations = [
            ('V (Azul)', 'Tensión de fase aplicada desde la red'),
            ('E (Naranja)', 'Fuerza electromotriz interna generada por el rotor'),
            ('I (Verde)', 'Corriente de línea del motor'),
            ('Rs·I (Morado)', 'Caída de tensión resistiva en el estator'),
            ('j·Xs·I (Rojo)', 'Caída de tensión reactiva en el estator'),
        ]

        y_pos = 6.5
        for label, description in explanations:
            # Color indicator
            color = label.split('(')[1].split(')')[0].lower()
            color_map = {'azul': 'blue', 'naranja': 'orange', 'verde': 'green',
                        'morado': 'purple', 'rojo': 'red'}

            # Texto
            ax.text(1, y_pos, f'{label}:', fontsize=11, fontweight='bold',
                   color=color_map.get(color, 'black'))
            ax.text(3, y_pos, description, fontsize=10)
            y_pos -= 0.8

        # Ecuación fasorial
        y_pos -= 0.5
        ax.text(1, y_pos, 'Ecuación fundamental:', fontsize=11, fontweight='bold')
        ax.text(3, y_pos, 'V = E + Rs·I + j·Xs·I', fontsize=10, fontfamily='monospace')

        # Interpretación del ángulo
        y_pos -= 1
        ax.text(1, y_pos, 'Ángulo de carga δ:', fontsize=11, fontweight='bold')
        ax.text(3, y_pos, 'δ = ∠E - ∠V (ángulo entre E y V)', fontsize=10)

        y_pos -= 0.7
        ax.text(1, y_pos, 'Factor de potencia:', fontsize=11, fontweight='bold')
        ax.text(3, y_pos, 'cosφ = cos(∠I - ∠V)', fontsize=10)

        # Leyenda adicional
        y_pos -= 1.2
        ax.text(1, y_pos, 'Región estable:', fontsize=11, fontweight='bold')
        ax.text(3, y_pos, '|δ| < δ_máx (donde dT_e/dδ < 0)', fontsize=10)

        return fig

    def _clear_phasors(self, ax: Axes) -> None:
        """
        Limpia los fasores anteriores del diagrama
        """
        # Remover patches (flechas) que no sean el círculo de referencia
        to_remove = []
        for patch in ax.patches:
            if not isinstance(patch, plt.Circle):
                to_remove.append(patch)
        for patch in to_remove:
            patch.remove()

        # Remover textos (excepto título y labels de ejes)
        to_remove = []
        for text in ax.texts:
            # Mantener solo textos que no sean nuestros labels de fasores
            if not any(char.isdigit() or char == '.' for char in text.get_text() if char not in '°VIEjXsRs'):
                continue
            to_remove.append(text)
        for text in to_remove:
            text.remove()

        # Limpiar líneas
        to_remove = []
        for line in ax.lines:
            # Mantener solo los ejes
            if line.get_linestyle() != '-':
                continue
            to_remove.append(line)
        for line in to_remove:
            line.remove()

    def save_phasor_diagram(self, filename: str, results: Optional[Dict[str, float]] = None,
                           dpi: int = 300) -> None:
        """
        Guarda el diagrama fasorial en un archivo

        Args:
            filename: Nombre del archivo (con extensión .png, .pdf, etc.)
            results: Resultados para mostrar (opcional)
            dpi: Resolución en puntos por pulgada
        """
        fig, ax = self.create_phasor_diagram()
        self.plot_phasors(ax, results)

        fig.savefig(filename, dpi=dpi, bbox_inches='tight')
        plt.close(fig)

    def _create_phasor_diagram_on_axes(self, ax) -> None:
        """
        Crea el diagrama fasorial básico en ejes existentes
        """
        # Configurar el gráfico como círculo unitario
        ax.set_aspect('equal')
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)

        # Dibujar círculo de referencia
        circle = plt.Circle((0, 0), 1, fill=False, color='lightgray', linestyle='--', alpha=0.5)
        ax.add_patch(circle)

        # Ejes coordenados
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)

        # Etiquetas de ángulos
        for angle in [0, 90, 180, 270]:
            rad_angle = np.radians(angle)
            x_text = 1.2 * np.cos(rad_angle)
            y_text = 1.2 * np.sin(rad_angle)
            ax.text(x_text, y_text, f'{angle}°', ha='center', va='center', fontsize=8)

        # Título
        ax.set_title('Diagrama Fasorial del Motor Síncrono', fontsize=12, pad=20)
        ax.set_xlabel('Parte Real')
        ax.set_ylabel('Parte Imaginaria')

    def _plot_phasors_on_axes(self, ax, results: Optional[Dict[str, float]] = None) -> None:
        """
        Dibuja los fasores principales en el diagrama (en ejes existentes)
        """
        if results is None:
            results = self.motor.steady_state_analysis()

        # Obtener magnitudes y ángulos
        V_magnitude = results.get('V_phase', self.motor.phase_voltage()) / self.scale_factor
        E_magnitude = results.get('E_magnitude', 0) / self.scale_factor
        I_magnitude = results.get('I_magnitude', 0) / self.scale_factor

        V_angle = 0  # Referencia
        I_angle = results.get('I_angle', 0)
        delta = results.get('delta', 0)

        # Crear fasores como números complejos normalizados
        V_phasor = polar_to_rectangular(V_magnitude, V_angle)
        E_phasor = polar_to_rectangular(E_magnitude, np.degrees(delta))
        I_phasor = polar_to_rectangular(I_magnitude, I_angle)

        # Limpiar fasores anteriores
        self._clear_phasors(ax)

        # Dibujar fasores
        self._draw_phasor(ax, V_phasor, 'V', self.colors['V'], label_text='Tensión V')
        self._draw_phasor(ax, E_phasor, 'E', self.colors['E'], label_text='FEM interna E')
        self._draw_phasor(ax, I_phasor, 'I', self.colors['I'], label_text='Corriente I')

        # Dibujar caídas de tensión (opcional)
        self._draw_voltage_drops(ax, V_phasor, E_phasor, I_phasor)

        # Añadir leyenda
        ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
