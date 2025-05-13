from flet import AlertDialog, Column, TextField, Colors, TextButton, ElevatedButton, Text, Page

from service.database import DatabaseManager, ConnectionConfigModel


class ConnConfigDialog(AlertDialog):

    host_field = TextField(
        value="http://127.0.0.1:8000/",
        label="Host",
        border_color=Colors.SURFACE_TINT,
    )

    token_field = TextField(
        value="",
        label="Token",
        password=True,
        multiline=True,
        can_reveal_password=True,
        border_color=Colors.SURFACE_TINT,

    )

    def __init__(self):
        super().__init__()

        self.title = Text("Connection Config")
        self.content = Column(
            controls=[
                self.host_field,
                self.token_field,
            ],
            width=400,
            height=250,
        )

        self.on_dismiss = lambda e: print("Cancel")

        self.cancel = TextButton(
            text="Cancel",
            on_click=self.cancel_click
        )

        self.confirm = ElevatedButton(
            text="Confirm",
            color=Colors.SURFACE,
            bgcolor=Colors.SURFACE_TINT,
            on_click=self.confirm_click,
            visible=False
        )

        self.btn_update = ElevatedButton(
            text="Update",
            color=Colors.SURFACE,
            bgcolor=Colors.SURFACE_TINT,
            on_click=self.btn_update_click,
            visible=False
        )

        self.actions = [
            self.cancel,
            self.btn_update,
            self.confirm,
        ]

    def cancel_click(self, e):
        print("Cancel")
        self.open = False
        self.update()

    def confirm_click(self, e):
        print("Confirm")
        self.open = False
        self.update()

        model = ConnectionConfigModel(
            host=self.host_field.value, token=self.token_field.value)
        DatabaseManager.add(model)

    def btn_update_click(self, e):
        print("Update")
        self.open = False
        self.update()

        model = DatabaseManager.get_first(ConnectionConfigModel)

        if model:
            id = model["id"]
            host = self.host_field.value
            token = self.token_field.value
            DatabaseManager.update(
                ConnectionConfigModel,
                id,
                host=host,
                token=token
            )

    def on_open(self, page: Page):
        print("Open")

        model = DatabaseManager.get_first(ConnectionConfigModel)
        print(model)

        if model:
            self.host_field.value = model["host"]
            self.token_field.value = model["token"]
            self.btn_update.visible = True
            self.confirm.visible = False
        else:
            self.btn_update.visible = False
            self.confirm.visible = True

        page.open(self)
        print("Opened")
        self.update()
