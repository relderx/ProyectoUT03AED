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
    page.val_categoria = None
    page.val_precio = None
    page.val_descripcion = None

    def cerrar_y_abrir_producto_view(e):
        page.window_close()  # Cerrar la ventana actual
        os.system("flet run .\\views\\producto_view\\src")  # Ejecutar la página principal

    def cerrar_y_abrir_pedidos(e):
        page.window_close()  # Cerrar la ventana actual
        os.system("flet run .\\views\\pedido_view\\src")  # Ejecutar la vista de pedidos

    def cambio_producto(e):
        page.val_producto = e.control.value
        page.update()

    def cambio_categoria(e):
        page.val_categoria = e.control.value
        page.update()

    def cambio_precio(e):
        page.val_precio = e.control.value
        page.update()

    def cambio_descripcion(e):
        page.val_descripcion = e.control.value
        page.update()

    def cerrar_producto(e):
        page.dialog.open = False
        page.val_producto = None
        page.val_categoria = None
        page.val_precio = None
        page.val_descripcion = None
        page.update()

    def guardar_producto(e):
        # Crear un objeto Producto con los valores del formulario
        nuevo_producto = Producto(
            page.val_producto, 
            page.val_categoria, 
            float(page.val_precio), 
            page.val_descripcion
        )

        # Agregar el nuevo producto a la base de datos
        add_producto(nuevo_producto)

        # Obtener los datos actualizados de los productos
        datos_tabla = obtener_datos()

        # Limpiar las filas de la tabla
        tabla.rows.clear()

        # Añadir las filas actualizadas a la tabla
        for fila in datos_tabla:
            tabla.rows.append(ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(dato))) for dato in fila]
            ))

        # Actualizar la tabla
        tabla.update()

        # Cerrar el diálogo
        page.dialog.open = False

        # Limpiar los campos de entrada
        producto.value = None
        categoria.value = None
        precio.value = None
        descripcion.value = None
        page.update()

    def cerrar_borrar(e):
        page.dialog.open = False

    def guardar_borrar(e):
        page.dialog.open = False

    def cerrar_modificar(e):
        page.dialog.open = False

    def guardar_modificar(e):
        page.dialog.open = False
    
    producto = ft.TextField(hint_text="Escribe el nombre del producto", hint_style=ft.TextStyle(color="#d8d8d8"),label="Producto", on_submit=guardar_producto)
    categoria = ft.TextField(hint_text="Escribe la categoría del producto", hint_style=ft.TextStyle(color="#d8d8d8"),label="Categoría", on_submit=guardar_producto)
    precio = ft.TextField(hint_text="Escribe el precio del producto", hint_style=ft.TextStyle(color="#d8d8d8"),label="Precio", on_submit=guardar_producto)
    descripcion = ft.TextField(hint_text="Escribe una descripción del producto", hint_style=ft.TextStyle(color="#d8d8d8"),label="Descripción", on_submit=guardar_producto)
    
    dialogInser = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            title=ft.Text("Insertar un Producto nuevo"),
            content=ft.Column([ 
                producto,
                categoria,
                precio,
                descripcion
            ], width=page.window.width*0.33, height=page.window.height*0.5),
            actions=[ 
                ft.TextButton("Cancelar", on_click=cerrar_producto),
                ft.ElevatedButton("Guardar", on_click=guardar_producto)
            ],
    )
    dialogBor = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            title=ft.Text("¿Quieres borrar el/los productos?"),
            content=ft.Column([ 
                producto,
                categoria,
                precio,
                descripcion
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
                categoria,
                precio,
                descripcion
            ], width=page.window.width*0.33, height=page.window.height*0.5),
            actions=[ 
                ft.TextButton("Cancelar", on_click=cerrar_modificar),
                ft.ElevatedButton("Guardar", on_click=guardar_modificar)
            ],
    )
        
    producto.on_change = cambio_producto
    categoria.on_change = cambio_categoria
    precio.on_change = cambio_precio
    descripcion.on_change = cambio_descripcion
    
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
        "Nombre del Producto", 
        "Descripción", 
        "Stock Disponible", 
        "Precio por Unidad", 
        "Categorías", 
        "Fecha de Creación", 
        "Última Modificación"
    ]

    def obtener_datos():
        return tabulate_productos()

    datos_tabla = obtener_datos()

    def crear_filas(datos):
        return [
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(dato))) for dato in fila]
            ) for fila in datos
        ]

    tabla = ft.DataTable(
        width=1920,
        border_radius=2,
        border=ft.border.all(2, "red"),
        horizontal_lines=ft.BorderSide(2, "blue"),
        vertical_lines=ft.BorderSide(2, "blue"),
        columns=[ft.DataColumn(ft.Text(encabezado)) for encabezado in encabezados_tabla],
        rows=crear_filas(datos_tabla),
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

        # Limpiar las filas de la tabla
        tabla.rows.clear()

        # Añadir las filas ordenadas a la tabla
        for fila in datos_ordenados:
            tabla.rows.append(ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(dato))) for dato in fila]
            ))

        # Actualizar la tabla
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

    buscar_filtro = ft.Row([
        input_buscar,
        dropdown_filtro,
        boton_filtrar
    ], alignment=ft.MainAxisAlignment.END)

    ordenar_filtro = ft.Row([
        dropdown_ordenar,
        boton_ordenar
    ], alignment=ft.MainAxisAlignment.END)

    page.add(
        encabezado,
        botones_inferiores,
        ft.Divider(),
        ft.Text("Productos", size=30, weight=ft.FontWeight.BOLD),
        buscar_filtro,
        ordenar_filtro,
        tabla_con_scroll,
        ft.Divider(),
    )

ft.app(target=main)
