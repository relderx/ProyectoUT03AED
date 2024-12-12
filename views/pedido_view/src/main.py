import flet as ft

def main(page: ft.Page):
    page.title = "Movimiento de Inventario"
    page.window_width = 1920
    page.window_height = 1080

    # Encabezado
    encabezado = ft.Text("Movimiento de Inventario", size=30, weight=ft.FontWeight.BOLD)

    # Botones superiores
    botones_superiores = ft.Row([
        ft.ElevatedButton("Página Principal", width=150),
        ft.ElevatedButton("Pedidos", width=150),
    ], alignment=ft.MainAxisAlignment.END)

        # Botones inferiores
    botones_inferiores = ft.Row([
        ft.ElevatedButton("Borrar", width=100, disabled=True),
        ft.ElevatedButton("Insertar", width=100),
        ft.ElevatedButton("Modificar", width=100, disabled=True),
    ], alignment=ft.MainAxisAlignment.END)

    # Tabla de productos
    encabezados_tabla = ["Producto", "Tipo de Movimiento", "Cantidad", "Fecha", "Comentario"]
    datos_tabla = [
        ["Producto1", "Entrada", "2", "", ""],
        ["Producto2", "Salida", "5", "", ""],
        ["Producto3", "", "1", "", ""],
    ]

    tabla = ft.DataTable(
        width=1920,
        border_radius=2,
        border=ft.border.all(2, "red"),
        horizontal_lines=ft.BorderSide(2, "blue"),
        vertical_lines=ft.BorderSide(2, "blue"),
        columns=[ft.DataColumn(ft.Text(encabezado)) for encabezado in encabezados_tabla],
        rows=[
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(dato)) for dato in fila]
            ) for fila in datos_tabla
        ],

    )

    # Campo de búsqueda
    buscar_filtro = ft.Row([
        ft.TextField(label="Buscar", width=200),
        ft.IconButton(icon=ft.icons.FILTER_LIST),
    ], alignment=ft.MainAxisAlignment.END)

    # Estructura de la página
    page.add(
        encabezado,
        botones_superiores,
        botones_inferiores,
        ft.Divider(),
        ft.Text("Productos", size=20, weight=ft.FontWeight.BOLD),
        tabla,
        buscar_filtro,
        ft.Divider(),
  
    )

ft.app(target=main)
