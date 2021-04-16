import time
import cv2
import mediapipe as mp
import pandas as pd
import openpyxl


class handDetector():
    def __init__(self, mode=False, maxHands = 2, detectionCon=0.6, trackCon = 0.8):
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
        # if self.results.multi_hand_landmarks:
        #     for handLms in self.results.multi_hand_landmarks:
        #         print("handLms : ",handLms)
        #         if draw:
        #             self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                # print("handLms : ",handLms)
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=[0,1], draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            if len(self.results.multi_hand_landmarks) == 1:
                myHand = self.results.multi_hand_landmarks[len(self.results.multi_hand_landmarks)-1]
                handedness = self.results.multi_handedness[0].classification[0]
                if handedness.label == 'Right':
                    for id, lm in enumerate(myHand.landmark):
                        # print(id,lm)
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        # print(id, cx, cy)
                        # which_h = str(which_h)[(str(which_h).find("label")+8):(str(which_h).find("label")+9)]
                        lmList.append([handedness.label,id, cx, cy])
                        # to_df(lmList)
                        if draw:
                            cv2.circle(img,(cx,cy), 10, (255,0,255), cv2.FILLED)
                        if id == 4 or id == 8 or id == 12 or id == 16 or id ==20 :
                            cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)
                if handedness.label == 'Left':
                    # print(myHand)
                    for id, lm in enumerate(myHand.landmark):
                        # print(id,lm)
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        # print(id, cx, cy)
                        lmList.append([handedness.label, id, cx, cy])
                        if draw:
                            cv2.circle(img,(cx,cy), 10, (255,0,255), cv2.FILLED)
                        if id == 4 or id == 8 or id == 12 or id == 16 or id ==20 :
                            cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

            if len(self.results.multi_hand_landmarks) == 2:
                for i in range(len(self.results.multi_hand_landmarks)):
                    myHand_R= self.results.multi_hand_landmarks[len(self.results.multi_hand_landmarks)-2]
                    myHand_L = self.results.multi_hand_landmarks[len(self.results.multi_hand_landmarks)-1]

                    handedness = self.results.multi_handedness[i-1].classification[0]
                    if handedness.label == 'Right':
                        for id, lm in enumerate(myHand_R.landmark):
                            # print(id,lm)
                            h, w, c = img.shape
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            lmList.append([handedness.label, id, cx, cy])

                            if draw:
                                cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                            if id == 4 or id == 8 or id == 12 or id == 16 or id == 20:
                                cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

                    elif handedness.label == 'Left':
                        for id, lm in enumerate(myHand_L.landmark):
                            h, w, c = img.shape
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            lmList.append([handedness.label, id, cx, cy])

                            if draw:
                                cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                            if id == 4 or id == 8 or id == 12 or id == 16 or id == 20:
                                cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

        return lmList

def to_dic(list):
    dic = {}
    if len(list) == 42:
        for i in range(int(len(list)/2)):
            location = list[i][2:4]
            dic['l' + str(i)] = location

        for i in range(int(len(list)/2)):
            location = list[i+21][2:4]
            dic['r' + str(i)] = location

    else:
        if list != [] and list[0][0] == 'Right':
            for i in range(len(list)):
                location = list[i][2:4]
                dic['r' + str(i)] = location

        elif list != [] and list[0][0] == 'Left':
            for i in range(len(list)):
                location = list[i][2:4]
                dic['l' + str(i)] = location
    return dic
def main():
    r_col_series = pd.Series(["r" + str(i) for i in range(21)])
    l_col_series = pd.Series(["l" + str(i) for i in range(21)])

    r_df = pd.DataFrame(columns=r_col_series)
    l_df = pd.DataFrame(columns=l_col_series)

    df = pd.concat([r_df,l_df], axis=1)

    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture('sample10/ajae/')
    # cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img,handNo=0, draw=False)
        print(lmList)
        my_dic = to_dic(lmList)

        # test_df = to_df(lmList)
        # if len(lmList)!=0:
        #     print(lmList)
        # print(test_df)
        # data_to_csv = pd.DataFrame(lmList)

        df = df.append(my_dic, ignore_index=True)

        # ================fps 계산===================#
        cTime = time.time()

        fps = 1 / (cTime - pTime)
        current_time = cTime - pTime
        if(success is True) and (current_time > 1./30):
            pTime = cTime
            cv2.imshow("Image", img)
            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 255), 3)


        df.to_csv("data", mode='w', header=False)
        # print("my_df :", my_df)
        if cv2.waitKey(10) & 0xFF == 27:
            break

    cv2.waitKey(0)
    # print("totalList: ", totalList)
    # handDatacsv = pd.DataFrame(totalList)
    # handDatacsv.to_excel(excel_writer='C:/Users/32141665/Desktop/test.xlsx')

if __name__ =="__main__":
    main()