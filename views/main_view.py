import flet as ft

from views.movimiento_view import movimiento_view
from views.producto_view import producto_view
from views.pedido_view import pedido_view

# Configuración principal de la vista de la aplicación
def main_view(page: ft.Page):
    page.title = "Sistema de gestión de inventario"  # Título de la aplicación
    page.theme_mode = ft.ThemeMode.SYSTEM  # Tema basado en el sistema
    page.adaptive = True  # Ajusta automáticamente el diseño a diferentes dispositivos

    # Manejo de rutas para navegar entre las vistas
    def route_change(route):
        page.views.clear()  # Limpiar vistas anteriores

        # Vista principal
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        # Barra de navegación superior
                        ft.AppBar(
                            title=ft.Text(
                                "Sistema de gestión de inventario",
                                weight=ft.FontWeight.BOLD,
                                size=36,
                            ),
                            bgcolor=ft.Colors.INVERSE_PRIMARY,
                            center_title=True,
                            leading=ft.IconButton(
                                ft.Icons.HOME, on_click=lambda _: page.go("/")
                            ),  # Botón Home
                            actions=[
                                ft.IconButton(
                                    ft.Icons.BRIGHTNESS_6,
                                    on_click=lambda _: toggle_theme(),
                                )
                            ],  # Cambio de tema
                        ),
                        # Botones para acceder a las diferentes secciones
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Gestionar Inventario",
                                    on_click=lambda _: page.go("/inventario"),
                                ),
                                ft.ElevatedButton(
                                    "Gestionar Movimientos de inventario",
                                    on_click=lambda _: page.go("/movimientos"),
                                ),
                                ft.ElevatedButton(
                                    "Gestionar Pedidos",
                                    on_click=lambda _: page.go("/pedidos"),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,  # Centra los botones horizontalmente
                        ),
                    ],
                )
            )

        # Vista para gestionar productos
        if page.route == "/inventario":
            page.views.append(producto_view(page))

        # Vista para gestionar movimientos
        if page.route == "/movimientos":
            page.views.append(movimiento_view(page))

        # Vista para gestionar pedidos
        if page.route == "/pedidos":
            page.views.append(pedido_view(page))

        page.update()  # Actualiza la página después de cambiar la ruta

    # Alternar entre temas claro y oscuro
    def toggle_theme():
        page.theme_mode = (
            "dark" if page.theme_mode == "light" else "light"
        )  # Cambia el modo de tema
        page.update()  # Actualiza la vista para reflejar el cambio

    # Elimina la vista superior del historial de navegación
    def view_pop(view):
        page.views.pop()  # Elimina la vista actual
        top_view = page.views[-1]  # Obtiene la vista anterior
        page.go(top_view.route)  # Navega a la vista anterior

    # Asignar manejadores de eventos para el cambio de rutas y la navegación hacia atrás
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)  # Navega a la ruta actual


if __name__ == "__main__":
    ft.app(target=main_view, view=ft.AppView.WEB_BROWSER, host="", port=80)
