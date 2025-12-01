"""
Modelo matemático del motor síncrono trifásico

Implementa las ecuaciones para:
- Régimen permanente (modelo fasorial)
- Modelo dinámico simplificado en ejes d-q
- Cálculos de potencias, pares y velocidades
"""

import numpy as np
import cmath
from typing import Dict, Tuple, Optional
from utils import (
    synchronous_speed_radps, phase_voltage, polar_to_rectangular,
    rectangular_to_polar, calculate_power_factor, normalize_angle
)


class SynchronousMotorModel:
    """
    Modelo de motor síncrono trifásico con rotor de polos salientes

    Parámetros eléctricos:
    - Rs: resistencia del estator [ohm]
    - Xd: reactancia síncrona en eje d [ohm]
    - Xq: reactancia síncrona en eje q [ohm]
    - Rf: resistencia del campo [ohm] (opcional)

    Parámetros mecánicos:
    - J: momento de inercia [kg·m²]
    - B: coeficiente de amortiguamiento [N·m·s/rad]
    - p: número de polos

    Variables de operación:
    - V_line: tensión de línea [V]
    - f: frecuencia [Hz]
    - If: corriente de excitación del rotor [A]
    - T_load: par de carga [N·m]
    - connection: tipo de conexión ('star' o 'delta')
    """

    def __init__(self):
        # Parámetros eléctricos por defecto (motor típico de 5 kVA)
        self.Rs = 0.5  # ohm
        self.Xd = 5.0  # ohm
        self.Xq = 3.5  # ohm
        self.Rf = 0.1  # ohm (opcional)

        # Parámetros mecánicos por defecto
        self.J = 0.1  # kg·m²
        self.B = 0.01  # N·m·s/rad
        self.p = 4  # número de polos

        # Variables de operación
        self.V_line = 400.0  # V
        self.f = 50.0  # Hz
        self.If = 2.0  # A
        self.T_load = 10.0  # N·m
        self.connection = 'star'  # 'star' o 'delta'

        # Estado interno
        self.delta = 0.0  # ángulo de carga eléctrico [rad]
        self.omega_m = 0.0  # velocidad mecánica [rad/s]
        self.time = 0.0  # tiempo de simulación [s]

    def update_parameters(self, **params):
        """Actualiza parámetros del modelo"""
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)

        # Recalcular velocidad síncrona si cambian f o p
        if 'f' in params or 'p' in params:
            self.omega_m = synchronous_speed_radps(self.f, self.p)

    def get_electrical_parameters(self) -> Dict[str, float]:
        """Retorna parámetros eléctricos actuales"""
        return {
            'Rs': self.Rs,
            'Xd': self.Xd,
            'Xq': self.Xq,
            'Rf': self.Rf,
            'p': self.p
        }

    def get_mechanical_parameters(self) -> Dict[str, float]:
        """Retorna parámetros mecánicos actuales"""
        return {
            'J': self.J,
            'B': self.B,
            'T_load': self.T_load
        }

    def get_operating_parameters(self) -> Dict[str, float]:
        """Retorna parámetros de operación actuales"""
        return {
            'V_line': self.V_line,
            'f': self.f,
            'If': self.If,
            'connection': self.connection
        }

    # ==================== CÁLCULOS BÁSICOS ====================

    def synchronous_speed(self) -> float:
        """Velocidad síncrona en rad/s"""
        return synchronous_speed_radps(self.f, self.p)

    def synchronous_speed_rpm(self) -> float:
        """Velocidad síncrona en RPM"""
        return 120 * self.f / self.p

    def phase_voltage(self) -> float:
        """Tensión de fase en V"""
        return phase_voltage(self.V_line, self.connection)

    # ==================== MODELO FASORIAL (RÉGIMEN PERMANENTE) ====================

    def calculate_internal_voltage(self) -> complex:
        """
        Calcula la fuerza electromotriz interna E_f
        E_f es proporcional a la corriente de excitación If
        """
        # Constante de proporcionalidad (puede ajustarse según el motor)
        K_e = 100.0  # V/A (típico para motores pequeños)

        # E_f = K_e * If (magnitud)
        # Fase inicial = 0 (referencia)
        E_f_magnitude = K_e * self.If

        # El ángulo de E_f depende del ángulo de carga δ
        # Para motor: E_f está adelantado respecto a V por el ángulo δ
        return polar_to_rectangular(E_f_magnitude, 0)

    def calculate_current_phasor(self, V_phasor: complex, E_phasor: complex) -> complex:
        """
        Calcula el fasor de corriente usando el modelo simplificado
        V = E + j Xs I + Rs I

        Para polos salientes, usamos Xs promedio o consideramos el ángulo.
        Para simplificar, usamos Xs = (Xd + Xq)/2
        """
        Xs_avg = (self.Xd + self.Xq) / 2

        # Ecuación: V = E + (Rs + j Xs) I
        # I = (V - E) / (Rs + j Xs)
        impedance = complex(self.Rs, Xs_avg)
        I_phasor = (V_phasor - E_phasor) / impedance

        return I_phasor

    def calculate_load_angle(self, V_phasor: complex, E_phasor: complex) -> float:
        """
        Calcula el ángulo de carga δ a partir de los fasores
        δ = ∠E - ∠V
        """
        _, V_angle = rectangular_to_polar(V_phasor)
        _, E_angle = rectangular_to_polar(E_phasor)
        delta_deg = E_angle - V_angle
        return np.radians(normalize_angle(delta_deg))

    def calculate_electromagnetic_torque(self, V_phasor: complex, I_phasor: complex) -> float:
        """
        Calcula el par electromagnético usando la fórmula general
        T_e = (3/ω_s) * Im(V * conj(I))

        Para motor síncrono simplificado:
        T_e = (3 V E / ω_s Xs) * sinδ
        """
        V_magnitude = abs(V_phasor)
        I_magnitude = abs(I_phasor)
        power_factor_angle = cmath.phase(I_phasor) - cmath.phase(V_phasor)

        # Potencia activa = 3 * V_fase * I_fase * cosφ
        active_power = 3 * V_magnitude * I_magnitude * np.cos(power_factor_angle)

        # T_e = P / ω_s
        omega_s = self.synchronous_speed()
        T_e = active_power / omega_s

        return T_e

    def calculate_torque_from_angle(self, delta: float) -> float:
        """
        Calcula el par electromagnético usando la fórmula clásica
        T_e = (3 V E / ω_s Xs) * sinδ

        Donde Xs es la reactancia síncrona promedio
        """
        V_phase = self.phase_voltage()
        E_magnitude = abs(self.calculate_internal_voltage())
        omega_s = self.synchronous_speed()
        Xs_avg = (self.Xd + self.Xq) / 2

        T_e_max = 3 * V_phase * E_magnitude / (omega_s * Xs_avg)
        T_e = T_e_max * np.sin(delta)

        return T_e

    def calculate_powers(self, V_phasor: complex, I_phasor: complex) -> Dict[str, float]:
        """
        Calcula potencias activa, reactiva y aparente
        """
        V_magnitude = abs(V_phasor)
        I_magnitude = abs(I_phasor)
        phi = cmath.phase(I_phasor) - cmath.phase(V_phasor)

        # Potencias por fase
        S_phase = V_magnitude * I_magnitude  # aparente por fase
        P_phase = V_magnitude * I_magnitude * np.cos(phi)  # activa por fase
        Q_phase = V_magnitude * I_magnitude * np.sin(phi)  # reactiva por fase

        # Potencias totales (3 fases)
        S = 3 * S_phase
        P = 3 * P_phase
        Q = 3 * Q_phase

        # Factor de potencia
        pf, pf_type = calculate_power_factor(P, S)

        return {
            'S': S,  # potencia aparente [VA]
            'P': P,  # potencia activa [W]
            'Q': Q,  # potencia reactiva [VAR]
            'pf': pf,  # factor de potencia [0-1]
            'pf_type': pf_type  # 'inductivo', 'capacitivo', 'unidad'
        }

    # ==================== ANÁLISIS EN RÉGIMEN PERMANENTE ====================

    def steady_state_analysis(self) -> Dict[str, float]:
        """
        Realiza análisis completo en régimen permanente
        Retorna todas las variables calculadas
        """
        # Fasores de tensión (referencia en 0°)
        V_phase = self.phase_voltage()
        V_phasor = polar_to_rectangular(V_phase, 0)

        # Fuerza electromotriz interna
        E_phasor = self.calculate_internal_voltage()

        # Corriente
        I_phasor = self.calculate_current_phasor(V_phasor, E_phasor)

        # Ángulo de carga
        delta = self.calculate_load_angle(V_phasor, E_phasor)

        # Par electromagnético
        T_e = self.calculate_electromagnetic_torque(V_phasor, I_phasor)

        # Potencias
        powers = self.calculate_powers(V_phasor, I_phasor)

        # Magnitudes de corriente
        I_magnitude, I_angle = rectangular_to_polar(I_phasor)

        # Velocidad
        omega_s = self.synchronous_speed()
        n_s = self.synchronous_speed_rpm()

        return {
            # Parámetros de entrada
            'V_line': self.V_line,
            'V_phase': V_phase,
            'f': self.f,
            'If': self.If,
            'T_load': self.T_load,

            # Variables calculadas
            'omega_s': omega_s,  # velocidad síncrona [rad/s]
            'n_s': n_s,  # velocidad síncrona [rpm]
            'delta': delta,  # ángulo de carga [rad]
            'delta_deg': np.degrees(delta),  # ángulo de carga [°]
            'I_magnitude': I_magnitude,  # corriente de línea [A]
            'I_angle': I_angle,  # ángulo de corriente [°]
            'T_e': T_e,  # par electromagnético [N·m]

            # Fasores (magnitudes)
            'E_magnitude': abs(E_phasor),
            'V_magnitude': abs(V_phasor),

            **powers  # potencias
        }

    # ==================== MODELO DINÁMICO ====================

    def dynamic_model_derivatives(self, state: np.ndarray, t: float) -> np.ndarray:
        """
        Ecuaciones diferenciales para simulación dinámica
        state = [omega_m, delta]

        Ecuaciones:
        d(omega_m)/dt = (T_e - T_L - B * omega_m) / J
        d(delta)/dt = omega_s - omega_m  (para motor síncrono)
        """
        omega_m, delta = state

        # Par electromagnético (función del ángulo de carga)
        T_e = self.calculate_torque_from_angle(delta)

        # Velocidad síncrona
        omega_s = self.synchronous_speed()

        # Ecuaciones diferenciales
        d_omega_m_dt = (T_e - self.T_load - self.B * omega_m) / self.J
        d_delta_dt = omega_s - omega_m  # diferencia entre velocidad síncrona y mecánica

        return np.array([d_omega_m_dt, d_delta_dt])

    def simulate_transient(self, t_span: Tuple[float, float],
                          initial_omega: Optional[float] = None,
                          initial_delta: Optional[float] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Simula comportamiento transitorio usando integración numérica
        """
        from scipy.integrate import odeint

        # Condiciones iniciales
        if initial_omega is None:
            initial_omega = 0.0  # arranque desde reposo
        if initial_delta is None:
            initial_delta = 0.0

        state0 = np.array([initial_omega, initial_delta])

        # Tiempo de simulación
        t = np.linspace(t_span[0], t_span[1], 1000)

        # Integración numérica
        try:
            solution = odeint(self.dynamic_model_derivatives, state0, t)
            return t, solution
        except Exception as e:
            print(f"Error en simulación dinámica: {e}")
            return t, np.zeros((len(t), 2))

    # ==================== ANÁLISIS DE ESTABILIDAD ====================

    def torque_angle_curve(self, delta_range: Tuple[float, float] = (0, np.pi),
                          num_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genera la curva característica T_e vs δ
        """
        deltas = np.linspace(delta_range[0], delta_range[1], num_points)
        torques = np.array([self.calculate_torque_from_angle(delta) for delta in deltas])

        return deltas, torques

    def maximum_torque(self) -> Tuple[float, float]:
        """
        Calcula el par máximo y el ángulo correspondiente
        """
        deltas, torques = self.torque_angle_curve()
        max_idx = np.argmax(torques)
        return torques[max_idx], deltas[max_idx]

    def power_factor_vs_excitation(self, If_range: Tuple[float, float] = (0.1, 5.0),
                                 num_points: int = 50) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Genera curva de factor de potencia vs corriente de excitación
        """
        If_values = np.linspace(If_range[0], If_range[1], num_points)
        pf_values = []
        pf_types = []

        # Guardar valor actual de If
        original_If = self.If

        for If in If_values:
            self.If = If
            results = self.steady_state_analysis()
            pf_values.append(results['pf'])
            pf_types.append(results['pf_type'])

        # Restaurar valor original
        self.If = original_If

        return If_values, np.array(pf_values), np.array(pf_types)
