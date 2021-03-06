import numpy as np 
import cv2
import glob
from matplotlib import pyplot as plt 

from imutils.video import FPS

import time

print("[INFO] loading model...")

net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt.txt', 'MobileNetSSD_deploy.caffemodel')

def object_detection(image):

	(h, w) = image.shape[:2]


	blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

	print("[INFO] computing object detections...")
	net.setInput(blob)
	detections = net.forward()

	# print(detections[0,0,0,3:7])

	for i in np.arange(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with the
		# prediction
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the `confidence` is
		# greater than the minimum confidence
		if confidence > .60:
			# extract the index of the class label from the `detections`,
			# then compute the (x, y)-coordinates of the bounding box for
			# the object
			idx = int(detections[0, 0, i, 1])
			if idx==15.0:
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

				# display the prediction
				label = "{}: {:.2f}%".format('Person', confidence * 100)
				print("[INFO] {}".format(label))
				cv2.rectangle(image, (startX, startY), (endX, endY),
					[0,255,0], 2)
				y = startY - 15 if startY - 15 > 15 else startY + 15
				cv2.putText(image, label, (startX, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255,0,0], 2)
	return image






# path='/home/ashish/Desktop/final_pedesitrian_detection/seq02-img-left/*.png'
path='seq03-img-left/*.png'


all_images=np.sort(glob.glob(path))
# # print(all_images)
fps = FPS().start()
for i in all_images:
	image=cv2.imread(i,1)
	image=object_detection(image)
	cv2.imshow('image',image)
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break
		
	fps.update()
	fps.stop()
	font = cv2.FONT_HERSHEY_SIMPLEX
	# cv2.putText(image,"FPS: {:.2f}".format(fps.fps()),(20,50), font, 1,(0,255,0),2,cv2.LINE_AA)

	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))



cv2.destroyAllWindows()




# 	print(i)
# # 	pass








# # load the input image and construct an input blob for the image
# # by resizing to a fixed 300x300 pixels and then normalizing it
# # (note: normalization is done via the authors of the MobileNet SSD
# # implementation)
# image = cv2.imread(args["image"])
# (h, w) = image.shape[:2]
# blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843,
# 	(300, 300), 127.5)

# # pass the blob through the network and obtain the detections and
# # predictions
# print("[INFO] computing object detections...")
# net.setInput(blob)
# detections = net.forward()

# # loop over the detections
# for i in np.arange(0, detections.shape[2]):
# 	# extract the confidence (i.e., probability) associated with the
# 	# prediction
# 	confidence = detections[0, 0, i, 2]
 
# 	# filter out weak detections by ensuring the `confidence` is
# 	# greater than the minimum confidence
# 	if confidence > args["confidence"]:
# 		# extract the index of the class label from the `detections`,
# 		# then compute the (x, y)-coordinates of the bounding box for
# 		# the object
# 		idx = int(detections[0, 0, i, 1])
# 		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
# 		(startX, startY, endX, endY) = box.astype("int")
 
# 		# display the prediction
# 		label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
# 		print("[INFO] {}".format(label))
# 		cv2.rectangle(image, (startX, startY), (endX, endY),
# 			COLORS[idx], 2)
# 		y = startY - 15 if startY - 15 > 15 else startY + 15
# 		cv2.putText(image, label, (startX, y),
# 			cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

# # show the output image
# cv2.imshow("Output", image)
# cv2.waitKey(0)
