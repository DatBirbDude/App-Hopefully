''' Sam's To do:
- Add instagram ~ 50%
- Add new posts
'''

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
    ListProperty, BooleanProperty  # Sam added ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDRoundFlatButton, MDIconButton
from kivymd.uix.card import MDCard

# Sam's import lines below
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
import os
from kivy.uix.image import Image, AsyncImage
import base62
from threading import Thread
from kivy.clock import Clock
from kivy.config import Config
from kivymd.uix.scrollview import MDScrollView

# Our own files below
import client

# Global variables that we use
Config.set('graphics', 'resizable', 0)
user_name = ''
admin = False

# Everything that runs on the server is toggleable with this yay
LOCAL=False

# Thread decorator to be used to live update the app
def mainthread(func):
    def delayed_func(*args):
        def callback_func(dt):
            func(*args)

        Clock.schedule_once(callback_func, 0)

    return delayed_func


# Parent screen - Allows settings, contact, and back buttons to work
class BaseScreen(Screen):
    int_width = Window.width
    int_height = Window.height

    # Changes to the "contact administration" screen
    def contact_button_press(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'contact'

    # Changes to the "settings" screen
    def settings_button_press(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'settings'

    # Changes to the "main" screen
    def back_button_press(self):
        self.manager.current = 'main'

    # Changes to "calendar" screen
    def calendar_button_press(self):
        self.manager.current = 'calendar'

    # Changes to "posts" screen
    def posts_button_press(self):
        self.manager.current = 'posts'

    # Changes to "clubs" screen
    def clubs_button_press(self):
        self.manager.current = 'clubs'

    # Function to change properties when size is changed <-- when on earth would a phone change size?
    @staticmethod
    def on_size(instance, value):
        # Updating DayNumsLabels in the .py file
        DayNumsLabels.size = Window.size
        DayNumsLabels.box_layout.pos = [DayNumsLabels.size[0] / 9, DayNumsLabels.size[1] * 6.9 / 10]
        DayNumsLabels.box_layout.size = [DayNumsLabels.size[0], DayNumsLabels.size[1] / 20]
        for label in DayNumsLabels.day_labels:
            label.width = DayNumsLabels.box_layout.width / 9

        # Updating MonthAndYearLabel in the .py file
        MonthAndYearLabel.size = Window.size
        MonthAndYearLabel.label.pos = [MonthAndYearLabel.size[0] / 2, MonthAndYearLabel.size[1] * 8.1 / 10]
        MonthAndYearLabel.label.size = [MonthAndYearLabel.size[0] / 100, MonthAndYearLabel.size[1] / 100]

        # Updating EventWidget in the .py file
        EventWidgets.size = Window.size
        ListLayout.event_widgets.update_canvas()
        ListLayout.event_widgets.create_event_labels()

        ListLayout.day_nums_layout.update_canvas()

        BugWidgets.size = Window.size
        AdminSettings.bug_widgets.text_buffer_x = Window.size[0] / 40
        AdminSettings.bug_widgets.text_buffer_y = Window.size[1] / 200
        AdminSettings.bug_widgets.generate_reports()

        AttendanceWidgets.size = Window.size
        AdminContactScreen.attendance_widgets.text_buffer_x = Window.size[0] / 40
        AdminContactScreen.attendance_widgets.text_buffer_y = Window.size[1] / 200
        AdminContactScreen.attendance_widgets.generate_reports()


# Log In Screen (Screen appears directly after opening app
class LogInScreen(Screen):
    # allows "log in" screen to edit the user's username
    global user_name
    global admin

    # Changes to "main" screen if the user logs in with valid credentials (in Credentials.json)
    def check_login(self):
        global user_name
        global admin
        logins = json.load(open('Credentials.json'))
        if LOCAL:
            if self.ids.UsernameInput.text in logins['admins']:
                if self.ids.PasswordInput.text == logins['admins'][self.ids.UsernameInput.text]['Password']:
                    user_name = logins['admins'][self.ids.UsernameInput.text]['Name']
                    self.manager.current = 'calendar'
            self.ids.UsernameInput.text = ''
            self.ids.PasswordInput.text = ''
        else:
            result = client.login(self.ids.UsernameInput.text, self.ids.PasswordInput.text)
            privilege = result["res"]
            user_name = result["name"]
            print("Welcome " + user_name)
            if privilege == 2:
                admin = True
                self.manager.current = 'calendar'
            elif privilege == 1:
                self.manager.current = 'calendar'
            else:
                # Vincent I need you to implement an in-app notif for this message
                print("Login not found")


# Screen with buttons to guide to every other screen
class MainScreen(BaseScreen):
    # Creates buffer variable, which is changed based on the size of the screen
    buffer = (Window.height + Window.width) / 80

    def on_size(self, instance, value):
        self.buffer = int(value[0] + value[1]) / 80


# Screen that allows for bug reports and logging out
class SettingsScreen(BaseScreen):

    # Takes user input from bug report and appends to Bugs.json
    def report_bug(self):
        global user_name
        new_bug_report = {
            'Name': user_name,
            'Bug': self.ids.BugInput.text
        }

        if LOCAL:
            temp = open('Bugs.json')
            bugs_file = json.load(temp)
            bugs_file.append(new_bug_report)
            with open('Bugs.json', "w") as result:
                json.dump(bugs_file, result, indent=4)
        else:
            client.addBug(new_bug_report["Name"], new_bug_report["Bug"])

        self.ids.BugInput.text = ''


# Parent class with all necessary date information
class CalendarInfo(Screen):
    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
              7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    date = datetime.date.today()  # Gets today's date
    year = date.year
    month = date.month
    day = date.day
    month_range = calendar.monthrange(year, month)
    weekday_offset = (date.weekday() + 1) % 7  # Formats days to always go from sunday to saturday


# Screen that shows the events on a given day
class CalendarScreen(CalendarInfo, BaseScreen):

    # Increments or decrements the month
    def month_change(self, change):
        if (CalendarInfo.month == 12 and change > 0) or (CalendarInfo.month == 1 and change < 0):
            CalendarInfo.year += math.ceil(numpy.sign(change) * change / 12) * numpy.sign(change)
        # ^ changes year when necessary ^

        CalendarInfo.month = (CalendarInfo.month + change - 1) % 12 + 1
        CalendarInfo.month_range = calendar.monthrange(CalendarInfo.year, CalendarInfo.month)
        # ^ Updates CalendarInfo.month and CalendarInfo.month_range ^

        if CalendarInfo.day <= CalendarInfo.month_range[1]:
            CalendarInfo.weekday_offset = (calendar.weekday(CalendarInfo.year, CalendarInfo.month,
                                                            CalendarInfo.day) + 1) % 7
        else:
            CalendarInfo.day = CalendarInfo.month_range[1]
            CalendarInfo.weekday_offset = (calendar.weekday(CalendarInfo.year, CalendarInfo.month,
                                                            CalendarInfo.day) + 1) % 7
        # ^ Deals with edge case of going from the end of a month with fewer days than the previous ^
        # i.e. March 30 --> Feb 30 (Doesn't exist)

        MonthAndYearLabel.label.text = str(CalendarInfo.months[CalendarInfo.month]) + ' ' + str(CalendarInfo.year)
        # ^ Updates the Month/Year label ^

        for i in range(0, 7):
            DayNumsLayout.day_of_weekdays[i] = str(CalendarInfo.day - CalendarInfo.weekday_offset + i)
            if CalendarInfo.month_range[1] >= int(DayNumsLayout.day_of_weekdays[i]) > 0:
                DayNumsLabels.day_labels[i].text = DayNumsLayout.day_of_weekdays[i]
            else:
                DayNumsLabels.day_labels[i].text = ''
            DayNumsLayout.is_selected[i] = False
        DayNumsLayout.is_selected[CalendarInfo.weekday_offset] = True
        # ^ Updates the labels that show the selected day and surrounding days ^

        ListLayout.day_nums_layout.update_canvas()
        ListLayout.event_widgets.set_events()
        # ^ Updates other Calendar properties ^


# Self Explanatory
class MonthAndYearLabel(Widget):
    size = (1, 1)

    # Label that displays month and year
    label = Label(text=str(CalendarInfo.months[CalendarInfo.month]) + ' ' + str(CalendarInfo.year),
                  font_name='Fonts/Vogue.ttf',
                  pos=[1, 1],
                  # Any change to pos or size has to also be changed in on_size method
                  size=[1, 1],
                  color=[0.1, 0.1, 0.1, 1])

    num_events = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(self.label)  # adds month/year label


# Unused possible calendar layout
class MonthLayout(CalendarInfo):
    pass


# Creates widgets that display the events on the "calendar" screen
class EventWidgets(Widget):
    size = (1, 1)
    num_events = 0

    summaries = []
    descriptions = []

    event_cards = []
    text_buffer_x = size[0] / 60
    text_buffer_y = size[1] / 200

    # Goes through Calendar.json and finds the events on a given day
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
                duration = int(event['DURATION'][1])  # Duration of the event in days
            except KeyError:
                duration = 1
            if year == CalendarInfo.year and month == CalendarInfo.month and day + duration > CalendarInfo.day >= day:
                self.num_events += 1
                try:
                    self.summaries.append(event['SUMMARY;ENCODING=QUOTED-PRINTABLE'])
                except KeyError:
                    self.summaries.append('')  # Edge case
                try:
                    self.descriptions.append(event['DESCRIPTION;ENCODING=QUOTED-PRINTABLE'])
                except KeyError:
                    self.descriptions.append('')  # Edge case
            # ^ Appends the event's summary and description (if they exist) ^

    def create_event_labels(self):
        self.text_buffer_x = Window.size[0] / 60
        self.text_buffer_y = Window.size[1] / 200
        self.event_cards = []
        for i in range(0, self.num_events):
            event_card = [Label(text=self.summaries[i],
                                size=[Window.size[0] * 9 / 10, Window.size[1] / 20],
                                text_size=[Window.size[0] * 9 / 10, Window.size[1] / 20],
                                halign='left',
                                valign='top',
                                font_size=Window.size[0] / 25,
                                color=(0.1, 0.1, 0.1, 1),
                                pos=[Window.size[0] / 20 + self.text_buffer_x,
                                     Window.size[1] * (6.2 / 10 - i / 5) - self.text_buffer_y]),
                          Label(text=self.descriptions[i],
                                size=[Window.size[0] * 9 / 10, Window.size[1] / 40],
                                text_size=[Window.size[0] * 9 / 10 - 1.5 * self.text_buffer_x, Window.size[1] / 20],
                                halign='left',
                                valign='top',
                                font_size=Window.size[0] / 30,
                                color=(0.1, 0.1, 0.1, 1),
                                pos=[Window.size[0] / 20,
                                     Window.size[1] * (5.5 / 10 - i / 5) - self.text_buffer_y])]
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
        self.size = Window.size
        self.do_the_json()
        self.update_canvas()
        self.create_event_labels()

    def update_canvas(self):

        self.canvas.clear()

        with self.canvas:
            for i in range(0, self.num_events):
                Color(255 / 255, 185 / 255, 245 / 255, 0.7)

                RoundedRectangle(size=[Window.size[0] * 9 / 10, Window.size[1] / 6],
                                 pos=[Window.size[0] / 20, Window.size[1] * (5.06 / 10 - i / 5)],
                                 radius=(Window.height / 60, Window.height / 60))

                Color(0.1, 0.1, 0.1, 1)

                Line(rounded_rectangle=[Window.size[0] / 20, Window.size[1] * (5.06 / 10 - i / 5),
                                        Window.size[0] * 9 / 10, Window.size[1] / 6,
                                        Window.height / 60],
                     width=1,
                     close=True)


# Not proud of this, but I'm too tired to refactor old code rather than just copy it and change a bit
class MiniEventWidgets(Widget):
    size = (1, 1)
    num_events = 0

    summaries = []
    descriptions = []

    event_cards = []
    text_buffer_x = size[0] / 180
    text_buffer_y = size[1] / 300

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
                                size=[self.size[0] * 8 / 10, self.size[1] / 20],
                                text_size=[self.size[0] * 8 / 10 - 2 * self.text_buffer_x, self.size[1] / 20],
                                halign='left',
                                valign='top',
                                font_size=self.size[0] / 30,
                                color=(246 / 255, 232 / 255, 234 / 255, 1),
                                pos=[self.size[0] / 10 + self.text_buffer_x,
                                     self.size[1] * (6.3 / 10 - i / 7) - self.text_buffer_y]),
                          Label(text=self.descriptions[i],
                                size=[self.size[0] * 8 / 10, self.size[1] / 40],
                                text_size=[self.size[0] * 8 / 10 - 1.5 * self.text_buffer_x, self.size[1] / 20],
                                halign='left',
                                valign='top',
                                font_size=self.size[0] / 35,
                                color=(246 / 255, 232 / 255, 234 / 255, 1),
                                pos=[self.size[0] / 20,
                                     self.size[1] * (3 / 5 - i / 5) - self.text_buffer_y])]
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

        with self.canvas:
            for i in range(0, self.num_events):
                Color(34 / 255, 24 / 255, 28 / 255, 1)

                RoundedRectangle(size=[self.size[0] * 8 / 10, self.size[1] / 8],
                                 pos=[self.size[0] / 10, self.size[1] * (5 / 9 - i / 7)],
                                 radius=(self.height / 20, self.height / 20))

                Color(0, 0, 0, 1)

                Line(rounded_rectangle=[self.size[0] / 10, self.size[1] * (5 / 9 - i / 7),
                                        self.size[0] * 8 / 10, self.size[1] / 8,
                                        self.height / 20],
                     width=1,
                     close=True)


class DayNumsLayout(Widget):
    day_of_weekdays = [str(CalendarInfo.day - CalendarInfo.weekday_offset),
                       str(CalendarInfo.day - CalendarInfo.weekday_offset + 1),
                       str(CalendarInfo.day - CalendarInfo.weekday_offset + 2),
                       str(CalendarInfo.day - CalendarInfo.weekday_offset + 3),
                       str(CalendarInfo.day - CalendarInfo.weekday_offset + 4),
                       str(CalendarInfo.day - CalendarInfo.weekday_offset + 5),
                       str(CalendarInfo.day - CalendarInfo.weekday_offset + 6)]

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
                    Color(239 / 255, 98 / 255, 108 / 255, 1)
                else:
                    Color(0, 0, 0, 0)

                Line(circle=[Window.size[0] * (3 / 18 + i / 9), Window.size[1] * 76.8 / 100, Window.size[0] / 20],
                     width=1)

    def update_canvas(self):

        self.canvas.clear()

        with self.canvas:

            for i in range(0, 7):
                if self.is_selected[i]:
                    Color(255 / 255, 185 / 255, 245 / 255, 1)
                else:
                    Color(0, 0, 0, 0)

                Line(circle=[Window.size[0] * (3 / 18 + i / 9), Window.size[1] * 7.15 / 10, Window.size[0] / 20],
                     width=1)

    def week_change(self, change):
        if 0 < (CalendarInfo.day - CalendarInfo.weekday_offset + 6 + 7 * change) or change > 0:
            if (CalendarInfo.day - CalendarInfo.weekday_offset + 7 * change) < CalendarInfo.month_range[
                1] or change < 0:
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


class DayNumsLabels(Widget):
    size = (1, 1)

    day_labels = []

    box_layout = BoxLayout(pos=[size[0] / 9, size[1] * 8 / 10],
                           size=[size[0], size[1] / 20])
    for i in range(0, 7):
        day_label = Label(text=DayNumsLayout.day_of_weekdays[i], size_hint=[None, 1], width=box_layout.width / 9,
                          color=[0.1, 0.1, 0.1, 1], font_name='Fonts/Vogue.ttf')
        day_labels.append(day_label)
        box_layout.add_widget(day_label)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(self.box_layout)


class ListLayout(CalendarInfo):
    event_widgets = EventWidgets()
    day_nums_layout = DayNumsLayout()
    day_nums_labels = DayNumsLabels()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(self.event_widgets)
        self.add_widget(self.day_nums_layout)
        self.add_widget(self.day_nums_labels)


# The next class is a sample from official kivy documentation, don't touch it or it will break everything
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class PostsScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height = Window.height * 74 / 12

class Filechooser(BoxLayout):
    def select(self, *args):
        try: self.label.text = args[1][0]
        except: pass

class Posts(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 50
        self.ButtonCheckConnection = Button(text="Get Posts")
        self.ButtonCheckConnection.bind(on_press=self.start_load_thread)
        self.add_widget(self.ButtonCheckConnection)
        self.ButtonCheckConnection = Button(text="Add Post")
        self.ButtonCheckConnection.bind(on_press=self.addPost)
        self.add_widget(self.ButtonCheckConnection)
    def addPost(self, *args):
        def post(instance):
            path = instance.content.label.text
            if path != "":
                client.addPost("Welcome", "S", "Hi hello", path)
            return False



        content = Filechooser()
        popup = Popup(content=content, size_hint=(0.9, 0.9))
        popup.bind(on_dismiss=post)
        popup.open()


        return

    def start_load_thread(self, *args):
        Thread(target=self.loadPosts, daemon=True).start()

    @mainthread
    def loadPosts(self, *_):
        # Attempt to fetch latest posts from server if allowed
        if not LOCAL:
            p = open("posts.json", "w")
            json.dump(client.getPosts(), p, indent=2)
            p.close()
        p = open("posts.json")
        posts = json.load(p)
        # Async draw in all posts
        for item in posts["posts"]:
            print(item["url"])
            self.add_widget(AsyncImage(source=item["url"]))


# End Sam breaking things


class ClubsList(BoxLayout):

    clubs_list = [
        "Adventure Club",
        "ASPCA",
        "Athletic Leadership Club",
        "AVID Club",
        "Backpacks for Baltimore Club",
        "Baseball Club",
        "Bee Club",
        "Best Buddies",
        "Black Lives Matter Club",
        "Book Club",
        "Chemathon - Level 1",
        "Chemathon - Level 2",
        "Chess Club",
        "Chick-fil-A Leadership Academy",
        "Chinese Club",
        "Color Guard – Marching Band",
        "Comic Book Club",
        "Cranes for Cancer",
        "CRASC",
        "Dance Company",
        "Dungeons & Dragons Club",
        "Environmental Club",
        "Envirothon Team",
        "Exploring All 22 / Football Game Tape",
        "Fellowship of Christian Athletes",
        "Femgineers Club",
        "Fostering Hope",
        "French Club",
        "Future Business Leaders of America",
        "Future Physicians Club",
        "Girls Empowerment League",
        "Graphic Design Club",
        "Harvest for the Hungry",
        "Hip Hop Collaboration",
        "Hispanic Student Voice",
        "Interact Club",
        "It's Academic",
        "Key Club",
        "Kids Fighting Cancer",
        "Latino Leaders Group",
        "Literary Magazine – Etchings",
        "Math Team",
        "Math, Engineering & Science Achievement (MESA)",
        "Mock Trial Club",
        "Model United Nations",
        "National Honor Society",
        "National Honor Society – Art",
        "National Honor Society – Chinese",
        "National Honor Society – English",
        "National Honor Society – Math (Mu Alpha Theta)",
        "National Honor Society – Science",
        "National Honor Society – Social Studies (Rho Kappa)",
        "National Honor Society – Spanish",
        "No Judgment Club",
        "Our Minds Matter",
        "Ping Pong Club",
        "Power Hawks FIRST Robotics Team",
        "Red Cross",
        "Remote Control Club",
        "Rocket Club",
        "SADD – Students Against Destructive Decisions",
        "Seahawk Scholars",
        "Seahawks Saving Shoreline Club",
        "Seeking Smiles",
        "STEM Family Committee",
        "STEM Senior Advisory Board",
        "Student Government Association",
        "Student Voice Committee",
        "Technology Student Association",
        "Theatre Company",
        "Unified Sports",
        "Walking Club",
        "Wii Club",
        "Wordsmithing Club",
        "Wounded Warrior Club",
        "Wreath Hawks",
        "Yearbook",
        "Your Choice: Student Reproductive Justice Coalition"
    ]
    size = (Window.width, Window.height * len(clubs_list) / 12)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.minimum_height = self.size[1]
        self.add_widget(Label(text='Clubs:',
                              font_size=Window.size[1] / 35,
                              size_hint=(1, None),
                              height=Window.size[1] / 6,
                              font_name='Fonts/Vogue.ttf',
                              color=(0.1, 0.1, 0.1, 1)
                              ))
        for i in range(0, len(self.clubs_list)):
            self.add_widget(Label(text=self.clubs_list[i],
                                  font_size=Window.size[1] / 50,
                                  size_hint=(1, None),
                                  height=Window.size[1] / 12,
                                  text_size=[Window.size[0] / 2, Window.size[1] / 12],
                                  color=(0.1, 0.1, 0.1, 1)
                                  ))
        with self.canvas:

            Color(0.1, 0.1, 0.1, 1)

            for i in range(0, len(self.clubs_list)):
                Line(rectangle=[Window.size[0] / 20, Window.size[1] * i / 12, Window.size[0] * 9 / 10, Window.size[1] / 12])


class ClubsScreen(BaseScreen):
    pass


class ClubsScrollView(MDScrollView):

    clubs_list = ClubsList()
    size_hint_y = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ContactScreen(BaseScreen):
    reason_for_contact = StringProperty('Absence')
    reason_num = 0
    reasons_for_contact = ['Absence', 'Late Arrival', 'Early Dismissal']
    border_color = ColorProperty([0, 0, 0, 0])

    date = datetime.datetime.now()
    year = date.year
    year_string = StringProperty(str(year))
    month = date.month
    month_string = StringProperty(CalendarInfo.months[month])
    day = date.day
    day_string = StringProperty(str(day))
    hour = date.hour
    hour_string = StringProperty(str(hour))
    minute = int((numpy.round(date.minute / 15) * 15))
    minute_string = StringProperty(str(minute))
    month_range = calendar.monthrange(year, month)

    need_time = BooleanProperty(False)

    def change_reason(self):
        self.reason_num += 1
        self.reason_num %= 3
        self.change_reason_layout(self.reason_num)
        self.reason_for_contact = self.reasons_for_contact[self.reason_num]

    def change_reason_layout(self, index):
        if index > 0:
            self.border_color = (0, 0, 0, 1)
            self.need_time = True
        else:
            self.border_color = (0, 0, 0, 0)
            self.need_time = False

    def change_day(self):
        self.day = (self.day + 1) % (self.month_range[1] + 1) + math.floor(self.day / self.month_range[1])
        self.day_string = str(self.day)

    def change_month(self):
        self.month = (self.month + 1) % 13 + math.floor(self.month / 12)
        self.month_string = str(CalendarInfo.months[self.month])
        self.month_range = calendar.monthrange(self.year, self.month)

    def change_year(self, change):
        self.year += change
        self.year_string = str(self.year)

    def change_hour(self):
        self.hour = (self.hour + 1) % 24
        self.hour_string = str(self.hour)

    def change_minute(self):
        self.minute = (self.minute + 15) % 60
        self.minute_string = str(self.minute)
        if self.minute_string == '0':
            self.minute_string = '00'

    def send_notice(self):
        global user_name
        temp_dict = {
            'Name': user_name,
            'Type': self.reasons_for_contact[self.reason_num],
            'Date': str(self.year) + '/' + str(self.month) + '/' + str(self.day) + '-' + str(self.hour) +
                    ':' + str(self.minute),
            'Notes': self.ids.Notes.text
        }
        if LOCAL:
            temp = open('Notices.json')
            notices = json.load(temp)
            notices.append(temp_dict)
            with open('Notices.json', "w") as result:
                json.dump(notices, result, indent=4)
        else:
            client.addNotice(temp_dict["Name"], temp_dict["Type"], temp_dict["Date"], temp_dict["Notes"])
        self.ids.Notes.text = ''


class BugWidgets(Widget):
    text_buffer_x = 0
    text_buffer_y = 0

    def __init__(self, **kwargs):
        self.size = Window.size
        self.text_buffer_x = self.width / 40
        self.text_buffer_y = self.height / 200
        super().__init__(**kwargs)
        self.generate_reports()

    def generate_reports(self):
        if not LOCAL:
            p = open("Bugs.json", "w")
            json.dump(client.getBugs(), p, indent=2)
            p.close()


        temp = open('Bugs.json')
        bugs_list = json.load(temp)

        self.create_bug_cards(bugs_list)
        self.create_bug_labels(bugs_list)

    def create_bug_cards(self, file):

        self.canvas.clear()

        with self.canvas:
            for i in range(len(file)):
                Color(255/255, 185/255, 245/255, 1)

                RoundedRectangle(size=[Window.width * 9 / 10, Window.height / 6],
                                 pos=[Window.width / 20, Window.height * (5 / 9 - i / 5)],
                                 radius=(Window.height / 20, Window.height / 20))

                Color(0.1, 0.1, 0.1, 1)

                Line(rounded_rectangle=[Window.size[0] / 20, Window.size[1] * (5 / 9 - i / 5),
                                        Window.size[0] * 9 / 10, Window.size[1] / 6,
                                        Window.height / 20],
                     width=1,
                     close=True)

    def create_bug_labels(self, file):
        for i in range(len(file)):
            self.add_widget(Label(text='Sent by: ' + file[i]['Name'],
                                  size=[Window.size[0] * 8 / 10, Window.size[1] / 20],
                                  text_size=[Window.size[0] * 8 / 10 - 2 * self.text_buffer_x, Window.size[1] / 20],
                                  halign='left',
                                  valign='top',
                                  font_size=Window.size[0] / 22.5,
                                  color=(246 / 255, 232 / 255, 234 / 255, 1),
                                  pos=[Window.size[0] / 10,
                                       Window.size[1] * (6.6 / 10 - i / 5) - self.text_buffer_y]))
            self.add_widget(Label(text=file[i]['Bug'],
                                  size=[Window.size[0] * 8 / 10, Window.size[1] / 40],
                                  text_size=[Window.size[0] * 8 / 10 - 1.5 * self.text_buffer_x, Window.size[1] / 20],
                                  halign='left',
                                  valign='top',
                                  font_size=Window.size[0] / 25,
                                  color=(246 / 255, 232 / 255, 234 / 255, 1),
                                  pos=[Window.size[0] / 10,
                                       Window.size[1] * (6.4 / 10 - i / 5) - self.text_buffer_y]))


class AdminSettings(BaseScreen):

    bug_widgets = BugWidgets()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(self.bug_widgets)


class AttendanceWidgets(Widget):
    text_buffer_x = 0
    text_buffer_y = 0

    def __init__(self, **kwargs):
        self.size = Window.size
        self.text_buffer_x = Window.width / 40
        self.text_buffer_y = Window.height / 200
        super().__init__(**kwargs)
        self.generate_reports()

    def generate_reports(self):
        if not LOCAL:
            p = open("Notices.json", "w")
            json.dump(client.getNotices(), p, indent=2)
            p.close()

        temp = open('Notices.json')
        notices_list = json.load(temp)

        self.create_attendance_cards(notices_list)
        self.create_attendance_labels(notices_list)

    def create_attendance_cards(self, file):

        with self.canvas:
            for i in range(len(file)):
                Color(255/255, 185/255, 245/255, 1)

                RoundedRectangle(size=[Window.width * 9 / 10, Window.height / 6],
                                 pos=[Window.width / 20, Window.height * (5 / 9 - i / 5)],
                                 radius=(Window.height / 20, Window.height / 20))

                Color(0.1, 0.1, 0.1, 1)

                Line(rounded_rectangle=[Window.size[0] / 20, Window.size[1] * (5 / 9 - i / 5),
                                        Window.size[0] * 9 / 10, Window.size[1] / 6,
                                        Window.height / 20],
                     width=1,
                     close=True)

    def create_attendance_labels(self, file):
        for i in range(len(file)):
            self.add_widget(
                Label(text='Sent by: ' + file[i]['Name'] + '   ' + file[i]['Date'] + '   ' + file[i]['Type'],
                      size=[Window.size[0] * 8 / 10, Window.size[1] / 20],
                      text_size=[Window.size[0] * 7.5 / 10 - 2 * self.text_buffer_x, Window.size[1] / 20],
                      halign='left',
                      valign='top',
                      font_size=Window.size[0] / 22.5,
                      color=(0.1, 0.1, 0.1, 1),
                      pos=[Window.size[0] / 10,
                           Window.size[1] * (6.6 / 10 - i / 5) - self.text_buffer_y]))
            self.add_widget(Label(text=file[i]['Notes'],
                                  size=[Window.size[0] * 8 / 10, Window.size[1] / 40],
                                  text_size=[Window.size[0] * 8 / 10 - 1.5 * self.text_buffer_x, Window.size[1] / 20],
                                  halign='left',
                                  valign='top',
                                  font_size=Window.size[0] / 25,
                                  color=(0.1, 0.1, 0.1, 1),
                                  pos=[Window.size[0] / 10,
                                       Window.size[1] * (6.1 / 10 - i / 5) - self.text_buffer_y]))


class AdminContactScreen(BaseScreen):
    attendance_widgets = AttendanceWidgets()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(self.attendance_widgets)


log_in_screen: LogInScreen
main_screen: MainScreen
calendar_screen: CalendarScreen
photos_screen: PostsScreen
clubs_screen: ClubsScreen
contact_screen: ContactScreen
settings_screen: SettingsScreen
admin_settings: AdminSettings
admin_contact: AdminContactScreen


class AppMaybe(MDApp):

    def build(self):
        Window.size = (280, 650)

        sm = ScreenManager()

        global log_in_screen
        global main_screen
        global calendar_screen
        global photos_screen
        global photos_screen
        global clubs_screen
        global settings_screen
        global admin_contact
        global admin_settings
        global contact_screen

        log_in_screen = LogInScreen(name='log_in')
        main_screen = MainScreen(name='main')
        calendar_screen = CalendarScreen(name='calendar')
        posts_screen = PostsScreen(name='posts')
        clubs_screen = ClubsScreen(name='clubs')
        contact_screen = ContactScreen(name='contact')
        settings_screen = SettingsScreen(name='settings')
        admin_settings = AdminSettings(name='admin_settings')
        admin_contact = AdminContactScreen(name='admin_contact')

        sm.add_widget(log_in_screen)
        sm.add_widget(main_screen)
        sm.add_widget(calendar_screen)
        sm.add_widget(posts_screen)
        sm.add_widget(clubs_screen)
        sm.add_widget(contact_screen)
        sm.add_widget(settings_screen)
        sm.add_widget(admin_settings)
        sm.add_widget(admin_contact)
        return sm


if __name__ == '__main__':
    '''
    in_file = jicson.fromFile('Calendar.ics')
    with open('Calendar.json', "w") as result:
            json.dump(in_file, result, indent=4)
    '''
    # Vincent if you want to comment control code, at least explain why
    # L nah

    AppMaybe().run()
