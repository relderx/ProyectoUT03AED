import os
import sys
import flet as ft

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils.helpers import tabulate_movimientos
from utils.db import add_movimiento, delete_movimiento, update_movimiento
from models.movimientos import Movimiento

def obtener_datos():
    return tabulate_movimientos()

def movimiento_view(page: ft.Page):
    page.title = "Gestión de Movimientos"

    # Variables globales
    page.val_producto = None
    page.val_tipo_movimiento = None
    page.val_cantidad = None
    page.val_comentario = None
    movimientos_seleccionados_ids = []

    # Obtener datos originales para usar en filtrado
    datos_originales = obtener_datos()

    def aplicar_filtro(e):
        filtro_seleccionado = filtro_dropdown.value
        texto_busqueda = texto_buscar.value.lower()

        if filtro_seleccionado == "Ningún filtro" or not texto_busqueda:
            datos_filtrados = datos_originales
        else:
            indice_columna = encabezados_tabla.index(filtro_seleccionado) - 1
            datos_filtrados = [
                fila for fila in datos_originales
                if texto_busqueda in str(fila[indice_columna]).lower()
            ]

        tabla.rows.clear()
        tabla.rows.extend(crear_filas(datos_filtrados))
        tabla.update()

    def aplicar_orden(e):
        orden_seleccionado = orden_dropdown.value
        if orden_seleccionado:
            indice_columna = encabezados_tabla.index(orden_seleccionado) - 1
            datos_ordenados = sorted(
                datos_originales,
                key=lambda x: float(x[indice_columna]) if str(x[indice_columna]).replace('.', '', 1).isdigit() else str(x[indice_columna]).lower()
            )
            tabla.rows.clear()
            tabla.rows.extend(crear_filas(datos_ordenados))
            tabla.update()

    def toggle_theme():
        page.theme_mode = 'dark' if page.theme_mode == 'light' else 'light'
        page.update()

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

    def cerrar_dialogo(e):
        page.dialog.open = False
        movimientos_seleccionados_ids.clear()
        boton_modificar.disabled = True
        boton_borrar.disabled = True
        page.update()

    def mostrar_notificacion(mensaje):
        page.snack_bar = ft.SnackBar(ft.Text(mensaje), bgcolor=ft.colors.GREEN)
        page.snack_bar.open = True
        page.update()

    def guardar_insertar(e):
        nuevo_movimiento = Movimiento(
            producto=producto.value.strip(),
            tipo_movimiento=tipo_movimiento.value.strip(),
            cantidad=int(cantidad.value.strip()),
            comentario=comentario.value.strip(),
        )

        add_movimiento(nuevo_movimiento)
        actualizar_tabla()
        cerrar_dialogo(e)
        mostrar_notificacion("Movimiento insertado correctamente.")

    def guardar_modificar(e):
        if movimientos_seleccionados_ids:
            movimiento_id = movimientos_seleccionados_ids[0]
            datos_actualizados = {
                "producto": producto.value,
                "tipo_movimiento": tipo_movimiento.value,
                "cantidad": int(cantidad.value),
                "comentario": comentario.value,
            }

            update_movimiento(movimiento_id, datos_actualizados)
            actualizar_tabla()
            cerrar_dialogo(e)

    def mostrar_vent_modificar(e):
        if len(movimientos_seleccionados_ids) != 1:
            mostrar_notificacion("Selecciona un único movimiento para modificar.")
            return

        movimiento_id = movimientos_seleccionados_ids[0]
        movimiento_seleccionado = next(
            (movimiento for movimiento in obtener_datos() if movimiento[0] == movimiento_id), None
        )

        if not movimiento_seleccionado:
            mostrar_notificacion("No se encontró el movimiento seleccionado.")
            return

        producto.value = movimiento_seleccionado[0]  # Producto
        tipo_movimiento.value = movimiento_seleccionado[1]  # Tipo de movimiento
        cantidad.value = str(movimiento_seleccionado[2])  # Cantidad
        comentario.value = movimiento_seleccionado[5] if len(movimiento_seleccionado) > 5 else ""  # Comentario

        page.dialog = dialog_modificar
        dialog_modificar.open = True
        page.update()

    def borrar_movimientos(e):
        for movimiento_id in movimientos_seleccionados_ids:
            delete_movimiento(movimiento_id)
        actualizar_tabla()
        movimientos_seleccionados_ids.clear()
        boton_borrar.disabled = True
        boton_modificar.disabled = True
        page.update()

    def actualizar_tabla():
        datos_tabla = obtener_datos()
        tabla.rows.clear()
        tabla.rows.extend(crear_filas(datos_tabla))
        tabla.update()

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

    dialog_borrar = ft.AlertDialog(
        shape=ft.RoundedRectangleBorder(radius=5),
        title=ft.Text("¿Quieres borrar los movimientos seleccionados?"),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),
            ft.ElevatedButton("Sí", on_click=lambda e: [borrar_movimientos(e), cerrar_dialogo(e)])
        ],
    )

    dialog_modificar = ft.AlertDialog(
        shape=ft.RoundedRectangleBorder(radius=5),
        title=ft.Text("Modificar Movimiento"),
        content=ft.Column([
            producto,
            tipo_movimiento,
            cantidad,
            comentario
        ]),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),
            ft.ElevatedButton("Guardar", on_click=guardar_modificar)
        ],
    )

    def abrir_dialogo_borrar(e):
        page.dialog = dialog_borrar
        dialog_borrar.open = True
        page.update()

    boton_borrar = ft.ElevatedButton("Borrar", width=100, disabled=True, on_click=abrir_dialogo_borrar)
    boton_modificar = ft.ElevatedButton("Modificar", width=100, on_click=mostrar_vent_modificar, disabled=True)

    def mostrar_vent_insertar(e):
        producto.value = ""
        tipo_movimiento.value = None
        cantidad.value = ""
        comentario.value = ""

        page.dialog = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            title=ft.Text("Insertar un Movimiento"),
            content=ft.Column([producto, tipo_movimiento, cantidad, comentario]),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialogo),
                ft.ElevatedButton("Guardar", on_click=guardar_insertar)
            ],
        )
        page.dialog.open = True
        page.update()
        producto.focus()

    def seleccionar_movimiento(e):
        movimiento_id = e.control.data
        if e.control.value:
            movimientos_seleccionados_ids.append(movimiento_id)
        else:
            movimientos_seleccionados_ids.remove(movimiento_id)
        boton_borrar.disabled = len(movimientos_seleccionados_ids) == 0
        boton_modificar.disabled = len(movimientos_seleccionados_ids) != 1
        page.update()

    encabezados_tabla = [
        "Seleccionar",
        "Producto",
        "Tipo de Movimiento",
        "Cantidad",
        "Fecha",
        "Comentario"
    ]

    def crear_filas(datos):
        filas = []
        for fila in datos:
            movimiento_id = fila[0]
            checkbox = ft.Checkbox(value=False, on_change=seleccionar_movimiento, data=movimiento_id)
            celdas = [ft.DataCell(checkbox)] + [ft.DataCell(ft.Text(str(dato))) for dato in fila]
            filas.append(ft.DataRow(cells=celdas))
        return filas

    datos_tabla = datos_originales

    tabla = ft.DataTable(
        width=1920,
        border_radius=2,
        border=ft.border.all(2, "red"),  # Color de borde rojo
        horizontal_lines=ft.BorderSide(2, "blue"),  # Líneas horizontales azules
        vertical_lines=ft.BorderSide(2, "blue"),  # Líneas verticales azules
        columns=[ft.DataColumn(ft.Text(encabezado)) for encabezado in encabezados_tabla],
        rows=crear_filas(datos_tabla),
    )

    texto_buscar = ft.TextField(label="Buscar", width=200)
    filtro_dropdown = ft.Dropdown(
        label="Filtrar por",
        options=[ft.dropdown.Option("Ningún filtro")] + [
            ft.dropdown.Option(encabezado) for encabezado in encabezados_tabla[1:]
        ],
        width=200,
        value="Ningún filtro"
    )
    boton_aplicar_filtro = ft.ElevatedButton("Aplicar Filtro", on_click=aplicar_filtro)

    orden_dropdown = ft.Dropdown(
        label="Ordenar por",
        options=[
            ft.dropdown.Option(encabezado) for encabezado in encabezados_tabla[1:]
        ],
        width=200,
        value="Producto"
    )
    boton_aplicar_orden = ft.ElevatedButton("Ordenar", on_click=aplicar_orden)

    buscar_filtro = ft.Row([
        texto_buscar,
        filtro_dropdown,
        boton_aplicar_filtro
    ])

    ordenar_filtro = ft.Row([
        orden_dropdown,
        boton_aplicar_orden
    ])

    return ft.View(
        "/movimientos",
        [
            ft.AppBar(
                title=ft.Text("Gestión de Movimientos", weight=ft.FontWeight.BOLD, size=36),
                bgcolor=ft.colors.INVERSE_PRIMARY,  # Color azul oscuro
                center_title=True,
                leading=ft.IconButton(ft.Icons.HOME, on_click=lambda _: page.go("/")),  # Botón de inicio
                actions=[
                    ft.IconButton(ft.Icons.BRIGHTNESS_6, on_click=lambda _: toggle_theme()),
                ],
            ),
            ft.Row(
                [
                    ft.Text("Gestión de Movimientos", size=30, weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.END
            ),
            ft.Row(
                [
                    boton_borrar,
                    ft.ElevatedButton("Insertar", width=100, on_click=mostrar_vent_insertar),
                    boton_modificar,
                ],
                alignment=ft.MainAxisAlignment.END
            ),
            ft.Row(
                [
                    buscar_filtro,
                ],
                alignment=ft.MainAxisAlignment.END
            ),
            ft.Row(
                [
                    ordenar_filtro,
                ],
                alignment=ft.MainAxisAlignment.END
            ),
            tabla,
        ],
        scroll=ft.ScrollMode.AUTO
    )


if __name__ == "__main__":
    ft.app(target=movimiento_view)
