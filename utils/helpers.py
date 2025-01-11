import os
import sys

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.db import get_productos, get_movimientos, get_pedidos, delete_pedido, update_pedido

def tabulate_productos():
    """Convierte los datos obtenidos desde la base de datos a un formato tabular para productos."""
    productos = list(get_productos())  # Convertir el cursor en una lista
    datos_tabla = []

    for producto in productos:
        datos_tabla.append([
            producto.get('producto', ''),
            producto.get('descripcion', ''),
            producto.get('stock', ''),
            producto.get('precio_unidad', ''),
            producto.get('categoria', ''),
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
        datos_tabla.append([
            pedido.get('num_pedido', ''),
            pedido.get('cliente', {}).get('nombre', ''),
            ", ".join([f"{producto['unidades']}× {producto['producto']}" for producto in pedido.get('productos', [])]),
            pedido.get('precio_total', ''),
            pedido.get('estado', ''),
            pedido.get('fecha_creacion', ''),
            pedido.get('fecha_modificacion', '')
        ])

    return datos_tabla

def borrar_pedido(num_pedido):
    """
    Elimina un pedido de la base de datos por su número.
    """
    try:
        delete_pedido(num_pedido)  # Llama a la función que elimina el pedido en MongoDB
        print(f"Pedido {num_pedido} eliminado correctamente.")
    except Exception as e:
        print(f"Error al eliminar el pedido {num_pedido}: {e}")

def modificar_pedido(num_pedido, nuevos_datos):
    """
    Modifica un pedido existente en la base de datos.
    """
    try:
        update_pedido(num_pedido, nuevos_datos)
        print(f"Pedido {num_pedido} modificado correctamente.")
    except Exception as e:
        print(f"Error al modificar el pedido {num_pedido}: {e}")
