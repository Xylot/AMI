# # import Kivy
# import kivy
# import random

# from kivy.app import App
# from kivy.uix.button import Button
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.label import Label
# from kivy.uix.textinput import TextInput

# class MyApp(App):

#     def build(self):
#         layout = BoxLayout(padding=10, orientation='vertical')
#         btn1 = Button(text="OK")
#         btn1.bind(on_press=self.buttonClicked)
#         layout.add_widget(btn1)
#         self.lbl1 = Label(text="test")
#         layout.add_widget(self.lbl1)
#         self.txt1 = TextInput(text='', multiline=False)
#         layout.add_widget(self.txt1)
#         return layout

#     def buttonClicked(self,btn):
#         self.lbl1.text = "You wrote " + self.txt1.text


# if __name__ == "__main__":
#     MyApp().run()

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.accordion import Accordion
from kivy.core.window import Window

import os
import json

Window.size = (800, 480)


kv_text = '''
<CustButton@Button>:
    font_size: 18
    spacing: [10, 10]
    size_hint: [.5, .8]

<CustLabel@Label>:
    font_size: 18
    pos_hint: [None, None]
    color: 1, 0.757, 0.145, 1
    size_hint: [.8,.8]


<CustLabel2@Label>:
    font_size: 18
    pos_hint: [None, None]
    color: 1, 0.757, 0.145, 1
    size_hint: [.8,.8]


<CustTextInput@TextInput>:
    font_size: 18
    write_tab: False    
    size_hint: [.5,.5]

<MyAccordion>:
    orientation: 'horizontal'
    AccordionItem:
        title: "Settings"
        GridLayout:
            padding: [10,10]
            rows: 1
            cols: 0
            
            BoxLayout:
                orientation: 'horizontal'
                padding: [10,10]

                GridLayout:
                    row_force_default: True
                    row_default_height: 50
                    rows: 4
                    cols: 2
                    padding: [30,30]

                    CustLabel:
                        text: "Time Per Recording"

                    CustTextInput:
                        id: recTime

                    CustLabel:
                        text: "Frames Per Second"

                    CustTextInput:
                        id: fps

                    CustLabel:
                        text: "Time Between Images"

                    CustTextInput:
                        id: tbi

                GridLayout:
                    rows: 4
                    cols: 2
                    row_force_default: True
                    row_default_height: 50
                    padding: [30,30]

                    CustLabel:
                        text: "Distance (Horizonatal)"

                    CustTextInput:
                        id: disH

                    CustLabel:
                        text: "Distance (Vertical)"

                    CustTextInput:
                        id: disV

                    CustLabel:
                        text: "Number of Recordings"

                    CustTextInput:
                        id: recNum

                    CustButton:
                        text: "Apply"
                        on_press: root.exportData()

'''
class MyAccordion(Accordion):
    def __init__(self):
        super(MyAccordion, self).__init__()
        self.filename = 'settings.dat'
        self.populateFields(self.filename)

    def exportData(self):
        self.recordingTime = int(self.ids.recTime.text)
        self.framesPerSecond = float(self.ids.fps.text)
        self.timeBetweenImages = int(self.ids.tbi.text)
        self.distanceVertical = int(self.ids.disV.text)
        self.distanceHorizontal = int(self.ids.disH.text)
        self.recordingCount = int(self.ids.recNum.text)

        self.settingsData = {
            'RecordingTime': self.recordingTime,
            'FramesPerSecond': self.framesPerSecond,
            'TimeBetweenImages': self.timeBetweenImages,
            'NumberOfRecordings': self.recordingCount,
            'DistanceVertical': self.distanceVertical,
            'DistanceHorizontal': self.distanceHorizontal
        }
		
        self.outputJSON(self.settingsData, self.filename)

    def outputJSON(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file)

    def readConfig(self, filename):
        with open(filename) as file:
            config = json.load(file)
        return config

    def populateFields(self, filename):
        if os.path.isfile(filename):
            self.currentSettings = self.readConfig(filename)
            self.ids.recTime.text = str(self.currentSettings['RecordingTime'])
            self.ids.fps.text = str(self.currentSettings['FramesPerSecond'])
            self.ids.tbi.text = str(self.currentSettings['TimeBetweenImages'])
            self.ids.recNum.text = str(self.currentSettings['NumberOfRecordings'])
            self.ids.disV.text = str(self.currentSettings['DistanceVertical'])
            self.ids.disH.text = str(self.currentSettings['DistanceHorizontal'])
        
	

class MyApp(App):
    def build(self):
        return MyAccordion()

def main():
    Builder.load_string(kv_text)
    app = MyApp()
    app.run()

if __name__ == '__main__':
    main()