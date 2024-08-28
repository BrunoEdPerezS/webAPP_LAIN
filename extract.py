import pandas as pd

# Nombre del archivo Excel
archivo_excel = 'stockterreno.xlsx'

# Cargar el DataFrame desde el archivo Excel
df = pd.read_excel(archivo_excel, engine='openpyxl')

# Nombre de la columna que deseas extraer
nombre_columna = 'descrip_producto'  # Cambia 'columna1' al nombre de la columna que deseas extraer

# Verificar si la columna existe en el DataFrame
if nombre_columna not in df.columns:
    raise ValueError(f"La columna '{nombre_columna}' no existe en el DataFrame.")

# Extraer la columna deseada y convertirla en una lista
columna = df[nombre_columna].tolist()

# Nombre del archivo Python
archivo_py = 'lista_columna.py'

# Guardar la lista en el archivo .py
with open(archivo_py, 'w') as f:
    f.write(f"lista = {columna}\n")
    
print(f"La columna '{nombre_columna}' ha sido guardada en {archivo_py}.")
