from datetime import datetime, timezone

class Producto:
    def __init__(self, nombre: str, descripcion: str, stock: int, precio_unidad: float, categoria: list[str], fecha_creacion=None, fecha_modificacion=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.stock = stock
        self.precio_unidad = precio_unidad
        self.categoria = categoria
        self.fecha_creacion = fecha_creacion if fecha_creacion else datetime.now(timezone.utc).isoformat()
        self.fecha_modificacion = fecha_modificacion if fecha_modificacion else datetime.now(timezone.utc).isoformat()

    def to_dict(self):
        return {
            "producto": self.nombre,
            "descripcion": self.descripcion,
            "stock": self.stock,
            "precio_unidad": self.precio_unidad,
            "categoria": self.categoria,
            "fecha_creacion": self.fecha_creacion,
            "fecha_modificacion": self.fecha_modificacion
        }

    def __repr__(self):
        return f"<Producto {self.nombre}, {self.stock} unidades, ${self.precio_unidad}>"