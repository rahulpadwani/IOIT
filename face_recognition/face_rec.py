import face_recognition
import cv2
import numpy as np
import os

people = os.listdir("people")
print(os.listdir("people"))
known_face_encodings =[]
known_face_names = []
for person in people:
#	print(person)
	if person.endswith("~"):	
		print(person,"deleted")
	else:
#		print(person)		
		img=face_recognition.load_image_file(str('people/'+person))
		img_encoding=face_recognition.face_encodings(img)[0]
		known_face_encodings.append(img_encoding)
		known_face_names.append(person[0:-4])

print(known_face_names)
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


def recognise(frame):
	#cv2.imshow("Tracking", frame)
	#cv2.waitKey(0)
	small_frame=frame
	#small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
	rgb_small_frame = small_frame[:, :, ::-1]
	face_locations = face_recognition.face_locations(rgb_small_frame)
	face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
	face_names = []
	for face_encoding in face_encodings:
		matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
		name = "Unknown"
		face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
		print(face_distances)
		best_match_index = np.argmin(face_distances)
		if matches[best_match_index]:			
			name = known_face_names[best_match_index]
			face_names.append(name)
	return face_names
