<!-- Por ChatGPT -->

# **Aplicación Multiplataforma con Flet y MongoDB**

## **Descripción del Proyecto**

Este proyecto es una aplicación multiplataforma desarrollada como parte del proyecto ABP (Aprendizaje Basado en Proyectos). Utiliza [Flet](https://flet.dev) para construir la interfaz de usuario y [MongoDB](https://www.mongodb.com/docs) como base de datos documental. La aplicación implementa funcionalidades CRUD (Crear, Leer, Actualizar, Eliminar) para gestionar datos, y está diseñada para resolver una necesidad práctica en un contexto específico.

## **Ventanas**
Las principales ventanas gráficas se reparten en el siguiente orden

### Ventana principal
En esta ventana se ven todos los productos de la empresa con su estocaje, a parte de los botones con los que se hacen las operaciones CRUD.

Por defecto los productos están ordenados por nombre de manera descendente, pero se pueden aplicar una gran variedad de filtros para ver los productos requeridos.

### Ventana de inserción
Al pulsar en el botón de insertar/añadir, saldrá un popup en el que se pone los datos del producto, asignando el producto/subproducto a su respectiva categoría y producto.

Si no se tiene seleccionado ningún producto, el botón aparecerá como insertar y al aparecer el popup ningún campo a rellenar saldrá rellenado, en caso de que se seleccione uno o más subproductos el botón se desactiva, en caso de que se tenga seleccionado un producto, el botón cambiará a añadir y, al hacer clic en el botón, se auto-rellenará el apartado de categoría con el de el producto padre.

Cuando se hayan añadido todos los datos del producto se podrá hacer clic en dos botones, Crear y Cancelar, si se le dá a crear se cierra la ventana, se crea/añade al producto y se actualiza la ventana principal, si se da a cancelar se cierra la ventana y se actualiza la ventana principal.

### Ventana de actualización
Por defecto, el botón está desactivado, pero se activará una vez se seleccione un solo producto.

Cuando se haga clic en el botón, se abrirá un popup con los datos auto-rellenados del producto, se podrán cambiar cualquiera de los datos.

Cuando se hayan añadido todos los datos del producto se podrá hacer clic en dos botones, Actualizar y Cancelar, si se le dá a actualizar se cierra la ventana, se actualizan los datos y se actualiza la ventana principal, si se da a cancelar se cierra la ventana y se actualiza la ventana principal.

### Ventana de eliminación
Por defecto, el botón está desactivado, pero se activará una vez se seleccione uno o más productos/subproductos.

Cuando se haga clic en el botón, se abrirá un popup de confirmación en el que se le pregunta al usuario si está seguro de hacer esta acción.

Si se le dá clic a si se cierra la ventana, se borran los productos y se actualiza la ventana principal, si se le dá a no se cierra la ventana y se actualiza la ventana principal.

## **Estructura BD**
### Colección: Productos
Esta colección almacena la información básica de cada producto.
```json
{
  "producto": "",           // string: Nombre del producto
  "descripcion": "",        // string: Descripción del producto
  "stock": 0,               // int: Cantidad en stock
  "precio_unidad": 0.0,     // float: Precio por unidad
  "categoria": ["",],       // array[string]: Categorías asociadas al producto
  "fecha_creacion": "",     // string: Fecha de creación en formato ISO 8601 (YYYY-MM-DD)
  "fecha_modificacion": ""  // string: Fecha de última modificación en formato ISO 8601
}
```

### Colección: Movimiento de Inventario
Esta colección registra los cambios en el inventario (entradas y salidas).
```json
{
  "producto": "",         // string: Nombre o identificador del producto
  "tipo_movimiento": "",  // string: "entrada" o "salida"
  "cantidad": 0,          // int: Cantidad del movimiento
  "fecha": "",            // string: Fecha en formato ISO 8601 (YYYY-MM-DD)
  "comentario": ""        // string: Comentario opcional sobre el movimiento
}
```

### Colección: Pedidos
Esta colección gestiona los pedidos realizados por los clientes o al proveedor.
```json
{
  "num_pedido": 0,          // int: Número identificador del pedido
  "cliente": {
    "nombre": "",           // string: Nombre del cliente
    "email": "",            // string: Correo electrónico del cliente
    "telefono": ""          // string: Teléfono del cliente
  },
  "productos": [
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

## Objetivos
- **Diseñar** una interfaz de usuario atractiva e intuitiva.
- **Implementar** funcionalidades CRUD con conexión a una base de datos MongoDB.
- **Garantizar** la adaptabilidad en dispositivos de escritorio y móviles.
- **Promover** el trabajo colaborativo en un entorno realista.

## Funcionalidades
- Visualización de datos en una lista con opciones de búsqueda y filtrado.
- Operaciones CRUD: Crear, Leer, Actualizar y Eliminar registros.
- Manejo eficiente de conexiones y errores con MongoDB.
- Validación básica de datos (como correos electrónicos y formatos de fecha).

## Requisitos
### Dependencias
- Python 3.10+
- [Flet](https://flet.dev)
- [MongoDB](https://www.mongodb.com/docs)
- [PyMongo](https://pymongo.readthedocs.io/en/stable/)
```bash
  pip install -r .\requirements.txt
```

<!--
project/
│
├── app.py                 # Punto de entrada de la aplicación
├── models/                # Modelos de datos
│   ├── user_model.py      # Ejemplo de modelo de usuario
│   └── ...
├── services/              # Lógica de negocio y acceso a MongoDB
│   ├── mongo_service.py   # Conexión a MongoDB
│   ├── crud_operations.py # Operaciones CRUD
│   └── ...
├── views/                 # Componentes de la interfaz de usuario
│   ├── main_view.py       # Vista principal
│   └── ...
├── utils/                 # Utilidades
│   ├── config.py          # Configuración de MongoDB
│   ├── validators.py      # Validaciones de datos
│   └── ...
├── README.md              # Documentación del proyecto
└── requirements.txt       # Dependencias del proyecto
-->