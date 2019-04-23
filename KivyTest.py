from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.core.window import Window
from kivy.uix.progressbar import ProgressBar
from kivy.uix.checkbox import CheckBox
from kivy.config import Config

import threading
import time

from CameraTools import CameraTools


class Home(FloatLayout):
	
	def __init__(self):
		super(Home, self).__init__()
		# Window.clearcolor = (1, 1, 1, 1)
		Window.size = (800, 480)
		self.size = Window.size
		self.deviceArray = Widget(size=(100,100))
		self.add_widget(self.deviceArray)

		self.addProgressbar()

		self.setNodeProperties()
		self.populateNodes(self.nodeSize)

		self.addCameraViewButton()
		self.addNodeIncrementButton()
		self.addSettingsButton()
		self.addStopButton()

		self.checkbox = CheckBox(pos=(400, Window.size[1] - 300), size=(100,100), size_hint = (.1,.1))
		#self.checkbox.bind(active=self.showWebcamFeed)
		#self.add_widget(self.checkbox)

		self.addStatusLabel()
		self.addTimeLeftLabel()
		self.addCameraPositionLabel()

		#self.recordNodes()

	def createNode(self, xpos, ypos):
		return Line(rounded_rectangle=(xpos, ypos, 100, 100, 10))
		#return Rectangle(pos=(xpos, ypos))

	def populateNodes(self, size):
		with self.deviceArray.canvas:
			for rowNum in range(0,size[0]):
				for colNum in range(0, size[1]):
					currentNode = rowNum * size[1] + colNum
					if currentNode == self.activeNode:
						Color(1,0,0,1)
						self.recordingProgressBar.value = (currentNode / self.nodeCount) * 1000
					else:
						Color(1,1,1,1)
					self.deviceArrayList.append(self.createNode(colNum * 100 + colNum * 10 + 10, Window.size[1] - (rowNum + 1) * 110))
	
	def changeActiveNode(self, instance):
		self.activeNode = self.activeNode + 1
		if self.activeNode >= self.nodeCount:
			self.activeNode = 0
		self.populateNodes(self.nodeSize)

	def changeActiveNode2(self):
		self.activeNode = self.activeNode + 1
		if self.activeNode >= self.nodeCount:
			self.activeNode = 0
		self.populateNodes(self.nodeSize)
		
	def showWebcamFeed(self, instance):
		webcamThread = WebcamThread(1, "CameraThread")
		webcamThread.start()
		#WebcamTest2.show_webcam()

	def showWebcamFeed2(self, instance):
		webcamThread = WebcamThread(1, "CameraThread")
		webcamThread.start()
		#WebcamTest2.show_webcam()

	def setNodeProperties(self):
		self.nodeSize = (2, 7)
		self.activeNode = 0
		self.nodeCount = self.getNodeCount()
		self.deviceArrayList = []

	def getNodeCount(self):
		return self.nodeSize[0] * self.nodeSize[1]

	def addProgressbar(self):
		self.recordingProgressBar = ProgressBar(max=1000, pos=(0, -220), width=100, height=400)
		self.add_widget(self.recordingProgressBar)
		self.currentProgress = 0
		self.recordingProgressBar.value = self.currentProgress

	def addCameraViewButton(self):
		self.cameraViewButton = Button(text='Camera View', pos=(670, Window.size[1] - 330), size_hint = (.125,.20833))
		self.cameraViewButton.bind(on_press=self.showWebcamFeed)
		self.add_widget(self.cameraViewButton)

	def addNodeIncrementButton(self):
		self.nodeIncrement = Button(text='Increment', pos=(670, Window.size[1] - 440), size_hint = (.125,.20833))
		self.nodeIncrement.bind(on_press=self.changeActiveNode)
		self.add_widget(self.nodeIncrement)

	def addSettingsButton(self):
		self.settingsButton = Button(text='Settings', pos=(560, Window.size[1] - 330), size_hint = (.125,.20833))
		self.settingsButton.bind(on_press=self.changeActiveNode)
		self.add_widget(self.settingsButton)

	def addStopButton(self):
		self.stopButton = Button(text='STOP', pos=(560, Window.size[1] - 440), size_hint = (.125,.20833))
		self.stopButton.background_color = (255,0,0,0.6)
		self.stopButton.bind(on_press=self.changeActiveNode)
		self.add_widget(self.stopButton)

	def addStatusLabel(self):
		self.statusLabel = Label(text='Current status:')
		self.statusLabel.font_size = '25sp'
		self.statusLabel.pos = (-310, -20)
		self.add_widget(self.statusLabel)

	def addTimeLeftLabel(self):
		self.timeLeftLabel = Label(text='Time left in recording:')
		self.timeLeftLabel.font_size = '25sp'
		self.timeLeftLabel.pos = (-271, -60)
		self.add_widget(self.timeLeftLabel)

	def addCameraPositionLabel(self):
		self.cameraPositionLabel = Label(text='Camera position (X,Y):')
		self.cameraPositionLabel.font_size = '25sp'
		self.cameraPositionLabel.pos = (-267, -100)
		self.add_widget(self.cameraPositionLabel)

	def recordNodes(self):
		for num, node in enumerate(self.deviceArrayList, start=1):
			# if num > self.nodeCount:
			# 	break
			if num > 3:
				break
			webcamThread = WebcamThread(num, num)
			webcamThread.start()
			#webcamThread.join()
			while webcamThread.isAlive():
				pass
			self.changeActiveNode2()
			#print("Device {}: {}".format(num, node))


class StatusInterface(App):
    def build(self):
        return Home()

class WebcamThread(threading.Thread):
   
   def __init__(self, threadID, location):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.location = location
      self.name = 'node ' + str(location)
      self.cameraTools = CameraTools()
   
   def run(self):
      print ("Starting " + self.name)
      # self.cameraTools.initializeCamera(4)
      # self.cameraTools.record(10)
      # self.cameraTools.view()
      self.cameraTools.recordNode(self.location, 1, 3)
      print ("Exiting " + self.name)


if __name__ == '__main__':
     StatusInterface().run()