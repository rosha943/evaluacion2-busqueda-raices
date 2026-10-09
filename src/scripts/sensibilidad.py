"""
Experimento de sensibilidad: cómo cambian las iteraciones al mover el
intervalo [a, b] (métodos cerrados) o la estimación inicial x0 (métodos abiertos).

Para los abiertos la secante usa x1 = x0 + 0.1.
Salida: src/data/sensibilidad.csv

Uso (desde la raíz del proyecto):
    python src/scripts/sensibilidad.py
"""

import csv
from pathlib import Path

import numpy as np

from funciones import MAX_ITER, TOL, raiz_referencia
from funciones import PROBLEMAS
from metodos import biseccion, falsa_posicion, newton_raphson, punto_fijo, secante

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

# Casos: intervalos válidos (cambio de signo) y estimaciones iniciales x0.
CASOS = {
    "polinomica_simple": {"intervalos": [(1.0, 2.0), (1.0, 3.0), (0.0, 2.0), (1.4, 1.6)],
                          "x0": [1.0, 1.5, 2.0]},
    "logaritmica": {"intervalos": [(2.0, 3.0), (2.0, 4.0), (1.5, 3.5)],
                    "x0": [2.0, 2.5, 3.5]},
    "exponencial": {"intervalos": [(0.0, 1.0), (0.0, 2.0), (0.2, 1.0)],
                    "x0": [0.0, 0.5, 1.0]},
    "mixta": {"intervalos": [(0.1, 1.0), (0.01, 1.0), (0.1, 2.0)],
              "x0": [0.1, 0.5, 1.0]},
}


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    por_id = {p["id"]: p for p in PROBLEMAS}
    filas = []

    for fid, caso in CASOS.items():
        p = por_id[fid]
        f, df, g = p["f"], p["df"], p["g"]
        alpha = raiz_referencia(p)
        print(f"\n== {p['nombre']} ({p['expr']}), raiz={alpha:.10f} ==")

        for a, b in caso["intervalos"]:
            parametro = f"[{a}, {b}]"
            for nombre, res in [
                ("biseccion", biseccion(f, a, b, alpha, tol=TOL, max_iter=MAX_ITER)),
                ("falsa_posicion", falsa_posicion(f, a, b, alpha, tol=TOL, max_iter=MAX_ITER)),
            ]:
                filas.append(_fila(fid, nombre, "intervalo", parametro, res))
                print(f"   {nombre:<16} {parametro:<14} it={res['iteraciones']:>3} conv={res['convergio']}")

        for x0 in caso["x0"]:
            parametro = f"x0={x0}"
            resultados = [
                ("punto_fijo", punto_fijo(g, x0, f, alpha, tol=TOL, max_iter=MAX_ITER)),
                ("secante", secante(f, x0, x0 + 0.1, alpha, tol=TOL, max_iter=MAX_ITER)),
                ("newton_raphson", newton_raphson(f, df, x0, alpha, tol=TOL, max_iter=MAX_ITER)),
            ]
            for nombre, res in resultados:
                filas.append(_fila(fid, nombre, "estimacion_inicial", parametro, res))
                print(f"   {nombre:<16} {parametro:<14} it={res['iteraciones']:>3} conv={res['convergio']}")

    ruta = DATA_DIR / "sensibilidad.csv"
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    print(f"\nDatos escritos en {ruta}")


def _fila(fid, metodo, tipo, parametro, res):
    return {
        "funcion": fid,
        "metodo": metodo,
        "tipo": tipo,
        "parametro": parametro,
        "convergio": res["convergio"],
        "iteraciones": res["iteraciones"],
        "raiz": "" if np.isnan(res["raiz"]) else f"{res['raiz']:.12f}",
        "motivo": res["motivo"],
    }


if __name__ == "__main__":
    main()
