import time
import cv2
import mediapipe as mp
import pandas as pd
import openpyxl

class handDetector():
    def __init__(self, mode=False, maxHands = 2, detectionCon=0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self. mpHands.Hands(self.mode, self.maxHands, self.detectionCon,
                                         self.trackCon)  # RGB use
        self.mpDraw = mp.solutions.drawing_utils


    def findHands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=[0,1], draw =True ):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[0]

            for id, lm in enumerate(myHand.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                which_h = self.results.multi_handedness
                which_h = str(which_h)[(str(which_h).find("label")+8):(str(which_h).find("label")+9)]
                # print(which_h)

                # print(test)

                lmList.append([handNo, which_h, id, cx, cy])
                if draw:
                    cv2.circle(img,(cx,cy), 10, (255,0,255), cv2.FILLED)
                # if wid == 4 or id == 8 or id == 12 or id == 16 or id ==20 :
                #     cv2.circle(img, (cx, cy), 15, (125, 125, 255), cv2.FILLED)

            if myHand is not None:
                myHand2 = self.results.multi_hand_landmarks[handNo[1]]
                print(myHand2)
        return lmList

def main():
    pTime = 0
    cTime = 0
    # cap = cv2.VideoCapture('hand_video/keti.mp4')
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    # totalList = pd.DataFrame({
    #     'r0': [],
    #     'r1': [],
    #     '2': [],
    #     '3': [],
    #     '4': [],
    #     '5': [],
    #     '6': [],
    #     '7': [],
    #     '8': [],
    #     '9': [],
    #     '10': [],
    #     '11': [],
    #     '12': [],
    #     '13': [],
    #     '14': [],
    #     '15': [],
    #     '16': [],
    #     '17': [],
    #     '18': [],
    #     '19': [],
    #     '20': [],
    # })
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img,handNo=0, draw=False)
        # totalList.append(lmList)
        if len(lmList)!=0:
            print(lmList)

        # data_to_csv = pd.DataFrame(lmList)
        #fps 계산
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
        cv2.imshow("Image", img)

        if cv2.waitKey(1)&0xFF == 27:
            break

    cv2.waitKey(0)
    # print("totalList: ", totalList)
    # handDatacsv = pd.DataFrame(totalList)
    # handDatacsv.to_excel(excel_writer='C:/Users/32141665/Desktop/test.xlsx')

if __name__ =="__main__":
    main()
