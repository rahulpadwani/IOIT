import cv2
import sys
import numpy as np
import face_rec as fc


def face_detect(video,pretraker,mode):
    """
    mode=> 1 for lost trackers
           2 for check for new faces
           3 lost some trackers
    """
    global detected_people
    global count
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # face_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
    flag = True
    bbox = (287, 23, 86, 320)
    # print("mode:-"+str(mode))
    trackers=[]
        
    while flag:
        ok, frame = video.read()
        if pretraker !=None and mode==2:
            for tracker in pretraker:
                ok, bbox = tracker.update(frame)
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                roi_color = frame[p1[1]:p2[1],p1[0]:p2[0]]
                name=fc.recognise(roi_color)
                if (len(name)>0):
                   print(str(count)+":-"+str(name))
                   if(str(name) not in detected_people):
                      detected_people.append(str(name))
                   count+=1
                #print(name)
                cv2.rectangle(frame, p1, p2, (0,0,0), -1, 1)
                
                
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('img',gray)
        
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            tracker = cv2.TrackerKCF_create()
            bbox=(x,y,w,h)
            ok = tracker.init(frame, bbox)    
            trackers.append(tracker)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,255),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            name=fc.recognise(roi_color)
            print(name)
            flag = False
            # break
        line=""
        for p in detected_people:
           line = line +","+ str(p)
        cv2.putText(frame, line, (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)
        cv2.imshow('face_detect',frame)
        k = cv2.waitKey(1) & 0xff
        # Exit if ESC pressed
        if k == 27 : break
        if ((pretraker !=None and mode !=1) or mode==2)  :
            flag=False
            # k = cv2.waitKey(0)
    if trackers:
        # print("new tracker")
        if mode ==2:
            for tracker in pretraker:
                trackers.append(tracker)
        return trackers
    else:
        # print("old tracker") 
        return pretraker
if __name__ == '__main__' :
    
    global detected_people
    global count
    count=0
    detected_people=[]
    # tracker = cv2.TrackerKCF_create()
    #video = cv2.VideoCapture(0)
    video = cv2.VideoCapture("http://192.168.43.21:8160")

    # Exit if video not opened.
    if not video.isOpened():
        print ("Could not open video")
        sys.exit()
 
    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()

    # default value
    bbox = (287, 23, 86, 320)

    # detectes face and generates a tracker for it
    # -----------------------------------------------
    trackers=face_detect(video,None,1)
    # -----------------------------------------------
    
    flag= False
    cnt=0
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
         
        # Start timer
        timer = cv2.getTickCount()
 
        # Update tracker
        bboxes=[]
        for tracker in trackers:
            ok, bbox = tracker.update(frame)
            if ok:
                bboxes.append(bbox)
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
 
        for bbox in bboxes:
                # Tracking success
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, (255,255,0), 3, 1)
                roi_color = frame[p1[1]:p2[1],p1[0]:p2[0]]
                name=fc.recognise(roi_color)
                if (len(name)>0):
                   print(str(count)+":-"+str(name))
                   if(str(name) not in detected_people):
                      detected_people.append(str(name))
                   count+=1
                #print(name)
        if len(bboxes)==0 :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            # print("used ")
            flag=True
        if cnt>50:
            flag=True
            cnt=100
            # cnt=0
        # Display tracker type on frame
        cv2.putText(frame, "KCF_face_tracker" + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
     
        # Display FPS on frame
        #cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)
        
        line=""
        for p in detected_people:
           line = line +","+ str(p)
        cv2.putText(frame, line, (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)
        # Display result
        cv2.imshow("Tracking", frame)
        if flag:
            """
                use haar_cascade to find the face again
                and reset the tracker
                single tracker
                tracker=face_detect(video)
                multi tracker
            """
            if cnt==100:
                trackers=face_detect(video,trackers,2)
            else:
                trackers=face_detect(video,trackers,1)
            cnt=0
            # print(len(trackers))
            # print("trackers:-"+str(len(trackers)))
            
            flag= False
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break
        if k == ord('c'):
            for tracker in trackers:
                for temp in trackers:
                    if temp==tracker:
                        print("true,",end=" ")
                    else:
                        print("false,",end=" ")
                print(" ")
        cnt+=1
