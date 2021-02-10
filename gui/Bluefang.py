# File name: floatlayout.py

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout

class ParentLayout(BoxLayout):
    pass

class BluefangApp(App):
    def build(self):
        return ParentLayout()

if __name__=="__main__":
    BluefangApp().run()