import os
import sys

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.pedidos import Pedido

# Crear un pedido
pedido = Pedido(
    num_pedido=1,
    cliente={"nombre": "Ana López", "email": "ana@example.com", "telefono": "987654321"},
    productos=[
        {"producto": "Teclado", "unidades": 2, "precio_unidad": 50.0},
        {"producto": "Monitor", "unidades": 1, "precio_unidad": 150.0}
    ],
    estado="pendiente"
)

print(pedido)
print(pedido.to_dict(), end='\n\n')

# Cambiar el estado
pedido.estado = "enviado"
# Modificar productos
pedido.productos = [{"producto": "Mouse", "unidades": 3, "precio_unidad": 25.0}]

print(pedido)
print(pedido.to_dict())
