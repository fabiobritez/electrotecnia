import matplotlib.pyplot as plt
import numpy as np

def graficar_galileo_ferraris():
    # Configuración de la figura
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Parámetros
    H_max = 1.0
    H_half = H_max / 2
    angle_deg = 60  # Ángulo para la foto instantánea
    angle_rad = np.radians(angle_deg)
    
    # Coordenadas de los vectores
    # Vector girando anti-horario (+omega)
    v1_x, v1_y = H_half * np.cos(angle_rad), H_half * np.sin(angle_rad)
    
    # Vector girando horario (-omega)
    v2_x, v2_y = H_half * np.cos(-angle_rad), H_half * np.sin(-angle_rad)
    
    # Vector resultante (Suma)
    v_sum_x = v1_x + v2_x
    v_sum_y = 0  # Se cancelan las componentes Y
    
    # Dibujar Ejes
    ax.axhline(0, color='black', linewidth=1, linestyle='--')
    ax.axvline(0, color='black', linewidth=1, linestyle='--')
    
    # Dibujar Vectores
    # 1. Vector Anti-horario
    ax.quiver(0, 0, v1_x, v1_y, angles='xy', scale_units='xy', scale=1, color='blue', width=0.012, label=r'$\frac{H_{max}}{2} e^{j\omega t}$')
    
    # 2. Vector Horario
    ax.quiver(0, 0, v2_x, v2_y, angles='xy', scale_units='xy', scale=1, color='blue', width=0.012, label=r'$\frac{H_{max}}{2} e^{-j\omega t}$')
    
    # 3. Resultante (Proyección en el eje Real)
    ax.quiver(0, 0, v_sum_x, v_sum_y, angles='xy', scale_units='xy', scale=1, color='red', width=0.015, label=r'$h = H_{max} \cos \omega t$')

    # Líneas de proyección (punteadas) para mostrar la suma
    ax.plot([v1_x, v_sum_x], [v1_y, 0], 'k:', alpha=0.5)
    ax.plot([v2_x, v_sum_x], [v2_y, 0], 'k:', alpha=0.5)

    # Flechas de rotación (arcos)
    ax.text(v1_x + 0.05, v1_y + 0.05, r'$+\omega$', fontsize=12)
    ax.text(v2_x + 0.05, v2_y - 0.1, r'$-\omega$', fontsize=12)
    
    # Etiquetas de los ejes
    ax.set_xlabel('Real', loc='right', fontsize=12)
    ax.set_ylabel('Imaginario', loc='top', fontsize=12)
    
    # Configuración final
    ax.set_xlim(-0.6, 1.1)
    ax.set_ylim(-0.7, 0.7)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right')
    ax.set_title('Principio de Galileo-Ferraris (Descomposición de Campos)', fontsize=14)
    
    # Quitar los ticks numéricos para que parezca más un diagrama teórico
    ax.set_xticks([])
    ax.set_yticks([])
    
    plt.show()

# Ejecutar la función
graficar_galileo_ferraris()
