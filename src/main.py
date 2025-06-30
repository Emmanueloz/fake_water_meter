import flet as ft
from flet import MainAxisAlignment
from components.TabForms import TabForms
from components.ConnConfig import ConnConfigDialog
from components.ListSends import ListSends
from components.ConnectionStatus import ConnectionStatus
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
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            ft.IconButton(
                icon=ft.Icons.SETTINGS,
                on_click=lambda e: conn_config_dialog.on_open(page)
            )
        ],
    )

    # Contenido responsivo
    content = ft.ResponsiveRow(
        spacing=20,
        run_spacing=20,
        expand=True,
        controls=[
            # Columna izquierda (Form y ConnectionStatus)
            ft.Column(
                col={"sm": 12, "md": 6},
                spacing=20,
                expand=True,
                controls=[
                    ft.Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Water Meter", size=30),
                            ConnectionStatus()
                        ],
                    ),
                    ft.Container(
                        content=TabForms(),
                        expand=True,
                        height=500,
                    )
                ]
            ),
            ListSends(
                col={"sm": 12, "md": 6},
            )
        ]
    )

    # Layout final
    page.add(content)


ft.app(main)
