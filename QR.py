import time, cv2, pickle
import numpy as np
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

while 1:
    #ret, img = cap.read()
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img = cap.read()
    gray = img
    if cap.isOpened():
        for barcode in decode(gray):
            Data = barcode.data.decode('utf-8')
            
            if (Data != ""):
                with open('/home/pi/Desktop/FINAL/qr.pickle', 'wb') as f:
                    pickle.dump(Data, f)
                    #print(Data)
            time.sleep(0.00001)
        #print(sensor_data)
    
                    
'''
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

detector = cv2.QRCodeDetector()
while True:
    try:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        data, bbox, _ = detector.detectAndDecode(gray)
        if(bbox is not None):
            if (data != ""):
                print(data)
                with open('/home/pi/Desktop/FINAL/qr.pickle', 'wb') as f:
                    pickle.dump(data, f)
        #if(cv2.waitKey(1) == ord("q")):
        #    break
        time.sleep(0.02)
    except cv2.error:
        pass'''

cap.release()
#cv2.error: OpenCV(4.5.1) /tmp/pip-wheel-yqhq3sgl/opencv-contrib-python_c4e7c7ffd9b7480c9c72164eb700cd45/opencv/modules/imgproc/src/convhull.
#cpp:143: error: (-215:Assertion failed) total >= 0 && (depth == CV_32F || depth == CV_32S) in function 'convexHull'