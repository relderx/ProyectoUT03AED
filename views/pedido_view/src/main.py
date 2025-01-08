import flet as ft

def main(page: ft.Page):
    page.title = 'Pedidos'
    page.window_width = 1920
    page.window_height = 1080
    page.bgcolor = ft.colors.WHITE
    page.theme_mode = 'light'
    page.window_maximized = True

    # Encabezado
    encabezado = ft.Row([
        ft.Text('Movimiento de Inventario', size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.LEFT),
        ft.Row(
            [
                ft.ElevatedButton('Página Principal', width=150),
                ft.ElevatedButton('Pedidos', width=150)
            ],
            alignment=ft.MainAxisAlignment.END,
            expand=True
        )
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # Botones inferiores
    botones_inferiores = ft.Row([
        ft.ElevatedButton('Borrar', width=100, disabled=True),
        ft.ElevatedButton('Insertar', width=100),
        ft.ElevatedButton('Modificar', width=100, disabled=True),
    ], alignment=ft.MainAxisAlignment.END)

    # Encabezados y datos ficticios
    encabezados_tabla = ['Producto', 'Tipo de Movimiento', 'Cantidad', 'Fecha', 'Comentario']
    datos_tabla = [
        ['Producto1', 'Entrada', 5, '2024-12-01', 'Nuevo stock recibido'],
        ['Producto2', 'Salida', 3, '2024-12-02', 'Pedido cliente A'],
        ['Producto3', 'Entrada', 10, '2024-12-03', 'Reabastecimiento semanal'],
        ['Producto4', 'Salida', 7, '2024-12-04', 'Devolución cliente B'],
        ['Producto5', 'Entrada', 20, '2024-12-05', 'Promoción de temporada'],
        ['Producto6', 'Salida', 15, '2024-12-06', 'Venta en tienda física'],
        ['Producto7', 'Entrada', 8, '2024-12-07', 'Reposición de inventario'],
        ['Producto8', 'Salida', 4, '2024-12-08', 'Pedido cliente C'],
        ['Producto9', 'Entrada', 12, '2024-12-09', 'Nuevo lote de proveedores'],
        ['Producto10', 'Salida', 2, '2024-12-10', 'Devolución de productos defectuosos']
    ]

    # Variable para mantener los datos mostrados (filtrados y/o ordenados)
    datos_mostrados = datos_tabla.copy()  # Inicialmente, son todos los datos

    # Función para actualizar la tabla
    def actualizar_tabla(datos):
        tabla.rows.clear()  # Limpiar las filas actuales de la tabla
        for fila in datos:
            tabla.rows.append(ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(dato))) for dato in fila]
            ))
        tabla.update()  # Actualizar la tabla visualmente

    # Función para filtrar datos
    def aplicar_filtro(e):
        filtro_campo = dropdown_filtro.value
        filtro_valor = input_buscar.value.strip().lower()  # Convertir a minúsculas y eliminar espacios

        nonlocal datos_mostrados
        if filtro_campo == 'Sin filtro':  # Sin filtro seleccionado
            # Mostrar filas donde el valor buscado aparece en cualquier columna
            datos_mostrados = [fila for fila in datos_tabla if any(filtro_valor in str(dato).lower() for dato in fila)]
        else:  # Filtrar según la columna seleccionada
            indice = encabezados_tabla.index(filtro_campo)
            datos_mostrados = [fila for fila in datos_tabla if filtro_valor in str(fila[indice]).lower()]

        actualizar_tabla(datos_mostrados)  # Actualizar la tabla con los datos filtrados

    # Función para ordenar la tabla
    def ordenar_tabla(e):
        columna_ordenar = dropdown_ordenar.value
        indice_columna = encabezados_tabla.index(columna_ordenar)

        nonlocal datos_mostrados
        # Ordenar los datos mostrados actuales
        datos_mostrados = sorted(datos_mostrados, key=lambda x: str(x[indice_columna]).lower())

        actualizar_tabla(datos_mostrados)  # Actualizar la tabla con los datos ordenados

    # Tabla de productos
    tabla = ft.DataTable(
        width=1920,
        border_radius=2,
        border=ft.border.all(2, 'red'),
        horizontal_lines=ft.BorderSide(2, 'blue'),
        vertical_lines=ft.BorderSide(2, 'blue'),
        columns=[ft.DataColumn(ft.Text(encabezado)) for encabezado in encabezados_tabla],
        rows=[
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(dato))) for dato in fila]
            ) for fila in datos_tabla
        ],
    )

    # Contenedor con scroll para la tabla
    tabla_con_scroll = ft.Column(
        controls=[tabla],
        height=500,  # Puedes ajustar la altura según sea necesario
        scroll=ft.ScrollMode.AUTO  # Habilitar el scroll vertical
    )

    # Campo de búsqueda con filtro
    dropdown_filtro = ft.Dropdown(
        label='Filtrar por',
        options=[ft.dropdown.Option(text='Sin filtro')] + [ft.dropdown.Option(text=encabezado) for encabezado in encabezados_tabla],
        width=200,
        value='Sin filtro'  # Sin filtro seleccionado por defecto
    )

    input_buscar = ft.TextField(label='Buscar', width=200, on_submit=aplicar_filtro)  # Aplicar filtro con Enter
    boton_filtrar = ft.ElevatedButton('Aplicar Filtro', on_click=aplicar_filtro)

    # Dropdown para ordenar la tabla
    dropdown_ordenar = ft.Dropdown(
        label='Ordenar por',
        options=[ft.dropdown.Option(text=encabezado) for encabezado in encabezados_tabla],
        width=200,
        value=encabezados_tabla[0]  # Ordenar por la primera columna por defecto
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
        ft.Text('Productos', size=20, weight=ft.FontWeight.BOLD),
        buscar_filtro,
        ordenar_filtro,
        tabla_con_scroll,
        ft.Divider(),
    )

ft.app(target=main)
