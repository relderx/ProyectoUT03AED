import flet as ft
from store import store_view  # Importas la vista desde otro archivo

def main(page: ft.Page):
    page.title = 'Sistema de gestión de inventario'
    page.theme_mode = 'light'

    def route_change(route):
        page.views.clear()

        # Vista principal
        if page.route == '/':
            page.views.append(
                ft.View(
                    '/',
                    [
                        ft.AppBar(
                            leading=ft.IconButton(ft.icons.HOME, on_click=lambda _: page.go('/'),
                            title=ft.Text('Sistema de gestión de inventario'),
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            center_title=True
                            ),
                        ),
                        ft.ElevatedButton('Visit Store', on_click=lambda _: page.go('/store')),
                    ],
                )
            )

        # Vista de la tienda
        if page.route == '/store':
            page.views.append(store_view(page))  # Llamas a la vista desde el archivo 'store.py'
        
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == '__main__':
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host='', port=80)
