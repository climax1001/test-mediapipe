import mediapipe as mp
import cv2
import matplotlib.pyplot as plt
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
count = 0
# For webcam input:

cap = cv2.VideoCapture('hand_video/k_office.mp4')
with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)
        count += 1
        z_list = [0,1]
        c_list = [0,1]
        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            if results.multi_handedness[0].classification[0].label == 'Left':
                for hand_landmarks in results.multi_hand_landmarks:
                    # x = hand_landmarks.landmark[0].x
                    # y = hand_landmarks.landmark[0].y
                    # z = hand_landmarks.landmark[11].z
                    # plt.plot(count,x,'r-o')
                    # plt.plot(count,y,'b-o')
                    # plt.plot(count,z,'g-o')
                    # plt.pause(0.01)
                    landmarks_drawing_spec = mp_drawing.DrawingSpec(thickness=5, circle_radius=10,
                                                                    color =(0,0,255))
                    connection_drawing_spec = mp_drawing.DrawingSpec(thickness=10, circle_radius=10,
                                                                     color=(255, 0, 0))
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS,landmarks_drawing_spec,connection_drawing_spec)
            if results.multi_handedness[0].classification[0].label == 'Right':
                for hand_landmarks in results.multi_hand_landmarks:
                    cx = hand_landmarks.landmark[0].x
                    cy = hand_landmarks.landmark[0].y
                    cz = hand_landmarks.landmark[0].z
                    x2 = hand_landmarks.landmark[4].x
                    y2 = hand_landmarks.landmark[4].y
                    z2 = hand_landmarks.landmark[4].z
                    x1 = hand_landmarks.landmark[8].x
                    y1 = hand_landmarks.landmark[8].y
                    z1 = hand_landmarks.landmark[8].z
                    degree = ((np.arctan2((y2-y1),(x2-x1)) * 180) / np.pi)
                    print(degree)
                    plt.plot(count,degree,'r-o')
                    #plt.plot(count,y,'b-o')
                    #plt.plot(count,z,'g-o')
                    plt.pause(0.01)
                    landmarks_drawing_spec2 = mp_drawing.DrawingSpec(thickness=5, circle_radius=10,
                                                                     color=(255, 0, 255))
                    connection_drawing_spec2 = mp_drawing.DrawingSpec(thickness=10, circle_radius=10,
                                                                      color=(0, 0, 255))
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                              landmarks_drawing_spec2, connection_drawing_spec2)
            cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
plt.show()
cap.release()