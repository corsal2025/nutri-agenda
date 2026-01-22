import flet as ft

try:
    print(ft.Colors.RED)
except AttributeError as e:
    print(f"CAUGHT ERROR: {e}")
except Exception as e:
    print(f"OTHER ERROR: {e}")
