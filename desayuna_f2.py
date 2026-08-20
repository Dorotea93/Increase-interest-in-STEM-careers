import pandas as pd
import numpy as np
import statsmodels.api as sm

# 1. Cargar el Excel usando tu ruta
file_path = r"C:\Users\Usuario\Desktop\Trabajo_UNI\Gemelos digitales\Articulos\EDucacion\encuestas desayuna ingeniería_art_v2.0.xlsx"
df = pd.read_excel(file_path, header=None)

# 2. Extraer datos (saltando SOLO la primera fila de cabeceras)
data = df.iloc[1:].copy()

# 3. Renombrar las variables predictoras clave
data = data.rename(columns={
    1: 'Gen_Estudiante',  
    3: 'Atencion_General', # Usaremos la atención/satisfacción general como predictor
    55: 'Interes_Previo', 
    56: 'Cambio_Interes'  
})

# 4. Filtrar solo a nuestro grupo de interés (Indecisos/No orientados)
# Hacemos un dropna() inicial por si hay valores nulos en estas columnas críticas
df_modelo = data[['Gen_Estudiante', 'Atencion_General', 'Interes_Previo', 'Cambio_Interes']].dropna().copy()
df_modelo = df_modelo[df_modelo['Interes_Previo'].isin(['Bajo', 'Moderado'])]

# 5. Dicotomizar las variables para el modelo matemático (Crear variables Dummy: 0 y 1)
# Variable Dependiente: 1 si Aumentó, 0 si no
df_modelo['VD_Aumento'] = np.where(df_modelo['Cambio_Interes'] == 'Aumentó', 1, 0)

# Variables Independientes:
df_modelo['Es_Chica'] = np.where(df_modelo['Gen_Estudiante'] == 'Femenino', 1, 0)
df_modelo['Interes_Moderado'] = np.where(df_modelo['Interes_Previo'] == 'Moderado', 1, 0) # Base = Interés Bajo
df_modelo['Atencion_General'] = pd.to_numeric(df_modelo['Atencion_General'], errors='coerce')

# Limpiar cualquier fila que haya quedado con nulos tras la conversión numérica
df_modelo = df_modelo.dropna()

print(f"Tamaño de la muestra para el modelo predictivo: {len(df_modelo)} estudiantes indecisos\n")

# 6. Construir y ajustar el modelo
# Definimos las variables predictoras (X) y la variable a predecir (y)
X = df_modelo[['Es_Chica', 'Interes_Moderado', 'Atencion_General']]
X = sm.add_constant(X) # Statsmodels requiere añadir una constante al modelo
y = df_modelo['VD_Aumento']

try:
    # Ajustamos el modelo (disp=0 oculta los mensajes de iteración del cálculo)
    modelo = sm.Logit(y, X).fit(disp=0)
    
    print("### 1. RESULTADOS DE LA REGRESIÓN LOGÍSTICA ###")
    print(modelo.summary())
    
    print("\n### 2. ODDS RATIOS (Probabilidad de conversión) ###")
    # Los coeficientes puros del Logit son difíciles de interpretar, los pasamos a Odds Ratios
    or_df = pd.DataFrame(np.exp(modelo.params), columns=['Odds Ratio'])
    or_df['P-valor'] = modelo.pvalues.round(4)
    print(or_df.round(3))
    
except Exception as e:
    print("Error al calcular el modelo:", e)