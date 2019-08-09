import cv2
import sys
import numpy as np

def face_detect(video):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    flag = True
    while flag:
        ok, frame = video.read()
        # cv2.imshow('img',frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            flag = not flag
            bbox=(x,y,w,h)
        cv2.imshow('img',frame)
        k = cv2.waitKey(30) & 0xff
    
            # k = cv2.waitKey(0)
    return bbox

if __name__ == '__main__' :
    
    tracker = cv2.TrackerKCF_create()
    video = cv2.VideoCapture(0)

    # Exit if video not opened.
    if not video.isOpened():
        print ("Could not open video")
        sys.exit()
 
    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()

    bbox = (287, 23, 86, 320)

    # Uncomment the line below to select a different bounding box
    # bbox = cv2.selectROI(frame, False)
    # -----------------------------------------------
    bbox = face_detect(video)
    # -----------------------------------------------
    ok = tracker.init(frame, bbox)
 
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
         
        # Start timer
        timer = cv2.getTickCount()
 
        # Update tracker
        ok, bbox = tracker.update(frame)
 
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
 
        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            print("used ")
            face_detect(video)
        # Display tracker type on frame
        cv2.putText(frame, "KCF_face_tracker" + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
     
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)
 
        # Display result
        cv2.imshow("Tracking", frame)
 
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break