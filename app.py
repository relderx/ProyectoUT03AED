import flet as ft
from views.main_view import main_view

if __name__ == "__main__":
    ft.app(target=main_view, view=ft.AppView.WEB_BROWSER, host='', port=80)