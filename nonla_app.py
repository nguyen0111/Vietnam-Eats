from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.image import Image

Window.size = (360, 640)

class Tab(BoxLayout, MDTabsBase):
    pass

class LoginScreen(MDScreen):
    pass

class MainScreen(MDScreen):
    bag_items = ListProperty([])

    def add_to_bag(self, item_name, price):
        found = False
        for i, (name, p, qty) in enumerate(self.bag_items):
            if name == item_name:
                self.bag_items[i] = (name, p, qty + 1)
                found = True
                break
        if not found:
            self.bag_items.append((item_name, price, 1))
        Clock.schedule_once(lambda dt: self.update_bag_display(), 0)

    def remove_from_bag(self, item_index):
        if 0 <= item_index < len(self.bag_items):
            name, price, qty = self.bag_items[item_index]
            if qty > 1:
                self.bag_items[item_index] = (name, price, qty - 1)
            else:
                del self.bag_items[item_index]
        Clock.schedule_once(lambda dt: self.update_bag_display(), 0)

    def update_bag_display(self, *args):
        bag_view = self.ids.bag_items_box
        bag_view.clear_widgets()
        total = 0.0
        for index, (name, price, qty) in enumerate(self.bag_items):
            try:
                price_value = float(price.replace('€', '').strip()) * qty
                total += price_value
            except Exception:
                continue

            item_box = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp', spacing=10)
            item_box.add_widget(MDLabel(text=name, size_hint_x=0.4))
            item_box.add_widget(MDLabel(text=f"€{price}", size_hint_x=0.2))
            item_box.add_widget(MDLabel(text=f"x{qty}", size_hint_x=0.1))
            remove_btn = MDRaisedButton(text="-", size_hint_x=None, width=30)
            remove_btn.bind(on_release=lambda btn, idx=index: self.remove_from_bag(idx))
            item_box.add_widget(remove_btn)
            add_btn = MDRaisedButton(text="+", size_hint_x=None, width=30)
            add_btn.bind(on_release=lambda btn, item=(name, price): self.add_to_bag(*item))
            item_box.add_widget(add_btn)
            bag_view.add_widget(item_box)

        total_label = MDLabel(text=f"Total: €{total:.2f}", bold=True, halign='center', theme_text_color="Custom", text_color=(0,0,0,1))
        bag_view.add_widget(total_label)
        bag_view.add_widget(MDRaisedButton(text="Pay", pos_hint={"center_x": 0.5}, on_release=self.checkout))

    def checkout(self, *args):
        popup = Popup(title="Successful",
                      content=Label(text="Thank you for ordering"),
                      size_hint=(0.7, 0.3))
        popup.open()

    def on_kv_post(self, base_widget):
        Clock.schedule_once(lambda dt: self.update_bag_display(), 0)

class NonlaApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.theme_style = "Light"

        sm = MDScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(MainScreen(name="menu"))
        sm.current = "login"
        return sm

if __name__ == "__main__":
    Builder.load_file("nonla.kv")
    NonlaApp().run()
