import cv2
import os
import time
import datetime
import numpy as np

class CameraTools:

	def __init__(self):
		self.displayCameraView = True
		self.complete = False
		self.createFolder('Node 1')

	def initializeCamera(self, num):
		self.cap = cv2.VideoCapture(0)
		self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
		self.out = cv2.VideoWriter(self.directoryPath + '/output ' + str(num) + '.avi', self.fourcc, 20.0, (640,480))

	def record(self, duration):
		startTime = time.time()
		pDelta = 0

		while(int(time.time() - startTime) < duration):
			self.recordingProgress = (int(time.time() - startTime) / duration) * 100
			ret, frame = self.cap.read()

			delta = int(time.time() - startTime)

			if delta > pDelta:
				print(delta)

			if ret == True:
				self.out.write(frame)

				if self.displayCameraView:
					cv2.imshow('framewow',frame)

				if cv2.waitKey(1) & 0xFF == ord('q'):
					self.endRecording()
					break
			else:
				break

			pDelta = delta

	def view(self):
		self.cap = cv2.VideoCapture(0)
		while True:
			ret, frame = self.cap.read()
			if ret == True:
				cv2.imshow('framewow',frame)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					self.endRecording()
					break

	def endRecording(self):
		self.cap.release()
		self.out.release()
		cv2.destroyAllWindows()
		self.complete = True

	def recordNode(self, location, count, duration):
		for i in range(count):
			self.nodeProgress = (i + 1) / count
			self.initializeCamera(i + 1)
			self.record(duration)
			self.endRecording()
		pass

	def createFolder(self, location):
		self.directoryPath = './Recordings/' + location + '/' + str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
		try:
			if not os.path.exists(self.directoryPath):
				os.makedirs(self.directoryPath)
		except OSError:
			print ('Error: Creating directory. ' +  self.directoryPath)

# test = CameraTools()
# test.view()

#wtfTest()