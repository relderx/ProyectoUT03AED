import os
import sys
import flet as ft

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils.helpers import tabulate_pedidos
from utils.db import add_pedido, delete_producto
from models.pedidos import Pedido

def pedido_view(page: ft.Page):
    page.title = "Gestión de Pedidos"
    
    def toggle_theme():
        # Cambiar entre 'light' y 'dark' al hacer clic
        page.theme_mode = 'dark' if page.theme_mode == 'light' else 'light'
        page.update()  # Actualiza la vista para reflejar el cambio de tema
        
    page.val_num_pedido = None
    page.val_nombre_cliente = None
    page.val_email_cliente = None
    page.val_telefono_cliente = None
    page.val_productos = None
    page.val_estado = None
    productos_seleccionados_ids = []
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
        
    def cerrar_dialogo(e):
        page.dialog.open = False
        page.update()

    def guardar_insertar(e):
        todos_productos = []
        for producto in page.val_productos.split(","):
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
        actualizar_tabla()
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

    def actualizar_tabla():
        datos_tabla = obtener_datos()
        tabla.rows.clear()
        tabla.rows.extend(crear_filas(datos_tabla))
        tabla.update()
        
    productos = ft.TextField(hint_text="Escribe los productos", hint_style=ft.TextStyle(color="#d8d8d8"), helper_text="El producto tiene que tener un formato de este tipo: nombre_producto x num_unidades (precio_unidad)\nSi se quiere añadir más productos, separalos por comas de la siguiente manera: \nnombre_producto x num_unidades (precio_unidad),nombre_producto x num_unidades (precio_unidad)",label="Productos", on_submit=guardar_insertar)
    estado = ft.TextField(hint_text="Escribe el estado del pedido", hint_style=ft.TextStyle(color="#d8d8d8"), helper_text="Tiene que ser uno de los siguientes: 'pendientes, enviado, entregado o cancelado'",label="Estado", on_submit=guardar_insertar)

    num_pedido = ft.TextField(hint_text="Escribe el número del pedido", hint_style=ft.TextStyle(color="#d8d8d8"),label="Número de pedido", on_submit=guardar_insertar)

    nombre_cliente = ft.TextField(hint_text="Escribe el nombre del cliente", hint_style=ft.TextStyle(color="#d8d8d8"),label="Nombre del Cliente", on_submit=guardar_insertar)
    email_cliente = ft.TextField(hint_text="Escribe el email del cliente", hint_style=ft.TextStyle(color="#d8d8d8"),label="Email del Cliente", on_submit=guardar_insertar)
    telefono_cliente = ft.TextField(hint_text="Escribe el teléfono del cliente", hint_style=ft.TextStyle(color="#d8d8d8"),label="Teléfono del Cliente", on_submit=guardar_insertar)
    cliente = ft.Column([nombre_cliente,email_cliente, telefono_cliente])

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
                title=ft.Text("Modificar un pedido nuevo"),
                content=ft.Column([
                    num_pedido,
                    cliente,
                    productos,
                    estado
                ],
                width=650,
                height=650
                ),
                actions=[
                    ft.TextButton("Cancelar", on_click=cerrar_modificar),
                    ft.ElevatedButton("Guardar", on_click=guardar_modificar)
                ],
        )
    
    def mostrar_vent_insertar(e):
        num_pedido.value = ""
        nombre_cliente.value = ""
        email_cliente.value = ""
        telefono_cliente.value = ""
        productos.value = ""
        estado.value = ""
        
        num_pedido.on_change = cambio_num_pedido
        nombre_cliente.on_change = cambio_nombre_cliente
        email_cliente.on_change = cambio_email_cliente
        telefono_cliente.on_change = cambio_telefono_cliente
        productos.on_change = cambio_productos
        estado.on_change = cambio_estado

        page.dialog = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            title=ft.Text("Inserta un pedido nuevo"),
            content=ft.Column([
                num_pedido,
                cliente,
                productos,
                estado
            ],
            width=650,
            height=650
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialogo),
                ft.ElevatedButton("Guardar", on_click=guardar_insertar)
            ],
        )
        page.dialog.open = True
        page.update()
        num_pedido.focus()

    def mostrar_vent_modificar(e):
        num_pedido.on_change = cambio_num_pedido
        nombre_cliente.on_change = cambio_nombre_cliente
        email_cliente.on_change = cambio_email_cliente
        telefono_cliente.on_change = cambio_telefono_cliente
        productos.on_change = cambio_productos
        estado.on_change = cambio_estado

        page.dialog = dialog_modificar
        dialog_modificar.open = True
        page.update()

    def mostrar_vent_borrar(e):
        page.dialog = dialog_borrar
        dialog_borrar.open = True
        page.update()


    boton_borrar = ft.ElevatedButton("Borrar", width=100, disabled=True, on_click=mostrar_vent_borrar)
    boton_modificar = ft.ElevatedButton("Modificar", width=100, on_click=mostrar_vent_modificar, disabled=True)
    botones_inferiores = ft.Row([
        boton_borrar,
        ft.ElevatedButton("Insertar", width=100, on_click=mostrar_vent_insertar),
        boton_modificar
    ], alignment=ft.MainAxisAlignment.END
    )
    
    # Encabezado
    encabezado = ft.Row([
        ft.Text("Gestión de pedidos", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.LEFT)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    # Encabezados de la tabla
    encabezados_tabla = [
        "Número de Pedido", "Cliente", "Productos", "Precio Total",
        "Estado", "Fecha de Creación", "Fecha de Modificación"
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

    # Obtener datos iniciales
    def obtener_datos():
        return tabulate_pedidos()

    datos_tabla = obtener_datos()

    # Crear la tabla
    def crear_filas(datos):
        filas = []
        for fila in datos:
            producto_id = fila[0]
            checkbox = ft.Checkbox(value=False, on_change=seleccionar_producto, data=producto_id)
            celdas = [ft.DataCell(checkbox)] + [ft.DataCell(ft.Text(str(dato))) for dato in fila]
            filas.append(ft.DataRow(cells=celdas))
        return filas

    tabla = ft.DataTable(
        width=1920,
        border_radius=2,
        border=ft.border.all(2, "red"),
        horizontal_lines=ft.BorderSide(2, "blue"),
        vertical_lines=ft.BorderSide(2, "blue"),
        columns=[ft.DataColumn(ft.Text(encabezado)) for encabezado in encabezados_tabla],
        rows=crear_filas(datos_tabla),
    )

    # Componentes de filtro
    input_buscar = ft.TextField(label="Buscar", width=200)
    dropdown_filtro = ft.Dropdown(
        label="Filtrar por",
        options=[ft.dropdown.Option("Ningún filtro")] + [ft.dropdown.Option(encabezado) for encabezado in encabezados_tabla],
        width=200,
        value="Ningún filtro"
    )
    datos_originales = obtener_datos()
    texto_buscar = ft.TextField(label="Buscar", width=200)

    def aplicar_filtro(e=None):
        filtro_seleccionado = filtro_dropdown.value
        texto_busqueda = texto_buscar.value.lower()

        if filtro_seleccionado == "Ningún filtro" or not texto_busqueda:
            # Si no hay filtro o búsqueda, restablecer datos originales
            datos_filtrados = datos_originales
        else:
            # Filtrar los datos según el criterio seleccionado (omitiendo la columna "Seleccionar")
            indice_columna = encabezados_tabla.index(filtro_seleccionado) - 1
            datos_filtrados = [
                fila for fila in datos_originales
                if texto_busqueda in str(fila[indice_columna]).lower()
            ]

        # Actualizar la tabla con los datos filtrados
        tabla.rows.clear()
        tabla.rows.extend(crear_filas(datos_filtrados))
        tabla.update()

    boton_filtrar = ft.ElevatedButton("Aplicar Filtro", on_click=aplicar_filtro)

    # Estructura de búsqueda y filtro
    buscar_filtro = ft.Row([
        input_buscar,
        dropdown_filtro,
        boton_filtrar
    ], alignment=ft.MainAxisAlignment.END)

    buscar_filtro = ft.Row([
        ft.TextField(label="Buscar", width=200),
        ft.Dropdown(
            label="Filtrar por",
            options=[ft.dropdown.Option("Ningún filtro")] + [
                ft.dropdown.Option("Número de Pedido"),
                ft.dropdown.Option("Cliente"),
                ft.dropdown.Option("Productos"),
                ft.dropdown.Option("Precio Total"),
                ft.dropdown.Option("Estado"),
                ft.dropdown.Option("Fecha de Creación"),
                ft.dropdown.Option("Fecha de Modificación"),
            ],
            width=200,
            value="Ningún filtro"
        ),
        ft.ElevatedButton("Aplicar Filtro")
    ], alignment=ft.MainAxisAlignment.END)
    boton_aplicar_orden = ft.ElevatedButton("Ordenar", on_click=aplicar_orden)
    
    orden_dropdown = ft.Dropdown(
        label="Ordenar por",
        options=[
            ft.dropdown.Option(encabezado) for encabezado in encabezados_tabla[1:]
        ],
        width=200,
        value="Nombre del Producto"
    )

    ordenar_filtro = ft.Row([
        orden_dropdown,
        boton_aplicar_orden
    ], alignment=ft.MainAxisAlignment.END)
    
    filtro_dropdown = ft.Dropdown(
        label="Filtrar por",
        options=[ft.dropdown.Option("Ningún filtro")] + [
            ft.dropdown.Option(encabezado) for encabezado in encabezados_tabla[1:]
        ],
        width=200,
        value="Ningún filtro"
    )
        
    return ft.View(
        '/pedidos',
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
            tabla,
            ft.Divider()
        ],
        scroll=ft.ScrollMode.AUTO  # Habilitar el scroll para la página
    )
