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
from kivy.properties import StringProperty
from kivy.clock import Clock

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

		self.timeRemaining = 10
		self.startTime = time.time()
		self.started = False
		self.currentStatus = "Idle"
		#self.timeLeftValueLabel.text = str(10-(time.time() - self.startTime))

		self.addProgressbar()

		self.setNodeProperties()
		self.populateNodes(self.nodeSize)

		self.addCameraViewButton()
		self.addNodeIncrementButton()
		self.addSettingsButton()
		self.addStopButton()

		#self.checkbox = CheckBox(pos=(400, Window.size[1] - 300), size=(100,100), size_hint = (.1,.1))
		#self.checkbox.bind(active=self.showWebcamFeed)
		#self.add_widget(self.checkbox)

		self.addStatusLabel()
		self.addTimeLeftLabel()
		self.addCameraPositionLabel()
		self.addTimeLeftValueLabel()
		self.addCurrentStatusLabel()
		self.addNodeLabels()

		self.cameraTools = CameraTools()
		#self.recordNodes()

	def updateTimeRemaining(self, *args):
		if self.started:
			if self.webcamThread.isAlive():
				self.currentStatus = "Recording"
				self.timeLeftValueLabel.text = str(10-int(time.time() - self.startTime))
			else:
				self.currentStatus = "Idle"
				self.timeLeftValueLabel.text = str(10)

		if self.currentStatus == "Idle" and self.currentStatusLabel.text == "Recording":
			self.changeActiveNode2()

		self.currentStatusLabel.text = self.currentStatus

	def createNode(self, xpos, ypos):
		return Line(rounded_rectangle=(xpos, ypos, 190, 210, 10))

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
					self.deviceArrayList.append(self.createNode(colNum * 198 + 10, Window.size[1] - 220))
	
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
		self.started = True
		self.startTime = time.time()
		self.webcamThread = WebcamThread(1, "CameraThread", self.cameraTools)		
		#self.timeLeftValueLabel.text = str(10-(time.time() - self.startTime))
		self.webcamThread.start()
		#WebcamTest2.show_webcam()

	def showWebcamFeed2(self, instance):
		webcamThread = WebcamThread(1, "CameraThread")
		webcamThread.start()
		#WebcamTest2.show_webcam()

	def setNodeProperties(self):
		self.nodeSize = (1, 4)
		self.activeNode = 0
		self.nodeCount = self.getNodeCount()
		self.deviceArrayList = []
		self.recordTime = 10
		self.recordCount = 1
		self.fps = 10.0

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
		self.timeLeftLabel.pos = (-271, -90)
		self.add_widget(self.timeLeftLabel)

	def addCameraPositionLabel(self):
		self.cameraPositionLabel = Label(text='Camera position (X,Y):')
		self.cameraPositionLabel.font_size = '25sp'
		self.cameraPositionLabel.pos = (-267, -160)
		self.add_widget(self.cameraPositionLabel)

	def addTimeLeftValueLabel(self):
		self.timeLeftValueLabel = Label(text=str(10-int(time.time() - self.startTime)))
		self.timeLeftValueLabel.font_size = '25sp'
		self.timeLeftValueLabel.pos = (-120, -90)
		self.add_widget(self.timeLeftValueLabel)

	def addCurrentStatusLabel(self):
		self.currentStatusLabel = Label(text=self.currentStatus)
		self.currentStatusLabel.font_size = '25sp'
		self.currentStatusLabel.pos = (-100, -20)
		self.add_widget(self.currentStatusLabel)

	def addNodeLabels(self):
		self.nodeLabel = Label(text='A1')
		self.nodeLabel.font_size = '25sp'
		#print(self.deviceArrayList[0].width)
		self.nodeLabel.pos = (-295, 125)
		self.add_widget(self.nodeLabel)
		self.nodeLabel = Label(text='A2')
		self.nodeLabel.font_size = '25sp'
		#print(self.deviceArrayList[0].width)
		self.nodeLabel.pos = (-95, 125)
		self.add_widget(self.nodeLabel)
		self.nodeLabel = Label(text='A3')
		self.nodeLabel.font_size = '25sp'
		#print(self.deviceArrayList[0].width)
		self.nodeLabel.pos = (105, 125)
		self.add_widget(self.nodeLabel)
		self.nodeLabel = Label(text='A4')
		self.nodeLabel.font_size = '25sp'
		#print(self.deviceArrayList[0].width)
		self.nodeLabel.pos = (305, 125)
		self.add_widget(self.nodeLabel)

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
		homeScreen = Home()
		Clock.schedule_interval(homeScreen.updateTimeRemaining, 1)
		return homeScreen

class WebcamThread(threading.Thread):
   
   def __init__(self, threadID, location, func):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.location = location
      self.name = 'node ' + str(location)
      self.cameraTools = func
   
   def run(self):
      print ("Starting " + self.name)
      # self.cameraTools.initializeCamera(4)
      # self.cameraTools.record(10)
      # self.cameraTools.view()
      self.cameraTools.recordNode(self.location, 1, 10)
      print ("Exiting " + self.name)


if __name__ == '__main__':
     StatusInterface().run()