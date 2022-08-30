import streamlit as st
import pickle
import numpy as np
import pandas as pd
import sklearn

label = 'Aprobado'

def custom_style(row):
    color = st.get_option('theme.backgroundColor') # get color corresponding to current theme
    if row[label] == False:
        color = st.get_option('theme.primaryColor')

    return ['background-color: %s' % color]*len(row.values)

def show_predict_page():
    st.write(
        '''
        ### Sistema de Predicción de Rendimiento Académico
        ''')

    courses = (
        'Selecciona',
        'IIC1103: Introducción a la Programación',
        'IIC2233: Programación Avanzada'
    )

    course = st.selectbox("Selecciona un curso:", courses)

    if course != 'Selecciona':

        st.write(f'#### {course}')
        code = course[:7]
        file = st.file_uploader("Carga un archivo (.csv) con las notas del semestre.")
        
        if file:
            df = pd.read_csv(file)
            st.write(
                    '''
                    #### Selecciona las columnas a utilizar:
                    *nota: debe ser un subset de ['tries', 'T1', 'I1', 'I2', 'T2']* 
                    ''')
            
            available_values = ['tries', 'T1', 'I1', 'I2', 'T2']
            selected_values = {}
            for column in available_values:
                selected_values[column] = st.checkbox(column, key=column)

            new_list = [value for value, selected in selected_values.items() if selected]
            next = st.button('Siguiente')
            num_selected = sum(selected_values.values())

            if num_selected >= 1:
                if next:
                    selected_data = df.loc[:, new_list]
                    st.write(
                        '''
                        #### Predicciones:
                        '''
                    )
                    model_folder = f'models/{code}'

                    model_path = f'{model_folder}/model{num_selected-1}.sav'
                    model = pickle.load(open(model_path, 'rb'))

                    copy = selected_data.copy()
                    copy[label] = model.predict(copy)
                    st.dataframe(copy.style.apply(custom_style, axis=1))
            else:
                st.warning('Debes seleccionar al menos un atributo.')
                next = False







