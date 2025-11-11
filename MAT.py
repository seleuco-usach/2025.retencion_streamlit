#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 30 10:54:08 2025

@author: xenomorfo
"""

# %%
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

####listado de tablas
cursor_1 = con_1.cursor()
cursor_1.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.\
                 TABLES WHERE TABLE_TYPE = 'BASE TABLE';")


for t in cursor_1.fetchall():
    print(t)
    
####listado de campos

cursor_1 = con_1.cursor()
columnas=cursor_1.execute("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.\
                          COLUMNS WHERE TABLE_NAME='CPP_DR2';")

for c in columnas.fetchall():
    print(c)


MAT=pd.read_sql("""
            SELECT 
                m.rut, 
                m.nombres,
                m.ap_paterno,
                m.sexo,
                m.nacionalidad,
                m.cod_plan,
                m.carrera_programa,
                LEFT(periodo_matricula, 4) AS ANHO_MAT,
                CODIGO_CARRERA=cod_carr_prog,
                LEFT(ingreso_plan, 4) AS ANHO_ING,
                CONCAT(m.rut, '-',LEFT(m.ingreso_plan, 4)) AS ID,
                CONCAT(m.rut, '-', LEFT(m.ingreso_plan, 4), '-', m.cod_plan) AS RUT_ANHO_PLAN,
                CONCAT(LEFT(ingreso_plan, 4), '-',m.cod_plan) AS ANHO_PLAN,
                CONCAT(c.SIES, '-', m.rut) AS SIES_RUT,
                CONCAT(LEFT(m.ingreso_plan, 4),'-' ,c.SIES, '-', m.rut) AS ANHO_SIES_RUT,
                m.via_ingreso,
                m.cod_via,
                m.region,
                m.fecha_nac,
                d.GRUPO_DEPENDENCIA,
                d.INGRESO_PERCAPITA_GRUPO_FA,
                d.PUNTAJE_PONDERADO,
                d.MATEMATICA,
                d.COMP_LECT,
                d.PTJE_NEM,
                d.PTJE_RANKING,
                c.SIES,
                o.Tipo_Carrera,
                o.Jornada,
                o.[Cine-F_13_Área],
                o.Duración_Total,
                o.Nivel_Carrera,
                g.GRATUIDAD,
                f.TIPO AS CAE,
                h.TIPO AS FSCU,
                cc.COD_FAC,
                cc.FACULTAD,
                cc.COD_DEPTO,
                cc.Columna2 AS depto,
                mu.NAC,
                COUNT(m.rut) AS Total,        
                d.INGRESO_PERCAPITA_GRUPO_FA,
                d.PUNTAJE_PONDERADO,
                d.MATEMATICA,
                d.COMP_LECT,
                d.PTJE_NEM,
                d.PTJE_RANKING
            FROM MATRICULA_V2_082025_PARA_TODO m
            LEFT JOIN DEMRE_E_2014_2025 d 
            ON CONCAT(m.rut, '-',LEFT(m.ingreso_plan, 4))=d.ID_ANHO
            LEFT JOIN CPP_DR2 c
            ON CONCAT(LEFT(periodo_matricula,4), '-',m.cod_plan)=c.ANHO_PLAN
            LEFT JOIN OA_SIES_2010_2025_USACH o
            ON CONCAT(c.ANHO, '_', c.SIES)=o.llave
            LEFT JOIN tb_gratuidad g
            ON CONCAT(m.rut, '-',LEFT(m.ingreso_plan, 4))=CONCAT(g.Rut,'-',g.AÑO)
            LEFT JOIN cae f
            ON CONCAT(m.rut, '-', LEFT(m.ingreso_plan, 4), '-', m.cod_plan)=CONCAT(f.RUN, '-',f.AÑO_ING,'-', f.CODIGO_PLAN)
            LEFT JOIN fscu h
            ON CONCAT(m.rut, '-', LEFT(m.ingreso_plan, 4), '-', m.cod_plan)=CONCAT(h.RUN, '-',h.AÑO_ING,'-', h.CODIGO_PLAN)
            LEFT JOIN centro_costo cc
            ON cod_carr_prog = [COD CARRERA]
            LEFT JOIN TABLA_MU mu
            ON CONCAT(LEFT(m.ingreso_plan, 4),'-' ,c.SIES, '-', m.rut) = CONCAT(mu.ANHO_MU, '-', mu.COD_SIES,'-', mu.N_DOC)
            GROUP BY
                m.rut,
                m.nombres,
                m.ap_paterno,
                m.sexo,
                m.nacionalidad,
                m.cod_plan,
                m.carrera_programa,
                LEFT(periodo_matricula, 4),
                CONCAT(m.rut, LEFT(m.ingreso_plan, 4)),
                CONCAT(m.rut, '-', LEFT(m.ingreso_plan, 4), '-', m.cod_plan),
                m.cod_carr_prog,
                CONCAT(LEFT(ingreso_plan, 4), '-',m.cod_plan),
                CONCAT(ANHO, '_', SIES),
                CONCAT(c.SIES, '-', m.rut),
                CONCAT(LEFT(m.ingreso_plan, 4),'-',c.SIES, '-', m.rut),
                m.ingreso_plan,
                m.via_ingreso,
                m.region,
                m.fecha_nac,
                d.GRUPO_DEPENDENCIA,
                d.INGRESO_PERCAPITA_GRUPO_FA,
                d.PUNTAJE_PONDERADO,
                d.MATEMATICA,
                d.COMP_LECT,
                d.PTJE_NEM,
                d.PTJE_RANKING,
                c.SIES,
                o.Tipo_Carrera,
                o.Jornada,
                o.[Cine-F_13_Área],
                o.Duración_Total,
                o.Nivel_Carrera,
                g.GRATUIDAD,
                f.TIPO,
                h.TIPO,
                cc.COD_FAC,
                cc.FACULTAD,
                cc.COD_DEPTO,
                cc.Columna2,
                m.cod_via,
                mu.NAC;""", con_1)


def buscar_rut(MAT):
    rut_buscado = int(input("Ingresa rut: "))
    if rut_buscado in MAT['rut'].values:
        print(MAT.loc[MAT['rut'] == rut_buscado, [
            'rut', 
            'ANHO_ING', 
            'ANHO_MAT', 
            'fecha_nac', 
            'CODIGO_CARRERA', 
            'cod_plan', 
            'PTJE_NEM',
            'GRUPO_DEPENDENCIA',
            'via_ingreso',
            'COH',
            'COH_CIDI'
        ]])
    else:
        print("no encontrado")

# Luego llama:
buscar_rut(MAT)


19828443

###NIVEL GLOBAL
MAT['NIVEL_GLOBAL']=np.where(MAT['CODIGO_CARRERA']=="UNICIT", "UNICIT",
    np.where(MAT['CODIGO_CARRERA']=="MIDA", "MAGISTER",
    np.where(MAT['CODIGO_CARRERA'].str[0:3]=="MAG","MAGISTER", 
    np.where(MAT['CODIGO_CARRERA'].str[0:3]=="DOC","DOCTORADO",
    np.where(MAT['CODIGO_CARRERA'].str[0:3]=="DIP","DIPLOMADO",
    np.where(MAT['CODIGO_CARRERA'].str[0:3]=="POS","POSTITUTLO","PREGRADO"))))))


MAT['fecha_nac']=pd.to_datetime(MAT['fecha_nac'])

MAT['fecha_nac']=pd.to_datetime(
    np.where(MAT['fecha_nac'] > pd.to_datetime('2025-01-01'), 
         MAT['fecha_nac'] - pd.DateOffset(years=100), 
    np.where(MAT['fecha_nac'] < pd.to_datetime('1910-01-01'), 
         MAT['fecha_nac'] + pd.DateOffset(years=100),MAT['fecha_nac'])))

MAT.info()
MAT=MAT.fillna(999)

MAT['ANHO_ING']=MAT['ANHO_ING'].astype(int)
#MAT['ANHO_ING']=MAT['ANHO_ING'].astype(str)
MAT['ANHO_MAT']=MAT['ANHO_MAT'].astype(int)

### edad
MAT['edad']=(((pd.to_datetime(date.today())-MAT['fecha_nac']).dt.days)/365).round(2)

#MAT[(MAT['rut']==19828443)]\
 #   .groupby(['rut', 'nombres', 'ap_paterno','via_ingreso','CODIGO_CARRERA'])

VIA_ING_ANIO=[81,63,26,29,	21,	66,	50,	15,	20,	49,	17,	60,	72,	43,	71,	10,	
              70,53,30,54,	55,	44,	16,	87,	95,	97,	85,	37,	68,	86,	19,	75,	
              64,62,76,27,	14,	77,	11,	74,	65,	12,	84,	73,	18,	83,	61, 99, 
              88,39]


VIA_ING_ANIO_CIDI=[10,11,12,13,	14,	15,	16,	17,	18,	19,	20,	21,	22,	
                   23,24,25,26,	27,	28, 29, 30, 31, 33,	34,	37,	38,	
                   39,40,41,43,	44,	49,	50,	52,	53,	54,	55, 57, 58,
                   59,60,61,62,	63,	64,	65,	66,	68,	70,	71,	72,	73,	
                   74,75,76,77,	78,	80,	79,	81,	82,	83,	84,	85,	86,	
                   87,88,89,91,	92,	95,	97,	99]



###Definición cohorte
MAT['COH']=np.where((np.isin(MAT['cod_via'], VIA_ING_ANIO).astype(int)==1) & 
         (MAT['ANHO_MAT']==MAT['ANHO_ING']),1,0)

MAT['COH_CIDI']=np.where((np.isin(MAT['cod_via'], VIA_ING_ANIO_CIDI).astype(int)==1) & 
         (MAT['ANHO_MAT']==MAT['ANHO_ING']),1,0)


MAT['id-anonimo']=MAT['rut']*25+MAT['ANHO_MAT']

####Definicion primer anio amplio
MAT['primer_anio']=np.where((MAT['ANHO_MAT']==MAT['ANHO_ING']),1,0)

###Informado SIES

informado_sies_2=pd.read_sql("""SELECT
            SIES_RUT,
            ANHO_SIES_RUT
            FROM TABLA_MU
            WHERE VIG=1 AND UNICIT='NO UNICIT'""",con_1)
            
MAT['INFORMADO_SIES']=MAT['ANHO_SIES_RUT'].isin(informado_sies_2['ANHO_SIES_RUT']).astype(int)


#rut_buscado=int(input("Ingresa rut:"))


###busqueda rut
#if rut_buscado in MAT['rut'].values:
 #   print(MAT.loc[MAT['rut']==rut_buscado, 
  #                            ['rut', 
   #                            'ANHO_ING',
    #                           'ANHO_MAT',
     #                          'fecha_nac',
      #                         'CODIGO_CARRERA',
       #                        'cod_plan',
        #                       'SIES']])
#else: print("no encontrado")


def buscar_rut(MAT):
    rut_buscado = int(input("Ingresa rut: "))
    if rut_buscado in MAT['rut'].values:
        print(MAT.loc[MAT['rut'] == rut_buscado, [
            'rut', 
            'ANHO_ING', 
            'ANHO_MAT', 
            'fecha_nac', 
            'CODIGO_CARRERA', 
            'cod_plan', 
            'PTJE_NEM',
            'GRUPO_DEPENDENCIA',
            'via_ingreso',
            'COH',
            'COH_CIDI'
        ]])
    else:
        print("no encontrado")

# Luego llama:
buscar_rut(MAT)


19828443
#COHORTES.loc[COHORTES['COH']==1, ['ANHO_ING',
#                                  'CODIGO_CARRERA_x', 
 #                                 'RET_1']]
 

#####ret
# COHORTES[COHORTES['CODIGO_CARRERA_x'].isin(["PEDEDFIS", 
#                         "PEDQUIMBIO", 
#                         "PEDBIOQUIM",
#                         "PEDINGLES"]) & (COHORTES['ANHO_ING']>2014) &(COHORTES['COH']==1)]\
#     .groupby(['CODIGO_CARRERA_x',
#                  'sexo',
#                  'RET_1',
#                  'RET_2',
#                  'RET_3',
#                  'ANHO_ING',
#                  'SIES',
#                  'NIVEL_GLOBAL'])['rut'].size().to_clipboard()



# COHORTES[
#     (COHORTES['NIVEL_GLOBAL']=="PREGRADO") &
#     (COHORTES['Tipo_Carrera']=="Plan Regular") &
#          (COHORTES['ANHO_ING']>2021)]\
# .groupby(['CODIGO_CARRERA_x', 
#           'INFORMADO_SIES',
#           'Tipo_Carrera',
#           'Duración_Total',
#           'Nivel_Carrera',
#           'RET_1',
#           'RET_2',
#           'ANHO_ING'])['rut'].size()


MAT[(MAT['SIES']==999) & 
    (MAT['primer_anio']==1) & (MAT['NIVEL_GLOBAL']=="PREGRADO")]\
    .groupby(['INFORMADO_SIES','ANHO_ING']).size().unstack()
    


MAT[(MAT['ANHO_MAT']==2024) &
    (MAT['NIVEL_GLOBAL']=="PREGRADO")]\
    .groupby(['rut','SIES', 
              'via_ingreso','NIVEL_GLOBAL',
              'INFORMADO_SIES','Tipo_Carrera','ANHO_MAT'])\
        .size().to_clipboard()
        

###Número de matriculas por rut unico
MAT[(MAT['ANHO_MAT']>2020) & 
    (MAT['NIVEL_GLOBAL']=="PREGRADO")]\
    .groupby(['ANHO_MAT',
              'COD_DEPTO',
              'depto',
              'COD_FAC',
              'FACULTAD'])['rut']\
    .nunique()
    
(
 MAT[(MAT['ANHO_MAT']>2020)]
    .groupby(['ANHO_MAT', 
              'FACULTAD',
              'NIVEL_GLOBAL'])['rut']\
    .nunique()
    .unstack()
    .to_clipboard()
    )
    
(    
MAT[(MAT['ANHO_MAT']>2020) & 
    (MAT['NIVEL_GLOBAL']=="PREGRADO") &
    (MAT['CODIGO_CARRERA']=="BACHI")]
    .groupby(['ANHO_MAT'])['rut']
    .nunique()
    )

(
MAT.groupby(['cod_plan',
             'SIES'])['rut']
.nunique()
.to_clipboard()
)

(
MAT[MAT['CODIGO_CARRERA']=="MAGCM"]
.groupby(['ANHO_ING',
          'sexo',
          'CODIGO_CARRERA',
          'cod_plan',
          'COH_CIDI',
          'COH',
          'SIES',
          'ANHO_MAT'])['rut']
.nunique()
.reset_index(name='Total')
.to_clipboard()
)

(
MAT[(MAT['NIVEL_GLOBAL']=="MAGISTER") | 
    (MAT['NIVEL_GLOBAL']=="DOCTORADO")]
.groupby([ 'cod_plan',
          'CODIGO_CARRERA',
          'NIVEL_GLOBAL',
          'FACULTAD'])['rut']
.nunique()
)





rut = MAT.loc[MAT['CODIGO_CARRERA'] == "MAGCM", 'rut'].drop_duplicates().tolist()


rut_2 = []
for i in MAT['rut']:
    if i in rut:
        print(i)
        rut_2.append(i)

pd.DataFrame(rut_2).drop_duplicates()

(
MAT[MAT['rut'].isin(rut)][['rut', 
                           'CODIGO_CARRERA', 
                           'sexo',
                           'NIVEL_GLOBAL',
                           'ANHO_ING',
                           'ANHO_MAT',
                           'COH',
                           'COH_CIDI']]
.drop_duplicates()
.to_clipboard()
)

(
MAT[MAT['ANHO_MAT']==2024]
.assign(id = MAT['ANHO_MAT']
        .astype(str) + '-' + MAT['cod_plan']
        .astype(str))
.groupby(['id','cod_plan','ANHO_MAT','NIVEL_GLOBAL'])['rut']
.nunique()
.reset_index(name= "n_distinct(RUT)")
.to_clipboard()
)

########times ranking
(
MAT[MAT['ANHO_ING']==2024]
.assign(id = MAT['ANHO_ING']
        .astype(str) + '-' + MAT['cod_plan']
        .astype(str))
.groupby(['NIVEL_GLOBAL','sexo','ANHO_ING', 'Tipo_Carrera'])['rut']
.nunique()
.reset_index(name= "n_distinct(RUT)")
.to_clipboard()
)

(
MAT[(MAT['ANHO_ING']==2024) & 
    (MAT['NIVEL_GLOBAL']!="DIPLOMADO") &
    (MAT['NIVEL_GLOBAL']!="POSTITUTLO")]
.assign(id = MAT['ANHO_ING']
        .astype(str) + '-' + MAT['cod_plan']
        .astype(str))
.groupby(['NIVEL_GLOBAL',
          'sexo','ANHO_ING', 
          'Tipo_Carrera',
          'cod_plan'])['rut']
.nunique()
.reset_index(name= "n_distinct(RUT)")
#.to_clipboard()
)
# %%
