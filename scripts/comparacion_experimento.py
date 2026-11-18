# comparacion_experimento.py — Comparación de grupos (Python)
# Ejecutar desde la raíz del repositorio:
#   python scripts/comparacion_experimento.py
import pandas as pd

# TODO 1: cargar plantillas/registro_experimento.csv con pandas
df = pd.read_csv("plantillas/registro_experimento.csv")

# TODO 2: promedio de ventas_producto por ubicacion
promedios = df.groupby("ubicacion")["ventas_producto"].mean()
print(promedios)

# TODO 3: número de registros por grupo
print(df["ubicacion"].value_counts())

# TODO 4: interpretación (sección 9 de la plantilla)
# - pasillo_principal muestra mayor venta promedio (1335 vs 1040).
# - Con 4 filas (2 por grupo, de tiendas distintas y una con promoción)
#   no se puede estimar la variabilidad ni descartar el azar o el efecto
#   de la tienda y la promoción.
# - Faltaría: más unidades, comparación pareada por tienda, IC 95 % /
#   prueba t, y excluir o ajustar las unidades con promoción simultánea.
