import os
from pathlib import Path

from kivy.properties import StringProperty

from Controller import config
from kivy.config import Config
Config.set("graphics", "width", f"{config.WIDTH}")
Config.set("graphics", "height", f"{config.HEIGHT}")

from kivymd.app import MDApp

from View.Manager.manager_screen import ManagerScreen

os.environ['AirQuality'] = str(Path(__file__).parent)


class AirQualityApp(MDApp):
    """AirQualityApp application for air quality and weather information"""
    level = StringProperty('EASY')
    player = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'LightBlue'
        self.manager_screen = ManagerScreen()

    def build(self):
        self.manager_screen.add_widget(self.manager_screen.create_screen('login'))
        return self.manager_screen


AirQualityApp().run()
