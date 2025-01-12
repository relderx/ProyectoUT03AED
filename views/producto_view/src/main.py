import os
import sys
import flet as ft

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils.helpers import tabulate_productos
from utils.db import add_producto
from models.productos import Producto

def main(page: ft.Page):
    page.title = "Gestión de Productos"
    page.window.width = 1920
    page.window.height = 1080
    page.bgcolor = ft.colors.WHITE
    page.theme_mode = 'light'
    page.window.maximized = True
    
    page.val_producto = None
    page.val_descripcion = None
    page.val_stock_disponible = None
    page.val_precio_unitario = None
    page.val_categorias = None

    def cerrar_y_abrir_producto_view(e):
        page.window_close()  # Cerrar la ventana actual
        os.system("flet run .\\views\\producto_view\\src")  # Ejecutar la página principal

    def cerrar_y_abrir_pedidos(e):
        page.window_close()  # Cerrar la ventana actual
        os.system("flet run .\\views\\pedido_view\\src")  # Ejecutar la vista de pedidos

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
        producto.value = None
        descripcion.value = None
        stock_disponible.value = None
        precio_unitario.value = None
        categorias.value = None
        page.update()

    def guardar_insertar(e):
        add_producto(Producto(
            page.val_producto, 
            page.val_descripcion, 
            int(page.val_stock_disponible), 
            float(page.val_precio_unitario),
            [categoria for categoria in page.val_categorias.split(",")]
        ))

        datos_tabla = obtener_datos()
        tabla.rows.clear()
        for fila in datos_tabla:
            tabla.rows.append(ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(dato))) for dato in fila]
            ))
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
        # Borra los productos seleccionados
        for pid in productos_seleccionados:
            # Eliminar el producto de la base de datos
            # Implementa la función para eliminar el producto
            # delete_producto(pid)
            pass
        page.dialog.open = False

    def cerrar_modificar(e):
        page.dialog.open = False

    def guardar_modificar(e):
        page.dialog.open = False
    
    producto = ft.TextField(hint_text="Escribe el nombre del producto", hint_style=ft.TextStyle(color="#d8d8d8"),label="Producto", on_submit=guardar_insertar)
    descripcion = ft.TextField(hint_text="Escribe la descripción del producto", hint_style=ft.TextStyle(color="#d8d8d8"),label="Descripción", on_submit=guardar_insertar)
    stock_disponible = ft.TextField(hint_text="Escribe el stock del producto", hint_style=ft.TextStyle(color="#d8d8d8"),label="Stock del producto", on_submit=guardar_insertar)
    precio_unitario = ft.TextField(hint_text="Escribe el precio del producto por unidad", hint_style=ft.TextStyle(color="#d8d8d8"),label="Precio unitario", on_submit=guardar_insertar)
    categorias = ft.TextField(hint_text="Escribe las categorías del producto", hint_style=ft.TextStyle(color="#d8d8d8"), helper_text="Separa cada categoría comas y sin espacios",label="Categorías del producto", on_submit=guardar_insertar)
    
    dialogInser = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            title=ft.Text("Insertar un Producto nuevo"),
            content=ft.Column([ 
                producto,
                descripcion,
                stock_disponible,
                precio_unitario,
                categorias
            ], width=page.window.width*0.33, height=page.window.height*0.5),
            actions=[ 
                ft.TextButton("Cancelar", on_click=cerrar_producto),
                ft.ElevatedButton("Guardar", on_click=guardar_insertar)
            ],
    )
    dialogBor = ft.AlertDialog(
        shape=ft.RoundedRectangleBorder(radius=5),
        title=ft.Text("¿Quieres borrar el/los productos?"),
        content=ft.Text("Estás seguro de que deseas eliminar los productos seleccionados?"),
        actions=[ 
            ft.TextButton("No", on_click=cerrar_borrar),
            ft.ElevatedButton("Sí", on_click=guardar_borrar)
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
        
    producto.on_change = cambio_producto
    descripcion.on_change = cambio_descripcion
    stock_disponible.on_change = cambio_stock_disponible
    precio_unitario.on_change = cambio_precio_unitario
    categorias.on_change = cambio_categorias
    
    def mostrar_vent_insertar(e):
        page.dialog = dialogInser
        page.dialog.open = True
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
        ft.Text("Gestión de Productos", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.LEFT),
        ft.Row([ 
            ft.ElevatedButton("Pedidos", width=150, on_click=cerrar_y_abrir_pedidos)
        ], alignment=ft.MainAxisAlignment.END, expand=True)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    botones_inferiores = ft.Row([ 
        ft.ElevatedButton("Borrar", width=100, disabled=True, on_click=mostrar_vent_borrar),
        ft.ElevatedButton("Insertar", width=100, on_click=mostrar_vent_insertar),
        ft.ElevatedButton("Modificar", width=100, disabled=True, on_click=mostrar_vent_modificar),
    ], alignment=ft.MainAxisAlignment.END)

   # Encabezados de la tabla
    encabezados_tabla = [
        "Seleccionar",  # Columna para el checkbox
        "Nombre del Producto", 
        "Descripción", 
        "Stock Disponible", 
        "Precio por Unidad", 
        "Categorías", 
        "Fecha de Creación", 
        "Última Modificación"
    ]

    productos_seleccionados = []  # Lista para almacenar los productos seleccionados

    def obtener_datos():
        return tabulate_productos()

    datos_tabla = obtener_datos()

    def crear_filas(productos, datos):
        rows = []
        for producto, fila in zip(productos, datos):
            cells = [
                ft.DataCell(
                    ft.Checkbox(
                        on_change=lambda e, pid=producto[0]: actualizar_seleccion(e, pid)
                    )
                ),  # Checkbox para selección
                *[ft.DataCell(ft.Text(str(dato))) for dato in fila]
            ]
            rows.append(ft.DataRow(cells=cells))
        return rows

    def actualizar_seleccion(e, pid):
        if e.control.value:
            productos_seleccionados.append(pid)
        else:
            productos_seleccionados.remove(pid)

        # Habilitar o deshabilitar el botón "Borrar" según si hay productos seleccionados
        botones_inferiores.controls[0].disabled = not bool(productos_seleccionados)
        page.update()

    tabla = ft.DataTable(
        width=1920,
        border_radius=2,
        border=ft.border.all(2, "red"),
        horizontal_lines=ft.BorderSide(2, "blue"),
        vertical_lines=ft.BorderSide(2, "blue"),
        columns=[ft.DataColumn(ft.Text(encabezado)) for encabezado in encabezados_tabla],
        rows=crear_filas(datos_tabla, datos_tabla),
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

    def aplicar_filtro(e=None):
        datos = obtener_datos()
        filtro = dropdown_filtro.value
        texto = input_buscar.value.lower()
        tabla.rows.clear()

        datos_filtrados = []
        if texto:
            if filtro == "Ningún filtro":
                datos_filtrados = [
                    fila for fila in datos if any(texto in str(campo).lower() for campo in fila)
                ]
            else:
                campo_indices = {
                    "Producto": 0,
                    "Categoría": 1,
                    "Precio": 2,
                    "Descripción": 3
                }
                indice = campo_indices.get(filtro, None)
                if indice is not None:
                    datos_filtrados = [
                        fila for fila in datos if texto in str(fila[indice]).lower()
                    ]
        else:
            datos_filtrados = datos

        for fila in datos_filtrados:
            tabla.rows.append(ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(dato))) for dato in fila]
            ))

        tabla.update()

    def ordenar_tabla(e):
        columna_ordenar = dropdown_ordenar.value
        indice_columna = encabezados_tabla.index(columna_ordenar)

        # Ordenar los datos basados en la columna seleccionada
        if columna_ordenar in ["Precio por Unidad", "Stock Disponible"]:  # Si es una columna numérica
            datos_ordenados = sorted(datos_tabla, key=lambda x: float(x[indice_columna]) if x[indice_columna] else 0)
        else:
            # Si es una columna de texto, ordenar alfabéticamente
            datos_ordenados = sorted(datos_tabla, key=lambda x: str(x[indice_columna]).lower())

        tabla.rows.clear()
        for fila in datos_ordenados:
            tabla.rows.append(ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(dato))) for dato in fila]
            ))

        tabla.update()

    page.add(
        encabezado,
        botones_inferiores,
        ft.Divider(),
        ft.Text("Productos", size=30, weight=ft.FontWeight.BOLD),
        tabla_con_scroll,
        ft.Divider(),
    )

ft.app(target=main)
