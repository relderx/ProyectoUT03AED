import flet as ft

def store_view(page: ft.Page):
    return ft.View(
        "/store",
        [
            ft.AppBar(
                title=ft.Text("Store"),
                bgcolor=ft.colors.SURFACE_VARIANT,
                center_title=True,
                leading=ft.IconButton(ft.icons.HOME, on_click=lambda _: page.go("/")),
            ),
            ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
        ],
    )
