from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, OneLineListItem
import requests

FIREBASE_URL = "https://mkvirtualworld-b4652-default-rtdb.firebaseio.com/"

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        screen = MDScreen()

        # Bottom Navigation (5 Tabs)
        nav = MDBottomNavigation()

        # 1. Home Tab
        home_tab = MDBottomNavigationItem(name='home', text='Home', icon='home')
        home_tab.add_widget(MDLabel(text="Welcome to Home", halign="center"))
        nav.add_widget(home_tab)

        # 2. Shayari Tab (Upload & Read & Delete)
        shayari_tab = MDBottomNavigationItem(name='shayari', text='Shayari', icon='book-open-variant')
        shayari_layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.shayari_input = MDTextField(hint_text="Write Shayari here...")
        upload_btn = MDRaisedButton(text="Upload Shayari", on_release=self.upload_shayari)
        
        self.shayari_list = MDList()
        scroll = MDScrollView()
        scroll.add_widget(self.shayari_list)
        shayari_layout.add_widget(self.shayari_input)
        shayari_layout.add_widget(upload_btn)
        shayari_layout.add_widget(scroll)
        shayari_tab.add_widget(shayari_layout)
        nav.add_widget(shayari_tab)

        # 3. Photo Tab
        photo_tab = MDBottomNavigationItem(name='photo', text='Photo', icon='image')
        photo_tab.add_widget(MDLabel(text="Photo Tab (URL Upload)", halign="center"))
        nav.add_widget(photo_tab)

        # 4. Video Tab
        video_tab = MDBottomNavigationItem(name='video', text='Video', icon='video')
        video_tab.add_widget(MDLabel(text="Video Tab (URL Upload)", halign="center"))
        nav.add_widget(video_tab)

        # 5. Profile Tab
        profile_tab = MDBottomNavigationItem(name='profile', text='Profile', icon='account')
        profile_tab.add_widget(MDLabel(text="User Profile", halign="center"))
        nav.add_widget(profile_tab)

        screen.add_widget(nav)
        return screen

    def on_start(self):
        self.load_shayari()

    # Upload Data to Firebase
    def upload_shayari(self, instance):
        text = self.shayari_input.text
        if text:
            data = {"text": text}
            requests.post(f"{FIREBASE_URL}/shayari.json", json=data)
            self.shayari_input.text = ""
            self.load_shayari()

    # Load Data from Firebase
    def load_shayari(self):
        self.shayari_list.clear_widgets()
        response = requests.get(f"{FIREBASE_URL}/shayari.json")
        data = response.json()
        if data:
            for key, value in data.items():
                item = OneLineListItem(text=value.get("text", ""))
                self.shayari_list.add_widget(item)

if __name__ == '__main__':
    MainApp().run()
