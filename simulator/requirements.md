Quiero que desarrolles un simulador interactivo y educativo de un motor síncrono trifásico, con énfasis en mostrar claramente las variables eléctricas y mecánicas y cómo se afectan entre sí. Supone que el usuario tiene formación de ingeniería (eléctrica/electrónica) y quiere entender tanto la teoría como el comportamiento dinámico y en régimen permanente.

### 1. Alcance general

- Tipo de máquina: motor síncrono trifásico, rotor de polos salientes (y opcionalmente rotor cilíndrico como segunda opción de modelo).
- Modo de operación: motor (no generador), conectado a una red trifásica balanceada.
- El simulador debe permitir:
  - Ver y modificar parámetros eléctricos, mecánicos y de control.
  - Ver cómo cambian las variables internas (corrientes, tensiones, ángulos, potencia, factor de potencia, velocidad, etc.).
  - Mostrar gráficas y diagramas de fasores relevantes.
  - Analizar tanto:
    - Régimen permanente (modelo fasorial).
    - Dinámica simplificada (modelo en ejes d–q con ecuaciones diferenciales).

### 2. Lenguaje, entorno y estructura

- Implementa el simulador en **[elige tú el entorno más adecuado, por ejemplo Python + interfaz gráfica sencilla (Tkinter, PyQt o similar) o interfaz web (HTML/JS)]**.
- Estructura el código en módulos o clases para separar:
  - Modelo del motor (parámetros y ecuaciones).
  - Núcleo de simulación numérica.
  - Interfaz de usuario.
  - Visualización de resultados (gráficos, fasores, curvas).

Explica brevemente en comentarios la organización del código.

### 3. Modelo físico–matemático

#### 3.1 Parámetros del motor

Incluye, como mínimo, estos parámetros editables:

- Eléctricos:
  - Tensiones de fase de línea: \( V_L \) (tensión de línea) o \( V_{fase} \).
  - Frecuencia eléctrica: \( f \).
  - Número de polos: \( p \).
  - Resistencias: \( R_s \) (estator), \( R_f \) (campo).
  - Reactancias sincronas: \( X_d \), \( X_q \) (para polos salientes) o \( X_s \) (para rotor cilíndrico).
  - Inductancias mutuas y de dispersión si usas modelo más detallado.
  - Corriente de excitación del rotor: \( I_f \) o tensión de campo \( V_f \).

- Mecánicos:
  - Momento de inercia del conjunto: \( J \).
  - Coeficiente de fricción / amortiguamiento: \( B \) (si se modela).
  - Par de carga mecánica: \( T_L \) (constante o función del tiempo).

- De operación:
  - Tipo de conexión: estrella/triángulo.
  - Modo de operación: subexcitado, nominal, sobreexcitado (ajustado mediante \( I_f \)).
  - Ángulo de carga eléctrico: \( \delta \).

#### 3.2 Relaciones básicas

Implementa y documenta las ecuaciones clave:

- Velocidad síncrona:
  - \( \omega_s = 2 \pi f \)
  - \( n_s = \dfrac{120 f}{p} \)

- Modelo fasorial en régimen permanente:
  - Ecuaciones para el fasor de fem interna \( \vec{E} \) y la corriente de línea \( \vec{I} \):
    - \( \vec{V} = \vec{E} + j X_s \vec{I} + R_s \vec{I} \) (modelo sencillo).
  - Explica cómo se obtiene el diagrama fasorial para subexcitación/sobreexcitación.

- Potencias y factor de potencia:
  - Potencia aparente: \( S = \sqrt{P^2 + Q^2} \).
  - Potencia activa: \( P = 3 V_{fase} I_{fase} \cos\phi \).
  - Potencia reactiva: \( Q = 3 V_{fase} I_{fase} \sin\phi \).
  - Factor de potencia: \( \cos\phi \), indicando adelanto/atraso.

- Par electromagnético en función del ángulo de carga (para modelo simplificado):
  - Motor síncrono clásico: \( T_e = \dfrac{3 V E}{\omega_s X_s} \sin\delta \) (o versión con \(X_d, X_q\) si usas polos salientes).
  - Muestra claramente la relación entre \( \delta \), \( T_e \), \( I_f \), \( V \) y \( X \).

- Modelo dinámico (ejes d–q, simplificado):
  - Plantea las ecuaciones en coordenadas d–q (Park):
    - Tensiones en d–q, corrientes, flujo, etc.
  - Ecuación mecánica:
    - \( J \dfrac{d\omega_m}{dt} = T_e - T_L - B \omega_m \)
  - Si es muy complejo, permite un modelo dinámico reducido (ej.: sólo ecuación mecánica usando un \(T_e(\delta)\) aproximado).

Comenta muy bien el código para que cada ecuación se identifique con la teoría.

### 4. Variables visibles e interdependencias

En la interfaz, quiero que se muestren en tiempo real (o al disparar la simulación):

- Variables de entrada (ajustables por el usuario):
  - \( V_L \) o \( V_{fase} \)
  - \( f \)
  - \( p \)
  - \( I_f \) o \( V_f \)
  - \( T_L \)
  - Parámetros \( R_s, X_d, X_q \) (o \(X_s\))
  - \( J, B \)

- Variables calculadas:
  - Velocidad mecánica \( \omega_m \) y en rpm \( n \), comparadas con \( \omega_s, n_s \).
  - Ángulo de carga \( \delta \).
  - Corriente de línea \( I \) y su ángulo respecto a la tensión.
  - Potencia activa \( P \), reactiva \( Q \), aparente \( S \).
  - Factor de potencia (indicando si es adelantado o atrasado).
  - Par electromagnético \( T_e \).
  - Deslizamiento aparente (si decides mostrarlo, aunque en síncrono ideal es 0).

Quiero que quede claro en la UI cómo:
- Cambiar \( I_f \) afecta:
  - \( \vec{E} \)
  - Factor de potencia
  - Corriente de línea
- Cambiar \( T_L \) afecta:
  - \( \delta \)
  - \( T_e \)
  - Estabilidad del motor (hasta el par máximo).
- Cambiar \( V \) o \( f \) afecta:
  - Flujo, corrientes, \( T_e \), etc.

### 5. Interfaz gráfica y visualizaciones

Implementa una interfaz donde se pueda:

1. **Ajustar parámetros** con sliders, cajas de texto o combo boxes:
   - \( V_L \), \( f \), \( I_f \), \( T_L \), \( R_s \), \( X_d \), \( X_q \), \( J \), etc.
   - Seleccionar tipo de operación: subexcitado, nominal, sobreexcitado (con presets que ajusten \( I_f \)).

2. **Ver gráficos**:
   - Curva par–ángulo \( T_e(\delta) \) con indicación del punto de operación.
   - Curva par–velocidad (aunque la velocidad en sincro sea casi fija, mostrar el punto de operación con diferentes cargas).
   - Evolución temporal de:
     - \( \omega_m(t) \)
     - \( T_e(t) \) y \( T_L(t) \)
     - \( P(t) \), \( Q(t) \), \( I(t) \) si se simulan transitorios.
   - Gráfico de factor de potencia vs corriente de excitación \( \cos\phi(I_f) \), mostrando región sub/sobre excitada.

3. **Diagrama fasorial**:
   - Representación gráfica de:
     - Tensión de fase \( \vec{V} \).
     - Fem interna \( \vec{E} \).
     - Corriente \( \vec{I} \).
     - Caída de tensión \( j X_s \vec{I} \) (y \( R_s \vec{I} \) si lo incluyes).
   - Actualizar el fasor en función de las variables cambiadas por el usuario.

### 6. Escenarios de simulación

Incluye al menos estos casos preconfigurados (presets):

1. **Arranque ideal** (suponiendo que de algún modo se engancha a síncrono):
   - Mostrar cómo la velocidad mecánica llega a la velocidad síncrona.
2. **Carga creciente**:
   - Aumentar \( T_L \) gradualmente y mostrar cómo crece \( \delta \) hasta cerca del par máximo.
3. **Cambio de excitación**:
   - Variar \( I_f \) desde subexcitado a sobreexcitado y mostrar:
     - Cambios en factor de potencia (de inductivo a capacitivo).
     - Cambios en la corriente de línea.
4. **Sobrecarga / pérdida de sincronismo** (si el modelo lo permite):
   - Mostrar que al exceder cierto par de carga, el motor no puede sostener el régimen síncrono.

### 7. Validación y explicación

- Incluye en el código o en un documento complementario:
  - Comparación cualitativa con curvas típicas de motor síncrono (par–ángulo, \( \cos\phi \) vs \( I_f \)).
  - Explicaciones en lenguaje técnico pero claro de:
    - Por qué el motor síncrono tiene velocidad fija.
    - Relación entre excitación y factor de potencia.
    - Estabilidad e inestabilidad en función del ángulo de carga \( \delta \).

- Comenta el código de forma abundante, indicando:
  - Qué ecuación se implementa en cada bloque.
  - Qué suposiciones se hacen (modelo simplificado, pérdidas ignoradas, etc.).

### 8. Entregables finales

Al final, entrega:

1. El código completo del simulador listo para ejecutar.
2. Instrucciones claras de:
   - Cómo instalar dependencias.
   - Cómo ejecutar la aplicación.
3. Un breve “manual de uso”:
   - Cómo cambiar parámetros.
   - Cómo interpretar gráficos y fasores.
   - Ejemplos de experimentos sugeridos (p. ej. “aumenta \( I_f \) y observa el cambio en \( \cos\phi \)”).

Tu objetivo es que el simulador sea a la vez:
- Didáctico (para entender el comportamiento físico del motor síncrono).
- Lo bastante riguroso como para servir de apoyo en un curso de máquinas eléctricas a nivel universitario.
