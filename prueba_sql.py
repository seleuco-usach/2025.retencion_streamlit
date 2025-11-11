import streamlit as st
import pyodbc
import pandas as pd
from datetime import date

st.title("Prueba de conexión a SQL Server")


#con_1 = pyodbc.connect(
 #       f"DRIVER={{ODBC Driver 17 for SQL Server}};"
  #      f"SERVER=158.170.66.56,1433;"
   #     f"DATABASE=PROC01ESTUDIO;"
    #    f"UID=proceso;"
     #   f"PWD=Estudio.2024;"
    #)

sql = st.secrets["sqlserver"]

con_1 = pyodbc.connect(
    f"DRIVER={{{sql['driver']}}};"
    f"SERVER={sql['server']};"
    f"DATABASE={sql['database']};"
    f"UID={sql['username']};"
    f"PWD={sql['password']};"
)
st.success("✅ Conexión exitosa")

    # Mostrar tablas disponibles
    
tablas = pd.read_sql("""SELECT
                         CAST(rut AS VARCHAR(12)) AS rut,
                         cod_plan,
                         LEFT(periodo_matricula, 4) AS ANHO_MAT,
                         COUNT(rut) AS total
                         FROM MATRICULA_V2_082025_PARA_TODO
                         GROUP BY
                         CAST(rut AS VARCHAR(12)),
                         cod_plan,
                         LEFT(periodo_matricula, 4)""", con_1)
st.write("**Rut encontrados:**")
#st.dataframe(tablas)


rut_buscado = st.text_input("Ingrese el RUT a buscar (sin puntos ni guion):", "12345678")

if rut_buscado:
    resultado = tablas.loc[tablas['rut'] == rut_buscado]
    st.dataframe(resultado)


