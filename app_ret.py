#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  4 11:34:38 2025

@author: xenomorfo
"""

import streamlit as st
import pandas as pd
import numpy as np

# Título
st.title("Retencion USACH")

# Entrada de texto
nombre = st.text_input("¿Cuál es tu nombre?", "Invitado")
st.write(f"La retención disminuye a medida que aumenta el año de ingreso")

# Generar y mostrar un gráfico
st.subheader("Retencion 2007 - 2025")


import pandas as pd
import numpy as np



tabla_ret=pd.read_csv("tabla_ret.csv")

tabla_ret['NIVEL_GLOBAL']=np.where(tabla_ret['CODIGO_CARRERA_x']=="UNICIT", "UNICIT",
    np.where(tabla_ret['CODIGO_CARRERA_x']=="MIDA", "MAGISTER",
    np.where(tabla_ret['CODIGO_CARRERA_x'].str[0:3]=="MAG","MAGISTER", 
    np.where(tabla_ret['CODIGO_CARRERA_x'].str[0:3]=="DOC","DOCTORADO",
    np.where(tabla_ret['CODIGO_CARRERA_x'].str[0:3]=="DIP","DIPLOMADO",
    np.where(tabla_ret['CODIGO_CARRERA_x'].str[0:3]=="POS","POSTITUTLO","PREGRADO"))))))


tabla_ret=tabla_ret[tabla_ret['NIVEL_GLOBAL']!="DIPLOMADO"]

tabla_ret_agrupada=(tabla_ret.groupby(['ANHO_ING',])
.agg({'ret_1': 'mean', 
      'ret_2': 'mean', 
      'ret_3': 'mean',
      'ret_4': 'mean'})
.reset_index()
)

tabla_ret_agrupada_carr=(tabla_ret.groupby(['ANHO_ING',
                                            'CODIGO_CARRERA_x', 'NIVEL_GLOBAL'])
.agg({'ret_1': 'mean', 
      'ret_2': 'mean', 
      'ret_3': 'mean',
      'ret_4': 'mean'})
.reset_index()
)
#tabla_ret=tabla_ret[['ANHO_ING','ret_1', 
#                     'ret_2', 'ret_3']].replace(0, np.nan)


#st.line_chart(
 #   data=tabla_ret,
  #  x="ANHO_ING",
   # y=["ret_1", "ret_2", "ret_3"]
#)

#import plotly.express as px
import altair as alt

#px.line(tabla_ret, x='ANHO_ING', y=['ret_1', 
 #                                  'ret_2', 
  #                                 'ret_3']) 

#chart = alt.Chart(tabla_ret_agrupada).mark_line().encode(
 #   x="ANHO_ING:O",
  #  y=alt.Y("value:Q"),
   # color="variable:N"
#).transform_fold(
 ##  as_=["variable", "value"]
#)


chart = (
    alt.Chart(tabla_ret_agrupada)
    .transform_fold(
        ["ret_1", 
         "ret_2", 
         "ret_3", "ret_4"],
        as_=["variable", "value"]
    )
    .mark_line(size = 2.5)
    .encode(
        x="ANHO_ING:O",
        y=alt.Y("value:Q"),
        color="variable:N"
    )
)



st.altair_chart(chart, use_container_width=True)


tabla_ret_largo=tabla_ret_agrupada.melt(id_vars=['ANHO_ING'], 
             value_vars=['ret_1', 'ret_2', 'ret_3', 'ret_4'])

tabla_ret_largo_carr=tabla_ret_agrupada_carr.melt(id_vars=['ANHO_ING', 
                                      'CODIGO_CARRERA_x', 'NIVEL_GLOBAL'], 
             value_vars=['ret_1', 
                         'ret_2', 
                         'ret_3', 
                         'ret_4'])

#ret_sel = st.radio("Selecciona la retención a visualizar:", 
 #        ('ret_1', 'ret_2', 'ret_3', "todo"), index=0)

ret_sel_carr = st.selectbox("Selecciona la carrera a visualizar:", 
         tabla_ret['CODIGO_CARRERA_x'].unique())



#st.line_chart(tabla_ret)



#tabla_ret_largo_filtrado=tabla_ret_largo[tabla_ret_largo['variable']==ret_sel]

tabla_ret_largo_filtrado_carr=tabla_ret_largo_carr[(tabla_ret_largo_carr['CODIGO_CARRERA_x']==ret_sel_carr)]

chart_fil = (alt.Chart(tabla_ret_largo_filtrado_carr)
             .mark_line(size = 4)
             .encode(
    x="ANHO_ING:O",
    y=alt.Y("value:Q", title = "Retención"),
    color="variable:N"
))

st.altair_chart(chart_fil, use_container_width=True)

# Contador de clics
#if "contador" not in st.session_state:
#    st.session_state.contador = 0

#if st.button("¡Haz clic aquí!"):
#    st.session_state.contador += 1

#st.write(f"Has hecho clic **{st.session_state.contador}** veces.")

# Despedida
#st.markdown("---")
#st.write("Gracias por probar esta demo de Streamlit.")
