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
from pprint import pprint

import threading
import time
import json

from CameraTools import CameraTools


class Home(FloatLayout):
	
	def __init__(self):
		super(Home, self).__init__()
		# Window.clearcolor = (1, 1, 1, 1)
		Window.size = (800, 480)
		#Window.borderless = True
		self.size = Window.size
		self.deviceArray = Widget(size=(100,100))
		self.add_widget(self.deviceArray)

		self.testNodeArray = [1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,0,0,0,1,0,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,0,1,1,1,1,1,0,0,1,0,1]
		self.fillQueue((8,6))
		self.setParameters()

		self.timeRemaining = 10
		self.startTime = time.time()
		self.started = False
		self.currentStatus = "Idle"

		self.addProgressbar()

		self.setNodeProperties()
		self.populateNodes(self.nodeSize)

		self.addCameraViewButton()
		self.addNodeIncrementButton()
		self.addSettingsButton()
		self.addStopButton()

		self.addStatusLabel()
		self.addTimeLeftLabel()
		self.addCameraPositionLabel()
		self.addTimeLeftValueLabel()
		self.addCurrentStatusLabel()

		self.cameraTools = CameraTools()

	def updateTimeRemaining(self, *args):
		if self.started:
			if self.webcamThread.isAlive():
				self.currentStatus = "Recording"
				self.timeLeftValueLabel.text = str(10-int(time.time() - self.startTime))
			else:
				self.currentStatus = "Idle"
				self.timeLeftValueLabel.text = str(10)

		if self.currentStatus == "Idle" and self.currentStatusLabel.text == "Recording":
			self.changeActiveNode3()

		if self.oldWidth is not Window.size[0]:
			self.deviceArray.canvas.clear()
			self.populateNodes(self.nodeSize)

		self.currentStatusLabel.text = self.currentStatus

	def createNode(self, xpos, ypos):
		return Line(rounded_rectangle=(xpos, ypos, Window.size[0] / 4 - 10, Window.size[1] / 2, 10))

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
					self.oldWidth = Window.size[0]
					self.deviceArrayList.append(self.createNode(colNum * (Window.size[0] / 4) + 5, Window.size[1] / 2 - 10))
		self.addNodeLabels()
	
	def fillQueue(self, size):
		self.posArray = []
		posRowArray = []
		initChar = 'A'
		#initChar = chr(ord('A') + size[0])
		for rowNum in range(1, size[0] + 1):
			for colNum in range(1, size[0] + 1):
				posRowArray.append(str(chr(ord(initChar)) + str(rowNum)))
				initChar = chr(ord(initChar) + 1)
			self.posArray.append(posRowArray)
			posRowArray = []
			initChar = 'A'

		self.flatPosArray = [item for sublist in self.posArray for item in sublist]
		self.nodesStatusArray = list(zip(self.flatPosArray, self.testNodeArray))
		self.nodeQueue = []
		for node in self.nodesStatusArray:
			if node[1] == 1:
				self.nodeQueue.append(node[0])
		self.recordedNodes = []
		print(self.nodeQueue)

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

	def changeActiveNode3(self):
		self.recordedNodes.append(self.nodeQueue.pop(0))
		for label in self.activeNodeLabels:
			label.canvas.clear()
		self.populateNodes(self.nodeSize)
		
	def showWebcamFeed(self, instance):
		self.started = True
		self.startTime = time.time()
		self.webcamThread = WebcamThread(1, self.nodeQueue[0], self.cameraTools, self.recordingTime, self.numberOfRecordings, self.framesPerSecond, self.timeBetweenImages)		
		self.webcamThread.start()

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
		#self.add_widget(self.recordingProgressBar)
		self.currentProgress = 0
		self.recordingProgressBar.value = self.currentProgress

	def addCameraViewButton(self):
		self.cameraViewButton = Button(text='Camera View', pos_hint={'x':.85, 'y':.25}, size_hint = (.125,.2))
		#self.cameraViewButton = Button(text='Camera View', pos=(670, Window.size[1] - 330), size_hint = (.125,.20833))
		self.cameraViewButton.bind(on_press=self.showWebcamFeed)
		self.add_widget(self.cameraViewButton)

	def addNodeIncrementButton(self):
		self.nodeIncrement = Button(text='Increment', pos_hint={'x':.85, 'y':.01}, size_hint = (.125,.2))
		#self.nodeIncrement = Button(text='Increment', pos=(670, Window.size[1] - 440), size_hint = (.125,.20833))
		self.nodeIncrement.bind(on_press=self.changeActiveNode)
		self.add_widget(self.nodeIncrement)

	def addSettingsButton(self):
		self.settingsButton = Button(text='Settings', pos_hint={'x':.7, 'y':.25}, size_hint = (.125,.2))
		#self.settingsButton = Button(text='Settings', pos=(560, Window.size[1] - 330), size_hint = (.125,.20833))
		self.settingsButton.bind(on_press=self.changeActiveNode)
		self.add_widget(self.settingsButton)

	def addStopButton(self):
		self.stopButton = Button(text='STOP', pos_hint={'x':.7, 'y':.01}, size_hint = (.125,.2))
		#self.stopButton = Button(text='STOP', pos=(560, Window.size[1] - 440), size_hint = (.125,.20833))
		self.stopButton.background_color = (255,0,0,0.6)
		self.stopButton.bind(on_press=self.changeActiveNode)
		self.add_widget(self.stopButton)

	def addStatusLabel(self):
		self.statusLabel = Label(text='Current status:')
		self.statusLabel.font_size = '20sp'
		#self.statusLabel.pos = (-310, -20)
		self.statusLabel.pos_hint = {'x':-.38, 'y':-.2}
		#self.statusLabel.texture_update()
		#self.statusLabel.size_hint = {'x':-.38, 'y':-.15}
		self.add_widget(self.statusLabel)

	def addTimeLeftLabel(self):
		self.timeLeftLabel = Label(text='Time left in recording:')
		self.timeLeftLabel.font_size = '20sp'
		# self.timeLeftLabel.pos = (-271, -90)
		self.timeLeftLabel.pos_hint = {'x':-.335, 'y':-.3}
		self.add_widget(self.timeLeftLabel)

	def addCameraPositionLabel(self):
		self.cameraPositionLabel = Label(text='Camera position (X,Y):')
		self.cameraPositionLabel.font_size = '20sp'
		#self.cameraPositionLabel.pos = (-267, -160)
		self.cameraPositionLabel.pos_hint = {'x':-.335, 'y':-.4}
		self.add_widget(self.cameraPositionLabel)

	def addTimeLeftValueLabel(self):
		self.timeLeftValueLabel = Label(text=str(10-int(time.time() - self.startTime)))
		self.timeLeftValueLabel.font_size = '20sp'
		self.timeLeftValueLabel.pos_hint = {'x':-.1, 'y':-.3}
		#self.timeLeftValueLabel.pos = (-120, -90)
		self.add_widget(self.timeLeftValueLabel)

	def addCurrentStatusLabel(self):
		self.currentStatusLabel = Label(text=self.currentStatus)
		self.currentStatusLabel.font_size = '20sp'
		#self.currentStatusLabel.pos = (-100, -20)
		self.currentStatusLabel.pos_hint = {'x':-.1, 'y':-.2}
		self.add_widget(self.currentStatusLabel)

	def addNodeLabels(self):
		self.activeNodeLabels = []
		for x in range(0,4):
			self.nodeLabel = Label(text = self.nodeQueue[3 - x])
			self.nodeLabel.font_size = '25sp'
			self.nodeLabel.pos_hint = {'x': .375 - x * .25, 'y':.23}
			self.add_widget(self.nodeLabel)
			self.activeNodeLabels.append(self.nodeLabel)

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
			self.changeActiveNode3()
			#print("Device {}: {}".format(num, node))

	def importSettings(self, filename):
		with open(filename) as file:
			config = json.load(file)
		return config

	def setParameters(self):
		self.settingsFilename = 'settings.dat'
		self.nodeActivityFilename = 'nodestatus.dat'
		self.currentSettings = self.importSettings(self.settingsFilename)
		self.recordingTime = self.currentSettings['RecordingTime']
		self.framesPerSecond = self.currentSettings['FramesPerSecond']
		self.timeBetweenImages = self.currentSettings['TimeBetweenImages']
		self.numberOfRecordings = self.currentSettings['NumberOfRecordings']
		self.distanceVertical = self.currentSettings['DistanceVertical']
		self.distanceHorizontal = self.currentSettings['DistanceHorizontal']


class StatusInterface(App):
	def build(self):
		homeScreen = Home()
		Clock.schedule_interval(homeScreen.updateTimeRemaining, 1)
		return homeScreen

class WebcamThread(threading.Thread):
   
   def __init__(self, threadID, location, func, recordingTime, numberOfRecordings, fps, imageInterval):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.location = location
      self.name = 'node ' + str(location)
      self.cameraTools = func
      self.numberOfRecordings = numberOfRecordings
      self.recordingTime = recordingTime
      self.fps = fps
      self.imageInterval = imageInterval
   
   def run(self):
      print ("Starting " + self.location)
      self.cameraTools.recordNode(self.location, self.numberOfRecordings, self.recordingTime, self.imageInterval, self.fps)
      print ("Exiting " + self.location)


if __name__ == '__main__':
     StatusInterface().run()