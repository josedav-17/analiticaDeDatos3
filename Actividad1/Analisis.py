import pandas as pd
from ydata_profiling import ProfileReport
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el dataset
df = pd.read_csv("Calidad_Del_Aire_En_Colombia.csv", sep=",", encoding="utf-8")

# 1. DUPLICADOS
duplicados = df.duplicated().sum()
print("🔁 Total de filas duplicadas:", duplicados)

# 2. VALORES NULOS
nulos = df.isnull().sum().sort_values(ascending=False)
print("\n🚫 Valores nulos por columna:\n", nulos)

# 3. TIPOS DE DATOS
tipos = df.dtypes
print("\n🧮 Tipos de datos por columna:\n", tipos)

# 4. DISTRIBUCIONES
num_cols = df.select_dtypes(include=['int64', 'float64']).columns
for col in num_cols:
    plt.figure(figsize=(6,3))
    sns.histplot(df[col].dropna(), kde=True)
    plt.title(f'Distribución de {col}')
    plt.xlabel(col)
    plt.ylabel('Frecuencia')
    plt.tight_layout()
    plt.show()

# 5. CORRELACIONES
correlaciones = df[num_cols].corr()
print("\n🔗 Matriz de correlación:\n", correlaciones)

plt.figure(figsize=(10,8))
sns.heatmap(correlaciones, annot=True, cmap='coolwarm', center=0)
plt.title("Mapa de calor de correlaciones")
plt.show()

# 6. RESUMEN ESTADÍSTICO
resumen = df.describe(include='all').transpose()
print("\n📊 Resumen estadístico:\n", resumen)


# 7. REPORTE INTERACTIVO CON PANDAS PROFILING
profile = ProfileReport(df, title="Reporte Exploratorio - Calidad del Aire", explorative=True)
profile.to_file("reporte_calidad_aire.html")

print("\n✅ Reporte HTML generado: 'reporte_calidad_aire.html'")
