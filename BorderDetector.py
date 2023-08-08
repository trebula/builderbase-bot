from pickle import FALSE
import cv2
import numpy as np
import matplotlib
from matplotlib.pyplot import imshow
from matplotlib import pyplot as plt
# import build.LineComputation as lc
import LineComputation as lc
from AttackStrategy.GiantCannon import GiantCannon
import pyautogui
import platform
import os

img_name = "redbounds/redbounds.PNG"

# read image
img = cv2.imread(img_name)

# trim image
# img = img[0:1000, 1000:1900]

# guassian blur
image = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
blur = cv2.GaussianBlur(image, (5,5), 0, 0)
# cv2.imwrite("redbounds/redbounds_blur3.jpg", image)

lower = np.uint8([10, 0, 0])
upper = np.uint8([35, 255, 255])
red_mask = cv2.inRange(blur, lower, upper)

# edges = cv2.Canny(image,100,200)

rho = 1  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 20  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 10  # minimum number of pixels making up a line
max_line_gap = 5  # maximum gap in pixels between connectable line segments
line_image = np.copy(img) * 0  # creating a blank to draw lines on

# Run Hough on edge detected image
# Output "lines" is an array containing endpoints of detected line segments
lines = cv2.HoughLinesP(red_mask, rho, theta, threshold, np.array([]),
                    min_line_length, max_line_gap)

for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),1)

# Draw the lines on the  image
lines_edges = cv2.addWeighted(blur, 0.8, line_image, 1, 0)

# get builder hall location
SCALES = np.array([100, 50, 63, 75, 87, 112, 125, 137, 150])
builderHallLoc = None
currRes = SCALES[0]
foundBH = False

blank = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

# start at 0.9 confidence and go down until found
conf = 0.9
while builderHallLoc is None:
    for scale in SCALES:
        image_name = "scaled/testcropped" + str(scale) + ".png"
        builderHallLoc = pyautogui.locate(image_name, img, grayscale=False, confidence=conf)

        # found builder hall at new scale
        if builderHallLoc is not None:
            print(builderHallLoc)
            print(scale)
            print(conf)
            # draw rectangle around builder hall on blank
            cv2.rectangle(blank, (builderHallLoc[0], builderHallLoc[1]), (builderHallLoc[0] + builderHallLoc[2], builderHallLoc[1] + builderHallLoc[3]), (0, 255, 0), 2)
            currRes = scale
            break
    
    # if not found, lower confidence
    if builderHallLoc is None:
        conf -= 0.05
        if conf <= 0.1:
            raise Exception("Could not find builder hall")

# convert to pixel location for mac retina screens (2x pixel density)
# if platform.system() == "Darwin":
#     builderHallLoc = tuple(x/2 for x in builderHallLoc)

dropLocations = lc.getFarthestIntersects(lines, builderHallLoc, 22, True)
dropLocations = np.reshape(dropLocations, (int(len(dropLocations)/2), 2))

# draw dot for each drop location
for dropLoc in dropLocations:
    cv2.circle(blank, (int(dropLoc[0]), int(dropLoc[1])), 5, (0,0,255), -1)

# draw different color dot at closest drop location (first one)
cv2.circle(blank, (int(dropLocations[0][0]), int(dropLocations[0][1])), 5, (0,255,0), -1)

# combine lines_edges and blank
final = cv2.addWeighted(lines_edges, 0.8, blank, 1, 0)

cv2.imshow("edges", final)
cv2.waitKey(0) 
cv2.destroyAllWindows() 
