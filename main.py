from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
import clr
from kivy.uix.textinput import TextInput
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import time
from kivy.properties import NumericProperty

'''Add Dll Data using pythonnet bibliothek'''

clr.AddReference("Dll/B24Lib")
from B24Lib import BGLib

print(dir(BGLib))

MyDll = BGLib()


class HomeScreen(Screen):
    pass


class ImageButton(ButtonBehavior, Image):
    pass


class Txt(TextInput):
    pass


class BluetoothScreen(Screen):
    def attach(self):
        ports2 = MyDll.Attach('COM7')
        print(ports2)
        print('Is Attached: ', MyDll.IsAttached)

    def connect(self):
        connect2 = MyDll.Connect("84AB")
        print('Is Connected: ', connect2)

        pass


class GraphScreen(Screen):

    def on_enter(self):
        x = []
        y = []
        for i in range(1, 15):
            data = MyDll.DataValue
            time.sleep(1)
            x.append(i)
            y.append(data)
        print(x)
        print(y)

        plt.plot(x, y)
        plt.ylabel("Y axis")
        plt.xlabel("X axis")

        graph_widget = self.ids.graph_widget
        graph_widget.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def save_graph(self):
        plt.show()
        plt.savefig("plot.pdf")


class DataRate(Screen):

    def data_rate(self):
        txt_dr = self.ids.input_dr
        input_text = txt_dr.text
        try:
            txt_dr_value = int(input_text)
            MyDll.DataRate = txt_dr_value
            print(MyDll.DataRate)

        except ValueError:
            print("just number ")

    pass


class Btry(Screen):

    def bt_th(self):
        txt = self.ids.input
        text_input1 = txt.text
        try:
            MyDll.BatteryThreshold = float(text_input1)
            print(MyDll.BatteryThreshold)
        except ValueError:
            print(" gib float number ")


GUI = Builder.load_file("main.kv")


class MainApp(App):
    def build(self):
        return GUI

    def change_screen(self, screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name


MainApp().run()
