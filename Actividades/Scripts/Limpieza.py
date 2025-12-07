import pandas as pd

RUTA_ARCHIVO = "Datos/Calidad_Del_Aire_En_Colombia.csv"

df = pd.read_csv(
    RUTA_ARCHIVO,
    sep=";", 
    encoding="latin1",
    engine="python"
)

df.columns = df.columns.str.strip()

print("✔ Datos cargados correctamente:", df.shape)

cols_texto = [
    "Autoridad Ambiental", "Estacion", "Variable", "Unidades",
    "Nombre del Departamento", "Nombre del Municipio",
    "Tipo de Estacion", "Ubicacion"
]

for c in cols_texto:
    if c in df.columns:
        df[c] = df[c].astype(str).str.strip()


def to_float_comma(series: pd.Series) -> pd.Series:
    s = (
        series.astype(str)
        .str.strip()
        .replace({"": pd.NA, "nan": pd.NA}, regex=False)
    )
    s = s.str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    return pd.to_numeric(s, errors="coerce")

for c in ["Latitud", "Longitud"]:
    if c in df.columns:
        df[c] = to_float_comma(df[c])

cols_numericas = [
    "Promedio", "Suma", "Percentil 98", "Maximo", "Minimo",
    "Representatividad Temporal"
]

for c in cols_numericas:
    if c in df.columns:
        df[c] = to_float_comma(df[c])

if "Porcentaje excedencias limite actual" in df.columns:
    s = (
        df["Porcentaje excedencias limite actual"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.strip()
    )
    s = s.str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    df["Porcentaje excedencias limite actual"] = pd.to_numeric(s, errors="coerce")


if "Dias de excedencias" in df.columns:
    df["Dias de excedencias"] = pd.to_numeric(
        df["Dias de excedencias"], errors="coerce"
    ).fillna(0).astype("Int64")
    print("✔ 'Dias de excedencias' preservado correctamente")

if "Anio" in df.columns:
    df["Anio"] = to_float_comma(df["Anio"]).round().astype("Int64")

for c in ["No. de datos", "Codigo del Municipio", "Codigo del Departamento", "ID Estacion"]:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype("Int64")

if {"Suma", "No. de datos"}.issubset(df.columns):
    df["Promedio_calculado"] = (df["Suma"] / df["No. de datos"]).astype(float)
    df["Promedio_calculado"] = df["Promedio_calculado"].round(3)
    print("✔ 'Promedio_calculado' generado correctamente")

df["Fecha_max_primer_evento"] = pd.to_datetime(
    df.get("Fechas/horas del maximo", pd.Series(dtype=str)),
    errors="coerce", dayfirst=True
)
df["Fecha_min_primer_evento"] = pd.to_datetime(
    df.get("Fechas/horas del minimo", pd.Series(dtype=str)),
    errors="coerce", dayfirst=True
)

NOMBRE_ARCHIVO = "calidad_aire_limpio_final_pwbi.csv"

df.to_csv(
    NOMBRE_ARCHIVO,
    index=False,
    sep=";", 
    decimal=",", 
    encoding="utf-8-sig"
)

print("\n📊 Resumen de columnas clave:")
print(df[["Promedio_calculado",
          "Dias de excedencias",
          "Porcentaje excedencias limite actual"]].describe())

print("\n📁 Archivo limpio generado correctamente:")
print(f"👉 {NOMBRE_ARCHIVO}")
