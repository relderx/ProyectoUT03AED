from datetime import datetime, timezone

class Producto:
    def __init__(self, nombre: str, descripcion: str, stock: int, precio_unidad: float, categoria: list[str]):
        '''
        Constructor de la clase Producto.'''
        
        self.nombre = self._validate_nombre(nombre)
        self.descripcion = descripcion
        self.stock = self._validate_stock(stock)
        self.precio_unidad = self._validate_precio(precio_unidad)
        self.categoria = self._validate_categoria(categoria)
        self.fecha_creacion = self._current_time()
        self.fecha_modificacion = self._current_time()

    @staticmethod
    def _current_time():
        '''
        Devuelve la hora actual en formato ISO 8601.'''
        
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _validate_nombre(nombre):
        '''
        Valida que el nombre sea una cadena no vacía.'''
        
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError('\'nombre\' debe ser una cadena no vacía.')
        return nombre

    @staticmethod
    def _validate_stock(stock):
        '''
        Valida que el stock sea un número entero no negativo.'''
        
        if not isinstance(stock, int) or stock < 0:
            raise ValueError('\'stock\' debe ser un entero no negativo.')
        return stock

    @staticmethod
    def _validate_precio(precio_unidad):
        '''
        Valida que el precio sea un número flotante no negativo.'''
        
        if not isinstance(precio_unidad, (int, float)) or precio_unidad < 0:
            raise ValueError('\'precio_unidad\' debe ser un número no negativo.')
        return precio_unidad

    @staticmethod
    def _validate_categoria(categoria):
        '''
        Valida que la categoría sea una lista de cadenas no vacías.'''
        
        if not isinstance(categoria, list) or not all(isinstance(cat, str) and cat.strip() for cat in categoria):
            raise ValueError('\'categoria\' debe ser una lista de cadenas no vacías.')
        return categoria

    @property
    def stock(self):
        '''
        Devuelve el stock actual del producto.'''
        
        return self._stock

    @stock.setter
    def stock(self, value):
        '''
        Actualiza el stock y registra la modificación.'''
        
        self._stock = self._validate_stock(value)
        self.fecha_modificacion = self._current_time()

    @property
    def precio_unidad(self):
        '''
        Devuelve el precio unitario del producto.'''
        
        return self._precio_unidad

    @precio_unidad.setter
    def precio_unidad(self, value):
        '''
        Actualiza el precio unitario y registra la modificación.'''
        
        self._precio_unidad = self._validate_precio(value)
        self.fecha_modificacion = self._current_time()

    def to_dict(self):
        '''
        Convierte el producto en un diccionario.'''
        
        return {
            'producto': self.nombre,
            'descripcion': self.descripcion,
            'stock': self.stock,
            'precio_unidad': self.precio_unidad,
            'categoria': self.categoria,
            'fecha_creacion': self.fecha_creacion,
            'fecha_modificacion': self.fecha_modificacion
        }

    def __repr__(self):
        '''
        Devuelve una representación en cadena del producto.'''
        
        return f'<Producto {self.nombre}, {self.stock} unidades, {self.precio_unidad}€/unidad>'
