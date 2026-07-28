import pandas as pd
import numpy as np
import statsmodels.api as sm

file_path = r"C:\Users\Usuario\Desktop\Trabajo_UNI\Gemelos digitales\Articulos\EDucacion\encuestas desayuna ingeniería_art_v2.0.xlsx"
df_main = pd.read_excel(file_path, header=None)

# 1. CORRECCIÓN: Usar iloc[1:] para no perder las dos primeras filas de respuestas
data = df_main.iloc[1:].copy().reset_index(drop=True)
data['Student_ID'] = data.index
data = data.rename(columns={1: 'Gen_Estudiante', 55: 'Interes_Previo', 56: 'Cambio_Interes'})

indecisos = data[data['Interes_Previo'].isin(['Bajo', 'Moderado'])].copy()
indecisos['VD_Aumento'] = np.where(indecisos['Cambio_Interes'] == 'Aumentó', 1, 0)
indecisos['Es_Chica'] = np.where(indecisos['Gen_Estudiante'] == 'Femenino', 1, 0)
indecisos['Interes_Moderado'] = np.where(indecisos['Interes_Previo'] == 'Moderado', 1, 0)

mentores_map = {
    4:  {'tipo': 'Estudiante Universitario', 'genero': 'Hombre'},
    6:  {'tipo': 'Profesor Senior', 'genero': 'Hombre'},
    8:  {'tipo': 'Profesor Senior', 'genero': 'Hombre'},
    10: {'tipo': 'Estudiante Universitario', 'genero': 'Hombre'},
    12: {'tipo': 'Investigador Joven', 'genero': 'Mixto'},
    14: {'tipo': 'Investigador Joven', 'genero': 'Mujer'},
    16: {'tipo': 'Investigador Joven', 'genero': 'Hombre'},
    18: {'tipo': 'Investigador Joven', 'genero': 'Mixto'},
    20: {'tipo': 'Profesor Senior', 'genero': 'Hombre'},
    22: {'tipo': 'Profesor Senior', 'genero': 'Mixto'},
    24: {'tipo': 'Investigador Joven', 'genero': 'Mixto'},
    26: {'tipo': 'Profesor Senior', 'genero': 'Hombre'},
    28: {'tipo': 'Profesor Senior', 'genero': 'Hombre'},
    30: {'tipo': 'Investigador Joven', 'genero': 'Mixto'},
    32: {'tipo': 'Investigador Joven', 'genero': 'Mixto'},
    34: {'tipo': 'Investigador Joven', 'genero': 'Hombre'},
    36: {'tipo': 'Investigador Joven', 'genero': 'Mixto'},
    38: {'tipo': 'Investigador Joven', 'genero': 'Hombre'},
    40: {'tipo': 'Profesor Senior', 'genero': 'Mixto'},
    42: {'tipo': 'Investigador Joven', 'genero': 'Mixto'},
    44: {'tipo': 'Profesor Senior', 'genero': 'Mixto'},
    46: {'tipo': 'Profesor Senior', 'genero': 'Hombre'},
    48: {'tipo': 'Investigador Joven', 'genero': 'Mujer'}
}

records = []
for _, row in indecisos.iterrows():
    participaciones, satisfacciones = [], []
    for col_p in range(4, 50, 2):
        col_s = col_p + 1
        val_p = pd.to_numeric(row[col_p], errors='coerce')
        val_s = pd.to_numeric(row[col_s], errors='coerce') if col_s in row.index else np.nan
        if pd.notna(val_p) or pd.notna(val_s):
            if pd.notna(val_p):
                participaciones.append(val_p)
            if pd.notna(val_s):
                satisfacciones.append(val_s)

    records.append({
        'Student_ID': row['Student_ID'],
        'Mean_Participacion': np.mean(participaciones) if participaciones else np.nan,
        'Mean_Satisfaccion': np.mean(satisfacciones) if satisfacciones else np.nan
    })

df_agregado = pd.DataFrame(records)

model_data = pd.merge(
    indecisos[['Student_ID', 'VD_Aumento', 'Es_Chica', 'Interes_Moderado']],
    df_agregado,
    on='Student_ID',
    how='inner'
).dropna(subset=['VD_Aumento', 'Interes_Moderado', 'Mean_Participacion', 'Mean_Satisfaccion'])

def correr(df, nombre):
    print(f"\n### {nombre} ###")
    print("N =", len(df))
    print("VD_Aumento:", df['VD_Aumento'].value_counts().to_dict())

    X = df[['Interes_Moderado', 'Mean_Participacion', 'Mean_Satisfaccion']]
    X = sm.add_constant(X)
    y = df['VD_Aumento']

    try:
        m = sm.Logit(y, X).fit(disp=0)
        print(m.summary())
        conf = m.conf_int()
        or_df = pd.DataFrame({
            'Odds Ratio': np.exp(m.params),
            'P-valor': m.pvalues,
            'IC 2.5%': np.exp(conf[0]),
            'IC 97.5%': np.exp(conf[1])
        })
        print(or_df.round(3))
    except Exception as e:
        print("Error:", e)

correr(model_data[model_data['Es_Chica'] == 1].copy(), "CHICAS")
correr(model_data[model_data['Es_Chica'] == 0].copy(), "CHICOS")