import flet as ft

def store_view(page: ft.Page):
    
    def toggle_theme():
        # Cambiar entre 'light' y 'dark' al hacer clic
        if page.theme_mode == 'light':
            page.theme_mode = 'dark'
        else:
            page.theme_mode = 'light'
        page.update()  # Actualiza la vista para reflejar el cambio de tema
        
    return ft.View(
        "/inventario",
        [
            ft.AppBar(
                title=ft.Text("Inventario", weight=ft.FontWeight.BOLD, size=36),
                bgcolor=ft.Colors.INVERSE_PRIMARY,
                center_title=True,
                leading=ft.IconButton(ft.Icons.HOME, on_click=lambda _: page.go("/")),  # Botón Home
                actions=[ft.IconButton(ft.Icons.BRIGHTNESS_6, on_click=lambda _: toggle_theme()), # Botón de cambio de tema (Light <-> Dark)
                ],
            ),
        ],
    )
