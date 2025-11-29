### Página 1: Arranque de Motor de Inducción

**Conceptos Generales**

Se denomina **arranque** al proceso de puesta en marcha de una máquina eléctrica. Para que esta operación pueda llevarse a cabo es necesario que el par de arranque sea superior al par resistente de la carga. De esta forma se obtiene un momento de aceleración que obliga a girar el rotor a una velocidad mayor hasta obtener el régimen permanente, que se da cuando se igualan los pares motor con el resistente.

El arranque va acompañado de un consumo elevado de corriente, hecho que se evidencia en el C. Equivalente (Circuito Equivalente), ya que $R_c$ (Resistencia de carga) se anula en ese instante, quedando el motor prácticamente en cortocircuito.

Las normas de los diferentes países establecen las máximas corrientes de arranque permitidas. Los valores varían con la potencia de la máquina y van desde **4,5 a 1,5** conforme se incrementa la potencia.

Para reducir la corriente de arranque se emplean distintos métodos, los cuales dependen también del tipo de rotor (Jaula de ardilla o Rotor bobinado).

En los motores con rotor en jaula de ardilla se usan:

**a) Arranque directo**

Este método se emplea en motores de pequeña potencia. El esquema de conexiones se muestra en la figura, donde el estator se conecta en estrella.

* **[Descripción del diagrama izquierdo]:** Se muestra la línea trifásica (R, S, T) bajando hacia un interruptor general manual y luego hacia las bobinas del estator ($U_1, V_1, W_1$).
* **[Descripción del diagrama derecho - Caja de bornes]:** Se muestra la configuración de la bornera para conexión Estrella. Los terminales $W_1, U_1, V_1$ reciben la alimentación, y los terminales $W_2, U_2, V_2$ (indicados como $Z, X, Y$ en el dibujo) están puenteados (cortocircuitados) horizontalmente.

**b) Arranque por Autotransformador**

En este método se intercala un autotransformador entre la red y el motor.
El proceso puede realizarse en escalones, con tensiones que van desde el 60, 75 y 100 por ciento de la tensión de línea.

* **[Descripción del diagrama]:** Se observan las líneas R, S, T conectadas a un autotransformador con varias tomas (taps). Un conmutador selecciona la toma para alimentar el estator del motor ($U_1, V_1, W_1$).

Como el par varía con el cuadrado de la tensión, el $Ta_{aut}$ (Par de arranque con autotransformador) se relaciona con el par de arranque directo ($Ta$) por la siguiente expresión:

$$Ta_{aut} = x^2 \cdot Ta$$

Donde $x$ indica la fracción de tensión respecto a la nominal ($U_N$).

**Ejemplo:**
Si en el arranque se aplica una tensión del 70% de $U_N$ (es decir, $x = 0,7$), el par de arranque con autotransformador será del **49%** del par de arranque directo al que se aplica $U_N$.

$$(0,7^2 = 0,49)$$


**c) Arranque por conmutación Estrella - Triángulo ($Y - \Delta$)**

Este método solo se puede utilizar en aquellos motores que estén preparados para funcionar en **triángulo** con la tensión de la red. La máquina se conecta en estrella en el momento del arranque y se pasa después a triángulo cuando está en funcionamiento.

Para facilitar la comprensión, en la figura se muestra un conmutador manual para alimentar los bobinados del estator del motor.

En arranque, se coloca el conmutador en la **posición 1** y se conectan los devanados en **estrella**.
Una vez que la máquina alcanza una velocidad estable, el conmutador se pasa conectando los devanados en **triángulo**.

**[Esquema del Conmutador Manual]**
*(El dibujo muestra las tres fases R, S, T conectando a través de un interruptor de dos posiciones a los bornes del motor. En una posición une los finales de bobina formando el centro de la estrella, y en la otra conecta principio con final de la siguiente bobina para el triángulo).*

Para analizar los valores que toman las distintas magnitudes, veamos las dos conexiones.

#### Esquema en Triángulo ($\Delta$)

*(Se muestra el circuito con las bobinas conectadas en delta)*

$$U_{f\Delta} = U_l$$
$$I_{f\Delta} = \frac{U_{f\Delta}}{Z} = \frac{U_l}{Z}$$
$$I_{l\Delta} = \sqrt{3} \cdot I_{f\Delta} = \sqrt{3} \cdot \frac{U_l}{Z}$$
$$T_\Delta = K \cdot U_{f\Delta}^2 = K \cdot U_l^2$$

*Donde:*
* $U_l$: Tensión de línea
* $U_f$: Tensión de fase
* $I_l$: Corriente de línea
* $I_f$: Corriente de fase
* $T$: Par o Cupla (Torque)

---

### Página 4: Relaciones y Conclusiones

#### Esquema en Estrella ($Y$) 
*(Se muestra el circuito con las bobinas conectadas en estrella)*

$$U_{fY} = \frac{U_l}{\sqrt{3}}$$
$$I_{fY} = \frac{U_{fY}}{Z} = \frac{U_l}{\sqrt{3} \cdot Z}$$
$$I_{lY} = I_{fY} = \frac{U_l}{\sqrt{3} \cdot Z}$$
$$T_Y = K \cdot U_{fY}^2 = K \cdot \left( \frac{U_l}{\sqrt{3}} \right)^2 = \frac{K \cdot U_l^2}{3}$$

#### Relaciones

Comparación entre los valores de Estrella ($Y$) y Triángulo ($\Delta$):

1.  **Tensiones:**
    $$\frac{U_{fY}}{U_{f\Delta}} = \frac{U_l / \sqrt{3}}{U_l} = \frac{1}{\sqrt{3}} \Rightarrow U_{fY} = \frac{U_{f\Delta}}{\sqrt{3}}$$

2.  **Corrientes de Fase:**
    $$\frac{I_{fY}}{I_{f\Delta}} = \frac{\frac{U_l}{\sqrt{3} \cdot Z}}{\frac{U_l}{Z}} = \frac{1}{\sqrt{3}} \Rightarrow I_{fY} = \frac{I_{f\Delta}}{\sqrt{3}}$$

3.  **Corrientes de Línea (Lo más importante para el arranque):**
    $$\frac{I_{lY}}{I_{l\Delta}} = \frac{\frac{U_l}{\sqrt{3} \cdot Z}}{\frac{\sqrt{3} \cdot U_l}{Z}} = \frac{1}{3} \Rightarrow I_{lY} = \frac{I_{l\Delta}}{3}$$

4.  **Par o Cupla:**
    $$\frac{T_Y}{T_\Delta} = \frac{\frac{K \cdot U_l^2}{3}}{K \cdot U_l^2} = \frac{1}{3} \Rightarrow T_Y = \frac{T_\Delta}{3}$$

**Conclusión:**

Entonces, el motor que esté preparado para trabajar en **Triángulo** (donde cada devanado de fase está construido para esa tensión) se conecta en **Estrella**. Recibe por fase una tensión $1/\sqrt{3}$ veces menor que la que recibe en la conexión Triángulo.

La cupla de arranque se reduce a la **tercera parte** y la corriente por fase en $1/\sqrt{3}$ veces.

---

### Control de Velocidad en Motores de Inducción

Desde el comienzo de la utilización de los motores eléctricos se ha intentado emplear el motor de inducción de **Jaula de Ardilla** por las ventajas que tiene éste sobre el motor de C.C. (Corriente Continua) y otras máquinas.

**A Saber:**
* Menor tamaño y Precio.
* Menor Complicación Constructiva (No tiene colector).
* Menor Requerimiento de Mantenimiento.
* No tiene Conmutación y se puede utilizar en atmósferas explosivas.

Como los distintos requerimientos implican el uso de la máquina a distintas velocidades, vamos entonces a analizar cómo controlar su velocidad.

A partir de la expresión que relaciona la velocidad del rotor $N$ [RPM] con el resbalamiento:

$$N = N_s (1 - s)$$

*Donde $N_s$ [RPM] es la velocidad sincrónica del Campo Magnético Rotante.*

Se deduce que las formas básicas de variar la velocidad de giro del motor son:

**I) Variando el deslizamiento $s$**
a) Control por variación de la tensión estatórica.
b) Control por variación de la corriente rotórica.

**II) Variando la velocidad sincrónica ($N_s$)**
$$N_s = 60 \frac{f}{P}$$
c) Variando el número de Polos ($P$).
d) Control por variación de la frecuencia ($f$).

---

### a) Variación del deslizamiento por control de la tensión estatórica

Al cargar un motor la velocidad se estabiliza en un valor para el cual el par motor se iguala al par resistente.

La expresión del par inducido ($T_{ind}$) es:

$$T_{ind} = \frac{P_{AG}}{\omega_s} = \frac{3 \cdot P}{\omega} \cdot I_{21}^2 \cdot \frac{R_{21}}{s}$$

*Con:*
$$\omega_s = \frac{\omega}{P} = \frac{2\pi f_1}{P}$$

Sabemos que la corriente rotórica referida al estator ($I_{21}$) es:

$$I_{21} = \frac{U_1}{(R_1 + \frac{R_{21}}{s}) + j(X_1 + X_{21})}$$

Y su módulo es:

$$|I_{21}| = \frac{U_1}{\sqrt{(R_1 + \frac{R_{21}}{s})^2 + (X_1 + X_{21})^2}}$$

Sustituyendo en la fórmula del par, se obtiene:

$$T_{ind} = 3 \cdot \frac{P}{2\pi f_1} \cdot \frac{U_1^2}{(R_1 + \frac{R_{21}}{s})^2 + (X_1 + X_{21})^2} \cdot \frac{R_{21}}{s}$$

La Cupla se maximiza cuando se minimiza el denominador. Derivando la cupla con respecto a $s$ e igualando a cero ($dT_{ind}/ds = 0$), podemos determinar el resbalamiento $S_{max}$ que determina la cupla máxima.

**Resultado:**

$$S_{max} = \frac{R_{21}}{\sqrt{R_1^2 + (X_1 + X_{21})^2}}$$

   ---

Lo que determina la $T_{ind(max)}$ (Par inducido máximo):

$$T_{ind(max)} = \frac{3 \cdot P}{2\pi f_1} \cdot \frac{U_1^2}{2 \left( R_1 + \sqrt{R_1^2 + (X_1 + X_{21})^2} \right)}$$

Puede apreciarse que el par es proporcional al **cuadrado de la tensión estatórica** para un determinado deslizamiento.

Reduciendo el voltaje de línea aplicada a los terminales del estator, el equilibrio se establece a una nueva velocidad menor que la anterior.
Se consigue regular la velocidad a base de **aumentar el deslizamiento**.

**[Gráfico de Curvas Par-Velocidad]**
*(El gráfico muestra varias curvas de par motor descendentes a medida que baja la tensión: $U_1, 0,75 U_1, 0,5 U_1, etc$. Se ve cómo el punto de cruce con la curva de "Par resistente" se mueve hacia la izquierda, reduciendo la velocidad y aumentando el deslizamiento $s$ hacia 1).*
* Eje Y: Par [N.m]
* Eje X: $S=1$ (Arranque) a $S=0$ (Sincronismo, $N_s$ RPM).

Este método de control de velocidad se utiliza a veces para controlar la velocidad de **pequeños motores de ventilación** porque tiene **bajo rendimiento**.

$$P_{conv} = (1 - s) P_{AG}$$

A medida que $s$ aumenta, la $P_{conv}$ (Potencia convertida) disminuye.

---

### Control por Variación de la Corriente Rotórica

*(Nota: Técnicamente es por variación de la resistencia del rotor).*

En los motores con **rotor bobinado**, es posible cambiar la forma de la curva Par-Velocidad mediante la inserción de resistores externos en el circuito del rotor, modificando el deslizamiento $s$ del punto de equilibrio entre el par motor y el par resistente, y controlar así la velocidad de operación.

* **Nota lateral:** Sin embargo, este método reduce la eficiencia de la máquina.
* **Nota lateral:** Se regula el deslizamiento mediante la variación de la resistencia del circuito del rotor.

**[Gráfico de Curvas con Resistencias]**
*(Se muestran curvas donde el par máximo se mantiene constante en magnitud, pero se desplaza hacia la izquierda a medida que aumenta la resistencia: $R, 2R, 3.5R$, etc. El par de arranque aumenta con la resistencia hasta cierto punto).*

De las ecuaciones que indican el resbalamiento para el cual se produce la cupla máxima ($S_{max}$), y la que indica el valor de la cupla máxima ($T_{max}$):

$$S_{max} = \frac{R_{21}}{\sqrt{R_1^2 + (X_1 + X_{21})^2}}$$

$$T_{max} = \frac{3P}{2\pi f_1} \cdot \frac{U_1^2}{2 \left( R_1 + \sqrt{R_1^2 + (X_1 + X_{21})^2} \right)}$$

Se observa que la cupla motora máxima es **independiente de $R_{21}$** (Resistencia rotórica), en tanto que el resbalamiento para el que se produce este máximo es **función de $R_{21}$**.

En condiciones normales de operación $(X_1 + X_{21}) \gg R_1$, por lo que podemos aproximar la $T_{max}$ a:

$$T_{max} \approx \frac{3P}{2\pi f_1} \cdot \frac{U_1^2}{2 (X_1 + X_{21})} = \frac{3P}{2 (2\pi)^2} \cdot \frac{U_1^2}{f_1^2 (L_1 + L_2)}$$

Esto indica que $T_{max}$ solo depende de la relación entre tensión y frecuencia $(U_1 / f_1)$.

Entonces, si se varía la tensión y la frecuencia de manera de mantener la relación $(U_1 / f_1)$ constante, no tendremos variaciones del máximo valor de la cupla.

---



### c) Variando el número de Polos

En algunos tipos de motores el devanado del estator está diseñado para que, mediante simples cambios en las conexiones de los bobinados, se pueda modificar el número de polos en la razón **2 a 1**.

Entonces es posible seleccionar cualquiera de las dos velocidades síncronas. El rotor, que casi siempre es del tipo de **Jaula de Ardilla**, reacciona produciendo un campo que tiene el mismo número de polos que el campo inductor del estator.

Los bobinados en las máquinas generalmente están divididos en dos mitades para cada fase como se indica en la figura.

**[Figura: Esquema de conexiones de bobinas]**
*(El dibujo muestra un esquema simplificado de una fase con dos grupos de bobinas y un interruptor que cambia la dirección de la corriente).*

* **(a) Conexión Serie (o corrientes en igual sentido):** Si conectamos las medias bobinas como en la figura (a), los flujos debidos a los campos de cada bobina se **suman** creando un par de Polos.
* **(b) Conexión Paralelo/Inversa:** Si en cambio conectamos las medias bobinas como en la figura (b), las líneas de flujo se cerrarán formando **2 pares de polos**.

---

#### Relación Frecuencia - Velocidad

En el primero de los casos, la frecuencia de los fasores de corriente y del campo giratorio tendrían la misma frecuencia.

En el segundo **caso**, cuando se cumple un ciclo eléctrico de $360^{\circ}$, el campo magnético rotante solo habrá recorrido $180^{\circ}$; por lo tanto, serán necesarios **2 ciclos eléctricos** para producir un ciclo geométrico (o mecánico).

Entonces:
$$f_s = \frac{f}{P} \quad (Hz)$$

*Donde:*
* $f_s$: Frecuencia del campo magnético rotante o Síncrona.
* $f$: Frecuencia de la red.
* $P$: Número de **pares** de Polos.

Las velocidades se definen como:
* $N_s$: Velocidad del Campo giratorio o Síncrono en [RPM].
* $\omega_s$: Velocidad del Campo giratorio o Síncrono en [rad/s].

$$\omega_s = 2\pi f_s = \frac{2\pi f}{P} \quad [rad/s]$$

$$N_s = 60 \cdot f_s = 60 \cdot \frac{f}{P} \quad [RPM]$$

Entonces, si variamos la cantidad de **pares de polos**, podemos variar la velocidad de Sincronismo. Como se observa en la siguiente tabla para $f = 50 Hz$:

| Par de Polos ($P$) | Polos Totales ($2P$) | $N_s$ [RPM] |
| :---: | :---: | :---: |
| **1** | 2 | **3000** |
| **2** | 4 | **1500** |
| **3** | 6 | **1000** |
| **4** | 8 | **750** |
| **5** | 10 | **600** |
| **6** | 12 | **500** |

---
> 📝 *Notas:*
> **Conexión Dahlander:**

> * Lo que describen tus apuntes (cambiar la conexión de bobinas para duplicar los polos) es el principio del **Motor Dahlander**.
> * **Explicación visual:** Imagina dos bobinas. Si la corriente circula en el 
> mismo sentido en ambas, crean un campo magnético amplio (Norte-Sur grande). Si inviertes una, creas dos campos más pequeños (Norte-Sur-Norte-Sur), duplicando los polos y reduciendo la velocidad a la mitad. 
 

Cuando se invierte la dirección del flujo de corriente en el devanado inferior del estator (porque se invierte el conexionado), el campo magnético dejará el estator tanto en el devanado superior como en el devanado inferior, constituyendo en cada caso un **polo norte**, y regresa al estator entre los 2 devanados produciendo un **par de polos sur**.

El rotor en un motor como este es de **Jaula de Ardilla**, y este siempre tiene tantos polos inducidos como polos tiene el estator y por lo tanto se puede adoptar cuando cambia el número de polos en el estator.

Como se ha dicho anteriormente, generalmente los bobinados están divididos en 2 mitades para cada fase como se indica a continuación, pudiéndose obtener 4 disposiciones posibles.

**[Diagramas de Conexión]**
*(Los dibujos muestran las bobinas $U-U'$ y $X-X'$. Arriba se muestran en serie y abajo en paralelo).*

Los bobinados se pueden conectar en **serie** o en **paralelo**.

De modo adicional, las fases se pueden conectar en **Estrella** o en **Triángulo**, lo que da por resultado ocho combinaciones posibles.

* El cambio de una conexión Delta ($\Delta$) a Estrella ($Y$) reduce la tensión de fase en $\sqrt{3}$.
* Por otra parte, el cambio de conexión de los devanados de **Serie a Paralelo** duplica el voltaje aplicado a cada bobina y, por lo tanto, se **duplica la densidad de flujo** en el entrehierro.

---

### Control de Velocidad Sincrónica por Control Escalar (Voltaje / Frecuencia)

Este es uno de los métodos de regulación más completos para motores de CA, tanto Síncronos como Asíncronos.
El procedimiento permite regular la velocidad desde valores superiores a la normal hasta velocidad nula, con muy buen rendimiento y manteniendo un par elevado.

A estas ventajas se añade el hecho de poder usar el motor de **Jaula de Ardilla**, que posee robustez, compacticidad y buena respuesta dinámica debido al reducido momento de inercia del motor.

Si la frecuencia eléctrica aplicada al estator del motor de inducción se cambia, la velocidad de rotación de su campo magnético $N_s$ cambiará en proporción directa al cambio de la frecuencia eléctrica:

$$f_s = \frac{f}{P} \quad (Hz)$$

Y el punto de vacío en la característica de la Curva del Momento torsión - Velocidad cambiará:

$$N_s = 60 \cdot f_s = 60 \cdot \frac{f}{P} \quad (RPM)$$

La velocidad síncrona $N_s$ para condiciones normales de funcionamiento se la conoce como **Velocidad Base**.

Usando el Control de frecuencia variable, es posible ajustar la velocidad del motor ya sea por encima o por debajo de la velocidad base. Sin embargo, es importante mantener los valores de Voltajes y Momento de Torsión dentro de ciertos límites mientras se varía la frecuencia para garantizar una operación segura.

---

### 📝 Notas

1.  **Conexión Dahlander (Par constante vs Potencia constante):**
    * En el texto donde menciona que al pasar de serie a paralelo "se duplica la densidad de flujo", es un punto crítico. En la práctica, para evitar la saturación magnética (que el núcleo no aguante más flujo), si conectas las bobinas en paralelo (para la velocidad alta), el diseño del motor Dahlander suele cambiar también de Triángulo a Estrella (o viceversa) para compensar los voltajes.
    * Existen dos tipos principales de conexión Dahlander:
        * **Par Constante:** Para cargas como grúas o cintas transportadoras.
        * **Par Variable (Ventiladores):** Donde el par cuadrático aumenta con la velocidad.

2.  **Sobre el Control Escalar (V/f):**
    * El título "Control Escalar" es muy importante. Se le llama así porque solo controlamos la **magnitud** del voltaje y la frecuencia, sin controlar la fase (posición vectorial) del flujo, que sería "Control Vectorial".
    * La última frase del apunte es la clave de todo este método: *"Es importante mantener los valores de Voltaje... dentro de ciertos límites"*. Esto se refiere a mantener la relación $V/f = constante$. Si bajas la frecuencia ($f$) sin bajar el voltaje ($V$), el motor se quema (saturación). Si subes la frecuencia sin poder subir más el voltaje (zona de debilitamiento de campo), el par motor cae. " (parecía un error de pluma), corregido a "mientras se varía".

    ---
