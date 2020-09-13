import time
from numpy import empty
import cv2
import os
import datetime

directory = r'D:\Mou\opencv_Screenshots'

cap = cv2.VideoCapture(0)

tracker = []
bbox = []
paths = []

finishLines = []

thickness = 3

success, img = cap.read()

maxTracker = 2

startPoint = []
endPoint = []

lineArr = []

countLines = 0

os.chdir(directory)
print(os.listdir(directory))

filename = 'tracked Line at ' + str(time.time()) + '.jpg'

def drawLines(img):
    global startPoint
    global endPoint
    global lineArr
    global countLines
    for i in range(0, maxTracker):
        startPoint[i] = endPoint[i]
        endPoint[i] = (int(bbox[i][0] + (bbox[i][2]/2)), int(bbox[i][1] + (bbox[i][3]/2)))
        #print(endPoint[i])
        color = (50*(i), 100*(i+1), 200*(i+2)/4)
        paths[i] = cv2.line(img, startPoint[i], endPoint[i], color, thickness)
        lineArr[i][countLines] = startPoint[i]
        lineArr[i].append(endPoint[i])
    countLines += 1

for i in range(0, maxTracker):
    tracker.append(cv2.TrackerCSRT_create())
    bbox.append(cv2.selectROI("Tracking", img, False))
    tracker[i].init(img, bbox[i])
    paths.append(None)
    startPoint.append((0,0))
    endPoint.append((0,0))
    lineArr.append([None])
    #print(endPoint[i])

drawLines(img)
#tracker = cv2.TrackerMOSSE_create()
#tracker = cv2.TrackerCSRT_create()
#success, img = cap.read()
#bbox = cv2.selectROI("Tracking", img, False)
#tracker.init(img, bbox)

def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x,y), ((x+w),(y+h)), (255, 0, 255), 3, 1)

def drawAllLines(img):
    for i in range(0, maxTracker):
        finishLines.append([None])
        color = (50*(i), 100*(i+1), 200*(i+2)/4)

        for a in range(0, int(countLines-1)):
            finishLines[i].append([None])
            finishLines[i][a] = cv2.line(img, tuple(lineArr[i][a]), tuple(lineArr[i][a+1]), color, thickness)

while True:

    if(cv2.waitKey(1) & 0xff == ord('q')):
        drawAllLines(img)
        cv2.imwrite(filename, img)

    timer = cv2.getTickCount()
    success, img = cap.read()

    for i in range(0, maxTracker):
        success, bbox[i] = tracker[i].update(img)

    #print(bbox)
    if success:
        for i in range(0, maxTracker):
            drawBox(img, bbox[i])
    else:
        for i in range(0, maxTracker):
            cv2.putText(img, "Lost " + str(i), (75, 75), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,0), 2)

    drawLines(img)

    cv2.imshow("Tracking", img)

    if cv2.waitKey(1) & 0xff == ord('e'):
        break