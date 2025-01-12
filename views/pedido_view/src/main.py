import os
import sys
import flet as ft

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils.helpers import tabulate_movimientos
from utils.db import add_pedido
from models.pedidos import Pedido

from utils.helpers import tabulate_pedidos

def main(page: ft.Page):
    page.title = "Gestión de Pedidos"
    page.window_width = 1920
    page.window_height = 1080
    page.bgcolor = ft.colors.WHITE
    page.theme_mode = 'light'
    page.window_maximized = True
    
    page.val_num_pedido = None
    page.val_cliente = None
    page.val_productos = None
    page.val_precio_total = None
    page.val_estado = None
    page.val_fech_creacion = None
    page.val_fech_modificacion = None
    
    def cerrar_y_abrir_movimiento_view(e):
        page.window_close()  # Cerrar la ventana actual
        os.system("flet run .\\views\\movimiento_view\\src")  # Ejecutar la página principal

    # Función para cerrar la ventana actual y abrir la ventana de pedidos
    def cerrar_y_abrir_producto(e):
        page.window_close()  # Cerrar la ventana actual
        os.system("flet run .\\views\\producto_view\\src")  # Ejecutar la vista de pedidos

    def cambio_num_pedido(e):
        page.val_num_pedido = e.control.value
        page.update()
        
    def cambio_cliente(e):
        page.val_cliente = e.control.value
        page.update()
        
    def cambio_productos(e):
        page.val_productos = e.control.value
        page.update()
        
    def cambio_precio_total(e):
        page.val_precio_total = e.control.value
        page.update()
        
    def cambio_estado(e):
        page.val_estado = e.control.value
        page.update()
        
    def cambio_fech_creacion(e):
        page.val_fech_creacion = e.control.value
        page.update()
        
    def cambio_fech_modificacion(e):
        page.val_fech_modificacion = e.control.value
        page.update()
        
    def cerra_insertar(e):
        page.val_num_pedido = None
        page.val_cliente = None
        page.val_productos = None
        page.val_precio_total = None
        page.val_estado = None
        page.val_fech_creacion = None
        page.val_fech_modificacion = None
        page.update()

    def guardar_insertar(e):
        add_pedido(Pedido(page.val_producto, page.val_tipMovimiento,int(page.val_cantidad),page.val_comentario))
        datos_tabla = obtener_datos()
        tabla.rows.clear()
        
        for fila in datos_tabla:
            tabla.rows.append(ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(dato))) for dato in fila]
            ))
        tabla.update()  
        
        page.dialog.open = False
        num_pedido.value() = None
        cliente.value = None
        page.val_productos = None
        page.val_precio_total = None
        page.val_estado = None
        page.val_fech_creacion = None
        page.val_fech_modificacion = None
        page.update()
        
    def cerrar_borrar(e):
        page.dialog.open = False
        page.val_num_pedido = None
        page.val_cliente = None
        page.val_productos = None
        page.val_precio_total = None
        page.val_estado = None
        page.val_fech_creacion = None
        page.val_fech_modificacion = None
        page.update()

    def guardar_borrar(e):
        page.dialog.open = False
        page.val_num_pedido = None
        page.val_cliente = None
        page.val_productos = None
        page.val_precio_total = None
        page.val_estado = None
        page.val_fech_creacion = None
        page.val_fech_modificacion = None
        page.update()
        
    def cerrar_modificar(e):
        page.dialog.open = False
        page.val_num_pedido = None
        page.val_cliente = None
        page.val_productos = None
        page.val_precio_total = None
        page.val_estado = None
        page.val_fech_creacion = None
        page.val_fech_modificacion = None
        page.update()

    def guardar_modificar(e):
        page.dialog.open = False
        page.val_num_pedido = None
        page.val_cliente = None
        page.val_productos = None
        page.val_precio_total = None
        page.val_estado = None
        page.val_fech_creacion = None
        page.val_fech_modificacion = None
        page.update()
    
    def mostrar_vent_insertar(e):
        page.dialog = dialogInser
        page.dialog.open = True
        page.update()
        num_pedido.focus()
    
    def mostrar_vent_borrar(e):
        page.dialog = dialogBor
        page.dialog.open = True
        page.update()
        num_pedido.focus()
    
    def mostrar_vent_modificar(e):
        page.dialog = dialogMod
        page.dialog.open = True
        page.update()
        num_pedido.focus()
    
    num_pedido = ft.TextField(hint_text="Escribe el número del pedido", hint_style=ft.TextStyle(color="#d8d8d8"),label="Número de pedido", on_submit=guardar_insertar)
    cliente = ft.Column([ft.TextField(hint_text="Escribe el nombre del cliente", hint_style=ft.TextStyle(color="#d8d8d8"),label="Nombre", on_submit=guardar_insertar),
                         ft.TextField(hint_text="Escribe el email del cliente", hint_style=ft.TextStyle(color="#d8d8d8"),label="Email", on_submit=guardar_insertar),
                         ft.TextField(hint_text="Escribe el teléfono del cliente", hint_style=ft.TextStyle(color="#d8d8d8"),label="Teléfono", on_submit=guardar_insertar)])
    cont_producto = 0
    for producto in page.val_productos.split(","):
        cont_producto += 1
    productos = ft.Column(ft.Row([ft.TextField(hint_text="Escribe la nombre del producto", hint_style=ft.TextStyle(color="#d8d8d8"),label="Producto", on_submit=guardar_insertar),
                                  ft.TextField(hint_text="Escribe las unidades solicitadas", hint_style=ft.TextStyle(color="#d8d8d8"),label="Unidades", on_submit=guardar_insertar),
                                  ft.TextField(hint_text="Escribe el precio por unidad", hint_style=ft.TextStyle(color="#d8d8d8"),label="Precio unitario", on_submit=guardar_insertar)]) for producto in range(cont_producto))
    estado = ft.TextField(hint_text="Escribe el estado del pedido", hint_style=ft.TextStyle(color="#d8d8d8"),label="Estado", on_submit=guardar_insertar)
    
    dialogInser = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            title=ft.Text("Inserta un pedido nuevo"),
            content=ft.Column([
                num_pedido,
                cliente,
                productos,
                estado
            ], width=page.window.width*0.33, height=page.window.height*0.5),
            actions=[
                ft.TextButton("Cancelar", on_click=cerra_insertar),
                ft.ElevatedButton("Guardar", on_click=guardar_insertar)
            ],
    )
    dialogBor = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            title=ft.Text("¿Quieres borrar el/los pedidos?"),
            content=ft.Column([
                num_pedido,
                tipMovimiento,
                cantidad,
                comentario
            ], width=page.window.width*0.33, height=page.window.height*0.5),
            actions=[
                ft.TextButton("Si", on_click=cerrar_borrar),
                ft.ElevatedButton("No", on_click=guardar_borrar)
            ],
    )
    dialogMod = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            title=ft.Text("Modificar un pedido nuevo"),
            content=ft.Column([
                num_pedido,
                tipMovimiento,
                cantidad,
                comentario
            ], width=page.window.width*0.33, height=page.window.height*0.5),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_modificar),
                ft.ElevatedButton("Guardar", on_click=guardar_modificar)
            ],
    )
        
    num_pedido.on_change = cambio_num_pedido
    tipMovimiento.on_change = cambio_cliente
    cantidad.on_change = cambio_productos
    comentario.on_change = cambio_precio_total

    # Encabezado
    encabezado = ft.Row([
        ft.Text("Gestión de pedidos", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.LEFT),
        ft.Row([
            ft.ElevatedButton("Movimiento", width=150, on_click=cerrar_y_abrir_movimiento_view),
            ft.ElevatedButton("Productos", width=150, on_click=cerrar_y_abrir_producto)
        ], alignment=ft.MainAxisAlignment.END, expand=True)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # Botones inferiores
    botones_inferiores = ft.Row([
        ft.ElevatedButton("Borrar", width=100, disabled=True, on_click=mostrar_vent_borrar),
        ft.ElevatedButton("Insertar", width=100, on_click=mostrar_vent_insertar),
        ft.ElevatedButton("Modificar", width=100, disabled=True, on_click=mostrar_vent_modificar),
    ], alignment=ft.MainAxisAlignment.END)

    # Encabezados de la tabla
    encabezados_tabla = [
        "Número de Pedido", "Cliente", "Productos", "Precio Total",
        "Estado", "Fecha de Creación", "Fecha de Modificación"
    ]

    # Obtener datos iniciales
    def obtener_datos():
        return tabulate_pedidos()

    datos_tabla = obtener_datos()

    # Crear la tabla
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

    # Contenedor con scroll para la tabla
    tabla_con_scroll = ft.Column(
        controls=[tabla],
        height=500,
        scroll=ft.ScrollMode.AUTO
    )

    # Componentes de filtro
    input_buscar = ft.TextField(label="Buscar", width=200)
    dropdown_filtro = ft.Dropdown(
        label="Filtrar por",
        options=[ft.dropdown.Option("Ningún filtro")] + [ft.dropdown.Option(encabezado) for encabezado in encabezados_tabla],
        width=200,
        value="Ningún filtro"
    )

    def aplicar_filtro(e=None):
        # Obtener datos originales
        datos = obtener_datos()

        # Filtro seleccionado y texto ingresado
        filtro = dropdown_filtro.value
        texto = input_buscar.value.lower()

        # Limpiar filas actuales de la tabla
        tabla.rows.clear()

        # Filtrar datos
        if texto:
            if filtro == "Ningún filtro":
                datos_filtrados = [
                    fila for fila in datos if any(texto in str(campo).lower() for campo in fila)
                ]
            else:
                campo_indices = {encabezado: i for i, encabezado in enumerate(encabezados_tabla)}
                indice = campo_indices.get(filtro)
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

    boton_filtrar = ft.ElevatedButton("Aplicar Filtro", on_click=aplicar_filtro)

    # Estructura de búsqueda y filtro
    buscar_filtro = ft.Row([
        input_buscar,
        dropdown_filtro,
        boton_filtrar
    ], alignment=ft.MainAxisAlignment.END)

    # Configuración de orden
    dropdown_ordenar = ft.Dropdown(
        label='Ordenar por',
        options=[ft.dropdown.Option(text=encabezado) for encabezado in encabezados_tabla],
        width=200,
        value=encabezados_tabla[0]
    )

    boton_ordenar = ft.ElevatedButton('Ordenar', on_click=lambda e: ordenar_tabla(e))

    ordenar_filtro = ft.Row([
        dropdown_ordenar,
        boton_ordenar
    ], alignment=ft.MainAxisAlignment.END)

    def ordenar_tabla(e):
        columna_ordenar = dropdown_ordenar.value
        indice_columna = encabezados_tabla.index(columna_ordenar)

        datos_ordenados = sorted(datos_tabla, key=lambda x: str(x[indice_columna]).lower())

        tabla.rows.clear()
        for fila in datos_ordenados:
            tabla.rows.append(ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(dato))) for dato in fila]
            ))

        tabla.update()

    # Estructura de la página
    page.add(
        encabezado,
        botones_inferiores,
        ft.Divider(),
        ft.Text("Pedidos", size=30, weight=ft.FontWeight.BOLD),
        buscar_filtro,
        ordenar_filtro,
        tabla_con_scroll,
        ft.Divider()
    )

ft.app(target=main)