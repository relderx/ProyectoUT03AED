import os
import sys

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.movimientos import Movimiento
from models.productos import Producto
from models.pedidos import Pedido
from utils.db import add_many_movimientos, add_many_productos, add_many_pedidos

# Crear 10 productos
# Cada producto tiene un nombre, descripción, stock disponible, precio unitario y una lista de categorías
productos = [
    Producto("Producto M", "Descripción M", 500, 89.67, ["Categoria3"]),
    Producto("Producto N", "Descripción N", 732, 45.23, ["Categoria2", "Categoria4"]),
    Producto("Producto O", "Descripción O", 300, 12.89, ["Categoria1"]),
    Producto("Producto P", "Descripción P", 654, 67.45, ["Categoria5", "Categoria6"]),
    Producto("Producto Q", "Descripción Q", 890, 34.78, ["Categoria4"]),
    Producto("Producto R", "Descripción R", 470, 76.89, ["Categoria2"]),
    Producto("Producto S", "Descripción S", 240, 89.90, ["Categoria6", "Categoria7"]),
    Producto("Producto T", "Descripción T", 128, 55.55, ["Categoria3"]),
    Producto("Producto U", "Descripción U", 910, 30.23, ["Categoria1", "Categoria7"]),
    Producto("Producto V", "Descripción V", 756, 20.75, ["Categoria2", "Categoria5"]),
]

# Crear 10 movimientos
# Cada movimiento tiene un producto asociado, un tipo de movimiento (entrada, salida, etc.), una cantidad y un comentario
movimientos = [
    Movimiento("Producto M", "entrada", 15, "Donación recibida"),
    Movimiento("Producto N", "salida", 22, "Venta realizada"),
    Movimiento("Producto O", "entrada", 50, "Compra mayorista"),
    Movimiento("Producto P", "salida", 10, "Muestra gratis"),
    Movimiento("Producto Q", "entrada", 35, "Ingreso inicial"),
    Movimiento("Producto R", "salida", 5, "Pedido especial"),
    Movimiento("Producto S", "entrada", 60, "Devolución de cliente"),
    Movimiento("Producto T", "entrada", 30, "Nueva adquisición"),
    Movimiento("Producto U", "salida", 12, "Promoción de ventas"),
    Movimiento("Producto V", "entrada", 45, "Stock inicial"),
]

# Crear 10 pedidos
# Cada pedido incluye un número único, un cliente (con nombre, email y teléfono), una lista de productos comprados, y un estado del pedido
pedidos = [
    Pedido("P045", {"nombre": "Cliente A", "email": "random1@email.com", "telefono": "123456789"}, [{"producto": "Producto M", "unidades": 3, "precio_unidad": 89.67}], "pendiente"),
    Pedido("P072", {"nombre": "Cliente B", "email": "random2@email.com", "telefono": "987654321"}, [{"producto": "Producto N", "unidades": 8, "precio_unidad": 45.23}], "enviado"),
    Pedido("P003", {"nombre": "Cliente C", "email": "random3@email.com", "telefono": "111222333"}, [{"producto": "Producto O", "unidades": 5, "precio_unidad": 12.89}], "entregado"),
    Pedido("P019", {"nombre": "Cliente D", "email": "random4@email.com", "telefono": "222333444"}, [{"producto": "Producto P", "unidades": 2, "precio_unidad": 67.45}], "cancelado"),
    Pedido("P051", {"nombre": "Cliente E", "email": "random5@email.com", "telefono": "555666777"}, [{"producto": "Producto Q", "unidades": 6, "precio_unidad": 34.78}], "pendiente"),
    Pedido("P037", {"nombre": "Cliente F", "email": "random6@email.com", "telefono": "888999000"}, [{"producto": "Producto R", "unidades": 4, "precio_unidad": 76.89}], "enviado"),
    Pedido("P008", {"nombre": "Cliente G", "email": "random7@email.com", "telefono": "444555666"}, [{"producto": "Producto S", "unidades": 7, "precio_unidad": 89.90}], "entregado"),
    Pedido("P063", {"nombre": "Cliente H", "email": "random8@email.com", "telefono": "333444555"}, [{"producto": "Producto T", "unidades": 5, "precio_unidad": 55.55}], "cancelado"),
    Pedido("P092", {"nombre": "Cliente I", "email": "random9@email.com", "telefono": "666777888"}, [{"producto": "Producto U", "unidades": 8, "precio_unidad": 30.23}], "pendiente"),
    Pedido("P014", {"nombre": "Cliente J", "email": "random10@email.com", "telefono": "777888999"}, [{"producto": "Producto V", "unidades": 9, "precio_unidad": 20.75}], "enviado"),
]


# Insertar los productos y mostrar los IDs generados
result_productos = add_many_productos(productos)
print(f"Se han insertado los productos con los IDs: {result_productos.inserted_ids}")

# Insertar los movimientos y mostrar los IDs generados
result_movimientos = add_many_movimientos(movimientos)
print(f"Se han insertado los movimientos con los IDs: {result_movimientos.inserted_ids}")

# Insertar los pedidos y mostrar los IDs generados
result_pedidos = add_many_pedidos(pedidos)
print(f"Se han insertado los pedidos con los IDs: {result_pedidos.inserted_ids}")