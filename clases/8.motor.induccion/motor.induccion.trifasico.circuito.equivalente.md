 

**Circuito Equivalente del Motor**

En toda máquina es importante determinar las características de entrada y de salida de la misma.

La potencia entregada a la carga es **potencia mecánica**; por lo tanto, en el análisis de la potencia mecánica de salida interesa determinar la **cupla motora** y la **velocidad de giro** en función de las variaciones de la carga.

La potencia absorbida de la red eléctrica es una **potencia eléctrica**; por lo tanto, será necesario estudiar las características de la energía eléctrica que la máquina recibe de la línea.

En razón a que la tensión de línea se supone constante (no varía con la carga), simplemente será necesario entonces estudiar las variaciones de la **corriente**, porque ello nos dará una idea de las variaciones de la potencia eléctrica de entrada.

Con el propósito de determinar estos valores de una manera simple, buscaremos modelizar la máquina mediante un **circuito eléctrico equivalente** que represente fielmente el funcionamiento del motor asíncrono.

El motor de inducción es una máquina **inductivamente** excitada*, en razón a que solo recibe potencia el estator, y este, mediante una acción transformadora (mecanismo de inducción), transfiere energía al rotor (induce voltajes y corrientes) que, como se ve, tiene un funcionamiento similar a un transformador.

Esto nos induce a pensar que el circuito equivalente del motor terminará por ser muy similar al de un transformador.

Para hacer nuestro razonamiento en las condiciones más simples, vamos a suponer la creación de un **campo magnético rotante** a partir de un motor bifásico, porque en un estator bifásico .tenemos dos arrollamientos **magnéticamente independientes** porque los ejes de sus arrollamientos son perpendiculares entre sí. La corriente que absorbe una fase no afecta a la corriente que toma la otra fase; es decir, se comportan con respecto a la línea como cargas pasivas independientes.

En contraposición a lo que sucede con un estator trifásico, en el cual hay 3 arrollamientos desfasados $120^\circ$ y hay acoplamiento magnético entre los arrollamientos, por lo tanto la corriente que toma una fase no es independiente de las que toman las otras fases.

*[Diagrama: Esquema de Fase A y Fase B conectadas a líneas]*

Como las dos fases son iguales, basta con hacer el análisis para una de ellas.

Vemos que cada fase puede tomarse como un **transformador monofásico**, donde el estator es el circuito primario y el rotor el circuito secundario, vinculados por un circuito magnético. Pero existe una diferencia fundamental con el transformador, y es que en la máquina estática no existe movimiento entre los arrollamientos, en tanto que en el caso del motor, el secundario está en **movimiento relativo** con respecto al primario.

*[Diagrama: Esquema simplificado de una fase]*

Esto trae aparejado algunos cambios que debemos considerar, a saber:
 
**a) Frecuencia de las corrientes inducidas**

Si el rotor está **bloqueado**, la frecuencia de las corrientes inducidas en el rotor ($f_2$), producida por la velocidad de deslizamiento $N_R$, es igual a la del estator ($f_1$).

$$f_1 = \frac{N_S \cdot P}{60}$$

> *Como $N_R = N_S - N$, para $N=0 \Rightarrow N_R = N_S$*

Entonces:
$$f_2 = \frac{N_R \cdot P}{60} = \frac{N_S \cdot P}{60} = f_1$$

Donde:
* $N_S$: Velocidad sincrónica (RPM)
* $N$: Velocidad del rotor (RPM)
* $P$: Número de pares de polos del estator

Si el rotor está **en marcha**, la frecuencia de las corrientes inducidas en el rotor será función de la diferencia de velocidades, o sea, de la velocidad de deslizamiento $N_R$.

Será:
$$N_R = N_S - N$$

$$f_2 = \frac{N_R \cdot P}{60} = \frac{N_R}{N_S} \cdot \frac{N_S \cdot P}{60} = S \cdot f_1$$

Recordando que el resbalamiento es $S = \frac{N_S - N}{N_S} = \frac{N_R}{N_S}$.

Es decir, la frecuencia de las corrientes inducidas en el rotor es **función del deslizamiento**.

**b) Variación del voltaje inducido**

Como consecuencia del movimiento relativo entre los campos magnéticos del rotor y del estator, se produce una variación del voltaje inducido en el rotor.

El mayor movimiento relativo se da cuando el rotor se encuentra detenido o bloqueado, por lo cual el voltaje inducido en el rotor alcanza su valor máximo.

Si llamamos $E_2$ al voltaje inducido en el rotor cuando este está detenido:

$$E_2 = 4,44 \cdot K_B \cdot N_2 \cdot f_2 \cdot \phi_m$$

Y como $f_2 = f_1$ (en rotor bloqueado):
$$E_2 = 4,44 \cdot K_B \cdot N_2 \cdot f_1 \cdot \phi_m$$

Donde:
* $N_2$: Número de espiras del rotor
* $K_B$: Factor de bobinado
* $\phi_m$: Flujo máximo del campo rotante del estator

---

### Página 17

La tensión inducida en el rotor cuando este está en **movimiento** es:

$$E_{2S} = 4,44 \cdot K_B \cdot N_2 \cdot f_2 \cdot \phi_m = 4,44 \cdot K_B \cdot N_2 \cdot S \cdot f_1 \cdot \phi_m$$

Por lo tanto:
$$E_{2S} = S \cdot E_2$$

Como se observa, la tensión inducida en el rotor es función de la frecuencia y directamente proporcional al resbalamiento.
El menor voltaje inducido en el rotor (0V) se produce cuando el rotor se mueve a la velocidad del campo rotante (no hay movimiento relativo).

**c) Reactancia de dispersión**

Otro elemento afectado por la diferencia de velocidades en el circuito del rotor es la **reactancia de dispersión**. Esta depende de la inductancia $L_2$ y de la frecuencia $f_2$ del voltaje inducido en el rotor, que varía con $S$. Por lo tanto:

$$X_{2S} = 2\pi \cdot f_2 \cdot L_2 = 2\pi \cdot S \cdot f_1 \cdot L_2$$

Llamando $X_2 = 2\pi \cdot f_1 \cdot L_2$ a la reactancia a rotor bloqueado (donde $f_2 = f_1$), resulta:

$$X_{2S} = S \cdot X_2$$

Por lo que la impedancia de cada fase del rotor para cualquier velocidad se expresa:

$$Z_{2S} = R_2 + j X_{2S} = R_2 + j S X_2$$

Teniendo en cuenta entonces los efectos que produce el resbalamiento sobre la reactancia y la tensión inducida en el rotor, y considerando la similitud que tiene esta máquina con el transformador, podemos esquematizar el **circuito equivalente por fase** del motor asíncrono de la siguiente forma:

*[Aquí aparece el diagrama del circuito equivalente exacto, mostrando el lado del estator ($R_1$, $X_1$, rama de magnetización) y el lado del rotor ($R_2$, $S X_2$, $E_{2S}$), indicando la carga mecánica]*

---  
Como vemos, este circuito es muy semejante al de un **transformador**, solo que la relación de transformación es variable y es función de $S$ (resbalamiento); y en lugar de una carga eléctrica se tiene una **carga mecánica**.

Como en cualquier transformador, hay una cierta resistencia y reactancia de dispersión en el bobinado primario (estator).

Donde con $R_1$ materializamos en el circuito equivalente las pérdidas que se producen por efecto Joule al recorrer la corriente el bobinado primario, provocando una caída de tensión.

Y con $X_1$ la caída de tensión producida por las líneas de flujo del estator (primario) que no concatenan al rotor (secundario) y se cierran a través del aire.

De la misma manera tenemos en cuenta estos efectos en el secundario (Rotor) con $R_2$ y $X_2$.

Como en cualquier transformador con núcleo de hierro, el flujo en la máquina está relacionado con el voltaje aplicado $E_1$.

Como en el motor el **entrehierro** es mayor que en un transformador, la **reluctancia** $\mathcal{R}$ se incrementa enormemente, lo que hace que se debilite el flujo y por ende el acoplamiento entre los bobinados primario y secundario.

*[Gráfico: Curva de Magnetización - Comparación entre Transformador y Motor de Inducción]*
> Se muestra que para un mismo flujo $\phi$, el motor requiere mucha más fuerza magnetomotriz (FMM) debido a la mayor reluctancia.
> $$\phi = \frac{FMM}{\mathcal{R}}$$

A mayor reluctancia se requiere **mayor corriente de magnetización** para lograr un nivel de flujo determinado. Por lo tanto, la **reactancia de magnetización** $X_0$ en el circuito equivalente del motor tendrá un valor **mucho menor** que el que correspondería a un transformador.

Con $R_0$ materializamos todas las pérdidas que se producen en el núcleo debido a la acción de las corrientes parásitas de Foucault y al fenómeno de histéresis.
Como estas son función lineal y cuadrática de la frecuencia, es lícito considerarlas en el principio del modelo porque $f_2$, cuando $N$ es cercana a $N_S$, es de 4 o 5 Hz.

El voltaje primario interno del estator $E_1$ se acopla al secundario $E_{2S}$ como en un transformador ideal con relación de espiras $K$.

En un motor con rotor bobinado esta se puede determinar como la relación entre el número de conductores por fase del estator y el número de conductores por fase del rotor, modificado por... 

...cualquier diferencia de factores de paso y de distribución.

En un motor con rotor a **jaula de ardilla** es difícil determinar $K$, porque no hay bobinados en el rotor. Teniendo en cuenta que el rotor actúa como un "espejo constructivo" del estator, podemos tomar $K=1$, lo que indica la misma cantidad de conductores activos en el rotor que en el estator.

Si en el circuito de la figura reducimos la **malla** del secundario al primario, nos queda el siguiente circuito:

**Valores referidos al primario:**
* $E_{21} = K \cdot E_2$
* $I_{21} = \frac{-I_2}{K}$
* $R_{21} = K^2 \cdot R_2$
* $X_{21} = K^2 \cdot X_2$

Donde los valores dependientes del resbalamiento son:
$$E_{21S} = S \cdot E_{21}$$
$$X_{21S} = S \cdot X_{21}$$

*[Diagrama del circuito con los valores referidos]*

Por lo tanto, la corriente que circula por una fase del rotor en marcha es:

$$I_{21} = \frac{S \cdot E_{21}}{R_{21} + j \cdot S \cdot X_{21}}$$

Dividiendo numerador y denominador por $S$:

$$I_{21} = \frac{E_{21}}{\frac{R_{21}}{S} + j \cdot X_{21}}$$

Lo que nos permite pasar al siguiente circuito:

*[Diagrama del Circuito Equivalente Final por Fase]*
> Se muestra el circuito donde la reactancia es constante ($X_{21}$) y la resistencia es variable ($\frac{R_{21}}{S}$).

Donde se observa que es posible tratar todos los efectos debidos a la variación de velocidad del rotor como causados por una impedancia variable alimentada con una fuente de voltaje constante.

En este circuito, la f.e.m. y la reactancia en el secundario no son más funciones del resbalamiento, lo que se ha obtenido mediante la introducción de una **resistencia variable en función de S** que es:

$$\frac{R_{21}}{S}$$

--- 
 

$$\frac{R_{21}}{S} = \frac{R_{21}}{S} + R_{21} - R_{21} = R_{21} + R_{21} \left( \frac{1-S}{S} \right)$$

Pasamos a un modelo en el que todos los elementos del secundario son independientes del resbalamiento y el único elemento que depende de $S$ es la **resistencia ficticia** $R_c = R_{21} \left( \frac{1-S}{S} \right)$ que reemplaza a la **carga mecánica**.

*[Diagrama: Circuito equivalente exacto con la carga separada]*
> Se muestra el rotor con $R_{21}$ (pérdidas cobre) y $R_c$ (potencia mecánica) en serie.

Este modelo permite separar la **Potencia de entrehierro** por fase ($P_{AG}$), que se disipa en $\frac{R_{21}}{S}$, en:
1.  Las **pérdidas en el cobre** disipadas en el rotor mediante $R_{21}$.
2.  La **Potencia eléctrica** ($P_{conv}$) que se convierte en mecánica para impulsar el eje del motor, disipada en la resistencia de carga ficticia $R_c = R_{21} \left( \frac{1-S}{S} \right)$.

Un modelo que permite simplificar el cálculo de la corriente primaria se obtiene trasladando la rama en derivación al principio del circuito, constituyendo un **circuito equivalente aproximado**.

Estos modelos nos permiten estudiar las características que sufre la energía eléctrica al atravesar la máquina desde el punto de vista eléctrico.

*[Diagrama: Circuito equivalente aproximado]*
> La rama de magnetización ($R_0, X_0$) se ha movido a los bornes de entrada $U_1$.

---

### Cálculo de Corrientes

Para determinar la potencia absorbida por la máquina de la red, solo será necesario determinar la **corriente de la red**, porque la tensión de línea se supone constante frente a las variaciones de la carga.

Si observamos el circuito equivalente aproximado para realizar el cálculo de la corriente primaria $I_1$, vemos que este está constituido por dos componentes:

$$\bar{I}_1 = \bar{I}_0 + \bar{I}_{21}$$

Donde $\bar{I}_0 = \frac{U_1}{Z_0}$ es la **corriente de vacío**, que es la corriente que la máquina toma de la red cuando el motor gira a una velocidad $\omega$ muy próxima a la velocidad del campo rotante $\omega_S$. Esto hace que el resbalamiento $S \approx 0$ y $R_c \Rightarrow \infty$; por lo tanto $I_{21} \approx 0$. Como se observa, $I_0$ es independiente de $S$.

El término $\bar{I}_{21}$ representa la **corriente rotórica referida al primario**.

$$\bar{I}_{21} = \frac{U_1}{ (R_1 + R_{21}) + R_{21}\left(\frac{1-S}{S}\right) + j(X_1 + X_{21}) }$$

Como se observa, esta corriente depende del resbalamiento $S$, por lo tanto varía con la velocidad del rotor.

Para analizar sus variaciones con la carga vamos a calcular su **módulo**:

$$|I_{21}| = \frac{U_1}{ \sqrt{ \left[ R_1 + R_{21} + R_{21}\left(\frac{1-S}{S}\right) \right]^2 + [X_1 + X_{21}]^2 } }$$

> *Nota:* Simplificando la parte resistiva del denominador, recuerda que $R_1 + R_{21} + R_{21}(\frac{1-S}{S})$ es matemáticamente igual a $R_1 + \frac{R_{21}}{S}$.

---
 
### Análisis Matemático

**Analizando la impedancia de la rama vemos que:**

*[Diagrama: Triángulo de Impedancias]*
> Hipotenusa: $Z$ (Impedancia total)
> Cateto vertical: $X_1 + X_{21}$
> Cateto horizontal: $R_1 + R_{21} + R_{21}(\frac{1-S}{S})$
> Ángulo: $\varphi_{21}$

Del triángulo de impedancias obtenemos el seno del ángulo:
$$\sin \varphi_{21} = \frac{X_1 + X_{21}}{\sqrt{\left[ R_1 + R_{21} + R_{21}(\frac{1-S}{S}) \right]^2 + [X_1 + X_{21}]^2}}$$

Tanto el módulo como el ángulo $\varphi_{21}$ varían con $S$ (resbalamiento).

Operando con el módulo de la corriente $|I_{21}|$ se tiene:

$$|I_{21}| = \frac{U_1}{\sqrt{\left[ R_1 + R_{21} + R_{21}(\frac{1-S}{S}) \right]^2 + [X_1 + X_{21}]^2}}$$

Multiplicamos y dividimos por $(X_1 + X_{21})$:

$$|I_{21}| = \frac{U_1}{(X_1 + X_{21})} \cdot \underbrace{\frac{(X_1 + X_{21})}{\sqrt{\dots}}}_{\sin \varphi_{21}}$$

$$|I_{21}| = \frac{U_1}{(X_1 + X_{21})} \cdot \sin \varphi_{21}$$

Esta expresión representa la **ecuación de una circunferencia** de diámetro:
$$D = \frac{U_1}{X_1 + X_{21}}$$

Este diámetro representa la intensidad de la corriente rotórica referida al primario en el caso particular en que las **resistencias rotóricas y estatóricas fuesen nulas** y el motor tenga el rotor bloqueado ($S=1$). Es decir, se trata de una corriente reactiva pura (deswatada*) y representa al fasor $I_{21}$ en una condición irreal, pero representa una situación límite para $S=1$ y resistencias nulas.

Para estados de carga variable, que hacen que la velocidad del rotor $\omega$ tome valores que van desde cero (rotor detenido, $S=1$) hasta la velocidad sincrónica ($\omega_S$, $S=0$), varía el ángulo $\varphi_{21}$ y con él varía el extremo del fasor $I_{21}$ describiendo un **círculo**.

Haciendo la aclaración que para la condición de rotor detenido ($S=1$), el lugar geométrico correspondiente ($P_{cc}$) no coincide con el diámetro de la circunferencia porque la impedancia que presenta la rama no es inductiva pura, sino que tiene una componente resistiva y el ángulo $\varphi_{21} \neq 90^\circ$.

> *Nota:* "Deswatada" es un término antiguo/técnico para referirse a una corriente que no produce potencia activa (Wattios), es decir, puramente reactiva.

---

### Análisis Gráfico

*[Diagrama: Diagrama Circular o de Heyland]*
> Se muestra el eje vertical de tensión $U_1$.
> El fasor $I_0$ (corriente de vacío) constante.
> El fasor $I_{21}$ que recorre el semicírculo.
> El fasor total $I_1$ que es la suma vectorial.

Si al fasor $I_{21}$, como se muestra en la gráfica precedente, le sumamos el fasor $I_0$ que representa la corriente de vacío, obtenemos la corriente $I_1$ que la máquina toma de la línea.

**1. Punto O (Marcha en vacío):**
El punto **O** corresponde a la marcha del motor en vacío (sin carga en el eje).
* En el rotor en sincronismo: $\omega = \omega_S$ o $n = n_S \Rightarrow S = 0$.
* Lo que impone una $R_c = R_{21}(\frac{1-S}{S})$ infinita.
* Por lo tanto $I_{21} = 0 \Rightarrow I_1 = I_0$.

**2. Punto $P_{cc}$ (Rotor detenido):**
Otro punto importante que podemos identificar en el diagrama es $P_{cc}$ (Punto de Cortocircuito), que corresponde a rotor detenido.
* Es decir: $\omega = 0$ o $n = 0 \Rightarrow S = 1 \Rightarrow R_c = 0$.
* Para este caso, **condición de arranque**, $I_{21}$ es máxima.
* Entonces la corriente $I_{arranque}$ puede ser de varios órdenes superior* a la corriente $I_1$ para una condición normal de carga.

> *Nota:* Cuando el texto dice "varios órdenes superior", en el contexto de ingeniería de motores, se refiere a que la corriente de arranque es **varias veces mayor** (típicamente de 5 a 7 veces la corriente nominal), no necesariamente órdenes de magnitud logarítmicos (potencias de 10).

---

 
### Potencia y Par

Sabemos que $Pot = Cupla \times Velocidad \ angular$.

Expresando la Cupla $T$ en $[Newton-metro]$ y la velocidad angular $\Omega$ en $[radianes/s]$ obtenemos la potencia en $[Watts]$.

$$P_{[W]} = T_{[N \cdot m]} \cdot \Omega_{[rad/s]}$$

$$P_{[W]} = 1,03 \cdot T_{[kgm]} \cdot N_{[RPM]}$$

Si a la **Potencia de Conversión** por fase $P_{conv(F)}$ le sumamos las pérdidas que por efecto Joule se disipan en el Cobre del rotor, obtenemos la **Potencia de Entrehierro** por fase $P_{AG(F)}$, que es la potencia que transfiere el estator al rotor por el mecanismo de inducción.

$$P_{AG(F)} = P_{conv(F)} + R_{21} \cdot I_{21}^2 = R_{21} \left(\frac{1-S}{S}\right) I_{21}^2 + R_{21} \cdot I_{21}^2$$

Simplificando:
$$P_{AG(F)} = \frac{R_{21}}{S} \cdot I_{21}^2$$
$$P_{cu \ rot(F)} = R_{21} \cdot I_{21}^2$$

Para calcular la potencia de entrehierro total $P_{AG}$ debemos multiplicar por tres la $P_{AG(F)}$.

$$P_{AG} = 3 \cdot \frac{R_{21}}{S} \cdot I_{21}^2$$

A esta potencia se la llama **Watts Sincrónicos**, porque son los watts que transfiere el Campo Rotante al rotor.

Si observamos el circuito, esta potencia es la que se disipa en el resistor $\frac{R_{21}}{S}$ en el circuito de una fase, la cual debe multiplicarse por tres para incluir las 3 fases.

Por otra parte:

$$P_{AG} = P_{entrada} - P_{\text{pérdidas Cu estator}} - P_{\text{pérdidas núcleo}}$$

---

### Página 23 (Balance de Potencias)

Nótese que la potencia que desarrolla la resistencia ficticia $R_c = R_{21} \left(\frac{1-S}{S}\right)$ al ser atravesada por la corriente $I_{21}$, tiene por fuerza que ser la potencia que el motor desarrolla en el eje en forma mecánica para una fase.

Esta potencia, que llamamos **Potencia de Conversión** $P_{conv}$, es la que se convierte en **Potencia Útil** o de **Salida**, a la que se suman las pérdidas mecánicas por fricción y ventilación* ($P_{fyw}$) y las pérdidas misceláneas ($P_{mis}$).

> *Nota de corrección:* En el original dice "Vendaval", que es una traducción muy literal del inglés "Windage". En electrotecnia en español, el término correcto es pérdidas por **ventilación** o rozamiento con el aire. También corregí "micolaneas" por "misceláneas".

$$P_{conv} = P_{salida} + P_{fyw} + P_{mis}$$

La $P_{conv}$ total es tres veces la $P_{conv}$ por fase.

$$P_{conv} = 3 \cdot R_{21} \left(\frac{1-S}{S}\right) \cdot I_{21}^2$$

Reemplazando $I_{21}$ por su expresión:
$$I_{21} = \frac{U_1}{\sqrt{\left(R_1 + \frac{R_{21}}{S}\right)^2 + (X_1 + X_{21})^2}}$$

Obtenemos la fórmula final:

$$P_{conv} = 3 \cdot R_{21} \left(\frac{1-S}{S}\right) \cdot \frac{U_1^2}{\left(R_1 + \frac{R_{21}}{S}\right)^2 + (X_1 + X_{21})^2}$$

---

### Resumen de Fórmulas Clave de esta parte:

1.  **Potencia de Entrehierro ($P_{AG}$):** Es la potencia total transferida al rotor.
    * $P_{AG} = 3 \cdot I_{21}^2 \cdot \frac{R_{21}}{S}$
2.  **Pérdidas en el Cobre del Rotor ($P_{cu2}$):**
    * $P_{cu2} = 3 \cdot I_{21}^2 \cdot R_{21} = S \cdot P_{AG}$
3.  **Potencia de Conversión ($P_{conv}$):** Es la potencia mecánica bruta.
    * $P_{conv} = P_{AG} - P_{cu2} = (1-S) \cdot P_{AG}$
 -------------

### Página 24

**Pérdidas en el estator**

Las pérdidas en el cobre del estator son las que disipa el resistor $R_1$ al ser atravesado por la corriente $I_{21}$ (en el modelo aproximado) y las podemos calcular:

$$P_{cu \ est} = 3 \cdot R_1 \cdot I_{21}^2$$

Las pérdidas en el núcleo debidas a la Histéresis y a las corrientes parásitas de Foucault las podemos determinar:

$$P_{nucleo} = 3 \cdot \frac{U_1^2}{R_0}$$

Si comparamos las expresiones de $P_{conv}$ y $P_{AG}$ se observa:

$$P_{conv} = (1-S) P_{AG}$$

Entonces, si a la $P_{AG}$ le sumamos las $P_{cu \ est}$ y las $P_{nucleo}$ podemos determinar la potencia de entrada al motor, o sea, la que este absorbe de la red.

**Momento o Cupla Inducida**

El momento inducido o Cupla inducida $T_{ind}$ en una máquina se define como el momento generado por la conversión de la potencia eléctrica $P_{conv}$ en potencia mecánica interna.

Este momento $T_{ind}$ difiere del momento realmente disponible en el eje del motor $T_{util}$ en una diferencia igual a la suma de los momentos de fricción y ventilación* antagónicos al de torsión.

> *Nota:* En el original dice "vendaval", el término técnico correcto es **ventilación** o rozamiento con el aire ($P_{fyw}$ = friction and windage).

Entonces el momento de Torsión Inducido se obtiene:

$$T_{ind} = \frac{P_{conv}}{\omega}$$

Si reemplazamos:
1.  $\omega = (1-S)\omega_S$
2.  $P_{conv} = (1-S)P_{AG}$

Tenemos:

$$T_{ind} = \frac{(1-S)P_{AG}}{(1-S)\omega_S} = \frac{P_{AG}}{\omega_S}$$

---

### Página 25

**Potencia Útil y Par de Salida**

La potencia útil o potencia de salida $P_S$:

$$P_S = P_{conv} - P_{fyw} = T_{ind} \cdot \omega - T_{fyw} \cdot \omega$$

$$P_S = (T_{ind} - T_{fyw}) \cdot \omega$$

Siendo $P_{fyw}$ las pérdidas por fricción y ventilación. La cupla de salida $T_{sal}$ es:

$$T_{sal} = \frac{P_S}{\omega} = T_{ind} - T_{fyw}$$

**Ecuación General del Par (Cupla)**

Si reemplazamos la corriente $I_{21}$ obtenida del circuito equivalente aproximado en la expresión de la Cupla inducida $T_{ind}$:

$$I_{21} = \frac{U_1}{\sqrt{\left( R_1 + \frac{R_{21}}{S} \right)^2 + (X_1 + X_{21})^2}}$$

Obtenemos:

$$T_{ind} = \frac{3 \cdot R_{21}}{\omega_S \cdot S} \cdot \left[ \frac{U_1^2}{\left( R_1 + \frac{R_{21}}{S} \right)^2 + (X_1 + X_{21})^2} \right]$$

**Cupla Máxima y Resbalamiento Crítico**

Para averiguar para qué valor de $S$ la cupla es máxima, derivamos e igualamos a cero: $\frac{dT_{ind}}{dS} = 0$, de donde obtenemos el resbalamiento máximo o crítico ($S_{max}$):

$$S_{max} = \frac{R_{21}}{\sqrt{R_1^2 + (X_1 + X_{21})^2}}$$

Sustituyendo el valor de $S_{max}$ en la expresión de la cupla inducida y operando se tiene la **Cupla Máxima**:

$$T_{ind \ max} = \frac{3}{\omega_S} \cdot \frac{U_1^2}{2 \left[ \sqrt{R_1^2 + (X_1 + X_{21})^2} + R_1 \right]}$$

**Conclusiones:**
Se observa que el máximo es **independiente de la resistencia del rotor** ($R_2$ o $R_{21}$) y es directamente proporcional al **cuadrado del voltaje** suministrado ($U_1^2$) y tiene una relación inversa a la magnitud de las **reactancias** del estator y del rotor.

---
 
### Página 26

Por lo tanto, mientras **menores sean** las reactancias de dispersión, mayor será la cupla de torsión.

Entonces, si se desea que la cupla máxima se produzca en el momento de arranque ($S=1$), reemplazamos este valor en $S_{max}$.

Como en la práctica $R_1 \ll (X_1 + X_{21})$, se debe cumplir:
$$R_{21} = X_1 + X_{21}$$

En la práctica, como $R_{21} < (X_1 + X_{21})$, se debe agregar en el arranque una **Resistencia exterior** $R_A$ a la resistencia del rotor para que se cumpla:

$$R_A + R_{21} = X_1 + X_{21}$$

**Diagrama de Flujo de Potencia**

Utilizando los cálculos anteriores vamos a analizar cómo se transfiere la potencia en la máquina, para lo cual vamos a ver el **diagrama de Flujo de Potencia y Pérdidas**.

En el diagrama se indica que la potencia eléctrica de entrada se da a través de un sistema de tensiones trifásicas.
1.  Las primeras pérdidas que se encuentran son las debidas al **cobre del estator** ($R_1 \cdot I_1^2$).
2.  Seguidamente se pierde energía en el núcleo por **Histéresis y Corrientes Parásitas** en el estator.
3.  La potencia disponible en este punto se traslada del estator al rotor a través del entrehierro de la máquina. Esta se la conoce como **Potencia de entrehierro** ($P_{AG}$).
4.  De la potencia trasladada al rotor, una parte de esta se pierde en el **bobinado de cobre del rotor** ($R_{21} \cdot I_{21}^2$).
5.  Y la potencia que queda es la **Potencia de Conversión** ($P_{conv}$) que se convierte de eléctrica en mecánica.
6.  Por último, a la potencia mecánica obtenida se le deben debitar las **pérdidas por rozamiento y acción del viento** (ventilación) $P_{fyw}$...

---

### Página 27

...y las pérdidas diversas ($P_{mis}$) para obtener la **Potencia de Salida** del motor.

**Consideraciones sobre las Pérdidas:**

Las pérdidas en el núcleo se producen parcialmente en el estator y parte en el rotor.
Como el motor funciona normalmente a una velocidad cercana a la del campo rotante, las pérdidas en el núcleo del rotor son mínimas comparadas con el estator, porque la frecuencia de las tensiones inducidas a esa velocidad son muy bajas (del orden de 5 Hz). Por lo tanto, la fracción más grande de estas provienen del estator.
Esto conlleva a que estas pérdidas, que están representadas por $R_0$, se agrupen en este punto en el modelo.

Cuanto más alta sea la velocidad de un motor, mayor serán las pérdidas por fricción y ventilación* y pérdidas diversas, en tanto que decrecen las pérdidas en el núcleo.

Ocasionalmente estas tres pérdidas se agrupan y se las denomina **Pérdidas Rotacionales**.
Estas se consideran constantes aún cuando la velocidad sea variable, porque las pérdidas cambian en forma opuesta con la velocidad y se compensan.

**Resumen de resistencias en el modelo:**

* La **Potencia de entrehierro** es la que se disipa en la resistencia $\frac{R_{21}}{S}$.
* Mientras que las **pérdidas en el cobre del rotor** son las que se disipan en $R_{21}$.
* La diferencia entre ellas es la **Potencia de Conversión** $P_{conv}$, lo cual debe disiparse en la resistencia de carga ficticia:
    $$R_c = R_{21} \left(\frac{1-S}{S}\right)$$

---
