import cv2

url = 'http://192.168.0.157:8080/video'  # Replace with your IP
cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
            corners = len(approx)

            x, y, w, h = cv2.boundingRect(approx)

            shape = "Unknown"
            if corners == 3:
                shape = "Triangle"
            elif corners == 4:
                aspectRatio = w / float(h)
                if 0.95 < aspectRatio < 1.05:
                    shape = "Square"
                else:
                    shape = "Rectangle"
            elif corners > 4:
                shape = "Circle"

            cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, shape, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (255, 255, 255), 2)

    cv2.imshow("Shape Detection", frame)
    cv2.imshow("Edges", edges)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
