import json
from calendar import Calendar
import calendar
import datetime

import jicson

from kivy.graphics import Color, RoundedRectangle, Canvas, Line, Callback
from kivy import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, ObjectProperty #Sam added ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDRoundFlatButton, MDIconButton
from kivymd.uix.card import MDCard

#Sam's import lines below
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.logger import Logger
from kivy.uix.scrollview import ScrollView
import os
import shutil
from kivy.config import Config
Config.set('graphics','resizable',0)
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
    year = date.year
    month = date.month
    day = date.day
    month_range = calendar.monthrange(year, month)
    weekday_offset = (date.weekday() + 1) % 7
    week_diff = 0


class CalendarScreen(CalendarInfo):
    pass


class MonthLayout(CalendarInfo):
    pass


class ListLayout(CalendarInfo):
    pass


class DayNumsLayout(BoxLayout):

    day_of_weekdays = [str(CalendarInfo.day - CalendarInfo.weekday_offset + CalendarInfo.week_diff),
                       str(CalendarInfo.day - CalendarInfo.weekday_offset + CalendarInfo.week_diff + 1),
                       str(CalendarInfo.day - CalendarInfo.weekday_offset + CalendarInfo.week_diff + 2),
                       str(CalendarInfo.day - CalendarInfo.weekday_offset + CalendarInfo.week_diff + 3),
                       str(CalendarInfo.day - CalendarInfo.weekday_offset + CalendarInfo.week_diff + 4),
                       str(CalendarInfo.day - CalendarInfo.weekday_offset + CalendarInfo.week_diff + 5),
                       str(CalendarInfo.day - CalendarInfo.weekday_offset + CalendarInfo.week_diff + 6)]

    is_selected = [False, False, False, False, False, False, False]
    is_being_clicked = [False, False, False, False, False, False, False]

    def __init__(self, **kwargs):
        self.size_hint = [1, None]
        self.height = Window.height / 20
        self.pos_hint = {'center_x' : 0.5, 'center_y' : 0.5}
        super().__init__(**kwargs)
        back_arrow = MDIconButton(size_hint=[1/9, 1], icon='ArrowBackIcon.png', )
        self.add_widget(back_arrow)
        for i in range(0, 7):
            day_num = Button(size_hint=[None, 1], width=Window.width / 9, font_name='Fonts/Vogue.ttf',
                             color=[246/255, 232/255, 234/255, 1], on_press=lambda x: self.on_being_clicked(i),
                             on_release=lambda x: self.on_select(i), text='O', background_color=[0, 0, 0, 0.5])
            self.add_widget(day_num)
        forward_arrow = MDIconButton(size_hint=[1/9, 1], width=Window.width / 18, icon='ArrowForwardIcon.png')
        self.add_widget(forward_arrow)

        with self.canvas:

            self.cb = Callback(self.my_callback)

            for i in range(0, 7):
                if self.is_selected[i]:
                    Color(239/255, 98/255, 108/255, 1)
                else:
                    Color(0, 0, 0, 0)

                Line(circle=[Window.width * (3/18 + i/9), Window.height * 76.8/100, Window.width / 20], width=1)

    def my_callback(self, instr):
        print('no plz')

    def week_change(self, change):
        for i in range(0, len(self.day_of_weekdays)):
            self.day_of_weekdays[i] = str(
                CalendarInfo.day - CalendarInfo.weekday_offset + CalendarInfo.week_diff + i + change)

    def on_being_clicked(self, button):
        self.is_being_clicked[button] = True
        self.canvas.ask_update()

    def on_select(self, button):
        self.is_being_clicked[button] = False
        self.is_selected[button] = True
        self.cb.ask_update()

#The next class is a sample from official kivy documentation, don't touch it or it will break everything
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
class PhotosScreen(Screen):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    img_input = ObjectProperty(None)
    def on_enter(self):
        print("debug")
        self.layout = PhotoList(cols=1)
        ib = Photo(
            wid="2",
            image="ico/strawberry.png",
            title="strawberry",
            label="Strawberry: Yummy Yummy\nPicked On: 5/6/2014, 2:01 PM"
        )
        self.layout.add_widget(ib)
        #Doesn't recognize new widget?
    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
    def load(self, path, filename):
        shutil.copy(os.path.join(path, filename[0]), os.path.join(os.getcwd(),"temp.png"))
        self.dismiss_popup()

                #This is the starter logic to image sharing, we just need to update the copy indexes and come up with a dynamic loader to make these things appear
class Post():
    def make(self, filepath, author, timestamp):
        f = open("Photos/index.json")
        d = json.load(f)
        for i in d["posts"]:
            return
class Photo(Button):
    wid = StringProperty('')
    image = StringProperty('')
    title = StringProperty('')
    label = StringProperty('')
    pass

class PhotoList(GridLayout):
    pass

#End Sam breaking things
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
#Vincent if you want to comment control code, at least explain why

    AppMaybe().run()
