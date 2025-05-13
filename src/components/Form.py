import time
from flet import Container, Colors, TextField, Row, Column, ElevatedButton, Dropdown, DropdownOption

from context.AppContext import AppContext
from enums.events import Events
from service.database import ConnectionConfigModel, DatabaseManager, RecordModel


class Form(Container):

    list_records: list[RecordModel] = []
    list_options: list[DropdownOption] = []

    name_record = TextField(
        value="New",
        label="Name",
        border_color=Colors.SURFACE_TINT,
        expand=True,
    )

    color_r_field = TextField(
        value="0",
        label="Red",
        border_color=Colors.SURFACE_TINT,
        expand=True,
    )
    color_g_field = TextField(
        value="0",
        label="Green",
        border_color=Colors.SURFACE_TINT,
        expand=True,
    )

    color_b_field = TextField(
        value="0",
        label="Blue",
        border_color=Colors.SURFACE_TINT,
        expand=True,
    )

    color_filed = Row(
        spacing=5,
        controls=[
            color_r_field,
            color_g_field,
            color_b_field,
        ]
    )

    conductivity_field = TextField(
        value="70",
        label="Conductivity",
        border_color=Colors.SURFACE_TINT,
    )

    ph_field = TextField(
        value="3.5",
        label="pH",
        border_color=Colors.SURFACE_TINT,
    )

    temperature_field = TextField(
        value="16",
        label="Temperature",
        border_color=Colors.SURFACE_TINT,
    )

    tds_field = TextField(
        value="60",
        label="TDS",
        border_color=Colors.SURFACE_TINT,
    )

    turbidity_field = TextField(
        value="70",
        label="Turbidity",
        border_color=Colors.SURFACE_TINT,

    )

    def __init__(self):
        super().__init__()

        AppContext.add_listener(
            Events.CONNECTION_SUCCESS, self.handler_con_success)
        AppContext.add_listener(Events.CONNECTION_ERROR,
                                self.handler_con_error)
        AppContext.add_listener(Events.CONNECTION_CLOSED,
                                self.handler_con_closed)

        AppContext.add_listener(Events.SET_LOOP_STARTED,
                                self.handler_loop_started)

        self.select_records = Dropdown(
            options=[],
            label="Select Record",
            value="New",
            border_color=Colors.SURFACE_TINT,
            expand=True,
            on_change=self.select_records_change
        )

        self.btn_save_record = ElevatedButton(
            text="Save",
            color=Colors.SURFACE,
            bgcolor=Colors.SURFACE_TINT,
            on_click=self.btn_save_record_click,
            visible=True
        )

        self.btn_update_record = ElevatedButton(
            text="Update",
            color=Colors.SURFACE,
            bgcolor=Colors.SURFACE_TINT,
            on_click=self.btn_update_record_click,
            visible=False
        )

        self.btn_connect = ElevatedButton(
            text="Start",
            color=Colors.SURFACE,
            bgcolor=Colors.SURFACE_TINT,
            on_click=self.btn_click
        )

        self.btn_disconnect = ElevatedButton(
            text="Stop",
            color=Colors.SURFACE,
            bgcolor=Colors.SURFACE_TINT,
            on_click=self.btn_disconnect_click,
            visible=False
        )

        self.btn_loop_send = ElevatedButton(
            text="Loop Send",
            color=Colors.SURFACE,
            bgcolor=Colors.SURFACE_TINT,
            on_click=self.btn_loop_send_click,
            visible=False
        )

        self.btn_loop_close = ElevatedButton(
            text="Stop Loop",
            color=Colors.SURFACE,
            bgcolor=Colors.SURFACE_TINT,
            on_click=self.btn_loop_close_click,
            visible=False
        )

        self.btn_clear = ElevatedButton(
            text="Clear",
            color=Colors.SURFACE,
            bgcolor=Colors.SURFACE_TINT,
            on_click=self.btn_clear_click
        )

        self.padding = 10

        self.update_list_records(is_update=False)

        self.content = Column(
            [
                Row(
                    spacing=5,
                    controls=[
                        self.select_records,
                        self.name_record,

                        self.btn_save_record,
                        self.btn_update_record
                    ],
                ),
                self.color_filed,
                self.conductivity_field,
                self.ph_field,
                self.temperature_field,
                self.tds_field,
                self.turbidity_field,
                Row(
                    [
                        self.btn_connect,
                        self.btn_disconnect,
                        self.btn_loop_send,
                        self.btn_loop_close,
                        self.btn_clear,
                    ],
                ),
            ]
        )

    def update_list_records(self, is_update: bool = True):
        self.list_records = DatabaseManager.get_all(RecordModel)
        list_options = [DropdownOption(text="New")]
        for record in self.list_records:
            list_options.append(DropdownOption(text=record["title"]))

        self.select_records.options = list_options
        if is_update:
            self.update()

    def select_records_change(self, e):
        print(e)
        if e.data == "New":
            self.btn_save_record.visible = True
            self.btn_update_record.visible = False
            self.name_record.label = "Name"
            self.name_record.value = "New"
        else:
            self.btn_save_record.visible = False
            self.btn_update_record.visible = True
            self.name_record.label = "Update"

            title = e.data
            """Busca o registro com o título de la lista de forma optima"""

            for record in self.list_records:
                if record["title"] == title:
                    print(record)
                    self.select_records.value = title
                    self.select_records.value = record["title"]
                    self.name_record.value = record["title"]
                    self.color_r_field.value = record["color_r"]
                    self.color_g_field.value = record["color_g"]
                    self.color_b_field.value = record["color_b"]
                    self.conductivity_field.value = record["conductivity"]
                    self.ph_field.value = record["ph"]
                    self.temperature_field.value = record["temperature"]
                    self.tds_field.value = record["tds"]
                    self.turbidity_field.value = record["turbidity"]
                    break

        self.update()

    def btn_save_record_click(self, e):
        record = RecordModel(
            title=self.name_record.value,
            color_r=int(self.color_r_field.value),
            color_g=int(self.color_g_field.value),
            color_b=int(self.color_b_field.value),
            conductivity=float(self.conductivity_field.value),
            ph=float(self.ph_field.value),
            temperature=float(self.temperature_field.value),
            tds=float(self.tds_field.value),
            turbidity=float(self.turbidity_field.value)
        )
        DatabaseManager.add(record)
        self.select_records.value = self.name_record.value
        self.update_list_records()

    def btn_update_record_click(self, e):
        print("Update")
        for record in self.list_records:
            if record["title"] == self.select_records.value:
                print(record)
                DatabaseManager.update(
                    RecordModel,
                    record["id"],
                    title=self.name_record.value,
                    color_r=int(self.color_r_field.value),
                    color_g=int(self.color_g_field.value),
                    color_b=int(self.color_b_field.value),
                    conductivity=float(self.conductivity_field.value),
                    ph=float(self.ph_field.value),
                    temperature=float(self.temperature_field.value),
                    tds=float(self.tds_field.value),
                    turbidity=float(self.turbidity_field.value)
                )
                self.select_records.value = self.name_record.value
                self.update_list_records()
                break

    def handler_con_success(self, message: str):
        print(message)
        self.btn_connect.visible = False
        self.btn_disconnect.visible = True
        self.btn_loop_send.visible = True
        self.btn_loop_close.visible = False

    def handler_con_error(self, message: str):
        print(message)
        self.btn_connect.visible = True
        self.btn_disconnect.visible = False
        self.btn_loop_send.visible = False
        self.btn_loop_close.visible = False

    def handler_con_closed(self, message: str):
        print(message)
        self.btn_connect.visible = True
        self.btn_disconnect.visible = False
        self.btn_loop_send.visible = False
        self.btn_loop_close.visible = False

    def handler_loop_started(self, is_started: bool):

        socket = AppContext.get_socket()

        if socket and is_started:
            self.btn_loop_send.visible = False
            self.btn_loop_close.visible = True
        elif socket:
            self.btn_loop_send.visible = True
            self.btn_loop_close.visible = False

    def btn_click(self, e):

        conn = DatabaseManager.get_first(ConnectionConfigModel)

        host = conn["host"] if conn else "http://127.0.0.1:8000/"
        token = conn["token"] if conn else ""

        AppContext.set_socket(host, token)

    def btn_disconnect_click(self, e):
        AppContext.close_socket()
        AppContext.set_loop_started(False)

    def btn_clear_click(self, e):
        AppContext.clear_list()

    def init_loop(self):
        while AppContext.get_loop_started():
            AppContext.send_data({
                "color": {
                    "r": int(self.color_r_field.value),
                    "g": int(self.color_g_field.value),
                    "b": int(self.color_b_field.value)
                },
                "conductivity": float(self.conductivity_field.value),
                "ph": float(self.ph_field.value),
                "temperature": float(self.temperature_field.value),
                "tds": float(self.tds_field.value),
                "turbidity": float(self.turbidity_field.value)
            })
            time.sleep(5)

    def btn_loop_send_click(self, e):
        AppContext.set_loop_started(True)
        self.init_loop()

    def btn_loop_close_click(self, e):
        AppContext.set_loop_started(False)
