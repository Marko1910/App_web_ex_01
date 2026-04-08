from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify
import psycopg2
import os
import traceback

app = Flask(__name__, template_folder='templates')

# Configuración de la base de datos
DB_HOST = 'dpg-d7bcj9ua2pns7381rhn0-a'
DB_NAME = 'dbexamen_ur9z'
DB_USER = 'dbexamen_ur9z_user'
DB_PASSWORD = 'R5fd8WNkY8uxYv7azKw5ILQZ62sKOb1H'


def conectar_db():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST,
        sslmode='disable')
    return conn


def crear_persona(dni, nombre, apellido, direccion, telefono):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO personas (dni, nombre, apellido, direccion, telefono) VALUES (%s, %s, %s, %s, %s)",
                   (dni, nombre, apellido, direccion, telefono))
    conn.commit()
    conn.close()

def obtener_registros():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas ORDER BY apellido")
    registros = cursor.fetchall()
    conn.close()
    return registros

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    dni = request.form['dni']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    crear_persona(dni, nombre, apellido, direccion, telefono)
    mensaje_confirmacion = "Registro Exitoso"
    return redirect(url_for('index', mensaje_confirmacion=mensaje_confirmacion))

@app.route('/administrar')
def administrar():
    registros=obtener_registros()
    return render_template('administrar.html',registros=registros)

@app.route('/eliminar/<dni>', methods=['POST'])
def eliminar_registro(dni):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personas WHERE dni = %s", (dni,))
    conn.commit()
    conn.close()
    return redirect(url_for('administrar'))

@app.errorhandler(Exception)
def handle_exception(e):
    tb = traceback.format_exc()
    print("ERROR:", tb)
    return f"<pre>ERROR:\n{tb}</pre>", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
