# %%
import pyodbc
import pandas as pd
import numpy as np
from datetime import date

from MAT import MAT   # Importa la variable directamente

19828443


####Tabla cohortes
TABLA_COH=MAT.loc[MAT['COH'] == 1, ['rut',
                                    'RUT_ANHO_PLAN','ANHO_ING',  
                                    'Tipo_Carrera',
                                    'INFORMADO_SIES',
                                    'Duración_Total',
                                    'Nivel_Carrera',
                                    'CODIGO_CARRERA', 
                                    'NIVEL_GLOBAL',
                                    'cod_plan']]


COHORTES=TABLA_COH.merge(MAT[['COH',
                              'rut','sexo',
                              'RUT_ANHO_PLAN',
                              'ANHO_MAT',
                              'CODIGO_CARRERA', 
                              'cod_plan', 'SIES']], 
                 on='rut', how='left')

COHORTES.groupby(['CODIGO_CARRERA_x', 
           'ANHO_ING'])['rut'].nunique()

#####RETENCIONES
####RET_1
COHORTES['RET_1']=\
np.where((COHORTES['ANHO_ING']!=COHORTES['ANHO_MAT']) &
         (COHORTES['ANHO_MAT']-COHORTES['ANHO_ING']==1) &
         (COHORTES['cod_plan_x']==COHORTES['cod_plan_y']),1,
np.where((COHORTES['ANHO_ING']!=COHORTES['ANHO_MAT']) &
         (COHORTES['ANHO_MAT']-COHORTES['ANHO_ING']==1) &
         (COHORTES['CODIGO_CARRERA_x']==COHORTES['CODIGO_CARRERA_y']),1,0))


COHORTES['RET_2']=\
np.where((COHORTES['ANHO_ING']!=COHORTES['ANHO_MAT']) &
         (COHORTES['ANHO_MAT']-COHORTES['ANHO_ING']==2) &
         (COHORTES['cod_plan_x']==COHORTES['cod_plan_y']),1,
np.where((COHORTES['ANHO_ING']!=COHORTES['ANHO_MAT']) &
         (COHORTES['ANHO_MAT']-COHORTES['ANHO_ING']==2) &
         (COHORTES['CODIGO_CARRERA_x']==COHORTES['CODIGO_CARRERA_y']),1,0))

COHORTES['RET_3']=\
np.where((COHORTES['ANHO_ING']!=COHORTES['ANHO_MAT']) &
         (COHORTES['ANHO_MAT']-COHORTES['ANHO_ING']==3) &
         (COHORTES['cod_plan_x']==COHORTES['cod_plan_y']),1,
np.where((COHORTES['ANHO_ING']!=COHORTES['ANHO_MAT']) &
         (COHORTES['ANHO_MAT']-COHORTES['ANHO_ING']==3) &
         (COHORTES['CODIGO_CARRERA_x']==COHORTES['CODIGO_CARRERA_y']),1,0))

(
COHORTES[COHORTES['CODIGO_CARRERA_x']=="ARQ"]
.groupby(['ANHO_ING',
          'CODIGO_CARRERA_x',
          'Duración_Total',
          'COH',
          'RET_1',
          'RET_2',
          'RET_3'])['rut']
.nunique()
#.agg(tot_coh = ('rut', 'nunique'),
#     ret_1_num =('RET_1', 'sum')
.reset_index(name = 'tot')
#.to_clipboard()
)

resultado =(
COHORTES[COHORTES['CODIGO_CARRERA_x']=="ARQ"]
.groupby(['ANHO_ING',
          'CODIGO_CARRERA_x'])
.agg(tot = ('rut', 'nunique'),
     ret_1_agg = ('RET_1', 'sum'),
     )
.reset_index()

)

resultado['tasa_ret_1']=resultado['ret_1_agg']/resultado['tot']


###cohortes
coh=(
COHORTES
.groupby(['ANHO_ING', 'CODIGO_CARRERA_x'])['rut']
.nunique()
.reset_index(name='coh')
)
####ret_1
ret_1=(
COHORTES[COHORTES['RET_1']==1]
.groupby(['ANHO_ING', 'CODIGO_CARRERA_x'])['rut']
.nunique()
.reset_index(name='ret_1_n')
)
####ret_2
ret_2=(
COHORTES[COHORTES['RET_2']==1]
.groupby(['ANHO_ING', 'CODIGO_CARRERA_x'])['rut']
.nunique()
.reset_index(name='ret_2_n')
)
####ret_3
ret_3=(
COHORTES[COHORTES['RET_3']==1]
.groupby(['ANHO_ING', 'CODIGO_CARRERA_x'])['rut']
.nunique()
.reset_index(name='ret_3_n')
)



tabla_ret=(coh
.merge(ret_1, on=['ANHO_ING', 'CODIGO_CARRERA_x'], how = 'left')
.merge(ret_2, on=['ANHO_ING', 'CODIGO_CARRERA_x'], how = 'left')
.merge(ret_3, on=['ANHO_ING', 'CODIGO_CARRERA_x'], how = 'left')
)

tabla_ret['ret_1']=tabla_ret['ret_1_n']/tabla_ret['coh']
tabla_ret['ret_2']=tabla_ret['ret_2_n']/tabla_ret['coh']
tabla_ret['ret_3']=tabla_ret['ret_3_n']/tabla_ret['coh']

###NIVEL GLOBAL
tabla_ret['NIVEL_GLOBAL']=np.where(tabla_ret['CODIGO_CARRERA_x']=="UNICIT", "UNICIT",
    np.where(tabla_ret['CODIGO_CARRERA_x']=="MIDA", "MAGISTER",
    np.where(tabla_ret['CODIGO_CARRERA_x'].str[0:3]=="MAG","MAGISTER", 
    np.where(tabla_ret['CODIGO_CARRERA_x'].str[0:3]=="DOC","DOCTORADO",
    np.where(tabla_ret['CODIGO_CARRERA_x'].str[0:3]=="DIP","DIPLOMADO",
    np.where(tabla_ret['CODIGO_CARRERA_x'].str[0:3]=="POS","POSTITUTLO","PREGRADO"))))))


tabla_ret
(
set_with_dataframe(spreadsheet.
        add_worksheet(title="TABLA_MU_3", 
                      rows=5000, cols= 10), 
                      tabla_ret[tabla_ret['NIVEL_GLOBAL']=="PREGRADO"])

)

tabla_ret.to_csv("tabla_ret.csv", index=False)

# %%
