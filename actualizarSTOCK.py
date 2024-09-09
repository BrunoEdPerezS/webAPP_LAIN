import pandas as pd
import json

def procesar_archivo_excel(archivo_excel):
    # Cargar el DataFrame desde el archivo Excel
    df = archivo_excel

    # Nombres de las columnas que deseas extraer
    nombre_columna   = 'descrip_producto'  
    codigo_columna   = 'codigo_producto'
    cantidad_columna = 'cant_total'

    # Verificar si las columnas existen en el DataFrame
    if nombre_columna not in df.columns:
        raise ValueError(f"La columna '{nombre_columna}' no existe en el DataFrame.")
    if codigo_columna not in df.columns:
        raise ValueError(f"La columna '{codigo_columna}' no existe en el DataFrame.")
    if cantidad_columna not in df.columns:
        raise ValueError(f"La columna '{cantidad_columna}' no existe en el DataFrame.")
    
    # Extraer las columnas deseadas y convertirlas en listas
    columna_descrip = df[nombre_columna].tolist()
    columna_codigo = df[codigo_columna].tolist()
    columna_cantidadSTOCK = df[cantidad_columna].tolist()

    # Transformar caracteres '' a " en ambas listas
    columna_descrip = [elemento.replace("''", '"') for elemento in columna_descrip]

    # Nombre del archivo Python
    archivo_py = 'lista_columna.py'

    # Convertir las listas a cadenas JSON seguras
    descrip_json = json.dumps(columna_descrip, ensure_ascii=False)
    codigo_json = json.dumps(columna_codigo, ensure_ascii=False)
    cantidadSTOCK_json = json.dumps(columna_cantidadSTOCK, ensure_ascii=False)

    # Guardar las listas en el archivo .py con codificación UTF-8
    with open(archivo_py, 'w', encoding='utf-8') as f:
        f.write(f"STOCK = {descrip_json}\n")
        f.write(f"CODIGO = {codigo_json}\n")
        f.write(f"cantidadSTOCK = {cantidadSTOCK_json}\n")

    # Convertir todos los elementos a mayúsculas para ambas listas (opcional)
    lista_mayusculas_descrip = [item.upper() for item in columna_descrip]
    #lista_mayusculas_codigo = [item.upper() for item in columna_codigo]

    return lista_mayusculas_descrip #lista_mayusculas_codigo
