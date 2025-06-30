from flet import Column, Container, Row, Text,ElevatedButton
import time
from random import randint,uniform

from context.AppContext import AppContext

class RandomRecords(Container):
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.color_r = Text("0")
        self.color_g = Text("0")
        self.color_b = Text("0")
        self.conductivity = Text("0")
        self.ph = Text("0")
        self.temperature = Text("0")
        self.tds = Text("0")
        self.turbidity = Text("0")

        self.btn_init_random = ElevatedButton(
            text="Start",
            on_click=self.start_random
        )

        self.btn_stop_random = ElevatedButton(
            text="stop",
            on_click=self.stop_random
        )

        self.content = Column(
            controls=[
                Text("Color: "),
                Row(
                    controls=[
                        self.color_r,
                        self.color_g,
                        self.color_b
                    ]
                ),
                Text("Conductividad: "),
                self.conductivity,
                self.ph,
                self.temperature,
                self.tds,
                self.turbidity,

                Row(
                    controls=[
                        self.btn_init_random,
                        self.btn_stop_random
                    ]
                )

            ]
        )

    def _random_color(self)->int:
        return randint(0,255)

    def _random_value(self,start:int,stop:int)->float:
        return uniform(start,stop)

    def _init_random(self) -> None:
        self.color_r.value = str(self._random_color())
        self.color_g.value = str(self._random_color())
        self.color_b.value = str(self._random_color())

        self.conductivity.value = str(self._random_value(0,3000))
        self.ph.value = str(self._random_value(0,10))
        self.temperature.value = str(self._random_value(0,35))
        self.tds.value = str(self._random_value(0,500))
        self.turbidity.value = str(self._random_value(0,50))
        
        self.update()

    def start_random(self,e):
        self._init_random()
        AppContext.set_loop_started(True)

        while AppContext.get_loop_started():
            AppContext.send_data({
                "color": {
                    "r": int(str(self.color_r.value)),
                    "g": int(str(self.color_g.value)),
                    "b": int(str(self.color_b.value))
                },
                "conductivity": float(str(self.conductivity.value)),
                "ph": float(str(self.ph.value)),
                "temperature": float(str(self.temperature.value)),
                "tds": float(str(self.tds.value)),
                "turbidity": float(str(self.turbidity.value))
            })
            time.sleep(5)
            self._init_random()


    def stop_random(self,e):
        AppContext.set_loop_started(False)
