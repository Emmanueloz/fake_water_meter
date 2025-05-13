from flet import Container, ListView, Text, Colors, border

from context.AppContext import AppContext
from enums.events import Events


class ListSends(Container):

    list_view = ListView(
        spacing=5,
        padding=5,
        height=300,
        auto_scroll=True,
        controls=[]
    )

    def __init__(self):
        super().__init__()
        self.border = border.all(width=1, color=Colors.SURFACE_TINT)
        self.border_radius = 10

        AppContext.add_listener(Events.SEND_SUCCESS, self.add)
        AppContext.add_listener(Events.CLEAR_LIST, self.clear)

        self.content = self.list_view

    def add(self, message: str):
        control = Text(message, color=Colors.SURFACE_TINT)
        self.list_view.controls.append(control)
        self.update()

    def clear(self, value):
        self.list_view.controls = []
        self.update()

    def add_error(self, message: str):
        control = Text(message, color=Colors.ERROR)
        self.list_view.controls.append(control)
        self.update()
