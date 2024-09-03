from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response
import json
import lista_columna
import pandas as pd
import io
from io import BytesIO
import actualizarSTOCK

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para usar la sesión en Flask

# Lista de elementos de ejemplo
#items = ["ITEM1", "ITEM2", "ITEM3", "ITEM4", "ELEMENTO1", "ELEMENTO2"]

items = lista_columna.STOCK

#items = lista_columna.STOCK
current_selected_items = {}

##Manejo de strings para filtrado-------------------
def separar_cadena(texto):
    #Separara cadena por *
    subcadenas = texto.split('*')
    return subcadenas
def eliminar_espacios(texto):
    # Reemplazar todos los espacios con una cadena vacía
    texto_sin_espacios = texto.replace(' ', '')
    return texto_sin_espacios
def eliminar_cadenas_vacias_o_espacios(lista):
    # Filtrar la lista para eliminar las cadenas vacías y las cadenas que solo contienen espacios
    lista_filtrada = [cadena for cadena in lista if cadena.strip()]
    return lista_filtrada
def convertir_a_mayusculas(texto):
    # Convertir la cadena a mayúsculas
    texto_mayusculas = texto.upper()
    return texto_mayusculas

##Manejo de strings para busqueda
def buscar_keywords(keywords, biglist):
    resultados = []
    
    for keyword in keywords:
        coincidencias = [elemento for elemento in biglist if keyword in elemento]
        resultados.append(coincidencias)
    
    return resultados

##Encuentra coincidencias entre elementos de listas
def encontrar_coincidencias(lists):
    if not lists:
        return []
    
    # Inicializa el conjunto con los elementos de la primera sublista
    coincidencias = set(lists[0])
    
    # Itera sobre el resto de las sublistas y actualiza el conjunto
    for sublista in lists[1:]:
        coincidencias &= set(sublista)
    
    # Convertir el conjunto a lista y retornarlo
    return list(coincidencias)

def generate_excel_report(selected_items):
    df = pd.DataFrame(list(selected_items.items()), columns=['Item', 'Value'])
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Report')
    buffer.seek(0)
    return buffer



@app.route('/', methods=['GET', 'POST'])
def index():
    global items  # Asegura que items se pueda modificar dentro de la función
    filtered_items = items  # Iniciar con la lista completa de elementos
    filter_text = request.form.get('filter_text', '')

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'filter':  # Acción para el filtrado
            filter_text = request.form.get('filter_text', '').lower()
            if (filter_text == ""):
                 filtered_items = items
            else:
                print("Texto input:")
                print(filter_text)
                #Formatear a mayuscula
                filter_text = convertir_a_mayusculas(filter_text)
                print("Texto en mayusculas:")
                print(filter_text)     
                ##Eliminar espacios en la string
                nospaceSTRING = eliminar_espacios(filter_text)
                print("Texto sin espacios:")
                print(nospaceSTRING)           
                ##Separar string por *
                separadaSTRING = separar_cadena(nospaceSTRING)
                print("String separada:")
                print(separadaSTRING)
                ##Finalmente eliminar todas las strings vacias
                keywords = eliminar_cadenas_vacias_o_espacios(separadaSTRING)
                print("Lista de keywords")
                print(keywords)
                coincidencias = buscar_keywords(keywords,items)
                print("Coincidencias pilladas: ")
                print(coincidencias)
                print("Elementos comunes entre keywords: ")
                comunes = encontrar_coincidencias(coincidencias)
                print(comunes)
                filtered_items = comunes
                #filtered_items = [item for item in items if filter_text in item.lower()]
                #print("Items filtrados")
                #print(filtered_items)



        elif action == 'save':  # Acción para guardar selección
            selected_items_json = request.form.get('selected_items', '{}')
            try:
                new_selected_items = json.loads(selected_items_json)
                print("Selected actuales")
                print(new_selected_items)
                
                # Obtener el diccionario de elementos seleccionados de la sesión
                current_selected_items = session.get('selected_items', {})
                print("Selected globales")
                print(current_selected_items)
                
                # Actualizar el diccionario con nuevos elementos, solo si las claves no existen o el valor es distinto
                for key, value in new_selected_items.items():
                    print("Diccionario actualizado")
                    #if key not in current_selected_items or current_selected_items[key] != value:
                    current_selected_items[key] = value
                
                # Guardar el diccionario actualizado en la sesión
                session['selected_items'] = current_selected_items
            except json.JSONDecodeError:
                # Manejar el error en caso de que JSON no sea válido
                session['selected_items'] = session.get('selected_items', {})
                
            if not session['selected_items']:
                return redirect(url_for('show_selection', message='No hay elementos agregados'))
            return redirect(url_for('show_selection'))

    return render_template('index.html', items=filtered_items, filter_text=filter_text)

@app.route('/show_selection', methods=['GET', 'POST'])
def show_selection():
    if request.method == 'POST':
        action_type = request.form.get('action_type')
        selected_items_json = request.form.get('selected_items', '{}')
        
        if action_type == 'save_report':
            print("Guardao")
        elif action_type == 'delete_report':
            session.pop('selected_items', None)
            return redirect(url_for('show_selection', message='Reporte eliminado'))
        
        elif action_type == 'delete_item':
            item_to_delete = request.form.get('item_to_delete')
            if item_to_delete:
                current_selected_items = session.get('selected_items', {})
                if item_to_delete in current_selected_items:
                    del current_selected_items[item_to_delete]
                    session['selected_items'] = current_selected_items
                    return redirect(url_for('show_selection', message=f'Elemento "{item_to_delete}" eliminado'))
        
        try:
            new_selected_items = json.loads(selected_items_json)
            current_selected_items = session.get('selected_items', {})
            for key, value in new_selected_items.items():
                current_selected_items[key] = value
            session['selected_items'] = current_selected_items
            
        except json.JSONDecodeError:
            session['selected_items'] = session.get('selected_items', {})

        return redirect(url_for('show_selection'))

    message = request.args.get('message', '')
    return render_template('selected.html', selected_items=session.get('selected_items', {}), message=message)


@app.route('/edit_stock')
def edit_stock():
    # Implementa la lógica para editar el stock aquí
    return "Función de edición de stock en construcción."

@app.route('/handle_action', methods=['POST'])
def handle_action():
    action_type = request.form.get('action_type')
    if action_type == 'save_report':
        print("guardado")
        print(session.get('selected_items', {}))
        # Obtener los elementos seleccionados de la sesión
        selected_items = session.get('selected_items', {})
        # Generar el archivo Excel
        buffer = generate_excel_report(selected_items)
        # Crear la respuesta
        response = Response(buffer, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response.headers['Content-Disposition'] = 'attachment; filename=report.xlsx'
        return response
    elif action_type == 'delete_report':
        session.pop('selected_items', None)
        return redirect(url_for('show_selection', message='Reporte eliminado'))

    return redirect(url_for('show_selection'))

@app.route('/delete_item', methods=['POST'])
def delete_item():
    data = request.get_json()
    item = data.get('item')
    
    # Obtener el diccionario de elementos seleccionados de la sesión
    current_selected_items = session.get('selected_items', {})
    
    if item in current_selected_items:
        del current_selected_items[item]
        session['selected_items'] = current_selected_items
        return jsonify({'success': True}), 200
    
    return jsonify({'success': False, 'message': 'Elemento no encontrado'}), 404

@app.route('/upload_stock', methods=['POST'])
def upload_stock():
    if 'file' not in request.files:
        return redirect(url_for('index', message='No file part'))

    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('index', message='No selected file'))
    
    if file and (file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
        try:
            df = pd.read_excel(file)
            print("Archivo Excel cargado:")
            print(df)
            actualizarSTOCK.procesar_archivo_excel(df)
            # Aquí puedes procesar el DataFrame df como necesites
            # Por ejemplo, convertir los valores a mayúsculas, etc.
            # Actualiza tu lista de elementos si es necesario
        except Exception as e:
            print(f"Error al procesar el archivo: {e}")
            return redirect(url_for('index', message='Error al procesar el archivo'))
    
    return redirect(url_for('index', filter='true',message='Archivo cargado exitosamente'))

if __name__ == '__main__':
    app.run(debug=True)





