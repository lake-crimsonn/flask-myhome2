import requests
import cv2
import socket
import base64

cap = cv2.VideoCapture(1)
url = "http://localhost:5000/sms"

HOST = 'localhost'
PORT = 5001

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((HOST, PORT))
while True:
    ret, frame = cap.read()

    base64_frame = base64.b64encode(frame)
    frame_length = str(len(base64_frame))

    soc.sendall(frame_length.encode('utf-8').lstrip(64))
    soc.send(base64_frame)

    if cv2.waitKey(1) == ord('a'):
        response = requests.get(url)
        print(response.text)

    if cv2.waitKey(1) == ord('q'):
        break

soc.close()
cap.release()
cv2.destroyAllWindows()
