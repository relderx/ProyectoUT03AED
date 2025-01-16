import os
import sys
import flet as ft

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from utils.helpers import tabulate_movimientos
from utils.db import (
    add_movimiento,
    delete_movimiento,
    update_movimiento,
    movimiento_existe,
    obtener_id_movimiento,
)
from models.movimientos import Movimiento

# Obtiene los datos de los movimientos
def obtener_datos():
    return tabulate_movimientos()  # Obtiene los datos tabulados de movimientos

# Configuración inicial de la vista de movimientos
def movimiento_view(page: ft.Page):
    page.title = "Gestión de Movimientos"

    # Variables globales para el estado de la página
    page.val_producto = None
    page.val_tipo_movimiento = None
    page.val_cantidad = None
    page.val_comentario = None
    movimientos_seleccionados_ids = []  # Lista de movimientos seleccionados

    # Obtener los datos originales para usar en la tabla y filtros
    datos_originales = obtener_datos()

    # Variable para controlar el orden ascendente o descendente
    global orden_invertido
    orden_invertido = False

    # Aplica un filtro a los datos en función de los criterios seleccionados
    def aplicar_filtro(e):
        filtro_seleccionado = filtro_dropdown.value
        texto_busqueda = texto_buscar.value.lower()

        # Mostrar todos los datos si no hay filtro o búsqueda
        if filtro_seleccionado == "Ningún filtro" or not texto_busqueda:
            datos_filtrados = datos_originales
        else:
            # Filtrar por la columna seleccionada
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

    # Aplica un orden a los datos en la tabla
    def aplicar_orden(e):
        global orden_invertido
        orden_seleccionado = orden_dropdown.value
        if orden_seleccionado:
            indice_columna = encabezados_tabla.index(orden_seleccionado) - 1

            def obtener_valor_ordenacion(fila):
                valor = fila[indice_columna]
                if str(valor).replace(".", "", 1).isdigit():
                    return float(valor)
                return str(valor).lower()

            datos_ordenados = sorted(
                datos_originales,
                key=obtener_valor_ordenacion,
                reverse=orden_invertido,
            )
            tabla.rows.clear()
            tabla.rows.extend(crear_filas(datos_ordenados))
            tabla.update()

    # Alterna el estado del orden entre ascendente y descendente
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

    # Funciones para manejar los cambios en los campos del formulario
    def cambio_producto(e):
        page.val_producto = e.control.value
        page.update()

    def cambio_tipo_movimiento(e):
        page.val_tipo_movimiento = e.control.value
        page.update()

    def cambio_cantidad(e):
        page.val_cantidad = e.control.value
        page.update()

    def cambio_comentario(e):
        page.val_comentario = e.control.value
        page.update()

    # Cierra el cuadro de diálogo y restablece los botones y selecciones
    def cerrar_dialogo(e):
        page.dialog.open = False
        movimientos_seleccionados_ids.clear()
        boton_modificar.disabled = True
        boton_borrar.disabled = True
        page.update()

    # Muestra una notificación en la barra inferior
    def mostrar_notificacion(mensaje):
        page.snack_bar = ft.SnackBar(ft.Text(mensaje), bgcolor=ft.colors.GREEN)
        page.snack_bar.open = True
        page.update()

    # Guarda un nuevo movimiento tras validar los datos
    def guardar_insertar(e):
        # Validar campos obligatorios
        if not (producto.value and producto.value.strip()):
            mostrar_notificacion("El campo 'Producto' no puede estar vacío.")
            return
        if not (tipo_movimiento.value and tipo_movimiento.value.strip()):
            mostrar_notificacion("El campo 'Tipo de Movimiento' no puede estar vacío.")
            return
        if not (cantidad.value and cantidad.value.strip()):
            mostrar_notificacion("El campo 'Cantidad' no puede estar vacío.")
            return

        # Validar que la cantidad sea un número entero positivo
        try:
            cantidad_valor = int(cantidad.value.strip())
            if cantidad_valor <= 0:
                mostrar_notificacion(
                    "El campo 'Cantidad' debe ser un número entero positivo."
                )
                return
        except ValueError:
            mostrar_notificacion(
                "El campo 'Cantidad' debe ser un número entero válido."
            )
            return

        # Validar si ya existe un movimiento para el producto
        if movimiento_existe(producto.value.strip()):
            mostrar_notificacion(
                "No se puede añadir, ya existe un movimiento para este producto."
            )
            return

        # Crear un nuevo movimiento
        nuevo_movimiento = Movimiento(
            producto=producto.value.strip(),
            tipo_movimiento=tipo_movimiento.value.strip(),
            cantidad=cantidad_valor,
            comentario=comentario.value.strip(),
        )
        # Guardar en la base de datos
        add_movimiento(nuevo_movimiento)
        mostrar_notificacion("Movimiento añadido exitosamente.")
        actualizar_tabla()
        cerrar_dialogo(e)

    # Modifica un movimiento existente tras validar los datos
    def guardar_modificar(e):
        if movimientos_seleccionados_ids:
            movimiento_id = movimientos_seleccionados_ids[0]

            # Validar campos obligatorios
            if not (producto.value and producto.value.strip()):
                mostrar_notificacion("El campo 'Producto' no puede estar vacío.")
                return
            if not (tipo_movimiento.value and tipo_movimiento.value.strip()):
                mostrar_notificacion(
                    "El campo 'Tipo de Movimiento' no puede estar vacío."
                )
                return
            if not (cantidad.value and cantidad.value.strip()):
                mostrar_notificacion("El campo 'Cantidad' no puede estar vacío.")
                return

            # Validar que la cantidad sea un número entero positivo
            try:
                cantidad_valor = int(cantidad.value.strip())
                if cantidad_valor <= 0:
                    mostrar_notificacion(
                        "El campo 'Cantidad' debe ser un número entero positivo."
                    )
                    return
            except ValueError:
                mostrar_notificacion(
                    "El campo 'Cantidad' debe ser un número entero válido."
                )
                return

            # Validar que no exista un duplicado
            if movimiento_existe(
                producto.value.strip()
            ) and movimiento_id != obtener_id_movimiento(producto.value.strip()):
                mostrar_notificacion(
                    "No se puede modificar, ya existe un movimiento con este producto."
                )
                return

            # Actualizar los datos del movimiento
            datos_actualizados = {
                "producto": producto.value.strip(),
                "tipo_movimiento": tipo_movimiento.value.strip(),
                "cantidad": cantidad_valor,
                "comentario": comentario.value.strip(),
            }
            update_movimiento(movimiento_id, datos_actualizados)

            mostrar_notificacion("El movimiento se modificó correctamente.")
            actualizar_tabla()
            cerrar_dialogo(e)

    # Muestra el cuadro de diálogo para modificar un movimiento seleccionado
    def mostrar_vent_modificar(e):
        if len(movimientos_seleccionados_ids) != 1:
            mostrar_notificacion("Selecciona un único movimiento para modificar.")
            return

        # Obtener los datos del movimiento seleccionado
        movimiento_id = movimientos_seleccionados_ids[0]
        movimiento_seleccionado = next(
            (
                movimiento
                for movimiento in obtener_datos()
                if movimiento[0] == movimiento_id
            ),
            None,
        )

        if not movimiento_seleccionado:
            mostrar_notificacion("No se encontró el movimiento seleccionado.")
            return

        # Cargar los datos del movimiento en los campos del formulario
        producto.value = movimiento_seleccionado[0]
        tipo_movimiento.value = movimiento_seleccionado[1]
        cantidad.value = str(movimiento_seleccionado[2])
        comentario.value = (
            movimiento_seleccionado[5] if len(movimiento_seleccionado) > 5 else ""
        )

        # Abrir el cuadro de diálogo para modificar
        page.dialog = dialog_modificar
        dialog_modificar.open = True
        page.update()

    # Elimina los movimientos seleccionados
    def borrar_movimientos(e):
        for movimiento_id in movimientos_seleccionados_ids:
            delete_movimiento(
                movimiento_id
            )  # Llama a la función para borrar el movimiento
        actualizar_tabla()  # Refresca la tabla después de eliminar
        movimientos_seleccionados_ids.clear()  # Limpia la lista de seleccionados
        boton_borrar.disabled = True
        boton_modificar.disabled = True
        page.update()

    # Actualiza los datos de la tabla con la información más reciente
    def actualizar_tabla():
        datos_tabla = obtener_datos()  # Obtiene los datos más recientes
        tabla.rows.clear()  # Limpia las filas de la tabla
        tabla.rows.extend(
            crear_filas(datos_tabla)
        )  # Crea nuevas filas con los datos actualizados
        tabla.update()

    # Definición de campos del formulario para movimientos
    producto = ft.TextField(hint_text="Escribe el producto", label="Producto")
    tipo_movimiento = ft.Dropdown(
        hint_text="Selecciona el tipo de movimiento",
        label="Tipo de Movimiento",
        options=[
            ft.dropdown.Option("entrada"),
            ft.dropdown.Option("salida"),
            ft.dropdown.Option("ajuste"),
        ],
    )
    cantidad = ft.TextField(hint_text="Escribe la cantidad", label="Cantidad")
    comentario = ft.TextField(hint_text="Escribe un comentario", label="Comentario")

    # Cuadro de diálogo para confirmar la eliminación de movimientos
    dialog_borrar = ft.AlertDialog(
        shape=ft.RoundedRectangleBorder(radius=5),
        title=ft.Text("¿Quieres borrar los movimientos seleccionados?"),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),
            ft.ElevatedButton(
                "Sí", on_click=lambda e: [borrar_movimientos(e), cerrar_dialogo(e)]
            ),
        ],
    )

    # Cuadro de diálogo para modificar un movimiento existente
    dialog_modificar = ft.AlertDialog(
        shape=ft.RoundedRectangleBorder(radius=5),
        title=ft.Text("Modificar Movimiento"),
        content=ft.Column([producto, tipo_movimiento, cantidad, comentario]),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),
            ft.ElevatedButton("Guardar", on_click=guardar_modificar),
        ],
    )

    # Abre el cuadro de diálogo para confirmar eliminación
    def abrir_dialogo_borrar(e):
        page.dialog = dialog_borrar
        dialog_borrar.open = True
        page.update()

    # Botones de acción: borrar y modificar
    boton_borrar = ft.ElevatedButton(
        "Borrar", width=100, disabled=True, on_click=abrir_dialogo_borrar
    )
    boton_modificar = ft.ElevatedButton(
        "Modificar", width=100, on_click=mostrar_vent_modificar, disabled=True
    )

    # Muestra el formulario para insertar un nuevo movimiento
    def mostrar_vent_insertar(e):
        # Restablece los valores de los campos
        producto.value = ""
        tipo_movimiento.value = None
        cantidad.value = ""
        comentario.value = ""

        # Configuración del cuadro de diálogo
        page.dialog = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            title=ft.Text("Insertar un Movimiento"),
            content=ft.Column([producto, tipo_movimiento, cantidad, comentario]),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialogo),
                ft.ElevatedButton("Guardar", on_click=guardar_insertar),
            ],
        )
        page.dialog.open = True
        page.update()
        producto.focus()

    # Selecciona o deselecciona un movimiento en la tabla
    def seleccionar_movimiento(e):
        movimiento_id = e.control.data
        if e.control.value:
            movimientos_seleccionados_ids.append(
                movimiento_id
            )  # Agrega el ID a la lista
        else:
            movimientos_seleccionados_ids.remove(
                movimiento_id
            )  # Elimina el ID de la lista
        # Habilita o deshabilita botones según la selección
        boton_borrar.disabled = len(movimientos_seleccionados_ids) == 0
        boton_modificar.disabled = len(movimientos_seleccionados_ids) != 1
        page.update()

    # Selecciona o deselecciona todos los movimientos
    def seleccionar_todos(e):
        # Determina si el checkbox global está marcado o no
        seleccionar = e.control.value
        movimientos_seleccionados_ids.clear()

        # Actualiza cada fila de la tabla
        for row in tabla.rows:
            checkbox = row.cells[
                0
            ].content  # Primer contenido de la fila es el checkbox
            checkbox.value = seleccionar  # Cambia el estado del checkbox
            if seleccionar:
                movimientos_seleccionados_ids.append(
                    checkbox.data
                )  # Agrega ID del movimiento si está seleccionado

        # Habilita o deshabilita los botones según la selección
        boton_borrar.disabled = not movimientos_seleccionados_ids
        boton_modificar.disabled = len(movimientos_seleccionados_ids) != 1
        page.update()

    # Encabezados de la tabla
    encabezados_tabla = [
        "Seleccionar",
        "Producto",
        "Tipo de Movimiento",
        "Cantidad",
        "Fecha",
        "Comentario",
    ]

    # Crea las filas de la tabla a partir de los datos
    def crear_filas(datos):
        filas = []
        for fila in datos:
            movimiento_id = fila[0]
            # Checkbox para seleccionar movimientos
            checkbox = ft.Checkbox(
                value=False,
                on_change=seleccionar_movimiento,
                data=movimiento_id,  # Asigna el ID del movimiento al checkbox
            )
            # Crea las celdas con los datos del movimiento
            celdas = [ft.DataCell(checkbox)] + [
                ft.DataCell(ft.Text(str(dato))) for dato in fila
            ]
            filas.append(ft.DataRow(cells=celdas))
        return filas

    # Datos iniciales para la tabla
    datos_tabla = datos_originales

    # Configuración de la tabla
    tabla = ft.DataTable(
        width=1920,
        border_radius=10,  # Mismo borde redondeado que la otra tabla
        border=ft.border.all(2, "red"),  # Color de borde rojo
        horizontal_lines=ft.BorderSide(2, "blue"),  # Líneas horizontales azules
        vertical_lines=ft.BorderSide(2, "blue"),  # Líneas verticales azules
        heading_row_height=40,  # Altura de los encabezados
        columns=[
            # Columna con checkbox global para seleccionar todos los movimientos
            ft.DataColumn(
                ft.Row(
                    [
                        ft.Text(
                            "Check Todos",
                            weight=ft.FontWeight.BOLD,  # Texto en negrita
                            size=14,  # Tamaño del texto para encabezado
                        ),
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

    # Elementos para búsqueda y filtrado
    texto_buscar = ft.TextField(label="Buscar", width=200)
    filtro_dropdown = ft.Dropdown(
        label="Filtrar por",
        options=[ft.dropdown.Option("Ningún filtro")]
        + [ft.dropdown.Option(encabezado) for encabezado in encabezados_tabla[1:]],
        width=200,
        value="Ningún filtro",
    )
    boton_aplicar_filtro = ft.ElevatedButton("Aplicar Filtro", on_click=aplicar_filtro)

    # Elementos para ordenamiento
    orden_dropdown = ft.Dropdown(
        label="Ordenar por",
        options=[
            ft.dropdown.Option(encabezado) for encabezado in encabezados_tabla[1:]
        ],
        width=200,
        value="Producto",
    )
    boton_aplicar_orden = ft.ElevatedButton("Ordenar", on_click=aplicar_orden)

    # Fila para búsqueda y filtrado
    buscar_filtro = ft.Row([texto_buscar, filtro_dropdown, boton_aplicar_filtro])

    # Fila para ordenamiento
    ordenar_filtro = ft.Row([orden_dropdown, boton_aplicar_orden])

    return ft.View(
        "/movimientos",
        [
            ft.AppBar(
                title=ft.Text(
                    "Gestión de Movimientos",
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
                        "Gestión de Movimientos",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
            ft.Row(
                [
                    boton_borrar,
                    ft.ElevatedButton(
                        "Insertar", width=100, on_click=mostrar_vent_insertar
                    ),
                    boton_modificar,
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
                    orden_dropdown,
                    boton_aplicar_orden,
                    boton_alternar_orden,  # Botón para invertir el orden
                ],
                alignment=ft.MainAxisAlignment.END,
            ),
            tabla,
        ],
        scroll=ft.ScrollMode.AUTO,
    )

if __name__ == "__main__":
    ft.app(target=movimiento_view)
