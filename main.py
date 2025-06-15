import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ========== SETUP GOOGLE SHEETS ==========
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("faceattendance-462916-b4d11df32761.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Face Attendance").sheet1

# Optional: Write header if empty
if sheet.row_count == 0 or sheet.cell(1, 1).value is None:
    sheet.append_row(["Name", "Time"])

# ========== LOAD AND ENCODE KNOWN FACES ==========
path = 'persons'
images = []
classNames = []

# Read images from 'persons' folder
personsList = os.listdir(path)
for cl in personsList:
    curImage = cv2.imread(f'{path}/{cl}')
    if curImage is not None:
        images.append(curImage)
        classNames.append(os.path.splitext(cl)[0])
print("Loaded classes:", classNames)

# Function to encode faces
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
print('Encoding Complete.')

# ========== START WEBCAM ==========
cap = cv2.VideoCapture(0)

# Keep track of names already logged in this session
logged_names = set()

while True:
    success, img = cap.read()
    if not success:
        print("⚠️ Could not access webcam.")
        break

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)

            # Log only once per session
            if name not in logged_names:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                sheet.append_row([name, now])
                logged_names.add(name)

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Face Recognition Attendance', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ========== CLEANUP ==========
cap.release()
cv2.destroyAllWindows()
