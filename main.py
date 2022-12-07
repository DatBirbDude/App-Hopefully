import json
import jicson

from kivy.graphics import Color, RoundedRectangle
from kivy import Config
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.card import MDCard


class LogInScreen(Screen):
    screen_width = NumericProperty(100)
    screen_height = NumericProperty(100)

    def on_size(self, instance, value):
        self.screen_width = value[0]
        self.screen_height = value[1]
        print(value)

    def check_login(self):
        logins = json.load(open('Credentials.json'))

        if self.ids.UsernameInput.text in logins['admins']:
            if self.ids.PasswordInput.text == logins['admins'][self.ids.UsernameInput.text]:
                self.manager.current = 'main'


class MainScreen(Screen):
    screen_width = Window.width
    screen_height = Window.height

    buffer = (int(screen_width) + int(screen_height)) / 80

    contact_button_color = [239 / 255, 98 / 255, 108 / 255, 1]
    clubs_button_color = [34 / 255, 24 / 255, 28 / 255, 0.8]
    photos_button_color = [34 / 255, 24 / 255, 28 / 255, 0.8]
    calendar_button_color = [34 / 255, 24 / 255, 28 / 255, 0.8]

    def on_size(self, instance, value):
        self.screen_width = value[0]
        self.screen_height = value[1]
        self.buffer = int(self.screen_width) / 25
        print(value)

    def calendar_button_press(self):
        self.manager.current = 'calendar'

    def photos_button_press(self):
        self.manager.current = 'photos'

    def clubs_button_press(self):
        self.manager.current = 'clubs'

    def contact_button_press(self):
        self.manager.current = 'contact'

    def settings_button_press(self):
        self.manager.current = 'settings'


class SettingsScreen(Screen):
    pass


class CalendarScreen(Screen):
    pass


class MonthLayout(Screen):
    pass


class ListLayout(Screen):
    pass


class PhotosScreen(Screen):
    pass


class ClubsScreen(Screen):
    pass


class ContactScreen(Screen):
    pass


class AppMaybe(MDApp):

    def build(self):
        Window.size = (280, 650)

        sm = ScreenManager()

        sm.add_widget(LogInScreen(name='log_in'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(CalendarScreen(name='calendar'))
        sm.add_widget(PhotosScreen(name='photos'))
        sm.add_widget(ClubsScreen(name='clubs'))
        sm.add_widget(ContactScreen(name='contact'))
        sm.add_widget(SettingsScreen(name='settings'))

        return sm


if __name__ == '__main__':

    '''
    in_file = jicson.fromFile('Calendar.ics')
    with open('Calendar.json', "w") as result:
            json.dump(in_file, result)
    '''

    AppMaybe().run()
