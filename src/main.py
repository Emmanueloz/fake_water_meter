import flet as ft
from components.ConnConfig import ConnConfigDialog
from components.ListSends import ListSends
from components.ConnectionStatus import ConnectionStatus
from components.Form import Form
from context.AppContext import AppContext
from service.database import DatabaseManager


DatabaseManager.init()


async def main(page: ft.Page):
    AppContext.set_page(page)
    conn_config_dialog = ConnConfigDialog()

    # Configuración clave para comportamiento nativo
    page.scroll = ft.ScrollMode.HIDDEN  # Scroll activado pero sin barra visible
    page.auto_scroll = False  # Evita saltos automáticos

    page.appbar = ft.AppBar(
        title=ft.Text("Fake Water Meter"),
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(
                icon=ft.icons.SETTINGS,
                on_click=lambda e: conn_config_dialog.on_open(page)
            )
        ],
    )

    # Contenedor principal con expansión controlada
    content = ft.Column(
        scroll=ft.ScrollMode.AUTO,  # Scroll manual
        spacing=20,  # Espacio entre controles
        controls=[
            ft.Text("Water Meter", size=30),
            Form(),  # Asegúrate que no tenga auto-scroll interno
            ConnectionStatus(),
            ListSends(),  # Verifica que sus hijos no fuerzen scroll
        ]
    )

    # Layout final (ajusta el padding para Android)
    page.add(
        ft.Container(
            content=content,
            # Evita cortes en bordes
            padding=ft.padding.only(top=10, bottom=50),
            expand=True  # Ocupa todo el espacio disponible
        )
    )


ft.app(main)
