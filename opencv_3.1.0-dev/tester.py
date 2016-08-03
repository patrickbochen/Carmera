import numpy as np
import cv2
import sys

print(cv2.__version__)

sys.exit(0)

if len(sys.argv) < 2:
    print("Save image to command argument not found!")
    print("Usage: python tester.py \"./image_output_name.jpg\"")
    sys.exit(0)

#cascade = cv2.CascadeClassifier('tmp/229109/data/cascade.xml')
#img     = cv2.imread('tmp/229109/pos/1441206908.218000.dr5rsgtqyjnw.24.0.jpg')

# cascade = cv2.CascadeClassifier('hogcascades/hogcascade_pedestrians.xml')
# img     = cv2.imread('test_images/person_3.jpg')

cascade = cv2.CascadeClassifier('haarcascades/haarcascade_upperbody.xml')
img     = cv2.imread('test_images/side_car01.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.equalizeHist(gray)

scaleFactor  = 1.3
minNeighbors = 2
minSize      = (80, 200)
maxSize      = (400, 340)
nRange       = range(2,10)

def detect(img, cascade):
    for scale in [float(i)/10 for i in range(11, 15)]:
        for neighbors in nRange:
            rects = cascade.detectMultiScale(gray, scaleFactor=scale, minNeighbors=neighbors,
                                             minSize=minSize, maxSize=maxSize, flags=cv2.CASCADE_SCALE_IMAGE)

            print('scale: %s, neighbors: %s, len rects: %d' % (scale, neighbors, len(rects)))

detect(gray, cascade)

stops = cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors,
                                 minSize=minSize, maxSize=maxSize, flags=cv2.CASCADE_SCALE_IMAGE)
for (x,y,w,h) in stops:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

cv2.imwrite(sys.argv[1], img)
