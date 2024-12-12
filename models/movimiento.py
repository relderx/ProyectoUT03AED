from datetime import datetime, timezone

class Movimiento:
    def __init__(self, producto: str, tipo_movimiento: str, cantidad: int, fecha=None, comentario=""):
        self.producto = producto
        self.tipo_movimiento = tipo_movimiento
        self.cantidad = cantidad
        self.fecha = fecha if fecha else datetime.now(timezone.utc).isoformat()
        self.comentario = comentario

    def to_dict(self):
        return {
            "producto": self.producto,
            "tipo_movimiento": self.tipo_movimiento,
            "cantidad": self.cantidad,
            "fecha": self.fecha,
            "comentario": self.comentario
        }

    def __repr__(self):
        return f"<Movimiento {self.tipo_movimiento} de {self.cantidad} unidades de {self.producto}>"