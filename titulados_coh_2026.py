
import pyodbc
import pandas as pd
import numpy as np

from MAT_2025 import MAT 


# Importa la variable di rectamente


con_1 = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER=158.170.66.56,{1433};"
    f"DATABASE=PROC01ESTUDIO;"
    f"UID=proceso;"
    f"PWD=Estudio.2024;")

con_2 = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER=158.170.66.56,{1433};"
    f"DATABASE=TABLAS_ESTUDIO;"
    f"UID=base_estudio;"
    f"PWD=Estudio.T4b145;")

print("Conexión exitosa")



####listado de tablas
cursor_1 = con_1.cursor()
cursor_1.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.\
                 TABLES WHERE TABLE_TYPE = 'BASE TABLE';")


for t in cursor_1.fetchall():
    print(t)
####listado de campos

cursor_1 = con_1.cursor()
columnas=cursor_1.execute("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.\
                          COLUMNS WHERE TABLE_NAME='COHORTE_AL_20240502';")

                          
for c in columnas.fetchall():
    print(c)



tabla_coh_act = MAT[MAT['COH_CIDI'] == 1]

tabla_coh_act['rut_codigo_carrera'] = tabla_coh_act['rut'].astype(str) + '-' + tabla_coh_act['CODIGO_CARRERA'].astype(str)

tabla_titulados = pd.read_sql("""SELECT      
          t.RUT,
          t.COD_PLAN,
          t.NIVEL_TIT_GRADO,
          t.ANHO_ACADEMICO,
          t.FECHA_RESOL,
          t.NUM_SEM_SUSP,
          t.FECHA_TITULO,
          t.NOMBRE_PLAN,
          CONCAT(t.RUT, '-', c.cod_carr_prog) AS rut_codigo_carrera,
          t.NOMBRE_TIT_GRADO,
          c.cod_carr_prog AS codigo_carrera
          FROM TITULADOS_2008_2025 t
          LEFT JOIN COD_PLAN_COD_CARRERA c
          ON t.COD_PLAN = c.cod_plan
          WHERE UPPER(t.NIVEL_TIT_GRADO) = 'TERMINAL'""", con_1)

titulados_coh = tabla_coh_act.merge(tabla_titulados, on='rut_codigo_carrera', how='left')

titulados_coh['ANHO_INI']=np.where(titulados_coh['periodo_ingreso'] == "01",  
                                   titulados_coh['ANHO_ING'].astype(str) +"-01-01",
                                   titulados_coh['ANHO_ING'].astype(str)+ "-08-08")


titulados_coh['ANHO_INI']=pd.to_datetime(titulados_coh['ANHO_INI'], 
                                         format='%Y-%m-%d')
titulados_coh['FECHA_TITULO']=pd.to_datetime(titulados_coh['FECHA_TITULO'], 
                                             format='%Y-%m-%d')


#titulados_coh['Duracion_semestres']=((titulados_coh['FECHA_TITULO'] - 
#                                      titulados_coh['ANHO_INI']).dt.days/30)/6

####Calculo 2
titulados_coh['Duracion_semestres'] = (round((titulados_coh['FECHA_TITULO'] - 
                                              titulados_coh['ANHO_INI']).dt.days,0)/30.4)/6

titulados_coh['titulado']=np.where(titulados_coh['NIVEL_TIT_GRADO']=="TERMINAL", 1,0)


titulados_coh['NIVEL_TIT_GRADO'].value_counts()

titulados_coh['DURACION_TOTAL'] = pd.to_numeric(titulados_coh['DURACION_TOTAL'], errors='coerce')


titulados_coh=titulados_coh.fillna(999)


titulados_coh['NIVEL_TIT_GRADO']=titulados_coh['NIVEL_TIT_GRADO'].fillna("999")

titulados_coh['exacto']=np.where((titulados_coh['NIVEL_TIT_GRADO']=="TERMINAL") & 
                                 ((titulados_coh['Duracion_semestres'] - 
                                  titulados_coh['DURACION_TOTAL']).fillna(999)<=0),1,0)

titulados_coh['oportuno']=np.where((titulados_coh['NIVEL_TIT_GRADO']=="TERMINAL") & 
                                   ((titulados_coh['Duracion_semestres'] - 
                                    titulados_coh['DURACION_TOTAL']).fillna(999)<=2),1,0)


VIA_INC=[97, 81, 26, 71, 75, 87,20,21,30,70,72, 44]



titulados_coh['INC'] = titulados_coh['cod_via'].isin(VIA_INC).astype(int)
titulados_coh['DUR_ANO'] = titulados_coh['DURACION_TOTAL']/2

titulados_coh = titulados_coh.assign(
    anho_op_arriba = np.ceil(titulados_coh['ANHO_ING'] + titulados_coh['DUR_ANO']),
    anho_op_abajo  = np.floor(titulados_coh['ANHO_ING'] + titulados_coh['DUR_ANO'])
)

titulados_coh['anho_op_arriba'] = np.ceil(titulados_coh['ANHO_ING'] + titulados_coh['DUR_ANO']).astype('Int64')
titulados_coh['anho_op_abajo'] = np.floor(titulados_coh['ANHO_ING'] + titulados_coh['DUR_ANO']).astype('Int64')



titulados_coh['NIVEL_GLOBAL_2'] = np.where(titulados_coh['NOMBRE_TIT_GRADO'].str.contains('DIPLOMADO', na=False), "DIPLOMADO", titulados_coh['NIVEL_GLOBAL'])

titulados_coh[(titulados_coh['anho_op_arriba'] == 2025) & 
              (titulados_coh['INC'] == 1)][['rut','sexo', 
                                            'cod_plan', 
                                            'ANHO_ING',
                                            'CODIGO_CARRERA',
                                            'cod_via',
                                            'DURACION_TOTAL', 
                                            'anho_op_arriba', 
                                            'anho_op_abajo', 
                                            'oportuno', 'exacto',
                                            'NIVEL_TIT_GRADO',
                                            'NOMBRE_TIT_GRADO', 
                                            'NIVEL_GLOBAL_2']].to_clipboard()
              


titulados_coh['anho_rut_cod'] = titulados_coh['ANHO_ING'].astype(str) +"-"+titulados_coh['rut'].astype(str) +"-"+ titulados_coh['cod_plan'].astype(str)

titulados_coh['dup'] = (titulados_coh.groupby('anho_rut_cod')['anho_rut_cod'].transform('size') > 1).astype(int)

tabla_tasa_oportuno = (
titulados_coh.groupby(['COH_CIDI', 
                       'CODIGO_CARRERA', 
                       'NIVEL_GLOBAL_2',
                       'ANHO_ING',
                       'anho_op_arriba',
                       'oportuno'])['rut']
.nunique()
.unstack()
.reset_index()
.assign(tasa = lambda x: x[1]/ (x[0] + x[1]))
)

tabla_tasa_oportuno.to_csv("tabla_tasa_oportuno.csv", index=False)

titulados_coh.drop_duplicates(subset='anho_rut_cod', keep='first', inplace=True)

