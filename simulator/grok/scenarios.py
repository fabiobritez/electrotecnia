"""
Escenarios preconfigurados para el simulador de motor síncrono

Define configuraciones preestablecidas para casos típicos de simulación:
- Arranque ideal
- Carga creciente
- Cambio de excitación
- Sobrecarga
"""

import numpy as np
from typing import Dict, List, Tuple, Any
from motor_model import SynchronousMotorModel
from simulation_engine import SimulationEngine


class SimulationScenarios:
    """
    Gestor de escenarios de simulación preconfigurados
    """

    def __init__(self, motor_model: SynchronousMotorModel):
        self.motor = motor_model
        self.engine = SimulationEngine(motor_model)

    def get_available_scenarios(self) -> List[str]:
        """Retorna lista de escenarios disponibles"""
        return [
            'startup_ideal',
            'load_increase_gradual',
            'excitation_sub_to_over',
            'excitation_over_to_sub',
            'overload_test',
            'frequency_variation',
            'voltage_sag'
        ]

    def get_scenario_description(self, scenario_name: str) -> str:
        """Retorna descripción del escenario"""
        descriptions = {
            'startup_ideal': 'Arranque ideal desde reposo hasta velocidad síncrona',
            'load_increase_gradual': 'Aumento gradual de carga para analizar estabilidad',
            'excitation_sub_to_over': 'Cambio de excitación de subexcitado a sobreexcitado',
            'excitation_over_to_sub': 'Cambio de excitación de sobreexcitado a subexcitado',
            'overload_test': 'Prueba de sobrecarga para determinar límite de estabilidad',
            'frequency_variation': 'Variación de frecuencia de la red',
            'voltage_sag': 'Caída temporal de tensión'
        }
        return descriptions.get(scenario_name, 'Escenario desconocido')

    def run_scenario(self, scenario_name: str, **params) -> Dict[str, Any]:
        """Ejecuta un escenario específico"""
        scenario_methods = {
            'startup_ideal': self.scenario_startup_ideal,
            'load_increase_gradual': self.scenario_load_increase_gradual,
            'excitation_sub_to_over': self.scenario_excitation_sub_to_over,
            'excitation_over_to_sub': self.scenario_excitation_over_to_sub,
            'overload_test': self.scenario_overload_test,
            'frequency_variation': self.scenario_frequency_variation,
            'voltage_sag': self.scenario_voltage_sag
        }

        if scenario_name not in scenario_methods:
            raise ValueError(f"Escenario '{scenario_name}' no disponible")

        return scenario_methods[scenario_name](**params)

    def scenario_startup_ideal(self, t_final: float = 3.0,
                              initial_omega_ratio: float = 0.0) -> Dict[str, Any]:
        """
        Escenario 1: Arranque ideal del motor

        El motor arranca desde reposo (o desde una velocidad inicial)
        hasta alcanzar la velocidad síncrona con carga nominal.
        """
        # Configuración del escenario
        config = {
            'name': 'startup_ideal',
            'description': 'Arranque ideal desde reposo hasta velocidad síncrona',
            'parameters': {
                't_final': t_final,
                'initial_omega_ratio': initial_omega_ratio
            }
        }

        # Condiciones iniciales
        omega_s = self.motor.synchronous_speed()
        initial_conditions = {
            'omega_m': initial_omega_ratio * omega_s,
            'delta': 0.0
        }

        # Simular con carga reducida durante arranque
        original_T_load = self.motor.T_load
        self.motor.T_load = 0.0  # arranque sin carga

        # Simulación
        results = self.engine.simulate_transient_response(
            (0, t_final), initial_conditions
        )

        # Restaurar carga
        self.motor.T_load = original_T_load

        # Añadir información del escenario
        results.update(config)
        results['omega_s'] = omega_s
        results['n_s'] = self.motor.synchronous_speed_rpm()

        return results

    def scenario_load_increase_gradual(self, t_final: float = 8.0,
                                      load_steps: int = 4,
                                      max_load_ratio: float = 1.2) -> Dict[str, Any]:
        """
        Escenario 2: Carga creciente

        Aumenta gradualmente la carga desde 0 hasta un valor máximo
        para analizar cómo responde el motor y cuándo pierde estabilidad.
        """
        config = {
            'name': 'load_increase_gradual',
            'description': f'Aumento gradual de carga en {load_steps} pasos hasta {max_load_ratio}x carga nominal',
            'parameters': {
                't_final': t_final,
                'load_steps': load_steps,
                'max_load_ratio': max_load_ratio
            }
        }

        # Carga nominal
        T_nominal = self.motor.T_load

        # Simular múltiples etapas de carga
        all_results = []
        current_time = 0.0

        for step in range(load_steps + 1):
            # Calcular carga para este paso
            load_ratio = step * max_load_ratio / load_steps
            self.motor.T_load = T_nominal * load_ratio

            # Tiempo para este paso
            step_duration = t_final / load_steps
            t_span = (current_time, current_time + step_duration)

            # Condiciones iniciales (continuar desde estado anterior)
            if step == 0:
                initial_conditions = {'omega_m': self.motor.synchronous_speed(), 'delta': 0.1}
            else:
                # Usar estado final del paso anterior
                prev_results = all_results[-1]
                initial_conditions = {
                    'omega_m': prev_results['omega_m'][-1],
                    'delta': prev_results['delta'][-1]
                }

            # Simular este paso
            step_results = self.engine.simulate_transient_response(t_span, initial_conditions)
            step_results['load_ratio'] = load_ratio
            step_results['T_load_step'] = self.motor.T_load

            all_results.append(step_results)
            current_time += step_duration

        # Combinar todos los resultados
        combined_results = self._combine_step_results(all_results)
        combined_results.update(config)

        # Restaurar carga nominal
        self.motor.T_load = T_nominal

        return combined_results

    def scenario_excitation_sub_to_over(self, t_final: float = 4.0,
                                       If_initial: float = 0.5,
                                       If_final: float = 4.0) -> Dict[str, Any]:
        """
        Escenario 3: Cambio de excitación de subexcitado a sobreexcitado

        Muestra cómo cambia el factor de potencia y otras variables
        al aumentar la corriente de excitación.
        """
        return self._excitation_change_scenario(
            t_final, If_initial, If_final, 'sub_to_over',
            'Cambio de excitación: subexcitado → sobreexcitado'
        )

    def scenario_excitation_over_to_sub(self, t_final: float = 4.0,
                                       If_initial: float = 4.0,
                                       If_final: float = 0.5) -> Dict[str, Any]:
        """
        Escenario 4: Cambio de excitación de sobreexcitado a subexcitado
        """
        return self._excitation_change_scenario(
            t_final, If_initial, If_final, 'over_to_sub',
            'Cambio de excitación: sobreexcitado → subexcitado'
        )

    def _excitation_change_scenario(self, t_final: float, If_initial: float,
                                   If_final: float, direction: str,
                                   description: str) -> Dict[str, Any]:
        """Implementación común para escenarios de cambio de excitación"""
        config = {
            'name': f'excitation_{direction}',
            'description': description,
            'parameters': {
                't_final': t_final,
                'If_initial': If_initial,
                'If_final': If_final
            }
        }

        # Condiciones iniciales con excitación inicial
        original_If = self.motor.If
        self.motor.If = If_initial

        initial_conditions = {'omega_m': self.motor.synchronous_speed(), 'delta': 0.2}

        # Simulación básica (simplificada - en realidad necesitaríamos
        # un modelo más completo para cambios dinámicos de excitación)
        results = self.engine.simulate_transient_response((0, t_final), initial_conditions)

        # Crear perfil de excitación
        t_eval = results['time']
        If_profile = If_initial + (If_final - If_initial) * t_eval / t_final

        # Calcular cómo cambian las variables con la excitación
        pf_profile = []
        P_profile = []
        Q_profile = []

        for If in If_profile[::10]:  # Muestrear cada 10 puntos para eficiencia
            self.motor.If = If
            steady_results = self.motor.steady_state_analysis()
            pf_profile.extend([steady_results['pf']] * 10)
            P_profile.extend([steady_results['P']] * 10)
            Q_profile.extend([steady_results['Q']] * 10)

        # Ajustar longitud
        pf_profile = pf_profile[:len(t_eval)]
        P_profile = P_profile[:len(t_eval)]
        Q_profile = Q_profile[:len(t_eval)]

        results.update({
            'If_profile': If_profile,
            'pf_profile': pf_profile,
            'P_profile': P_profile,
            'Q_profile': Q_profile
        })

        results.update(config)

        # Restaurar excitación original
        self.motor.If = original_If

        return results

    def scenario_overload_test(self, overload_ratios: List[float] = [1.1, 1.3, 1.5],
                              t_final: float = 2.0) -> Dict[str, Any]:
        """
        Escenario 5: Prueba de sobrecarga

        Aplica diferentes niveles de sobrecarga para determinar
        el límite de estabilidad del motor.
        """
        config = {
            'name': 'overload_test',
            'description': f'Prueba de sobrecarga con ratios: {overload_ratios}',
            'parameters': {
                'overload_ratios': overload_ratios,
                't_final': t_final
            }
        }

        T_nominal = self.motor.T_load
        all_results = []

        for ratio in overload_ratios:
            # Aplicar sobrecarga
            self.motor.T_load = T_nominal * ratio

            # Condiciones iniciales
            initial_conditions = {'omega_m': self.motor.synchronous_speed(), 'delta': 0.3}

            # Simular
            results = self.engine.simulate_transient_response((0, t_final), initial_conditions)
            results['overload_ratio'] = ratio
            results['stable'] = self._check_stability(results)

            all_results.append(results)

        # Combinar resultados
        combined_results = self._combine_overload_results(all_results)
        combined_results.update(config)

        # Restaurar carga nominal
        self.motor.T_load = T_nominal

        return combined_results

    def scenario_frequency_variation(self, t_final: float = 6.0,
                                    f_initial: float = 50.0,
                                    f_min: float = 48.0,
                                    f_max: float = 52.0) -> Dict[str, Any]:
        """
        Escenario 6: Variación de frecuencia

        Simula cambios en la frecuencia de la red y su efecto
        en la operación del motor.
        """
        config = {
            'name': 'frequency_variation',
            'description': f'Variación de frecuencia: {f_min}-{f_max} Hz',
            'parameters': {
                't_final': t_final,
                'f_initial': f_initial,
                'f_min': f_min,
                'f_max': f_max
            }
        }

        # Este escenario requiere un modelo más avanzado
        # Por ahora, devolver configuración básica
        results = {
            'time': np.linspace(0, t_final, 100),
            'frequency_profile': f_initial * np.ones(100),  # placeholder
            'note': 'Este escenario requiere implementación avanzada del modelo dinámico'
        }

        results.update(config)
        return results

    def scenario_voltage_sag(self, t_final: float = 3.0,
                            sag_magnitude: float = 0.8,
                            sag_duration: float = 0.5,
                            sag_start: float = 1.0) -> Dict[str, Any]:
        """
        Escenario 7: Caída de tensión (voltage sag)

        Simula una caída temporal de tensión y la respuesta del motor.
        """
        config = {
            'name': 'voltage_sag',
            'description': f'Caída de tensión al {sag_magnitude*100:.0f}% durante {sag_duration}s',
            'parameters': {
                't_final': t_final,
                'sag_magnitude': sag_magnitude,
                'sag_duration': sag_duration,
                'sag_start': sag_start
            }
        }

        # Perfil de tensión
        t_eval = np.linspace(0, t_final, 1000)
        V_profile = np.ones_like(t_eval)

        # Aplicar sag
        sag_mask = (t_eval >= sag_start) & (t_eval <= sag_start + sag_duration)
        V_profile[sag_mask] = sag_magnitude

        results = {
            'time': t_eval,
            'V_profile': V_profile,
            'note': 'Este escenario requiere implementación avanzada del modelo dinámico'
        }

        results.update(config)
        return results

    def _combine_step_results(self, step_results: List[Dict]) -> Dict:
        """Combina resultados de múltiples pasos de simulación"""
        if not step_results:
            return {}

        # Concatenar arrays temporales
        combined = {
            'time': np.concatenate([r['time'] for r in step_results]),
            'omega_m': np.concatenate([r['omega_m'] for r in step_results]),
            'delta': np.concatenate([r['delta'] for r in step_results]),
            'delta_deg': np.concatenate([r['delta_deg'] for r in step_results]),
            'T_e': np.concatenate([r['T_e'] for r in step_results]),
            'T_load': np.concatenate([r['T_load'] for r in step_results]),
            'load_steps': [r.get('load_ratio', 0) for r in step_results]
        }

        return combined

    def _combine_overload_results(self, overload_results: List[Dict]) -> Dict:
        """Combina resultados de pruebas de sobrecarga"""
        if not overload_results:
            return {}

        combined = {
            'overload_ratios': [r['overload_ratio'] for r in overload_results],
            'stability_results': [r['stable'] for r in overload_results],
            'max_deltas': [np.max(r['delta']) for r in overload_results],
            'max_omega_deviations': [np.max(np.abs(r['omega_m'] - self.motor.synchronous_speed()))
                                    for r in overload_results]
        }

        return combined

    def _check_stability(self, results: Dict) -> bool:
        """
        Verifica si la simulación indica estabilidad

        Criterios simples:
        - La velocidad no se desvía mucho de la síncrona
        - El ángulo de carga no crece indefinidamente
        - El sistema alcanza un estado estacionario
        """
        omega_m = results['omega_m']
        delta = results['delta']
        omega_s = self.motor.synchronous_speed()

        # Criterios de estabilidad
        omega_deviation = np.abs(omega_m - omega_s)
        max_omega_dev = np.max(omega_deviation)
        max_delta = np.max(np.abs(delta))

        # Umbrales arbitrarios (podrían ajustarse)
        stable = (max_omega_dev < 5.0) and (max_delta < np.pi/2)

        return stable
