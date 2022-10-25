from datetime import datetime

from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
from kivy.properties import ObjectProperty, ListProperty, DictProperty, StringProperty

from View.Manager.api_manager import APIManager
from View.Manager.notification_manager import notification_manager
from Controller.exceptions import APIException
from Controller.utils import APPLabel, get_aqi_category


class MainScreenView(MDScreen):
    """Main App Screen."""
    country_menu = ObjectProperty()
    states_menu = ObjectProperty()
    cities_menu = ObjectProperty()
    country_list = ListProperty()
    state_list = ListProperty()
    city_list = ListProperty()
    city_data = DictProperty()
    hometown = StringProperty()

    def __init__(self, **kwargs):
        super(MainScreenView, self).__init__(**kwargs)
        self.notifier = notification_manager
        try:
            self.api_manager = APIManager()
        except APIException as ex:
            self.notifier.notify(ex.user_error_message)
        Clock.schedule_once(self.get_clock)
        Clock.schedule_interval(self.get_clock, 60)

    @property
    def countries(self):
        try:
            return {country[:5].upper(): country for country in self.api_manager.get_countries()}
        except APIException as ex:
            self.notifier.notify(ex.user_error_message)
            return {}

    def switch_screen(self, navigation_rail, navigation_rail_item):
        name_screen = navigation_rail_item.icon.split("-")[0].lower()
        if name_screen in self.ids.screen_manager.screen_names:
            self.ids.screen_manager.current = name_screen

    def on_enter(self):
        navigation_rail_items = self.ids.navigation_rail.get_items()[:]
        navigation_rail_items.reverse()

        for widget in navigation_rail_items:
            name_screen = widget.icon.split("-")[0].lower()
            screen = MDScreen(name=name_screen, radius=[18, 0, 0, 0])
            self.ids.screen_manager.add_widget(screen)

    def get_clock(self, widget):
        current_time = datetime.now()
        self.ids.clock.text = current_time.strftime('%H:%M')

    def open_countries(self):
        if not self.country_list:
            items = self.countries.items()
            if not items:  # Exception is raised in property getter
                return

            for abbreviation, country in items:
                self.country_list.append(
                    {'viewclass': 'OneLineListItem',
                     'text': f'{country}',
                     'on_press': lambda x=country: self.country_callback(x)}
                )
        self.country_menu = MDDropdownMenu(width_mult=4)
        if self.ids.screen_manager.current == 'air':
            self.country_menu.caller = self.ids.air_country
        else:
            self.country_menu.caller = self.ids.weather_country
        self.country_menu.items = self.country_list
        self.country_menu.open()

    def country_callback(self, country):
        self.country_menu.caller.text = str(country)
        try:
            self.state_list = self.api_manager.get_states(country=country)
        except APIException as ex:
            self.notifier.notify(ex.user_error_message)
        self.country_menu.dismiss()
        if self.ids.screen_manager.current == 'air':
            self.ids.air_state.disabled = False
        else:
            self.ids.weather_state.disabled = False

    def open_states(self, country):
        items = [
            {'viewclass': 'OneLineListItem',
             'text': f'{state}',
             'on_press': lambda x=country, y=state: self.state_callback(x, y)}
            for state in self.state_list]

        self.states_menu = MDDropdownMenu(width_mult=4)
        if self.ids.screen_manager.current == 'air':
            self.states_menu.caller = self.ids.air_state
        else:
            self.states_menu.caller = self.ids.weather_state
        self.states_menu.items = items
        self.states_menu.open()

    def state_callback(self, country, state):
        self.states_menu.caller.text = str(state)
        try:
            self.city_list = self.api_manager.get_cities(country, state)
        except APIException as ex:
            self.notifier.notify(ex.user_error_message)

        if self.ids.screen_manager.current == 'air':
            self.ids.air_city.disabled = False
        else:
            self.ids.weather_city.disabled = False
        self.states_menu.dismiss()

    def open_cities(self):
        state = self.states_menu.caller.text
        country = self.country_menu.caller.text
        items = [
            {'viewclass': 'OneLineListItem',
             'text': f'{city}',
             'on_press': lambda x=city: self.city_callback(x, country, state)}
            for city in self.city_list]
        self.cities_menu = MDDropdownMenu(width_mult=4)
        if self.ids.screen_manager.current == 'air':
            self.cities_menu.caller = self.ids.air_city
        else:
            self.cities_menu.caller = self.ids.weather_city

        self.cities_menu.items = items
        self.cities_menu.open()

    def city_callback(self, city, country, state):
        self.cities_menu.caller.text = str(city)
        try:
            data = self.api_manager.get_city_data(city, state, country)
        except APIException as ex:
            self.notifier.notify(ex.user_error_message)
            return
        self.city_data = data
        self.cities_menu.dismiss()

        if self.ids.screen_manager.current == 'air':
            self.show_air_quality(data['pollution'])
        else:
            self.show_weather(data['weather'])

    def show_air_quality(self, data):
        self.ids.air_label.clear_widgets(self.ids.air_label.children)
        try:
            aqi = data['aqius']  # AQI value based on US EPA standard
            pollutant = data['mainus']  # main pollutant for US AQI
        except APIException as ex:
            self.notifier.notify(ex.user_error_message)
            return
        category = get_aqi_category(aqi)
        label = APPLabel(aqi=category)
        label.text = f'Air quality is {category}\nAQI level: {aqi} - Main pollutant: {pollutant}'
        self.ids.air_label.add_widget(label)

    def show_weather(self, data):
        self.ids.weather_label.clear_widgets(self.ids.weather_label.children)
        try:
            temperature = data['tp']  # temperature in Celsius
            pressure = data['pr']  # atmospheric pressure in hPa
            humidity = data['hu']  # humidity %
            wind_speed = data['ws']  # wind speed (m/s)
            wind_direction = data['wd']  # 360° (N=0, E=90, S=180, W=270)
        except APIException as ex:
            self.notifier.notify(ex.user_error_message)
            return

        text = f"""
        Current temperature: {temperature} \u00B0C \n
        Humidity {humidity}% | Pressure {pressure} hPa \n
        Wind speed {wind_speed} m/s | Wind direction {wind_direction} \n(N=0, E=90, S=180, W=270)"""
        label = APPLabel('moderate')
        label.text = text
        self.ids.weather_label.add_widget(label)

    def my_city_data(self):
        try:
            if not self.ids.my_city.children:
                data = self.api_manager.get_nearest_city()
                self.hometown = data['city']
                aqi_value = get_aqi_category(data['current']['pollution']['aqius'])
                label_text = f"Home city: {data['city']}\nCountry: {data['country']}, State: {data['state']}\n\n" \
                             f"Current Air Quality: \n    AQI - {data['current']['pollution']['aqius']}, " \
                             f"Pollutant: {data['current']['pollution']['mainus']}\n\nCurrent Weather Data: \n    " \
                             f"Temperature - {data['current']['weather']['tp']} \u00B0C \n    Atmospheric " \
                             f"Pressure: {data['current']['weather']['pr']} hPa\n    " \
                             f"Humidity: {data['current']['weather']['hu']}% \n    " \
                             f"Wind Speed: {data['current']['weather']['ws']} m/s"
                label = APPLabel(aqi=aqi_value, hometown=True)
                label.text = label_text
                self.ids.my_city.add_widget(label)
        except APIException as ex:
            self.notifier.notify(ex.user_error_message)
