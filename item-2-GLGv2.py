import hashlib
import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for
from cryptography.fernet import Fernet

app = Flask(__name__)

clave_secreta = Fernet.generate_key()

with open('clave_secreta.txt', 'wb') as archivo_clave:
    archivo_clave.write(clave_secreta)

def get_db_connection():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre_apellido TEXT, correo TEXT, contraseña_hash TEXT)''')
    conn.commit()
    conn.close()

init_db()

def cifrar_contraseña(contraseña):
    cifrador = Fernet(clave_secreta)
    return cifrador.encrypt(contraseña.encode()).decode()

def validar_contraseña(contraseña, contraseña_hash):
    cifrador = Fernet(clave_secreta)
    contraseña_cifrada = cifrador.encrypt(contraseña.encode()).decode()
    return contraseña_cifrada == contraseña_hash

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre_apellido = request.form['nombre_apellido']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        contraseña_hash = hashlib.sha256(contraseña.encode()).hexdigest()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre_apellido, correo, contraseña_hash) VALUES (?, ?, ?)",
                       (nombre_apellido, correo, contraseña_hash))
        conn.commit()
        conn.close()
        return 'Usuario registrado correctamente'
    return render_template('formulario_registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            datos = request.get_json()
            if not datos or 'correo' not in datos or 'contraseña' not in datos:
                return 'Inicio de sesión fallido: Datos incompletos', 400

            correo = datos['correo']
            contraseña = datos['contraseña']

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE correo=?", (correo,))
            usuario = cursor.fetchone()
            conn.close()

            if usuario:
                if usuario[2] == correo and hashlib.sha256(contraseña.encode()).hexdigest() == usuario[3]:
                    return 'Inicio de sesión exitoso'
                else:
                    return 'Inicio de sesión fallido: contraseña incorrecta', 401
            else:
                return 'Inicio de sesión fallido: usuario no registrado', 404
        except Exception as e:
            return 'Error al iniciar sesión', 500
    else:
        return render_template('formulario_login.html')


@app.route('/')
def formulario_login():
    return render_template('formulario_login.html')


if __name__ == '__main__':
    app.run(port=8500)

conn.close()
