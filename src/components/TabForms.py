from flet import Tabs, Tab, Container,  Text, Alignment
from components.Form import Form


class TabForms(Tabs):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected_index = 0
        self.animation_duration = 300

        self.tabs = [
            Tab(
                text="Formulario",
                content=Form()
            ),
            Tab(
                text="Aleatorio",
                content=Container(
                    content=Text("Datos aleatorio")
                )
            )

        ]
