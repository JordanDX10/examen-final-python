"""
Examen final - Python (Pandas y NumPy)
Análisis del costo de vida por país.
Uso:  python analisis_costo_vida.py costo_de_vida.csv
"""
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

RUTA = sys.argv[1] if len(sys.argv) > 1 else "living__6___3_.csv"
Path("graficos").mkdir(exist_ok=True)

# ---------- 1. Carga y limpieza ----------
df = pd.read_csv(RUTA)
df.columns = df.columns.str.strip()

def buscar(*claves):
    """Encuentra la columna cuyo nombre contenga alguna de las claves."""
    for c in df.columns:
        if any(k in c.lower() for k in claves):
            return c
    raise SystemExit(f"No encontré una columna con {claves}. Columnas: {list(df.columns)}")

c_pais = buscar("countr", "pais", "país")
c_costo = buscar("cost")
c_rank = buscar("rank")

df[c_costo] = pd.to_numeric(df[c_costo].astype(str).str.replace(",", "."), errors="coerce")
df[c_rank] = pd.to_numeric(df[c_rank], errors="coerce")
df[c_pais] = df[c_pais].astype(str).str.strip()

# ---------- 2. Revisión inicial (Ejercicio 1) ----------
filas, columnas = df.shape
promedio = np.mean(df[c_costo].dropna())
mas_alto = df.loc[df[c_costo].idxmax()]
mas_bajo = df.loc[df[c_costo].idxmin()]
peru = df[df[c_pais].str.contains("peru|perú", case=False, na=False)]

lineas = [
    "REVISIÓN INICIAL DEL DATASET",
    f"Nro. de Filas: {filas}",
    f"Nro. de Columnas: {columnas}",
    f"Costo de vida promedio: {promedio:.2f}",
    f"País con costo de vida más alto: {mas_alto[c_pais]} ({mas_alto[c_costo]})",
    f"País con costo de vida más bajo: {mas_bajo[c_pais]} ({mas_bajo[c_costo]})",
]
if peru.empty:
    lineas += ["Costo de Vida en Perú: no encontrado", "Ranking de Perú: no encontrado"]
else:
    p = peru.iloc[0]
    lineas += [f"Costo de Vida en Perú: {p[c_costo]}", f"Ranking de Perú: {int(p[c_rank])}"]
print("\n".join(lineas))
Path("resultados.txt").write_text("\n".join(lineas), encoding="utf-8")

# ---------- 3. Visualizaciones (Ejercicio 2) ----------
def barras(datos, titulo, archivo, color):
    datos = datos.sort_values(c_costo)
    plt.figure(figsize=(9, 5))
    plt.barh(datos[c_pais], datos[c_costo], color=color)
    plt.title(titulo)
    plt.xlabel("Índice de costo de vida")
    plt.tight_layout()
    plt.savefig(f"graficos/{archivo}", dpi=150)
    plt.close()

barras(df.nlargest(10, c_costo), "Top 10 países con mayor costo de vida", "top10_mas_altos.png", "#ef4444")
barras(df.nsmallest(10, c_costo), "Top 10 países con menor costo de vida", "top10_mas_bajos.png", "#22c55e")

AMERICA = ["Antigua and Barbuda", "Argentina", "Bahamas", "Barbados", "Belize", "Bolivia", "Brazil",
    "Canada", "Chile", "Colombia", "Costa Rica", "Cuba", "Dominica", "Dominican Republic", "Ecuador",
    "El Salvador", "Grenada", "Guatemala", "Guyana", "Haiti", "Honduras", "Jamaica", "Mexico",
    "Nicaragua", "Panama", "Paraguay", "Peru", "Saint Lucia", "Suriname", "Trinidad and Tobago",
    "United States", "Uruguay", "Venezuela", "Puerto Rico"]
cont = [c for c in df.columns if "contin" in c.lower()]
if cont:   # el dataset trae la columna Continent: es lo más exacto
    america = df[df[cont[0]].astype(str).str.lower() == "america"]
else:      # si no existe, usamos la lista manual
    america = df[df[c_pais].str.lower().isin([a.lower() for a in AMERICA])]
if america.empty:
    print("Aviso: no coincidió ningún país de América. Revisa cómo están escritos los nombres.")
else:
    barras(america, "Costo de vida de los países de América", "america.png", "#6366f1")
    print(f"\nPaíses de América encontrados: {len(america)}")
