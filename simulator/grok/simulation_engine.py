"""
Motor de simulación numérica para el simulador de motor síncrono

Maneja:
- Integración numérica de ecuaciones diferenciales
- Cálculos iterativos para régimen permanente
- Gestión de escenarios de simulación
- Optimización de parámetros
"""

import numpy as np
from scipy.integrate import odeint, solve_ivp
from scipy.optimize import fsolve
from typing import Dict, List, Tuple, Callable, Optional, Any
from motor_model import SynchronousMotorModel
import time


class SimulationEngine:
    """
    Motor de simulación para análisis dinámico y estático del motor síncrono
    """

    def __init__(self, motor_model: SynchronousMotorModel):
        self.motor = motor_model
        self.tolerance = 1e-6
        self.max_iterations = 100
        self.time_step = 0.01  # s

    def solve_steady_state(self, **fixed_params) -> Dict[str, float]:
        """
        Resuelve el estado estacionario del motor
        Encuentra el ángulo de carga δ que satisface T_e = T_L
        """
        # Guardar parámetros actuales
        original_params = {}
        for param in fixed_params:
            if hasattr(self.motor, param):
                original_params[param] = getattr(self.motor, param)
                setattr(self.motor, param, fixed_params[param])

        def equilibrium_equation(delta):
            """Ecuación: T_e(δ) - T_L = 0"""
            T_e = self.motor.calculate_torque_from_angle(delta)
            return T_e - self.motor.T_load

        # Estimación inicial del ángulo de carga
        delta_guess = 0.1  # rad

        try:
            # Resolver numéricamente
            delta_solution = fsolve(equilibrium_equation, delta_guess,
                                  xtol=self.tolerance, maxfev=self.max_iterations)

            # Actualizar el motor con la solución encontrada
            self.motor.delta = delta_solution[0]

            # Calcular todas las variables
            results = self.motor.steady_state_analysis()

        except Exception as e:
            print(f"Error resolviendo estado estacionario: {e}")
            # Fallback: análisis básico
            results = self.motor.steady_state_analysis()

        # Restaurar parámetros originales
        for param, value in original_params.items():
            setattr(self.motor, param, value)

        return results

    def simulate_transient_response(self,
                                  t_span: Tuple[float, float],
                                  initial_conditions: Optional[Dict[str, float]] = None,
                                  events: Optional[List[Callable]] = None) -> Dict[str, np.ndarray]:
        """
        Simula respuesta transitoria completa del motor

        Args:
            t_span: (t_inicio, t_final)
            initial_conditions: condiciones iniciales {'omega_m': ..., 'delta': ...}
            events: funciones para detectar eventos durante la simulación

        Returns:
            Diccionario con arrays temporales de todas las variables
        """
        # Condiciones iniciales por defecto
        if initial_conditions is None:
            initial_conditions = {
                'omega_m': 0.0,  # arranque desde reposo
                'delta': 0.0
            }

        omega_m_0 = initial_conditions.get('omega_m', 0.0)
        delta_0 = initial_conditions.get('delta', 0.0)
        state0 = np.array([omega_m_0, delta_0])

        # Función de derivadas
        def derivatives(t, state):
            return self.motor.dynamic_model_derivatives(state, t)

        # Simulación con solve_ivp (más robusto que odeint)
        sol = solve_ivp(derivatives, t_span, state0,
                       method='RK45', rtol=1e-8, atol=1e-10,
                       dense_output=True, events=events)

        if not sol.success:
            print(f"Error en simulación: {sol.message}")
            return {}

        # Arrays temporales
        t_eval = np.linspace(t_span[0], t_span[1], 1000)
        states = sol.sol(t_eval)

        omega_m = states[0]
        delta = states[1]

        # Calcular variables dependientes en cada instante
        results = {
            'time': t_eval,
            'omega_m': omega_m,
            'delta': delta,
            'delta_deg': np.degrees(delta),
            'T_load': np.full_like(t_eval, self.motor.T_load)
        }

        # Calcular T_e(t), potencias, etc. en cada punto
        T_e_array = []
        P_array = []
        Q_array = []
        pf_array = []

        for i, t in enumerate(t_eval):
            # Actualizar estado temporal del motor
            self.motor.delta = delta[i]
            self.motor.omega_m = omega_m[i]
            self.motor.time = t

            # Calcular par electromagnético
            T_e = self.motor.calculate_torque_from_angle(delta[i])
            T_e_array.append(T_e)

            # Para potencias necesitamos análisis fasorial completo
            # (esto es una aproximación simplificada)
            omega_s = self.motor.synchronous_speed()
            P_inst = T_e * omega_s  # P = T_e * ω_s
            P_array.append(P_inst)

            # Q y pf requieren cálculo fasorial completo - aproximación
            Q_array.append(0.0)  # TODO: implementar cálculo completo
            pf_array.append(1.0)  # TODO: implementar cálculo completo

        results.update({
            'T_e': np.array(T_e_array),
            'P': np.array(P_array),
            'Q': np.array(Q_array),
            'pf': np.array(pf_array)
        })

        return results

    def parameter_sweep(self, parameter: str, value_range: Tuple[float, float],
                       num_points: int = 20, **fixed_params) -> List[Dict[str, float]]:
        """
        Realiza un barrido de parámetros y calcula el estado estacionario para cada valor

        Args:
            parameter: nombre del parámetro a variar
            value_range: (valor_min, valor_max)
            num_points: número de puntos en el barrido
            fixed_params: otros parámetros a mantener fijos

        Returns:
            Lista de diccionarios con resultados para cada valor del parámetro
        """
        values = np.linspace(value_range[0], value_range[1], num_points)
        results = []

        # Guardar valor original
        original_value = getattr(self.motor, parameter)

        for value in values:
            # Actualizar parámetro
            setattr(self.motor, parameter, value)

            # Aplicar parámetros fijos
            for param, val in fixed_params.items():
                setattr(self.motor, param, val)

            # Resolver estado estacionario
            result = self.solve_steady_state()
            result[f'parameter_{parameter}'] = value
            results.append(result)

        # Restaurar valor original
        setattr(self.motor, parameter, original_value)

        return results

    def stability_analysis(self, delta_range: Tuple[float, float] = (-np.pi/2, np.pi/2),
                          num_points: int = 100) -> Dict[str, np.ndarray]:
        """
        Analiza la estabilidad del motor en función del ángulo de carga

        Returns:
            Diccionario con curvas de estabilidad
        """
        deltas = np.linspace(delta_range[0], delta_range[1], num_points)

        # Curva par-ángulo
        T_e_curve = np.array([self.motor.calculate_torque_from_angle(delta) for delta in deltas])

        # Derivada dT_e/dδ (estabilidad local)
        dTe_ddelta = np.gradient(T_e_curve, deltas)

        # Región estable: dT_e/dδ < 0
        stable_region = dTe_ddelta < 0

        # Par máximo
        max_torque_idx = np.argmax(T_e_curve)
        T_max = T_e_curve[max_torque_idx]
        delta_max = deltas[max_torque_idx]

        return {
            'delta': deltas,
            'T_e': T_e_curve,
            'dTe_ddelta': dTe_ddelta,
            'stable_region': stable_region,
            'T_max': T_max,
            'delta_max': delta_max
        }

    def find_operating_point(self, target_parameter: str, target_value: float,
                           vary_parameter: str, param_range: Tuple[float, float]) -> Optional[float]:
        """
        Encuentra el valor de un parámetro que produce un resultado deseado

        Ejemplo: encontrar If que produce cierto factor de potencia

        Args:
            target_parameter: parámetro objetivo ('pf', 'P', 'T_e', etc.)
            target_value: valor deseado
            vary_parameter: parámetro a variar ('If', 'V_line', etc.)
            param_range: rango de búsqueda

        Returns:
            Valor del parámetro que produce el resultado deseado
        """
        def objective_function(param_value):
            setattr(self.motor, vary_parameter, param_value)
            results = self.motor.steady_state_analysis()
            return results.get(target_parameter, 0) - target_value

        # Búsqueda usando fsolve
        param_guess = (param_range[0] + param_range[1]) / 2

        try:
            solution = fsolve(objective_function, param_guess,
                            xtol=self.tolerance, maxfev=self.max_iterations)
            return solution[0]
        except:
            return None

    def simulate_scenario(self, scenario_name: str, **scenario_params) -> Dict[str, Any]:
        """
        Ejecuta un escenario de simulación predefinido

        Args:
            scenario_name: nombre del escenario
            scenario_params: parámetros específicos del escenario

        Returns:
            Resultados de la simulación
        """
        scenarios = {
            'startup': self._scenario_startup,
            'load_increase': self._scenario_load_increase,
            'excitation_change': self._scenario_excitation_change,
            'overload': self._scenario_overload
        }

        if scenario_name not in scenarios:
            raise ValueError(f"Escenario desconocido: {scenario_name}")

        return scenarios[scenario_name](**scenario_params)

    def _scenario_startup(self, t_final: float = 2.0) -> Dict[str, Any]:
        """Escenario: Arranque del motor desde reposo"""
        t_span = (0, t_final)
        initial_conditions = {'omega_m': 0.0, 'delta': 0.0}

        # Simular con T_load = 0 durante arranque
        original_T_load = self.motor.T_load
        self.motor.T_load = 0.0

        results = self.simulate_transient_response(t_span, initial_conditions)

        # Restaurar T_load
        self.motor.T_load = original_T_load

        results['scenario'] = 'startup'
        results['description'] = 'Arranque del motor desde reposo hasta velocidad síncrona'

        return results

    def _scenario_load_increase(self, t_final: float = 5.0,
                               load_steps: int = 5) -> Dict[str, Any]:
        """Escenario: Aumento gradual de carga"""
        t_span = (0, t_final)
        initial_conditions = {'omega_m': self.motor.synchronous_speed(), 'delta': 0.1}

        # Crear perfil de carga que aumenta gradualmente
        t_eval = np.linspace(0, t_final, 1000)
        T_load_profile = np.zeros_like(t_eval)

        for i in range(load_steps):
            t_start = i * t_final / load_steps
            t_end = (i + 1) * t_final / load_steps
            mask = (t_eval >= t_start) & (t_eval <= t_end)
            T_load_profile[mask] = (i + 1) * self.motor.T_load / load_steps

        # Esta es una simplificación - en un modelo más completo
        # necesitaríamos simular con carga variable
        results = self.simulate_transient_response(t_span, initial_conditions)

        results['scenario'] = 'load_increase'
        results['description'] = f'Aumento gradual de carga en {load_steps} pasos'
        results['T_load_profile'] = T_load_profile

        return results

    def _scenario_excitation_change(self, t_final: float = 3.0,
                                   If_initial: float = 1.0,
                                   If_final: float = 4.0) -> Dict[str, Any]:
        """Escenario: Cambio de corriente de excitación"""
        t_span = (0, t_final)
        initial_conditions = {'omega_m': self.motor.synchronous_speed(), 'delta': 0.2}

        # Perfil de excitación que cambia linealmente
        t_eval = np.linspace(0, t_final, 1000)
        If_profile = If_initial + (If_final - If_initial) * t_eval / t_final

        # Simulación básica (simplificada)
        results = self.simulate_transient_response(t_span, initial_conditions)

        results['scenario'] = 'excitation_change'
        results['description'] = f'Cambio de excitación: {If_initial}A → {If_final}A'
        results['If_profile'] = If_profile

        return results

    def _scenario_overload(self, overload_factor: float = 1.5,
                          t_final: float = 2.0) -> Dict[str, Any]:
        """Escenario: Sobrecarga que puede llevar a pérdida de sincronismo"""
        t_span = (0, t_final)
        initial_conditions = {'omega_m': self.motor.synchronous_speed(), 'delta': 0.5}

        # Aplicar sobrecarga
        original_T_load = self.motor.T_load
        self.motor.T_load = original_T_load * overload_factor

        results = self.simulate_transient_response(t_span, initial_conditions)

        # Restaurar carga original
        self.motor.T_load = original_T_load

        results['scenario'] = 'overload'
        results['description'] = f'Sobrecarga {overload_factor}x que puede causar inestabilidad'
        results['overload_factor'] = overload_factor

        return results
