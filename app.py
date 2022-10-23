from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
Window.size = (350, 500)

screen_helper = """
ScreenManager:
    MenuScreen:
    Scan:
    Help:

<MenuScreen>:
    name: 'menu'
    MDTopAppBar:
        title: 'PLATE NUMBER RECOGNITION'
        pos_hint: {"top":1}

    Image:
        source: 'logo.png'
        pos_hint: {"center_x":0.5, "center_y":0.6}
        size_hint:(0.65,0.65)
        
    MDFillRoundFlatButton:
        text: 'SCAN'
        font_size: '20'
        pos_hint: {'center_x':0.5,'center_y':0.30}
        size_hint: (0.5,0.10)
        on_press: root.manager.current = 'scan'

    MDFillRoundFlatButton:
        text: 'HELP'
        font_size: '20'
        pos_hint: {'center_x':0.5,'center_y':0.15}
        size_hint: (0.5,0.10)
        on_press: root.manager.current = 'help'
        
<Scan>:
    name: 'scan'
    MDFillRoundFlatButton:
        text: 'Play'
        pos_hint: {'center_x':0.8,'center_y':0.1}
        on_press: root.play()
        
    MDFillRoundFlatButton:
        text: 'Back'
        pos_hint: {'center_x':0.2,'center_y':0.1}
        on_press: root.manager.current = 'menu'
    
<Help>:
    name: 'help'
    MDFillRoundFlatButton:
        text: 'Back'
        pos_hint: {'center_x':0.5,'center_y':0.1}
        on_press: root.manager.current = 'menu'


"""


class MenuScreen(Screen):
    pass   
        
class Scan(Screen):
    def play(self):
        self.img=Image()
        screen = Screen()
        screen.add_widget(self.img)
        self.capture = cv2.VideoCapture(0)
        cv2.namedWindow("Detection")
        Clock.schedule_interval(self.update, 1.0/33.0)
        return screen

    def update(self, dt):
        ret, frame = self.capture.read()
        cv2.imshow("Detection", frame)
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img.texture = texture
        
class Help(Screen):
    pass

sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(Scan(name='scan'))
sm.add_widget(Help(name='help'))


class App(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        screen = Builder.load_string(screen_helper)
        return screen
App().run()

