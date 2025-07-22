from flet import ElevatedButton, Row, Colors

from context.AppContext import AppContext
from service.database import DatabaseManager
from service.database import ConnectionConfigModel, DatabaseManager
from enums.events import Events


class ControlButtons(Row):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        AppContext.add_listener(
            Events.CONNECTION_SUCCESS, self.handler_con_success)
        AppContext.add_listener(Events.CONNECTION_ERROR,
                                self.handler_con_error)
        AppContext.add_listener(Events.CONNECTION_CLOSED,
                                self.handler_con_closed)
        self.btn_connect = ElevatedButton(
            text="Connect",
            color=Colors.SURFACE,
            bgcolor=Colors.SURFACE_TINT,
            on_click=self.on_connect_click
        )
        self.btn_disconnect = ElevatedButton(
            text="Disconnect",
            visible=False,
            color=Colors.SURFACE,
            bgcolor=Colors.SURFACE_TINT,
            on_click=self.on_disconnect_click

        )
        self.btn_clear = ElevatedButton(
            text="Clear",
            on_click=self.on_clear_click
        )

        self.controls = [
            self.btn_connect,
            self.btn_disconnect,
            self.btn_clear
        ]

    def on_connect_click(self, e):

        conn = DatabaseManager.get_first(ConnectionConfigModel)  # type: ignore

        host = conn["host"] if conn else "http://127.0.0.1:8000/"
        token = conn["token"] if conn else ""

        AppContext.set_socket(host, token)

    def on_disconnect_click(self, e):
        AppContext.close_socket()
        AppContext.set_loop_started(False)

    def handler_con_success(self, message: str):
        print(message)
        self.btn_connect.visible = False
        self.btn_disconnect.visible = True

    def handler_con_error(self, message: str):
        print(message)
        self.btn_connect.visible = True
        self.btn_disconnect.visible = False

    def handler_con_closed(self, message: str):
        print(message)
        self.btn_connect.visible = True
        self.btn_disconnect.visible = False

    def on_clear_click(self, e):
        AppContext.clear_list()
