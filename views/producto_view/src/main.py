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

    def cerrar_producto(e):
        page.dialog.open = False
        page.update()

    def guardar_insertar(e):
        add_producto(Producto(
            page.val_producto,
            page.val_descripcion,
            int(page.val_stock_disponible),
            float(page.val_precio_unitario),
            [categoria.strip() for categoria in page.val_categorias.split(",")]
        ))
        actualizar_tabla()
        cerrar_producto(e)

    def borrar_productos(e):
        for producto_id in productos_seleccionados_ids:
            delete_producto(producto_id)  # Pasa solo el ID
        actualizar_tabla()
        productos_seleccionados_ids.clear()
        boton_borrar.disabled = True
        page.update()

    def obtener_datos():
        return tabulate_productos()

    def actualizar_tabla():
        datos_tabla = obtener_datos()
        tabla.rows.clear()
        tabla.rows.extend(crear_filas(datos_tabla))
        tabla.update()
        
        page.dialog.open = False
        
        producto.value = None
        descripcion.value = None
        stock_disponible.value = None
        precio_unitario.value = None
        categorias.value = None
        page.update()

    def cerrar_borrar(e):
        page.dialog.open = False

    def guardar_borrar(e):
        page.dialog.open = False

    def cerrar_modificar(e):
        page.dialog.open = False

    def guardar_modificar(e):
        page.dialog.open = False
    
    producto = ft.TextField(hint_text="Escribe el nombre del producto", hint_style=ft.TextStyle(color="#d8d8d8"),label="Producto", on_submit=guardar_insertar)
    descripcion = ft.TextField(hint_text="Escribe la descripción del producto", hint_style=ft.TextStyle(color="#d8d8d8"),label="Descripción", on_submit=guardar_insertar)
    stock_disponible = ft.TextField(hint_text="Escribe el stock del producto", hint_style=ft.TextStyle(color="#d8d8d8"), helper_text="El valor tiene que ser un número entero",label="Stock del producto", on_submit=guardar_insertar)
    precio_unitario = ft.TextField(hint_text="Escribe el precio del producto por unidad", hint_style=ft.TextStyle(color="#d8d8d8"), helper_text="El valor puede ser entero o flotante",label="Precio unitario", on_submit=guardar_insertar)
    categorias = ft.TextField(hint_text="Escribe las categorías del producto", hint_style=ft.TextStyle(color="#d8d8d8"), helper_text="Separa cada categoría comas y sin espacios",label="Categorías del producto", on_submit=guardar_insertar)
    
    dialogBor = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            title=ft.Text("¿Quieres borrar el/los productos?"),
            content=ft.Column([ 
                producto,
                descripcion,
                stock_disponible,
                precio_unitario,
                categorias
            ], width=page.window.width*0.33, height=page.window.height*0.5),
            actions=[ 
                ft.TextButton("Si", on_click=cerrar_borrar),
                ft.ElevatedButton("No", on_click=guardar_borrar)
            ],
    )
    dialogMod = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            title=ft.Text("Modificar un Producto"),
            content=ft.Column([ 
                producto,
                descripcion,
                stock_disponible,
                precio_unitario,
                categorias
            ], width=page.window.width*0.33, height=page.window.height*0.5),
            actions=[ 
                ft.TextButton("Cancelar", on_click=cerrar_modificar),
                ft.ElevatedButton("Guardar", on_click=guardar_modificar)
            ],
    )
    
    def mostrar_vent_insertar(e):
        producto = ft.TextField(hint_text="Escribe el nombre del producto", hint_style=ft.TextStyle(color="#d8d8d8"), label="Producto", on_submit=guardar_insertar)
        descripcion = ft.TextField(hint_text="Escribe la descripción del producto", hint_style=ft.TextStyle(color="#d8d8d8"), label="Descripción", on_submit=guardar_insertar)
        stock_disponible = ft.TextField(hint_text="Escribe el stock del producto", hint_style=ft.TextStyle(color="#d8d8d8"), label="Stock del producto", on_submit=guardar_insertar)
        precio_unitario = ft.TextField(hint_text="Escribe el precio del producto por unidad", hint_style=ft.TextStyle(color="#d8d8d8"), label="Precio unitario", on_submit=guardar_insertar)
        categorias = ft.TextField(hint_text="Escribe las categorías del producto", hint_style=ft.TextStyle(color="#d8d8d8"), helper_text="Separa cada categoría comas y sin espacios", label="Categorías del producto", on_submit=guardar_insertar)
        
        producto.on_change = cambio_producto
        descripcion.on_change = cambio_descripcion
        stock_disponible.on_change = cambio_stock_disponible
        precio_unitario.on_change = cambio_precio_unitario
        categorias.on_change = cambio_categorias
        
        dialogInser = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            title=ft.Text("Insertar un Producto nuevo"),
            content=ft.Column(
                [
                    producto,
                    descripcion,
                    stock_disponible,
                    precio_unitario,
                    categorias
                ],
                # width=page.window.width * 0.33,
                # height=page.window.height * 0.5
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_producto),
                ft.ElevatedButton("Guardar", on_click=guardar_insertar)
            ],
        )
        
        page.dialog = dialogInser
        dialogInser.open = True
        page.update()
        producto.focus()
    
    def mostrar_vent_borrar(e):
        page.dialog = dialogBor
        page.dialog.open = True
        page.update()
        producto.focus()
    
    def mostrar_vent_modificar(e):
        page.dialog = dialogMod
        page.dialog.open = True
        page.update()
        producto.focus()

    encabezado = ft.Row([ 
        ft.Text("Gestión de Productos", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.LEFT)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    botones_inferiores = ft.Row([ 
        ft.ElevatedButton("Borrar", width=100, disabled=True, on_click=mostrar_vent_borrar),
        ft.ElevatedButton("Insertar", width=100, on_click=mostrar_vent_insertar),
        ft.ElevatedButton("Modificar", width=100, disabled=True, on_click=mostrar_vent_modificar),
    ], alignment=ft.MainAxisAlignment.END)

    # Encabezados de la tabla
    encabezados_tabla = [
        "Seleccionar",  # Nueva columna para los checkboxes
        "Nombre del Producto", 
        "Descripción", 
        "Stock Disponible", 
        "Precio por Unidad", 
        "Categorías", 
        "Fecha de Creación", 
        "Última Modificación"
    ]

    productos_seleccionados = []

    def seleccionar_producto(e):
        producto_id = e.control.data  # Recibe el ID del producto directamente del checkbox
        if e.control.value:
            productos_seleccionados_ids.append(producto_id)
        else:
            productos_seleccionados_ids.remove(producto_id)
        boton_borrar.disabled = len(productos_seleccionados_ids) == 0
        page.update()

    def crear_filas(datos):
        filas = []
        for fila in datos:
            producto_id = fila[0]  # Asume que el ID del producto está en la primera columna
            checkbox = ft.Checkbox(value=False, on_change=seleccionar_producto, data=producto_id)
            celdas = [ft.DataCell(checkbox)] + [ft.DataCell(ft.Text(str(dato))) for dato in fila]
            filas.append(ft.DataRow(cells=celdas))
        return filas

    datos_tabla = obtener_datos()

    encabezado = ft.Row([
        ft.Text("Gestión de Productos", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.LEFT),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    boton_borrar = ft.ElevatedButton("Borrar", width=100, disabled=True, on_click=borrar_productos)

    botones_inferiores = ft.Row([
        boton_borrar,
        ft.ElevatedButton("Insertar", width=100, on_click=lambda _: mostrar_vent_insertar()),
        ft.ElevatedButton("Modificar", width=100, disabled=True, on_click=lambda _: None),
    ], alignment=ft.MainAxisAlignment.END)

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Seleccionar")),
            ft.DataColumn(ft.Text("Nombre del Producto")),
            ft.DataColumn(ft.Text("Descripción")),
            ft.DataColumn(ft.Text("Stock Disponible")),
            ft.DataColumn(ft.Text("Precio por Unidad")),
            ft.DataColumn(ft.Text("Categorías")),
            ft.DataColumn(ft.Text("Fecha de Creación")),
            ft.DataColumn(ft.Text("Última Modificación")),
        ],
        rows=crear_filas(datos_tabla),
    )

    def mostrar_vent_insertar():
        dialog_insertar = ft.AlertDialog(
            title=ft.Text("Insertar Producto"),
            content=ft.Column([
                ft.TextField(label="Producto", on_change=cambio_producto),
                ft.TextField(label="Descripción", on_change=cambio_descripcion),
                ft.TextField(label="Stock", on_change=cambio_stock_disponible),
                ft.TextField(label="Precio", on_change=cambio_precio_unitario),
                ft.TextField(label="Categorías", on_change=cambio_categorias),
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_producto),
                ft.ElevatedButton("Guardar", on_click=guardar_insertar)
            ],
        )
        page.dialog = dialog_insertar
        dialog_insertar.open = True
        page.update()

    input_buscar = ft.TextField(label="Buscar", width=200)
    dropdown_filtro = ft.Dropdown(
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
    )

    def aplicar_filtro(e=None):
        datos = obtener_datos()
        filtro = dropdown_filtro.value
        texto = input_buscar.value.lower()

        tabla.rows.clear()

        if texto:
            if filtro == "Ningún filtro":
                datos_filtrados = [
                    fila for fila in datos if any(texto in str(campo).lower() for campo in fila)
                ]
            else:
                campo_indices = {
                    "Nombre del Producto": 1,
                    "Descripción": 2,
                    "Stock Disponible": 3,
                    "Precio por Unidad": 4,
                    "Categorías": 5
                }
                indice = campo_indices.get(filtro)
                datos_filtrados = [
                    fila for fila in datos if texto in str(fila[indice]).lower()
                ]
        else:
            datos_filtrados = datos

        tabla.rows.extend(crear_filas(datos_filtrados))
        tabla.update()

    boton_filtrar = ft.ElevatedButton("Aplicar Filtro", on_click=aplicar_filtro)

    buscar_filtro = ft.Row([
        input_buscar,
        dropdown_filtro,
        boton_filtrar
    ], alignment=ft.MainAxisAlignment.END)

    dropdown_ordenar = ft.Dropdown(
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
    )

    def ordenar_tabla(e):
        columna_ordenar = dropdown_ordenar.value
        campo_indices = {
            "Nombre del Producto": 1,
            "Descripción": 2,
            "Stock Disponible": 3,
            "Precio por Unidad": 4,
            "Categorías": 5
        }
        indice_columna = campo_indices.get(columna_ordenar)
        datos_ordenados = sorted(datos_tabla, key=lambda x: str(x[indice_columna]).lower())

        tabla.rows.clear()
        tabla.rows.extend(crear_filas(datos_ordenados))
        tabla.update()

    boton_ordenar = ft.ElevatedButton('Ordenar', on_click=ordenar_tabla)

    ordenar_filtro = ft.Row([
        dropdown_ordenar,
        boton_ordenar
    ], alignment=ft.MainAxisAlignment.END)

    def cerrar_y_abrir_pedidos(e):
        page.window_close()
        os.system("flet run .\\views\\pedido_view\\src")

    def cerrar_y_abrir_movimientos(e):
        page.window_close()
        os.system("flet run .\\views\\movimiento_view\\src")

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
