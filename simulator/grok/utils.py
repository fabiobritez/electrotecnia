"""
Utilidades matemáticas para el simulador de motor síncrono
"""

import numpy as np
import cmath


def polar_to_rectangular(magnitude: float, angle_deg: float) -> complex:
    """Convierte de coordenadas polares a rectangulares"""
    angle_rad = np.radians(angle_deg)
    return complex(magnitude * np.cos(angle_rad), magnitude * np.sin(angle_rad))


def rectangular_to_polar(z: complex) -> tuple[float, float]:
    """Convierte de coordenadas rectangulares a polares (magnitud, ángulo en grados)"""
    magnitude = abs(z)
    angle_deg = np.degrees(cmath.phase(z))
    return magnitude, angle_deg


def deg_to_rad(angle_deg: float) -> float:
    """Convierte grados a radianes"""
    return np.radians(angle_deg)


def rad_to_deg(angle_rad: float) -> float:
    """Convierte radianes a grados"""
    return np.degrees(angle_rad)


def rpm_to_radps(rpm: float) -> float:
    """Convierte RPM a radianes por segundo"""
    return rpm * 2 * np.pi / 60


def radps_to_rpm(radps: float) -> float:
    """Convierte radianes por segundo a RPM"""
    return radps * 60 / (2 * np.pi)


def synchronous_speed_rpm(f: float, p: int) -> float:
    """Calcula velocidad síncrona en RPM"""
    return 120 * f / p


def synchronous_speed_radps(f: float, p: int) -> float:
    """Calcula velocidad síncrona en rad/s"""
    return 2 * np.pi * f / p


def phase_voltage(line_voltage: float, connection: str = 'star') -> float:
    """Calcula tensión de fase a partir de tensión de línea"""
    if connection.lower() == 'star':
        return line_voltage / np.sqrt(3)
    elif connection.lower() == 'delta':
        return line_voltage
    else:
        raise ValueError("Connection must be 'star' or 'delta'")


def line_current(phase_current: float, connection: str = 'star') -> float:
    """Calcula corriente de línea a partir de corriente de fase"""
    if connection.lower() == 'star':
        return phase_current
    elif connection.lower() == 'delta':
        return phase_current * np.sqrt(3)
    else:
        raise ValueError("Connection must be 'star' or 'delta'")


def power_factor_correction(current_angle: float, voltage_angle: float = 0) -> str:
    """Determina si el factor de potencia es inductivo o capacitivo"""
    phi = current_angle - voltage_angle
    if phi > 0:
        return "inductivo"  # corriente retrasada
    elif phi < 0:
        return "capacitivo"  # corriente adelantada
    else:
        return "unidad"


def calculate_power_factor(active_power: float, apparent_power: float) -> tuple[float, str]:
    """Calcula factor de potencia y tipo (inductivo/capacitivo)"""
    if apparent_power == 0:
        return 1.0, "unidad"

    pf = active_power / apparent_power
    pf = min(1.0, max(-1.0, pf))  # Clamp to [-1, 1]

    if pf >= 0:
        return pf, "inductivo" if pf < 1.0 else "unidad"
    else:
        return -pf, "capacitivo"


def normalize_angle(angle_deg: float) -> float:
    """Normaliza ángulo al rango [-180, 180] grados"""
    while angle_deg > 180:
        angle_deg -= 360
    while angle_deg <= -180:
        angle_deg += 360
    return angle_deg


def calculate_rms(value: float, is_peak: bool = True) -> float:
    """Calcula valor RMS a partir del valor peak o mantiene RMS"""
    if is_peak:
        return value / np.sqrt(2)
    return value


def calculate_peak(value: float, is_rms: bool = True) -> float:
    """Calcula valor peak a partir del valor RMS o mantiene peak"""
    if is_rms:
        return value * np.sqrt(2)
    return value
