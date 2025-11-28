import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ==========================================================
# CONFIGURACIÓN INICIAL
# ==========================================================
f = 50                     # frecuencia eléctrica en Hz
w = 2*np.pi*f              # pulsación
Hmax = 1                   # amplitud del campo magnético
sequence = "CBA"           # cambiar a "CBA" para invertir giro

# Tiempo
t = np.linspace(0, 0.04, 1000)   # 40 ms = 2 ciclos

# ==========================================================
# Definición de fases según secuencia
# ==========================================================
if sequence == "ABC":
    phi_a, phi_b, phi_c = 0, -120*np.pi/180, +120*np.pi/180
else:
    phi_a, phi_b, phi_c = 0, +120*np.pi/180, -120*np.pi/180

# ==========================================================
# FUNCIONES DE CAMPO MAGNÉTICO
# ==========================================================
def ha(t): 
    return Hmax * np.cos(w*t + phi_a)

def hb(t): 
    return Hmax * np.cos(w*t + phi_b)

def hc(t): 
    return Hmax * np.cos(w*t + phi_c)

# vectores geométricos de cada bobina
ua = np.exp(1j * 0)
ub = np.exp(1j * (-120*np.pi/180))
uc = np.exp(1j * (+120*np.pi/180))

# Campo total rotante
def h_total(t):
    return ha(t)*ua + hb(t)*ub + hc(t)*uc

# ==========================================================
# FIGURA Y SUBPLOTS
# ==========================================================
fig = plt.figure(figsize=(12,8))

# Señales temporales
ax1 = fig.add_subplot(2,2,1)
ax1.set_title("Corrientes trifásicas")
ax1.set_xlabel("Tiempo [s]")
ax1.set_ylim(-1.1*Hmax, 1.1*Hmax)

line_a, = ax1.plot([], [], label="A", color="r")
line_b, = ax1.plot([], [], label="B", color="g")
line_c, = ax1.plot([], [], label="C", color="b")
ax1.legend()

# Fasores instantáneos
ax2 = fig.add_subplot(2,2,2)
ax2.set_title("Fasores de los Campos Ha, Hb, Hc")
ax2.set_xlim(-1.3*Hmax, 1.3*Hmax)
ax2.set_ylim(-1.3*Hmax, 1.3*Hmax)
ax2.set_aspect('equal')

fasor_a, = ax2.plot([], [], 'r')
fasor_b, = ax2.plot([], [], 'g')
fasor_c, = ax2.plot([], [], 'b')

# Campo rotante
# Campo rotante
ax3 = fig.add_subplot(2,1,2)
ax3.set_title("Campo Magnético Rotante Resultante (Vector)")
ax3.set_xlim(-2*Hmax, 2*Hmax)
ax3.set_ylim(-2*Hmax, 2*Hmax)
ax3.set_aspect('equal')
ax3.grid(True)

# Flecha inicial (vector rotante)
rot_arrow = ax3.quiver(0, 0, 0, 0, angles='xy', scale_units='xy', scale=1, color='m')

# (Opcional) trayectoria del extremo
# trail, = ax3.plot([], [], 'm--', alpha=0.4)
# history_x, history_y = [], []

# ==========================================================
# ANIMACIÓN
# ==========================================================
history_x = []
history_y = []

def update(frame):
    tt = t[frame]

    # Señales temporales
    line_a.set_data(t[:frame], ha(t[:frame]))
    line_b.set_data(t[:frame], hb(t[:frame]))
    line_c.set_data(t[:frame], hc(t[:frame]))

    # Fasores
    Ha = ha(tt) * ua
    Hb = hb(tt) * ub
    Hc = hc(tt) * uc

    fasor_a.set_data([0, Ha.real], [0, Ha.imag])
    fasor_b.set_data([0, Hb.real], [0, Hb.imag])
    fasor_c.set_data([0, Hc.real], [0, Hc.imag])

    # Campo total
        # Campo total instantáneo
    H = h_total(tt)

    # Actualizar flecha (vector)
    rot_arrow.set_UVC(H.real, H.imag)

    # (Opcional) trayectoria
    # history_x.append(H.real)
    # history_y.append(H.imag)
    # trail.set_data(history_x, history_y)

    return line_a, line_b, line_c, fasor_a, fasor_b, fasor_c, rot_arrow


ani = FuncAnimation(fig, update, frames=len(t), interval=20, blit=False)

plt.tight_layout()
plt.show()

