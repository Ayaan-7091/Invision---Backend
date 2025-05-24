import cv2
import numpy as np

url = 'http://192.168.0.157:8080/video'  # Replace with your IP
cap = cv2.VideoCapture(url)

while(True):
    retr, frame = cap.read()

    if not retr:
        print("Error occurred in reading the frame")
        break

    frame = cv2.resize(frame,(640,480))
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

   # Red (2 parts)
    lower_red1 = np.array([0, 100, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 70])
    upper_red2 = np.array([180, 255, 255])

    # Green
    lower_green = np.array([36, 100, 70])
    upper_green = np.array([86, 255, 255])

    # Blue
    lower_blue = np.array([94, 100, 70])
    upper_blue = np.array([126, 255, 255])

    # Creating Individual Masks
    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Combining all masks
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)
    combined_mask = cv2.bitwise_or(red_mask, green_mask)
    combined_mask = cv2.bitwise_or(combined_mask, blue_mask)

    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            # drawing contour
            cv2.drawContours(frame, [contour], -1, (0,0,255), 2)
            
            #bounding box
            x,y,w,h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,0),2)

            #center point
            cx = x + w//2
            cy = y + h//2
            cv2.circle(frame, (cx,cy), 5, (255, 255, 255), -1)
            cv2.putText(frame, f"({cx},{cy})", ( cx+10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255, 255, 255), 1 )

    cv2.imshow('RAW',frame)
    cv2.imshow('Red Mask',red_mask)
    # cv2.imshow('Green Mask',green_mask)
    # cv2.imshow('Blue Mask',blue_mask)
    # cv2.imshow('Combined Mask',combined_mask)

    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

cap.release()
cv2.destroyAllWindows() 