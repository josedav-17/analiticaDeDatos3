import pandas as pd
from ydata_profiling import ProfileReport

# LEEMOS EL DATASET
df = pd.read_csv(
    "Datos/Calidad_Del_Aire_En_colombia.csv",
    sep=";", 
    engine="python", 
    encoding="latin1",
    on_bad_lines="skip"
)

# VISIÓN GENERAL DEL DATASET - AQUI SACAMOS LAS COLUMNAS
print("COLUMNAS DEL DATASET:")
print(df.columns)

# INFORMACIÓN GENERAL DEL DATASET - ESTO INCLUYE TIPO DE DATOS Y USO DE MEMORIA
print("\nINFORMACIÓN GENERAL DEL DATASET:")
df.info()

# RESUMEN ESTADÍSTICO
print("\nRESUMEN ESTADÍSTICO:")
print(df.describe())

# VALIDACION DE NULOS
print("\nVALORES NULOS POR COLUMNA:")
nulos = df.isnull().sum().sort_values(ascending=False)
print(nulos)

# VALIDACION DE NULOS EN PORCENTAJE
print("\nPORCENTAJE DE VALORES NULOS:")
porcentaje_nulos = (df.isnull().sum() / len(df)) * 100
print(porcentaje_nulos.sort_values(ascending=False))

# VALIDACION DE DUPLICADOS
print("\nFILAS DUPLICADAS (fila completa):")
duplicados_fila = df.duplicated().sum()
print(duplicados_fila)

# VALIDACION DE DUPLICADOS EN PORCENTAJE
porc_duplicados_fila = round((duplicados_fila / len(df)) * 100, 2)
print("Porcentaje de duplicados por fila", porc_duplicados_fila, "%")

if duplicados_fila > 0:
    print("\nEJEMPLOS DE FILAS COMPLETAS DUPLICADAS:")
    print(df[df.duplicated()].head())

# VALIDACION DE DUPLICADOS LÓGICOS - ESTO PARA RASTREAR REGISTROS QUE DEBERÍAN SER ÚNICOS SEGÚN UNA CLAVE COMPUESTA
print("\nDUPLICADOS LÓGICOS POR CLAVE ID Estación, Variable, Año:")
clave = ["ID Estacion", "Variable", "Anio"]

faltantes = [c for c in clave if c not in df.columns]
if faltantes:
    print("No se pueden evaluar duplicados lógicos. Faltan columnas:", faltantes)
else:
    mask_dup_logicos = df.duplicated(subset=clave, keep=False)
    df_dup_logicos = df[mask_dup_logicos].sort_values(clave)

    num_filas_dup_logicos = len(df_dup_logicos)
    num_claves_con_duplicados = df_dup_logicos[clave].drop_duplicates().shape[0]

    print("Filas que comparten clave lógica repetida:", num_filas_dup_logicos)
    print("Número de combinaciones ID Estacion-Variable-Año con más de un registro:", num_claves_con_duplicados)

    print("\nEJEMPLOS DE DUPLICADOS LÓGICOS:")
    print(df_dup_logicos.head(10))

# DETECCIÓN DE OUTLIERS
columnas_numericas = df.select_dtypes(include=["int64", "float64"]).columns
print("\nDETECCIÓN DE VALORES EXTREMOS (OUTLIERS) EN COLUMNAS NUMÉRICAS:")
for col in columnas_numericas:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    limite_inf = Q1 - 1.5 * IQR
    limite_sup = Q3 + 1.5 * IQR
    outliers = df[(df[col] < limite_inf) | (df[col] > limite_sup)]
    print(f"\nColumna: {col}")
    print("Cantidad de outliers:", len(outliers))

# GENERACIÓN DE REPORTE AUTOMÁTICO - USANDO YDATA PROFILING
profile = ProfileReport(df, title="Reporte Calidad del Aire en Colombia", explorative=True)
profile.to_file("Reportes/reporte_calidad_aire.html")
print("\n📄 Reporte generado: Reportes/reporte_calidad_aire.html")