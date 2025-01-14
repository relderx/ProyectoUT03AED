import flet as ft

from views.movimiento_view.src.main import movimiento_view
from views.producto_view.src.main import producto_view
from views.pedido_view.src.main import pedido_view

def main_view(page: ft.Page):
    page.title = 'Sistema de gestión de inventario'
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.adaptive = True

    def route_change(route):
        page.views.clear()

        # Vista principal
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.AppBar(
                            title=ft.Text("Sistema de gestión de inventario", weight=ft.FontWeight.BOLD, size=36),
                            bgcolor=ft.Colors.INVERSE_PRIMARY,
                            center_title=True,
                            leading=ft.IconButton(ft.Icons.HOME, on_click=lambda _: page.go("/")),  # Botón Home
                            actions=[ft.IconButton(ft.Icons.BRIGHTNESS_6, on_click=lambda _: toggle_theme()), # Botón de cambio de tema (Light <-> Dark)
                            ],
                        ),
                        
                        ft.Row(
                            [
                                ft.ElevatedButton("Gestionar Inventario", on_click=lambda _: page.go("/inventario")),
                                ft.ElevatedButton("Gestionar Movimientos de inventario", on_click=lambda _: page.go("/movimientos")),
                                ft.ElevatedButton("Gestionar Pedidos", on_click=lambda _: page.go("/pedidos")),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,  # Centra los botones horizontalmente
                        ),
                    ],
                )
            )

        if page.route == "/inventario":
            page.views.append(producto_view(page))
            
        if page.route == "/movimientos":
            page.views.append(movimiento_view(page))
            
        if page.route == "/pedidos":
            page.views.append(pedido_view(page))
        
        page.update()

    def toggle_theme():
        # Cambiar entre 'light' y 'dark' al hacer clic
        page.theme_mode = 'dark' if page.theme_mode == 'light' else 'light'
        page.update()  # Actualiza la vista para reflejar el cambio de tema

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == '__main__':
    ft.app(target=main_view, view=ft.AppView.WEB_BROWSER, host='', port=80)