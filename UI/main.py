from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import Clock
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from Backend.apiconnect import ApiConnect
import time
import requests
from plyer import gps
from location import Locate
from plyer.utils import platform


class FirstWindow(MDScreen):
    # Attributes
    counter = 0
    elapsed_time = None

    # A method to switch screen
    def search(self, *args):
        self.manager.current = "search_resto"
        self.manager.transition.direction = "left"

    # A method to time before calling search function - to switch to search screen
    def on_act(self):
        self.counter = 1
        self.manager.get_screen("welcome").ids.Location.text = "Welcome"
        Clock.schedule_once(self.search, 0.5)

    # A method that changes text on the switch button
    def on_inact(self):
        self.counter = 0
        self.manager.get_screen("welcome").ids.Location.text = "Let's find you!"


# A SecondWindow class with ten methods
class SecondWindow(MDScreen):
    init_time = time.time()
    anim = None
    anim1 = None
    # lat = "9.0567"
    # lon = "7.4969"
    # lat = app.gps_update()
    conn_res = []

    if platform == "android" or "ios":
        get_gps = Locate()
        # lat = get_gps.gps_locate()[0]
        # lon = get_gps.gps_locate()[1]
        lat = "9.0567"
        lon = "7.4969"
    else:
        lat = "9.0567"
        lon = "7.4969"

    def conn(self):
        try:
            connect = ApiConnect()
            res = connect.connect_google_api(self.lat, self.lon)
            list_gen = connect.extract(res)
            return list_gen
        except requests.exceptions.ConnectionError:
            return f"Connection Error"

    def on_enter(self):
        self.tap_label()
        self.tap_label_()

    def just_blink(self):
        self.blink()
        Clock.schedule_once(self.next, 3)

    def blink(self):
        # Animation that changes the size and radius of a tap button
        self.anim = Animation(outer_opacity=0, tap_size=120)
        self.anim.bind(on_complete=self.reset)
        self.anim.start(self)
        self.manager.get_screen("search_resto").ids.tap_label.text = "Searching"

    def tap_label(self):
        self.anim1 = Animation(opa=0, step=0, transition="linear")
        self.anim1.bind(on_complete=self.reset_label)
        self.anim1.start(self)

    def tap_label_(self):
        self.anim1 = Animation(opa=0.5, step=0, transition="linear")
        self.anim1.bind(on_complete=self.reset_label_)
        self.anim1.start(self)

    def reset(self, *args):
        self.outer_opacity = 0.3
        self.tap_size = self.d_tap_size
        self.blink()

    def reset_label(self, *args):
        self.opa = 0
        self.tap_label_()

    def reset_label_(self, *args):
        self.opa = 0.3
        self.tap_label()

    def next(self, *args):
        self.manager.current = "search_result"
        self.manager.transition.direction = "left"
        self.tap_size = self.d_tap_size - 25
        self.anim.cancel_all(self)
        self.anim1.cancel_all(self)
        self.manager.get_screen("search_resto").ids.tap_label.text = "Tap to search"


# A ResultWindow class with methods and attribute
class ResultWindow(MDScreen):
    # Attribute
    button_radius = 28

    # creating an object from SecondWindow class
    win = SecondWindow()

    # A callback Method to switch screens
    def callback(self, button):
        self.manager.current = "search_resto"
        self.manager.transition.direction = "right"
        self.manager.get_screen("search_result").ids.container.clear_widgets()
        self.manager.get_screen("search_result").ids.info.clear_widgets()
        x_th = self.win
        x_th.conn_res = None

    # Initiate a blocks of code once ResultWindow Screen enters
    def on_enter(self):
        x_th = self.win


        list_gen = x_th.conn()
        x = isinstance(list_gen, list)
        if len(list_gen) > 0 and x:
            for i in list_gen:
                card = MDCard(
                    md_bg_color="lightblue",
                    padding=[10, 10, 10, 10],
                    spacing="50",
                    radius=[15, 15, 15, 15],
                    orientation="vertical",
                    size_hint=[self.width, None],
                    elevation=2,
                    height="100dp"
                )

                # Create a content Boxlayout
                content = MDBoxLayout(
                    orientation="vertical",
                    padding="2dp"
                )

                # Add content to the content Boxlayout
                content.add_widget(MDLabel(
                    text=f" " + f"{i['name']}".capitalize(),
                    font_name="Roboto",
                    font_style="H5",
                    bold=True,
                    theme_text_color="Custom",
                    text_color=(0, 0, 0, 1)
                ))

                content.add_widget(MDLabel(
                    text=f"Place: {i['vicinity']}\nRatings: {i['rating']}/5",
                    font_style="Body2",
                    padding="8dp"
                ))

                # Add content BoxLayout to the card.
                card.add_widget(content)

                # Add card to container
                self.manager.get_screen("search_result").ids.container.add_widget(
                    card
                )
        elif len(list_gen) == 0 and x:
            # Add content to the content Boxlayout
            box_layout = MDBoxLayout(
                orientation="vertical",
                padding="8dp"
            )
            no_contents = MDLabel(
                text=f"No Result",
                font_name="Roboto",
                font_style="H3",
                halign="center",
                theme_text_color="Error",
                pos_hint={"y": 0.5}
            )

            box_layout.add_widget(no_contents)
            self.manager.get_screen("search_result").ids.info.add_widget(
                box_layout
            )
        else:

            no_content = MDLabel(
                text=list_gen,
                font_name="Roboto",
                font_style="H5",
                halign="center",
                theme_text_color="Error",
                pos_hint={"center_y": 0.5}
            )

            # box_layout.add_widget(no_content)
            self.manager.get_screen("search_result").ids.info.add_widget(
                no_content
            )


# MainApp class
class MainApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FirstWindow(name="welcome"))
        sm.add_widget(SecondWindow(name="search_resto"))
        sm.add_widget(ResultWindow(name="search_result"))

        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Red"
        return Builder.load_file("resto.kv")


MainApp().run()
