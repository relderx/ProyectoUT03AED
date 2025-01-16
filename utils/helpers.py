import os
import sys

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.db import get_productos, get_movimientos, get_pedidos

# Tabular los datos de productos desde la base de datos
def tabulate_productos():
    productos = list(get_productos())  # Convertir el cursor en una lista
    datos_tabla = []

    for producto in productos:
        # Construir la cadena de categorías
        categorias = ""
        for categoria in producto.get("categoria", ""):
            categorias += f"{categoria} "
        # Agregar los datos del producto a la tabla
        datos_tabla.append(
            [
                producto.get("producto", ""),
                producto.get("descripcion", ""),
                producto.get("stock", ""),
                producto.get("precio_unidad", ""),
                categorias,
                producto.get("fecha_creacion", ""),
                producto.get("fecha_modificacion", ""),
            ]
        )

    return datos_tabla


# Tabular los datos de movimientos desde la base de datos, eliminando duplicados
def tabulate_movimientos():
    movimientos = list(get_movimientos())  # Convertir el cursor en una lista
    datos_tabla = []
    movimientos_vistos = set()  # Usar un conjunto para evitar duplicados

    for movimiento in movimientos:
        # Crear una fila para el movimiento
        fila = (
            movimiento.get("producto", ""),
            movimiento.get("tipo_movimiento", ""),
            movimiento.get("cantidad", ""),
            movimiento.get("fecha", ""),
            movimiento.get("comentario", ""),
        )
        # Añadir la fila si no está duplicada
        if fila not in movimientos_vistos:
            movimientos_vistos.add(fila)
            datos_tabla.append(list(fila))

    return datos_tabla


# Tabular los datos de pedidos desde la base de datos
def tabulate_pedidos():
    pedidos = list(get_pedidos())  # Convertir el cursor en una lista
    datos_tabla = []

    for pedido in pedidos:
        # Verificar que el pedido sea válido
        if not isinstance(pedido, dict):
            print(f"Warning: Unexpected pedido format: {pedido}")
            continue

        # Obtener los datos del cliente y los productos
        cliente = pedido.get("cliente", {})
        productos = pedido.get("productos", [])
        # Agregar los datos del pedido a la tabla
        datos_tabla.append(
            [
                pedido.get("num_pedido", ""),
                cliente.get("nombre", "") if isinstance(cliente, dict) else "",
                cliente.get("email", "") if isinstance(cliente, dict) else "",
                cliente.get("telefono", "") if isinstance(cliente, dict) else "",
                ", ".join(
                    [
                        f"{p.get('producto', '')} x {p.get('unidades', 0)} ({p.get('precio_unidad', 0)}€ x unidad)"
                        for p in productos
                        if isinstance(p, dict)
                    ]
                ),
                pedido.get("precio_total", 0),
                pedido.get("estado", ""),
                pedido.get("fecha_creacion", ""),
                pedido.get("fecha_modificacion", ""),
            ]
        )

    # Verificar que todas las filas tengan 10 elementos
    for row in datos_tabla:
        if len(row) != 10:
            print(f"Invalid row length: {len(row)}, Row: {row}")

    return datos_tabla
