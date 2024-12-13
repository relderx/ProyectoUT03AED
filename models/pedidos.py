from datetime import datetime, timezone

class Pedido:
    def __init__(self, num_pedido, cliente_nombre, cliente_email, cliente_telefono, productos, precio_total, estado, fecha_creacion=None, fecha_modificacion=None):
        self.num_pedido = num_pedido
        # self.cliente = cliente  # Cliente es un diccionario con 'nombre', 'email', 'telefono'
        self.cliente = {'nombre': cliente_nombre, 'email': cliente_email, 'telefono': cliente_telefono}
        self.productos = productos  # Lista de diccionarios con 'producto', 'unidades', 'precio_unidad'
        self.precio_total = precio_total
        self.estado = estado
        self.fecha_creacion = fecha_creacion if fecha_creacion else datetime.now(timezone.utc).isoformat()
        self.fecha_modificacion = fecha_modificacion if fecha_modificacion else datetime.now(timezone.utc).isoformat()

    def to_dict(self):
        return {
            'num_pedido': self.num_pedido,
            'cliente': self.cliente,
            'productos': self.productos,
            'precio_total': self.precio_total,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion,
            'fecha_modificacion': self.fecha_modificacion
        }

    def __repr__(self):
        return f'<Pedido {self.num_pedido}, Cliente: {self.cliente['nombre']}, Estado: {self.estado}>'