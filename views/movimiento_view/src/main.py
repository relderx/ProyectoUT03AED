import os
import sys
import flet as ft
# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from tests.add_many_movimientos import movimientos
# from flet import navigation

listMovimientos = []
for movimiento in movimientos:
    listMovimientos.append(movimiento.to_dict())

from utils.helpers import tabulate_movimientos

def main(page: ft.Page):
    page.title = "Movimiento de Inventario"
    page.window_width = 1920
    page.window_height = 1080
    page.bgcolor = ft.colors.WHITE
    page.theme_mode = "light"

    # Encabezado
    encabezado = ft.Row([
        ft.Text("Movimiento de Inventario", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.LEFT),
        ft.Row(
            [
                ft.ElevatedButton("Página Principal", width=150),
                ft.ElevatedButton("Pedidos", width=150)
            ],
            alignment=ft.MainAxisAlignment.END,
            expand=True
        )
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # Botones inferiores
    botones_inferiores = ft.Row([
        ft.ElevatedButton("Borrar", width=100, disabled=True),
        ft.ElevatedButton("Insertar", width=100),
        ft.ElevatedButton("Modificar", width=100, disabled=True),
    ], alignment=ft.MainAxisAlignment.END)

    # Por ahora usar datos ficticios
    encabezados_tabla = ["Producto", "Tipo de Movimiento", "Cantidad", "Fecha", "Comentario"]

# Función para actualizar la tabla según el filtro o búsqueda
    def aplicar_filtro(e):
        filtro_campo = dropdown_filtro.value
        filtro_valor = input_buscar.value.lower()  # Convertir el valor de búsqueda a minúsculas

        tabla.rows.clear()  # Limpiar las filas actuales de la tabla

        for fila in listMovimientos:
            if filtro_campo == "Sin filtro":  # Sin filtro seleccionado
                # Comprobar si el valor de búsqueda está en cualquier columna de la fila
                if any(filtro_valor in str(fila[dato]).lower() for dato in fila):  # Compara sin distinguir mayúsculas/minúsculas
                    tabla.rows.append(ft.DataRow(
                        cells=[ft.DataCell(ft.Text(str(fila[dato]))) for dato in fila]
                    ))
            else:  # Con filtro seleccionado
                indice = encabezados_tabla.index(filtro_campo)
                # Comprobar si el valor de búsqueda está en la columna seleccionada
                if filtro_valor in str(fila[indice]).lower():  # Compara sin distinguir mayúsculas/minúsculas
                    tabla.rows.append(ft.DataRow(
                        cells=[ft.DataCell(ft.Text(str(fila[dato]))) for dato in fila]
                    ))

        tabla.update()  # Actualizar la tabla con los nuevos resultados filtrados


    # Tabla de productos
    tabla = ft.DataTable(
        width=1920,
        border_radius=2,
        border=ft.border.all(2, "red"),
        horizontal_lines=ft.BorderSide(2, "blue"),
        vertical_lines=ft.BorderSide(2, "blue"),
        columns=[ft.DataColumn(ft.Text(encabezado)) for encabezado in encabezados_tabla],
        rows=[
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(fila[dato]))) for dato in fila]
            ) for fila in listMovimientos
        ],
    )

    # Campo de búsqueda con filtro
    dropdown_filtro = ft.Dropdown(
        label="Filtrar por",
        options=[ft.dropdown.Option(text="Sin filtro")] + [ft.dropdown.Option(text=encabezado) for encabezado in encabezados_tabla],
        width=200,
        value="Sin filtro"  # Sin filtro seleccionado por defecto
    )

    input_buscar = ft.TextField(label="Buscar", width=200)
    boton_filtrar = ft.ElevatedButton("Aplicar Filtro", on_click=aplicar_filtro)

    buscar_filtro = ft.Row([
        dropdown_filtro,
        input_buscar,
        boton_filtrar
    ], alignment=ft.MainAxisAlignment.END)

    # Estructura de la página
    page.add(
        encabezado, 
        botones_inferiores,
        ft.Divider(),
        ft.Text("Productos", size=20, weight=ft.FontWeight.BOLD),
        buscar_filtro,
        tabla,
        ft.Divider(),
    )

ft.app(target=main)
