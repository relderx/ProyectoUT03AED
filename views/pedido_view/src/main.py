import flet as ft
from utils.helpers import tabulate_pedidos  # Importar la función para obtener los pedidos

def main(page: ft.Page):
    page.title = 'Gestión de Pedidos'
    page.window_width = 1920
    page.window_height = 1080
    page.bgcolor = ft.colors.WHITE
    page.theme_mode = 'light'
    page.window_maximized = True
    
    def mostrar_vent_insertar(e):
        dialog = ft.AlertDialog(
            shape=ft.RoundedRectangleBorder(radius=5),
            title=ft.Text("Insertar_Movimiento"),
            content=ft.Column([
                ft.TextField(label="Producto"),
                ft.TextField(label="Tipo de Movimiento"),
                ft.TextField(label="Cantidad"),
                ft.TextField(label="Fecha"),
                ft.TextField(label="Comentario"),
                ft.Row([ft.TextField(label="Cositas"), ft.TextField(label="Más cositas")])
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_movimiento),
                ft.ElevatedButton("Guardar", on_click=guardar_movimiento)
            ],
        )
        page.dialog = dialog
        page.dialog.open = True
        page.update()

    def cerrar_movimiento(e):
        page.dialog.open = False
        page.update()

    def guardar_movimiento(e):
        # Lógica para guardar el movimiento
        page.dialog.open = False
        page.update()

    # Encabezado
    encabezado = ft.Row([
        ft.Text('Gestión de Pedidos', size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.LEFT),
        ft.Row(
            [
                ft.ElevatedButton('Página Principal', width=150),
                ft.ElevatedButton('Movimientos', width=150)
            ],
            alignment=ft.MainAxisAlignment.END,
            expand=True
        )
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # Botones inferiores
    botones_inferiores = ft.Row([
        ft.ElevatedButton('Borrar', width=100, disabled=True),
        ft.ElevatedButton('Insertar', width=100, on_click=mostrar_vent_insertar),
        ft.ElevatedButton('Modificar', width=100, disabled=True),
    ], alignment=ft.MainAxisAlignment.END)

    # Encabezados de la tabla
    encabezados_tabla = [
        'Número de Pedido', 'Cliente', 'Productos', 'Precio Total',
        'Estado', 'Fecha de Creación', 'Fecha de Modificación'
    ]

    # Obtener los datos de la base de datos
    datos_tabla = tabulate_pedidos()

    # Variable para mantener los datos mostrados
    datos_mostrados = datos_tabla.copy()

    def transformar_pedido_a_fila(pedido):
        cliente_info = f"{pedido['cliente']} ({pedido['email']})"
        productos_info = "; ".join(
            f"{p['producto']} x{p['unidades']} @ {p['precio_unidad']}€" for p in pedido['productos']
        )
        return [
            pedido['num_pedido'],
            cliente_info,
            productos_info,
            f"{pedido['precio_total']}€",
            pedido['estado'],
            pedido['fecha_creacion'],
            pedido['fecha_modificacion']
        ]

    # Tabla de pedidos
    tabla = ft.DataTable(
        width=1920,
        border_radius=2,
        border=ft.border.all(2, 'red'),
        horizontal_lines=ft.BorderSide(2, 'blue'),
        vertical_lines=ft.BorderSide(2, 'blue'),
        columns=[ft.DataColumn(ft.Text(encabezado)) for encabezado in encabezados_tabla],
        rows=[]
    )

    # Función para actualizar la tabla
    def actualizar_tabla(datos):
        tabla.rows.clear()
        for pedido in datos:
            tabla.rows.append(ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(valor))) for valor in transformar_pedido_a_fila(pedido)]
            ))
        tabla.update()

    # Función para aplicar el filtro
    def aplicar_filtro(e):
        filtro_campo = dropdown_filtro.value
        filtro_valor = input_buscar.value.strip().lower()
        nonlocal datos_mostrados

        datos_filtrados = []
        for pedido in datos_tabla:
            fila = transformar_pedido_a_fila(pedido)
            columna_idx = encabezados_tabla.index(filtro_campo) if filtro_campo != 'Sin filtro' else None

            if columna_idx is not None:
                if filtro_valor in str(fila[columna_idx]).lower():
                    datos_filtrados.append(pedido)
            else:
                if any(filtro_valor in str(celda).lower() for celda in fila):
                    datos_filtrados.append(pedido)

        datos_mostrados = datos_filtrados
        actualizar_tabla(datos_mostrados)

    # Función para ordenar la tabla
    def ordenar_tabla(e):
        columna_ordenar = dropdown_ordenar.value
        nonlocal datos_mostrados

        if columna_ordenar == 'Número de Pedido':
            datos_mostrados.sort(key=lambda x: int(x['num_pedido']))  # Orden numérico
        elif columna_ordenar == 'Cliente':
            datos_mostrados.sort(key=lambda x: x['cliente'].lower())
        elif columna_ordenar == 'Estado':
            datos_mostrados.sort(key=lambda x: x['estado'].lower())
        elif columna_ordenar == 'Fecha de Creación':
            datos_mostrados.sort(key=lambda x: x['fecha_creacion'])

        actualizar_tabla(datos_mostrados)

    # Campo de búsqueda con filtro
    dropdown_filtro = ft.Dropdown(
        label='Filtrar por',
        options=[ft.dropdown.Option(text='Sin filtro')] + 
                [ft.dropdown.Option(text=encabezado) for encabezado in encabezados_tabla],
        width=200,
        value='Sin filtro'
    )

    input_buscar = ft.TextField(label='Buscar', width=200, on_submit=aplicar_filtro)
    boton_filtrar = ft.ElevatedButton('Aplicar Filtro', on_click=aplicar_filtro)

    # Dropdown para ordenar la tabla
    dropdown_ordenar = ft.Dropdown(
        label='Ordenar por',
        options=[ft.dropdown.Option(text=encabezado) for encabezado in encabezados_tabla],
        width=200,
        value='Número de Pedido'
    )
    boton_ordenar = ft.ElevatedButton('Ordenar', on_click=ordenar_tabla)

    # Configuración de búsqueda y filtro
    buscar_filtro = ft.Row([input_buscar, dropdown_filtro, boton_filtrar], alignment=ft.MainAxisAlignment.END)

    # Configuración de orden
    ordenar_filtro = ft.Row([dropdown_ordenar, boton_ordenar], alignment=ft.MainAxisAlignment.END)

    # Estructura de la página
    page.add(
        encabezado,
        botones_inferiores,
        ft.Divider(),
        ft.Text('Pedidos', size=20, weight=ft.FontWeight.BOLD),
        buscar_filtro,
        ordenar_filtro,
        tabla,
        ft.Divider(),
    )

    # Actualizar tabla con datos de la base de datos
    actualizar_tabla(datos_tabla)

ft.app(target=main)