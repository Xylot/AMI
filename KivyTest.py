from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.core.window import Window

class myLayout(FloatLayout):
	def __init__(self):
		super(myLayout, self).__init__()
		# Window.clearcolor = (1, 1, 1, 1)
		self.size = Window.size
		self.deviceArray = Widget(size=(100,100))
		self.add_widget(self.deviceArray)

		self.deviceArrayList = []

		self.activeNode = 2

		self.populateNodes(2, 7)

		# with self.deviceArray.canvas:
		# 	for x in range(0,7):
		# 		if x == self.activeNode:
		# 			Color(1,0,0,1)
		# 		else:
		# 			Color(1,1,1,1)
		# 		self.deviceArrayList.append(self.createNode(x * 100 + x * 10 + 18, Window.size[1] - 110))
		# 		self.deviceArrayList.append(self.createNode(x * 100 + x * 10 + 18, Window.size[1] - 220))
		
		self.cameraViewButton = Button(text='My first button', pos=(300, 300), size_hint = (.1,.1))
		self.add_widget(self.cameraViewButton)

	def createNode(self, xpos, ypos):
		return Rectangle(pos=(xpos, ypos))

	def populateNodes(self, rows, cols):
		with self.deviceArray.canvas:
			for rowNum in range(0,rows):
				for colNum in range(0, cols):
					currentNode = rowNum * cols + colNum
					if currentNode == self.activeNode:
						Color(1,0,0,1)
					else:
						Color(1,1,1,1)
					self.deviceArrayList.append(self.createNode(colNum * 100 + colNum * 10 + 18, Window.size[1] - (rowNum + 1) * 110))



class MyApp(App):
    def build(self):
        return myLayout()


if __name__ == '__main__':
     MyApp().run()