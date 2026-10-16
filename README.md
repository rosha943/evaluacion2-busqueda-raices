# Evaluación 2: La raíz que se esconde

Comparación de seis métodos de búsqueda de raíces (bisección, falsa posición, punto fijo, secante, Newton-Raphson y Newton-Raphson mejorado) sobre seis funciones, con análisis de convergencia.

Autores: Marcos Hoces y Rosario Torres· Universidad Católica del Maule · Laboratorio evaluado 2

## Entorno

Requiere Python 3.10 o superior. Se usa un entorno virtual (venv).

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

En Linux o macOS: `python3 -m venv .venv`, `source .venv/bin/activate`, `pip install -r requirements.txt`.

Dependencias (`requirements.txt`): numpy, matplotlib.

## Ejecución

Todos los comandos se ejecutan desde la raíz de este proyecto (`evaluacion2-busqueda-raices/`), con el entorno activado. Ejecutar en este orden:

```powershell
python src/scripts/ejecutar.py     # 1. aplica los 6 métodos y genera los CSV
python src/scripts/sensibilidad.py # 2. experimento de intervalo / x0
python src/scripts/graficar.py     # 3. genera los PNG en src/assets/
```

## Estructura

```
evaluacion2-busqueda-raices/
├── README.md          <- este archivo
├── requirements.txt   <- numpy, matplotlib
├── informe.md         <- respuestas a las preguntas de convergencia y conclusión
└── src/
    ├── assets/        <- gráficos PNG generados
    ├── data/          <- CSV generados
    └── scripts/       <- scripts de Python
```

## Scripts

- `src/scripts/metodos.py`: implementación de los seis métodos con numpy. Criterio de parada |f(x_n)| < tol o |x_n − x_{n−1}| < tol, tol = 1e-6, tope de 100 iteraciones. Devuelve la raíz, el historial de iteraciones y un estimador del orden de convergencia.
- `src/scripts/funciones.py`: las seis funciones del enunciado, sus derivadas, las reformulaciones x = g(x) de punto fijo, el ambiente controlado (intervalos, x₀, multiplicidad) y la verificación de la raíz (cambio de signo o tangencia).
- `src/scripts/ejecutar.py`: aplica los seis métodos a cada función. Escribe los CSV de datos y el resumen de convergencia.
- `src/scripts/sensibilidad.py`: mueve el intervalo (métodos cerrados) y la estimación inicial (métodos abiertos) y registra las iteraciones.
- `src/scripts/graficar.py`: genera los gráficos: función con raíz marcada, |error| vs iteración en escala log, resumen de iteraciones y sensibilidad.

## Datos generados (`src/data/`)

- `<funcion>.csv`: columnas `x, f(x)` sobre el rango de graficación.
- `iteraciones_<funcion>.csv`: historial por método (n, x_n, f(x_n), error).
- `resumen_convergencia.csv`: iteraciones, raíz, error final y orden estimado por método y función.
- `ambiente.csv`: verificación del ambiente controlado (f(a), f(b), raíz de referencia, g′(α), validez).
- `sensibilidad.csv`: iteraciones según intervalo o x₀.

## Gráficos (`src/assets/`)

- `raiz_<funcion>.png`: función con la raíz marcada (y la tangencia en la raíz doble).
- `error_<funcion>.png`: |error| vs iteración (escala log) para los métodos de cada función.
- `resumen_iteraciones.png`: iteraciones por método y función.
- `sensibilidad.png`: iteraciones según intervalo o estimación inicial.

## Notas

- Los métodos cerrados (bisección y falsa posición) no se ejecutan en la raíz doble porque no hay cambio de signo en el intervalo; el script lo registra como "no aplica".
- En la raíz doble, Newton mejorado usa m = 2; en las raíces simples usa m = 1, por lo que coincide con Newton-Raphson.
