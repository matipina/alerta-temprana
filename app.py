import streamlit as st
from predict_page import show_predict_page
import sklearn

def app_begin():
    st.title("Sistema de Alerta Temprana")
    st.write('El objetivo de este sistema es predecir qué estudiantes se encuentran en\
            situación de riesgo académico. Para esto, solo debes seleccionar un curso,\
            cargar las notas disponibles de ese curso, y seleccionar las evaluaciones que\
            serán usadas para generar las predicciones.')
    return

st.set_page_config(
     page_title="Sistema de Alerta Temprana",
     page_icon="🆘",
 )


app_begin()

start = st.button('Empezar')


if 'start_button' not in st.session_state:
    st.session_state['start_button'] = start

if start:
    st.session_state['start_button'] = start

if st.session_state['start_button']:
    show_predict_page()
