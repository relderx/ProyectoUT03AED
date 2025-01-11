import flet as ft
from fastapi import FastAPI
import uvicorn
import threading

from views.producto_view.src.main import main as create_producto_page

# Crear la app FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "¡Hola desde FastAPI!"}

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Ejecutar FastAPI en un hilo
    threading.Thread(target=run_fastapi).start()

    # Ejecutar Flet en tu dirección IP local
    ft.app(target=create_producto_page, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=8550)
