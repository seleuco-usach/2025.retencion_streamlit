import pyodbc
import pandas as pd
import numpy as np
from datetime import date


con_1 = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER=158.170.66.56,{1433};"
    f"DATABASE=PROC01ESTUDIO;"
    f"UID=proceso;"
    f"PWD=Estudio.2024;")

print("Conexión exitosa")

cursor_1 = con_1.cursor()
columnas=cursor_1.execute("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.\
                          COLUMNS WHERE TABLE_NAME='TABLA_MU';")

for c in columnas.fetchall():
    print(c)


pd.read_sql("""SELECT 
                ANHO_SIES,
                N_DOC,
                SEXO
                FROM TABLA_MU""", con_1)