import sqlite3, yara
from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# Función de verificación de credenciales
@auth.verify_password
def verify_password(username, password):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cur.fetchone()
    if user and user[2] == password:
        return username    

@app.route('/api/rule', methods=['POST'])
@auth.login_required
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
        return {'message': 'Sintaxis YARA invalida: |'+ rule +' | '+format(str(e))}, 400

    # DB save
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO yara_rules (name, rule) VALUES (?, ?)', (name, rule))
    conn.commit()
    cur.close()

    # Retornar la respuesta
    return jsonify({'message': 'Regla YARA agregada correctamente'}), 201

@app.route('/api/rule/<int:rule_id>', methods=['GET'])
def get_yara_rule(rule_id):
    # Buscar la regla por ID
    result = find_by_id(rule_id)
    if result:
        # Retornar la regla YARA
        return jsonify(result)
    else:
        # Si no se encuentra la regla, devolver un error 404
        return jsonify({'error': 'No se encontró la regla YARA'}), 404


@app.route('/api/rule/<int:rule_id>', methods=['PUT'])
def update_yara_rule(rule_id):
    # Buscar la regla por ID
    result = find_by_id(rule_id)
    if not result:
        return jsonify({'error': 'No se encontró la regla YARA'}), 404

    # Obtener los nuevos datos del body
    name = request.json.get('name', result['yara_rule'])
    rule = request.json.get('rule', result['yara_rule'])

    # Validar que los nuevos datos sean correctos
    if not name or not rule:
        return jsonify({'error': 'Los datos del body son incorrectos'}), 400

    # Validacion sintaxis YARA
    try:
        yara.compile(source=rule)
    except yara.SyntaxError as e:
        return {'message': 'Sintaxis YARA invalida: |'+ rule +' | '+format(str(e))}, 400

    # Actualizar los datos en la base de datos
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('UPDATE yara_rules SET name=?, rule=? WHERE id=?', (name, rule, rule_id))
    conn.commit()
    cur.close()

    # Retornar la respuesta
    return jsonify({'message': 'Regla YARA actualizada correctamente'}), 200


@app.route('/api/analyze/text', methods=['POST'])
@auth.login_required
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


@app.route('/api/analyze/file', methods=['POST'])
@auth.login_required
def file_analyzer():
    files = request.files['file']
    rule_ids = request.form['rules'].split(",")

    # leer el contenido del archivo
    file_content = files.read()

    # Obtener las reglas YARA almacenadas en la base de datos
    rules = []
    for rule_id in rule_ids:
        rule = find_by_id(rule_id)
        if rule:
            rules.append(rule)

    # Ejecutar las reglas YARA contra el texto
    results = []
    for rule in rules:
        matched = False
        compiled_rule = yara.compile(source=rule['yara_rule'])
        matched = bool(compiled_rule.match(data=file_content))
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

