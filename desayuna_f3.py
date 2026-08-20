import pandas as pd
import numpy as np
import statsmodels.api as sm

# 1. Cargar la hoja principal
file_path = r"C:\Users\Usuario\Desktop\Trabajo_UNI\Gemelos digitales\Articulos\EDucacion\encuestas desayuna ingeniería_art_v2.0.xlsx"
df_main = pd.read_excel(file_path, header=None)

# 2. Preparar los datos base (CORREGIDO: iloc[1:] para no perder las primeras respuestas)
data = df_main.iloc[1:].copy().reset_index(drop=True)
data['Student_ID'] = data.index

data = data.rename(columns={
    1: 'Gen_Estudiante',
    55: 'Interes_Previo',
    56: 'Cambio_Interes'
})

# 3. Filtrar alumnado indeciso
indecisos = data[data['Interes_Previo'].isin(['Bajo', 'Moderado'])].copy()

indecisos['VD_Aumento'] = np.where(indecisos['Cambio_Interes'] == 'Aumentó', 1, 0)
indecisos['Es_Chica'] = np.where(indecisos['Gen_Estudiante'] == 'Femenino', 1, 0)
indecisos['Interes_Moderado'] = np.where(indecisos['Interes_Previo'] == 'Moderado', 1, 0)

# 4. Diccionario de mentores por columna de participación
mentores_map = {
    4:  {'tipo': 'Estudiante Universitario', 'genero': 'Hombre'},
    6:  {'tipo': 'Profesor Senior',          'genero': 'Hombre'},
    8:  {'tipo': 'Profesor Senior',          'genero': 'Hombre'},
    10: {'tipo': 'Estudiante Universitario', 'genero': 'Hombre'},
    12: {'tipo': 'Investigador Joven',       'genero': 'Mixto'},
    14: {'tipo': 'Investigador Joven',       'genero': 'Mujer'},
    16: {'tipo': 'Investigador Joven',       'genero': 'Hombre'},
    18: {'tipo': 'Investigador Joven',       'genero': 'Mixto'},
    20: {'tipo': 'Profesor Senior',          'genero': 'Hombre'},
    22: {'tipo': 'Profesor Senior',          'genero': 'Mixto'},
    24: {'tipo': 'Investigador Joven',       'genero': 'Mixto'},
    26: {'tipo': 'Profesor Senior',          'genero': 'Hombre'},
    28: {'tipo': 'Profesor Senior',          'genero': 'Hombre'},
    30: {'tipo': 'Investigador Joven',       'genero': 'Mixto'},
    32: {'tipo': 'Investigador Joven',       'genero': 'Mixto'},
    34: {'tipo': 'Investigador Joven',       'genero': 'Hombre'},
    36: {'tipo': 'Investigador Joven',       'genero': 'Mixto'},
    38: {'tipo': 'Investigador Joven',       'genero': 'Hombre'},
    40: {'tipo': 'Profesor Senior',          'genero': 'Mixto'},
    42: {'tipo': 'Investigador Joven',       'genero': 'Mixto'},
    44: {'tipo': 'Profesor Senior',          'genero': 'Mixto'},
    46: {'tipo': 'Profesor Senior',          'genero': 'Hombre'},
    48: {'tipo': 'Investigador Joven',       'genero': 'Mujer'}
}

# 5. Construir huella de experiencia por estudiante
records = []

for _, row in indecisos.iterrows():
    sid = row['Student_ID']
    participaciones = []
    satisfacciones = []
    tuvo_mujer = 0

    # Columnas de participación: 4,6,8,...,48
    # Columnas de satisfacción: 5,7,9,...,49
    for col_p in range(4, 50, 2):
        col_s = col_p + 1

        val_p = pd.to_numeric(row[col_p], errors='coerce')
        val_s = pd.to_numeric(row[col_s], errors='coerce') if col_s in row.index else np.nan

        # Si respondió al menos una de las dos, asumimos asistencia al taller
        if pd.notna(val_p) or pd.notna(val_s):
            if pd.notna(val_p):
                participaciones.append(val_p)
            if pd.notna(val_s):
                satisfacciones.append(val_s)

            mentor_info = mentores_map.get(col_p)
            if mentor_info and mentor_info['genero'] in ['Mujer', 'Mixto']:
                tuvo_mujer = 1

    if len(participaciones) > 0 or len(satisfacciones) > 0:
        records.append({
            'Student_ID': sid,
            'Mean_Participacion': np.mean(participaciones) if len(participaciones) > 0 else np.nan,
            'Mean_Satisfaccion': np.mean(satisfacciones) if len(satisfacciones) > 0 else np.nan,
            'Tuvo_Mentora_Mujer': tuvo_mujer
        })

df_agregado = pd.DataFrame(records)

# 6. Unir con variables base
model_data = pd.merge(
    indecisos[['Student_ID', 'VD_Aumento', 'Es_Chica', 'Interes_Moderado']],
    df_agregado,
    on='Student_ID',
    how='inner'
)

# 7. Eliminar nulos solo en variables del modelo
model_data = model_data.dropna(subset=[
    'VD_Aumento',
    'Es_Chica',
    'Interes_Moderado',
    'Mean_Participacion',
    'Mean_Satisfaccion',
    'Tuvo_Mentora_Mujer'
])

print(f"Muestra final procesada: {len(model_data)} estudiantes indecisos\n")

# 8. Ajustar modelo logístico final
X = model_data[
    ['Es_Chica',
     'Interes_Moderado',
     'Mean_Participacion',
     'Mean_Satisfaccion',
     'Tuvo_Mentora_Mujer']
]

X = sm.add_constant(X)
y = model_data['VD_Aumento']

try:
    modelo_final = sm.Logit(y, X).fit(disp=0)

    print("### 1. MODELO LOGÍSTICO FINAL ###")
    print(modelo_final.summary())

    print("\n### 2. ODDS RATIOS ###")
    conf = modelo_final.conf_int()
    or_df = pd.DataFrame({
        'Odds Ratio': np.exp(modelo_final.params),
        'P-valor': modelo_final.pvalues,
        'IC 2.5%': np.exp(conf[0]),
        'IC 97.5%': np.exp(conf[1])
    })
    print(or_df.round(3))

except Exception as e:
    print("Error al ajustar el modelo:", e)