import flet as ft
import time

def main(page: ft.Page):
    page.title = "Prueba para flet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    texto = ft.Text(value="", color="red")
    page.add(texto)

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()
        
    for i in range(10):
        texto.value = f"Step {i}"
        page.update()
        time.sleep(1)
        
        if str(type(page.controls[-1])) != "<class 'flet.core.row.Row'>":
            page.add(ft.Row(
                [
                    ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                    txt_number,
                    ft.IconButton(ft.Icons.ADD, on_click=plus_click),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ))

ft.app(main)