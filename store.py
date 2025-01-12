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
        "/store",
        [
            ft.AppBar(
                title=ft.Text("Store"),
                bgcolor=ft.colors.SURFACE_VARIANT,
                center_title=True,
                leading=ft.IconButton(ft.icons.HOME, on_click=lambda _: page.go("/")),  # Botón Home
                actions=[ft.IconButton(ft.icons.BRIGHTNESS_6, on_click=lambda _: toggle_theme())],  # Botón de cambio de tema
            ),
        ],
    )
