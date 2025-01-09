import os
import sys

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.movimientos import Movimiento
from models.productos import Producto
from models.pedidos import Pedido
from utils.db import add_many_movimientos, add_many_productos, add_many_pedidos

# Crear 10 productos
productos = [
    Producto("Producto A", "Descripción A", 100, 10.0, ["Categoria1"]),
    Producto("Producto B", "Descripción B", 200, 20.0, ["Categoria1", "Categoria2"]),
    Producto("Producto C", "Descripción C", 300, 30.0, ["Categoria2"]),
    Producto("Producto D", "Descripción D", 400, 40.0, ["Categoria3"]),
    Producto("Producto E", "Descripción E", 500, 50.0, ["Categoria3", "Categoria4"]),
    Producto("Producto F", "Descripción F", 600, 60.0, ["Categoria4"]),
    Producto("Producto G", "Descripción G", 700, 70.0, ["Categoria5"]),
    Producto("Producto H", "Descripción H", 800, 80.0, ["Categoria5", "Categoria6"]),
    Producto("Producto I", "Descripción I", 900, 90.0, ["Categoria6"]),
    Producto("Producto J", "Descripción J", 1000, 100.0, ["Categoria7"])
]

# Crear 10 movimientos
movimientos = [
    Movimiento("Producto A", "entrada", 50, "Ingreso inicial"),
    Movimiento("Producto B", "salida", 10, "Venta"),
    Movimiento("Producto C", "entrada", 100, "Compra mayorista"),
    Movimiento("Producto D", "salida", 5, "Muestra gratis"),
    Movimiento("Producto E", "entrada", 20, "Devolución de cliente"),
    Movimiento("Producto F", "entrada", 30, "Nueva adquisición"),
    Movimiento("Producto G", "salida", 15, "Pedido especial"),
    Movimiento("Producto H", "entrada", 200, "Stock inicial"),
    Movimiento("Producto I", "salida", 25, "Promoción de ventas"),
    Movimiento("Producto J", "entrada", 10, "Donación recibida")
]

# Crear 10 pedidos
pedidos = [
    Pedido(f"P001", {"nombre": "Cliente A", "email": "clientea@email.com", "telefono": "123456789"}, [{"producto": "Producto A", "unidades": 10, "precio_unidad": 10.0}], "pendiente"),
    Pedido(f"P002", {"nombre": "Cliente B", "email": "clienteb@email.com", "telefono": "987654321"}, [{"producto": "Producto B", "unidades": 5, "precio_unidad": 20.0}], "enviado"),
    Pedido(f"P003", {"nombre": "Cliente C", "email": "clientec@email.com", "telefono": "123123123"}, [{"producto": "Producto C", "unidades": 3, "precio_unidad": 30.0}], "entregado"),
    Pedido(f"P004", {"nombre": "Cliente D", "email": "cliented@email.com", "telefono": "321321321"}, [{"producto": "Producto D", "unidades": 2, "precio_unidad": 40.0}], "cancelado"),
    Pedido(f"P005", {"nombre": "Cliente E", "email": "clientee@email.com", "telefono": "654654654"}, [{"producto": "Producto E", "unidades": 7, "precio_unidad": 50.0}], "pendiente"),
    Pedido(f"P006", {"nombre": "Cliente F", "email": "clientef@email.com", "telefono": "987987987"}, [{"producto": "Producto F", "unidades": 8, "precio_unidad": 60.0}], "enviado"),
    Pedido(f"P007", {"nombre": "Cliente G", "email": "clienteg@email.com", "telefono": "567567567"}, [{"producto": "Producto G", "unidades": 6, "precio_unidad": 70.0}], "entregado"),
    Pedido(f"P008", {"nombre": "Cliente H", "email": "clienteh@email.com", "telefono": "111222333"}, [{"producto": "Producto H", "unidades": 10, "precio_unidad": 80.0}], "pendiente"),
    Pedido(f"P009", {"nombre": "Cliente I", "email": "clientei@email.com", "telefono": "444555666"}, [{"producto": "Producto I", "unidades": 15, "precio_unidad": 90.0}], "enviado"),
    Pedido(f"P010", {"nombre": "Cliente J", "email": "clientej@email.com", "telefono": "777888999"}, [{"producto": "Producto J", "unidades": 12, "precio_unidad": 100.0}], "entregado")
]

# Agregar productos, movimientos y pedidos a la base de datos
result_productos = add_many_productos(productos)
print(f"Se han insertado los productos con los IDs: {result_productos.inserted_ids}")

result_movimientos = add_many_movimientos(movimientos)
print(f"Se han insertado los movimientos con los IDs: {result_movimientos.inserted_ids}")

result_pedidos = add_many_pedidos(pedidos)
print(f"Se han insertado los pedidos con los IDs: {result_pedidos.inserted_ids}")
