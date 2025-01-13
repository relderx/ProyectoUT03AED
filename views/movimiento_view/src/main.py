import os
import sys
import flet as ft

# Add the project root folder to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils.helpers import tabulate_movimientos
from utils.db import add_movimiento
from models.movimientos import Movimiento

def movimiento_view(page: ft.Page):
    def toggle_theme():
        page.theme_mode = 'dark' if page.theme_mode == 'light' else 'light'
        page.update()

    page.title = "Gestión de Movimientos de Inventario"
    page.scroll = ft.ScrollMode.ALWAYS

    def close_and_open_view(view_path):
        page.window_close()
        os.system(f"flet run {view_path}")

    def update_value(attr, e):
        setattr(page, attr, e.control.value)
        page.update()

    def close_dialog(dialog, *fields):
        dialog.open = False
        for field in fields:
            field.value = None
        page.update()

    def save_movimiento(_):
        add_movimiento(Movimiento(page.val_producto, page.val_tipMovimiento, int(page.val_cantidad), page.val_comentario))
        update_table()
        close_dialog(dialog_insert, producto, tipo_movimiento, cantidad, comentario)

    def update_table():
        datos_tabla = obtener_datos()
        tabla.rows.clear()
        tabla.rows.extend(crear_filas(datos_tabla))
        tabla.update()

    def create_dialog(title, content, actions):
        return ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            title=ft.Text(title),
            content=ft.Column(content, width=page.window.width * 0.33, height=page.window.height * 0.5),
            actions=actions
        )

    producto = ft.TextField(hint_text="Escribe el nombre del producto", label="Producto", on_submit=save_movimiento)
    tipo_movimiento = ft.TextField(hint_text="Escribe el tipo de movimiento", helper_text="Debe ser 'entrada', 'salida' o 'ajuste'", label="Tipo de Movimiento", on_submit=save_movimiento)
    cantidad = ft.TextField(hint_text="Escribe la cantidad del producto", label="Cantidad", on_submit=save_movimiento)
    comentario = ft.TextField(hint_text="Escribe un comentario para el movimiento", label="Comentario", on_submit=save_movimiento)

    dialog_insert = create_dialog(
        "Inserta un Movimiento nuevo",
        [producto, tipo_movimiento, cantidad, comentario],
        [ft.TextButton("Cancelar", on_click=lambda _: close_dialog(dialog_insert, producto, tipo_movimiento, cantidad, comentario)),
         ft.ElevatedButton("Guardar", on_click=save_movimiento)]
    )

    def show_dialog(dialog):
        page.dialog = dialog
        page.dialog.open = True
        page.update()
        producto.focus()

    encabezado = ft.Row([
        ft.Text("Movimiento de Inventario", size=30, weight=ft.FontWeight.BOLD),
        ft.Row([
            ft.ElevatedButton("Productos", width=150, on_click=lambda _: close_and_open_view(".\\views\\producto_view\\src")),
            ft.ElevatedButton("Pedidos", width=150, on_click=lambda _: close_and_open_view(".\\views\\pedido_view\\src"))
        ], alignment=ft.MainAxisAlignment.END, expand=True)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    botones_inferiores = ft.Row([
        ft.ElevatedButton("Borrar", width=100, disabled=True),
        ft.ElevatedButton("Insertar", width=100, on_click=lambda _: show_dialog(dialog_insert)),
        ft.ElevatedButton("Modificar", width=100, disabled=True)
    ], alignment=ft.MainAxisAlignment.END)

    encabezados_tabla = ["Producto", "Tipo de Movimiento", "Cantidad", "Fecha", "Comentario"]

    def obtener_datos():
        return tabulate_movimientos()

    def crear_filas(datos):
        return [ft.DataRow(cells=[ft.DataCell(ft.Text(str(dato))) for dato in fila]) for fila in datos]

    tabla = ft.DataTable(
        width=1920,
        border_radius=2,
        border=ft.border.all(2, "red"),
        horizontal_lines=ft.BorderSide(2, "blue"),
        vertical_lines=ft.BorderSide(2, "blue"),
        columns=[ft.DataColumn(ft.Text(encabezado)) for encabezado in encabezados_tabla],
        rows=crear_filas(obtener_datos())
    )

    tabla_con_scroll = ft.Column(
        controls=[tabla],
        height=500,
        scroll=ft.ScrollMode.AUTO
    )

    dropdown_filtro = ft.Dropdown(
        label="Filtrar por",
        options=[ft.dropdown.Option("Ningún filtro")] + [ft.dropdown.Option(encabezado) for encabezado in encabezados_tabla],
        width=200,
        value="Ningún filtro"
    )

    input_buscar = ft.TextField(label="Buscar", width=200)

    def aplicar_filtro(_=None):
        datos = obtener_datos()
        filtro = dropdown_filtro.value
        texto = input_buscar.value.lower()
        tabla.rows.clear()

        if texto:
            if filtro == "Ningún filtro":
                datos_filtrados = [fila for fila in datos if any(texto in str(campo).lower() for campo in fila)]
            else:
                campo_indices = {"Producto": 0, "Tipo de Movimiento": 1, "Cantidad": 2, "Fecha": 3, "Comentario": 4}
                indice = campo_indices.get(filtro, None)
                if indice is not None:
                    datos_filtrados = [fila for fila in datos if texto in str(fila[indice]).lower()]
        else:
            datos_filtrados = datos

        tabla.rows.extend(crear_filas(datos_filtrados))
        tabla.update()

    def ordenar_tabla(_):
        columna_ordenar = dropdown_ordenar.value
        indice_columna = encabezados_tabla.index(columna_ordenar)
        datos_ordenados = sorted(obtener_datos(), key=lambda x: str(x[indice_columna]).lower())
        tabla.rows.clear()
        tabla.rows.extend(crear_filas(datos_ordenados))
        tabla.update()

    dropdown_ordenar = ft.Dropdown(
        label='Ordenar por',
        options=[ft.dropdown.Option(text=encabezado) for encabezado in encabezados_tabla],
        width=200,
        value=encabezados_tabla[0]
    )
    boton_ordenar = ft.ElevatedButton('Ordenar', on_click=ordenar_tabla)

    input_buscar.on_submit = aplicar_filtro
    boton_filtrar = ft.ElevatedButton("Aplicar Filtro", on_click=aplicar_filtro)

    buscar_filtro = ft.Row([input_buscar, dropdown_filtro, boton_filtrar], alignment=ft.MainAxisAlignment.END)
    ordenar_filtro = ft.Row([dropdown_ordenar, boton_ordenar], alignment=ft.MainAxisAlignment.END)

    return ft.View(
        "/movimientos",
        [
            ft.AppBar(
                title=ft.Text("Movimientos de Inventario", weight=ft.FontWeight.BOLD, size=36),
                bgcolor=ft.Colors.INVERSE_PRIMARY,
                center_title=True,
                leading=ft.IconButton(ft.Icons.HOME, on_click=lambda _: page.go("/")),
                actions=[ft.IconButton(ft.Icons.BRIGHTNESS_6, on_click=lambda _: toggle_theme())]
            ),
            ft.Container(
                content=ft.Column(
                    [
                        encabezado,
                        botones_inferiores,
                        ft.Divider(),
                        ft.Text("Movimientos", size=30, weight=ft.FontWeight.BOLD),
                        buscar_filtro,
                        ordenar_filtro,
                        tabla_con_scroll,
                        ft.Divider()
                    ],
                    scroll=ft.ScrollMode.AUTO
                ),
                expand=True
            )
        ]
    )
