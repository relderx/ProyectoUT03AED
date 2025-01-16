import sys
import os
from datetime import datetime, timezone
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
    producto_data['fecha_modificacion'] = producto_data.get(
        'fecha_modificacion', 
        datetime.now(timezone.utc).isoformat()
    )
    return COLL_PRO.update_one({'producto': producto_id}, {'$set': producto_data})

def obtener_id_producto(nombre_producto):
    """
    Devuelve el ID (_id) del producto basado en su nombre.
    Si no existe un producto con ese nombre, devuelve None.
    """
    producto = COLL_PRO.find_one({'producto': nombre_producto})
    return producto['_id'] if producto else None

def delete_producto(producto_id):
    '''Elimina un producto de la colección de productos utilizando su ID.'''
    return COLL_PRO.delete_one({'producto': producto_id})

def producto_existe(nombre_producto):
    '''Verifica si un producto con el nombre dado ya existe en la base de datos.'''
    return COLL_PRO.find_one({'producto': nombre_producto}) is not None

def get_movimientos():
    '''Obtiene todos los documentos de la colección de movimientos de inventario.'''
    return COLL_MOV.find()

def add_movimiento(movimiento: Movimiento):
    '''Inserta un nuevo movimiento de inventario en la colección de movimientos.'''
    return COLL_MOV.insert_one(movimiento.to_dict())

def add_many_movimientos(movimientos: list[Movimiento]):
    '''Inserta múltiples movimientos de inventario en la colección de movimientos.'''
    return COLL_MOV.insert_many([mov.to_dict() for mov in movimientos])

def update_movimiento(movimiento_id, movimiento_data):
    '''Actualiza un movimiento existente en la colección de movimientos.'''
    return COLL_MOV.update_one({'producto': movimiento_id}, {'$set': movimiento_data})

def delete_movimiento(movimiento_id):
    '''Elimina un movimiento de la colección de movimientos utilizando su ID.'''
    return COLL_MOV.delete_one({'producto': movimiento_id})

def movimiento_existe(producto):
    '''Verifica si un movimiento con el producto dado ya existe en la base de datos.'''
    return COLL_MOV.find_one({'producto': producto}) is not None

def obtener_id_movimiento(producto_nombre):
    """
    Devuelve el ID (_id) del movimiento basado en el nombre del producto.
    Si no existe un movimiento con ese producto, devuelve None.
    """
    movimiento = COLL_MOV.find_one({'producto': producto_nombre})
    return movimiento['_id'] if movimiento else None

def get_pedidos():
    '''Obtiene todos los documentos de la colección de pedidos.'''
    return COLL_PED.find()

def add_pedido(pedido: Pedido):
    '''Inserta un nuevo pedido en la colección de pedidos.'''
    return COLL_PED.insert_one(pedido.to_dict())

def add_many_pedidos(pedidos: list[Pedido]):
    '''Inserta múltiples pedidos en la colección de pedidos.'''
    return COLL_PED.insert_many([ped.to_dict() for ped in pedidos])

def update_pedido(pedido_id, pedido_data):
    '''Actualiza un pedido existente en la colección de pedidos.'''
    return COLL_PED.update_one({'num_pedido': pedido_id}, {'$set': pedido_data})

def delete_pedido(pedido_id):
    '''Elimina un pedido de la colección de pedidos utilizando su ID.'''
    return COLL_PED.delete_one({'num_pedido': pedido_id})
