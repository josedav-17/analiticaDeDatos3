import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Leer dataset limpio
df = pd.read_csv("Datos/calidad_aire_limpio.csv")

# Filtrar contaminante principal: PM10
df_pm10 = df[df["Variable"].str.upper().str.contains("PM10", na=False)]

print("\n📊 ANÁLISIS EXCLUSIVO DE PM10")
print(df_pm10[["Promedio", "Maximo", "Minimo", "Dias de excedencias", "Excedencias limite actual"]].describe())

# Correlación PM10 vs Excedencias
print("\n🔗 CORRELACIÓN ENTRE PM10 Y EXCEDENCIAS:")
print(df_pm10[["Promedio", "Maximo", "Minimo", "Dias de excedencias", "Excedencias limite actual"]].corr())

# Evolución temporal PM10
print("\n📈 TENDENCIA TEMPORAL DE PM10:")
print(df_pm10.groupby("Anio")["Promedio"].mean())

# Top estaciones con mayor PM10
print("\n🌍 ESTACIONES CON MAYOR CONTAMINACIÓN PM10:")
print(df_pm10.groupby("Estacion")["Promedio"].mean().sort_values(ascending=False).head(10))

# Si hay variables meteorológicas relacionadas con este contaminante
variables_meteo = [
    "Tiempo de exposicion (horas)", "Representatividad Temporal",
    "Percentil 98", "Mediana"
]
variables_correlacion = [v for v in variables_meteo if v in df_pm10.columns] + \
    ["Promedio", "Maximo", "Excedencias limite actual"]

print("\n🧠 MATRIZ DE CORRELACIÓN PM10 vs VARIABLES RELACIONADAS:")
correlacion_pm10 = df_pm10[variables_correlacion].corr()
print(correlacion_pm10)

# Heatmap
plt.figure(figsize=(10,6))
sns.heatmap(correlacion_pm10, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlación PM10 vs variables ambientales")
plt.show()
