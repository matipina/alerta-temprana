import streamlit as st
import pickle
import numpy as np
import pandas as pd
import sklearn
import os

label = 'Predicción'
pass_label = 'Aprueba'
fail_label = 'Reprueba'

course_variables = {
    'IIC1103': ['T1', 'I1', 'T2', 'I2', 'T3'],
    'IIC2233': [],
    'ICH1104': ['T1', 'I1', 'T2', 'I2', 'T3']
}

def custom_style(row):
    color = st.get_option('theme.backgroundColor') # get color corresponding to current theme
    if row[label] == fail_label:
        color = st.get_option('theme.primaryColor')

    return ['background-color: %s' % color]*len(row.values)


def get_attempts(filename, df, code, id):
    '''
    1. Revisamos todos los archivos en {code}
    2. Cargamos los archivos que no son {df}
    3. Comparamos la columna {id} de {df} con los demás archivos, y contamos las repeticiones
    de cada elemento
    4. Retornamos {df} con columna {tries}
    '''

    data_path = os.path.join('data', code)

    id_col = df[id]
    other_ids = []

    for root, _, files in os.walk(data_path, topdown = False):
        for name in files:
            if name != filename:
                if name.endswith('.csv'):
                    new_df = pd.read_csv(os.path.join(root, name))
                    other_ids.append(new_df[id])

                elif name.endswith('.xlsx') or name.endswith('.xls'):
                    new_df = pd.read_excel(os.path.join(root, name))
                    other_ids.append(new_df[id])

    # almacenamos los otros ids en {other_ids}
    for id_cols in other_ids:
        pass

    return


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
        model_directory = f'models/{code}'

        file = st.file_uploader("Carga un archivo (.csv o .xlsx) con las notas del semestre.")
        if file:
            filename = file.name
            if filename.endswith('.csv'):
                df = pd.read_csv(file)
            elif filename.endswith('.xlsx') or filename.endswith('.xls'):
                df = pd.read_excel(file)
            else:
                st.warning('Tipo de archivo no válido. Inténtalo de nuevo.')

            # Arreglamos el formato de los nombres de las columnas,
            # eliminando espacios en blanco.
            df.columns = df.columns.str.strip().str.upper()

            id_col = st.selectbox(
                '''
                Selecciona una columna que identifique a los estudiantes (id).
                Esta columna debe tener valores únicos.
                ''',
                df.columns.to_list())
                
            if id_col:
                st.write(f'"*{id_col}*" seleccionada como columna de identificación.')
            
            # Obtenemos 'tries'
            # df_full = get_attempts(filename, df, code, id=id_col)



            st.write(
                    '''
                    #### Selecciona las columnas a utilizar para las predicciones: 
                    ''')
            
            available_values = course_variables[code]

            value_options = []
            for i in range(1, len(available_values)+1):
                value_options.append(available_values[:i])

            predictors = st.radio(
            "Selecciona las columnas a utilizar para las predicciones:",
            value_options,
            format_func=' - '.join
            )

            
            next_2 = st.button('Siguiente', key='model_preparation')
            num_selected = len(predictors)

            if num_selected >= 1:
                if next_2:
                    selected_data = df.loc[:, predictors]
                    st.write(
                        '''
                        #### Predicciones:
                        '''
                    )

                    model_path = f'{model_directory}/model{num_selected}.sav'
                    model = pickle.load(open(model_path, 'rb'))

                    copy = selected_data.copy()
                    clean_data = copy.dropna(subset=predictors)
                    predictions = model.predict(clean_data)
                    clean_data.loc[:, label] = predictions

                    # Agregar datos para identificar a los estudiantes
                    '''
                    if any(i in df.columns for i in ('id', 'ID', 'Id')):
                        student_data = df.loc[:, df.columns.isin(('id', 'ID', 'Id'))]
                    else:
                        student_data = df.iloc[:, 0]
                    '''
                    student_data = df[id_col]
                    final_data = clean_data.merge(student_data, left_index=True, right_index=True)

                    cols = [id_col] + clean_data.columns.tolist()
                    final_data = final_data[cols]
                    final_data[label] = [pass_label if i==1 else fail_label for i in final_data[label]]
                    
                    st.dataframe(final_data.style.apply(custom_style, axis=1))

                    st.download_button(
                                    "Descargar",
                                    final_data.to_csv().encode('utf-8'),
                                    f"predicciones_{'_'.join(predictors)}.csv",
                                    "text/csv",
                                    key='download-csv'
                                    )

                    
            else:
                st.warning('Debes seleccionar al menos un atributo.')
                next = False