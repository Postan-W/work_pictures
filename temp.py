import cv2
cap = cv2.VideoCapture("./video_origin/55.mp4")
num = cap.get(7)
print(num)