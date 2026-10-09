"""
Funciones del enunciado "La raíz que se esconde", con sus derivadas y
reformulaciones de punto fijo x = g(x), más el ambiente controlado de cada una.
"""

import numpy as np

TOL = 1e-6
MAX_ITER = 100


def _f_polinomica(x):
    return x**3 - x - 2


def _df_polinomica(x):
    return 3 * x**2 - 1


def _f_doble(x):
    return (x - 2) ** 2


def _df_doble(x):
    return 2 * (x - 2)


def _f_log(x):
    return np.log(x) + x - 4


def _df_log(x):
    return 1 / x + 1


def _f_exp(x):
    return np.exp(-x) - x


def _df_exp(x):
    return -np.exp(-x) - 1


def _f_trig(x):
    return np.cos(x) - x


def _df_trig(x):
    return -np.sin(x) - 1


def _f_mixta(x):
    return np.sqrt(x) - np.cos(x)


def _df_mixta(x):
    return 1 / (2 * np.sqrt(x)) + np.sin(x)


# Cada problema declara su ambiente controlado (sección 4 del enunciado).
# - a, b: intervalo para métodos cerrados; para abiertos x0 = a y x1 = b.
# - m: multiplicidad de la raíz (1 simple, 2 doble) para Newton mejorado.
# - raiz_conocida: raíz exacta si se conoce (raíz doble); None si se calcula.
# - g: reformulación x = g(x) para punto fijo.
PROBLEMAS = [
    {
        "id": "polinomica_simple",
        "nombre": "Polinómica (raíz simple)",
        "expr": "x^3 - x - 2",
        "f": _f_polinomica,
        "df": _df_polinomica,
        "g": lambda x: np.cbrt(x + 2),
        "g_expr": "x = cbrt(x + 2)",
        "a": 1.0,
        "b": 2.0,
        "m": 1,
        "raiz_conocida": None,
        "doble": False,
    },
    {
        "id": "polinomica_doble",
        "nombre": "Polinómica (raíz doble)",
        "expr": "(x - 2)^2",
        "f": _f_doble,
        "df": _df_doble,
        "g": lambda x: x - 0.5 * (x - 2) ** 2,
        "g_expr": "x = x - 0.5 (x - 2)^2",
        "a": 1.2,
        "b": 1.3,
        "m": 2,
        "raiz_conocida": 2.0,
        "doble": True,
    },
    {
        "id": "logaritmica",
        "nombre": "Logarítmica",
        "expr": "ln(x) + x - 4",
        "f": _f_log,
        "df": _df_log,
        "g": lambda x: 4 - np.log(x),
        "g_expr": "x = 4 - ln(x)",
        "a": 2.0,
        "b": 3.0,
        "m": 1,
        "raiz_conocida": None,
        "doble": False,
    },
    {
        "id": "exponencial",
        "nombre": "Exponencial",
        "expr": "e^(-x) - x",
        "f": _f_exp,
        "df": _df_exp,
        "g": lambda x: np.exp(-x),
        "g_expr": "x = e^(-x)",
        "a": 0.0,
        "b": 1.0,
        "m": 1,
        "raiz_conocida": None,
        "doble": False,
    },
    {
        "id": "trigonometrica",
        "nombre": "Trigonométrica",
        "expr": "cos(x) - x",
        "f": _f_trig,
        "df": _df_trig,
        "g": lambda x: np.cos(x),
        "g_expr": "x = cos(x)",
        "a": 0.0,
        "b": 1.0,
        "m": 1,
        "raiz_conocida": None,
        "doble": False,
    },
    {
        "id": "mixta",
        "nombre": "Mixta",
        "expr": "sqrt(x) - cos(x)",
        "f": _f_mixta,
        "df": _df_mixta,
        "g": lambda x: np.cos(x) ** 2,
        "g_expr": "x = cos(x)^2",
        "a": 0.1,
        "b": 1.0,
        "m": 1,
        "raiz_conocida": None,
        "doble": False,
    },
]


# Rango [x_min, x_max] para graficar cada función (solo visualización).
RANGO_GRAFICA = {
    "polinomica_simple": (0.0, 2.5),
    "polinomica_doble": (0.5, 3.5),
    "logaritmica": (1.2, 4.5),
    "exponencial": (-0.5, 1.5),
    "trigonometrica": (-0.5, 1.5),
    "mixta": (0.01, 1.5),
}


def raiz_referencia(p):
    """Raíz de referencia: exacta si se conoce; si no, bisección de alta precisión."""
    if p["raiz_conocida"] is not None:
        return p["raiz_conocida"]
    f, a, b = p["f"], p["a"], p["b"]
    if f(a) * f(b) >= 0:
        raise ValueError(f"{p['id']}: no hay cambio de signo en [a, b]")
    for _ in range(200):
        c = (a + b) / 2
        if f(a) * f(c) <= 0:
            b = c
        else:
            a = c
        if b - a < 1e-15:
            break
    return (a + b) / 2


def verificar_ambiente(p):
    """
    Demuestra la raíz en el rango:
      - cambio de signo f(a)·f(b) < 0 (Bolzano) para las que cruzan;
      - tangencia al eje (f(α)=0 y f'(α)=0) para la raíz doble.
    Devuelve un dict con los valores calculados y un booleano 'valido'.
    """
    f, df = p["f"], p["df"]
    fa, fb = float(f(p["a"])), float(f(p["b"]))
    info = {
        "id": p["id"],
        "a": p["a"],
        "b": p["b"],
        "f(a)": fa,
        "f(b)": fb,
        "tol": TOL,
        "max_iter": MAX_ITER,
    }
    alpha = raiz_referencia(p)
    info["alpha"] = alpha
    info["f(alpha)"] = float(f(alpha))
    info["f'(alpha)"] = float(df(alpha))
    if p["doble"]:
        info["metodo_demostracion"] = "tangencia al eje (f=0, f'=0)"
        info["valido"] = abs(info["f(alpha)"]) < 1e-12 and abs(info["f'(alpha)"]) < 1e-12
    else:
        info["metodo_demostracion"] = "cambio de signo (Bolzano)"
        info["valido"] = fa * fb < 0
    return info
