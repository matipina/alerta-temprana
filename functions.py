def get_tries(df, ids, sem_keys):    
    # Por cada semestre que no sea el primero, revisamos los ids del semestre anterior,
    # y si encontramos uno repetido en el semestre actual, sumamos 1 a su columna tries
    df['tries'] = int(0)
    for i in range(1, len(ids)):
        sem = sem_keys[i]
        prev_sem = sem_keys[i-1]
        # Buscar ids repetidos
        for id in ids[i]:
            if id in ids[i-1]:
                # Asignar a tries del estudiante id en el semestre i,
                # el valor de tries del estudiante id en el semestre i-1, +1
                df.loc[sem, 'tries'][df.loc[sem, 'id'] == id] = (int(df.loc[prev_sem, 'tries'][df.loc[prev_sem, 'id'] == id]) + 1)
    return df

