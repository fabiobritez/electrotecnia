

### Motor Asincrónico Trifásico

**Definición y concepto general**

El motor asíncrono trifásico a inducción es un mecanismo al cual ingresa energía eléctrica en forma de un conjunto de corrientes trifásicas y se convierte en energía mecánica bajo la forma de un movimiento giratorio de velocidad ligeramente variable con la carga aplicada a su eje.

**Principio de funcionamiento: El Estator**

Para explicar su principio de funcionamiento acudimos a un estator constituido por 3 devanados individuales separados 120° geométricos alrededor de la superficie de la máquina. Al cual, si lo alimentamos con un sistema trifásico de corrientes, se producirá entonces un **campo magnético rotante**, al cual idealizamos por medio de un polo norte y un polo sur, y que gira con una velocidad constante $N_s$ denominada **velocidad sincrónica**.

$$N_s = \frac{60 \cdot f}{P} \quad [RPM]$$

*Donde:*
* $f$: Frecuencia
* $P$: Número de pares de polos


**Interacción electromagnética**

Suponemos que en el espacio afectado por el campo magnético rotante colocamos un conductor rectangular cerrado eléctricamente (en cortocircuito) y vinculado mecánicamente a un eje coincidente con el eje del estator, y que presenta el grado de libertad de poder girar alrededor de ese eje (que es normal al campo rotante).

El campo magnético rotante lo hemos representado por medio de dos polos exteriores que giran produciendo el flujo magnético $\Phi$.

**Generación del movimiento (F.E.M. y Cupla)**


Por el movimiento relativo de la espira con respecto al campo, se induce una **f.e.m.** (fuerza electromotriz) en la espira que hace circular una corriente por la misma, cuyo sentido (se determina con la regla de la mano derecha "Mov, Ind, Campo") tenderá a hacer girar la espira en el mismo sentido del campo.


Debido a la interacción de la corriente con el campo aparece una **acción ponderomotriz** que determina una cupla que tiende a hacer girar la espira para que acompañe al campo.

**Tipos de Rotores**

1.  **Rotor en Jaula de Ardilla:**
    Este esquema elemental sirve para comprender el principio de funcionamiento del motor con rotor en cortocircuito, que da origen al M.A. (Motor Asincrónico) con rotor en jaula de ardilla.
    
2.  **Rotor Bobinado:**
    Si en lugar de dejar la espira en cortocircuito, abrimos la misma espira y conectamos sus terminales a dos anillos rozantes que, mediante escobillas, se conectan con una **resistencia variable exterior**; mediante el ajuste de esta se podrá variar la corriente $I$ que circula por la espira y, por consiguiente, las características de marcha del motor.
    
    En definitiva, este sistema es igual al anterior con la diferencia que permite **regular la marcha** del órgano rotante. Y nos permite comprender el motor asincrónico con rotor bobinado.


**Conclusión: La importancia de la diferencia de velocidad**

Para ambos ejemplos se verifica que: Si el rotor llegase a girar con la misma velocidad del campo rotante, no habría variación de flujo en la espira, no habría f.e.m., no habría corriente, no habría cupla y el motor trataría de disminuir su velocidad.

Pero al hacerlo, se produciría variación de flujo y cupla que lo haría girar nuevamente. Por lo tanto, **la base de la existencia de una cupla motora es la diferencia de velocidad entre el campo y la velocidad del rotor a esa diferencia de velocidades se la llamó **velocidad de deslizamiento**.


Si a esta velocidad la referimos a la velocidad sincrónica ($N_s$), obtenemos el **resbalamiento** ($S$):

$$S\% = \frac{N_S - N}{N_S} \cdot 100$$

*Donde:*
* $N$: Velocidad del rotor
* $N_S$: La velocidad sincrónica


> **Nota importante:** La esencia de la cupla es que se cumpla la condición: $N_S > N$.

---

### Hallaremos la expresión de la Cupla

**1. Análisis del Flujo Magnético**
El flujo máximo que alcanza a concatenar la espira corresponde a instantes en que el campo magnético es normal (perpendicular) al plano de la espira. Su valor está dado por:

$$\Phi_m = \mu H \cdot a \cdot b$$


Siempre suponiendo a la espira fija, el flujo concatenado por la espira va a variar en el tiempo con ley cosenoidal:

$$\Phi(t) = \Phi_m \cdot \cos(\omega_s t)$$

**2. Inducción de la F.E.M. (Ley de Faraday y Lenz)**

Esa variación de flujo origina una f.e.m. (fuerza electromotriz) inducida en la espira que es proporcional a la velocidad de variación del flujo y con el signo dado por la Ley de Lenz:

$$e(t) = - \frac{d\Phi(t)}{dt} = \omega_s \cdot \Phi_m \cdot \sin(\omega_s t)$$

**3. Corriente en la espira**

La f.e.m. hace circular por la espira cerrada (que como carga eléctrica presenta una resistencia $R$ y una autoinducción $L$) una corriente $i(t)$:

$$i(t) = \frac{e(t)}{Z} = \frac{\omega_s \cdot \Phi_m \cdot \sin(\omega_s t - \varphi)}{\sqrt{R^2 + \omega_s^2 L^2}}$$

*Donde el ángulo de desfasaje es:*
$$\varphi = \arctan\left(\frac{\omega_s L}{R}\right)$$ 

**4. Fuerzas sobre los conductores (Ley de Laplace)**

Debido a la acción del campo magnético rotante aparecen fuerzas sobre los conductores. Dado que las fuerzas que actúan sobre los conductores $a$ son **absorbidas** por el vínculo, solo se tendrán en cuenta las fuerzas que actúan sobre los lados activos $b$.

La dirección de las fuerzas son las indicadas en la figura, ya que por la Ley de Laplace:
$$\vec{F} = b \cdot (\vec{i} \wedge \vec{B})$$

Es decir, la fuerza es proporcional a la intensidad de la corriente, a la inducción $B$ y a la longitud del conductor $b$, con un sentido dado por la palma de la mano derecha.


Sustituyendo la corriente $i(t)$ obtenida anteriormente:

$$F(t) = i(t) \cdot b \cdot B = \frac{b \cdot B \cdot \omega_s \cdot \Phi_m \cdot \sin(\omega_s t - \varphi)}{\sqrt{R^2 + \omega_s^2 L^2}}$$

**5. Cálculo de la Cupla (Momento Torsor)**
Las dos fuerzas constituyen una cupla que producen un momento torsor con respecto al centro de la espira que actúa en el sentido de giro del Campo.

Para hallar el módulo de la cupla tendremos que encontrar la expresión de la cupla motora instantánea, que será igual al producto de una de las fuerzas $F$ por el **brazo de palanca** correspondiente ($a \cdot \sin(\omega_s t)$).

$$C_m(t) = F(t) \cdot a \cdot \sin(\omega_s t)$$

Sustituyendo $F(t)$:

$$C_m(t) = \frac{\omega_s \cdot \Phi_m \cdot a \cdot b \cdot B}{\sqrt{R^2 + \omega_s^2 L^2}} \cdot \sin(\omega_s t - \varphi) \cdot \sin(\omega_s t)$$

Como sabemos que $a \cdot b = \text{Área de la espira}$ y que $\Phi_m = B \cdot a \cdot b$, podemos simplificar la expresión final:

$$C_m(t) = \frac{\omega_s \cdot \Phi_m^2}{\sqrt{R^2 + \omega_s^2 L^2}} \cdot \sin(\omega_s t - \varphi) \cdot \sin(\omega_s t)$$
 


 

### Deducción de la Cupla Media

El hecho de que exista esta cupla motora instantánea no asegura que el sistema gire, por eso debemos ver si hay algún **valor promedio** en el tiempo que actúe siempre en el mismo sentido.

**1. Descomposición Trigonométrica**

Como sabemos por identidad trigonométrica que:

$$\sin(\omega_s t) \cdot \sin(\omega_s t - \varphi) = \frac{1}{2} [\cos(\omega_s t - \omega_s t + \varphi) - \cos(\omega_s t + \omega_s t - \varphi)]$$
$$= \frac{1}{2} [\cos \varphi - \cos(2\omega_s t - \varphi)]$$

Reemplazando en la expresión de la cupla instantánea $C_m(t)$ (obtenida en la parte anterior), se tiene:

$$C_m(t) = \frac{1}{2} \frac{\omega_s \Phi_m^2}{\sqrt{R^2 + (\omega_s L)^2}} \cos \varphi - \frac{1}{2} \frac{\omega_s \Phi_m^2}{\sqrt{R^2 + (\omega_s L)^2}} \cos(2\omega_s t - \varphi)$$

**2. Análisis de los términos**

Esta expresión está compuesta por dos términos:
1.  Uno **independiente del tiempo** (constante).
2.  Y otro que **varía en el tiempo** con ley cosenoidal y una frecuencia doble del valor de red ($2\omega_s$).

Esa fluctuación no se traduce en movimiento porque es **absorbida** por el momento de inercia que tiene la parte móvil. De manera que lo que corresponde a la cupla motora es el valor de la **cupla media** que determinamos integrando en un período $T$:

$$\bar{C}_m = \frac{1}{T} \int_0^T C_m(t) dt = \frac{1}{2} \frac{\omega_s \Phi_m^2}{\sqrt{R^2 + \omega_s^2 L^2}} \cdot \cos \varphi$$


**3. Sustitución de la Impedancia**

Donde el ángulo $\varphi$ es el argumento de la impedancia del circuito R-L que constituye la espira cortocircuitada. Del triángulo de impedancia:

$$\cos \varphi = \frac{R}{\sqrt{R^2 + (\omega_s L)^2}}$$

Reemplazando esto en la expresión de la cupla motora media:

$$\bar{C}_m = \frac{1}{2} \frac{\omega_s \Phi_m^2}{\sqrt{R^2 + (\omega_s L)^2}} \cdot \frac{R}{\sqrt{R^2 + (\omega_s L)^2}}$$

$$\bar{C}_m = \frac{1}{2} \frac{\omega_s \Phi_m^2 R}{(R^2 + (\omega_s L)^2)}$$

---

### El Efecto de la Rotación (Velocidad Relativa)

Se observa que la cupla promedio actúa en un sentido determinado y que, si es mayor que la cupla resistente, dará origen al movimiento.

El razonamiento que se ha hecho es para una espira detenida frente al campo rotante, pero en realidad esta no permanece detenida, sino que **rota con el Campo**.

Apenas empieza a rotar la espira, como el campo rotante gira a una velocidad $\omega_s$ constante, la posición relativa del campo con respecto a la espira no vendrá dada por $\omega_s t$, sino que habrá que tener en cuenta ese **movimiento relativo** del campo con respecto a la espira.

**Introducción de la Velocidad de Deslizamiento ($\omega_R$)**

Suponiendo que la espira gire a una velocidad también constante que designamos con $\omega$, todo el razonamiento que hemos realizado podría repetirse y tomarse como válido si se sustituye, en la expresión de la Cupla media, a la velocidad absoluta del campo rotante $\omega_s$ por la **velocidad de rotación relativa** del campo respecto a la espira.

Es decir:
$$\omega_R = \omega_s - \omega$$

Porque sería exactamente el razonamiento que haría un observador que acompaña a la espira en su movimiento. A esta velocidad relativa se la llama **velocidad angular de deslizamiento** del campo respecto a la espira.

Como $\omega_s$ y $\omega$ son constantes, $\omega_R$ también lo será. Y por lo tanto la cupla media será:

$$\bar{C}_m = \frac{1}{2} \cdot \frac{\omega_R \cdot \Phi_m^2 \cdot R}{R^2 + (\omega_R L)^2}$$

---
 

### Análisis de la Función Cupla ($\bar{C}_m$)

Analicemos la expresión de $\bar{C}_m$ ya que en todo motor interesa determinar las características externas de la máquina, que son la **Cupla** y la **Velocidad de Giro**.

El gráfico a analizar nos vincula la variación de la cupla motora media en función de la velocidad de giro del motor. El producto de estos dos factores nos da la potencia mecánica de salida del motor.

La vinculación de $\bar{C}_m$ con $\omega$ la obtenemos si sustituimos $\omega_R$ por $(\omega_s - \omega)$ en la expresión.

**Estrategia Gráfica**
Primero representaremos $\bar{C}_m$ en función de $\omega_R$ y después, mediante un cambio en la orientación del eje de abscisas, pasamos al gráfico definitivo.

Supongamos un crecimiento de $\omega_R$ positivo hacia la izquierda a partir de cero, con el propósito de que cuando cambiemos $\omega$ por $\omega_R$ el crecimiento de $\omega$ sea en forma convencional (hacia la derecha).


**Campo de Variación de las Variables**
Observemos cuál es el campo de variación de las variables $\omega$ y $\omega_R$ con significado físico.

1.  **Analíticamente:** $\omega$ podría variar de $-\infty$ a $+\infty$.
2.  **Físicamente:** Para que haya cupla motora, $\omega < \omega_s$. Como límite podría ser igual.
    * Como la espira es arrastrada por el campo, es evidente que **no va a girar con velocidad mayor que este**.
    * Si $\omega > \omega_s$, $\omega_R$ sería negativo y la cupla también, por lo que se produce un **efecto de frenado**. Esta no es una condición normal de funcionamiento (para un motor).

Vemos también que $\omega > 0$ porque el rotor es arrastrado por el Campo. Imaginar situaciones en que $\omega < 0$ implica que la espira gire en sentido contrario al Campo, pero esta condición no es una condición normal de funcionamiento. Por lo tanto:

$$0 \leq \omega \leq \omega_s$$

De esto se deduce que los límites establecidos para $\omega_R$ corresponden a:

$$0 \leq \omega_R \leq \omega_s$$

---

### Cálculo del Máximo (Cupla Máxima)

Observando la expresión de la $\bar{C}_m$:

$$\bar{C}_m = \frac{1}{2} \frac{\omega_R \cdot \Phi_m^2 \cdot R}{R^2 + \omega_R^2 L^2}$$

Vemos los comportamientos en los extremos:
* Si $\omega_R = 0 \Rightarrow \bar{C}_m = 0$
* Si $\omega_R = \infty \Rightarrow \bar{C}_m = 0$

La función $\bar{C}_m$ pasa por dos valores nulos para dos valores de la variable independiente. Por lo tanto, de acuerdo con el **Teorema de Rolle**, en algún punto intermedio la función pasa por un máximo o un mínimo. En nuestro caso será un máximo.

**Derivada para encontrar el máximo**
Para ubicarlo derivamos e igualamos a cero:

$$\frac{d\bar{C}_m}{d\omega_R} = \frac{(R^2 + \omega_R^2 L^2) \cdot (\text{const}) - (\text{const}) \cdot \omega_R \cdot (2\omega_R L^2)}{(\text{denominador})^2} = 0$$

*Nota: En el apunte se simplifican las constantes del numerador, resultando en:*

$$R^2 + \omega_R^2 L^2 - 2\omega_R^2 L^2 = 0$$

$$R^2 - \omega_R^2 L^2 = 0 \quad \Rightarrow \quad \omega_{R_{max}} = \frac{R}{L}$$

Esta es la abscisa del máximo (la velocidad de deslizamiento a la cual ocurre la fuerza máxima).

**Valor de la Cupla Máxima**
Reemplazando este valor en la expresión de $\bar{C}_m$ tendremos la ordenada del máximo:

$$\bar{C}_{m_{max}} = \frac{1}{2} \frac{\frac{R}{L} \cdot \Phi_m^2 \cdot R}{R^2 + (\frac{R}{L})^2 \cdot L^2}$$

Operando el denominador: $R^2 + \frac{R^2}{L^2} L^2 = R^2 + R^2 = 2R^2$.

$$\bar{C}_{m_{max}} = \frac{1}{2} \frac{\frac{\Phi_m^2 \cdot R^2}{L}}{2 R^2} = \frac{1}{4} \frac{\Phi_m^2}{L}$$

$$\bar{C}_{m_{max}} = \frac{1}{4} \frac{\Phi_m^2}{L}$$

---

### Observaciones Importantes:
1.  **Independencia de R:** Fíjate en el resultado final: $\bar{C}_{m_{max}} = \frac{1}{4} \frac{\Phi_m^2}{L}$. ¡La cupla máxima **no depende de la resistencia R**!
    * Esto significa que si aumentamos la resistencia del rotor (como en un rotor bobinado), el valor *máximo* de fuerza que puede hacer el motor es el mismo, lo único que cambia es *a qué velocidad* ($\omega_R = R/L$) ocurre ese máximo.
2.  **Teorema de Rolle:** El apunte menciona correctamente a Rolle para justificar la existencia del máximo entre dos ceros (0 e infinito).
 

---
### Análisis Gráfico y Estabilidad de Marcha

**Construcción de la Curva Característica**
Graficamos la $\bar{C}_m$ en función de $\omega_R$:


El campo de variación de $\omega_R$ es $0 \leq \omega_R \leq \omega_s$.
A cada valor de $\omega_R$, como $\omega_s$ es constante, le corresponde un valor de $\omega$ (velocidad mecánica):

* Si $\omega_R = \omega_s \Rightarrow \omega = 0$ (Rotor detenido)
* Si $\omega_R = 0 \Rightarrow \omega = \omega_s$ (Sincronismo)

$\omega = 0$ representa las condiciones de **arranque**, es decir, cuando el rotor está detenido.

Con estas condiciones podemos pasar al gráfico definitivo de $\bar{C}_m = f(\omega)$:


---

### Análisis de Estabilidad (Puntos de Equilibrio)

Comparemos la cupla motora $C_{ms}$ con una cupla resistente $C_{rs}$ que la representamos por una recta de ordenada constante (e independiente de la velocidad de giro) y de menor valor que la ordenada máxima de $C_{m_{max}}$.

> **Nota:** Si $C_{rs}$ estuviese por encima de la máxima, el motor nunca podría arrastrar esa cupla resistente.

El equilibrio en funcionamiento de régimen corresponderá a una cupla motora igual a la resistente:
$$C_{ms} = C_{rs}$$

En el gráfico existen **2 puntos posibles de equilibrio**, indicados por **1** y **2**. Hay que ver si alguno es estable, para lo cual seguimos el siguiente análisis:

Separamos al sistema de la condición de equilibrio y observamos cómo reacciona:
a) Si la reacción representa una vuelta a la condición inicial, el equilibrio es **estable**.
b) Si la reacción del sistema es tal que tiende a alejar aún más de las condiciones iniciales, el equilibrio es **inestable**.

**Análisis del Punto 1 (Rama inestable)**
En el punto 1 tenemos que la velocidad de giro es $\omega_1$.
* **Si se frena al motor:** La cupla motora $C_{ms}$ disminuye frenándose aún más, alejándose de la posición de equilibrio.
* **Si se aumenta la velocidad de giro:** Vemos que $\bar{C}_m$ se hace más grande, aumentando más la velocidad de giro.

Lo que indica que el punto 1 es de **equilibrio inestable**.

**Análisis del Punto 2 (Rama estable)**
En el punto 2 la velocidad de giro es $\omega_2$.
* **Si se frena al motor:** La cupla motora crece haciéndose mayor que la resistente, acelerando nuevamente al motor y tendiendo al punto de equilibrio inicial.
* **Si se acelera el motor:** La $C_m$ se hace menor que $C_r$, y se frena el motor (volviendo al equilibrio).

Por lo que vemos que **el único punto de equilibrio estable es el 2**.

**Conclusión final**
Este análisis fue para una cupla resistente $C_r = \text{cte}$, aunque para otros valores de cuplas resistentes vemos que hacia la **derecha de $C_{m_{max}}$** (zona de baja $\omega_R$ o alta $\omega$) corresponde a puntos de funcionamiento **estable**.

 
---
### Control de Velocidad y Cupla de Arranque

**El Problema del Arranque**
Observando el diagrama vemos que $C_m$ (Cupla motora) es menor que $C_r$ (Cupla resistente) en el arranque, lo que impediría que el motor desamarre (arranque).

**La Solución: Variación de la Resistencia Rotórica**
Si observamos las características del máximo, vemos que la abscisa:
$$\omega = \omega_s - \frac{R}{L}$$
depende de la resistencia del circuito eléctrico del rotor, en tanto que el valor de la ordenada de la Cupla media máxima:
$$\bar{C}_{m_{max}} = \frac{1}{4} \frac{\Phi_m^2}{L}$$
es **independiente de esa resistencia**.

Ello nos indica la posibilidad de desplazar la abscisa sin variar la ordenada. Es decir, modificando la resistencia eléctrica del circuito del rotor podemos variar la velocidad a la cual se produce el máximo.

**Incrementando R** podemos llevar el punto $S$ (el máximo) al origen, haciendo que **la cupla en el arranque sea máxima**.


**Implementación en Rotor Bobinado**
Para variar la resistencia del rotor mediante un control exterior, abrimos la espira y a través de **anillos de contacto**, sobre los cuales apoyan dos **escobillas**, intercalamos una **resistencia variable $R_a$**.

Entonces la abscisa del máximo es:
$$\omega_{max} = \omega_s - \frac{R + R_a}{L}$$

Si modificamos $R_a$ podemos llevar la abscisa del máximo al valor que deseemos.

**Representación en función del Resbalamiento (S)**
Otra variante es representar la $\bar{C}_m$ en función del resbalamiento $S$:
$$S = \frac{\omega_R}{\omega_s}$$


* Las diversas curvas (1, 2, 3) corresponden a distintas resistencias rotóricas y son las representaciones gráficas de $C = f(S)$.
* Supongamos que el motor debe proporcionar una **Cupla resistente constante $C_r$**.

---

### Puntos de Funcionamiento y Construcción Física

**Análisis de los Puntos de Operación**
En la intersección $F$ se localizará el funcionamiento a la velocidad $\omega_1$, adoptando una resistencia rotórica que corresponde a la **Curva 1** (donde $R_2 = R + R_a$).

Si el mecanismo exige más cupla, por ejemplo $C'_r$, el funcionamiento se localizará en $F'$ a la velocidad algo menor.

A aumentos de cupla la máquina responde de igual forma hasta $G$ (valor máximo de cupla). De $G$ a $A$ el funcionamiento es **inestable**.

**De la Espira a la Jaula de Ardilla**
La cupla que hemos calculado corresponde a una sola espira. Para aumentar la potencia mecánica se multiplica el número de espiras, considerando espiras en planos verticales, a 45°, etc.


Se observa que el lado $a$ cumple la función de unir los lados $b$.
Entonces no es necesario que los lados $a$ estén en el mismo plano que los $b$, y podrían tomar la forma de $a'$, ya que deben cumplir con la condición de estar en planos normales (perpendiculares) a los $b$ para que no haya fuerzas y de cupla; **para que las fuerzas que actúan sobre los lados $a$ sean absorbidas por el vínculo.**

Esto nos lleva a unir los conductores $b$ (lados activos) con un **anillo** en lugar de hacerlo con conductores diametrales, constituyendo un **motor en jaula de ardilla**.

---

Todas estas maniobras (agregar resistencias externas) son posibles en los motores de rotor bobinado. Pero, ¿cómo controlar la cupla en motores con rotor a **jaula de ardilla**?

**La Solución:**
Se construyen motores a **Doble Jaula** o **Ranura Profunda**, también denominados de "alta cupla de arranque", que tratan de lograr las cualidades funcionales de los motores a rotor bobinado (alta fuerza al arrancar y buena velocidad al marchar).


**Principio de Funcionamiento (Doble Jaula)**
El rotor tiene dos conjuntos de barras (jaulas):
1.  **Jaula Exterior:** Es de **alta resistencia** (sección pequeña o material resistivo) y **baja reactancia** (está cerca del entrehierro, menos dispersión).
2.  **Jaula Interior:** Es de **baja resistencia** (sección grande, cobre) y **alta reactancia** (está enterrada profundamente en el hierro).

**Análisis del Proceso de Arranque y Marcha**

* **En el Arranque ($S=1$):**
    La frecuencia del rotor es máxima e igual a la de red ($f_2 = f_1$). Debido a la alta frecuencia, la reactancia inductiva de la jaula interior es muy grande ($X_L = 2\pi f L$), impidiendo el paso de corriente por ella.
    Por lo tanto, la corriente $I_2$ se establece **preferentemente por la jaula exterior**. Como esta tiene alta resistencia, logramos una **alta cupla de arranque**.

* **En Marcha (Velocidad Nominal):**
    Cuando el motor toma velocidad, **baja la frecuencia $f_2$** del rotor (tiende a cero). Al bajar la frecuencia, la reactancia de la jaula interior disminuye drásticamente.
    La corriente ahora busca el camino de menor impedancia, por lo que **actúa preferentemente la jaula interior** (que tiene resistencia menor). Esto asegura un buen rendimiento y poca pérdida de calor durante el funcionamiento normal.

**Motores de Ranura Profunda**
Los motores con **ranura profunda** son más económicos y actúan bajo el mismo principio, donde la parte profunda de la barra se comporta como la jaula interior (mayor inductancia) y la parte superior como la exterior.

---

### Análisis Gráfico (Curvas Características)

En el gráfico final se observa la superposición de efectos:


* **Curva Alta $R_2$ (Verde/Roja fina):** Comportamiento de la jaula exterior (buen arranque, mal deslizamiento en marcha).
* **Curva Baja $R_2$ (Azul/Fina):** Comportamiento de la jaula interior (mal arranque, buen deslizamiento en marcha).
* **Curva Deseada (Resultante gruesa):** Es la suma de ambas. Se obtiene una cupla alta en el arranque y se mantiene una buena velocidad en régimen.

**Fórmula de Potencia**
En el recuadro se destaca la ecuación de conversión de energía:

$$P_{CONV} = (1 - S) \cdot P_{AG}$$

*Donde:*
* $P_{CONV}$: Potencia convertida (Mecánica interna).
* $S$: Resbalamiento.
* $P_{AG}$: Potencia del Air Gap (Potencia en el entrehierro).

---
 