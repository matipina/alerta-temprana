import streamlit as st
import pickle
import numpy as np
import pandas as pd
import sklearn

label = 'Aprobado'
course_variables = {
    'IIC1103': ['tries', 'T1', 'I1', 'T2', 'I2'],
    'IIC2233': [],
    'ICH1104': ['T1', 'I1', 'T2', 'I2', 'T3']
}

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
        'IIC2233: Programación Avanzada',
        'ICH1104: Mecánica de fluidos',
        'ICS1113: Optimización',    
    )

    course = st.selectbox("Selecciona un curso:", courses)

    if course != 'Selecciona':

        st.write(f'#### {course}')
        code = course[:7]
        model_folder = f'models/{code}'

        file = st.file_uploader("Carga un archivo (.csv o .xlsx) con las notas del semestre.")
        if file:
            filename = file.name
            if filename.endswith('.csv'):
                df = pd.read_csv(file)
            elif filename.endswith('.xlsx') or filename.endswith('.xls'):
                df = pd.read_excel(file)
            else:
                st.warning('Tipo de archivo no válido. Inténtalo de nuevo.')

            st.write(
                    f'''
                    #### Selecciona las columnas a utilizar para las predicciones: 
                    ''')
            
            available_values = course_variables[code]
            selected_values = {}

            value_options = []
            for i in range(1, len(available_values)+1):
                value_options.append(available_values[:i])

            new_list = st.select_slider(
                f'Columnas disponibles: {"   -   ".join(course_variables[code])}',
                options=value_options,
                format_func=' - '.join
                )
            
            '''
            # Creamos un checkbox para cada valor disponible
            for column in available_values:
                selected_values[column] = st.checkbox(column, key=column)
            
            # Creamos una lista con los valores seleccionados en las checkboxes
            new_list = [value for value, selected in selected_values.items() if selected]
            '''
            
            next = st.button('Siguiente')
            #num_selected = sum(selected_values.values())
            num_selected = len(new_list)

            if num_selected >= 1:
                if next:
                    selected_data = df.loc[:, new_list]
                    st.write(
                        '''
                        #### Predicciones:
                        '''
                    )

                    model_path = f'{model_folder}/model{num_selected-1}.sav'
                    model = pickle.load(open(model_path, 'rb'))

                    copy = selected_data.copy()
                    clean_data = copy.dropna(subset=new_list)
                    clean_data[label] = model.predict(clean_data)

                    # Agregar datos para identificar a los estudiantes
                    if any(i in df.columns for i in ('id', 'ID', 'Id')):
                        student_data = df.loc[:, df.columns.isin(('id', 'ID', 'Id'))]
                    else:
                        student_data = df.iloc[:, 0]
                    final_data = clean_data.merge(student_data, left_index=True, right_index=True)

                    cols = student_data.columns.tolist() + clean_data.columns.tolist()
                    final_data = final_data[cols]
                    
                    st.dataframe(final_data.style.apply(custom_style, axis=1))

                    st.download_button(
                                    "Descargar",
                                    final_data.to_csv().encode('utf-8'),
                                    f"predicciones_{'_'.join(new_list)}.csv",
                                    "text/csv",
                                    key='download-csv'
                                    )

                    
            else:
                st.warning('Debes seleccionar al menos un atributo.')
                next = False







