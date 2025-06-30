from flet import ElevatedButton, Row,Colors


class ControlButtons(Row):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.btn_connect = ElevatedButton(
            text="Connect",
            color=Colors.SURFACE,
            bgcolor=Colors.SURFACE_TINT,
        )
        self.btn_disconnect = ElevatedButton(
            text="Disconnect",
            visible=False,
            color=Colors.SURFACE,
            bgcolor=Colors.SURFACE_TINT,
        )
        self.btn_clear = ElevatedButton(
            text="Clear",
        )

        self.controls = [
            self.btn_connect,
            self.btn_disconnect,
            self.btn_clear
        ]
