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

### 3.1 ¿Qué método convergió en menos iteraciones en cada función? ¿Por qué?

- **Polinómica simple (x³−x−2):** Newton y Newton mejorado (5 iteraciones), seguidos de secante (6). Son los de menor orden de convergencia observado.
- **Logarítmica:** empate entre secante, Newton y Newton mejorado (3 iteraciones).
- **Exponencial:** Newton y Newton mejorado (3 iteraciones).
- **Trigonométrica:** secante, Newton y Newton mejorado (4 iteraciones).
- **Mixta:** secante, Newton y Newton mejorado (3 iteraciones).
- **Raíz doble:** Newton mejorado con m = 2 (1 iteración, exacta).

La razón es el orden de convergencia. Newton usa la derivada y, en raíces simples, reduce el error cuadráticamente en cada paso. La secante tiene orden ≈ 1.6 y aprovecha dos aproximaciones previas sin calcular derivada. La bisección solo sabe que la raíz está en un intervalo que se reduce a la mitad: para [0, 1] con tol = 1e-6 necesita log₂(1/1e-6) ≈ 20 iteraciones, exactamente lo que se observa. Punto fijo y falsa posición son lineales.

### 3.2 ¿Qué orden de convergencia tiene cada método y cómo se refleja en el gráfico |error| vs iteración?

Orden estimado (mediana de log(e_{k+1}/e_k)/log(e_k/e_{k−1}) con errores > 1e-12, columna `orden_estimado` de `resumen_convergencia.csv`):

| Método | Orden teórico | Estimado (rango en las funciones simples) |
|---|---|---|
| Newton-Raphson | 2 (cuadrático) | 1.94 – 2.01 |
| Newton mejorado (m correcto) | 2 | 1.94 – 2.01 (raíces simples con m=1); exacto en la raíz doble |
| Secante | 1.618 (superlineal) | 1.52 – 1.69 (la mixta da 2.40, pero con solo 3 iteraciones no es fiable) |
| Falsa posición | 1 (lineal) | ≈ 1 |
| Punto fijo | 1 (lineal, tasa \|g′(α)\|) | ≈ 1 |
| Bisección | 1 (lineal, factor 1/2 sobre el intervalo) | no representativo |

En `src/assets/error_*.png` se ve así: la curva de Newton cae casi en vertical (cada iteración agrega varias cifras), la secante tiene pendiente intermedia y los métodos lineales son rectas con pendiente constante en escala log. El punto fijo de la mixta tiene pendiente muy suave (tasa ≈ 0.96 por iteración) y termina en el tope de 100 iteraciones.

La bisección no tiene una pendiente limpia en el gráfico porque el error de la iterada puede subir o bajar en cada paso; lo que decrece de forma garantizada es la longitud del intervalo, no el error.

### 3.3 ¿Qué métodos requieren un intervalo con cambio de signo y cuáles no?

- **Cerrados (exigen f(a)·f(b) < 0):** bisección y falsa posición. Ambos se niegan a ejecutarse cuando no hay cambio de signo (raíz doble).
- **Abiertos (solo necesitan estimaciones):** punto fijo, secante, Newton-Raphson y Newton mejorado. Pueden converger incluso sin cambio de signo, pero también pueden divergir o converger a otra raíz.

### 3.4 En la función que toca el eje x (raíz doble): ¿qué métodos fallan o no aplican y cuál se comporta mejor? ¿Por qué?

- **Bisección y falsa posición:** no aplican. f(1.2) = 0.64 y f(1.3) = 0.49 tienen el mismo signo, y la tangencia no produce cambio de signo.
- **Punto fijo con g(x) = x − 0.5(x−2)²:** diverge (error > 6e5 en la iteración 7). Además g′(2) = 1, así que incluso cerca de la raíz la convergencia es, en el mejor caso, sublineal. Con x₀ = 1.2 queda fuera de la zona de atracción.
- **Secante:** converge, pero linealmente con tasa cercana a 1 y termina con error 7.4e-4 (14 iteraciones).
- **Newton-Raphson simple:** converge linealmente con tasa 1/2 (cada paso reduce el error a la mitad, de ahí el orden estimado 1). Termina con error 7.8e-4 en 10 iteraciones.
- **Newton mejorado con m = 2:** el mejor comportamiento. f/f′ = (x−2)/2, así que x₁ = x₀ − 2·(x₀−2)/2 = 2, exacto en una iteración.

Un detalle importante del criterio de parada: para una raíz doble, |f(x)| = (x−2)² < 1e-6 se cumple con error ≈ 1e-3, no con 1e-6. Por eso Newton y secante "paran" con error 7.8e-4 y 7.4e-4: cumplen el criterio pero no la precisión de la raíz. Este es el motivo por el que el criterio |f| < tol no es suficiente para raíces múltiples.

### 3.5 ¿Cómo influyen el intervalo inicial y la estimación inicial en la cantidad de iteraciones y en si el método converge?

Datos de `src/data/sensibilidad.csv` (`src/assets/sensibilidad.png`):

- **Bisección** depende del ancho del intervalo: [1, 2] → 20, [1, 3] → 21, [0, 2] → 21, [1.4, 1.6] → 18. El número crece solo logarítmicamente con el ancho (log₂).
- **Falsa posición** es muy sensible al intervalo porque se estanca cuando un extremo queda lejos: [1, 2] → 12, [1, 3] → 26, [1.4, 1.6] → 5. Acotar mejor la raíz le conviene mucho.
- **Newton** depende fuertemente de x₀ cuando la función es más curvada: en x³−x−2, x₀ = 1.5 → 2 iteraciones; x₀ = 1.0 → 5; x₀ = 2.0 → 4. En la exponencial x₀ = 0.5 → 2; x₀ = 0 → 3. Siempre converge en estos casos porque f′ no se anula cerca de la raíz.
- **Secante** también mejora con una buena x₀ (x³−x−2: 3 con x₀ = 1.5, 6 con x₀ = 1.0 o 2.0).
- **Punto fijo** cambia poco con x₀ en las funciones que converge (7–8 iteraciones en x³−x−2, 13–14 en la logarítmica), pero el factor determinante es |g′(α)|, no x₀. En la mixta no converge para ninguna x₀ (0.1, 0.5, 1.0), porque |g′(α)| = 0.959 implica una convergencia tan lenta que no alcanza 1e-6 en 100 iteraciones.

Conclusión de la sección: el intervalo afecta cuántas iteraciones hacen falta; la estimación inicial afecta cuántas y, en métodos abiertos, si el método converge.

### 3.6 ¿Qué método recomiendan según el tipo de función, considerando el compromiso entre velocidad y robustez?

Véase la conclusión (sección 4).

## 4. Conclusión

**¿Qué método elegirían para cada tipo de función y por qué (velocidad vs robustez)?**

- **Polinómica simple (x³−x−2):** Newton-Raphson (5 iteraciones). Es suave, con derivada fácil y sin singularidades cerca de la raíz. Si la derivada no está disponible, la secante (6 iteraciones) es la alternativa.
- **Logarítmica:** Newton o secante (3 iteraciones). La función es suave en [2, 3] y la derivada 1/x + 1 no se anula. Falsa posición (4 iteraciones) sería la opción robusta cuando hay que garantizar un intervalo con cambio de signo.
- **Exponencial:** Newton (3 iteraciones). Punto fijo es lento (25 iteraciones) aunque converge.
- **Trigonométrica:** Newton o secante (4 iteraciones). Punto fijo tarda 34 iteraciones.
- **Mixta (√x − cos x):** secante o Newton (3 iteraciones). Punto fijo con g = cos²(x) no converge en 100 iteraciones; se debe evitar.
- **Raíz doble:** Newton mejorado con m = 2 (1 iteración). Newton simple y secante convergen pero con orden 1 y error final ≈ 1e-3 bajo el criterio |f| < tol.

Tomando velocidad y robustez en conjunto: Newton (o Newton mejorado) es el más rápido cuando la derivada está disponible y la estimación inicial es razonable. La secante es la mejor alternativa sin derivada. Falsa posición ofrece un equilibrio entre velocidad y seguridad, porque garantiza convergencia dentro del intervalo. Bisección es la más robusta, pero necesita siempre unas 20 iteraciones para tol = 1e-6 con intervalo de ancho 1. Punto fijo solo conviene cuando |g′(α)| es pequeño (≤ 0.35 en estos casos).

**¿Qué ocurrió en la raíz doble y qué dice eso sobre «tener raíz» frente a «cambiar de signo»?**

En (x−2)² la función toca el eje sin cruzarlo. Ahí existe una raíz (f(2) = 0), pero no hay cambio de signo, así que bisección y falsa posición no pueden aplicarse, aunque la raíz exista. El método de Newton simple también pierde su orden cuadrático porque f′(2) = 0. Esto demuestra que "tener raíz" y "cambiar de signo" son propiedades distintas: los métodos cerrados se basan en el cambio de signo, mientras que los abiertos se basan en la información local de f y de f′. Para raíces múltiples hay que usar la multiplicidad (Newton mejorado) o cambiar el método, no solo confiar en la búsqueda de un cambio de signo.

**¿Cómo cambió el número de iteraciones al mover el intervalo o la estimación inicial?**

- Bisección: cambia con el ancho del intervalo, de forma logarítmica (18 a 21 iteraciones en las pruebas).
- Falsa posición: cambia mucho (de 4 a 26 iteraciones) según la posición de los extremos.
- Newton y secante: cambian de 2 a 5 iteraciones según x₀; una estimación cercana a la raíz reduce el número de iteraciones de forma notable.
- Punto fijo: depende de |g′(α)|, no de x₀; en la mixta no converge con ninguna x₀ probada.

Por tanto, los números de iteraciones dependen más del método y de la función que de la elección del intervalo, salvo en falsa posición, donde el intervalo tiene un efecto grande.
