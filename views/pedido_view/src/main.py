import os
import sys
import flet as ft

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils.helpers import tabulate_movimientos
from utils.db import add_pedido
from models.pedidos import Pedido

from utils.helpers import tabulate_pedidos

def pedido_view(page: ft.Page):
    def toggle_theme():
        page.theme_mode = 'dark' if page.theme_mode == 'light' else 'light'
        page.update()  # Actualiza la vista para reflejar el cambio de tema
        
    page.title = "Gestión de Pedidos"
    
    page.val_num_pedido = None
    page.val_nombre_cliente = None
    page.val_email_cliente = None
    page.val_telefono_cliente = None
    page.val_productos = None
    page.val_estado = None
    
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
    
    def cambio_nombre_cliente(e):
        page.val_nombre_cliente = e.control.value
        page.update()
        
    def cambio_email_cliente(e):
        page.val_email_cliente = e.control.value
        page.update()
        
    def cambio_telefono_cliente(e):
        page.val_email_cliente = e.control.value
        page.update()
        
    def cambio_productos(e):
        page.val_productos = e.control.value
        page.update()
        
    def cambio_estado(e):
        page.val_estado = e.control.value
        page.update()
        
    def cerra_insertar(e):
        page.dialog.open = False
        num_pedido.value = None
        for cli in cliente.controls:
            cli.value = None
        productos.value = None
        estado.value = None
        page.update()

    def guardar_insertar(e):
        todos_productos = []
        for producto in productos.value.split(","):
            proInsert = {}
            sep_producto = producto.split(" x ")
            sep_info_producto = sep_producto[1].split(" (")
            proInsert.update({"producto":f"{sep_producto[0]}","unidades":int(sep_info_producto[0]),"precio_unidad":float(sep_info_producto[1])})
            todos_productos.insert(0,proInsert)
            
        add_pedido(Pedido(page.val_num_pedido, {
            "nombre":f"{page.val_nombre_cliente}",
            "email":f"{page.val_email_cliente}",
            "telefono":f"{page.val_telefono_cliente}"},
        todos_productos,page.val_estado))
        
        datos_tabla = obtener_datos()
        tabla.rows.clear()
        
        for fila in datos_tabla:
            tabla.rows.append(ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(dato))) for dato in fila]
            ))
        tabla.update()  
        
        page.dialog.open = False
        num_pedido.value = None
        for cli in cliente.controls:
            cli.value = None
        productos.value = None
        estado.value = None
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
    
    # def mostrar_vent_borrar(e):
    #     page.dialog = dialogBor
    #     page.dialog.open = True
    #     page.update()
    #     num_pedido.focus()
    
    # def mostrar_vent_modificar(e):
    #     page.dialog = dialogMod
    #     page.dialog.open = True
    #     page.update()
    #     num_pedido.focus()
    
    num_pedido = ft.TextField(hint_text="Escribe el número del pedido", hint_style=ft.TextStyle(color="#d8d8d8"),label="Número de pedido", on_submit=guardar_insertar)
    
    nombre_cliente = ft.TextField(hint_text="Escribe el nombre del cliente", hint_style=ft.TextStyle(color="#d8d8d8"),label="Nombre del Cliente", on_submit=guardar_insertar)
    email_cliente = ft.TextField(hint_text="Escribe el email del cliente", hint_style=ft.TextStyle(color="#d8d8d8"),label="Email del Cliente", on_submit=guardar_insertar)
    telefono_cliente = ft.TextField(hint_text="Escribe el teléfono del cliente", hint_style=ft.TextStyle(color="#d8d8d8"),label="Teléfono del Cliente", on_submit=guardar_insertar)
    cliente = ft.Column([nombre_cliente,email_cliente, telefono_cliente])
    
    productos = ft.TextField(hint_text="Escribe los productos", hint_style=ft.TextStyle(color="#d8d8d8"), helper_text="El producto tiene que tener un formato de este tipo: nombre_producto x num_unidades (precio_unidad)\nSi se quiere añadir más productos, separalos por comas de la siguiente manera: \nnombre_producto x num_unidades (precio_unidad),nombre_producto x num_unidades (precio_unidad)",label="Productos", on_submit=guardar_insertar)
    estado = ft.TextField(hint_text="Escribe el estado del pedido", hint_style=ft.TextStyle(color="#d8d8d8"), helper_text="Tiene que ser uno de los siguientes: 'pendientes, enviado, entregado o cancelado'",label="Estado", on_submit=guardar_insertar)
    
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
    # dialogBor = ft.AlertDialog(
    #         shape=ft.RoundedRectangleBorder(radius=5),
    #         title=ft.Text("Borrar Pedidos"),
    #         content=ft.Column([
    #             num_pedido,
    #             tipMovimiento,
    #             cantidad,
    #             comentario
    #         ], width=page.window.width*0.33, height=page.window.height*0.5),
    #         actions=[
    #             ft.TextButton("Si", on_click=guardar_borrar),
    #             ft.ElevatedButton("No", on_click=cerrar_borrar)
    #         ],
    # )
    # dialogMod = ft.AlertDialog(
    #         shape=ft.RoundedRectangleBorder(radius=5),
    #         title=ft.Text("Modificar un pedido nuevo"),
    #         content=ft.Column([
    #             num_pedido,
    #             tipMovimiento,
    #             cantidad,
    #             comentario
    #         ], width=page.window.width*0.33, height=page.window.height*0.5),
    #         actions=[
    #             ft.TextButton("Cancelar", on_click=cerrar_modificar),
    #             ft.ElevatedButton("Guardar", on_click=guardar_modificar)
    #         ],
    # )
        
    num_pedido.on_change = cambio_num_pedido
    nombre_cliente.on_change = cambio_nombre_cliente
    email_cliente.on_change = cambio_email_cliente
    telefono_cliente.on_change = cambio_telefono_cliente
    productos.on_change = cambio_productos
    estado.on_change = cambio_estado

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
        # ft.ElevatedButton("Borrar", width=100, disabled=True, on_click=mostrar_vent_borrar),
        ft.ElevatedButton("Borrar", width=100, disabled=True),
        ft.ElevatedButton("Insertar", width=100, on_click=mostrar_vent_insertar),
        # ft.ElevatedButton("Modificar", width=100, disabled=True, on_click=mostrar_vent_modificar),
        ft.ElevatedButton("Modificar", width=100, disabled=True),
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
        
    return ft.View(
        "/pedidos",
        [
            ft.AppBar(
                title=ft.Text("Gestión de Pedidos", weight=ft.FontWeight.BOLD, size=36),
                bgcolor=ft.Colors.INVERSE_PRIMARY,
                center_title=True,
                leading=ft.IconButton(ft.Icons.HOME, on_click=lambda _: page.go("/")),  # Botón Home
                actions=[ft.IconButton(ft.Icons.BRIGHTNESS_6, on_click=lambda _: toggle_theme()), # Botón de cambio de tema (Light <-> Dark)
                ],
            ),
            encabezado,
            botones_inferiores,
            ft.Divider(),
            ft.Text("Pedidos", size=30, weight=ft.FontWeight.BOLD),
            buscar_filtro,
            ordenar_filtro,
            tabla_con_scroll,
            ft.Divider()
        ],
    )