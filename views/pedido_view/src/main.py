import os
import sys
import flet as ft

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils.helpers import tabulate_pedidos
print(tabulate_pedidos())

def main(page: ft.Page):
    page.title = "Gestión de Pedidos"
    page.window_width = 1920
    page.window_height = 1080
    page.bgcolor = ft.colors.WHITE
    page.theme_mode = 'light'
    page.window_maximized = True

    # Encabezado
    encabezado = ft.Row([
        ft.Text("Gestión de Pedidos", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.LEFT),
        ft.Row(
            [
                ft.ElevatedButton("Página Principal", width=150),
                ft.ElevatedButton("Movimientos", width=150)
            ],
            alignment=ft.MainAxisAlignment.END,
            expand=True
        )
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # Botones inferiores
    boton_borrar = ft.ElevatedButton("Borrar", width=100, disabled=True)
    boton_insertar = ft.ElevatedButton("Insertar", width=100, on_click=lambda e: mostrar_vent_insertar(e))
    boton_modificar = ft.ElevatedButton("Modificar", width=100, disabled=True)

    botones_inferiores = ft.Row([
        boton_borrar,
        boton_insertar,
        boton_modificar
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

    # Diálogo de inserción
    numero_pedido = ft.TextField(hint_text="Número de Pedido", label="Número de Pedido")
    cliente = ft.TextField(hint_text="Cliente", label="Cliente")
    productos = ft.TextField(hint_text="Productos", label="Productos")
    precio_total = ft.TextField(hint_text="Precio Total", label="Precio Total")
    estado = ft.TextField(hint_text="Estado", label="Estado")
    fecha_creacion = ft.TextField(hint_text="Fecha de Creación", label="Fecha de Creación")
    fecha_modificacion = ft.TextField(hint_text="Fecha de Modificación", label="Fecha de Modificación")

    dialog = ft.AlertDialog(
        shape=ft.RoundedRectangleBorder(radius=5),
        title=ft.Text("Insertar Pedido"),
        content=ft.Column([
            numero_pedido,
            cliente,
            productos,
            precio_total,
            estado,
            fecha_creacion,
            fecha_modificacion
        ], width=page.window_width * 0.33, height=page.window_height * 0.5),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(e)),
            ft.ElevatedButton("Guardar", on_click=lambda e: guardar_pedido(e))
        ],
    )

    def mostrar_vent_insertar(e):
        page.dialog = dialog
        page.dialog.open = True
        page.update()

    def cerrar_dialogo(e):
        page.dialog.open = False
        page.update()

    def guardar_pedido(e):
        # Lógica para guardar pedido
        print("Pedido guardado")
        page.dialog.open = False
        page.update()

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