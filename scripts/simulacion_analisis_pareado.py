# Simulación del experimento y análisis pareado (material complementario)
import numpy as np
import pandas as pd
from scipy import stats

tiendas = ["Quito Norte", "Quito Sur", "Guayaquil Centro", "Guayaquil Norte",
           "Cuenca Centro", "Cuenca Sur", "Ambato Centro", "Manta", "Loja", "Machala"]
semanas = [1, 2, 3, 4]

# --- Diseño: sorteo de la condición inicial (5 y 5, con semilla) ---
rng = np.random.default_rng(2026)
primera = rng.permutation(["pasillo_principal"] * 5 + ["habitual"] * 5)

filas = []
for tienda, cond in zip(tiendas, primera):
    otra = "habitual" if cond == "pasillo_principal" else "pasillo_principal"
    for s in semanas:
        filas.append({"tienda": tienda, "semana": s,
                      "ubicacion": cond if s % 2 == 1 else otra})
diseno = pd.DataFrame(filas)

# --- Simulación de ventas (datos ficticios, solo para probar el análisis) ---
rng = np.random.default_rng(1234598)
efecto_tienda = dict(zip(tiendas, rng.normal(1100, 120, len(tiendas))))
efecto_semana = {1: 0, 2: 30, 3: 60, 4: 90}

diseno["ventas_producto"] = (
    diseno["tienda"].map(efecto_tienda)
    + diseno["semana"].map(efecto_semana)
    + (diseno["ubicacion"] == "pasillo_principal") * 220
    + rng.normal(0, 90, len(diseno))
).round(0).astype(int)

# Promoción simultánea registrada (confusor)
diseno["promocion_simultanea"] = "no"
mask = (diseno["tienda"] == "Guayaquil Centro") & (diseno["semana"] == 1)
diseno.loc[mask, "promocion_simultanea"] = "si"
diseno.loc[mask, "ventas_producto"] += 180

diseno.to_csv("resultado_simulacion.csv", index=False)

# --- Análisis pareado: una fila por tienda ---
piv = diseno.groupby(["tienda", "ubicacion"])["ventas_producto"].mean().unstack()
piv["diferencia"] = piv["pasillo_principal"] - piv["habitual"]
print(piv.round(1))

n = len(piv)
media = piv["diferencia"].mean()
dev = piv["diferencia"].std(ddof=1)
print(f"\nMedia de la diferencia: {media:.2f}")
print(f"Desviación estándar: {dev:.2f}")

t_crit = stats.t.ppf(0.975, df=n - 1)
ic_inf = media - t_crit * dev / n ** 0.5
ic_sup = media + t_crit * dev / n ** 0.5
print(f"IC 95% = [{ic_inf:.2f}, {ic_sup:.2f}]")

prueba = stats.ttest_rel(piv["pasillo_principal"], piv["habitual"])
print(f"Prueba t pareada: t = {prueba.statistic:.2f}, p = {prueba.pvalue:.10f}")
