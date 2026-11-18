import numpy as np
import pandas as pd

tiendas = ["Quito Norte", "Quito Sur", "Guayaquil Centro", "Guayaquil Norte",
           "Cuenca Centro", "Cuenca Sur", "Ambato Centro", "Manta", "Loja", "Machala"]

rng = np.random.default_rng(2026)
# Sorteo balanceado: 5 tiendas empiezan en pasillo_principal y 5 en habitual
orden = rng.permutation(["pasillo_principal"] * 5 + ["habitual"] * 5)

filas = []
for tienda, ini in zip(tiendas, orden):
    otra = "habitual" if ini == "pasillo_principal" else "pasillo_principal"
    for semana in [1, 2, 3, 4]:
        filas.append({"tienda": tienda, "semana": semana,
                      "ubicacion": ini if semana % 2 == 1 else otra})
diseno = pd.DataFrame(filas)
print(diseno.drop_duplicates("tienda")[["tienda", "ubicacion"]]
      .rename(columns={"ubicacion": "ubicacion_semana1"}).to_string(index=False))
print("\nUnidades (tienda-semana) por ubicacion:")
print(diseno["ubicacion"].value_counts())
diseno.to_csv("plantillas/asignacion_diseno.csv", index=False
