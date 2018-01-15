# Python program to illustrate HoughLine
# method for line detection
import cv2
import numpy as np
import sys

if len(sys.argv) < 3:
    print "Needs 2 arguments"
    exit()

# Reading the required image in
# which operations are to be done.
# Make sure that the image is in the same
# directory in which this python program is
img = cv2.imread(sys.argv[1])

blur = cv2.blur(img,(9,9))

# Convert the img to grayscale
gray = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)

# Apply edge detection method on the image
edges = cv2.Canny(gray,50,150,apertureSize = 3)

# This returns an array of r and theta values
lines = cv2.HoughLines(edges,1,np.pi/180, int(sys.argv[2]))
#  for p in lines: print p
#  print lines

# The below for loop runs till r and theta values
# are in the range of the 2d array
for thisline in lines:
    for r,theta in thisline:
        #  for r,theta in lines[0]:

        # Stores the value of cos(theta) in a
        a = np.cos(theta)

        # Stores the value of sin(theta) in b
        b = np.sin(theta)

        # x0 stores the value rcos(theta)
        x0 = a*r

        # y0 stores the value rsin(theta)
        y0 = b*r

        # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
        x1 = int(x0 + 1000*(-b))

        # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
        y1 = int(y0 + 1000*(a))

        # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
        x2 = int(x0 - 1000*(-b))

        # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
        y2 = int(y0 - 1000*(a))

        # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
        # (0,0,255) denotes the colour of the line to be
        #drawn. In this case, it is red.
        cv2.line(img,(x1,y1), (x2,y2), (0,0,255),2)

# All the changes made in the input image are finally
# written on a new image houghlines.jpg
cv2.imwrite('withlines.jpg', img)
