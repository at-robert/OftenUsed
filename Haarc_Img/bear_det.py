import numpy as np
import cv2

# face_cascade = cv2.CascadeClassifier('./haarc_xml/haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier('./haarc_xml/haarcascade_eye.xml')

#this is the cascade we just made. Call what you want
bear_cascade = cv2.CascadeClassifier('./haarc_xml/cascade_bear.xml')

cap = cv2.VideoCapture(0)

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # add this
    # image, reject levels level weights.
    # bears = bear_cascade.detectMultiScale(gray, 1.3, 5)
    bears = bear_cascade.detectMultiScale(gray, scaleFactor=1.3,minNeighbors=10,minSize=(20,20))
    
    # add this
    for (x,y,w,h) in bears:
        # cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,'Bear',(x,y), font, 0.5, (11,255,255), 2, cv2.LINE_AA)

    # for (x,y,w,h) in faces:
    #     cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

    #     roi_gray = gray[y:y+h, x:x+w]
    #     roi_color = img[y:y+h, x:x+w]
    #     eyes = eye_cascade.detectMultiScale(roi_gray)
    #     for (ex,ey,ew,eh) in eyes:
    #         cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 99:
        break

cap.release()
cv2.destroyAllWindows()