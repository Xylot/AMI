from kivy.base import runTouchApp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.vector import Vector
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

import json

Window.size = (800, 480)

# Builder.load_string('''
# <CircularButton>
#     background_color: 0.5,.5,.5,.5
#     canvas.before:
#         Color:
#             rgba: self.background_color
#         Ellipse:
#             pos: self.pos
#             size: self.size
#     ''')

Builder.load_string('''
<Node>
    background_color: 1,1,1,1
    canvas:
        Color:
            rgba: self.background_color
        Line:
            rounded_rectangle: (self.x+17, self.y+5, 50, 50, 10)

    ''')

class NodeArray(GridLayout):
	def __init__(self):
		super(NodeArray, self).__init__()
		self.padding = 10
		self.cols = 9
		self.rows = 7
		self.intialChar = 'A'
		self.initialNum = self.rows - 1
		self.nodeList = []
		self.binaryMatrix = [0 for x in range((self.cols - 1) * (self.rows - 1))]
		self.populateGrid()

	def populateGrid(self):
		for x in range(0, self.rows * self.cols):
			if self.checkLastRow(x, self.rows, self.cols):
				if x == (self.rows * self.cols - self.cols):
					self.add_widget(Label(text=''))
				else:
					self.add_widget(Label(text=self.intialChar, font_size = '20sp'))
					self.intialChar = chr(ord(self.intialChar) + 1)
			else:
				if x % 9 == 0:
					if x == (self.rows - 1) * self.cols:
						self.addApplyButton()
					else:
						self.add_widget(Label(text=str(self.initialNum), font_size = '20sp'))
					self.initialNum = self.initialNum - 1
				else:
					self.createNode()

	def createNode(self):
		node = Node()
		self.nodeList.append(node)
		self.add_widget(node)

	def checkLastRow(self, index, rows, cols):
		if index > (rows * cols - cols):
			return True

	def addApplyButton(self):
		self.applyButton = Button(text='Apply')
		self.applyButton.bind(on_press=self.exportNodeConfiguration)
		self.add_widget(self.applyButton)

	def createBinaryMatrix(self):
		for index, node in enumerate(self.nodeList):
			self.binaryMatrix[index] = int(node.activated)

	def createConfigDictionary(self):
		self.configDict = {'rows':self.rows, 'cols':self.cols, 'data':self.binaryMatrix}

	def outputJSON(self):
		with open('nodeInfo.config', 'w') as file:
			json.dump(self.configDict, file)

	def exportNodeConfiguration(self, instance):
		self.createBinaryMatrix()
		self.createConfigDictionary()
		self.outputJSON()


class Node(ButtonBehavior, Label):
	def __init__(self, **kwargs):
		super(Node, self).__init__(**kwargs)
		self.activated = False

	def on_press(self, *args):
		self.activated = not self.activated
		if not self.activated:
			self.background_color = (1, 1, 1, 1)
		else:
			self.background_color = (1, 0, 0, 1)

	def collide_point(self, x, y):
		return Vector(x, y).distance((self.x + 35, self.y + 35)) <= 35

if __name__ == '__main__':
	runTouchApp(NodeArray())