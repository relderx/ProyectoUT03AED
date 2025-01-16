import os
import sys
import flet as ft

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.helpers import tabulate_productos
from utils.db import (
    add_producto,
    delete_producto,
    update_producto,
    producto_existe,
    obtener_id_producto,
)
from models.productos import Producto

# Obtiene los datos de los movimientos
def obtener_datos():
    return tabulate_productos()


def producto_view(page: ft.Page):
    page.title = "Gestión de Productos"

    # Variables globales
    page.val_producto = None
    page.val_descripcion = None
    page.val_stock_disponible = None
    page.val_precio_unitario = None
    page.val_categorias = None
    productos_seleccionados_ids = []

    # Obtener datos originales para usar en filtrado
    datos_originales = obtener_datos()

    # Variable global para controlar el orden
    global orden_invertido
    orden_invertido = False

    def aplicar_filtro(e):
        datos_filtrados = obtener_datos()  # Siempre obtener datos actuales
        filtro_seleccionado = filtro_dropdown.value
        texto_busqueda = texto_buscar.value.lower()

        if filtro_seleccionado == "Ningún filtro" or not texto_busqueda:
            # Si no hay filtro o búsqueda, mostrar todos los datos
            tabla.rows.clear()
            tabla.rows.extend(crear_filas(datos_filtrados))
        else:
            # Filtrar los datos según el criterio seleccionado
            indice_columna = encabezados_tabla.index(filtro_seleccionado) - 1
            datos_filtrados = [
                fila
                for fila in datos_filtrados
                if texto_busqueda in str(fila[indice_columna]).lower()
            ]
            tabla.rows.clear()
            tabla.rows.extend(crear_filas(datos_filtrados))
        tabla.update()

   # Aplica el orden seleccionado a los datos de la tabla
    def aplicar_orden(e):
        global orden_invertido
        orden_seleccionado = orden_dropdown.value

        if orden_seleccionado:
            # Obtener los datos actualizados desde la base de datos
            datos_actualizados = obtener_datos()

            indice_columna = encabezados_tabla.index(orden_seleccionado) - 1

            def obtener_valor_ordenacion(fila):
                valor = fila[indice_columna]
                # Si la columna es "Stock Disponible" o "Precio por Unidad", convertir a número
                if encabezados_tabla[indice_columna + 1] in [
                    "Stock Disponible",
                    "Precio por Unidad",
                ]:
                    try:
                        return float(valor)
                    except ValueError:
                        return float("inf")
                return str(valor).lower()

            try:
                # Ordenar los datos basados en la columna seleccionada
                datos_ordenados = sorted(
                    datos_actualizados,
                    key=obtener_valor_ordenacion,
                    reverse=orden_invertido,
                )
                # Actualizar las filas de la tabla
                tabla.rows.clear()
                tabla.rows.extend(crear_filas(datos_ordenados))
                tabla.update()
            except Exception as ex:
                mostrar_notificacion(f"Error al ordenar: {ex}")

    # Alternar el estado del orden
    def alternar_orden(e):
        global orden_invertido
        orden_invertido = not orden_invertido
        aplicar_orden(e)

    # Botón para alternar el orden
    boton_alternar_orden = ft.IconButton(
        icon=ft.Icons.SWAP_VERT,
        tooltip="Invertir Orden",
        on_click=alternar_orden,
    )

    # Alterna entre los temas claro y oscuro
    def toggle_theme():
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()

    # Cambia el valor del producto seleccionado
    def cambio_producto(e):
        page.val_producto = e.control.value
        page.update()

    # Cambia el valor de la descripción
    def cambio_descripcion(e):
        page.val_descripcion = e.control.value
        page.update()

    # Cambia el valor del stock disponible
    def cambio_stock_disponible(e):
        page.val_stock_disponible = e.control.value
        page.update()

    # Cambia el valor del precio unitario
    def cambio_precio_unitario(e):
        page.val_precio_unitario = e.control.value
        page.update()

    # Cambia el valor de las categorías
    def cambio_categorias(e):
        page.val_categorias = e.control.value
        page.update()

    # Cierra el diálogo y limpia las selecciones realizadas
    def cerrar_dialogo(e):
        page.dialog.open = False
        # Deshabilitar el botón "Modificar" después de cerrar el diálogo
        productos_seleccionados_ids.clear()  # Limpia la selección
        boton_modificar.disabled = True
        boton_borrar.disabled = True
        page.update()

    # Muestra una notificación con el mensaje proporcionado
    def mostrar_notificacion(mensaje):
        page.snack_bar = ft.SnackBar(ft.Text(mensaje), bgcolor=ft.colors.GREEN)
        page.snack_bar.open = True
        page.update()

    # Valida e inserta un nuevo producto en la base de datos
    def guardar_insertar(e):
        # Validar si algún campo está vacío o es None
        if not (page.val_producto and page.val_producto.strip()):
            mostrar_notificacion("El campo 'Producto' no puede estar vacío.")
            return
        if not (page.val_descripcion and page.val_descripcion.strip()):
            mostrar_notificacion("El campo 'Descripción' no puede estar vacío.")
            return
        if not (page.val_stock_disponible and page.val_stock_disponible.strip()):
            mostrar_notificacion("El campo 'Stock disponible' no puede estar vacío.")
            return
        if not (page.val_precio_unitario and page.val_precio_unitario.strip()):
            mostrar_notificacion("El campo 'Precio unitario' no puede estar vacío.")
            return
        if not (page.val_categorias and page.val_categorias.strip()):
            mostrar_notificacion("El campo 'Categorías' no puede estar vacío.")
            return

        # Validar que el stock sea un número entero
        try:
            stock_disponible = int(page.val_stock_disponible.strip())
            if stock_disponible < 0:
                mostrar_notificacion(
                    "El campo 'Stock disponible' debe ser un número entero positivo."
                )
                return
        except ValueError:
            mostrar_notificacion(
                "El campo 'Stock disponible' debe ser un número entero válido."
            )
            return

        # Validar que el precio unitario sea un número entero o flotante
        try:
            precio_unitario = float(page.val_precio_unitario.strip())
            if precio_unitario < 0:
                mostrar_notificacion(
                    "El campo 'Precio unitario' debe ser un número positivo."
                )
                return
        except ValueError:
            mostrar_notificacion(
                "El campo 'Precio unitario' debe ser un número válido (entero o flotante)."
            )
            return

        # Verificar si el producto ya existe
        if producto_existe(page.val_producto.strip()):
            mostrar_notificacion("No se puede añadir, el producto ya existe.")
            return

        # Si no existe, continuar con la inserción
        newCategorias = []
        for categoria in page.val_categorias.split(","):
            newCategorias.append(categoria.strip())

        # Añadir el nuevo producto a la base de datos
        add_producto(
            Producto(
                page.val_producto.strip(),
                page.val_descripcion.strip(),
                stock_disponible,
                precio_unitario,
                newCategorias,
            )
        )
        mostrar_notificacion("Producto añadido exitosamente.")

        # Actualizar los datos originales y la tabla
        global datos_originales
        datos_originales = obtener_datos()  # Refleja los nuevos datos
        actualizar_tabla()
        cerrar_dialogo(e)

    # Guarda las modificaciones realizadas a un producto existente
    def guardar_modificar(e):
        if productos_seleccionados_ids:
            producto_id = productos_seleccionados_ids[0]

            # Validar que el producto no exista con el mismo nombre
            if producto_existe(
                page.val_producto.strip()
            ) and producto_id != obtener_id_producto(page.val_producto.strip()):
                mostrar_notificacion(
                    "El nombre del producto ya existe, no se puede modificar."
                )
                return

            # Validar que el stock sea un número entero
            try:
                stock_disponible = int(page.val_stock_disponible.strip())
                if stock_disponible < 0:
                    mostrar_notificacion(
                        "El campo 'Stock disponible' debe ser un número entero positivo."
                    )
                    return
            except ValueError:
                mostrar_notificacion(
                    "El campo 'Stock disponible' debe ser un número entero válido."
                )
                return

            # Validar que el precio unitario sea un número entero o flotante
            try:
                precio_unitario = float(page.val_precio_unitario.strip())
                if precio_unitario < 0:
                    mostrar_notificacion(
                        "El campo 'Precio unitario' debe ser un número positivo."
                    )
                    return
            except ValueError:
                mostrar_notificacion(
                    "El campo 'Precio unitario' debe ser un número válido (entero o flotante)."
                )
                return

            # Actualizar los datos del producto
            updated_data = {
                "producto": page.val_producto.strip(),
                "descripcion": page.val_descripcion.strip(),
                "stock": stock_disponible,
                "precio_unidad": precio_unitario,
                "categoria": [
                    categoria.strip() for categoria in page.val_categorias.split(",")
                ],
            }
            update_producto(producto_id, updated_data)

            # Mostrar notificación de éxito
            mostrar_notificacion("El pedido se modificó correctamente.")
            actualizar_tabla()
            cerrar_dialogo(e)

    # Elimina los productos seleccionados de la base de datos
    def borrar_productos(e):
        for producto_id in productos_seleccionados_ids:
            delete_producto(producto_id)
        actualizar_tabla()
        productos_seleccionados_ids.clear()
        boton_borrar.disabled = True
        boton_modificar.disabled = True
        page.update()

    # Actualiza los datos de la tabla con información reciente
    def actualizar_tabla():
        datos_tabla = obtener_datos()
        tabla.rows.clear()
        tabla.rows.extend(crear_filas(datos_tabla))
        tabla.update()

    # Definición de campos de texto para el formulario de productos
    producto = ft.TextField(
        hint_text="Escribe el nombre del producto",
        hint_style=ft.TextStyle(color="#d8d8d8"),
        label="Producto",
        on_submit=guardar_insertar,
    )
    descripcion = ft.TextField(
        hint_text="Escribe la descripción del producto",
        hint_style=ft.TextStyle(color="#d8d8d8"),
        label="Descripción",
        on_submit=guardar_insertar,
    )
    stock_disponible = ft.TextField(
        hint_text="Escribe el stock del producto",
        hint_style=ft.TextStyle(color="#d8d8d8"),
        helper_text="El valor tiene que ser un número entero",
        label="Stock del producto",
        on_submit=guardar_insertar,
    )
    precio_unitario = ft.TextField(
        hint_text="Escribe el precio del producto por unidad",
        hint_style=ft.TextStyle(color="#d8d8d8"),
        helper_text="El valor puede ser entero o flotante",
        label="Precio unitario",
        on_submit=guardar_insertar,
    )
    categorias = ft.TextField(
        hint_text="Escribe las categorías del producto",
        hint_style=ft.TextStyle(color="#d8d8d8"),
        helper_text="Separa cada categoría con comas y sin espacios",
        label="Categorías del producto",
        on_submit=guardar_insertar,
    )

    # Definición del diálogo de confirmación para eliminar productos
    dialog_borrar = ft.AlertDialog(
        shape=ft.RoundedRectangleBorder(radius=5),
        title=ft.Text("¿Quieres borrar el/los productos seleccionados?"),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),
            ft.ElevatedButton(
                "Sí", on_click=lambda e: [borrar_productos(e), cerrar_dialogo(e)]
            ),
        ],
    )

    # Definición del diálogo para modificar un producto existente
    dialog_modificar = ft.AlertDialog(
        shape=ft.RoundedRectangleBorder(radius=5),
        title=ft.Text("Modificar un Producto"),
        content=ft.Column(
            [producto, descripcion, stock_disponible, precio_unitario, categorias],
            width=650,
            height=650,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),
            ft.ElevatedButton("Guardar", on_click=guardar_modificar),
        ],
    )

    # Muestra el formulario para insertar un nuevo producto
    def mostrar_vent_insertar(e):
        producto.value = ""
        descripcion.value = ""
        stock_disponible.value = ""
        precio_unitario.value = ""
        categorias.value = ""
        producto.on_change = cambio_producto
        descripcion.on_change = cambio_descripcion
        stock_disponible.on_change = cambio_stock_disponible
        precio_unitario.on_change = cambio_precio_unitario
        categorias.on_change = cambio_categorias

        page.dialog = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            title=ft.Text("Insertar un Producto nuevo"),
            content=ft.Column(
                [producto, descripcion, stock_disponible, precio_unitario, categorias]
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialogo),
                ft.ElevatedButton("Guardar", on_click=guardar_insertar),
            ],
        )
        page.dialog.open = True
        page.update()
        producto.focus()

    # Obtiene los datos de un producto dado su ID
    def obtener_datos_producto(producto_id):
        datos = obtener_datos()  # Obtener todos los productos
        for fila in datos:
            if fila[0] == producto_id:  # Suponiendo que el ID es la primera columna
                return {
                    "producto": fila[0],  # Nombre del producto
                    "descripcion": fila[1],  # Descripción
                    "stock_disponible": fila[2],  # Stock disponible
                    "precio_unitario": fila[3],  # Precio por unidad
                    "categorias": fila[4].split(","),  # Categorías separadas por comas
                }
        raise ValueError(f"Producto con ID {producto_id} no encontrado.")

    # Muestra el cuadro de diálogo para modificar un producto seleccionado
    def mostrar_vent_modificar(e):
        global producto_seleccionado_data
        if len(productos_seleccionados_ids) != 1:
            mostrar_notificacion("Selecciona un único producto para modificar.")
            return

        producto_id = productos_seleccionados_ids[0]
        producto_seleccionado_data = next(
            (producto for producto in obtener_datos() if producto[0] == producto_id),
            None,
        )
        if not producto_seleccionado_data:
            mostrar_notificacion("No se encontró el producto seleccionado.")
            return

        # Cargar los datos actuales en las variables
        page.val_producto = producto_seleccionado_data[0]
        page.val_descripcion = producto_seleccionado_data[1]
        page.val_stock_disponible = str(producto_seleccionado_data[2])
        page.val_precio_unitario = str(producto_seleccionado_data[3])
        page.val_categorias = producto_seleccionado_data[4]

        # Crear el cuadro de diálogo para modificar
        dialog_modificar = ft.AlertDialog(
            title=ft.Text("Modificar Producto"),
            content=ft.Column(
                [
                    ft.TextField(
                        label="Nombre del Producto",
                        value=page.val_producto,
                        on_change=lambda e: cambio_producto(e),
                        hint_text="Nombre del producto",
                    ),
                    ft.TextField(
                        label="Descripción",
                        value=page.val_descripcion,
                        on_change=lambda e: cambio_descripcion(e),
                        hint_text="Descripción del producto",
                    ),
                    ft.TextField(
                        label="Stock Disponible",
                        value=page.val_stock_disponible,
                        on_change=lambda e: cambio_stock_disponible(e),
                        hint_text="Cantidad disponible",
                    ),
                    ft.TextField(
                        label="Precio por Unidad",
                        value=page.val_precio_unitario,
                        on_change=lambda e: cambio_precio_unitario(e),
                        hint_text="Precio del producto",
                    ),
                    ft.TextField(
                        label="Categorías",
                        value=page.val_categorias,
                        on_change=lambda e: cambio_categorias(e),
                        hint_text="Categorías separadas por comas",
                    ),
                ]
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialogo),
                ft.ElevatedButton("Guardar", on_click=guardar_modificar),
            ],
        )
        page.dialog = dialog_modificar
        dialog_modificar.open = True
        page.update()

    # Muestra el cuadro de diálogo para confirmar el borrado de productos seleccionados
    def mostrar_vent_borrar(e):
        page.dialog = dialog_borrar
        dialog_borrar.open = True
        page.update()

    # Encabezado de la interfaz de gestión de productos
    encabezado = ft.Row(
        [
            ft.Text(
                "Gestión de Productos",
                size=30,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.RIGHT,
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # Botones de acción: Borrar, Insertar y Modificar
    boton_borrar = ft.ElevatedButton(
        "Borrar", width=100, disabled=True, on_click=mostrar_vent_borrar
    )
    boton_modificar = ft.ElevatedButton(
        "Modificar", width=100, on_click=mostrar_vent_modificar, disabled=True
        )
    botones_inferiores = ft.Row(
        [
            boton_borrar,
            ft.ElevatedButton(
                "Insertar",
                width=120,
                height=40,
                bgcolor="#007BFF",
                color="white",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                icon=ft.Icons.ADD,  # Icono de "Agregar"
                on_click=mostrar_vent_insertar,  # Acción al hacer clic
            ),
            boton_modificar,
        ],
        alignment=ft.MainAxisAlignment.END,  # Alineación a la derecha
    )

    # Gestiona la selección de productos individuales
    def seleccionar_producto(e):
        producto_id = e.control.data
        if e.control.value:
            productos_seleccionados_ids.append(producto_id)
        else:
            productos_seleccionados_ids.remove(producto_id)
        boton_borrar.disabled = len(productos_seleccionados_ids) == 0
        boton_modificar.disabled = len(productos_seleccionados_ids) != 1
        page.update()

    # Gestiona la selección masiva de productos
    def seleccionar_todos(e):
        # Determinar si el checkbox global está marcado o no
        seleccionar = e.control.value
        productos_seleccionados_ids.clear()

        # Actualizar cada fila de la tabla
        for row in tabla.rows:
            checkbox = row.cells[
                0
            ].content  # Primer contenido de la fila es el checkbox
            checkbox.value = seleccionar  # Cambiar el estado del checkbox
            if seleccionar:
                productos_seleccionados_ids.append(
                    checkbox.data
                )  # Agregar ID del producto si está seleccionado

        # Habilitar o deshabilitar los botones según la selección
        boton_borrar.disabled = not productos_seleccionados_ids
        boton_modificar.disabled = len(productos_seleccionados_ids) != 1
        page.update()

    # Encabezados de la tabla de productos
    encabezados_tabla = [
        "Seleccionar",
        "Nombre del Producto",
        "Descripción",
        "Stock Disponible",
        "Precio por Unidad",
        "Categorías",
        "Fecha de Creación",
        "Última Modificación",
    ]

    # Crea filas para la tabla a partir de los datos proporcionados
    def crear_filas(datos):
        filas = []
        for fila in datos:
            producto_id = fila[0]
            # Checkbox para seleccionar productos
            checkbox = ft.Checkbox(
                value=False,
                on_change=seleccionar_producto,
                data=producto_id,  # Asigna el ID del producto al checkbox
            )
            # Crea celdas con los datos del producto
            celdas = [ft.DataCell(checkbox)] + [
                ft.DataCell(ft.Text(str(dato))) for dato in fila
            ]
            filas.append(ft.DataRow(cells=celdas))
        return filas

    # Datos iniciales para la tabla
    datos_tabla = datos_originales

    # Configuración de la tabla de productos
    tabla = ft.DataTable(
        width=1920,
        border_radius=10,
        border=ft.border.all(2, "red"),
        horizontal_lines=ft.BorderSide(2, "blue"),
        vertical_lines=ft.BorderSide(2, "blue"),
        heading_row_height=40,
        columns=[
            # Columna con checkbox global para seleccionar todos los productos
            ft.DataColumn(
                ft.Row(
                    [
                        ft.Checkbox(value=False, on_change=seleccionar_todos),
                    ]
                )
            )
        ]
        + [
            ft.DataColumn(
                ft.Text(
                    encabezado,
                    weight=ft.FontWeight.BOLD,  # Texto en negrita
                    size=14,  # Tamaño del texto
                )
            )
            for encabezado in encabezados_tabla[1:]  # Aplicar a los demás encabezados
        ],
        rows=crear_filas(datos_tabla),  # Filas generadas dinámicamente
    )

    # Campo de texto para búsqueda
    texto_buscar = ft.TextField(label="Buscar", width=200)

    # Dropdown para aplicar filtros
    filtro_dropdown = ft.Dropdown(
        label="Filtrar por",
        options=[ft.dropdown.Option("Ningún filtro")]
        + [ft.dropdown.Option(encabezado) for encabezado in encabezados_tabla[1:]],
        width=200,
        value="Ningún filtro",
    )

    # Botón para aplicar filtro
    boton_aplicar_filtro = ft.ElevatedButton("Aplicar Filtro", on_click=aplicar_filtro)

    # Dropdown para seleccionar criterio de orden
    orden_dropdown = ft.Dropdown(
        label="Ordenar por",
        options=[
            ft.dropdown.Option(encabezado) for encabezado in encabezados_tabla[1:]
        ],
        width=200,
        value="Nombre del Producto",
    )

    # Botón para aplicar orden
    boton_aplicar_orden = ft.ElevatedButton("Ordenar", on_click=aplicar_orden)

    # Sección para búsqueda y filtrado
    buscar_filtro = ft.Row(
        [texto_buscar, filtro_dropdown, boton_aplicar_filtro],
        alignment=ft.MainAxisAlignment.END,
    )

    # Sección para ordenamiento
    ordenar_filtro = ft.Row(
        [orden_dropdown, boton_aplicar_orden, boton_alternar_orden],
        alignment=ft.MainAxisAlignment.END,
    )

    # Retorna la vista principal del inventario
    return ft.View(
        "/inventario",
        [
            ft.AppBar(
                title=ft.Text(
                    "Gestión de Productos",
                    weight=ft.FontWeight.BOLD,
                    size=36,
                ),
                bgcolor=ft.colors.INVERSE_PRIMARY,
                center_title=True,
                leading=ft.IconButton(ft.Icons.HOME, on_click=lambda _: page.go("/")),
                actions=[
                    ft.IconButton(
                        ft.Icons.BRIGHTNESS_6, on_click=lambda _: toggle_theme()
                    ),
                ],
            ),
            ft.Row(
                [
                    ft.Text(
                        "Gestión de Productos",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Insertar",
                        width=120,
                        height=40,
                        bgcolor="#007BFF",
                        color="white",
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                        icon=ft.Icons.ADD,
                        on_click=mostrar_vent_insertar,
                    ),
                    boton_modificar,
                    boton_borrar,
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
            ft.Row(
                [
                    buscar_filtro,
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
            ft.Row(
                [
                    ordenar_filtro,
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
            tabla,
        ],
        scroll=ft.ScrollMode.AUTO,
    )


if __name__ == "__main__":
    ft.app(target=producto_view)
