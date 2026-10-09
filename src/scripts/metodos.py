"""
Métodos de búsqueda de raíces implementados con numpy.

Métodos cerrados (requieren cambio de signo): biseccion, falsa_posicion.
Métodos abiertos (parten de estimaciones): punto_fijo, secante,
newton_raphson, newton_mejorado.

Criterio de parada (sección 5 del enunciado):
    |f(x_n)| < tol  o  |x_n - x_{n-1}| < tol

Cada método devuelve un diccionario con:
    metodo, convergio, raiz, iteraciones, historial, motivo, orden_estimado
donde historial es una lista de dicts con n, x, fx, error.
"""

import numpy as np

TOL = 1e-6
MAX_ITER = 100


def _registro(n, x, fx, raiz_ref):
    return {
        "n": n,
        "x": float(x),
        "fx": float(fx),
        "error": float(abs(x - raiz_ref)),
    }


def _parada(fx, x, x_prev, tol):
    if abs(fx) < tol:
        return True
    return x_prev is not None and abs(x - x_prev) < tol


def _resultado(metodo, convergio, raiz, historial, motivo):
    return {
        "metodo": metodo,
        "convergio": convergio,
        "raiz": float(raiz) if raiz is not None else np.nan,
        "iteraciones": len(historial),
        "historial": historial,
        "motivo": motivo,
        "orden_estimado": orden_estimado(historial),
    }


def orden_estimado(historial):
    """
    Estima el orden de convergencia p con la mediana de
        p_k = log(e_{k+1}/e_k) / log(e_k/e_{k-1})
    sobre los errores mayores que 1e-12 (por encima del ruido de punto flotante).
    Es una estimación empírica: para bisección el error no decrece de forma
    monótona, así que su valor no es representativo.
    """
    e = np.array([h["error"] for h in historial if 1e-12 < h["error"] < np.inf])
    if len(e) < 3:
        return np.nan
    with np.errstate(all="ignore"):
        p = np.log(e[2:] / e[1:-1]) / np.log(e[1:-1] / e[:-2])
    p = p[np.isfinite(p)]
    return float(np.median(p)) if len(p) else np.nan


def _no_aplica(metodo, motivo):
    return _resultado(metodo, False, None, [], motivo)


def _tope(metodo, historial):
    return _resultado(metodo, False, historial[-1]["x"] if historial else None,
                      historial, f"tope de {MAX_ITER} iteraciones alcanzado")


def biseccion(f, a, b, raiz_ref, tol=TOL, max_iter=MAX_ITER):
    """Método cerrado: divide [a, b] a la mitad conservando el cambio de signo."""
    nombre = "biseccion"
    fa, fb = f(a), f(b)
    if fa * fb >= 0:
        return _no_aplica(nombre, "no hay cambio de signo en [a, b]")
    historial, x_prev = [], None
    for n in range(1, max_iter + 1):
        c = (a + b) / 2.0
        fc = f(c)
        historial.append(_registro(n, c, fc, raiz_ref))
        if _parada(fc, c, x_prev, tol):
            return _resultado(nombre, True, c, historial, "criterio de parada cumplido")
        if f(a) * fc < 0:
            b = c
        else:
            a = c
        x_prev = c
    return _tope(nombre, historial)


def falsa_posicion(f, a, b, raiz_ref, tol=TOL, max_iter=MAX_ITER):
    """Método cerrado: interpolación lineal entre (a, f(a)) y (b, f(b))."""
    nombre = "falsa_posicion"
    fa, fb = f(a), f(b)
    if fa * fb >= 0:
        return _no_aplica(nombre, "no hay cambio de signo en [a, b]")
    historial, x_prev = [], None
    for n in range(1, max_iter + 1):
        if fb - fa == 0:
            return _resultado(nombre, False, None, historial, "division por cero")
        c = b - fb * (b - a) / (fb - fa)
        fc = f(c)
        historial.append(_registro(n, c, fc, raiz_ref))
        if _parada(fc, c, x_prev, tol):
            return _resultado(nombre, True, c, historial, "criterio de parada cumplido")
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
        x_prev = c
    return _tope(nombre, historial)


def punto_fijo(g, x0, f, raiz_ref, tol=TOL, max_iter=MAX_ITER):
    """Método abierto: iteración x_{n+1} = g(x_n) con g reformulada desde f(x) = 0."""
    nombre = "punto_fijo"
    historial, x, x_prev = [], float(x0), None
    with np.errstate(all="ignore"):
        for n in range(1, max_iter + 1):
            x_new = float(g(x))
            if not np.isfinite(x_new) or abs(x_new) > 1e8:
                return _resultado(nombre, False, None, historial, "divergencia (valor no finito)")
            fx = f(x_new)
            historial.append(_registro(n, x_new, fx, raiz_ref))
            if _parada(fx, x_new, x_prev, tol):
                return _resultado(nombre, True, x_new, historial, "criterio de parada cumplido")
            x_prev, x = x, x_new
    return _tope(nombre, historial)


def secante(f, x0, x1, raiz_ref, tol=TOL, max_iter=MAX_ITER):
    """Método abierto: x_{n+1} = x_n - f(x_n)(x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))."""
    nombre = "secante"
    historial = []
    f0, f1 = f(x0), f(x1)
    xa, xb = float(x0), float(x1)
    for n in range(1, max_iter + 1):
        if f1 - f0 == 0:
            return _resultado(nombre, False, None, historial, "division por cero")
        x2 = xb - f1 * (xb - xa) / (f1 - f0)
        f2 = f(x2)
        historial.append(_registro(n, x2, f2, raiz_ref))
        if _parada(f2, x2, xb, tol):
            return _resultado(nombre, True, x2, historial, "criterio de parada cumplido")
        xa, f0 = xb, f1
        xb, f1 = x2, f2
    return _tope(nombre, historial)


def newton_raphson(f, df, x0, raiz_ref, tol=TOL, max_iter=MAX_ITER):
    """Método abierto: x_{n+1} = x_n - f(x_n) / f'(x_n)."""
    return newton_mejorado(f, df, x0, raiz_ref, m=1, tol=tol, max_iter=max_iter,
                           nombre="newton_raphson")


def newton_mejorado(f, df, x0, raiz_ref, m=2, tol=TOL, max_iter=MAX_ITER,
                    nombre="newton_mejorado"):
    """
    Newton-Raphson con factor de multiplicidad m:
        x_{n+1} = x_n - m * f(x_n) / f'(x_n)
    Con m = 1 es Newton-Raphson simple. Con m = multiplicidad de la raíz
    restaura el orden cuadrático en raíces múltiples.
    """
    historial, x, x_prev = [], float(x0), None
    with np.errstate(all="ignore"):
        for n in range(1, max_iter + 1):
            fx, dfx = f(x), df(x)
            if dfx == 0:
                return _resultado(nombre, False, None, historial, "f'(x) = 0")
            x_new = x - m * fx / dfx
            if not np.isfinite(x_new) or abs(x_new) > 1e8:
                return _resultado(nombre, False, None, historial, "divergencia (valor no finito)")
            fn = f(x_new)
            historial.append(_registro(n, x_new, fn, raiz_ref))
            if _parada(fn, x_new, x, tol):
                return _resultado(nombre, True, x_new, historial, "criterio de parada cumplido")
            x_prev, x = x, x_new
    return _tope(nombre, historial)
