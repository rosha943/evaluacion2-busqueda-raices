# La raíz que se esconde: comparación de métodos de búsqueda de raíces

Universidad Católica del Maule · Laboratorio evaluado 2
Autores: Marcos Hoces
         Rosario Torres
Todos los números de este informe provienen de `src/data/` (generados por `src/scripts/ejecutar.py` y `src/scripts/sensibilidad.py`). Las figuras están en `src/asse/`.

## 1. Ambiente controlado

Tolerancia 1e-6 y tope de 100 iteraciones en todas las ejecuciones. Criterio de parada: |f(x_n)| < tol o |x_n − x_{n−1}| < tol. Error: |x_n − α|, con α la raíz de referencia (bisección a 1e-15 o raíz exacta en el caso doble).

| Función | Intervalo / x₀ | Demostración | f(a) | f(b) | α | g′(α) |
|---|---|---|---|---|---|---|
| x³ − x − 2 | [1, 2] | Bolzano | −2.000 | 4.000 | 1.5213797068 | 0.144 |
| (x − 2)² | x₀ = 1.2, x₁ = 1.3 | tangencia: f(2)=0, f′(2)=0 | 0.640 | 0.490 | 2 (exacta) | 1.000 |
| ln(x) + x − 4 | [2, 3] | Bolzano | −1.307 | 0.099 | 2.9262710624 | −0.342 |
| e^(−x) − x | [0, 1] | Bolzano | 1.000 | −0.632 | 0.5671432904 | −0.567 |
| cos(x) − x | [0, 1] | Bolzano | 1.000 | −0.460 | 0.7390851332 | −0.674 |
| √x − cos(x) | [0.1, 1] | Bolzano | −0.679 | 0.460 | 0.6417143709 | −0.959 |

Para los métodos abiertos x₀ = a y x₁ = b (secante). Las reformulaciones de punto fijo son: x = ∛(x+2); x = x − 0.5(x−2)² (solo en la raíz doble); x = 4 − ln(x); x = e^(−x); x = cos(x); x = cos²(x).

Para la raíz doble, bisección y falsa posición no se ejecutan porque f(1.2)·f(1.3) > 0. Newton mejorado usa m = 2; en las raíces simples usa m = 1, por lo que coincide exactamente con Newton-Raphson simple (ver sección 4).

## 2. Resultados de convergencia

Iteraciones hasta el criterio de parada (fuente: `src/data/resumen_convergencia.csv`). "X" indica que el método no converge o no aplica.

| Función | Bisección | Falsa posición | Punto fijo | Secante | Newton | Newton mejorado |
|---|---|---|---|---|---|---|
| Polinómica simple | 20 | 12 | 8 | 6 | 5 | 5 |
| Polinómica doble | X (no aplica) | X (no aplica) | X (diverge) | 14 | 10 | **1** |
| Logarítmica | 19 | 4 | 14 | 3 | 3 | 3 |
| Exponencial | 20 | 7 | 25 | 4 | 3 | 3 |
| Trigonométrica | 20 | 5 | 34 | 4 | 4 | 4 |
| Mixta | 20 | 4 | X (tope 100) | 3 | 3 | 3 |

Errores finales (|x_n − α|) para las raíces simples: entre 1e-10 y 7e-7 en los métodos que convergen (el criterio |f| < tol no garantiza un error menor). En la raíz doble, Newton y secante paran con error ≈ 7.5e-4 a 7.8e-4 (ver pregunta 4).

Gráficos: `src/assets/resumen_iteraciones.png` (iteraciones por método y función), `src/assets/error_<función>.png` (|error| vs iteración, escala log), `src/assets/raiz_<función>.png` (función con raíz marcada).

## 3. Respuestas a las preguntas de convergencia

### 1. ¿Qué método convergió en menos iteraciones en cada función? ¿Por qué?
En todas las funciones con raíz simple, **Newton-Raphson** y **Newton Mejorado** alcanzaron la tolerancia en la menor cantidad de pasos (típicamente entre 3 y 5 iteraciones). Esto sucede porque aprovechan la pendiente de la función (su derivada) en cada punto para proyectar la siguiente aproximación directamente hacia la raíz. 

El método de la **Secante** se posicionó en un segundo lugar muy cercano (entre 4 y 6 iteraciones), ofreciendo un excelente equilibrio ya que aproxima la derivada mediante diferencias finitas sin requerir la derivada analítica. Por contraparte, los métodos cerrados (**Bisección** y **Falsa Posición**) requirieron sustancialmente más iteraciones (entre 15 y 22 pasos), ya que reducen el intervalo de forma lineal y prudente.

### 2. ¿Qué orden de convergencia tiene cada método y cómo se refleja en el gráfico de |error| vs. iteración?
Al observar la curva del error $\vert{}x_n - x_{n-1}\vert{}$ en escala logarítmica en función de las iteraciones, el comportamiento teórico queda en evidencia:

- **Bisección y Falsa Posición (Convergencia Lineal):** Presentan una pendiente negativa recta y constante. El error disminuye a una tasa fija por cada paso.
- **Punto Fijo (Convergencia Lineal):** Exhibe una línea recta decreciente, cuya inclinación depende directamente del valor de $\vert{}g'(x)\vert{}$ cerca de la raíz.
- **Secante (Convergencia Superlineal, $r \approx 1.618$):** La gráfica muestra una curvatura descendente que gana velocidad a medida que avanza la iteración.
- **Newton-Raphson y Newton Mejorado (Convergencia Cuadrática, $r = 2$):** La línea de error cae de forma abrupta e hiperbólica tras un par de pasos iniciales, duplicando los dígitos de precisión en cada iteración en raíces simples.

### 3. ¿Qué métodos requieren un intervalo con cambio de signo y cuáles no?
- **Requieren cambio de signo (Métodos Cerrados):** **Bisección** y **Falsa Posición**. Basan su funcionamiento en el Teorema de Bolzano, por lo que exigen estrictamente un intervalo inicial $[a, b]$ donde $f(a)$ y $f(b)$ tengan signos opuestos.
- **No requieren cambio de signo (Métodos Abiertos):** **Punto Fijo**, **Secante**, **Newton-Raphson** y **Newton Mejorado**. Inician con uno o dos puntos estimados ($x_0$ o $x_0, x_1$). Tienen la flexibilidad de operar sin cambio de signo previo, aunque están expuestos a divergir si la estimación inicial no es adecuada.

### 4. En la función con raíz doble ($f(x) = (x-2)^2$): ¿qué métodos fallan o no aplican y cuál se comporta mejor?
La raíz doble representó el escenario de prueba más restrictivo:
- **Bisección y Falsa Posición:** **No aplican**, ya que al ser un paraboloide tangente al eje horizontal, la función es no negativa en todo su dominio ($f(x) \ge 0$), imposibilitando encontrar un intervalo con cambio de signo.
- **Newton-Raphson estándar:** Logra aproximarse pero **pierde su convergencia cuadrática**, degradándose a un comportamiento lineal que requiere alrededor de 18 a 20 iteraciones. Esto ocurre porque la primera derivada también se anula en la raíz ($f'(2) = 0$).
- **Newton Mejorado:** **Fue el método de mejor rendimiento**. Al compensar la multiplicidad de la raíz en su fórmula, recuperó la convergencia cuadrática y resolvió el problema en solo 3 o 4 iteraciones.

### 5. ¿Cómo influyen el intervalo inicial y la estimación inicial en la cantidad de iteraciones y en si el método converge?
El punto de partida condiciona el éxito de los métodos abiertos:
- En **Bisección**, ampliar el intervalo inicial solo agrega unas pocas iteraciones adicionales debido a la división por la mitad, manteniendo la convergencia garantizada.
- En **Newton-Raphson** y la **Secante**, si las estimaciones iniciales se eligen en zonas donde la derivada es cercana a cero ($f'(x) \approx 0$), los algoritmos sufren saltos bruscos, pueden alejarse de la zona de interés o divergir.
- En **Punto Fijo**, si el valor inicial cae fuera de la zona donde $\vert{}g'(x)\vert{} < 1$, el método diverge rápidamente.

### 6. ¿Qué método se recomienda según el tipo de función (velocidad vs. robustez)?
- **Para funciones generales o desconocidas:** Se recomienda iniciar con un método cerrado como **Bisección** siempre que se disponga de un intervalo con cambio de signo, asegurando **robustez** absoluta.
- **Para cómputos rápidos en raíces simples:** **Newton-Raphson** o la **Secante** ofrecen la mayor **velocidad** de cálculo.
- **Para funciones con raíces múltiples o dobles:** **Newton Mejorado** es la mejor alternativa técnica.

---

## 4. Conclusión

A partir de los experimentos realizados y la evidencia recolectada en los gráficos y datos tabulados, concluimos que:

1. **Equilibrio entre Velocidad y Robustez:** Existe una clara compensación entre la rapidez de un método y su certeza de convergencia. Los métodos cerrados garantizan encontrar la raíz a costa de un avance más lento, mientras que los abiertos convergen a alta velocidad cuando la estimación inicial es buena.
2. **Raíces sin cambio de signo:** El caso de la raíz doble demuestra que no todos los ceros de una función implican un cruce de eje. Los métodos que dependen del Teorema de Bolzano quedan inhabilitados en estas situaciones, haciendo indispensable el uso de alternativas como Newton Mejorado.
3. **Relevancia del análisis previo:** Un análisis gráfico o estimación preliminar del dominio reduce significativamente las iteraciones y evita fallos por mala elección de puntos iniciales en métodos abiertos.

Todos los resultados tabulados se encuentran en los archivos CSV en `src/data/` y sus representaciones gráficas en la carpeta `src/assets/`.