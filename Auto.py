import cv2
import time
import os
import numpy as np
import HandTrackingModule as htm
import pyautogui as auto
import sys
import math

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0

frameR = 100 #Frame Reduction
wScr , hScr = auto.size()

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]
i, j = 0, 0
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    img = cv2.flip(img, 1)
    # print(lmList)

    if len(lmList) != 0:
        fingers = []
        # left and right hand will function differenlty
        # Thumb

        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
            # print("Index finger Open")
        else:
            fingers.append(0)
        # 4 Fingers
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
                # print("Index finger Open")
            else:
                fingers.append(0)
        # print(fingers)
        totalFingers = fingers.count(1)
        # if totalFingers == 1: # below is a better approach
        #     auto.sleep(0.5)
        #     auto.keyDown("ctrl")
        #     auto.press("t")
        #     auto.keyUp("ctrl")
        # if index and pinky tip greater than their pipLOL         and           middle and ring tip lower than their pip

        cv2.rectangle(img, (frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,150),2)
        if lmList[tipIds[1]][2] < lmList[tipIds[1]-2][2] and lmList[tipIds[4]][2] < lmList[tipIds[4]-2][2] and lmList[tipIds[2]][2] > lmList[tipIds[2]-2][2] and lmList[tipIds[3]][2] > lmList[tipIds[3]-2][2]:
            # auto.sleep(1)
            print(i)
            i += 1
            if i > 15:
                cv2.putText(img,f"New Tab Created",(175,450),cv2.FONT_HERSHEY_PLAIN,2,(245,200,50),3)
                if i > 20:
                    i = 0
                    auto.hotkey('ctrl','t')

        # if index and pinky tip lower than their pipLOL         and           middle and ring tip greater than their pip
        elif lmList[tipIds[1]][2] > lmList[tipIds[1]-2][2] and lmList[tipIds[4]][2] > lmList[tipIds[4]-2][2] and lmList[tipIds[2]][2] < lmList[tipIds[2]-2][2] and lmList[tipIds[3]][2] < lmList[tipIds[3]-2][2]:
            # auto.sleep(1)
            print(j)
            j += 1
            if j > 15:
                cv2.putText(img,f"This Tab Closed",(175,450),cv2.FONT_HERSHEY_PLAIN,2,(245,200,50),3)
                if j > 20:
                    j = 0
                    auto.hotkey('ctrl','w')
        else:
            i, j = 0, 0

        thumbx, thumby, thumbex = lmList[4][1], lmList[4][2], lmList[2][1]
        indx, indy = lmList[8][1], lmList[8][2]
        midx, midy = lmList[12][1], lmList[12][2]
        ringx, ringy = lmList[16][1], lmList[16][2]
        pinkx, pinky = lmList[20][1], lmList[20][2]


        disIndThumb = math.hypot(thumbx - indx, thumby - indy)
        disMidThumb = math.hypot(thumbx - midx, thumby - midy)
        disRingThumb = math.hypot(thumbx - ringx, thumby - ringy)
        disPinkThumb = math.hypot(thumbx - pinkx, thumby - pinky)

        # disIndOriginx = math.hypot(0 - indx, 0 - 0)
        # disIndOriginy = math.hypot(0 - 0, 0 - indy)
        # # print(disPinkThumb)
        # # print(disRingThumb)
        # print(disIndOriginx, disIndOriginy)

        auto.FAILSAFE = False
        # if disRingThumb < 20 and disRingThumb < 20:


        # if thumbx < thumbex: # this means that thumb go right on left off
        # working smooth
        if lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][2] and lmList[20][2] > lmList[18][2] and thumbx > thumbex:
            # posx, posy = lmList[0][1], lmList[0][2]

            #previous
            # convx = np.interp(indx,(0,640),(0,1920))
            # convx = 1920 - convx
            # convy = np.interp(indy,(0,480),(0,1080))

            # 5. Convert Co-ordinates
            convx = np.interp(indx, (frameR, wCam - frameR), (0, wScr))
            convx = 1920 - convx
            convy = np.interp(indy, (frameR, hCam - frameR), (0, hScr))

            # x and y both of them are inverted since the origin is the top left
            # if the origin were traditional i'd not have any problems
            # however since the y is working fine and i think i know how, x goes left when I go right and vice versa
            # y goes up when i go up,
            # for x if I update it as substracted value from the maximum value it should work fine
            # for y no update is necessary
            # Yeah baby that worked pretty fine, IM A FUCKIN GENIUS
            #getting complex

            auto.moveTo(convx, convy, 0, auto.easeInQuad)

        elif disIndThumb < 20 and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] < lmList[18][2] :
            auto.leftClick()
        elif disMidThumb < 20 and lmList[8][2] < lmList[6][2] and lmList[16][2] < lmList[14][2] and lmList[20][2] < lmList[18][2] :
            auto.rightClick()
        elif disRingThumb < 20 and lmList[12][2] < lmList[10][2] and lmList[8][2] < lmList[6][2] and lmList[20][2] < lmList[18][2] :
            auto.hotkey('ctrl','tab')
        elif disPinkThumb < 20 and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and lmList[8][2] < lmList[6][2] :
            sys.exit()


        # if disRingThumb < 10 and disRingThumb < 10 and disMidThumb < 20 and disIndThumb < 10:
        #     sys.exit()


        # print(totalFingers)

        # dig = totalFingers #Directly passed it
        # cv2.rectangle(img, (160, 400), (480, 480), (0, 255, 0), cv2.FILLED)
        # cv2.putText(img, f"New Tab Created", (45,375), cv2.FONT_HERSHEY_PLAIN, 3, (200, 20, 120), 5)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    # img = cv2.flip(img,1)
    cv2.putText(img,f"FPS :{int(fps)}", (420,60), cv2.FONT_HERSHEY_COMPLEX, 1, (250,50,170), 3)

    cv2.imshow("Counter",img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break











# Finally with the i and j included in the yo and yo invert to new tab and close tab
# I'm a fuckin genius
# Lol