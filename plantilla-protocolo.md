# Plantilla de protocolo — Experimento de ubicación de producto

**Equipo:** ___ · **Integrantes:** ___ · **Fecha:** 18/11/2026
**Fork:** (pega aquí el enlace de tu fork)

---

## 1. Pregunta e hipótesis

**Pregunta:** ¿cambiar la ubicación del producto estrella al pasillo principal aumenta sus ventas?

**Hipótesis (H1):** durante 4 semanas, las ventas semanales del producto estrella (unidades vendidas por tienda y semana) son, en promedio, mayores cuando el producto está en el pasillo principal (tratamiento) que cuando está en su ubicación habitual (control).

**Hipótesis nula (H0):** la media de ventas semanales es igual en ambas ubicaciones (μ_principal − μ_habitual = 0).

Se refuta si el intervalo de confianza al 95 % de la diferencia pareada incluye el 0 (o p ≥ 0,05).

## 2. Unidad experimental

**Unidad:** la combinación **tienda-semana** (una tienda durante una semana), que es lo que recibe una ubicación. Las tiendas actúan como bloques: cada una pasa por ambas condiciones (diseño cruzado o *crossover*).

**Número de unidades y justificación:** 10 tiendas × 4 semanas = **40 unidades** (20 con pasillo principal y 20 con ubicación habitual). Se usan 10 tiendas de distintas ciudades (Quito, Guayaquil, Cuenca, Ambato, Manta, Loja, Machala) para cubrir contextos variados. Como cada tienda es su propio control, se elimina la variación entre tiendas (tamaño, ciudad, clientela), lo que permite detectar efectos con pocas tiendas. 4 semanas bastan para alternar dos veces la condición sin alargar demasiado el experimento ni mezclar temporadas.

## 3. Factor, niveles y tratamiento

- **Factor (variable manipulada):** ubicación del producto estrella en la tienda.
- **Niveles:** `pasillo_principal` y `habitual`.
- **Tratamiento (combinación asignada):** mover el producto estrella al pasillo principal durante una semana. El pasillo principal es un *nivel* del factor; el *tratamiento* es la acción de asignar ese nivel a la unidad tienda-semana. Todo lo demás (precio, producto, empaque, horario) queda igual.

## 4. Grupo de control

**Referencia:** las unidades tienda-semana en las que el producto permanece en su **ubicación habitual**, sin ningún cambio.

**Rol:** da la línea base de ventas que se habría observado sin intervenir. Sin ella no se sabría si un aumento se debe a la ubicación o a otras causas (tendencia, temporada, afluencia). Como la misma tienda aparece en ambos grupos, el control es especialmente comparable.

## 5. Aleatorización

**Método:** en cada tienda se alternan las condiciones por semana (semanas 1 y 3 una condición; semanas 2 y 4 la otra). **Lo que se sortea es qué condición va primero en cada tienda**: 5 tiendas empiezan en pasillo principal y 5 en habitual (permutación al azar, balanceada).

**Por qué es necesario:** si la gerencia eligiera, por ejemplo, empezar con pasillo principal en las mejores tiendas, o en la semana de más afluencia, la diferencia mezclaría ubicación con otros factores (sesgo de selección). El sorteo hace que los factores conocidos y desconocidos se repartan al azar entre los grupos. Además el orden balanceado compensa tendencias en el tiempo (p. ej. ventas que suben cada semana), porque cada condición ocupa en promedio las mismas semanas.

**Código (Python, semilla 2026):** `scripts/asignacion_aleatoria.py`

```python
import numpy as np
rng = np.random.default_rng(2026)
orden = rng.permutation(["pasillo_principal"] * 5 + ["habitual"] * 5)
```

**Resultado de la corrida** (condición de la semana 1; la semana 2 es la otra, la 3 repite la 1, la 4 repite la 2):

| Tienda | Semana 1 |
|---|---|
| Quito Norte | pasillo_principal |
| Quito Sur | habitual |
| Guayaquil Centro | pasillo_principal |
| Guayaquil Norte | habitual |
| Cuenca Centro | habitual |
| Cuenca Sur | pasillo_principal |
| Ambato Centro | habitual |
| Manta | pasillo_principal |
| Loja | habitual |
| Machala | pasillo_principal |

Resultado: 20 unidades `pasillo_principal` y 20 `habitual`. Como el investigador asigna con código, es un **experimento** y no un estudio observacional.

## 6. Respuesta y medición

- **Variable respuesta:** ventas del producto estrella (`ventas_producto`, en unidades vendidas por tienda y semana).
- **Período de medición:** 4 semanas (lunes a domingo), con cambio de ubicación cada lunes antes de abrir.
- **Quién registra y cómo:** el sistema de punto de venta (POS) registra automáticamente las ventas, y el analista de BI las extrae al `registro_experimento.csv`. Los cajeros no pueden ser ciegos al tratamiento, ni los clientes, porque la ubicación es visible. El **ciego parcial** se logra porque el analista que compara los datos recibe los grupos codificados (A/B) hasta terminar el análisis. Límite: no hay doble ciego posible.

## 7. Factores a controlar (mínimo 4)

| Factor a controlar | Cómo se controla o registra |
|---|---|
| 1. Promociones simultáneas | Prohibir promociones del producto durante el experimento; si ocurre alguna, se registra en la columna `promocion_simultanea` y se excluye o ajusta esa unidad. |
| 2. Temporada / semana del mes | Alternar condiciones dentro de cada tienda (cruzado) y balancear el orden, de modo que ambas condiciones pasen por las mismas semanas. Evitar feriados y quincena de pago, o registrarlos. |
| 3. Afluencia de clientes | Registrar el número de tickets o visitantes por tienda y semana, y usarlo como covariable o razón (ventas por cliente). |
| 4. Stock del producto | Garantizar abastecimiento igual en ambas condiciones; registrar quiebres de stock y excluir las semanas afectadas. |
| 5. Precio | Mantener el precio fijo durante las 4 semanas en todas las tiendas. |
| 6. Tamaño y ciudad de la tienda | Bloqueo: cada tienda es su propio control (diseño pareado). |

## 8. Limitaciones del diseño

- **Efecto de arrastre (*carryover*):** clientes que se acostumbraron a ver el producto en el pasillo principal podrían seguir buscándolo ahí la semana siguiente; se mitiga alternando y, idealmente, con una semana de lavado.
- **Pocas tiendas (N = 10) y solo 4 semanas:** poca potencia; un efecto pequeño podría no detectarse, y una tendencia temporal fuerte podría distorsionar.
- **Sin ciego real:** el personal sabe qué condición se aplica y podría, sin querer, recomendar más el producto.
- **Efecto de novedad:** el aumento podría deberse a que el cambio llama la atención y desaparecer con el tiempo.
- **Generalización:** los resultados valen para el producto estrella y estas 10 tiendas; no se podrá concluir lo mismo para otros productos, ciudades o épocas (p. ej. Navidad).
- **Canibalización:** no se mide si subir este producto reduce las ventas de otros del mismo pasillo, así que no se concluye sobre la rentabilidad total.
- **Promociones no previstas** (como una promoción local en una semana) pueden confundirse con el efecto de la ubicación si no se registran.

## 9. Comparación en código (Python)

Script: `scripts/comparacion_experimento.py`

```python
import pandas as pd

df = pd.read_csv("plantillas/registro_experimento.csv")
promedios = df.groupby("ubicacion")["ventas_producto"].mean()
print(promedios)
print("\nMayor venta promedio:", promedios.idxmax())
print("Diferencia (principal - habitual):",
      promedios["pasillo_principal"] - promedios["habitual"])
print("Filas por grupo:\n", df["ubicacion"].value_counts())
```

**Salida** (sobre `plantillas/registro_experimento.csv`, 4 filas):

```
ubicacion
habitual             1040.0
pasillo_principal    1335.0
Name: ventas_producto, dtype: float64

Mayor venta promedio: pasillo_principal
Diferencia (principal - habitual): 295.0
Filas por grupo:
 ubicacion
pasillo_principal    2
habitual             2
```

**Preguntas:**

1. **¿Qué grupo muestra mayor venta promedio?** `pasillo_principal` (1335 vs. 1040, diferencia de 295).
2. **¿Por qué con 4 filas no se puede concluir nada?** Con 2 filas por grupo no se puede estimar la variabilidad ni calcular un intervalo o p-valor fiables; una sola semana atípica movería el promedio. Además, la plantilla no fue aleatorizada ni controla promociones, semana o afluencia. Las 4 filas son de la semana 1 y de tiendas distintas (no pareadas), y Guayaquil Centro tuvo `promocion_simultanea = si`, que infla el promedio del pasillo principal. Una diferencia de 295 podría ser puro azar, tienda o promoción, no ubicación.
3. **¿Qué le faltaría al análisis para ser justo?** Con el protocolo ejecutado (40 unidades): (a) comparar de forma **pareada** por tienda (diferencia pasillo − habitual en cada tienda); (b) calcular el **intervalo de confianza al 95 %** y la **prueba t pareada**; (c) excluir o ajustar las unidades con promoción simultánea o quiebre de stock; (d) considerar la semana y la afluencia como covariables; (e) reportar el tamaño del efecto junto con el p-valor.

---

## Bonus (+5): adaptación a un ensayo clínico (vacuna)

| Elemento | Ubicación de producto | Ensayo de vacuna |
|---|---|---|
| Unidad experimental | tienda-semana | participante (adultos voluntarios) |
| Factor / niveles | ubicación: principal / habitual | vacuna: candidata / placebo |
| Control | ubicación habitual | grupo placebo |
| Aleatorización | sorteo del orden por tienda | sorteo con semilla de cada participante a vacuna o placebo (idealmente estratificado por edad y sexo) |
| Respuesta | ventas semanales | casos confirmados de la enfermedad en el seguimiento |
| Ciego | parcial (analista) | **doble ciego**: ni participantes ni evaluadores saben quién recibe qué |
| Factores a controlar | promociones, afluencia, stock, precio | edad, sexo, comorbilidades, exposición, centro de salud |
| Limitaciones | arrastre, novedad | abandono, ética (no dejar sin tratamiento), generalización |

La lógica es la misma: el investigador asigna al azar, hay un grupo de referencia, se mide la misma respuesta en ambos y se controlan los factores que podrían confundir.
