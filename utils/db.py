import sys
import os
from pymongo import MongoClient

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.productos import Producto
from models.movimientos import Movimiento
from models.pedidos import Pedido

# Establece la conexión a MongoDB
CLIENT = MongoClient('localhost', 27017)
DB = CLIENT['proyecto_aed_mongodb']

# Definir las colecciones de la base de datos
COLL_PRO = DB['productos']
COLL_MOV = DB['movimientos']
COLL_PED = DB['pedidos']

# Funciones de productos
def get_productos():
    '''Obtiene todos los documentos de la colección de productos.'''
    return COLL_PRO.find()

def add_producto(producto: Producto):
    '''Inserta un nuevo producto en la colección de productos.'''
    return COLL_PRO.insert_one(producto.to_dict())

def add_many_productos(producto: list[Producto]):
    '''Inserta múltiples productos en la colección de productos.'''
    return COLL_PRO.insert_many([pro.to_dict() for pro in producto])

def update_producto(producto_id, producto_data):
    '''Actualiza un producto existente en la colección de productos.'''
    return COLL_PRO.update_one({'_id': producto_id}, {'$set': producto_data})

def delete_producto(producto_id):
    '''Elimina un producto de la colección de productos utilizando su ID.'''
    return COLL_PRO.delete_one({'_id': producto_id})

# Funciones de movimientos
def get_movimientos():
    '''Obtiene todos los documentos de la colección de movimientos de inventario.'''
    return COLL_MOV.find()

def add_movimiento(movimiento: Movimiento):
    '''Inserta un nuevo movimiento de inventario en la colección de movimientos.'''
    return COLL_MOV.insert_one(movimiento.to_dict())

def add_many_movimientos(movimientos: list[Movimiento]):
    '''Inserta múltiples movimientos de inventario en la colección de movimientos.'''
    return COLL_MOV.insert_many([mov.to_dict() for mov in movimientos])

# Funciones de pedidos
def get_pedidos():
    '''Obtiene todos los documentos de la colección de pedidos.'''
    return COLL_PED.find()

def add_pedido(pedido: Pedido):
    '''Inserta un nuevo pedido en la colección de pedidos.'''
    return COLL_PED.insert_one(pedido.to_dict())

def add_many_pedidos(pedidos: list[Pedido]):
    '''Inserta múltiples pedidos en la colección de pedidos.'''
    return COLL_PED.insert_many([ped.to_dict() for ped in pedidos])