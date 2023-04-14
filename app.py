import sqlite3, yara
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

    # Validacion sintaxis YARA 
    try:
        yara.compile(source=rule)
    except yara.SyntaxError as e:
        return {'message': 'Sintaxis YARA invalida: {}'.format(str(e))}, 400

    # DB save
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO yara_rules (name, rule) VALUES (?, ?)', (name, rule))
    conn.commit()
    cur.close()

    # Retornar la respuesta
    return jsonify({'message': 'Regla YARA agregada correctamente'}), 201


@app.route('/api/analyze/text', methods=['POST'])
def text_analyzer():
    text = request.json['text']
    rule_ids = request.json['rules']

    # Obtener las reglas YARA almacenadas en la base de datos
    rules = []
    for rule_id in rule_ids:
        rule = find_by_id(rule_id['rule_id'])
        if rule:
            rules.append(rule)

    # Ejecutar las reglas YARA contra el texto
    results = []
    for rule in rules:
        matched = False
        compiled_rule = yara.compile(source=rule['yara_rule'])
        matched = bool(compiled_rule.match(data=text))
        results.append({'rule_id': rule['rule_id'],'matched':matched})

    return jsonify({'message': rules,'status': "ok",'results': results}), 201

def find_by_id(rule_id):
    # Conexión a la base de datos SQLite
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Consulta SQL para buscar la regla por su identificador
    query = 'SELECT name, rule FROM yara_rules WHERE id = ?'
    result = cursor.execute(query, (rule_id,)).fetchone()

    if result:
        name, rule = result
        return ({'rule_id': rule_id, 'yara_rule': rule})

    # Cerrar la conexión a la base de datos
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)

