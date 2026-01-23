import flet as ft
import logging

logging.basicConfig(level=logging.INFO)

def main(page: ft.Page):
    page.add(ft.Text("Hello World"))

try:
    ft.app(target=main, web_renderer="html", port=8552, view=ft.AppView.WEB_BROWSER)
    print("SUCCESS: Started with html renderer")
except Exception as e:
    print(f"FAILURE: {e}")
