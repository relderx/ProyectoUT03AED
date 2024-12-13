import os
import sys

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.movimientos import Movimiento
from utils.db import add_many_movimientos

# Crear 10 movimientos
movimientos = [
    Movimiento("Producto A", "entrada", 50, comentario="Ingreso inicial"),
    Movimiento("Producto B", "salida", 10, comentario="Venta"),
    Movimiento("Producto C", "entrada", 100, comentario="Compra mayorista"),
    Movimiento("Producto A", "salida", 5, comentario="Muestra gratis"),
    Movimiento("Producto B", "entrada", 20, comentario="Devolución de cliente"),
    Movimiento("Producto D", "entrada", 30, comentario="Nueva adquisición"),
    Movimiento("Producto C", "salida", 15, comentario="Pedido especial"),
    Movimiento("Producto E", "entrada", 200, comentario="Stock inicial"),
    Movimiento("Producto F", "salida", 25, comentario="Promoción de ventas"),
    Movimiento("Producto G", "entrada", 10, comentario="Donación recibida")
]

# Insertar movimientos en MongoDB
result = add_many_movimientos(movimientos)

# Verificar inserción
print(f"Se han insertado los siguientes IDs: {result.inserted_ids}")
