from kivy.base import runTouchApp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.vector import Vector
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

Window.size = (800, 220)

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
            rounded_rectangle: (self.x+7, self.y+5, 100, 100, 10)

    ''')

class NodeArray(GridLayout):
	def __init__(self):
		super(NodeArray, self).__init__()
		# self.padding = 10
		self.cols = 7
		self.rows = 2
		for x in range(0,14):
			self.add_widget(Node())

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
		#return Widget(pos=(self.x, self.y), size=(self.width, self.height)).collide_point(x, y)
		#print(Vector(x, y).distance((self.x+50, self.y+50)))
		return Vector(x, y).distance((self.x+50, self.y+50)) <= 50

if __name__ == '__main__':
	runTouchApp(NodeArray())