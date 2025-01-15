import os
import sys
import flet as ft

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from utils.helpers import tabulate_pedidos
from utils.db import add_pedido, delete_pedido, update_pedido
from models.pedidos import Pedido

def obtener_datos():
    try:
        datos = tabulate_pedidos() or []
        print("Datos obtenidos:", datos)  # Verifica la estructura
        return datos
    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return []

def pedido_view(page: ft.Page):
    page.title = "Gestión de Pedidos"

    # Variables globales
    page.val_num_pedido = None
    page.val_nombre_cliente = None
    page.val_email_cliente = None
    page.val_telefono_cliente = None
    page.val_productos = None
    page.val_estado = None
    pedidos_seleccionados_ids = []

    # Obtener datos originales para usar en filtrado
    datos_originales = obtener_datos()

    def aplicar_filtro(e):
        filtro_seleccionado = filtro_dropdown.value
        texto_busqueda = texto_buscar.value.lower()

        if filtro_seleccionado == "Ningún filtro" or not texto_busqueda:
            datos_filtrados = datos_originales
        else:
            indice_columna = encabezados_tabla.index(filtro_seleccionado) - 1
            datos_filtrados = [
                fila for fila in datos_originales
                if texto_busqueda in str(fila[indice_columna]).lower()
            ]

        tabla.rows.clear()
        tabla.rows.extend(crear_filas(datos_filtrados))
        tabla.update()

    def aplicar_orden(e):
        orden_seleccionado = orden_dropdown.value
        if orden_seleccionado:
            indice_columna = encabezados_tabla.index(orden_seleccionado) - 1
            datos_ordenados = sorted(
                datos_originales,
                key=lambda x: str(x[indice_columna]).lower()
            )
            tabla.rows.clear()
            tabla.rows.extend(crear_filas(datos_ordenados))
            tabla.update()

    def toggle_theme():
        page.theme_mode = 'dark' if page.theme_mode == 'light' else 'light'
        page.update()

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
        page.val_telefono_cliente = e.control.value
        page.update()

    def cambio_productos(e):
        page.val_productos = e.control.value
        page.update()

    def cambio_estado(e):
        page.val_estado = e.control.value
        page.update()

    def cerrar_dialogo(e):
        page.dialog.open = False
        pedidos_seleccionados_ids.clear()
        boton_modificar.disabled = True
        boton_borrar.disabled = True
        page.update()

    def mostrar_notificacion(mensaje):
        page.snack_bar = ft.SnackBar(ft.Text(mensaje), bgcolor=ft.colors.GREEN)
        page.snack_bar.open = True
        page.update()

    def guardar_insertar(e):
        try:
            productos_lista = []
            for producto in productos.value.split(","):
                partes = producto.split(" x ")
                nombre = partes[0].strip()
                unidades_precio = partes[1].split(" (")
                unidades = int(unidades_precio[0].strip())
                precio = float(unidades_precio[1].strip(")"))
                productos_lista.append({"producto": nombre, "unidades": unidades, "precio_unidad": precio})

            nuevo_pedido = Pedido(
                num_pedido=num_pedido.value.strip(),
                cliente={
                    "nombre": nombre_cliente.value.strip(),
                    "email": email_cliente.value.strip(),
                    "telefono": telefono_cliente.value.strip()
                },
                productos=productos_lista,
                estado=estado.value.strip()
            )

            add_pedido(nuevo_pedido)
            actualizar_tabla()
            cerrar_dialogo(e)
            mostrar_notificacion("Pedido insertado correctamente.")
        except Exception as ex:
            mostrar_notificacion(f"Error al insertar pedido: {ex}")

    def guardar_modificar(e):
        try:
            if pedidos_seleccionados_ids:
                pedido_id = pedidos_seleccionados_ids[0]
                productos_lista = []
                for producto in productos.value.split(","):
                    partes = producto.split(" x ")
                    nombre = partes[0].strip()
                    unidades_precio = partes[1].split(" (")
                    unidades = int(unidades_precio[0].strip())
                    precio = float(unidades_precio[1].strip(")"))
                    productos_lista.append({"producto": nombre, "unidades": unidades, "precio_unidad": precio})

                datos_actualizados = {
                    "num_pedido": num_pedido.value.strip(),
                    "cliente": {
                        "nombre": nombre_cliente.value.strip(),
                        "email": email_cliente.value.strip(),
                        "telefono": telefono_cliente.value.strip()
                    },
                    "productos": productos_lista,
                    "estado": estado.value.strip()
                }

                update_pedido(pedido_id, datos_actualizados)
                actualizar_tabla()
                cerrar_dialogo(e)
        except Exception as ex:
            mostrar_notificacion(f"Error al modificar pedido: {ex}")

    def borrar_pedidos(e):
        try:
            for pedido_id in pedidos_seleccionados_ids:
                delete_pedido(pedido_id)
            actualizar_tabla()
            pedidos_seleccionados_ids.clear()
            boton_borrar.disabled = True
            boton_modificar.disabled = True
            page.update()
        except Exception as ex:
            mostrar_notificacion(f"Error al borrar pedidos: {ex}")

    def actualizar_tabla():
        try:
            datos_tabla = obtener_datos()
            tabla.rows.clear()
            tabla.rows.extend(crear_filas(datos_tabla))
            tabla.update()
        except Exception as ex:
            mostrar_notificacion(f"Error al actualizar la tabla: {ex}")

    def mostrar_vent_insertar(e):
        num_pedido.value = ""
        nombre_cliente.value = ""
        email_cliente.value = ""
        telefono_cliente.value = ""
        productos.value = ""
        estado.value = ""
        page.dialog = ft.AlertDialog(
            title=ft.Text("Insertar Pedido"),
            content=ft.Column([
                num_pedido,
                nombre_cliente,
                email_cliente,
                telefono_cliente,
                productos,
                estado
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialogo),
                ft.ElevatedButton("Guardar", on_click=guardar_insertar)
            ]
        )
        page.dialog.open = True
        page.update()

    def mostrar_vent_modificar(e):
        if len(pedidos_seleccionados_ids) != 1:
            mostrar_notificacion("Selecciona un único pedido para modificar.")
            return

        pedido_id = pedidos_seleccionados_ids[0]
        pedido = next((p for p in obtener_datos() if p[0] == pedido_id), None)
        if not pedido:
            mostrar_notificacion("Pedido no encontrado.")
            return

        num_pedido.value = pedido[0]
        nombre_cliente.value = pedido[1].get("nombre", "")
        email_cliente.value = pedido[1].get("email", "")
        telefono_cliente.value = pedido[1].get("telefono", "")
        productos.value = ", ".join(
            [f"{p['producto']} x {p['unidades']} ({p['precio_unidad']})" for p in pedido[2]]
        )
        estado.value = pedido[3]
        page.dialog = ft.AlertDialog(
            title=ft.Text("Modificar Pedido"),
            content=ft.Column([
                num_pedido,
                nombre_cliente,
                email_cliente,
                telefono_cliente,
                productos,
                estado
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialogo),
                ft.ElevatedButton("Guardar", on_click=guardar_modificar)
            ]
        )
        page.dialog.open = True
        page.update()

    num_pedido = ft.TextField(label="Número de Pedido", hint_text="Escribe el número del pedido", on_submit=guardar_insertar)
    nombre_cliente = ft.TextField(label="Nombre del Cliente", hint_text="Escribe el nombre del cliente", on_submit=guardar_insertar)
    email_cliente = ft.TextField(label="Email del Cliente", hint_text="Escribe el email del cliente", on_submit=guardar_insertar)
    telefono_cliente = ft.TextField(label="Teléfono del Cliente", hint_text="Escribe el teléfono del cliente", on_submit=guardar_insertar)
    productos = ft.TextField(label="Productos", hint_text="Formato: producto x unidades (precio),...", on_submit=guardar_insertar)
    estado = ft.TextField(label="Estado", hint_text="Pendiente, Enviado, Entregado, Cancelado", on_submit=guardar_insertar)

    encabezados_tabla = [
        "Seleccionar",
        "Número de Pedido",
        "Cliente",
        "Productos",
        "Estado",
        "Fecha de Creación",
        "Fecha de Modificación"
    ]

    def crear_filas(datos):
        filas = []
        if not datos:
            filas.append(ft.DataRow(cells=[ft.DataCell(ft.Text("No hay datos disponibles")) for _ in encabezados_tabla]))
            return filas

        for fila in datos:
            # Asegura que cada fila tenga el número correcto de columnas
            fila.extend(["" for _ in range(len(encabezados_tabla) - len(fila) - 1)])
            checkbox = ft.Checkbox(value=False, on_change=lambda e: seleccionar_pedido(e, fila[0]))
            celdas = [ft.DataCell(checkbox)] + [ft.DataCell(ft.Text(str(dato))) for dato in fila]
            filas.append(ft.DataRow(cells=celdas))
        return filas

    def seleccionar_pedido(e, pedido_id):
        if e.control.value:
            pedidos_seleccionados_ids.append(pedido_id)
        else:
            pedidos_seleccionados_ids.remove(pedido_id)
        boton_borrar.disabled = len(pedidos_seleccionados_ids) == 0
        boton_modificar.disabled = len(pedidos_seleccionados_ids) != 1
        page.update()

    tabla = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(h)) for h in encabezados_tabla],
        rows=crear_filas(datos_originales)
    )

    boton_borrar = ft.ElevatedButton("Borrar", on_click=lambda e: borrar_pedidos(e), disabled=True)
    boton_modificar = ft.ElevatedButton("Modificar", on_click=mostrar_vent_modificar, disabled=True)
    boton_insertar = ft.ElevatedButton("Insertar", on_click=mostrar_vent_insertar)

    buscar_filtro = ft.Row([
        texto_buscar := ft.TextField(label="Buscar", width=200),
        filtro_dropdown := ft.Dropdown(
            label="Filtrar por",
            options=[ft.dropdown.Option("Ningún filtro")] + [
                ft.dropdown.Option(encabezado) for encabezado in encabezados_tabla[1:]
            ],
            width=200,
            value="Ningún filtro"
        ),
        ft.ElevatedButton("Aplicar Filtro", on_click=aplicar_filtro)
    ], alignment=ft.MainAxisAlignment.END)

    ordenar_filtro = ft.Row([
        orden_dropdown := ft.Dropdown(
            label="Ordenar por",
            options=[
                ft.dropdown.Option(encabezado) for encabezado in encabezados_tabla[1:]
            ],
            width=200,
            value="Número de Pedido"
        ),
        ft.ElevatedButton("Ordenar", on_click=aplicar_orden)
    ], alignment=ft.MainAxisAlignment.END)

    botones_inferiores = ft.Row([
        boton_borrar,
        boton_insertar,
        boton_modificar
    ], alignment=ft.MainAxisAlignment.END)

    encabezado = ft.Row([
        ft.Text("Gestión de Pedidos", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.LEFT)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    return ft.View(
        "/inventario",
        [
            ft.AppBar(
                title=ft.Text("Gestión de Pedidos", weight=ft.FontWeight.BOLD, size=36), 
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
    ft.app(target=pedido_view)
