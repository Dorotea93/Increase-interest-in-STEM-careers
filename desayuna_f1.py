import pandas as pd
import numpy as np

# 1. Cargar tu Excel usando la ruta absoluta de tu ordenador
file_path = r"C:\Users\Usuario\Desktop\Trabajo_UNI\Gemelos digitales\Articulos\EDucacion\encuestas desayuna ingeniería_art_v2.0.xlsx" 
df = pd.read_excel(file_path, header=None)

# 2. Extraer los datos reales (saltando SOLO la primera fila de cabeceras)
data = df.iloc[1:].copy()

# 3. Renombrar las columnas clave para esta fase
data = data.rename(columns={
    1: 'Gen_Estudiante',  
    2: 'Edad',
    55: 'Interes_Previo', 
    56: 'Cambio_Interes'  
})

# 4. Limpieza básica
df_demo = data[['Gen_Estudiante', 'Edad', 'Interes_Previo', 'Cambio_Interes']].copy()

# Convertimos la edad a número para evitar problemas si se leyó como texto
df_demo['Edad'] = pd.to_numeric(df_demo['Edad'], errors='coerce') 

# NUEVO PASO: Eliminar filas basura/vacías al final del Excel (garantiza las 584 respuestas)
df_demo = df_demo.dropna(subset=['Gen_Estudiante', 'Edad'])

print("### 1. PERFIL DEMOGRÁFICO DE LA MUESTRA ###")
print(df_demo['Gen_Estudiante'].value_counts().to_string())
print("\nMedia de edad:", round(df_demo['Edad'].mean(), 2))
print("Desviación estándar de edad:", round(df_demo['Edad'].std(), 2))

print("\n### 2. PUNTO DE PARTIDA (Interés previo) ###")
print(df_demo['Interes_Previo'].value_counts(normalize=True).round(3) * 100)

print("\n### 3. MATRIZ DE CONVERSIÓN (El 'Efecto' del Programa) ###")
# Cruzamos el antes y el después para ver el flujo de estudiantes
tabla_conversion = pd.crosstab(df_demo['Interes_Previo'], df_demo['Cambio_Interes'], margins=True)
print(tabla_conversion)

print("\n### 4. PORCENTAJES DE ÉXITO EN INDECISOS ###")
# Porcentajes por fila
tabla_porcentajes = pd.crosstab(df_demo['Interes_Previo'], df_demo['Cambio_Interes'], normalize='index').round(3) * 100
print(tabla_porcentajes)