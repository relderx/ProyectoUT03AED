import sys
import os
from pymongo import MongoClient

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.productos import Producto
from models.movimientos import Movimiento
from models.pedidos import Pedido

# Establece la conexión a MongoDB
CLIENT = MongoClient('localhost', 27017)  # Asegúrate de que MongoDB esté corriendo en localhost:27017
DB = CLIENT['proyecto_aed_mongodb']

# Definir las colecciones
COLL_PRO = DB['productos']
COLL_MOV = DB['movimientos']
COLL_PED = DB['pedidos']

def get_productos():
    '''Obtiene todos los productos de la base de datos.'''
    return COLL_PRO.find()

def add_producto(producto: Producto):
    '''Inserta un producto nuevo en la base de datos.'''
    return COLL_PRO.insert_one(producto.to_dict())

def update_producto(producto_id, producto_data):
    '''Actualiza un producto en la base de datos.'''
    return COLL_PRO.update_one({'_id': producto_id}, {'$set': producto_data})

def delete_producto(producto_id):
    '''Elimina un producto de la base de datos.'''
    return COLL_PRO.delete_one({'_id': producto_id})

def get_movimientos():
    '''Obtiene todos los movimientos de inventario.'''
    return COLL_MOV.find()

def add_movimiento(movimiento: Movimiento):
    '''Inserta un nuevo movimiento de inventario.'''
    return COLL_MOV.insert_one(movimiento.to_dict())

def add_many_movimientos(movimientos: list[Movimiento]):
    '''Inserta múltiples documentos de movimientos en la colección correspondiente.'''
    return COLL_MOV.insert_many([mov.to_dict() for mov in movimientos])

def get_pedidos():
    '''Obtiene todos los pedidos de la base de datos.'''
    return COLL_PED.find()

def add_pedido(pedido: Pedido):
    '''Inserta un nuevo pedido en la base de datos.'''
    return COLL_PED.insert_one(pedido.to_dict())

