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

## **Estructura BBDD**

### Tabla Productos
**PK**: Nombre

**Atributos**: Nombre, Descripción, Cantidad, FK_Categoría, Fecha de creación, Fecha de última creación

### Tabla Categoría
**PK**: Nombre de Categoría

**Atributos**: Nombre de Categoría

### Tabla SubProductos
**PK**: FK_ID-Producto, ID-Subproducto

**Atributos**: FK_ID-Producto, ID-Subproducto, Fecha creación


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