<!-- Por ChatGPT -->

# Aplicación Multiplataforma con Flet y MongoDB

## Descripción del Proyecto

Este proyecto es una aplicación multiplataforma desarrollada como parte del proyecto ABP (Aprendizaje Basado en Proyectos). Utiliza [Flet](https://flet.dev) para construir la interfaz de usuario y [MongoDB](https://www.mongodb.com/docs) como base de datos documental. La aplicación implementa funcionalidades CRUD (Crear, Leer, Actualizar, Eliminar) para gestionar datos, y está diseñada para resolver una necesidad práctica en un contexto específico.

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
- Librerías adicionales:
```bash
  pip install pymongo
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
└── README.md              # Documentación del proyecto
-->

