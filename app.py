from flask import Flask, render_template_string
import flet as ft

app = Flask(__name__)

# Ruta principal de Flask
@app.route("/")
def index():
    # Página HTML básica para incluir la aplicación Flet
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flet con Flask</title>
    </head>
    <body>
        <h1>Aplicación Flet Integrada</h1>
        <iframe src="http://localhost:8550" style="width:100%; height:90vh; border:none;"></iframe>
    </body>
    </html>
    """)

if __name__ == "__main__":
    # Inicia Flask en el puerto 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
