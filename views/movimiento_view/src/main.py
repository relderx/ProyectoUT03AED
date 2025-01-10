import os
import sys
import flet as ft

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils.helpers import tabulate_movimientos
print(tabulate_movimientos())

def main(page: ft.Page):
    page.title = "Movimiento de Inventario"
    page.window_width = 1920
    page.window_height = 1080
    page.bgcolor = ft.colors.WHITE
    page.theme_mode = 'light'
    page.window_maximized = True

# ... (resto de tu código)
    def cerrar_movimiento(e):
        print(producto)
        page.dialog.open = False
        page.update()

    # Función para guardar el nuevo movimiento (ejemplo)
    def guardar_movimiento(e):
        # Obtener los datos de los campos del diálogo
        # ...
        # Agregar el nuevo movimiento a la base de datos o lista
        # ...
        page.dialog.open = False
        page.update()
        # Actualizar la tabla con el nuevo dato
        # ...
    
    producto = ft.TextField(hint_text="Escribe el nombre del producto", hint_style=ft.TextStyle(color="#d8d8d8"),label="Producto", on_submit=guardar_movimiento)
    tipMovimiento = ft.TextField(hint_text="Escribe el tipo de movimiento", hint_style=ft.TextStyle(color="#d8d8d8"),label="Tipo de Movimiento", on_submit=guardar_movimiento)
    cantidad = ft.TextField(hint_text="Escribe la cantidad del producto", hint_style=ft.TextStyle(color="#d8d8d8"),label="Cantidad", on_submit=guardar_movimiento)
    fecha = ft.TextField(hint_text="Escribe la fecha en la que se realiza la acción", hint_style=ft.TextStyle(color="#d8d8d8"),label="Fecha", on_submit=guardar_movimiento)
    comentario = ft.TextField(hint_text="Escribe un comentario para el movimiento", hint_style=ft.TextStyle(color="#d8d8d8"),label="Comentario", on_submit=guardar_movimiento)
    dialog = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            title=ft.Text("Insertar_Movimiento"),
            content=ft.Column([
                producto,
                tipMovimiento,
                cantidad,
                fecha,
                comentario
            ], width=page.window_width*0.33, height=page.window_height*0.5),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_movimiento),
                ft.ElevatedButton("Guardar", on_click=guardar_movimiento)
            ],
        )
    
    def mostrar_vent_insertar(e):
        page.dialog = dialog
        page.dialog.open = True
        page.update()
        producto.focus()

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
        ft.ElevatedButton("Insertar", width=100, on_click=mostrar_vent_insertar),
        ft.ElevatedButton("Modificar", width=100, disabled=True),
    ], alignment=ft.MainAxisAlignment.END)

    # Encabezados de la tabla
    encabezados_tabla = ["Producto", "Tipo de Movimiento", "Cantidad", "Fecha", "Comentario"]

    # Obtener datos originales de la base de datos
    def obtener_datos():
        return tabulate_movimientos()

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
        height=500,  # Puedes ajustar la altura según sea necesario
        scroll=ft.ScrollMode.AUTO  # Habilitar el scroll vertical
    )

    # Componentes de filtro
    dropdown_filtro = ft.Dropdown(
        label="Filtrar por",
        options=[ft.dropdown.Option("Ningún filtro")] + [ft.dropdown.Option(encabezado) for encabezado in encabezados_tabla],
        width=200,
        value="Ningún filtro"
    )

    input_buscar = ft.TextField(label="Buscar", width=200)

    def aplicar_filtro(e=None):  # e=None para aceptar llamadas sin evento
        # Obtener datos originales de nuevo
        datos = obtener_datos()

        # Obtener filtro seleccionado y texto ingresado
        filtro = dropdown_filtro.value
        texto = input_buscar.value.lower()

        # Limpiar las filas actuales de la tabla
        tabla.rows.clear()  # Asegurarse de que no haya filas previas

        # Filtrar los datos
        datos_filtrados = []
        if texto:  # Si hay texto ingresado
            if filtro == "Ningún filtro":
                # Buscar en todos los campos
                datos_filtrados = [
                    fila for fila in datos if any(texto in str(campo).lower() for campo in fila)
                ]
            else:
                # Filtrar por campo específico
                campo_indices = {
                    "Producto": 0,
                    "Tipo de Movimiento": 1,
                    "Cantidad": 2,
                    "Fecha": 3,
                    "Comentario": 4
                }
                indice = campo_indices.get(filtro, None)
                if indice is not None:
                    datos_filtrados = [
                        fila for fila in datos if texto in str(fila[indice]).lower()
                    ]
        else:
            # Si no hay texto, mostrar todos los datos
            datos_filtrados = datos

        # Agregar las filas filtradas a la tabla
        for fila in datos_filtrados:
            tabla.rows.append(ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(dato))) for dato in fila]
            ))

        tabla.update()  # Actualizar la tabla con los resultados filtrados

    # Función para ordenar la tabla
    def ordenar_tabla(e):
        columna_ordenar = dropdown_ordenar.value
        indice_columna = encabezados_tabla.index(columna_ordenar)

        # Ordenar los datos según la columna seleccionada
        datos_ordenados = sorted(datos_tabla, key=lambda x: str(x[indice_columna]).lower())

        tabla.rows.clear()  # Limpiar las filas actuales de la tabla
        for fila in datos_ordenados:
            tabla.rows.append(ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(dato))) for dato in fila]
            ))

        tabla.update()  # Actualizar la tabla con los datos ordenados

    # Dropdown para ordenar la tabla
    dropdown_ordenar = ft.Dropdown(
        label='Ordenar por',
        options=[ft.dropdown.Option(text=encabezado) for encabezado in encabezados_tabla],
        width=200,
        value=encabezados_tabla[0]  # Ordenar por la primera columna por defecto
    )
    boton_ordenar = ft.ElevatedButton('Ordenar', on_click=ordenar_tabla)

    # Configuración de eventos
    input_buscar.on_submit = aplicar_filtro  # Aplicar filtro al presionar Enter
    boton_filtrar = ft.ElevatedButton("Aplicar Filtro", on_click=aplicar_filtro)

    # Estructura de búsqueda y filtro
    buscar_filtro = ft.Row([
        input_buscar,
        dropdown_filtro,
        boton_filtrar
    ], alignment=ft.MainAxisAlignment.END)

    # Configuración de orden
    ordenar_filtro = ft.Row([
        dropdown_ordenar,
        boton_ordenar
    ], alignment=ft.MainAxisAlignment.END)

    # Estructura de la página
    page.add(
        encabezado,
        botones_inferiores,
        ft.Divider(),
        ft.Text("Movimientos", size=30, weight=ft.FontWeight.BOLD),
        buscar_filtro,
        ordenar_filtro,
        tabla_con_scroll,  # Agregar la tabla dentro del contenedor con scroll
        ft.Divider(),
    )

ft.app(target=main)