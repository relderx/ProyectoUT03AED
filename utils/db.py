import sys
import os
from pymongo import MongoClient

from models.producto import Producto
from models.movimiento import Movimiento
from models.pedido import Pedido

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

def get_producto_by_id(producto_id):
    '''Obtiene un producto por su ID.'''
    return COLL_PRO.find_one({'_id': producto_id})

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

def get_pedidos():
    '''Obtiene todos los pedidos de la base de datos.'''
    return COLL_PED.find()

def add_pedido(pedido: Pedido):
    '''Inserta un nuevo pedido en la base de datos.'''
    return COLL_PED.insert_one(pedido.to_dict())

def get_pedido_by_id(pedido_id):
    '''Obtiene un pedido por su ID.'''
    return COLL_PED.find_one({'_id': pedido_id})

