import sqlite3
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuración de base de datos
DB_NAME = "usuarios.db"

def inicializar_bd():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Crear tabla de usuarios si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    
    mi_nombre = "Luis_Bustos" 
    
    usuarios_iniciales = [
        (mi_nombre, "ClaveExamen2026!"),
        ("usuario_docente", "IplacexDevnet2026")
    ]
    
    # Insertar usuarios guardando sus contraseñas en Hash SHA-256
    for user, password in usuarios_iniciales:
        # Generar hash SHA-256
        pwd_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        try:
            cursor.execute('INSERT INTO usuarios (username, password_hash) VALUES (?, ?)', (user, pwd_hash))
            print(f"Usuario '{user}' registrado con Hash: {pwd_hash}")
        except sqlite3.IntegrityError:
            pass # El usuario ya está registrado
            
    conn.commit()
    conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"status": "error", "mensaje": "Se requiere username y password"}), 400
        
    username = data['username']
    password = data['password']
    
    # Generar hash de la contraseña ingresada para comparar
    pwd_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM usuarios WHERE username = ? AND password_hash = ?', (username, pwd_hash))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({"status": "exito", "mensaje": f"Autenticacion exitosa. Bienvenido {username}"}), 200
    else:
        return jsonify({"status": "error", "mensaje": "Credenciales invalidas"}), 401

if __name__ == '__main__':
    print("Inicializando base de datos SQLite con Hashing SHA-256...")
    inicializar_bd()
    print("Iniciando servidor Web Flask en el puerto 5800...")
    app.run(host='0.0.0.0', port=5800)
