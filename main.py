import json

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

    def checkLogin(self):
        logins = json.load(open('Credentials.json'))

        if self.ids.UsernameInput.text in logins['admins']:
            if self.ids.PasswordInput.text == logins['admins'][self.ids.UsernameInput.text]:
                self.manager.current = '2'


class MainScreen(Screen):
    pass


class AppMaybe(MDApp):

    def build(self):

        Window.size = (280, 650)

        sm = ScreenManager()

        sm.add_widget(LogInScreen(name = '1'))
        sm.add_widget(MainScreen(name = '2'))

        return sm

if __name__ == '__main__':
    AppMaybe().run()
