import flet as ft
from store import store_view  # Importas la vista desde otro archivo

class UI(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        
        self.container = ft.ResponsiveRow(
            
        )
        
    def build(self):
        return super().container

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
                            title=ft.Text("Sistema de gestión de inventario", weight=ft.FontWeight.BOLD, size=38),
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            center_title=True,
                            leading=ft.IconButton(ft.icons.HOME, on_click=lambda _: page.go("/")),  # Botón Home
                            actions=[ft.IconButton(ft.icons.BRIGHTNESS_6, on_click=lambda _: toggle_theme()), # Botón de cambio de tema (Light <-> Dark)
                            ],
                        ),
                        
                        ft.Row(
                            [
                                ft.ElevatedButton("Gestionar Inventario", on_click=lambda _: page.go("/store")),
                                ft.ElevatedButton("Gestionar Movimientos de inventario", on_click=lambda _: page.go("/store")),
                                ft.ElevatedButton("Gestionar Pedidos", on_click=lambda _: page.go("/store")),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,  # Centra los botones horizontalmente
                        ),
                    ],
                )
            )

        # Vista de la tienda
        if page.route == "/store":
            page.views.append(store_view(page))  # Llamas a la vista desde el archivo 'store.py'
        
        page.update()

    def toggle_theme():
        # Cambiar entre 'light' y 'dark' al hacer clic
        if page.theme_mode == 'light':
            page.theme_mode = 'dark'
        else:
            page.theme_mode = 'light'
        page.update()  # Actualiza la vista para reflejar el cambio de tema

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(main_view, view=ft.AppView.WEB_BROWSER, host='', port=80)
