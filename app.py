import flet as ft

from views.producto_view.src.main import main as create_producto_page

if __name__ == "__main__":
    ft.app(target=create_producto_page, view=ft.AppView.WEB_BROWSER, host='', port=80)