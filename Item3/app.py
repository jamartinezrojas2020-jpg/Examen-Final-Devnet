from flask import Flask, request, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DB = "usuarios.db"


def crear_bd():
    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            password TEXT
        )
    """)

    conexion.commit()
    conexion.close()


crear_bd()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Examen DevNet</title>
</head>
<body>

<h2>Registro de Usuario</h2>

<form action="/registro" method="post">

Usuario:<br>
<input type="text" name="usuario"><br><br>

Contraseña:<br>
<input type="password" name="password"><br><br>

<input type="submit" value="Registrar">

</form>

<hr>

<h2>Iniciar Sesión</h2>

<form action="/login" method="post">

Usuario:<br>
<input type="text" name="usuario"><br><br>

Contraseña:<br>
<input type="password" name="password"><br><br>

<input type="submit" value="Ingresar">

</form>

</body>
</html>
"""


@app.route("/")
def inicio():
    return render_template_string(HTML)


@app.route("/registro", methods=["POST"])
def registro():

    usuario = request.form["usuario"]
    password = request.form["password"]

    hash_password = generate_password_hash(password)

    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios(usuario,password) VALUES(?,?)",
            (usuario, hash_password)
        )

        conexion.commit()

        mensaje = f"""
        <h2>Usuario registrado correctamente</h2>

        Usuario: {usuario}

        <br><br>

        <a href="/">Volver</a>
        """

    except:

        mensaje = """
        <h2>El usuario ya existe</h2>

        <a href="/">Volver</a>
        """

    conexion.close()

    return mensaje


@app.route("/login", methods=["POST"])
def login():

    usuario = request.form["usuario"]
    password = request.form["password"]

    conexion = sqlite3.connect(DB)
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT password FROM usuarios WHERE usuario=?",
        (usuario,)
    )

    fila = cursor.fetchone()

    conexion.close()

    if fila:

        if check_password_hash(fila[0], password):

            return f"""
            <h2>Bienvenido {usuario}</h2>

            <a href="/">Volver</a>
            """

    return """
    <h2>Usuario o contraseña incorrectos</h2>

    <a href="/">Volver</a>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5800, debug=True)