"""
Genera los gráficos PNG en src/assets/ a partir de los CSV de src/data/.

Salidas:
  - raiz_<id>.png     : función con la raíz marcada (y la tangencia en la raíz doble)
  - error_<id>.png    : |error| vs iteración (escala log) comparando métodos
  - resumen_iteraciones.png : iteraciones por método y función
  - sensibilidad.png  : iteraciones según intervalo / estimación inicial

Ejecutar ejecutar.py y sensibilidad.py antes que este script.

Uso (desde la raíz del proyecto):
    python src/scripts/graficar.py
"""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from funciones import PROBLEMAS, RANGO_GRAFICA, TOL, raiz_referencia  # noqa: E402

SRC_DIR = Path(__file__).resolve().parents[1]  # carpeta src/
DATA_DIR = SRC_DIR / "data"
ASSETS_DIR = SRC_DIR / "assets"
METODOS = ["biseccion", "falsa_posicion", "punto_fijo", "secante",
           "newton_raphson", "newton_mejorado"]
ETIQUETAS = {
    "biseccion": "Bisección",
    "falsa_posicion": "Falsa posición",
    "punto_fijo": "Punto fijo",
    "secante": "Secante",
    "newton_raphson": "Newton-Raphson",
    "newton_mejorado": "Newton mejorado",
}


def leer_iteraciones(fid):
    """Historial de iteraciones de una función: {metodo: [(n, x, fx, error), ...]}."""
    datos = {m: [] for m in METODOS}
    with open(DATA_DIR / f"iteraciones_{fid}.csv", encoding="utf-8") as fh:
        for fila in csv.DictReader(fh):
            datos[fila["metodo"]].append(
                (int(fila["n"]), float(fila["x_n"]), float(fila["f(x_n)"]), float(fila["error"]))
            )
    return datos


def leer_resumen():
    """Resumen de convergencia: {(funcion, metodo): fila}."""
    with open(DATA_DIR / "resumen_convergencia.csv", encoding="utf-8") as fh:
        return {(f["funcion"], f["metodo"]): f for f in csv.DictReader(fh)}


def grafica_raiz(p):
    datos = np.genfromtxt(DATA_DIR / f"{p['id']}.csv", delimiter=",", skip_header=1)
    x, y = datos[:, 0], datos[:, 1]
    alpha = raiz_referencia(p)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(x, y, color="tab:blue", label=f"f(x) = {p['expr']}")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(p["a"], color="gray", linestyle=":", label=f"a = {p['a']}" if not p["doble"] else f"x0 = {p['a']}")
    if not p["doble"]:
        ax.axvline(p["b"], color="gray", linestyle="--", label=f"b = {p['b']}")
        ax.plot([alpha], [0], "o", color="red", markersize=8, label=f"raíz α = {alpha:.6f}")
    else:
        ax.plot([alpha], [0], "o", color="red", markersize=8, label=f"raíz doble α = {alpha:.6f}")
        # tangencia: recta tangente en la raíz (pendiente f'(α) = 0)
        ax.plot(x, np.zeros_like(x), color="red", linestyle="--", linewidth=1,
                label="tangente en α (f'(α)=0)")
    ax.set_title(f"{p['nombre']}: raíz marcada")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    ruta = ASSETS_DIR / f"raiz_{p['id']}.png"
    fig.savefig(ruta, dpi=120)
    plt.close(fig)
    return ruta


def grafica_error(p, resumen):
    datos = leer_iteraciones(p["id"])
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    for m in METODOS:
        filas = datos[m]
        if not filas:
            continue
        n = np.array([r[0] for r in filas])
        err = np.array([r[3] for r in filas])
        err = np.maximum(err, 1e-16)  # evita log(0) en errores exactos
        conv = resumen[(p["id"], m)]["convergio"] == "True"
        etiqueta = ETIQUETAS[m] + ("" if conv else " (no converge)")
        ax.semilogy(n, err, marker="o", markersize=3, linestyle="-" if conv else "--", label=etiqueta)
    ax.axhline(TOL, color="black", linestyle=":", linewidth=1, label="tol = 1e-6")
    ax.set_title(f"{p['nombre']}: |error| vs iteración (escala log)")
    ax.set_xlabel("iteración n")
    ax.set_ylabel("|x_n − α|")
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=8)
    fig.tight_layout()
    ruta = ASSETS_DIR / f"error_{p['id']}.png"
    fig.savefig(ruta, dpi=120)
    plt.close(fig)
    return ruta


def grafica_resumen(resumen):
    ids = [p["id"] for p in PROBLEMAS]
    fig, ax = plt.subplots(figsize=(11, 5))
    ancho = 0.13
    x = np.arange(len(ids))
    for i, m in enumerate(METODOS):
        valores, hatch = [], []
        for fid in ids:
            fila = resumen[(fid, m)]
            conv = fila["convergio"] == "True"
            valores.append(int(fila["iteraciones"]) if conv else 0)
            hatch.append(conv)
        barras = ax.bar(x + (i - 2.5) * ancho, valores, ancho, label=ETIQUETAS[m])
        for barra, conv, fid in zip(barras, hatch, ids):
            if not conv:
                barra.set_hatch("//")
                barra.set_alpha(0.4)
                ax.text(barra.get_x() + barra.get_width() / 2, 0.5, "X", ha="center", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels([p["nombre"] for p in PROBLEMAS], rotation=12, fontsize=8)
    ax.set_ylabel("iteraciones hasta convergencia")
    ax.set_title("Resumen de iteraciones por método y función (rayado = no convergió / no aplica)")
    ax.grid(axis="y", alpha=0.3)
    ax.legend(fontsize=8, ncol=3)
    fig.tight_layout()
    ruta = ASSETS_DIR / "resumen_iteraciones.png"
    fig.savefig(ruta, dpi=120)
    plt.close(fig)
    return ruta


def grafica_sensibilidad():
    with open(DATA_DIR / "sensibilidad.csv", encoding="utf-8") as fh:
        filas = list(csv.DictReader(fh))
    funciones = []
    for f_ in filas:
        if f_["funcion"] not in funciones:
            funciones.append(f_["funcion"])
    nombres = {p["id"]: p["nombre"] for p in PROBLEMAS}
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    for ax, fid in zip(axes.flat, funciones):
        sub = [f_ for f_ in filas if f_["funcion"] == fid]
        parametros = []
        for f_ in sub:
            if f_["parametro"] not in parametros:
                parametros.append(f_["parametro"])
        metodos = []
        for f_ in sub:
            if f_["metodo"] not in metodos:
                metodos.append(f_["metodo"])
        ancho = 0.8 / max(len(metodos), 1)
        x = np.arange(len(parametros))
        for i, m in enumerate(metodos):
            # cada método solo tiene valores para sus propios parámetros (intervalo o x0)
            posiciones, vals, conv = [], [], []
            for j, par in enumerate(parametros):
                fila = next((f_ for f_ in sub if f_["metodo"] == m and f_["parametro"] == par), None)
                if fila is None:
                    continue
                posiciones.append(j + (i - len(metodos) / 2) * ancho + ancho / 2)
                vals.append(int(fila["iteraciones"]))
                conv.append(fila["convergio"] == "True")
            barras = ax.bar(posiciones, vals, ancho, label=ETIQUETAS.get(m, m))
            for b_, c_ in zip(barras, conv):
                if not c_:
                    b_.set_hatch("//")
                    b_.set_alpha(0.4)
        ax.set_xticks(x)
        ax.set_xticklabels(parametros, rotation=20, fontsize=8)
        ax.set_title(nombres.get(fid, fid))
        ax.set_ylabel("iteraciones")
        ax.grid(axis="y", alpha=0.3)
        ax.legend(fontsize=7)
    fig.suptitle("Sensibilidad: intervalo [a, b] (cerrados) y estimación inicial x0 (abiertos)")
    fig.tight_layout()
    ruta = ASSETS_DIR / "sensibilidad.png"
    fig.savefig(ruta, dpi=120)
    plt.close(fig)
    return ruta


def main():
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    resumen = leer_resumen()
    generados = []
    for p in PROBLEMAS:
        generados.append(grafica_raiz(p))
        generados.append(grafica_error(p, resumen))
    generados.append(grafica_resumen(resumen))
    generados.append(grafica_sensibilidad())
    for r in generados:
        print("generado:", r)


if __name__ == "__main__":
    main()
