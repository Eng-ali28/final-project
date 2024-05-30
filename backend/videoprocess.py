import pygame
import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from app import getIsStopValue
from tracker import *
import time
from math import dist  # محمد هي المكتبة لسا ما تعاملنا معا لا تحذف التعليمة
from PIL import ImageGrab
# from app import getIsStopValue

model = YOLO('yolov8s.pt')
# ...............................

# play music


def play_song(song_file):
    pygame.mixer.init()
    pygame.mixer.music.load(song_file)
    pygame.mixer.music.play()


# اسم الملف الصوتي الخاص بك
song_file = "v.mp3"  # قم بتغييره إلى مسار واسم ملف الأغنية الخاصة بك
# ................................

# Mouse callback function





cy1 = None
cy2 = None

def car_process(videoPath, distance1 , distance2):
    
        # Initialize variables
    # def mouse_callback(event, x, y, flags, param):
    #     global  cy1 , cy2
    #     if event == cv2.EVENT_LBUTTONDOWN:
    #         if cy1 is None:
    #             cy1 = y
    #             print("cy1 set to", cy1)
    #         elif cy2 is None:
    #             cy2 = y
    #             print("cy2 set to", cy2)
        



    
    # Open video capture

    # Create named window and set mouse callback
    cv2.namedWindow('image')
    # cv2.setMouseCallback('RGB', mouse_callback)

    my_file = open("coco.txt", "r")
    data = my_file.read()
    class_list = data.split("\n")
    # print(class_list)

    count = 0

    tracker = Tracker()

    offset = 6

    vh_down = {}
    counter = []
    vh_up = {}
    counter1 = []
    cap = cv2.VideoCapture(videoPath)

    while True:
        # isStop = getIsStopValue()
        # print(isStop)
        success, frame = cap.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            break
        frame = buffer.tobytes()

        count += 1
        if count % 3 != 0:
            continue
        # frame = cv2.resize(frame, (1020, 500))

        # results = model.predict(frame)
    #   print(results)
        # a = results[0].boxes.data
    #     px = pd.DataFrame(a).astype("float")
    # #    print(px)
    #     list = []

        # for index, row in px.iterrows():
        #     #        print(row)

        #     x1 = int(row[0])
        #     y1 = int(row[1])
        #     x2 = int(row[2])
        #     y2 = int(row[3])
        #     d = int(row[5])
        #     c = class_list[d]
        #     if 'car' in c:
        #         list.append([x1, y1, x2, y2])
        # bbox_id = tracker.update(list)
        # for bbox in bbox_id:
        #     x3, y3, x4, y4, id = bbox
        #     cx = int(x3+x4)//2
        #     cy = int(y3+y4)//2

        #     # cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)

        #     if cy1 is not None and cy1 < (cy+offset) and cy1 > (cy-offset):
        #         vh_down[id] = time.time()  # لما تلمس الخط الأول
        #     if id in vh_down:

        #         if cy2 is not None and cy2 < (cy+offset) and cy2 > (cy-offset):
        #             # ناقص الوقت يلي قطعت فيه الخط الأول
        #             elapsed_time = time.time() - vh_down[id]
        #             if counter.count(id) == 0:
        #                 counter.append(id)
        #                 distance1 = 75  # meters
        #                 a_speed_ms = distance1 / elapsed_time
        #                 a_speed_kh = a_speed_ms * 3.6
        #                 cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
        #                 cv2.putText(frame, str(id), (x3, y3),
        #                             cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)
        #                 cv2.putText(frame, str(int(a_speed_kh))+'Km/h', (x4, y4),
        #                             cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
        #                 if int(a_speed_kh) > 10:
        #                     play_song(song_file)
        #                     screenshot = ImageGrab.grab()
        #                     screenshot.save("screenshot.png")
        #                     cv2.putText(frame, "PHOTO", (50, 50),
        #                                 cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)

        #     ##### going UP#####
        #     if cy2 is not None and cy2 < (cy+offset) and cy2 > (cy-offset):
        #         vh_up[id] = time.time()
        #     if id in vh_up:

        #         if cy1 is not None and cy1 < (cy+offset) and cy1 > (cy-offset):
        #             elapsed1_time = time.time() - vh_up[id]

        #             if counter1.count(id) == 0:
        #                 counter1.append(id)
        #                 distance2 = 10  # meters
        #                 a_speed_ms1 = distance2 / elapsed1_time
        #                 a_speed_kh1 = a_speed_ms1 * 3.6
        #                 cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
        #                 cv2.putText(frame, str(id), (x3, y3),
        #                             cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)
        #                 cv2.putText(frame, str(int(a_speed_kh1))+'Km/h', (x4, y4),
        #                             cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)

        # if cy1 is not None:
        #     cv2.line(frame, (274, cy1), (814, cy1), (255, 255, 255), 1)
        #     cv2.putText(frame, ('L1'), (277, cy1-5),
        #                 cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)

        # if cy2 is not None:
        #     cv2.line(frame, (177, cy2), (927, cy2), (255, 255, 255), 1)
        #     cv2.putText(frame, ('L2'), (182, cy2-5),
        #                 cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)

        # d = (len(counter))
        # u = (len(counter1))
        # cv2.putText(frame, ('goingdown:-')+str(d), (60, 90),
        #             cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)

        # cv2.putText(frame, ('goingup:-')+str(u), (60, 130),
        #             cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
        # # cv2.imshow("RGB", frame)
        # if cv2.waitKey(1) & 0xFF == 27:
        #     break

        
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # if isStop == "True" :
        #     cap.release()
        #     cv2.destroyAllWindows()


def stopVideo():
    print("stop video")



