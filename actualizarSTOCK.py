import pandas as pd
import json

def procesar_archivo_excel(archivo_excel):

    # Cargar el DataFrame desde el archivo Excel
    df = archivo_excel

    # Nombre de la columna que deseas extraer
    nombre_columna = 'descrip_producto'  # Cambia 'descrip_producto' al nombre de la columna que deseas extraer

    # Verificar si la columna existe en el DataFrame
    if nombre_columna not in df.columns:
        raise ValueError(f"La columna '{nombre_columna}' no existe en el DataFrame.")

    # Extraer la columna deseada y convertirla en una lista
    columna = df[nombre_columna].tolist()

    #Transformar caracteres ''
    columna = [elemento.replace("''", '"') for elemento in columna]

    # Nombre del archivo Python
    archivo_py = 'lista_columna.py'

    # Convertir la lista a una cadena JSON segura
    columna_json = json.dumps(columna, ensure_ascii=False)

    # Guardar la lista en el archivo .py con codificación UTF-8
    with open(archivo_py, 'w', encoding='utf-8') as f:
        f.write(f"STOCK = {columna_json}\n")

    # Convertir todos los elementos a mayúsculas
    lista_mayusculas = [item.upper() for item in columna]
    

    return lista_mayusculas
