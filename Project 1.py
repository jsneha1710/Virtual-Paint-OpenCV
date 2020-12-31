import cv2
import numpy as np
cap=cv2.VideoCapture(0)  #to capture video from webcam (0) and from file(1)
cap.set(3,640) #setting the width and height
cap.set(4,480)
cap.set(10,150)
mycolors=[(5,107,0,19,255,255),
          (133,56,0,159,156,255),
          (57,76,0,100,255,255)]
mycolorvalue=[(51,153,255),
              (255,0,255),
              (0,255,0)]
mypoints=[]
def findcolor(img,mycolors,mycolorvalue):
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count=0
    newpoints=[]
    for color in mycolors:
        lower=np.array(color[0:3])
        upper=np.array(color[3:6])
        mask=cv2.inRange(imgHSV,lower,upper)
        #cv2.imshow(str(color[0]),mask)
        x,y=getcontours(mask)
        cv2.circle(imgResult,(x,y),10,mycolorvalue[count],cv2.FILLED)
        if(x!=0 and y!=0):
            newpoints.append([x,y,count])
        count+=1
    return newpoints

def getcontours(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if(area>500):
            #cv2.drawContours(imgResult,cnt,-1,(255,0,0),1)
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            x ,y ,w ,h=cv2.boundingRect(approx)
    return x+w//2,y

def drawcanvas(mypoints,mycolorvalue):
    for point in mypoints:
        cv2.circle(imgResult, (point[0],point[1]), 10, mycolorvalue[point[2]], cv2.FILLED)


while True:
    success,img=cap.read()
    imgResult=img.copy()
    newpoints=findcolor(img,mycolors,mycolorvalue)
    if(len(newpoints)!=0):
        for d in newpoints:
            mypoints.append(d)
    if (len(mypoints) != 0):
        drawcanvas(mypoints,mycolorvalue)
    drawcanvas(newpoints,mycolorvalue)
    cv2.imshow("Video",imgResult)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

