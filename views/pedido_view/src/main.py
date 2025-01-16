import os
import sys
import flet as ft

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from utils.helpers import tabulate_pedidos
from utils.db import add_pedido, delete_pedido, update_pedido
from models.pedidos import Pedido


def obtener_datos():
    return tabulate_pedidos()


def pedido_view(page: ft.Page):
    page.title = "Gestión de Pedidos"

    # Variables globales
    page.val_pedido = None
    page.val_nombreCliente = None
    page.val_emailCliente = None
    page.val_telefonoCliente = None
    page.val_productos = None
    page.val_estado = None
    pedidos_seleccionados_ids = []

    # Obtener datos originales para usar en filtrado
    datos_originales = obtener_datos()

    # Aplica un filtro a los datos en función de la selección y el texto de búsqueda
    def aplicar_filtro():
        filtro_seleccionado = filtro_dropdown.value
        texto_busqueda = texto_buscar.value.lower()

        # Si no se selecciona filtro o el texto de búsqueda está vacío, mostrar los datos originales
        if filtro_seleccionado == "Ningún filtro" or not texto_busqueda:
            datos_filtrados = datos_originales
        else:
            indice_columna = encabezados_tabla.index(filtro_seleccionado) - 1
            datos_filtrados = [
                fila
                for fila in datos_originales
                if texto_busqueda in str(fila[indice_columna]).lower()
            ]

        # Actualizar la tabla con los datos filtrados
        tabla.rows.clear()
        tabla.rows.extend(crear_filas(datos_filtrados))
        tabla.update()

    # Aplica un orden a los datos de la tabla en función de la columna seleccionada
    def aplicar_orden(e):
        orden_seleccionado = orden_dropdown.value
        if orden_seleccionado:
            indice_columna = encabezados_tabla.index(orden_seleccionado) - 1
            datos_ordenados = sorted(
                datos_originales,
                key=lambda x: float(x[indice_columna])
                if str(x[indice_columna]).replace(".", "", 1).isdigit()
                else str(x[indice_columna]).lower(),
            )
            # Actualizar la tabla con los datos ordenados
            tabla.rows.clear()
            tabla.rows.extend(crear_filas(datos_ordenados))
            tabla.update()

    # Alterna entre los temas claro y oscuro
    def toggle_theme():
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        page.update()

    # Funciones para manejar los cambios en los campos del formulario de pedidos
    def cambio_pedido(e):
        page.val_pedido = e.control.value
        page.update()

    def cambio_nombreCliente(e):
        page.val_nombreCliente = e.control.value
        page.update()

    def cambio_emailCliente(e):
        page.val_emailCliente = e.control.value
        page.update()

    def cambio_telefonoCliente(e):
        page.val_telefonoCliente = e.control.value
        page.update()

    def cambio_productos(e):
        page.val_productos = e.control.value
        page.update()

    def cambio_estado(e):
        page.val_estado = e.control.value
        page.update()

    # Cierra el cuadro de diálogo y restablece el estado de los botones y la selección
    def cerrar_dialogo(e=None):
        if page.dialog:
            page.dialog.open = False  # Cierra el diálogo
            page.dialog = None  # Limpia la referencia al diálogo
            pedidos_seleccionados_ids.clear()  # Limpia la selección
            boton_modificar.disabled = True
            boton_borrar.disabled = True
            page.update()

    # Muestra una notificación en la barra inferior
    def mostrar_notificacion(mensaje):
        page.snack_bar = ft.SnackBar(ft.Text(mensaje), bgcolor=ft.colors.GREEN)
        page.snack_bar.open = True
        page.update()

    # Guarda un nuevo pedido en la base de datos tras realizar las validaciones necesarias
    def guardar_insertar(e):
        try:
            # Validar que todos los campos sean obligatorios
            if (
                not pedido.value.strip()
                or not nombreCliente.value.strip()
                or not emailCliente.value.strip()
                or not telefonoCliente.value.strip()
                or not productos.value.strip()
                or not estado.value
            ):
                mostrar_notificacion("Todos los campos son obligatorios.")
                return

            # Validar formato del email
            if (
                "@" not in emailCliente.value.strip()
                or "." not in emailCliente.value.strip()
            ):
                mostrar_notificacion("El formato del email no es válido.")
                return

            # Validar formato del teléfono
            if (
                not telefonoCliente.value.strip().isdigit()
                or len(telefonoCliente.value.strip()) < 7
                or len(telefonoCliente.value.strip()) > 15
            ):
                mostrar_notificacion(
                    "El teléfono debe contener solo números y tener entre 7 y 15 dígitos."
                )
                return

            # Validar formato de los productos ingresados
            try:
                products = []
                for producto in productos.value.split(","):
                    elemento = producto.split(" x ")
                    if len(elemento) != 3:
                        mostrar_notificacion(
                            "Formato de productos incorrecto. Usa: 'nombre x unidades x precio'."
                        )
                        return
                    products.append(
                        {
                            "producto": elemento[0].strip(),
                            "unidades": int(elemento[1].strip()),
                            "precio_unidad": float(elemento[2].strip()),
                        }
                    )
            except ValueError:
                mostrar_notificacion(
                    "Las unidades y el precio deben ser números válidos."
                )
                return

            # Procesar datos del cliente
            cliente = {
                "nombre": nombreCliente.value.strip(),
                "email": emailCliente.value.strip(),
                "telefono": telefonoCliente.value.strip(),
            }

            # Crear un nuevo pedido
            nuevo_pedido = Pedido(
                num_pedido=pedido.value.strip(),
                cliente=cliente,
                productos=products,
                estado=estado.value.strip(),
            )

            # Insertar el pedido en la base de datos
            add_pedido(nuevo_pedido)
            actualizar_tabla()  # Actualizar la tabla con los nuevos datos
            cerrar_dialogo()  # Cerrar el cuadro de diálogo
            mostrar_notificacion("Pedido insertado correctamente.")
        except Exception as ex:
            # Mostrar error si ocurre algún problema
            mostrar_notificacion(f"Error al insertar el pedido: {ex}")

    # Guarda los cambios realizados en un pedido existente
    def guardar_modificar(e):
        if pedidos_seleccionados_ids:
            try:
                # Obtener el ID del pedido seleccionado
                pedido_id = pedidos_seleccionados_ids[0]

                # Validar que todos los campos sean obligatorios
                if (
                    not pedido.value.strip()
                    or not nombreCliente.value.strip()
                    or not emailCliente.value.strip()
                    or not telefonoCliente.value.strip()
                    or not productos.value.strip()
                    or not estado.value
                ):
                    mostrar_notificacion("Todos los campos son obligatorios.")
                    return

                # Validar formato del email
                if (
                    "@" not in emailCliente.value.strip()
                    or "." not in emailCliente.value.strip()
                ):
                    mostrar_notificacion("El formato del email no es válido.")
                    return

                # Validar formato del teléfono
                if (
                    not telefonoCliente.value.strip().isdigit()
                    or len(telefonoCliente.value.strip()) < 7
                    or len(telefonoCliente.value.strip()) > 15
                ):
                    mostrar_notificacion(
                        "El teléfono debe contener solo números y tener entre 7 y 15 dígitos."
                    )
                    return

                # Validar formato de productos
                try:
                    products = []
                    for producto in productos.value.split(","):
                        elemento = producto.split(" x ")
                        if len(elemento) != 3:
                            mostrar_notificacion(
                                "Formato de productos incorrecto. Usa: 'nombre x unidades x precio'."
                            )
                            return
                        products.append(
                            {
                                "producto": elemento[0].strip(),
                                "unidades": int(elemento[1].strip()),
                                "precio_unidad": float(elemento[2].strip()),
                            }
                        )
                except ValueError:
                    mostrar_notificacion(
                        "Las unidades y el precio deben ser números válidos."
                    )
                    return

                # Procesar datos del cliente
                cliente = {
                    "nombre": nombreCliente.value.strip(),
                    "email": emailCliente.value.strip(),
                    "telefono": telefonoCliente.value.strip(),
                }

                # Preparar datos actualizados para el pedido
                datos_actualizados = {
                    "num_pedido": pedido.value.strip(),
                    "cliente": cliente,
                    "productos": products,
                    "estado": estado.value.strip(),
                }

                # Actualizar el pedido en la base de datos
                update_pedido(pedido_id, datos_actualizados)

                # Refrescar la tabla y cerrar el diálogo
                actualizar_tabla()
                cerrar_dialogo()
                mostrar_notificacion("Pedido modificado correctamente.")
            except Exception as ex:
                mostrar_notificacion(f"Error al modificar el pedido: {ex}")

    # Abre el cuadro de diálogo para modificar un pedido seleccionado
    def mostrar_dialogo_modificar(e):
        if len(pedidos_seleccionados_ids) != 1:
            mostrar_notificacion("Selecciona un único pedido para modificar.")
            return

        # Obtener los datos del pedido seleccionado
        pedido_id = pedidos_seleccionados_ids[0]
        pedido_seleccionado = next(
            (fila for fila in datos_originales if fila[0] == pedido_id), None
        )

        if not pedido_seleccionado:
            mostrar_notificacion("No se encontró el pedido seleccionado.")
            return

        # Cargar los datos del pedido en los campos del formulario
        pedido.value = pedido_seleccionado[0]
        nombreCliente.value = pedido_seleccionado[1]
        emailCliente.value = pedido_seleccionado[2]
        telefonoCliente.value = pedido_seleccionado[3]
        productos.value = pedido_seleccionado[4]
        estado.value = pedido_seleccionado[6]

        # Abrir el cuadro de diálogo para modificar
        page.dialog = dialog_modificar
        page.dialog.open = True
        page.update()

    # Abre el cuadro de diálogo para confirmar la eliminación de pedidos seleccionados
    def abrir_dialogo_borrar(e):
        page.dialog = dialog_borrar
        page.dialog.open = True
        page.update()

    # Elimina los pedidos seleccionados de la base de datos
    def borrar_pedidos(e):
        try:
            for pedido_id in pedidos_seleccionados_ids:
                delete_pedido(pedido_id)
            actualizar_tabla()
            pedidos_seleccionados_ids.clear()
            boton_borrar.disabled = True
            boton_modificar.disabled = True
            page.update()
            cerrar_dialogo()
            mostrar_notificacion("Pedido(s) borrado(s) correctamente.")
        except Exception as ex:
            mostrar_notificacion(f"Error al borrar pedido(s): {ex}")

    # Actualiza los datos mostrados en la tabla
    def actualizar_tabla():
        datos_tabla = obtener_datos()
        tabla.rows.clear()
        tabla.rows.extend(crear_filas(datos_tabla))
        tabla.update()

    # Define los campos del formulario para pedidos
    pedido = ft.TextField(hint_text="Escribe el ID del pedido", label="Pedido")
    nombreCliente = ft.TextField(
        hint_text="Escribe el nombre del cliente", label="Cliente"
    )
    emailCliente = ft.TextField(hint_text="Escribe el email del cliente", label="Email")
    telefonoCliente = ft.TextField(
        hint_text="Escribe el teléfono del cliente", label="Teléfono"
    )
    productos = ft.TextField(
        hint_text="Escribe los productos",
        helper_text="Introduce los productos de la siguiente manera: nom_pro x unid x pre_unid,otro_pro...",
        label="Productos",
    )
    estado = ft.Dropdown(
        hint_text="Selecciona el estado",
        label="Estado",
        options=[
            ft.dropdown.Option("pendiente"),
            ft.dropdown.Option("enviado"),
            ft.dropdown.Option("entregado"),
            ft.dropdown.Option("cancelado"),
        ],
    )

    # Botones para acciones principales: borrar y modificar pedidos
    boton_borrar = ft.ElevatedButton(
        "Borrar", width=100, disabled=True, on_click=abrir_dialogo_borrar
    )
    boton_modificar = ft.ElevatedButton(
        "Modificar", width=100, on_click=mostrar_dialogo_modificar, disabled=True
    )

    # Cuadro de diálogo para confirmación de borrado
    dialog_borrar = ft.AlertDialog(
        shape=ft.RoundedRectangleBorder(radius=5),
        title=ft.Text("¿Quieres borrar los pedidos seleccionados?"),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),  # Evento para cancelar
            ft.ElevatedButton("Sí", on_click=borrar_pedidos),
        ],
    )

    # Cuadro de diálogo para modificar un pedido
    dialog_modificar = ft.AlertDialog(
        shape=ft.RoundedRectangleBorder(radius=5),
        title=ft.Text("Modificar Pedido"),
        content=ft.Column(
            [pedido, nombreCliente, emailCliente, telefonoCliente, productos, estado],
            width=650,
            height=650,
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),  # Evento para cancelar
            ft.ElevatedButton("Guardar", on_click=guardar_modificar),
        ],
    )

    # Muestra el cuadro de diálogo para insertar un nuevo pedido
    def mostrar_vent_insertar(e):
        pedido.value = ""
        nombreCliente.value = ""
        emailCliente.value = ""
        telefonoCliente.value = ""
        productos.value = ""
        estado.value = None

        pedido.on_change = cambio_pedido
        nombreCliente.on_change = cambio_nombreCliente
        emailCliente.on_change = cambio_emailCliente
        telefonoCliente.on_change = cambio_telefonoCliente
        productos.on_change = cambio_productos
        estado.on_change = cambio_estado

        page.dialog = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            title=ft.Text("Insertar un Pedido nuevo"),
            content=ft.Column(
                [
                    pedido,
                    nombreCliente,
                    emailCliente,
                    telefonoCliente,
                    productos,
                    estado,
                ],
                width=650,
                height=650,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialogo),  # Evento para cancelar
                ft.ElevatedButton("Guardar", on_click=guardar_insertar),
            ],
        )
        page.dialog.open = True
        page.update()
        pedido.focus()

    # Gestiona la selección de pedidos en la tabla
    def seleccionar_pedido(e):
        pedido_id = e.control.data
        if e.control.value:
            pedidos_seleccionados_ids.append(pedido_id)
        else:
            pedidos_seleccionados_ids.remove(pedido_id)
        # Habilitar o deshabilitar botones según la selección
        boton_borrar.disabled = len(pedidos_seleccionados_ids) == 0
        boton_modificar.disabled = len(pedidos_seleccionados_ids) != 1
        page.update()

    # Selecciona o deselecciona todos los pedidos en la tabla
    def seleccionar_todos(e):
        # Determinar si el checkbox global está marcado o no
        seleccionar = e.control.value
        pedidos_seleccionados_ids.clear()

        # Actualizar cada fila de la tabla
        for row in tabla.rows:
            checkbox = row.cells[
                0
            ].content  # El primer contenido de la fila es el checkbox
            checkbox.value = seleccionar  # Cambiar el estado del checkbox
            if seleccionar:
                pedidos_seleccionados_ids.append(
                    checkbox.data
                )  # Agregar ID del pedido si está seleccionado

        # Habilitar o deshabilitar los botones según la selección
        boton_borrar.disabled = not pedidos_seleccionados_ids
        boton_modificar.disabled = len(pedidos_seleccionados_ids) != 1
        page.update()

    # Encabezados de la tabla de pedidos
    encabezados_tabla = [
        "Seleccionar",
        "ID Pedido",
        "Cliente",
        "Email",
        "Teléfono",
        "Productos",
        "Precio Total",
        "Estado",
        "Fecha de Creación",
        "Última Modificación",
    ]

    # Crea las filas de la tabla a partir de los datos proporcionados
    def crear_filas(datos):
        filas = []
        for fila in datos:
            pedido_id = fila[0]
            # Checkbox para seleccionar pedidos
            checkbox = ft.Checkbox(
                value=False, on_change=seleccionar_pedido, data=pedido_id
            )
            # Crea las celdas con el checkbox y los datos del pedido
            celdas = [ft.DataCell(checkbox)] + [
                ft.DataCell(ft.Text(str(dato))) for dato in fila
            ]
            filas.append(ft.DataRow(cells=celdas))
        return filas

    # Datos iniciales para la tabla
    datos_tabla = datos_originales

    # Configuración de la tabla de pedidos
    tabla = ft.DataTable(
        width=1920,
        border_radius=2,
        border=ft.border.all(2, "#1e88e5"),
        horizontal_lines=ft.BorderSide(2, "#1e88e5"),
        vertical_lines=ft.BorderSide(2, "#1e88e5"),
        columns=[
            # Columna con checkbox global para seleccionar todos los pedidos
            ft.DataColumn(
                ft.Row(
                    [
                        ft.Text("Check Todos"),
                        ft.Checkbox(value=False, on_change=seleccionar_todos),
                    ]
                )
            )
        ]
        + [
            ft.DataColumn(ft.Text(encabezado)) for encabezado in encabezados_tabla[1:]
        ],  # Columnas de la tabla
        rows=crear_filas(datos_tabla),  # Filas generadas dinámicamente
    )

    # Campo de texto para búsqueda
    texto_buscar = ft.TextField(label="Buscar", width=200)

    # Dropdown para seleccionar el criterio de filtrado
    filtro_dropdown = ft.Dropdown(
        label="Filtrar por",
        options=[ft.dropdown.Option("Ningún filtro")]
        + [ft.dropdown.Option(encabezado) for encabezado in encabezados_tabla[1:]],
        width=200,
        value="Ningún filtro",
    )

    # Botón para aplicar el filtro seleccionado
    boton_aplicar_filtro = ft.ElevatedButton("Aplicar Filtro", on_click=aplicar_filtro)

    # Dropdown para seleccionar el criterio de ordenamiento
    orden_dropdown = ft.Dropdown(
        label="Ordenar por",
        options=[
            ft.dropdown.Option(encabezado) for encabezado in encabezados_tabla[1:]
        ],
        width=200,
        value="ID Pedido",
    )

    # Botón para aplicar el orden seleccionado
    boton_aplicar_orden = ft.ElevatedButton("Ordenar", on_click=aplicar_orden)

    # Fila que contiene los elementos de búsqueda y filtrado
    buscar_filtro = ft.Row(
        [texto_buscar, filtro_dropdown, boton_aplicar_filtro],
        alignment=ft.MainAxisAlignment.END,
    )

    # Fila que contiene los elementos para ordenar
    ordenar_filtro = ft.Row(
        [orden_dropdown, boton_aplicar_orden], alignment=ft.MainAxisAlignment.END
    )

    return ft.View(
        "/pedidos",
        [
            ft.AppBar(
                title=ft.Text("Gestión de Pedidos", weight=ft.FontWeight.BOLD, size=36),
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
                        "Gestión de Pedidos",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.RIGHT,
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            # Fila para botones principales
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
            buscar_filtro,
            ordenar_filtro,
            tabla,
        ],
        scroll=ft.ScrollMode.AUTO,
    )


if __name__ == "__main__":
    ft.app(target=pedido_view)
