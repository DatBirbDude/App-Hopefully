import json
from calendar import Calendar
import calendar
import datetime

import jicson

from kivy.graphics import Color, RoundedRectangle
from kivy import Config
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.card import MDCard


class BaseScreen(Screen):
    def contact_button_press(self):
        self.manager.current = 'contact'

    def settings_button_press(self):
        self.manager.current = 'settings'


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


class MainScreen(BaseScreen):

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


class SettingsScreen(BaseScreen):
    pass


class CalendarInfo(BaseScreen):

    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
              7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    date = datetime.date.today()
    year = NumericProperty(date.year)
    month = NumericProperty(date.month)
    day = NumericProperty(date.day)
    month_range = calendar.monthrange(year, month)
    weekday_offset = NumericProperty((date.weekday() + 1) % 7)
    week_diff = 0

    def week_change(self, change):
        if int(self.day - self.weekday_offset) <= int(self.month_range[1]):
            self.day += change * 7

    def on_update(self):



class CalendarScreen(CalendarInfo):
    pass


class MonthLayout(CalendarInfo):
    pass


class ListLayout(CalendarInfo):
    pass


class PhotosScreen(BaseScreen):
    pass


class ClubsScreen(BaseScreen):
    pass


class ContactScreen(BaseScreen):
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
