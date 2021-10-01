import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
#set the height and width of the frame
cap.set(3, frameWidth)
cap.set(4, frameHeight)

#set the brightness
cap.set(10, 150)

#list of colors with their hue and saturations min and max values
myColors = [[5,107,0,19,255,255],
            [133,56,0,159,156,255],
            [57,76,0,100,255,255]]

#We have to define if some color is detected what should be the color on our drawing
myColorValue = [[51, 153, 255],
                [255, 0, 255],
                [0,255,0]]  #BGR

#For displaying drawing we store each point and loop around them
myPoints =[] #[x, y, colorId]


#find the color in our image
def findColor(img, myColors, myColorValue):
    count = 0
    newPoints = []
    for color in myColors:
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper) #masks the other colors as black except ones which we want to detect
        x, y = getContours(mask)
        cv2.circle(imgresult, (x,y), 10, myColorValue[count], cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x, y, count])
        count+=1
        #cv2.imshow('img', mask)
    return newPoints

# Find the bounding box across the colors
def getContours(img):
    contours, heirarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            #cv2.drawContours(imgresult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    #We want to send the tip of the image rather than center
    return x+w//2, y

def drawonCanvas(myPoints, myColorValue):
    for point in myPoints:
        cv2.circle(imgresult, (point[0], point[1]), 10, myColorValue[point[2]], cv2.FILLED)

while True:
    success, img = cap.read()
    imgresult = img.copy()
    newPoints = findColor(img, myColors, myColorValue)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(myPoints)!=0:
        drawonCanvas(myPoints, myColorValue)
    cv2.imshow("Result", imgresult)
    if cv2.waitKey(1) & 0xFF == ord('q'):# to exit if q is pressed
        break;

