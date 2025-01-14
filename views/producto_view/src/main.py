import os
import sys
import flet as ft
from utils.helpers import tabulate_productos
from utils.db import add_producto, delete_producto
from models.productos import Producto

def producto_view(page: ft.Page):
    page.title = "Gestión de Productos"

    # Variables globales
    page.val_producto = None
    page.val_descripcion = None
    page.val_stock_disponible = None
    page.val_precio_unitario = None
    page.val_categorias = None
    productos_seleccionados_ids = []

    def toggle_theme():
        page.theme_mode = 'dark' if page.theme_mode == 'light' else 'light'
        page.update()

    def cambio_producto(e):
        page.val_producto = e.control.value
        page.update()

    def cambio_descripcion(e):
        page.val_descripcion = e.control.value
        page.update()

    def cambio_stock_disponible(e):
        page.val_stock_disponible = e.control.value
        page.update()

    def cambio_precio_unitario(e):
        page.val_precio_unitario = e.control.value
        page.update()

    def cambio_categorias(e):
        page.val_categorias = e.control.value
        page.update()

    def cerrar_dialogo(e):
        page.dialog.open = False
        page.update()

    def guardar_insertar(e):
        print(page.val_producto)
        newCategorias = []
        for categoria in page.val_categorias.split(","):
            newCategorias.append(categoria.strip())
        add_producto(Producto(page.val_producto, page.val_descripcion, int(page.val_stock_disponible), int(page.val_precio_unitario), newCategorias))
        actualizar_tabla()
        cerrar_dialogo(e)

    def guardar_modificar(e):
        # Aquí implementa la lógica para modificar un producto existente.
        cerrar_dialogo(e)

    def borrar_productos(e):
        # Borrar los productos seleccionados
        for producto_id in productos_seleccionados_ids:
            delete_producto(producto_id)  # Elimina por ID
        actualizar_tabla()
        # Limpia los productos seleccionados y habilita/deshabilita botones
        productos_seleccionados_ids.clear()
        boton_borrar.disabled = True
        boton_modificar.disabled = True  # Asegurarse de que "Modificar" esté deshabilitado
        page.update()

    def obtener_datos():
        return tabulate_productos()

    def actualizar_tabla():
        datos_tabla = obtener_datos()
        tabla.rows.clear()
        tabla.rows.extend(crear_filas(datos_tabla))
        tabla.update()

    producto = ft.TextField(hint_text="Escribe el nombre del producto", hint_style=ft.TextStyle(color="#d8d8d8"), label="Producto", on_submit=guardar_insertar)
    descripcion = ft.TextField(hint_text="Escribe la descripción del producto", hint_style=ft.TextStyle(color="#d8d8d8"), label="Descripción", on_submit=guardar_insertar)
    stock_disponible = ft.TextField(hint_text="Escribe el stock del producto", hint_style=ft.TextStyle(color="#d8d8d8"), helper_text="El valor tiene que ser un número entero", label="Stock del producto", on_submit=guardar_insertar)
    precio_unitario = ft.TextField(hint_text="Escribe el precio del producto por unidad", hint_style=ft.TextStyle(color="#d8d8d8"), helper_text="El valor puede ser entero o flotante", label="Precio unitario", on_submit=guardar_insertar)
    categorias = ft.TextField(hint_text="Escribe las categorías del producto", hint_style=ft.TextStyle(color="#d8d8d8"), helper_text="Separa cada categoría con comas y sin espacios", label="Categorías del producto", on_submit=guardar_insertar)

    dialog_borrar = ft.AlertDialog(
        shape=ft.RoundedRectangleBorder(radius=5),
        title=ft.Text("¿Quieres borrar el/los productos seleccionados?"),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),
            ft.ElevatedButton("Sí", on_click=lambda e: [borrar_productos(e), cerrar_dialogo(e)])
        ],
    )

    dialog_modificar = ft.AlertDialog(
        shape=ft.RoundedRectangleBorder(radius=5),
        title=ft.Text("Modificar un Producto"),
        content=ft.Column([
            producto,
            descripcion,
            stock_disponible,
            precio_unitario,
            categorias
        ], width=650, height=650),
        actions=[
            ft.TextButton("Cancelar", on_click=cerrar_dialogo),
            ft.ElevatedButton("Guardar", on_click=guardar_modificar)
        ],
    )

    # def mostrar_vent_insertar(e):
    #     producto.on_change = cambio_producto
    #     descripcion.on_change = cambio_descripcion
    #     stock_disponible.on_change = cambio_stock_disponible
    #     precio_unitario.on_change = cambio_precio_unitario
    #     categorias.on_change = cambio_categorias

    def mostrar_vent_insertar(e):
        # Resetea los valores de los inputs antes de abrir el diálogo
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
        

    # Configura el diálogo
        page.dialog = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            title=ft.Text("Insertar un Producto nuevo"),
            content=ft.Column([
                producto,
                descripcion,
                stock_disponible,
                precio_unitario,
                categorias
            ], width=650, height=650),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialogo),
                ft.ElevatedButton("Guardar", on_click=guardar_insertar)
            ],
        )
        # Abre el diálogo
        page.dialog.open = True
        page.update()
        producto.focus()

    def mostrar_vent_modificar(e):
        producto.on_change = cambio_producto
        descripcion.on_change = cambio_descripcion
        stock_disponible.on_change = cambio_stock_disponible
        precio_unitario.on_change = cambio_precio_unitario
        categorias.on_change = cambio_categorias

        page.dialog = dialog_modificar
        dialog_modificar.open = True
        page.update()

    def mostrar_vent_borrar(e):
        page.dialog = dialog_borrar
        dialog_borrar.open = True
        page.update()

    encabezado = ft.Row([
        ft.Text("Gestión de Productos", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.LEFT)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    boton_borrar = ft.ElevatedButton("Borrar", width=100, disabled=True, on_click=mostrar_vent_borrar)
    boton_modificar = ft.ElevatedButton("Modificar", width=100, on_click=mostrar_vent_modificar, disabled=True)
    botones_inferiores = ft.Row([
        boton_borrar,
        ft.ElevatedButton("Insertar", width=100, on_click=mostrar_vent_insertar),
        boton_modificar
    ], alignment=ft.MainAxisAlignment.END)

    encabezados_tabla = [
        "Seleccionar",
        "Nombre del Producto",
        "Descripción",
        "Stock Disponible",
        "Precio por Unidad",
        "Categorías",
        "Fecha de Creación",
        "Última Modificación"
    ]

    def seleccionar_producto(e):
        producto_id = e.control.data
        if e.control.value:
            productos_seleccionados_ids.append(producto_id)
        else:
            productos_seleccionados_ids.remove(producto_id)
        boton_borrar.disabled = len(productos_seleccionados_ids) == 0
        boton_modificar.disabled = len(productos_seleccionados_ids) != 1
        page.update()

    def crear_filas(datos):
        filas = []
        for fila in datos:
            producto_id = fila[0]
            checkbox = ft.Checkbox(value=False, on_change=seleccionar_producto, data=producto_id)
            celdas = [ft.DataCell(checkbox)] + [ft.DataCell(ft.Text(str(dato))) for dato in fila]
            filas.append(ft.DataRow(cells=celdas))
        return filas

    datos_tabla = obtener_datos()

    tabla = ft.DataTable(
        width=1920,
        border_radius=2,
        border=ft.border.all(2, "red"),
        horizontal_lines=ft.BorderSide(2, "blue"),
        vertical_lines=ft.BorderSide(2, "blue"),
        columns=[ft.DataColumn(ft.Text(encabezado)) for encabezado in encabezados_tabla],
        rows=crear_filas(datos_tabla),
    )

    buscar_filtro = ft.Row([
        ft.TextField(label="Buscar", width=200),
        ft.Dropdown(
            label="Filtrar por",
            options=[ft.dropdown.Option("Ningún filtro")] + [
                ft.dropdown.Option("Nombre del Producto"),
                ft.dropdown.Option("Descripción"),
                ft.dropdown.Option("Stock Disponible"),
                ft.dropdown.Option("Precio por Unidad"),
                ft.dropdown.Option("Categorías")
            ],
            width=200,
            value="Ningún filtro"
        ),
        ft.ElevatedButton("Aplicar Filtro")
    ], alignment=ft.MainAxisAlignment.END)

    ordenar_filtro = ft.Row([
        ft.Dropdown(
            label='Ordenar por',
            options=[
                ft.dropdown.Option("Nombre del Producto"),
                ft.dropdown.Option("Descripción"),
                ft.dropdown.Option("Stock Disponible"),
                ft.dropdown.Option("Precio por Unidad"),
                ft.dropdown.Option("Categorías")
            ],
            width=200,
            value="Nombre del Producto"
        ),
        ft.ElevatedButton('Ordenar')
    ], alignment=ft.MainAxisAlignment.END)

    return ft.View(
        "/inventario",
        [
            ft.AppBar(
                title=ft.Text("Gestión de Productos", weight=ft.FontWeight.BOLD, size=36),
                bgcolor=ft.Colors.INVERSE_PRIMARY,
                center_title=True,
                leading=ft.IconButton(ft.Icons.HOME, on_click=lambda _: page.go("/")),
                actions=[
                    ft.IconButton(ft.Icons.BRIGHTNESS_6, on_click=toggle_theme),
                ],
            ),
            encabezado,
            botones_inferiores,
            ft.Divider(),
            buscar_filtro,
            ordenar_filtro,
            tabla,
            ft.Divider()
        ],
        scroll=ft.ScrollMode.AUTO
    )

if __name__ == "__main__":
    ft.app(target=producto_view)
