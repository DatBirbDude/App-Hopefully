import os, sys
os.environ["KIVY_NO_CONSOLELOG"] = "1" # Suppress kivy output
from kivy.resources import resource_add_path, resource_find
import json
import math
import calendar
import datetime
from kivymd.icon_definitions import md_icons
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
from kivymd.uix.button import MDRoundFlatButton, MDIconButton, MDRectangleFlatButton
from kivymd.uix.card import MDCard
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
LOCAL = False
screen_num = -1

# Screen Shifting variable
screen_num = -1

# Gives user access to the admin screens if admin = True
def make_admin():
    settings_screen.make_admin()
    admin_settings.make_admin()
    contact_screen.make_admin()
    admin_contact.make_admin()


# Thread decorator to be used to live update the app
def mainthread(func):
    def delayed_func(*args):
        def callback_func(dt):
            func(*args)

        Clock.schedule_once(callback_func, 0)

    return delayed_func


# Button that switches to the admin version of a screen
class AdminButton(MDRectangleFlatButton):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Go To Admin\nScreen'
        self.pos = (Window.width * 6 / 10, Window.height / 9)
        self.size = (Window.width / 3, Window.height / 15)
        self.font_size = Window.height / 50
        self.text_color = (0.1, 0.1, 0.1, 1)
        self.line_color = (0.1, 0.1, 0.1, 1)
        self.disabled = True
        self.opacity = 0

    # Updates widget if size changes and BaseScreen.on_size() is called
    def update_wid(self):
        self.pos = (Window.width * 6 / 10, Window.height / 9)
        self.size = (Window.width / 3, Window.height / 15)
        self.font_size = Window.height / 50


# Parent screen - Allows settings, contact, and back buttons to work
class BaseScreen(Screen):

    # Changes to the "settings" screen
    def settings_button_press(self):
        global screen_num
        self.manager.transition.direction = 'right'
        screen_num = 0
        self.manager.current = 'settings'

    # Changes to "clubs" screen
    def clubs_button_press(self):
        global screen_num
        if screen_num < 1:
            self.manager.transition.direction = 'left'
        else:
            self.manager.transition.direction = 'right'
        screen_num = 1
        self.manager.current = 'clubs'

    # Changes to "calendar" screen
    def calendar_button_press(self):
        global screen_num
        if screen_num < 2:
            self.manager.transition.direction = 'left'
        else:
            self.manager.transition.direction = 'right'
        screen_num = 2
        self.manager.current = 'calendar'

    # Changes to "posts" screen
    def posts_button_press(self):
        global screen_num
        if screen_num < 3:
            self.manager.transition.direction = 'left'
        else:
            self.manager.transition.direction = 'right'
        screen_num = 3
        self.manager.current = 'posts'

    # Changes to the "contact administration" screen
    def contact_button_press(self):
        global screen_num
        if screen_num < 4:
            self.manager.transition.direction = 'left'
        else:
            self.manager.transition.direction = 'right'
        screen_num = 4
        self.manager.current = 'contact'

    # Changes to the "add posts" screen
    def add_post_button_press(self):
        global screen_num
        self.manager.transition.direction = 'left'
        screen_num = 5
        self.manager.current = 'add_post'

    # Changes to the "admin settings" screen
    def admin_settings_button_press(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'admin_settings'

    # Changes to the "admin contact administration" screen
    def admin_contact_button_press(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'admin_contact'

    # Function to change properties when size is changed
    def on_size(self, instance, value):
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

        # Updating BugWidgets in the .py file
        BugWidgetsScroll.bug_widgets.text_buffer_x = Window.size[0] / 40
        BugWidgetsScroll.bug_widgets.text_buffer_y = Window.size[1] / 200
        BugWidgetsScroll.bug_widgets.generate_reports()

        # Updating AttendanceWidgets in the .py file
        AttendanceWidgets.size = Window.size
        AttendanceScroll.attendance_widgets.text_buffer_x = Window.size[0] / 40
        AttendanceScroll.attendance_widgets.text_buffer_y = Window.size[1] / 200
        AttendanceScroll.attendance_widgets.generate_reports()

        # Updating ClubsList in the .py file
        ClubsScrollView.clubs_list.update_canvas()
        ClubsScrollView.clubs_list.create_list()

        # Updating PostsList in the .py file
        PostsScroll.posts_list.padding = (Window.width / 20, 0, Window.width / 20, 0)
        PostsScroll.posts_list.loadPosts()

        # Updating AdminButtons in the .py file
        self.ids.AdminSettingsButton.update_wid()
        self.ids.AdminContactButton.update_wid()
        self.ids.ReturnSettingsButton.update_wid()
        self.ids.ReturnContactButton.update_wid()


# Log In Screen (Screen appears directly after opening app
class LogInScreen(Screen):

    # allows "log in" screen to edit the user's username
    global user_name
    global admin

    # Changes to "calendar" screen if the user logs in with valid credentials (in Credentials.json)
    def check_login(self):
        global user_name
        global admin
        logins = json.load(open('Credentials.json'))
        self.ids.FailedLoginLabel.text = ''
        if LOCAL: # Log in sequence when user is disconnected from server
            if self.ids.UsernameInput.text in logins['admins']:
                if self.ids.PasswordInput.text == logins['admins'][self.ids.UsernameInput.text]['Password']:
                    user_name = logins['admins'][self.ids.UsernameInput.text]['Name']
                    admin = True
                    self.manager.current = 'calendar'
                else:
                    self.ids.FailedLoginLabel.text = 'Your password is incorrect'
            elif self.ids.UsernameInput.text in logins['users']:
                if self.ids.PasswordInput.text == logins['users'][self.ids.UsernameInput.text]['Password']:
                    user_name = logins['users'][self.ids.UsernameInput.text]['Name']
                    self.manager.current = 'calendar'
                else:
                    self.ids.FailedLoginLabel.text = 'Your password is incorrect'
            else:
                self.ids.FailedLoginLabel.text = 'Username not found'
        else: # Log in sequence when user is connected to server
            print("Sending" + self.ids.UsernameInput.text + self.ids.PasswordInput.text)
            result = client.login(self.ids.UsernameInput.text, self.ids.PasswordInput.text)
            privilege = result["res"]
            user_name = result["name"]
            print("Welcome " + user_name)
            if privilege == 3:
                admin = True
                self.manager.current = 'calendar'
            elif privilege == 2:
                admin = False
                self.manager.current = 'calendar'
            elif privilege == 1:
                admin = False
                self.ids.FailedLoginLabel.text = 'Your password is incorrect'
            elif privilege == 0:
                admin = False
                self.ids.FailedLoginLabel.text = 'Username not found'
            else:
                self.ids.FailedLoginLabel.text = 'How did you even get this message?'

        # Activates AdminButtons if admin == True
        make_admin()

        self.ids.UsernameInput.text = ''
        self.ids.PasswordInput.text = ''


# Screen that allows users to add new accounts
class SignUpScreen(Screen):

    # Creates new user if the inputted username is unique
    def sign_up(self):

        new_name = self.ids.NameInput.text
        new_username = self.ids.NewUsernameInput.text
        new_password = self.ids.NewPasswordInput.text
        logins = json.load(open('Credentials.json'))
        if LOCAL:
            if not (new_username in logins['admins'] or new_username in logins['users']):
                logins['users'].update({new_username: {'Password': new_password, 'Name': new_name}})
                with open('Credentials.json', "w") as result:
                    json.dump(logins, result, indent=4)
                self.manager.current = 'log_in'
            else:
                print('Username already in use')
        else:
            result = client.signup(self.ids.NewUsernameInput.text, self.ids.NewPasswordInput.text, self.ids.NameInput.text)
            #Error mimics privilege, but we are looking for users with unique usernames and passwords this time
            error = result["error"]
            user_name = result["new user"]["Name"]
            print("Welcome " + user_name)
            if error < 1:
                self.manager.current = 'log_in'
            else:
                print('Username already in use')

        self.ids.NameInput.text = ''
        self.ids.NewUsernameInput.text = ''
        self.ids.NewPasswordInput.text = ''


# Screen that allows for bug reports and logging out
class SettingsScreen(BaseScreen):

    # Reveals the "settings" screen admin button if admin == True
    def make_admin(self):
        if admin:
            self.ids.AdminSettingsButton.disabled = False
            self.ids.AdminSettingsButton.opacity = 1
        else:
            self.ids.AdminSettingsButton.disabled = True
            self.ids.AdminSettingsButton.opacity = 0

    # Initializer method
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.make_admin()

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

        BugWidgetsScroll.bug_widgets.generate_reports()


# Parent class with all necessary date information
class CalendarInfo(Screen):

    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
              7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    date = datetime.date.today()  # Gets today's date
    year = date.year # The current year
    month = date.month # The current month
    day = date.day # The current day
    month_range = calendar.monthrange(year, month) # The number of days in the current month
    weekday_offset = (date.weekday() + 1) % 7  # Formats days to always go from sunday to saturday


# Screen that shows the events on a given day
class CalendarScreen(CalendarInfo, BaseScreen):

    # Increments or decrements the month
    def month_change(self, change):
        if (CalendarInfo.month == 12 and change > 0) or (CalendarInfo.month == 1 and change < 0):
            CalendarInfo.year += int(math.ceil(change / int(abs(change)) * change / 12) * change / int(abs(change)))
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

    # Initializer method
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(self.label)  # adds month/year label


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

    # Uses information in the .json file to create the event labels
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

    # Initializer method
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = Window.size
        self.do_the_json()
        self.update_canvas()
        self.create_event_labels()

    # Creates a number of boxes based on the number of events on the given day
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


# Creates the selection circle and weekday letters on the "calendar" screen
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

    # Initializer method
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

    # Updates the location of selection circle
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

    # Shifts layout after a change in week
    def week_change(self, change):
        if 0 < (CalendarInfo.day - CalendarInfo.weekday_offset + 6 + 7 * change) or change > 0:
            if (CalendarInfo.day - CalendarInfo.weekday_offset + 7 * change) < \
                    CalendarInfo.month_range[1] or change < 0:
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

    # Changes selection circle location after a change in day
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


# Shows the changing day numbers in the "calendar" screen
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

    # Initializer method
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(self.box_layout)


# List layout for the "calendar" screen
class ListLayout(CalendarInfo):
    event_widgets = EventWidgets()
    day_nums_layout = DayNumsLayout()
    day_nums_labels = DayNumsLabels()

    # Initializer method
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(self.event_widgets)
        self.add_widget(self.day_nums_layout)
        self.add_widget(self.day_nums_labels)


# The next class is a sample from official kivy documentation, don't touch it or it will break everything
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


# Screen that shows the posts on the Starlight instagram
class PostsScreen(BaseScreen):

    # Initializer method
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# Allows users to choose photos to upload to instagram
class Filechooser(BoxLayout):
    def select(self, *args):
        try:
            self.label.text = args[1][0]
        except:
            pass


# Widgets with each post from the Starlight instagram
class Posts(GridLayout):
    cols = 2
    size_hint_y = None
    pos_hint = {'center_x': 0.5, 'center_y': 0.5}
    padding = [Window.width / 20, 0, Window.width / 20, 0]
    text_buffer_x = 0
    text_buffer_y = 0

    # Initializer method
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_load_thread()

    def start_load_thread(self, *args):
        Thread(target=self.loadPosts, daemon=True).start()

    # Updates the canvas that is below the text on screen
    def update_canvas_before(self, posts):

        with self.canvas:
            for item in posts["posts"]:
                Color(255 / 255, 185 / 255, 245 / 255, 0.8)

                Rectangle(size=(Window.width * 9 / 10, Window.height / 3),
                          pos=(Window.width / 20, Window.height * (5 * item['num'] + 1) / 12))

    # Updates the canvas that is above the text on screen
    def update_canvas_after(self, posts):

        with self.canvas:
            for item in posts["posts"]:
                Color(0.1, 0.1, 0.1, 1)

                Line(rectangle=[Window.width / 20, Window.height * (5 * item['num'] + 1) / 12,
                                Window.width * 9 / 10, Window.height / 3])

                Line(rectangle=[Window.width / 2, Window.height * (5 * item['num'] + 1) / 12,
                                Window.width * 4.5 / 10, Window.height / 3])

                Line(rectangle=[Window.width / 20, Window.height * (5 * item['num'] + 1) / 12,
                                Window.width * 9 / 10, Window.height / 4])

                Line(rectangle=[Window.width / 2, Window.height * (5 * item['num'] + 1) / 12,
                                Window.width * 4.5 / 10, Window.height / 6])

    # Loads the posts from instagram
    @mainthread
    def loadPosts(self, *_):

        self.clear_widgets()


        # Attempt to fetch the latest posts from server if allowed

        if not LOCAL:
            p = open("posts.json", "w")
            json.dump(client.getPosts(), p, indent=2)
            p.close()
        p = open("posts.json")
        posts = json.load(p)
        # Async draw in all posts
        self.canvas.clear()
        self.update_canvas_before(posts)
        self.text_buffer_x = Window.width / 40
        self.text_buffer_y = Window.height / 200
        for item in posts["posts"]:
            self.add_widget(Label(text='By: ' + item['author'], size_hint_y=None,
                                  height=Window.height / 12, color=(0.1, 0.1, 0.1, 1),
                                  text_size=(Window.width * 4.5 / 10 - 2 * self.text_buffer_x,
                                             Window.height / 12 - 2 * self.text_buffer_y),
                                  valign='center', font_size=Window.height / 50,
                                  halign='center', pos_hint={'center_x': 0.5}))
            self.add_widget(Label(text='Date: ' + item['date'], color=(0.1, 0.1, 0.1, 1),
                                  text_size=(Window.width * 4.5 / 10 - 2 * self.text_buffer_x,
                                             Window.height / 12 - 2 * self.text_buffer_y),
                                  valign='center', halign='center',
                                  font_size=Window.height / 50))
            self.add_widget(AsyncImage(source=item["url"], size_hint=(1, None),
                                       height=Window.height / 4, mipmap=False))
            box_layout = BoxLayout(orientation='vertical')
            box_layout.add_widget(Label(text=item['name'], size_hint_y=None,
                                        height=Window.height / 12, color=(0.1, 0.1, 0.1, 1),
                                        text_size=(Window.width * 4.5 / 10 - 2 * self.text_buffer_x,
                                                   Window.height / 12 - 2 * self.text_buffer_y), valign='center',
                                        halign='left', font_size=Window.height / 50))
            box_layout.add_widget(Label(text=item['desc'], size_hint_y=None,
                                        height=Window.height / 6, color=(0.1, 0.1, 0.1, 1),
                                        text_size=(Window.width * 4.5 / 10 - 2 * self.text_buffer_x,
                                                   Window.height / 6 - 2 * self.text_buffer_y), valign='center',
                                        halign='left', font_size=Window.height / 55,
                                        pos_hint={'center_x': 0.5}))
            self.add_widget(box_layout)
            for i in range(0, 2):
                self.add_widget(Label(size_hint_y=None, height=Window.height / 12))

            self.update_canvas_after(posts)


# Allows the "posts" screen to scroll
class PostsScroll(ScrollView):
    posts_list = Posts()
    posts_list.bind(minimum_height=posts_list.setter('height'))
    always_overscroll = False

    # Initializer method
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(self.posts_list)


# Screen in which users can add posts to the starlight instagram
class AddPostScreen(BaseScreen):

    # Method to add post to instagram
    def addPost(self, *args):
        global user_name

        def post(instance):
            path = instance.content.label.text
            if path != "" and path[-4:] == ".jpg":
                client.addPost(self.ids.NameInput.text, user_name, self.ids.DescriptionInput.text, path)
                self.ids.NameInput.text = ''
                self.ids.DescriptionInput.text = ''
            return False

        content = Filechooser()
        popup = Popup(content=content, size_hint=(0.9, 0.9))
        popup.bind(on_dismiss=post)
        popup.open()

        return


# List of clubs here at South River High School
class ClubsList(GridLayout):
    cols = 1
    size_hint_y = None
    pos_hint = {'center_x': 0.5, 'center_y': 0.5}

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

    # Initializer method
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_canvas()
        self.create_list()

    # Creates the text widgets for each club
    def create_list(self):

        self.clear_widgets()

        self.add_widget(Label(text='Clubs at SRHS:',
                              font_size=Window.size[1] / 35,
                              size_hint=(1, None),
                              pos_hint={'center_x': 0.5, 'center_y': 0.5},
                              height=Window.size[1] / 6,
                              font_name='Fonts/Vogue.ttf',
                              color=(0.1, 0.1, 0.1, 1)
                              ))
        for i in range(0, len(self.clubs_list)):
            self.add_widget(Label(text=self.clubs_list[i],
                                  font_size=Window.size[1] / 50,
                                  size_hint=(1, None),
                                  pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                  halign='center',
                                  valign='center',
                                  height=Window.size[1] / 12,
                                  text_size=[Window.size[0] / 2, Window.size[1] / 12],
                                  color=(0.1, 0.1, 0.1, 1)
                                  ))

    # Updates the boxes around each club's text widget
    def update_canvas(self):

        self.canvas.clear()

        with self.canvas:

            Color(0.1, 0.1, 0.1, 1)

            for i in range(0, len(self.clubs_list)):
                Line(rectangle=[Window.size[0] / 20, Window.size[1] * i / 12, Window.size[0] * 9 / 10,
                                Window.size[1] / 12])


# Screen that shows all the clubs at South River High School
class ClubsScreen(BaseScreen):
    pass


# Allows clubs screen to scroll through all the clubs
class ClubsScrollView(MDScrollView):
    clubs_list = ClubsList()
    clubs_list.bind(minimum_height=clubs_list.setter('height'))
    size_hint_y = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(self.clubs_list)


# Screen where users can report absences to school administration
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
    minute = int((math.floor(date.minute / 15) * 15))
    minute_string = StringProperty(str(minute))
    month_range = calendar.monthrange(year, month)

    need_time = BooleanProperty(False)

    # Reveals the admin button for the "contact administration" screen if admin == True
    def make_admin(self):
        if admin:
            self.ids.AdminContactButton.disabled = False
            self.ids.AdminContactButton.opacity = 1
        else:
            self.ids.AdminContactButton.disabled = True
            self.ids.AdminContactButton.opacity = 0

    # Initializer method
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.make_admin()

    # Changes the type of absence (i.e. Absent, Early Dismissal, Late Arrival)
    def change_reason(self):
        self.reason_num += 1
        self.reason_num %= 3
        self.change_reason_layout(self.reason_num)
        self.reason_for_contact = self.reasons_for_contact[self.reason_num]

    # Changes the type of absence shown on screen
    def change_reason_layout(self, index):
        if index > 0:
            self.border_color = (0, 0, 0, 1)
            self.need_time = True
        else:
            self.border_color = (0, 0, 0, 0)
            self.need_time = False

    # Changes the day the user is reporting their absence
    def change_day(self):
        self.day = (self.day + 1) % (self.month_range[1] + 1) + math.floor(self.day / self.month_range[1])
        self.day_string = str(self.day)

    # Changes the month the user is reporting their absence
    def change_month(self):
        self.month = (self.month + 1) % 13 + math.floor(self.month / 12)
        self.month_string = str(CalendarInfo.months[self.month])
        self.month_range = calendar.monthrange(self.year, self.month)

    # Chnages the year the user is reporting their absence
    def change_year(self, change):
        self.year += change
        self.year_string = str(self.year)

    # Changes the hour the user is reporting their absence
    def change_hour(self):
        self.hour = (self.hour + 1) % 24
        self.hour_string = str(self.hour)

    # Changes the minute (in increments of 15) the user is reporting their absence
    def change_minute(self):
        self.minute = (self.minute + 15) % 60
        self.minute_string = str(self.minute)
        if self.minute_string == '0':
            self.minute_string = '00'

    # Sends the absence notice to backend server
    def send_notice(self):
        global user_name
        if self.reason_num > 0:
            temp_dict = {
                'Name': user_name,
                'Type': self.reasons_for_contact[self.reason_num],
                'Date': str(self.month) + '/' + str(self.day) + '/' + str(self.year) + '-' + self.hour_string +
                        ':' + self.minute_string,
                'Notes': self.ids.Notes.text
            }
        else:
            temp_dict = {
                'Name': user_name,
                'Type': self.reasons_for_contact[self.reason_num],
                'Date': str(self.month) + '/' + str(self.day) + '/' + str(self.year),
                'Notes': self.ids.Notes.text
            }
        if LOCAL:
            temp = open('Notices.json')
            notices = json.load(temp)
            notices.append(temp_dict)
            with open('Notices.json', "w") as result:
                json.dump(notices, result, indent=4)
        else:
            client.addNotice(temp_dict["Name"], temp_dict["Type"], temp_dict["Notes"], temp_dict["Date"])

        AttendanceScroll.attendance_widgets.generate_reports()
        self.ids.Notes.text = ''


# The list of widgets for each bug report on the "admin settings" screen
class BugWidgets(GridLayout):
    cols = 1
    size_hint_y = None
    pos_hint = {'center_x': 0.5, 'center_y': 0.5}
    spacing = (0, Window.height / 30)
    padding = [0, Window.height / 50, 0, 0]
    text_buffer_x = 0
    text_buffer_y = 0

    # Initializer method
    def __init__(self, **kwargs):
        self.text_buffer_x = Window.width / 40
        self.text_buffer_y = Window.height / 200
        super().__init__(**kwargs)
        self.generate_reports()

    # Retrieves and generates bug reports
    def generate_reports(self):
        if not LOCAL:
            p = open("Bugs.json", "w")
            json.dump(client.getBugs(), p, indent=2)
            p.close()

        temp = open('Bugs.json')
        bugs_list = json.load(temp)

        self.size = (Window.width, Window.height * len(bugs_list) / 5)

        self.clear_widgets()
        self.create_bug_cards(bugs_list)
        self.create_bug_labels(bugs_list)

    # Creates the boxes each bug report is inside of
    def create_bug_cards(self, file):

        self.canvas.clear()

        with self.canvas:
            for i in range(len(file)):
                Color(255 / 255, 185 / 255, 245 / 255, 1)

                RoundedRectangle(size=[Window.width * 9 / 10, Window.height / 6],
                                 pos=[Window.width / 20, self.height - Window.height * (1 / 6 + i / 5)],
                                 radius=(Window.height / 60, Window.height / 60))

                Color(0.1, 0.1, 0.1, 1)

                Line(rounded_rectangle=[Window.size[0] / 20, self.height - Window.height * (1 / 6 + i / 5),
                                        Window.size[0] * 9 / 10, Window.size[1] / 6,
                                        Window.height / 60],
                     width=1,
                     close=True)

    # Creates the text for each report
    def create_bug_labels(self, file):
        for i in range(len(file)):
            grid_layout = GridLayout(cols=1, spacing=(0, Window.height / 50), size_hint_y=None,
                                     height=Window.height / 6)
            grid_layout.add_widget(Label(text='Sent by: ' + file[i]['Name'],
                                         size_hint=(0.8, .2),
                                         pos_hint={'left': 0, 'center_y': 0.5},
                                         text_size=[Window.size[0] * 8 / 10 - 2 * self.text_buffer_x,
                                                    Window.size[1] / 30],
                                         halign='left',
                                         valign='top',
                                         font_size=Window.size[0] / 22.5,
                                         color=(.1, .1, .1, 1)))
            grid_layout.add_widget(Label(text=file[i]['Bug'],
                                         size_hint=(0.8, .8),
                                         pos_hint={'center_x': 0.5, 'top': 0},
                                         text_size=[Window.size[0] * 8 / 10 - 1.5 * self.text_buffer_x,
                                                    Window.size[1] * 2 / 15],
                                         halign='left',
                                         valign='top',
                                         font_size=Window.size[0] / 25,
                                         color=(.1, .1, .1, 1)))
            self.add_widget(grid_layout)


# Screen where admins can see bug reports
class AdminSettings(BaseScreen):

    # Activates the return AdminButton if admin == True
    def make_admin(self):
        if admin:
            self.ids.ReturnSettingsButton.disabled = False
            self.ids.ReturnSettingsButton.opacity = 1
        else:
            self.ids.ReturnSettingsButton.disabled = True
            self.ids.ReturnSettingsButton.opacity = 0

    # Initializer method
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.make_admin()


# Allows "admin settings" screen to scroll through the bug reports
class BugWidgetsScroll(ScrollView):
    bug_widgets = BugWidgets()
    bug_widgets.bind(minimum_height=bug_widgets.setter('height'))

    # Initializer method
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(self.bug_widgets)


# List of widgets of absence reports for "admin contact administration" screen
class AttendanceWidgets(GridLayout):

    cols = 1
    size_hint_y = None
    pos_hint = {'center_x': 0.5, 'center_y': 0.5}
    spacing = (0, Window.height / 30)
    padding = [0, Window.height / 50, 0, 0]
    text_buffer_x = 0
    text_buffer_y = 0

    # Initializer method
    def __init__(self, **kwargs):
        self.size = Window.size
        self.text_buffer_x = Window.width / 40
        self.text_buffer_y = Window.height / 200
        super().__init__(**kwargs)
        self.generate_reports()

    # Retrieves and creates absence reports
    def generate_reports(self):
        if not LOCAL:
            p = open("Notices.json", "w")
            json.dump(client.getNotices(), p, indent=2)
            p.close()

        temp = open('Notices.json')
        notices_list = json.load(temp)

        self.height = Window.height * (len(notices_list) / 5 - 1/60)
        self.create_attendance_cards(notices_list)
        self.create_attendance_labels(notices_list)

    # Creates boxes for attendance reports to be inside of
    def create_attendance_cards(self, file):

        self.canvas.clear()

        with self.canvas:
            for i in range(len(file)):
                Color(255 / 255, 185 / 255, 245 / 255, 1)

                RoundedRectangle(size=[Window.width * 9 / 10, Window.height / 6],
                                 pos=[Window.width / 20, self.height - Window.height * (1 / 6 + i / 5)],
                                 radius=(Window.height / 60, Window.height / 60))

                Color(0.1, 0.1, 0.1, 1)

                Line(rounded_rectangle=[Window.size[0] / 20, self.height - Window.height * (1 / 6 + i / 5),
                                        Window.size[0] * 9 / 10, Window.size[1] / 6,
                                        Window.height / 60],
                     width=1,
                     close=True)

    # Creates text widgets for attendance reports
    def create_attendance_labels(self, file):

        self.clear_widgets()

        for i in range(len(file)):
            grid_layout = GridLayout(cols=1, size_hint_y=None,
                                     height=Window.height / 6)
            grid_layout.add_widget(
                Label(text='Sent by: ' + file[i]['Name'] + '   ' + file[i]['Date'] + '   ' + file[i]['Type'],
                      size_hint=(0.8, .3),
                      pos_hint={'left': 0, 'center_y': 0.5},
                      text_size=[Window.size[0] * 8 / 10 - 2 * self.text_buffer_x,
                                 Window.size[1] / 20],
                      halign='left',
                      valign='top',
                      font_size=Window.size[0] / 22.5,
                      color=(.1, .1, .1, 1)))
            grid_layout.add_widget(Label(text=file[i]['Notes'],
                                         size_hint=(0.8, .7),
                                         pos_hint={'center_x': 0.5, 'top': 0},
                                         text_size=[Window.size[0] * 8 / 10 - 1.5 * self.text_buffer_x,
                                                    Window.size[1] * 7 / 60],
                                         halign='left',
                                         valign='top',
                                         font_size=Window.size[0] / 25,
                                         color=(.1, .1, .1, 1)))

            self.add_widget(grid_layout)


# Allows "admin contact screen" to scroll through absence reports
class AttendanceScroll(ScrollView):
    attendance_widgets = AttendanceWidgets()
    attendance_widgets.bind(minimum_height=attendance_widgets.setter('height'))

    # Initializer method
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(self.attendance_widgets)


# Screen that allows admins to see absence reports from users
class AdminContactScreen(BaseScreen):

    # Activates the return AdminButton for this screen
    def make_admin(self):
        if admin:
            self.ids.ReturnContactButton.disabled = False
            self.ids.ReturnContactButton.opacity = 1
        else:
            self.ids.ReturnContactButton.disabled = True
            self.ids.ReturnContactButton.opacity = 0

    # Initializer method
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.make_admin()


# Instances of each screen
log_in_screen: LogInScreen
sign_up_screen: SignUpScreen
calendar_screen: CalendarScreen
photos_screen: PostsScreen
add_post_screen: AddPostScreen
clubs_screen: ClubsScreen
contact_screen: ContactScreen
settings_screen: SettingsScreen
admin_contact: AdminContactScreen
admin_settings: AdminSettings


# App
class StarLight(MDApp):

    # Builds app
    def build(self):
        Window.size = (280, 650)

        sm = ScreenManager()

        global log_in_screen
        global sign_up_screen
        global calendar_screen
        global photos_screen
        global add_post_screen
        global clubs_screen
        global contact_screen
        global settings_screen
        global admin_contact
        global admin_settings

        log_in_screen = LogInScreen(name='log_in')
        sign_up_screen = SignUpScreen(name='sign_up')
        calendar_screen = CalendarScreen(name='calendar')
        posts_screen = PostsScreen(name='posts')
        add_post_screen = AddPostScreen(name='add_post')
        clubs_screen = ClubsScreen(name='clubs')
        contact_screen = ContactScreen(name='contact')
        settings_screen = SettingsScreen(name='settings')
        admin_settings = AdminSettings(name='admin_settings')
        admin_contact = AdminContactScreen(name='admin_contact')

        # Adds screens to screen manager
        sm.add_widget(log_in_screen)
        sm.add_widget(sign_up_screen)
        sm.add_widget(calendar_screen)
        sm.add_widget(posts_screen)
        sm.add_widget(add_post_screen)
        sm.add_widget(clubs_screen)
        sm.add_widget(contact_screen)
        sm.add_widget(settings_screen)
        sm.add_widget(admin_settings)
        sm.add_widget(admin_contact)
        return sm


# Runs the file
if __name__ == '__main__':

    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))

    StarLight().run()
