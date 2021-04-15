import time
import cv2
import mediapipe as mp
import pandas as pd
import openpyxl

class handDetector():
    def __init__(self, mode=False, maxHands = 2, detectionCon=0.9, trackCon = 0.8):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self. mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)  # RGB use
        self.mpDraw = mp.solutions.drawing_utils


    def findHands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print("Multi_hand_landmarks :",self.results.multi_hand_landmarks)
        # print(self.results)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=[0,1], draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:

            myHand = self.results.multi_hand_landmarks[handNo]
            handedness = self.results.multi_handedness[0].classification[0]
            # print(handedness)
            if handedness.label == 'Right':
                # print(myHand)
                for id, lm in enumerate(myHand.landmark):
                    # print(id,lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # print(id, cx, cy)
                    which_h = self.results.multi_handedness
                    # print(which_h)
                    which_h = str(which_h)[(str(which_h).find("label")+8):(str(which_h).find("label")+9)]
                    lmList.append([which_h, id, cx, cy])
                    if draw:
                        cv2.circle(img,(cx,cy), 10, (255,0,255), cv2.FILLED)
                    if id == 4 or id == 8 or id == 12 or id == 16 or id ==20 :
                        cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)

            if handedness.label == 'Left':
                print(myHand)
                for id, lm in enumerate(myHand.landmark):
                    print(id,lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # print(id, cx, cy)
                    which_h = self.results.multi_handedness
                    # print(which_h)
                    which_h = str(which_h)[(str(which_h).find("label")+8):(str(which_h).find("label")+9)]
                    lmList.append([which_h, id, cx, cy])
                    if draw:
                        cv2.circle(img,(cx,cy), 10, (255,0,255), cv2.FILLED)
                    if id == 4 or id == 8 or id == 12 or id == 16 or id ==20 :
                        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        return lmList

    def left_hand_tracker(self, img):
        lmlist = []
        # if self.results.multi_hand_landmarks:
        #     myhand =
        return lmlist

def to_df(list):
    df = pd.DataFrame(list, columns=["r" + str(i for i in range(20))])
    for i in list:
        df.loc[i] = list[i][3:4]

    return df

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture('hand_video/keti.mp4')
    # cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img,handNo=0, draw=False)
        # test_df = to_df(lmList)
        # if len(lmList)!=0:
        #     print(lmList)
        # print(test_df)
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
