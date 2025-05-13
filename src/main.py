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

    page.appbar = ft.AppBar(
        title=ft.Text("Fake Water Meter"),
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(
                icon=ft.Icons.SETTINGS,
                # on_click=lambda e: page.open(conn_config_dialog)
                on_click=lambda e: conn_config_dialog.on_open(page)
            )
        ],
    )

    form = Form()
    connection_status = ConnectionStatus()
    list_sends = ListSends()

    page.add(
        ft.SafeArea(
            ft.Column(
                [
                    ft.Text("Water Meter", size=30),
                    form,
                    connection_status,
                    list_sends,
                ]
            )
        )
    )


ft.app(main)
