import os
import sys

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.db import get_productos, get_movimientos, get_pedidos

def tabulate_productos():
    """Convierte los datos obtenidos desde la base de datos a un formato tabular para productos."""
    productos = list(get_productos())  # Convertir el cursor en una lista
    datos_tabla = []

    for producto in productos:
        categorias = ""
        for categoria in producto.get('categoria', ''):
            categorias += f"{categoria} "
        datos_tabla.append([
            producto.get('producto', ''),
            producto.get('descripcion', ''),
            producto.get('stock', ''),
            producto.get('precio_unidad', ''),
            categorias,
            producto.get('fecha_creacion', ''),
            producto.get('fecha_modificacion', '')
        ])

    return datos_tabla

def tabulate_movimientos():
    """Convierte los datos obtenidos desde la base de datos a un formato tabular sin duplicados."""
    movimientos = list(get_movimientos())  # Convertir el cursor en una lista
    datos_tabla = []

    # Usar un conjunto para evitar duplicados
    movimientos_vistos = set()

    for movimiento in movimientos:
        fila = (
            movimiento.get('producto', ''),
            movimiento.get('tipo_movimiento', ''),
            movimiento.get('cantidad', ''),
            movimiento.get('fecha', ''),
            movimiento.get('comentario', '')
        )
        if fila not in movimientos_vistos:  # Verificar si la fila ya existe
            movimientos_vistos.add(fila)  # Añadir la fila al conjunto
            datos_tabla.append(list(fila))  # Añadir la fila como lista a los datos

    return datos_tabla

def tabulate_pedidos():
    """Convierte los datos obtenidos desde la base de datos a un formato tabular para pedidos."""
    pedidos = list(get_pedidos())  # Convertir el cursor en una lista
    datos_tabla = []

    for pedido in pedidos:
        if not isinstance(pedido, dict):
            print(f"Warning: Unexpected pedido format: {pedido}")
            continue  # Skip invalid entries

        cliente = pedido.get('cliente', {})
        productos = pedido.get('productos', [])
        datos_tabla.append([
            pedido.get('num_pedido', ''),
            cliente.get('nombre', '') if isinstance(cliente, dict) else '',
            cliente.get('email', '') if isinstance(cliente, dict) else '',
            cliente.get('telefono', '') if isinstance(cliente, dict) else '',
            ", ".join([
                f"{p.get('producto', '')} x {p.get('unidades', 0)} ({p.get('precio_unidad', 0)}€ x unidad)" 
                for p in productos if isinstance(p, dict)
            ]),
            pedido.get('precio_total', 0),
            pedido.get('estado', ''),
            pedido.get('fecha_creacion', ''),
            pedido.get('fecha_modificacion', '')
        ])

    # Ensure rows have exactly 10 elements
    for row in datos_tabla:
        if len(row) != 10:
            print(f"Invalid row length: {len(row)}, Row: {row}")

    return datos_tabla
