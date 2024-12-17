from datetime import datetime, timezone

class Pedido:
    # Estados permitidos para los pedidos
    VALID_STATES = {'pendiente', 'enviado', 'entregado', 'cancelado'}

    def __init__(self, num_pedido, cliente, productos, estado):
        '''
        Constructor de la clase Pedido.

        :param num_pedido: (int) Número identificador del pedido.
        :param cliente: (dict) Información del cliente con claves: 'nombre', 'email', 'telefono'.
        :param productos: (list[dict]) Lista de productos con claves: 'producto', 'unidades', 'precio_unidad'.
        :param estado: (str) Estado actual del pedido (ej: 'pendiente', 'enviado').'''
        
        self.num_pedido = num_pedido
        self.cliente = self._validate_cliente(cliente)
        self._productos = self._validate_productos(productos)
        self._precio_total = self._calcular_precio_total()
        self._estado = self._validate_estado(estado)
        self.fecha_creacion = self._current_time()  # Fecha de creación se inicializa automáticamente
        self.fecha_modificacion = self._current_time()  # Fecha de modificación se inicializa automáticamente

    @staticmethod
    def _current_time():
        '''
        Devuelve la hora actual en formato ISO 8601.
        :return: (str) Fecha y hora actual en formato ISO 8601.'''
        
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _validate_cliente(cliente):
        '''
        Valida que el cliente sea un diccionario con claves requeridas.

        :param cliente: (dict) Información del cliente.
        :return: (dict) Cliente validado.
        :raises ValueError: Si el cliente no tiene las claves esperadas.'''
        
        required_keys = {'nombre', 'email', 'telefono'}
        if not isinstance(cliente, dict) or not required_keys.issubset(cliente.keys()):
            raise ValueError(f'\'cliente\' debe ser un diccionario con las claves {required_keys}')
        return cliente

    @staticmethod
    def _validate_productos(productos):
        '''
        Valida que la lista de productos contenga elementos con claves requeridas.

        :param productos: (list[dict]) Lista de productos.
        :return: (list[dict]) Productos validados.
        :raises ValueError: Si algún producto no cumple con las especificaciones.'''
        
        if not isinstance(productos, list):
            raise ValueError('\'productos\' debe ser una lista de diccionarios')
        for producto in productos:
            required_keys = {'producto', 'unidades', 'precio_unidad'}
            if not isinstance(producto, dict) or not required_keys.issubset(producto.keys()):
                raise ValueError(f'Cada producto debe ser un diccionario con las claves {required_keys}')
            if not isinstance(producto['unidades'], int) or producto['unidades'] < 0:
                raise ValueError('\'unidades\' debe ser un entero no negativo')
            if not isinstance(producto['precio_unidad'], (int, float)) or producto['precio_unidad'] < 0:
                raise ValueError('\'precio_unidad\' debe ser un número no negativo')
        return productos

    @staticmethod
    def _validate_estado(estado):
        '''
        Valida que el estado esté dentro de los valores permitidos.

        :param estado: (str) Estado del pedido.
        :return: (str) Estado validado.
        :raises ValueError: Si el estado no es válido.'''
        
        if estado not in Pedido.VALID_STATES:
            raise ValueError(f'Estado inválido. Debe ser uno de {Pedido.VALID_STATES}')
        return estado

    def _calcular_precio_total(self):
        '''
        Calcula el precio total del pedido sumando (unidades * precio_unidad) de cada producto.

        :return: (float) Precio total del pedido.'''
        
        return sum(p['unidades'] * p['precio_unidad'] for p in self._productos)

    @property
    def productos(self):
        '''
        Devuelve la lista de productos.

        :return: (list[dict]) Lista de productos.'''
        
        return self._productos

    @productos.setter
    def productos(self, value):
        '''
        Permite actualizar la lista de productos, recalculando el precio total y actualizando la fecha de modificación.

        :param value: (list[dict]) Nueva lista de productos.'''
        
        self._productos = self._validate_productos(value)
        self._precio_total = self._calcular_precio_total()
        self.fecha_modificacion = self._current_time()

    @property
    def precio_total(self):
        '''
        Devuelve el precio total del pedido.

        :return: (float) Precio total.'''
        
        return self._precio_total

    @property
    def estado(self):
        '''
        Devuelve el estado actual del pedido.

        :return: (str) Estado del pedido.'''
        
        return self._estado

    @estado.setter
    def estado(self, value):
        '''
        Permite actualizar el estado del pedido, validándolo y actualizando la fecha de modificación.

        :param value: (str) Nuevo estado del pedido.'''
        
        self._estado = self._validate_estado(value)
        self.fecha_modificacion = self._current_time()

    def to_dict(self):
        '''
        Convierte la instancia del pedido en un diccionario.

        :return: (dict) Representación del pedido en formato diccionario.'''
        
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
        '''
        Representación en cadena del pedido.

        :return: (str) Representación legible del pedido.'''
        
        return (f'<Pedido {self.num_pedido}, Cliente: {self.cliente['nombre']}, Estado: {self.estado}, Precio: {self.precio_total}>')