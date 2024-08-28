import re
import json
from collections import Counter
from flask import Flask, render_template, request, redirect, url_for
from lista_columna import STOCK
import pandas as pd
from flask import send_file
import json
from io import BytesIO


app = Flask(__name__)

# Lista de elementos
items = STOCK
items = [item.upper() for item in items]

# Lista para almacenar los elementos seleccionados
selected_items = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global selected_items
    filter_text = request.form.get('filter_text', '')

    if filter_text == "":
        filtered_items = items
    else:
        filtered_items = filter_items(filter_text)

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            selected_item = request.form.get('selected_item')
            if selected_item and selected_item not in selected_items:
                selected_items.append(selected_item)
        elif action == 'filter':
            # No extra processing required for filter action
            pass

    return render_template('index.html', items=filtered_items, filter_text=filter_text, selected_items=selected_items)

@app.route('/selected')
def show_selected():
    return render_template('selected.html', selected_items=selected_items)

def unspace_format(search_text):
    keywords = search_text.replace(" ", "")
    keywords = search_text.split("*")
    keywords = [cadena for cadena in keywords if cadena != ""]
    return keywords

def find_coincidences(lista, keywords):
    matches = []
    for i in keywords:
        for j in lista:
            if i in j:
                matches.append(j)
    contador = Counter(matches)
    if len(keywords) > 1:
        matches = [item for item, count in contador.items() if count > 1]
    return matches

def filter_items(search_text):
    keywords = unspace_format(search_text)
    matches = find_coincidences(items, keywords)
    return matches

@app.route('/delete_selected', methods=['POST'])
def delete_selected():
    global selected_items
    items_to_delete = request.form.getlist('selected_items')
    selected_items = [item for item in selected_items if item not in items_to_delete]
    return redirect(url_for('show_selected'))

@app.route('/save_lists', methods=['POST'])
def save_lists():
    global selected_items
    inputs = json.loads(request.form.get('inputs', '[]'))
    
    df = pd.DataFrame({
        'Selected Items': selected_items,
        'Items': inputs
    })
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos')
    
    output.seek(0)
    
    return send_file(
        output,
        as_attachment=True,
        download_name='listas.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

if __name__ == '__main__':
    app.run(debug=True)
