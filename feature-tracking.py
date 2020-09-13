import time
import copy
import cv2
import os
import datetime

directory = r'D:\Mou\opencv_Screenshots'

cap = cv2.VideoCapture(0)

tracker = []
bbox = []
paths = []

finishLines = []

thickness = 1

standardThickness = 2

success, img = cap.read()
cache = copy.deepcopy(img)

maxTracker = 1

startPoint = []
endPoint = []

lineArr = []

countLines = 0

filename = ''

os.chdir(directory)

def initVars(i):
    paths.append(None)
    startPoint.append((0,0))
    endPoint.append((0,0))
    lineArr.append([None])

def drawLines(img):
    global thickness
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
    if thickness != standardThickness:
        thickness = standardThickness

for i in range(0, maxTracker):
    tracker.append(cv2.TrackerCSRT_create())
    bbox.append(cv2.selectROI("Tracking", img, False))
    tracker[i].init(img, bbox[i])
    initVars(i)

drawLines(img)

def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x,y), ((x+w),(y+h)), (255, 0, 255), 3, 1)

def drawAllLines(img):
    global cache
    cache = copy.deepcopy(img)
    global filename
    filename = 'tracked Line at ' + str(time.time()) + '.jpg'
    print(filename)
    for i in range(0, maxTracker):
        finishLines.append([None])
        color = (50*(i), 100*(i+1), 200*(i+2)/4)

        for a in range(0, int(countLines-1)):
            finishLines[i].append([None])
            finishLines[i][a] = cv2.line(img, tuple(lineArr[i][a]), tuple(lineArr[i][a+1]), color, thickness)

def clearVars():
    finishLines.clear()
    paths.clear()
    countLines = 0
    for i in range(0, maxTracker):
        initVars(i)
    print(finishLines)

while True:

    if(cv2.waitKey(1) & 0xff == ord('q')):
        drawAllLines(img)
        cv2.imwrite(filename, img)
        img = copy.deepcopy(img)
        print(os.listdir(directory))
        clearVars()

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