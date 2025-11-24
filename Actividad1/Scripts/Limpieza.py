import pandas as pd
import numpy as np

# LEEMOS EL DATASET
df = pd.read_csv(
    "Datos/Calidad_Del_Aire_En_colombia.csv",
    sep=";",
    engine="python",
    encoding="latin1",
    on_bad_lines="skip"
)

# ELIMINAMOS COLUMNAS INNECESARIAS Y DUPLICADOS
df = df.drop(columns=["Unnamed: 28"], errors="ignore")
df.columns = df.columns.str.strip()

# ELIMINAMOS DUPLICADOS EXACTOS
duplicados_exactos = df.duplicated().sum()
df = df.drop_duplicates()

# ELIMINAMOS DUPLICADOS LÓGICOS BASADOS EN CLAVE COMPUESTA
if all(c in df.columns for c in ["ID Estacion", "Variable", "Anio"]):
    duplicados_logicos = df.duplicated(subset=["ID Estacion", "Variable", "Anio"]).sum()
    df = df.drop_duplicates(subset=["ID Estacion", "Variable", "Anio"])
else:
    duplicados_logicos = 0

df = df.reset_index(drop=True)

# REPARACIÓN DE TIPOS DE DATOS Y FORMATO PORQUE EVIDENCIE PROBLEMAS DE CODIFICACIÓN
def reparar_codificacion(x):
    try:
        return x.encode("latin1").decode("utf-8")
    except:
        return x

# REPARAR Y LIMPIAR COLUMNAS DE TEXTO
cols_texto = [
    "Autoridad Ambiental","Estacion","Variable","Unidades",
    "Tipo de Estacion","Nombre del Departamento","Nombre del Municipio","Ubicacion"
]

# LIMPIEZA DE TEXTO
for c in cols_texto:
    if c in df.columns:
        df[c] = df[c].astype(str).apply(reparar_codificacion).str.strip().str.replace(r"\s+", " ", regex=True)

# LIMPIEZA DE FECHAS
for c in ["Fechas/horas del maximo", "Fechas/horas del minimo"]:
    if c in df.columns:
        df[c] = df[c].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)

# REPARAR Y LIMPIAR COLUMNAS TIPOS NUMÉRICOS
def convertir_num(c):
    df[c] = df[c].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    df[c] = pd.to_numeric(df[c], errors="coerce")

# CONVERTIR COLUMNAS A TIPOS NUMÉRICOS
columnas_float = [
    "Promedio","Suma","Representatividad Temporal","Porcentaje excedencias limite actual",
    "Mediana","Percentil 98","Maximo","Minimo","Tiempo de exposicion (horas)"
]

# CONVERTIR A FLOAT
for c in columnas_float:
    if c in df.columns:
        convertir_num(c)
        df[c] = df[c].astype(float)

# CONVERTIR A INT
columnas_int = [
    "ID Estacion","Anio","No. de datos",
    "Dias de excedencias","Codigo del Departamento","Codigo del Municipio"
]

# CONVERTIR A INT
for c in columnas_int:
    if c in df.columns:
        convertir_num(c)
        df[c] = df[c].round().astype("Int64")

# 🔥 CORRECCIÓN CLAVE → Conservamos valores reales de excedencias
if "Excedencias limite actual" in df.columns:
    df["Excedencias limite actual"] = (
        df["Excedencias limite actual"]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    df["Excedencias limite actual"] = pd.to_numeric(df["Excedencias limite actual"], errors="coerce")
    df["Excedencias limite actual"] = df["Excedencias limite actual"].fillna(0)  # Solo relleno si es NA, no sobreescribe valores válidos

# LIMPIEZA ADICIONAL Y MANEJO DE OUTLIERS
for c in ["Latitud", "Longitud"]:
    if c in df.columns:
        df[c] = df[c].astype(str).str.replace(",", ".", regex=False)
        df[c] = pd.to_numeric(df[c], errors="coerce").astype(float)

# LIMPIEZA DE FECHAS - EXTRAEMOS SOLO LA FECHA DEL PRIMER EVENTO
if "Fechas/horas del maximo" in df.columns:
    df["Fecha_max_primer_evento"] = df["Fechas/horas del maximo"].astype(str).str.split(" - ").str[0]
    df["Fecha_max_primer_evento"] = pd.to_datetime(df["Fecha_max_primer_evento"], errors="coerce", dayfirst=True)

# LIMPIEZA DE FECHAS - EXTRAEMOS SOLO LA FECHA DEL PRIMER EVENTO
if "Fechas/horas del minimo" in df.columns:
    df["Fecha_min_primer_evento"] = df["Fechas/horas del minimo"].astype(str).str.split(" - ").str[0]
    df["Fecha_min_primer_evento"] = pd.to_datetime(df["Fecha_min_primer_evento"], errors="coerce", dayfirst=True)

# MANEJO DE OUTLIERS - USANDO IQR PARA RECORTAR VALORES EXTREMOS
columnas_outliers = [
    "Promedio","Maximo","Minimo","Dias de excedencias","Porcentaje excedencias limite actual"
]

# RECORTE DE OUTLIERS
for c in columnas_outliers:
    if c in df.columns and pd.api.types.is_numeric_dtype(df[c]):
        Q1 = df[c].quantile(0.25)
        Q3 = df[c].quantile(0.75)
        IQR = Q3 - Q1
        df[c] = df[c].clip(lower=Q1 - 1.5 * IQR, upper=Q3 + 1.5 * IQR)

# MANEJO DE VALORES NULOS
df = df[df["Ubicacion"].notnull()]

# GUARDAR DATASET LIMPIO
df.to_csv("Datos/calidad_aire_limpio.csv", index=False)

# INFORME FINAL PARA PODER GENERAR EL ARCHIVO EN WORD
print("LIMPIEZA FINALIZADA")
print("Duplicados exactos eliminados:", duplicados_exactos)
print("Duplicados lógicos eliminados:", duplicados_logicos)

print("\nVALORES NULOS FINALES:")
print(df.isnull().sum().sort_values(ascending=False))

print("\nTIPOS DE DATOS FINALES:")
print(df.dtypes)
