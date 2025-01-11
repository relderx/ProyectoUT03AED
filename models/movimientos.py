from datetime import datetime, timezone

class Movimiento:
    VALID_TYPES = {'entrada', 'salida', 'ajuste'}

    def __init__(self, producto: str, tipo_movimiento: str, cantidad: int, comentario: str = ''):
        '''
        Constructor de la clase Movimiento.'''
        
        self.producto = self._validate_producto(producto)
        self.tipo_movimiento = self._validate_tipo_movimiento(tipo_movimiento)
        self.cantidad = self._validate_cantidad(cantidad)
        self.fecha = self._current_time()
        self.comentario = comentario

    @staticmethod
    def _current_time():
        '''
        Devuelve la hora actual en formato ISO 8601.'''
        
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _validate_producto(producto):
        '''
        Valida que el producto sea una cadena no vacía.'''
        
        if not isinstance(producto, str) or not producto.strip():
            raise ValueError('\'producto\' debe ser una cadena no vacía.')
        return producto

    @staticmethod
    def _validate_tipo_movimiento(tipo_movimiento):
        '''
        Valida que el tipo de movimiento sea uno de los valores permitidos.'''
        
        if tipo_movimiento not in Movimiento.VALID_TYPES:
            raise ValueError(f'\'tipo_movimiento\' debe ser uno de {Movimiento.VALID_TYPES}')
        return tipo_movimiento

    @staticmethod
    def _validate_cantidad(cantidad):
        '''
        Valida que la cantidad sea un número entero positivo.'''
        
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError('\'cantidad\' debe ser un entero positivo.')
        return cantidad

    def to_dict(self):
        '''
        Convierte el movimiento en un diccionario.'''
        
        return {
            'producto': self.producto,
            'tipo_movimiento': self.tipo_movimiento,
            'cantidad': self.cantidad,
            'fecha': self.fecha,
            'comentario': self.comentario
        }
    def __str__(self):
        return f"{self.producto}, {self.cantidad}, {self.comentario}, {self.tipo_movimiento}, {self.fecha}"

    def __repr__(self):
        '''
        Devuelve una representación en cadena del movimiento.'''
        
        return (f'<Movimiento: {self.tipo_movimiento} de {self.cantidad} unidades de {self.producto}>')
