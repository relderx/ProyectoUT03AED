import os
import sys
import flet as ft
from utils.helpers import tabulate_productos
from utils.db import add_producto, delete_producto, update_producto
from models.productos import Producto

def obtener_datos():
    return tabulate_productos()

def producto_view(page: ft.Page):
    page.title = "Gestión de Productos"

    # Variables globales
    page.val_producto = None
    page.val_descripcion = None
    page.val_stock_disponible = None
    page.val_precio_unitario = None
    page.val_categorias = None
    productos_seleccionados_ids = []

    # Obtener datos originales para usar en filtrado
    datos_originales = obtener_datos()

    def aplicar_filtro(e):
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
        # Deshabilitar el botón "Modificar" después de cerrar el diálogo
        productos_seleccionados_ids.clear()  # Limpia la selección
        boton_modificar.disabled = True
        boton_borrar.disabled = True
        page.update()

    def mostrar_notificacion(mensaje):
        page.snack_bar = ft.SnackBar(ft.Text(mensaje), bgcolor=ft.colors.GREEN)
        page.snack_bar.open = True
        page.update()

    def guardar_insertar(e):
        newCategorias = []
        for categoria in page.val_categorias.split(","):
            newCategorias.append(categoria.strip())
        add_producto(Producto(page.val_producto, page.val_descripcion, int(page.val_stock_disponible), float(page.val_precio_unitario), newCategorias))
        actualizar_tabla()
        cerrar_dialogo(e)

    def guardar_modificar(e):
        if productos_seleccionados_ids:
            producto_id = productos_seleccionados_ids[0]
            updated_data = {
                "producto": page.val_producto,
                "descripcion": page.val_descripcion,
                "stock": int(page.val_stock_disponible),
                "precio_unidad": int(page.val_precio_unitario),
                "categoria": [categoria.strip() for categoria in page.val_categorias.split(",")]
            }
            update_producto(producto_id, updated_data)
            actualizar_tabla()
            cerrar_dialogo(e)

    def borrar_productos(e):
        for producto_id in productos_seleccionados_ids:
            delete_producto(producto_id)
        actualizar_tabla()
        productos_seleccionados_ids.clear()
        boton_borrar.disabled = True
        boton_modificar.disabled = True
        page.update()

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

    def obtener_datos_producto(producto_id):
        datos = obtener_datos()  # Obtener todos los productos (puedes ajustar esta parte según tu estructura)
        for fila in datos:
            if fila[0] == producto_id:  # Suponiendo que el ID es la primera columna
                return {
                    "producto": fila[0],  # Nombre del producto
                    "descripcion": fila[1],  # Descripción
                    "stock_disponible": fila[2],  # Stock disponible
                    "precio_unitario": fila[3],  # Precio por unidad
                    "categorias": fila[4].split(",")  # Categorías separadas por comas
                }
        raise ValueError(f"Producto con ID {producto_id} no encontrado.")


    def mostrar_vent_modificar(e):
        global producto_seleccionado_data
        if len(productos_seleccionados_ids) != 1:
            mostrar_notificacion("Selecciona un único producto para modificar.")
            return

        producto_id = productos_seleccionados_ids[0]
        producto_seleccionado_data = next(
            (producto for producto in obtener_datos() if producto[0] == producto_id), None
        )
        if not producto_seleccionado_data:
            mostrar_notificacion("No se encontró el producto seleccionado.")
            return

        # Cargar los datos actuales en las variables
        page.val_producto = producto_seleccionado_data[0]  # Asegúrate de que el índice sea correcto
        page.val_descripcion = producto_seleccionado_data[1]
        page.val_stock_disponible = str(producto_seleccionado_data[2])
        page.val_precio_unitario = str(producto_seleccionado_data[3])
        page.val_categorias = producto_seleccionado_data[4]

        # Crear el cuadro de diálogo para modificar
        dialog_modificar = ft.AlertDialog(
            title=ft.Text("Modificar Producto"),
            content=ft.Column([
                ft.TextField(
                    label="Nombre del Producto",
                    value=page.val_producto,
                    on_change=lambda e: cambio_producto(e),
                    hint_text="Nombre del producto"
                ),
                ft.TextField(
                    label="Descripción",
                    value=page.val_descripcion,
                    on_change=lambda e: cambio_descripcion(e),
                    hint_text="Descripción del producto"
                ),
                ft.TextField(
                    label="Stock Disponible",
                    value=page.val_stock_disponible,
                    on_change=lambda e: cambio_stock_disponible(e),
                    hint_text="Cantidad disponible"
                ),
                ft.TextField(
                    label="Precio por Unidad",
                    value=page.val_precio_unitario,
                    on_change=lambda e: cambio_precio_unitario(e),
                    hint_text="Precio del producto"
                ),
                ft.TextField(
                    label="Categorías",
                    value=page.val_categorias,
                    on_change=lambda e: cambio_categorias(e),
                    hint_text="Categorías separadas por comas"
                ),
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialogo),
                ft.ElevatedButton("Guardar", on_click=guardar_modificar)
            ],
        )
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

    def seleccionar_producto(e):
        producto_id = e.control.data
        if e.control.value:
            productos_seleccionados_ids.append(producto_id)
        else:
            productos_seleccionados_ids.remove(producto_id)
        boton_borrar.disabled = len(productos_seleccionados_ids) == 0
        boton_modificar.disabled = len(productos_seleccionados_ids) != 1
        page.update()

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

    def crear_filas(datos):
        filas = []
        for fila in datos:
            producto_id = fila[0]
            checkbox = ft.Checkbox(value=False, on_change=seleccionar_producto, data=producto_id)
            celdas = [ft.DataCell(checkbox)] + [ft.DataCell(ft.Text(str(dato))) for dato in fila]
            filas.append(ft.DataRow(cells=celdas))
        return filas

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

    datos_tabla = datos_originales

    tabla = ft.DataTable(
        width=1920,
        border_radius=2,
        border=ft.border.all(2, "red"),
        horizontal_lines=ft.BorderSide(2, "blue"),
        vertical_lines=ft.BorderSide(2, "blue"),
        columns=[ft.DataColumn(ft.Text(encabezado)) for encabezado in encabezados_tabla],
        rows=crear_filas(datos_tabla),
    )

    texto_buscar = ft.TextField(label="Buscar", width=200)
    filtro_dropdown = ft.Dropdown(
        label="Filtrar por",
        options=[ft.dropdown.Option("Ningún filtro")] + [
            ft.dropdown.Option(encabezado) for encabezado in encabezados_tabla[1:]
        ],
        width=200,
        value="Ningún filtro"
    )
    boton_aplicar_filtro = ft.ElevatedButton("Aplicar Filtro", on_click=aplicar_filtro)

    orden_dropdown = ft.Dropdown(
        label="Ordenar por",
        options=[
            ft.dropdown.Option(encabezado) for encabezado in encabezados_tabla[1:]
        ],
        width=200,
        value="Nombre del Producto"
    )
    boton_aplicar_orden = ft.ElevatedButton("Ordenar", on_click=aplicar_orden)

    buscar_filtro = ft.Row([
        texto_buscar,
        filtro_dropdown,
        boton_aplicar_filtro
    ], alignment=ft.MainAxisAlignment.END)

    ordenar_filtro = ft.Row([
        orden_dropdown,
        boton_aplicar_orden
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
