import cv2
import numpy as np

cap = cv2.VideoCapture(0) # Open the default camera
if not cap.isOpened():
    print("Error opening camera!")
    exit()

while True:
    ret, frame = cap.read() # Capture frame
    if not ret:
        print("Error capturing frame!")
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert to HSV color space
    red_mask = cv2.inRange(hsv_frame, np.array([0, 100, 100]), np.array([100, 255, 255])) # Threshold for red color
    cv2.imshow('Mascara', red_mask)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel) # Opening to remove noise
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel) # Closing to fill gaps
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        bbox = cv2.boundingRect(contours[0])
        cv2.rectangle(frame, bbox, (0, 255, 0), 2) # Draw bounding box on frame
        x, y = bbox[0] + bbox[2] // 2, bbox[1] + bbox[3] // 2
        cv2.putText(frame, f"({x}, {y})", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2) # Display position on frame

    cv2.imshow("Frame", frame) # Show frame with bounding box and position
    if cv2.waitKey(1) == ord('q'): # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()