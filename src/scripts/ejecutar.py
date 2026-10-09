"""
Ejecuta los seis métodos sobre las funciones del enunciado y genera los datos.

Salidas (en src/data/):
  - <id>.csv               : columnas x, f(x) sobre el rango de graficación
  - iteraciones_<id>.csv   : metodo, n, x_n, f(x_n), error por iteración
  - resumen_convergencia.csv : funcion, metodo, convergio, iteraciones, raiz, error, orden
  - ambiente.csv           : verificación del ambiente controlado de cada función

Uso (desde la raíz del proyecto):
    python src/scripts/ejecutar.py
"""

import csv
from pathlib import Path

import numpy as np

from funciones import PROBLEMAS, RANGO_GRAFICA, TOL, MAX_ITER, raiz_referencia, verificar_ambiente
from metodos import (
    biseccion,
    falsa_posicion,
    newton_mejorado,
    newton_raphson,
    punto_fijo,
    secante,
)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
N_PUNTOS = 400


def correr_metodos(p):
    """Aplica los seis métodos a un problema y devuelve {nombre: resultado}."""
    f, df, g = p["f"], p["df"], p["g"]
    a, b, m = p["a"], p["b"], p["m"]
    alpha = raiz_referencia(p)

    resultados = {
        "biseccion": biseccion(f, a, b, alpha, tol=TOL, max_iter=MAX_ITER),
        "falsa_posicion": falsa_posicion(f, a, b, alpha, tol=TOL, max_iter=MAX_ITER),
        "punto_fijo": punto_fijo(g, a, f, alpha, tol=TOL, max_iter=MAX_ITER),
        "secante": secante(f, a, b, alpha, tol=TOL, max_iter=MAX_ITER),
        "newton_raphson": newton_raphson(f, df, a, alpha, tol=TOL, max_iter=MAX_ITER),
        "newton_mejorado": newton_mejorado(f, df, a, alpha, m=m, tol=TOL, max_iter=MAX_ITER),
    }
    return resultados, alpha


def escribir_funcion(p):
    """CSV con columnas (x, f(x)) sobre el rango de graficación."""
    x_min, x_max = RANGO_GRAFICA[p["id"]]
    x = np.linspace(x_min, x_max, N_PUNTOS)
    with np.errstate(all="ignore"):
        y = p["f"](x)
    ruta = DATA_DIR / f"{p['id']}.csv"
    np.savetxt(ruta, np.column_stack([x, y]), delimiter=",", header="x,f(x)",
               comments="", fmt="%.10f")
    return ruta


def escribir_iteraciones(p, resultados):
    """CSV con el historial de iteraciones de todos los métodos de una función."""
    ruta = DATA_DIR / f"iteraciones_{p['id']}.csv"
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["metodo", "n", "x_n", "f(x_n)", "error"])
        for nombre, r in resultados.items():
            for h in r["historial"]:
                w.writerow([nombre, h["n"], f"{h['x']:.12f}", f"{h['fx']:.6e}", f"{h['error']:.6e}"])
    return ruta


def fmt(v, dec=10):
    return "" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.{dec}g}"


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    ambientes = []
    filas_resumen = []
    for p in PROBLEMAS:
        amb = verificar_ambiente(p)
        # |g'(alpha)| por diferencia central: determina si punto fijo converge (< 1)
        h = 1e-6
        amb["g_prima_alpha"] = float((p["g"](amb["alpha"] + h) - p["g"](amb["alpha"] - h)) / (2 * h))
        ambientes.append(amb)
        print(f"\n== {p['nombre']}: {p['expr']} ==")
        print(f"   ambiente: [{p['a']}, {p['b']}]  valido={amb['valido']}  "
              f"({amb['metodo_demostracion']})  raiz={amb['alpha']:.12f}")

        resultados, alpha = correr_metodos(p)
        escribir_funcion(p)
        escribir_iteraciones(p, resultados)

        for nombre, r in resultados.items():
            ultimo_error = r["historial"][-1]["error"] if r["historial"] else np.nan
            print(f"   {nombre:<16} conv={str(r['convergio']):<5} it={r['iteraciones']:>3}  "
                  f"raiz={fmt(r['raiz'], 10):<14} error={fmt(ultimo_error, 3):<10} "
                  f"orden={fmt(r['orden_estimado'], 3)}  ({r['motivo']})")
            filas_resumen.append({
                "funcion": p["id"],
                "metodo": nombre,
                "convergio": r["convergio"],
                "iteraciones": r["iteraciones"],
                "raiz": fmt(r["raiz"], 12),
                "raiz_referencia": fmt(alpha, 12),
                "error_final": fmt(ultimo_error, 6),
                "orden_estimado": fmt(r["orden_estimado"], 4),
                "motivo": r["motivo"],
            })

    with open(DATA_DIR / "resumen_convergencia.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas_resumen[0].keys()))
        w.writeheader()
        w.writerows(filas_resumen)

    with open(DATA_DIR / "ambiente.csv", "w", newline="", encoding="utf-8") as fh:
        claves = ["id", "a", "b", "f(a)", "f(b)", "alpha", "f(alpha)", "f'(alpha)",
                  "g_prima_alpha", "metodo_demostracion", "tol", "max_iter", "valido"]
        w = csv.DictWriter(fh, fieldnames=claves, extrasaction="ignore")
        w.writeheader()
        for amb in ambientes:
            w.writerow(amb)

    print(f"\nDatos escritos en {DATA_DIR}")


if __name__ == "__main__":
    main()
