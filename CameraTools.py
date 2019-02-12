import cv2
import os
import time
import datetime
import numpy as np


class CameraTools:

	def __init__(self):
		self.recordingCount = 5
		self.createFolder()
		for i in range(1,10):
			self.initializeCamera(i)
			self.record(10)
			self.endRecording()
			time.sleep(3)
		

	def initializeCamera(self, num):
		self.cap = cv2.VideoCapture(0)
		self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
		self.out = cv2.VideoWriter(self.directoryPath + '/output ' + str(num) + '.avi',self.fourcc, 20.0, (640,480))

	def record(self, duration):
		startTime = time.time()

		while(int(time.time() - startTime) < duration):
		    ret, frame = self.cap.read()
		    if ret==True:

		        self.out.write(frame)

		        cv2.imshow('frame',frame)
		        # if cv2.waitKey(1) & 0xFF == ord('q'):
		        #     break
		    else:
		        break

	def endRecording(self):
		self.cap.release()
		self.out.release()
		cv2.destroyAllWindows()

	def createFolder(self):
		self.directoryPath = './Recordings/' + str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
		try:
			if not os.path.exists(self.directoryPath):
				os.makedirs(self.directoryPath)
		except OSError:
			print ('Error: Creating directory. ' +  self.directoryPath)

test = CameraTools()