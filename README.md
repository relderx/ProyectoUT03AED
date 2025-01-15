# Aplicación Multiplataforma con Flet y MongoDB

## ¿Qué se necesita para utilizar el proyecto?

Pullea el proyecto dentro de un enviroment de python, para crearlo se utiliza el siguiente comando:

```bash
  py -m venv nombreCarpeta
```

Luego entra en el enviroment, activalo e instala el flet:

```bash
  cd nombreCarpeta
  .\Scripts\activate
  pip install flet
```

Por último, también instala pymongo dentro del enviroment:
```bash
  pip install pymongo
```

Una vez termines, ejecuta el siguiente comando para correr la ventana principal después de haber clonado el repositorio dentro del enviroment:

```bash
  flet run .\views\producto_view.py
```

## Descripción del Proyecto

Este proyecto es una aplicación multiplataforma diseñada para gestionar un sistema de inventarios, pedidos y movimientos de productos. Se desarrolla como parte del proyecto ABP (Aprendizaje Basado en Proyectos), utilizando [Flet](https://flet.dev) para la construcción de la interfaz de usuario y [MongoDB](https://www.mongodb.com/docs) como base de datos documental. La aplicación implementa funcionalidades CRUD (Crear, Leer, Actualizar, Eliminar) para gestionar productos, movimientos de inventario y pedidos, con un enfoque en la simplicidad y eficiencia.

## Ventanas

Las principales ventanas gráficas de la aplicación se organizarán de la siguiente manera:

### Ventana de Productos

- Visualización de todos los productos en el inventario.
- Opciones para agregar, editar y eliminar productos.
- Funcionalidades de búsqueda y filtrado por categoría, precio, y nombre.

### Ventana de Movimientos de Inventario

- Visualiza el historial de movimientos (entradas y salidas) de productos.
- Permite registrar nuevos movimientos (entradas o salidas de inventario).
- Búsqueda por fecha, tipo de movimiento y producto.

### Ventana de Pedidos

- Gestión de los pedidos de los clientes o proveedores.
- Opciones para crear nuevos pedidos, ver los detalles de los existentes y actualizar el estado de los mismos.
- Búsqueda por número de pedido, estado y cliente.

## Estructura de carpetas

```plaintext
Proyecto/
│
├─models/                     # Modelos de datos (definición de estructuras de base de datos)
│ ├───movimientos.py          # Modelo de movimiento de inventario
│ ├───pedidos.py              # Modelo de pedido
│ └───productos.py            # Modelo de producto
│
├─services/                   # Lógica de negocio y servicios
│ ├───movimientos_service.py  # Lógica para gestionar movimientos de inventario
│ ├───pedidos_service.py      # Lógica para gestionar pedidos
│ └───productos_service.py    # Lógica para manejar productos
│
├─utils/                      # Utilidades y funciones generales
│ ├───db.py                   # Conexión y operaciones básicas con MongoDB
│ ├───helpers.py              # Funciones auxiliares y generales
│ └───validators.py           # Funciones de validación de datos
│
├─views/                      # Interfaces de usuario y vistas
│ ├───movimiento_view.py      # Vistas y formularios para movimientos de inventario
│ ├───pedido_view.py          # Vistas y formularios para pedidos
│ └───producto_view.py        # Vistas y formularios para productos
│
├─main.py                     # Archivo principal que inicia la aplicación
│
└─README.md                   # Archivo explicatorio de todo el proyecto
```

## Estructura de la base de datos

La base de datos se organiza en colecciones que almacenan los datos relevantes para la gestión del productos, movimientos y pedidos.

### Colección: Productos

Esta colección almacena la información básica de cada producto en el inventario.

```plaintext
{
  "producto": "",           // string: Nombre del producto
  "descripcion": "",        // string: Descripción del producto
  "stock": 0,               // int: Cantidad en stock
  "precio_unidad": 0.0,     // float: Precio por unidad
  "categoria": [""],        // array[string]: Categorías asociadas al producto
  "fecha_creacion": "",     // string: Fecha de creación en formato ISO 8601 (YYYY-MM-DD)
  "fecha_modificacion": ""  // string: Fecha de última modificación en formato ISO 8601
}
```

### Colección: Movimiento de Inventario

Esta colección registra los cambios en el inventario, ya sean entradas o salidas de productos.

```plaintext
{
  "producto": "",         // string: Nombre o identificador del producto
  "tipo_movimiento": "",  // string: "entrada" o "salida"
  "cantidad": 0,          // int: Cantidad del movimiento
  "fecha": "",            // string: Fecha del movimiento en formato ISO 8601 (YYYY-MM-DD)
  "comentario": ""        // string: Comentario opcional sobre el movimiento
}
```

### Colección: Pedidos

Esta colección gestiona los pedidos realizados por los clientes o a proveedores.

```plaintext
{
  "num_pedido": 0,          // int: Número identificador del pedido
  "cliente": {
    "nombre": "",           // string: Nombre del cliente
    "email": "",            // string: Correo electrónico del cliente
    "telefono": ""          // string: Teléfono del cliente
  },
  "productos": [            // array[dict]: Lista de productos solicitados
    {
      "producto": "",       // string: Nombre o identificador del producto
      "unidades": 0,        // int: Cantidad de unidades solicitadas
      "precio_unidad": 0.0  // float: Precio unitario del producto
    }
  ],
  "precio_total": 0.0,      // float: Precio total del pedido
  "estado": "",             // string: Estado del pedido (ejemplo: "pendiente", "enviado")
  "fecha_creacion": "",     // string: Fecha de creación en formato ISO 8601 (YYYY-MM-DD)
  "fecha_modificacion": ""  // string: Fecha de última modificación en formato ISO 8601
}
```

## **Objetivos**

- **Diseñar** una interfaz de usuario atractiva e intuitiva.
- **Implementar** funcionalidades CRUD con conexión a una base de datos MongoDB.
- **Garantizar** la adaptabilidad en dispositivos de escritorio y móviles.
- **Promover** el trabajo colaborativo en un entorno realista.

## **Funcionalidades**

- **Visualización de datos**: Mostrar productos, movimientos y pedidos en formato de lista con opciones de búsqueda y filtrado por diferentes criterios.
- **Operaciones CRUD**: Implementación de operaciones de Crear, Leer, Actualizar y Eliminar productos, movimientos y pedidos.
- **Gestión de inventario**: Registrar entradas y salidas de productos y realizar un seguimiento detallado de los movimientos.
- **Pedidos**: Crear y gestionar pedidos de productos, actualizar su estado y calcular el precio total.
- **Validación de datos**: Comprobar la validez de los datos ingresados (por ejemplo, correos electrónicos, fechas, cantidades).

## **Requisitos**

### Dependencias

- Python 3.10+
- [Flet](https://flet.dev)
- [MongoDB](https://www.mongodb.com/docs)
- [PyMongo](https://pymongo.readthedocs.io/en/stable/)
