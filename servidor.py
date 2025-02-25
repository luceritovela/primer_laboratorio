from flask import Flask, jsonify, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecreto'

# Credenciales válidas para autenticación
USUARIO_VALIDO = "jenni"
CLAVE_VALIDA = "1234j"

# Base de datos simulada
base_datos = {
    'usuarios': [
        {'id': 1, 'nombre': 'Juan'},
        {'id': 2, 'nombre': 'Maria'},
    ]
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        clave = request.form.get('clave')
        
        if usuario == USUARIO_VALIDO and clave == CLAVE_VALIDA:
            session['usuario'] = usuario
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Credenciales incorrectas. Inténtelo de nuevo.")
    
    return render_template('login.html')

@app.route('/index')
def index():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', usuarios=base_datos['usuarios'])

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    if request.method == 'POST':
        # Intentar recibir JSON primero
        if request.is_json:
            nuevo_usuario = request.json.get("nombre")
        else:  # Si no es JSON, recibir desde un formulario HTML
            nuevo_usuario = request.form.get("nombre")

        if nuevo_usuario:
            nuevo_id = max([u['id'] for u in base_datos['usuarios']], default=0) + 1
            base_datos['usuarios'].append({'id': nuevo_id, 'nombre': nuevo_usuario})
            return jsonify({"mensaje": "Usuario agregado exitosamente", "id": nuevo_id}), 201
        
        return jsonify({"error": "Nombre requerido"}), 400
    
    return jsonify(base_datos['usuarios'])

@app.route('/usuarios/<int:usuario_id>', methods=['GET', 'DELETE'])
def manejar_usuario(usuario_id):
    usuario = next((u for u in base_datos['usuarios'] if u['id'] == usuario_id), None)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    if request.method == 'DELETE':
        base_datos['usuarios'].remove(usuario)
        return jsonify({"mensaje": "Usuario eliminado exitosamente"}), 200
    
    return jsonify(usuario)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
