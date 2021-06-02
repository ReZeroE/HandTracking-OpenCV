import cv2
import time
import mediapipe as mp

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FPS, 60)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# object creation
mpHand = mp.solutions.hands
handObj = mpHand.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.4, min_tracking_confidence=0.6)
mpDraw = mp.solutions.drawing_utils

prevTime = 0
currTime = 0

while True:
    switch, img = capture.read()
    imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = handObj.process(imageRGB)


    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks != None:
        for handLandmarks in results.multi_hand_landmarks: # handLandmarks is a single hand
            for id, lm in enumerate(handLandmarks.landmark):

                #print(id, lm)
                height, width, c = img.shape
                cx, cy = int(lm.x * width), int(lm.y * height)
                print(id, cx, cy)

            mpDraw.draw_landmarks(img, handLandmarks, mpHand.HAND_CONNECTIONS)

    # fps calc
    currTime = time.time()
    fps = 1/(currTime - prevTime)
    prevTime = currTime

    # parameters: (image, message_to_display, location, font, font_size, color, thickness)
    cv2.putText(img, str(int(fps)), (10, 70), (cv2.FONT_HERSHEY_SIMPLEX), 3, (255, 0, 255), 3)


    cv2.imshow("Web Cam", img)
    cv2.waitKey(1)