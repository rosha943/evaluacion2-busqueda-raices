# Evaluación 2: La raíz que se esconde

**Laboratorio Evaluado 2 — Búsqueda de raíces y análisis de convergencia**  

*Universidad Católica del Maule*



## Descripción del Proyecto



En el presente laboratorio se implementan y analizan seis métodos numéricos clásicos para la resolución de ecuaciones no lineales. Se evalúa el comportamiento de los algoritmos sobre funciones de diversa naturaleza: polinómicas (con raíces simples y dobles), exponenciales, logarítmicas, trigonométricas y mixtas. 



Además de la determinación numérica de las raíces, la investigación se enfoca en el estudio comparativo del proceso de convergencia, considerando indicadores como la tasa de reducción del error, la cantidad de iteraciones requeridas y la estabilidad numérica ante distintas condiciones iniciales.



---



## Estructura del Repositorio



El proyecto se encuentra estructurado conforme a los requerimientos técnicos fijados en la pauta de evaluación:



evaluacion2-busqueda-raices/

├── .gitignore

├── README.md                 <- Documentación técnica y guía de ejecución

├── requirements.txt          <- Dependencias del proyecto (numpy, matplotlib)

├── informe.md                <- Análisis numérico, respuestas y conclusiones

└── src/

    ├── assets/               <- Gráficos de funciones, error e iteraciones (.png)

    ├── data/                 <- Registros numéricos y resultados en formato CSV

    └── scripts/              <- Implementación de métodos y algoritmos en Python



---



## Guía de Instalación y Ejecución



Para replicar los experimentos y regenerar los datos e imágenes del proyecto, se deben seguir los pasos descritos a continuación:



### 1. Clonar el repositorio

git clone https://github.com/rosha943/evaluacion2-busqueda-raices.git

cd evaluacion2-busqueda-raices



### 2. Configurar el entorno virtual (venv)

Se recomienda el uso de un entorno virtual para aislar las dependencias del sistema.



En Windows (PowerShell):

python -m venv .venv

.\.venv\Scripts\Activate.ps1



En Linux / macOS:

python3 -m venv .venv

source .venv/bin/activate



### 3. Instalar dependencias

pip install -r requirements.txt



### 4. Ejecución del programa principal

Para ejecutar los cálculos numéricos, exportar los archivos CSV a la carpeta src/data/ y generar las representaciones gráficas en src/assets/, se ejecuta:

python src/scripts/ejecutar.py



---



## Descripción de los Módulos



- src/scripts/funciones.py: Define las funciones matemáticas bajo estudio, sus derivadas analíticas y las funciones auxiliares g(x) empleadas en el método de Punto Fijo.

- src/scripts/metodos.py: Contiene la implementación algorítmica de los seis métodos iterativos (Bisección, Falsa Posición, Punto Fijo, Secante, Newton-Raphson y Newton-Raphson Mejorado) mediante la librería numpy.

- src/scripts/graficar.py: Genera y exporta las visualizaciones en formato PNG mediante matplotlib (curvas con raíces identificadas, evolución del error en escala logarítmica y comparativas de iteración).

- src/scripts/sensibilidad.py: Analiza la variabilidad del número de iteraciones y la estabilidad de los métodos frente a modificaciones en las estimaciones e intervalos iniciales.

- src/scripts/ejecutar.py: Módulo integrador encargado de la orquestación general de los experimentos.