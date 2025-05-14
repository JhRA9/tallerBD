import os
import comtradeapicall
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Configuro mi clave de API para usarla en las consultas
os.environ['COMTRADE_API_KEY'] = '1f7e33652d3b4c4cb40f19f37a48e3ff'

# Consulto los datos de exportacion de cafe para cada ano
years = ['2021', '2022']
lista_dfs = []
for year in years:
    print(f"Consultando datos para el ano {year}...")
    df_year = comtradeapicall.previewFinalData(
        typeCode='C',
        freqCode='A',
        clCode='HS',
        period=year,
        reporterCode='170',
        partnerCode='842',
        partner2Code='',
        customsCode='',
        motCode='',
        cmdCode='0901',
        flowCode='X',
        includeDesc=True
    )
    lista_dfs.append(df_year)

# Uno los resultados en un solo DataFrame
mydf = pd.concat(lista_dfs, ignore_index=True)
print("He unido los datos de ambos anos y ahora tengo esta vista preliminar:")
print(mydf.head())

# Reviso las columnas y obtengo un resumen estadistico
print("Columnas disponibles en el DataFrame:", mydf.columns.tolist())
print(mydf[['period', 'fobvalue', 'netWgt']].describe())

# Exporto los datos a un archivo Excel
excel_file = 'exportaciones_cafe_col_usa.xlsx'
print(f"Guardando los datos en '{excel_file}'...")
mydf.to_excel(excel_file, index=False)
print("El archivo Excel fue creado:", os.path.exists(excel_file))

# Almaceno los datos en una base de datos SQLite
db_file = 'comtrade.db'
tabla = 'exportaciones_cafe_col_usa'
print(f"Conectando o creando la base SQLite '{db_file}'...")
conn = sqlite3.connect(db_file)
print(f"Guardando datos en la tabla '{tabla}'...")
mydf.to_sql(tabla, conn, if_exists='replace', index=False)

# Verifico las primeras filas de la tabla en SQLite
temp = pd.read_sql_query(f"SELECT * FROM {tabla} LIMIT 5", conn)
print("Primeras filas en la tabla SQLite:")
print(temp)

# Cierro la conexion a la base de datos
try:
    conn.close()
    print("Conexion SQLite cerrada.")
except Exception:
    pass

# Grafico el valor de exportaciones por ano
print("Generando grafico de columnas para comparar 2021 vs 2022...")
graph = mydf.groupby('period')['fobvalue'].sum()
graph.plot(kind='bar')
plt.title('Exportaciones de cafe de Colombia a EE.UU. (2021-2022)')
plt.xlabel('Ano')
plt.ylabel('Valor comercial (USD)')
plt.grid(True)
plt.tight_layout()
plt.show()