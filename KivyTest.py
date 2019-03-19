from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.core.window import Window
from kivy.uix.progressbar import ProgressBar
from kivy.config import Config

class Home(FloatLayout):
	def __init__(self):
		super(Home, self).__init__()
		# Window.clearcolor = (1, 1, 1, 1)
		Window.size = (780, 600)
		self.size = Window.size
		self.deviceArray = Widget(size=(100,100))
		self.add_widget(self.deviceArray)

		self.setNodeProperties()


		self.recordingProgressBar = ProgressBar(max=1000, pos=(0, -250), width=100, height=400)
		self.add_widget(self.recordingProgressBar)
		self.currentProgress = 0
		self.recordingProgressBar.value = self.currentProgress

		self.populateNodes(self.nodeSize)
		
		self.cameraViewButton = Button(text='Camera View', pos=(567, Window.size[1] - 475), size_hint = (.268,.4))
		self.cameraViewButton.bind(on_press=self.changeActiveNode)
		self.add_widget(self.cameraViewButton)

	def createNode(self, xpos, ypos):
		return Rectangle(pos=(xpos, ypos))

	def populateNodes(self, size):
		with self.deviceArray.canvas:
			for rowNum in range(0,size[0]):
				for colNum in range(0, size[1]):
					currentNode = rowNum * size[1] + colNum
					self.recordingProgressBar.value = (currentNode / self.nodeCount) * 1000
					if currentNode == self.activeNode:
						Color(1,0,0,1)
					else:
						Color(1,1,1,1)
					self.deviceArrayList.append(self.createNode(colNum * 100 + colNum * 10 + 10, Window.size[1] - (rowNum + 1) * 110))
	
	def changeActiveNode(self, instance):
		self.activeNode = self.activeNode + 1
		if self.activeNode >= self.nodeCount:
			self.activeNode = 0
		self.populateNodes(self.nodeSize)

	def setNodeProperties(self):
		self.nodeSize = (2, 7)
		self.activeNode = 0
		self.nodeCount = self.getNodeCount()
		self.deviceArrayList = []

	def getNodeCount(self):
		return self.nodeSize[0] * self.nodeSize[1]


class StatusInterface(App):
    def build(self):
        return Home()


if __name__ == '__main__':
     StatusInterface().run()