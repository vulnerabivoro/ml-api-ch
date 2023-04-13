import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/rule', methods=['POST'])
def add_yara_rule():
    # Obtener los datos del body
    name = request.json['name']
    rule = request.json['rule']
    
    # Validar que los datos del body sean correctos
    if not name or not rule:
        return jsonify({'error': 'Los datos del body son incorrectos'}), 400

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    
    # Agregar la regla YARA
    # Código para agregar la regla YARA
    cur.execute('INSERT INTO yara_rules (name, rule) VALUES (?, ?)', (name, rule))
    conn.commit()
    cur.close()

    # Retornar la respuesta
    return jsonify({'message': 'Regla YARA agregada correctamente'}), 201

if __name__ == '__main__':
    app.run(debug=True)

