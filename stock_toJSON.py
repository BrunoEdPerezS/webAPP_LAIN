import pandas as pd
import json
import os

def procesar_archivo_excel(archivo_excel):
    # Cargar el DataFrame desde el archivo Excel
    df = archivo_excel

    # Nombres de las columnas que deseas extraer
    nombre_columna = 'descrip_producto'  
    codigo_columna = 'codigo_producto'
    cantidad_columna = 'cant_total'

    # Verificar si las columnas existen en el DataFrame
    if nombre_columna not in df.columns:
        raise ValueError(f"La columna '{nombre_columna}' no existe en el DataFrame.")
    if codigo_columna not in df.columns:
        raise ValueError(f"La columna '{codigo_columna}' no existe en el DataFrame.")
    if cantidad_columna not in df.columns:
        raise ValueError(f"La columna '{cantidad_columna}' no existe en el DataFrame.")
    
    # Extraer las columnas deseadas y convertirlas en listas
    columna_descrip = df[nombre_columna].str.upper().tolist()
    columna_codigo = df[codigo_columna].tolist()
    columna_cantidadSTOCK = df[cantidad_columna].tolist()

    # Transformar caracteres '' a " en ambas listas
    columna_descrip = [elemento.replace("''", '"') for elemento in columna_descrip]

    # Convertir las listas a un diccionario
    datos_json = {
        'STOCK': columna_descrip,
        'CODIGO': columna_codigo,
        'cantidadSTOCK': columna_cantidadSTOCK
    }

    # Obtener la ruta al directorio actual
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    # Construir la ruta al archivo en la carpeta static
    ruta_json = os.path.join(directorio_actual, 'static', 'lista_columna.json')

    # Guardar los datos en un archivo JSON con codificación UTF-8
    with open(ruta_json, 'w', encoding='utf-8') as f:
        json.dump(datos_json, f, ensure_ascii=False, indent=4)

    # Convertir todos los elementos a mayúsculas para la lista de descripciones
    lista_mayusculas_descrip = [item.upper() for item in columna_descrip]

    print("JSON guardado en:", ruta_json)
    return lista_mayusculas_descrip  # O puedes devolver también el código y cantidad si lo necesitas

