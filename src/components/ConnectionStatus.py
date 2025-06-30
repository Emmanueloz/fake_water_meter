from flet import Row, Text, Colors

from context.AppContext import AppContext
from enums.events import Events


class ConnectionStatus(Row):
    def __init__(self, **kwargs):
        super().__init__()
        AppContext.add_listener(Events.CONNECTION_SUCCESS,
                                self.handler_connection_success)
        AppContext.add_listener(Events.CONNECTION_ERROR,
                                self.handler_connection_error)

        AppContext.add_listener(Events.CONNECTION_CLOSED, self.handler_closed)

        AppContext.add_listener(Events.SET_LOOP_STARTED,
                                self.handler_loop_started)

        self.message = Text(
            "Disconnected",
            size=20,
        )
        self.controls = [
            Text("Status", size=20),
            self.message,
        ]

    def handler_connection_success(self, message: str):
        print(f"Connection success: {message}")
        self.message.value = message
        self.message.color = Colors.GREEN_500

    def handler_connection_error(self, message: str):
        print(f"Connection error: {message}")
        self.message.value = message
        self.message.color = Colors.RED_500

    def handler_closed(self, message: str):
        print(f"Connection closed: {message}")
        self.message.value = message
        self.message.color = Colors.WHITE

    def handler_loop_started(self, is_started: bool):
        socket = AppContext.get_socket()
        if not socket:
            return

        self.message.value = "Loop started" if is_started else "Connected"
        self.message.color = Colors.GREEN_500
