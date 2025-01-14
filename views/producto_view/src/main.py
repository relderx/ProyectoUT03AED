import os
import sys
import flet as ft

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils.helpers import tabulate_productos
from utils.db import add_producto
from models.productos import Producto

def producto_view(page: ft.Page):
    page.title = "Gestión de Productos"
    
    def toggle_theme():
        # Cambiar entre 'light' y 'dark' al hacer clic
        page.theme_mode = 'dark' if page.theme_mode == 'light' else 'light'
        page.update()  # Actualiza la vista para reflejar el cambio de tema
    
    page.val_producto = None
    page.val_descripcion = None
    page.val_stock_disponible = None
    page.val_precio_unitario = None
    page.val_categorias = None

    def cerrar_y_abrir_movimientos(e):
        page.window_close()  # Cerrar la ventana actual
        os.system("flet run .\\views\\movimiento_view\\src")  # Ejecutar la página principal

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
    
    # dialogInser = ft.AlertDialog(
    #         shape=ft.RoundedRectangleBorder(radius=5),
    #         title=ft.Text("Insertar un Producto nuevo"),
    #         content=ft.Column([ 
    #             producto,
    #             descripcion,
    #             stock_disponible,
    #             precio_unitario,
    #             categorias
    #         ], width=page.window.width*0.33, height=page.window.height*0.5),
    #         actions=[ 
    #             ft.TextButton("Cancelar", on_click=cerrar_producto),
    #             ft.ElevatedButton("Guardar", on_click=guardar_insertar)
    #         ],
    # )
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
        # Obtener el índice de la fila seleccionada
        row_index = e.control.data
        if e.control.value:
            # Agregar el producto a la lista de seleccionados
            productos_seleccionados.append(datos_tabla[row_index])
        else:
            # Eliminar el producto de la lista de seleccionados
            productos_seleccionados.remove(datos_tabla[row_index])

    def obtener_datos():
        return tabulate_productos()

    datos_tabla = obtener_datos()

    def crear_filas(datos):
        filas = []
        for i, fila in enumerate(datos):
            checkbox = ft.Checkbox(value=False, on_change=seleccionar_producto, data=i)
            celdas = [ft.DataCell(checkbox)] + [ft.DataCell(ft.Text(str(dato))) for dato in fila]
            filas.append(ft.DataRow(cells=celdas))
        return filas

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
                campo_indices = {encabezado: i for i, encabezado in enumerate(encabezados_tabla[1:])}
                indice = campo_indices.get(filtro)
                if indice is not None:
                    datos_filtrados = [
                        fila for fila in datos if texto in str(fila[indice]).lower()
                    ]
                else:
                    datos_filtrados = datos
        else:
            datos_filtrados = datos

        # Regenerar filas con los datos filtrados
        filas_filtradas = crear_filas(datos_filtrados)
        tabla.rows.extend(filas_filtradas)
        tabla.update()


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
        options=[ft.dropdown.Option("Ningún filtro")] + [ft.dropdown.Option(encabezado) for encabezado in encabezados_tabla[1:]],  # Excluir "Seleccionar"
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
                    fila for fila in datos if any(texto in str(campo).lower() for campo in fila[1:])  # Ignorar primera columna
                ]
            else:
                campo_indices = {encabezado: i for i, encabezado in enumerate(encabezados_tabla[1:], start=1)}
                indice = campo_indices.get(filtro)
                if indice is not None:
                    datos_filtrados = [
                        fila for fila in datos if texto in str(fila[indice]).lower()
                    ]
                else:
                    datos_filtrados = datos
        else:
            datos_filtrados = datos

        # Regenerar filas con los datos filtrados
        filas_filtradas = crear_filas(datos_filtrados)
        tabla.rows.extend(filas_filtradas)
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
        "/inventario",
        [
            ft.AppBar(
                title=ft.Text("Gestión de Productos", weight=ft.FontWeight.BOLD, size=36),
                bgcolor=ft.Colors.INVERSE_PRIMARY,
                center_title=True,
                leading=ft.IconButton(ft.Icons.HOME, on_click=lambda _: page.go("/")),  # Botón Home
                actions=[ft.IconButton(ft.Icons.BRIGHTNESS_6, on_click=lambda _: toggle_theme()), # Botón de cambio de tema (Light <-> Dark)
                ],
            ),
            encabezado,
            botones_inferiores,
            ft.Divider(),
            ft.Text("Producto", size=30, weight=ft.FontWeight.BOLD),
            buscar_filtro,
            ordenar_filtro,
            tabla_con_scroll,  # Agregar la tabla dentro del contenedor con scroll
            ft.Divider(),
        ]
    )


# ft.app(target=producto_view)
