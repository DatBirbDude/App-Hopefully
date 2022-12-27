import json
import math
from calendar import Calendar
import calendar
import datetime

import jicson
import numpy
from kivy.clock import Clock

from kivy.graphics import Color, Rectangle, RoundedRectangle, Canvas, Line, Callback
from kivy import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, ObjectProperty, ColorProperty, \
    ListProperty  # Sam added ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
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

    int_width = Window.width
    int_height = Window.height

    def contact_button_press(self):
        self.manager.current = 'contact'

    def settings_button_press(self):
        self.manager.current = 'settings'

    def on_size(self, instance, value):
        self.width = value[0]
        self.height = value[1]


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
    def month_change(self, change):  # Error: If you go back and forth between months, it won't go to the right day
        if (CalendarInfo.month == 12 and change > 0) or (CalendarInfo.month == 1 and change < 0):
            CalendarInfo.year += math.ceil(numpy.sign(change) * change / 12) * numpy.sign(change)
        CalendarInfo.month = (CalendarInfo.month + change - 1) % 12 + 1
        CalendarInfo.month_range = calendar.monthrange(CalendarInfo.year, CalendarInfo.month)
        CalendarInfo.weekday_offset = (calendar.weekday(CalendarInfo.year, CalendarInfo.month, CalendarInfo.day) + 1) % 7
        MonthAndYearLabel.label.text = str(CalendarInfo.months[CalendarInfo.month]) + ' ' + str(CalendarInfo.year)
        for i in range(0, 7):
            DayNumsLayout.day_of_weekdays[i] = str(CalendarInfo.day - CalendarInfo.weekday_offset + i)
            if CalendarInfo.month_range[1] >= int(DayNumsLayout.day_of_weekdays[i]) > 0:
                DayNumsLabels.day_labels[i].text = DayNumsLayout.day_of_weekdays[i]
            else:
                DayNumsLabels.day_labels[i].text = ''
            DayNumsLayout.is_selected[i] = False
        DayNumsLayout.is_selected[CalendarInfo.weekday_offset] = True
        ListLayout.day_nums_layout.update_canvas()
        ListLayout.event_widgets.set_events()
        print(CalendarInfo.day)
        print(CalendarInfo.month)
        print(CalendarInfo.year)


    def on_size(self, instance, value):
        # Updating DayNumsLabels in the .py file
        DayNumsLabels.size = Window.size
        DayNumsLabels.box_layout.pos = [DayNumsLabels.size[0] / 9, DayNumsLabels.size[1] * 7.42/10]
        DayNumsLabels.box_layout.size = [DayNumsLabels.size[0], DayNumsLabels.size[1] / 20]
        for label in DayNumsLabels.day_labels:
            label.width = DayNumsLabels.box_layout.width / 9

        # Updating MonthAndYearLabel in the .py file
        MonthAndYearLabel.size = Window.size
        MonthAndYearLabel.label.pos = [MonthAndYearLabel.size[0] / 2, MonthAndYearLabel.size[1] * 7/8]
        MonthAndYearLabel.label.size = [MonthAndYearLabel.size[0] / 100, MonthAndYearLabel.size[1] / 100]

        # Updating EventWidget in the .py file
        EventWidgets.size = Window.size


class MonthAndYearLabel(Widget):

    size = Window.size

    label = Label(text=str(CalendarInfo.months[CalendarInfo.month]) + ' ' + str(CalendarInfo.year),
                  font_name='Fonts/Vogue.ttf',
                  pos=[size[0] / 10, size[1] / 2],
                  # Any change to pos or size has to also be changed in on_size method
                  size=[size[0] / 2, size[1] * 7/8],
                  color=[246 / 255, 232 / 255, 234 / 255, 1])

    num_events = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(self.label)


class MonthLayout(CalendarInfo):
    pass


class EventWidgets(Widget):
    size = (280, 650)
    num_events = 0

    summaries = []
    descriptions = []

    event_cards = []
    text_buffer_x = size[0] / 40
    text_buffer_y = size[1] / 200

    # I'm low-key proud of this even though it's probably wildly inefficient
    def do_the_json(self):

        self.summaries = []
        self.descriptions = []
        self.num_events = 0

        temp = open('Calendar.json')
        cal = json.load(temp)
        for i in range(0, len(cal['VCALENDAR'][0]['VEVENT'])):
            event = cal['VCALENDAR'][0]['VEVENT'][i]
            year = int(event['DTSTART'][0:4])
            month = int(event['DTSTART'][4:6])
            day = int(event['DTSTART'][6:8])
            try:
                duration = int(event['DURATION'][1])
            except KeyError:
                duration = 1
            if year == CalendarInfo.year and month == CalendarInfo.month and day + duration > CalendarInfo.day >= day:
                self.num_events += 1
                try:
                    self.summaries.append(event['SUMMARY;ENCODING=QUOTED-PRINTABLE'])
                except KeyError:
                    self.summaries.append('')
                try:
                    self.descriptions.append(event['DESCRIPTION;ENCODING=QUOTED-PRINTABLE'])
                except KeyError:
                    self.descriptions.append('')

    def create_event_labels(self):
        self.event_cards = []
        print(len(self.event_cards))
        for i in range(0, self.num_events):
            event_card = [Label(text=self.summaries[i],
                                size=[self.size[0] * 9 / 10, self.size[1] / 20],
                                text_size=[self.size[0] * 9 / 10, self.size[1] / 20],
                                halign='left',
                                valign='top',
                                font_size=self.size[0] / 25,
                                color=(246 / 255, 232 / 255, 234 / 255, 1),
                                pos=[self.size[0] / 20 + self.text_buffer_x,
                                     self.size[1] * (6.7/10 - i/5) - self.text_buffer_y]),
                          Label(text=self.descriptions[i],
                                size=[self.size[0] * 9/10 , self.size[1] / 40],
                                text_size=[self.size[0] * 9 / 10 - 1.5 * self.text_buffer_x, self.size[1] / 20],
                                halign='left',
                                valign='top',
                                font_size=self.size[0] / 30,
                                color=(246 / 255, 232 / 255, 234 / 255, 1),
                                pos=[self.size[0] / 20,
                                     self.size[1] * (3/5 - i/5) - self.text_buffer_y])]
            self.event_cards.append(event_card)
        for i in range(0, self.num_events):
            for o in range(0, 2):
                self.add_widget(self.event_cards[i][o])

    def set_events(self):
        self.do_the_json()
        self.update_canvas()
        self.create_event_labels()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_the_json()
        self.update_canvas()
        self.create_event_labels()

    def update_canvas(self):

        self.canvas.clear()
        self.size = (280, 650)

        with self.canvas:

            for i in range(0, self.num_events):
                Color(34 / 255, 24 / 255, 28 / 255, 1)

                RoundedRectangle(size=[self.size[0] * 9/10, self.size[1] / 6],
                                 pos=[self.size[0] / 20, self.size[1] * (5/9 - i/5)],
                                 radius=(self.height / 20, self.height / 20))

                Color(0, 0, 0, 1)  # 132/255, 220/255, 207/255, 1

                Line(rounded_rectangle=[self.size[0] / 20, self.size[1] * (5/9 - i/5),
                                        self.size[0] * 9/10, self.size[1] / 6,
                                        self.height / 20],
                     width=1,
                     close=True)


class DayNumsLayout(Widget):
    size = (280, 650)

    day_of_weekdays = [str(CalendarInfo.day - CalendarInfo.weekday_offset + CalendarInfo.week_diff),
                       str(CalendarInfo.day - CalendarInfo.weekday_offset + CalendarInfo.week_diff + 1),
                       str(CalendarInfo.day - CalendarInfo.weekday_offset + CalendarInfo.week_diff + 2),
                       str(CalendarInfo.day - CalendarInfo.weekday_offset + CalendarInfo.week_diff + 3),
                       str(CalendarInfo.day - CalendarInfo.weekday_offset + CalendarInfo.week_diff + 4),
                       str(CalendarInfo.day - CalendarInfo.weekday_offset + CalendarInfo.week_diff + 5),
                       str(CalendarInfo.day - CalendarInfo.weekday_offset + CalendarInfo.week_diff + 6)]

    is_selected = [False, False, False, False, False, False, False]
    is_selected[CalendarInfo.weekday_offset] = True

    select_color = [Color(0, 0, 0, 0), Color(0, 0, 0, 0), Color(0, 0, 0, 0),
                    Color(0, 0, 0, 0), Color(0, 0, 0, 0), Color(0, 0, 0, 0),
                    Color(0, 0, 0, 0)]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas:

            for i in range(0, 7):
                if self.is_selected[i]:
                    Color(239/255, 98/255, 108/255, 1)
                else:
                    Color(0, 0, 0, 0)

                Line(circle=[self.size[0] * (3/18 + i/9), self.size[1] * 76.8/100, self.size[0] / 20], width=1)

    def update_canvas(self):

        with self.canvas:

            for i in range(0, 7):
                if self.is_selected[i]:
                    Color(239/255, 98/255, 108/255, 1)
                else:
                    Color(49/255, 47/255, 47/255, 1)

                Line(circle=[Window.width * (3/18 + i/9), Window.height * 76.8/100, Window.width / 20], width=1)

    def my_callback(self, instr):
        pass

    def week_change(self, change):
        if 0 < (CalendarInfo.day - CalendarInfo.weekday_offset + 6 + 7 * change) or change > 0:
            if (CalendarInfo.day - CalendarInfo.weekday_offset + 7 * change) < CalendarInfo.month_range[1] or change < 0:
                CalendarInfo.day += 7 * change
                for i in range(0, 7):
                    self.is_selected[i] = False
                if CalendarInfo.month_range[0] <= CalendarInfo.day <= CalendarInfo.month_range[1]:
                    self.is_selected[CalendarInfo.weekday_offset] = True
                self.update_canvas()
        for i in range(0, len(self.day_of_weekdays)):
            self.day_of_weekdays[i] = str(CalendarInfo.day - CalendarInfo.weekday_offset + i)
            if CalendarInfo.month_range[1] >= int(self.day_of_weekdays[i]) > 0:
                DayNumsLabels.day_labels[i].text = self.day_of_weekdays[i]
            else:
                DayNumsLabels.day_labels[i].text = ''
        print(CalendarInfo.day)

        ListLayout.event_widgets.do_the_json()
        ListLayout.event_widgets.update_canvas()
        ListLayout.event_widgets.create_event_labels()

    def on_being_clicked(self, button):
        for i in range(0, 7):
            self.is_selected[i] = False
        if CalendarInfo.month_range[1] >= int(self.day_of_weekdays[button]) > 0:
            self.is_selected[button] = True
            CalendarInfo.day += button - CalendarInfo.weekday_offset
            CalendarInfo.weekday_offset = (calendar.weekday(CalendarInfo.year, CalendarInfo.month,
                                                            CalendarInfo.day) + 1) % 7
            print(CalendarInfo.day)
            ListLayout.event_widgets.do_the_json()
            ListLayout.event_widgets.update_canvas()
            ListLayout.event_widgets.create_event_labels()
            self.update_canvas()


class ListLayout(CalendarInfo):

    event_widgets = EventWidgets()
    day_nums_layout = DayNumsLayout()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(self.event_widgets)
        self.add_widget(self.day_nums_layout)


class DayNumsLabels(Widget):
    size = (Window.width, Window.height)  # This is a temporary fix that doesn't shift with size

    day_labels = []

    box_layout = BoxLayout(pos=[size[0] / 9, size[1] * 7.42/10],
                           size=[size[0], size[1] / 20])
    for i in range(0, 7):
        day_label = Label(text=DayNumsLayout.day_of_weekdays[i], size_hint=[None, 1], width=box_layout.width / 9,
                          color=[246/255, 232/255, 234/255, 1], font_name='Fonts/Vogue.ttf')
        day_labels.append(day_label)
        box_layout.add_widget(day_label)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (Window.width, Window.height)
        self.add_widget(self.box_layout)




# The next class is a sample from official kivy documentation, don't touch it or it will break everything
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

        log_in_screen = LogInScreen(name='log_in')
        main_screen = MainScreen(name='main')
        calendar_screen = CalendarScreen(name='calendar')
        photos_screen = PhotosScreen(name='photos')
        clubs_screen = ClubsScreen(name='clubs')
        contact_screen = ContactScreen(name='contact')
        settings_screen = SettingsScreen(name='settings')

        sm.add_widget(log_in_screen)
        sm.add_widget(main_screen)
        sm.add_widget(calendar_screen)
        sm.add_widget(photos_screen)
        sm.add_widget(clubs_screen)
        sm.add_widget(contact_screen)
        sm.add_widget(settings_screen)
        return sm


if __name__ == '__main__':
    '''
    in_file = jicson.fromFile('Calendar.ics')
    with open('Calendar.json', "w") as result:
            json.dump(in_file, result, indent=4)
    '''
#Vincent if you want to comment control code, at least explain why
    #L nah

    AppMaybe().run()
