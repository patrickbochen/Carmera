import cv2
import sys

cascade = cv2.CascadeClassifier('haarcascades/haarcascade_upperbody.xml')
img     = cv2.imread('test_images/person_3.jpg')

#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#gray = cv2.equalizeHist(gray)

# # car detection.
cars = cascade.detectMultiScale(img, 1.1, 4)

ncars = 0
for (x,y,w,h) in cars:
    print(x)
    print(y)
    print(w)
    print(h)
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    ncars = ncars + 1

# show result
cv2.imwrite(sys.argv[1], img)

