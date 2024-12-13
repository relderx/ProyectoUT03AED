import os
import sys

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.db import get_movimientos

def tabulate_movimientos():
    '''Convierte los datos obtenidos desde la base de datos a un formato tabular.'''
    movimientos = list(get_movimientos())  # Convertir el cursor en una lista
    datos_tabla = []

    for movimiento in movimientos:
        datos_tabla.append([
            movimiento.get('producto', ''),
            movimiento.get('tipo_movimiento', ''),
            movimiento.get('cantidad', ''),
            movimiento.get('fecha', ''),
            movimiento.get('comentario', '')
        ])

    return datos_tabla