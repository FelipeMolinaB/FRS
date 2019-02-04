# import the necessary packages
from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import Tkinter as tki
import threading
import datetime
import imutils
import cv2
import os
import cv2,dlib
import sys
from renderFace import renderFace
from Tkinter import *
import ttk
from PIL import Image
import tkMessageBox
from time import sleep
import numpy as np
import time
from sklearn.externals import joblib
from multiprocessing import Pool
import shutil
from face_average_2 import face_average_utilities_dos as fa_utl

class PhotoBoothApp:
	def __init__(self):
		# store the video stream object and output path, then initialize
		# the most recently read frame, thread for reading frames, and
		# the thread stop event

		self.b_take_data = False
		self.n_images = 0
		self.name = ""
		self.directory_save_data = ""
		#self.vs = vs
		self.outputPath = "data/"
		self.frame = None
		self.frame_original = None
		self.thread = None
		self.stopEvent = None

		# initialize the root window and image panel
		self.root = tki.Tk()
		self.panel = None
		self.panel_face_average = None
		self.fa_image = False

		self.root.title("Similarity")

		#label1 = Label(self.root, text="First").grid(row=0)
		#label2 = Label(self.root, text="Second").grid(row=1)
		self.entry1 = Entry(self.root)
		entry2 = Entry(self.root)
		enroll_button = tki.Button(self.root, text="Enroll Nombre!", command=self.star_data_capture)

		generate_face_average_button = tki.Button(self.root, text="Generate Face Average!", command=self.get_face_average)
		take_photo_face_average_button = tki.Button(self.root, text="Take photo", command=self.takeSnapshot)
		delete_photos_face_average_button = tki.Button(self.root, text="Delete photos!", command=self.delete_snapshots)

		self.w = tki.Label(self.root, text="")
		#button1 = tki.Button(self.root, text="button1!", command=self.calculate)
		#button2 = tki.Button(self.root, text="button2!", command=self.calculate)
		#e1.grid(row=0, column=1)
		#e2.grid(row=1, column=1)

		#Label(self.root, text="Nombre").grid(sticky=E)
		#Label(self.root, text="Second").grid(sticky=E)

		# for enrollement
		#self.entry1.grid(row=0, column=1)
		#enroll_button.grid(row=0, column=0, sticky=W)

		self.w.grid(row=1, column=0)


		generate_face_average_button.grid(row=4, column=0, sticky=W)
		take_photo_face_average_button.grid(row=5, column=0, sticky=W)
		delete_photos_face_average_button.grid(row=6, column=0, sticky=W)



		#self.panel.grid(row=0, column=2, columnspan=2, rowspan=2, sticky=W + E + N + S, padx=5, pady=5)
		#button1.grid(row=2, column=2)
		#button2.grid(row=2, column=3)



		# create a button, that when pressed, will take the current
		# frame and save it to file
		# btn = tki.Button(self.root, text="Snapshot!",command=self.takeSnapshot)
		# btn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

		# self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
		# self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
		# self.mainframe.columnconfigure(0, weight=1)
		# self.mainframe.rowconfigure(0, weight=1)
        #
		# feet = StringVar()
		# meters = StringVar()
        #
		# feet_entry = ttk.Entry(self.mainframe, width=7, textvariable=feet)
		# feet_entry.grid(column=2, row=1, sticky=(W, E))
        #
		# ttk.Label(self.mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
		# ttk.Button(self.mainframe, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky=W)
        #
		# ttk.Label(self.mainframe, text="feet").grid(column=3, row=1, sticky=W)
		# ttk.Label(self.mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
		# ttk.Label(self.mainframe, text="meters").grid(column=3, row=2, sticky=W)
        #
		# for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
        #
		# feet_entry.focus()
		# #self.root.bind('<Return>', self.calculate)


		# # create labels and text
		# Label(self.root, text="First Name").grid(row=0)
		# Label(self.root, text="Last Name").grid(row=1)
		#
		# e1 = Entry(self.root)
		# e2 = Entry(self.root)
		#
		# e1.grid(row=0, column=1)
		# e2.grid(row=1, column=1)


		# start a thread that constantly pools the video sensor for
		# the most recently read frame
		self.stopEvent = threading.Event()
		self.thread = threading.Thread(target=self.videoLoop, args=())
		self.thread.start()

		# set a callback to handle when the window is closed
		self.root.wm_title("Similarity")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)


	def wrapper_parallel_descriptors(self, args):

		return self.parallel_descriptors(*args)


	def parallel_descriptors(self, array_shapes):
		print ("parallel_descriptors")
		print ("len array_shapes %s" %len(array_shapes))

	def videoLoop(self):

		try:
			print ("pwd: %s" %os.getcwd())

			PREDICTOR_PATH = "models/shape_predictor_68_face_landmarks.dat"
			FACE_RECOGNITION_MODEL_PATH = '/root/openface/demos/web/project/models/dlib_face_recognition_resnet_model_v1.dat'

			RESIZE_HEIGHT = 480
			SKIP_FRAMES = 2

			cap = cv2.VideoCapture(1)

			# Check if OpenCV is able to read feed from camera
			if (cap.isOpened() is False):
				print("Unable to connect to camera")
				sys.exit()

			# Just a place holder. Actual value calculated after 100 frames.
			fps = 30.0

			# Get first frame
			ret, im = cap.read()

			# We will use a fixed height image as input to face detector
			if ret == True:
				height = im.shape[0]
				# calculate resize scale
				RESIZE_SCALE = float(height) / RESIZE_HEIGHT
				size = im.shape[0:2]
			else:
				print("Unable to read frame")
				sys.exit()

			# Load face detection and pose estimation models
			detector = dlib.get_frontal_face_detector()
			predictor = dlib.shape_predictor(PREDICTOR_PATH)
			faceRecognizer = dlib.face_recognition_model_v1(FACE_RECOGNITION_MODEL_PATH)
			# initiate the tickCounter
			t = cv2.getTickCount()
			count = 0

			# Grab and process frames until the main window is closed by the user.
			while (True):#not self.stopEvent.is_set()):

				faceDescriptors = None

				if count == 0:
					t = cv2.getTickCount()
				# Grab a frame
				ret, im = cap.read()
				# create imSmall by resizing image by resize scale
				imSmall = cv2.resize(im, None, fx=1.0 / RESIZE_SCALE, fy=1.0 / RESIZE_SCALE, interpolation=cv2.INTER_LINEAR)

				# Process frames at an interval of SKIP_FRAMES.
				# This value should be set depending on your system hardware
				# and camera fps.
				# To reduce computations, this value should be increased
				if (count % SKIP_FRAMES == 0):
					# Detect faces
					faces = detector(imSmall, 0)

				# Iterate over faces
				#im_original = im
				array_shapes =[]
				for face in faces:
					# Since we ran face detection on a resized image,
					# we will scale up coordinates of face rectangle
					newRect = dlib.rectangle(int(face.left() * RESIZE_SCALE),
											 int(face.top() * RESIZE_SCALE),
											 int(face.right() * RESIZE_SCALE),
											 int(face.bottom() * RESIZE_SCALE))

					# Find face landmarks by providing reactangle for each face
					shape = predictor(im, newRect)

					# Compute face descriptor using neural network defined in Dlib.
					# It is a 128D vector that describes the face in img identified by shape.
					faceDescriptor = faceRecognizer.compute_face_descriptor(im, shape)

					time_faceDescriptor = time.time()
					# print("time_faceDescriptor %s" % (time_faceDescriptor-shape_landmarks))
					# Convert face descriptor from Dlib's format to list, then a NumPy array
					faceDescriptorList = [x for x in faceDescriptor]
					faceDescriptorNdarray = np.asarray(faceDescriptorList, dtype=np.float64)
					faceDescriptorNdarray = faceDescriptorNdarray[np.newaxis, :]

					# Stack face descriptors (1x128) for each face in images, as rows
					if faceDescriptors is None:
						faceDescriptors = faceDescriptorNdarray
					else:
						faceDescriptors = np.concatenate((faceDescriptors, faceDescriptorNdarray), axis=0)

					#print (faceDescriptors[0])
					#print("time faceDescriptors %s" %(time.time() - time_faceDescriptor))

					rootdir = "/root/openface/demos/web/project/general_svm"
					name_file = "svm_training_100.pkl"
					file_path = os.path.join(rootdir, name_file)
					clf = joblib.load(file_path)

					y_pred = clf.predict(faceDescriptors)
					cedula = y_pred[0]

					rootdir = "/root/openface/demos/web/project"
					users_file_path = os.path.join(rootdir, "users.pkl")
					users = joblib.load(users_file_path)

					name = "error"
					for user in users:
						if user[0] == cedula:
							name = user[1]
							break

					texto_label = name

					for i in xrange(0, len(y_pred)):
						rootdir = "/root/openface/demos/web/project/binary_svm_models"
						file_path_2 = os.path.join(rootdir, "binary_svm_" + str(cedula) + ".pkl")
						clf_2 = joblib.load(file_path_2)
						y_pred_2 = clf_2.predict(faceDescriptors)

						if y_pred_2[i] == 1:
							texto_label = name + " oki" + "\n"
						else:
							texto_label = name + " unknown" + "\n"



					self.w = tki.Label(self.root, text=texto_label)
					self.w.grid(row=1, column=0, columnspan=1, rowspan=2, sticky=W + E + N + S, padx=5, pady=5)

					# Draw facial landmarks
					renderFace(im, shape)

				if self.b_take_data == True:
					self.n_images = self.n_images + 1
					cv2.putText(im, "{0:.2f}-n".format(self.n_images), (50, size[0] - 50), cv2.FONT_HERSHEY_COMPLEX, 1.5,(0, 0, 255), 3)
					self.takeSnapshot(self.n_images)
					sleep(0.3)
					if self.n_images >= 15:
						self.n_images = 0
						self.b_take_data = False


				self.frame = im #self.vs.read()
				self.frame = imutils.resize(self.frame, width=400)

				# OpenCV represents images in BGR order; however PIL
				# represents images in RGB order, so we need to swap
				# the channels, then convert to PIL and ImageTk format
				image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
				image = Image.fromarray(image)
				image = ImageTk.PhotoImage(image)

				# if the panel is not None, we need to initialize it
				if self.panel is None:
					self.panel = tki.Label(image=image)
					self.panel.image = image
					#self.panel.pack(side="left", padx=10, pady=10)
					self.panel.grid(row=0, column=2, columnspan=2, rowspan=2, sticky=W + E + N + S, padx=5, pady=5)
				# otherwise, simply update the panel
				else:
					self.panel.configure(image=image)
					self.panel.image = image

				face_average_image = image

				face_average_image = None
				if self.fa_image == False:
					face_average_image = image
				elif self.fa_image == True:

					path_image_face_average = "/root/openface/demos/web/project/data_face_average/face_average_image.jpg"
					# path_face_average = os.path.join(rootdir, "data_face_average")
					# name_file = "face_average_image.jpg"  # face_persona_path.split("/")[-1].split(".")[0]
					# path_image_face_average = os.path.join(path_face_average, name_file)

					try:
						#print("path_image_fake %s" % path_image_face_average)
						face_average_image_aux = cv2.imread(path_image_face_average)

						face_average_image_aux = imutils.resize(face_average_image_aux, width=400)

						# OpenCV represents images in BGR order; however PIL
						# represents images in RGB order, so we need to swap
						# the channels, then convert to PIL and ImageTk format
						face_average_image_aux = cv2.cvtColor(face_average_image_aux, cv2.COLOR_BGR2RGB)
						face_average_image_aux = Image.fromarray(face_average_image_aux)
						face_average_image_aux = ImageTk.PhotoImage(face_average_image_aux)
						face_average_image = face_average_image_aux
					except:
						print ("error in face average")
						self.fa_image == False


				#face_average_image = cv2.cvtColor(face_average_image, cv2.COLOR_BGR2RGB)
					#face_average_image = Image.fromarray(face_average_image)
					#face_average_image = ImageTk.PhotoImage(face_average_image)

				# if the panel is not None, we need to initialize it
				if self.panel_face_average is None:
					self.panel_face_average = tki.Label(image=face_average_image)
					self.panel_face_average.image = face_average_image
					# self.panel_face_average.pack(side="left", padx=10, pady=10)
					self.panel_face_average.grid(row=0, column=4, columnspan=4, rowspan=4, sticky=W + E + N + S, padx=5, pady=5)
				# otherwise, simply update the panel
				else:
					self.panel_face_average.configure(image=face_average_image)
					self.panel_face_average.image = face_average_image

				ret, im_original = cap.read()
				self.frame_original = im_original  # self.vs.read()
				self.frame_original = imutils.resize(self.frame_original, width=400)

				if self.stopEvent.is_set():
					break

			cap.release()
			sys.exit()


		except RuntimeError, e:
		 	print("[INFO] caught a RuntimeError")

	def star_data_capture(self):

		if (self.entry1.get() == ""):
			tkMessageBox.showinfo("ERROR", "Name must not be empty")
		else:
			self.directory_save_data = os.path.sep.join((self.outputPath, self.entry1.get()))
			print (self.directory_save_data )
			if not os.path.exists(self.directory_save_data ):
				os.makedirs(self.directory_save_data )
			self.b_take_data = True

	def takeSnapshot(self):

		i = 0

		ts = datetime.datetime.now()
		print (ts.strftime("%Y-%m-%d_%H-%M-%S"))

		rootdir = "/root/openface/demos/web/project"
		path_svm_model = os.path.join(rootdir, "data_face_average")

		if not os.path.exists(path_svm_model):
			os.makedirs(path_svm_model)

		file_name =  str(ts) + ".jpg"
		file_path = os.path.join(path_svm_model, file_name)
		cv2.imwrite(file_path, self.frame_original.copy())

	def delete_snapshots(self):

		ts = datetime.datetime.now()
		print (ts.strftime("%Y-%m-%d_%H-%M-%S"))

		rootdir = "/root/openface/demos/web/project"
		path_svm_model = os.path.join(rootdir, "data_face_average")

		try:
			shutil.rmtree(path_svm_model)
		except:
			pass

		self.fa_image = False

	def get_face_average(self):

		ts = datetime.datetime.now()
		print(ts.strftime("%Y-%m-%d_%H-%M-%S"))

		rootdir = "/root/openface/demos/web/project"
		path_face_average = os.path.join(rootdir, "data_face_average")

		if not os.path.exists(path_face_average):
			print ("there are not photos for generating face average")
		else:
			print ("generate face average")
			imagePaths = []
			for file in os.listdir(path_face_average):
				if file.endswith(".jpg"):
					path_file = os.path.join(path_face_average, file)
					imagePaths.append(path_file)

			print (imagePaths)
			output = fa_utl.generate_average_face(imagePaths)

			name_file = "face_average_image.jpg"  # face_persona_path.split("/")[-1].split(".")[0]

			path_image_face_average = os.path.join(path_face_average, name_file)

			#print("path_image_fake %s" % path_image_face_average)
			cv2.imwrite(path_image_face_average, output)
			self.fa_image = True

	def calculate(self):
		pass

	def onClose(self):
		# set the stop event, cleanup the camera, and allow the rest of
		# the quit process to continue
		print("[INFO] closing...")
		self.stopEvent.set()
		#self.vs.stop()
		self.root.quit()
