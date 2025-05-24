from flask import Flask, request, jsonify, send_file
import cv2
import numpy as np
import tempfile
import os

app = Flask(__name__)

def detector(image_path):
    image = cv2.imread(image_path) 

    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),1)


    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,  # Invert to make shapes white on black
        11,
        2
    )

    kernel = np.ones((2,2),np.uint8)
    thresh = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel)

    contours, _ = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    shapes = []

    for contour in contours:
        if cv2.contourArea(contour) < 500:
             continue

        approx = cv2.approxPolyDP(contour,0.02 * cv2.arcLength(contour,True),True)
        x, y, w, h = cv2.boundingRect(approx)
        
        aspect_ratio = w/float(h)
        shape_type = None
        if len(approx) == 3:
            shape_type = "Triangle"
        elif len(approx) == 4:
            if 0.95<=aspect_ratio<=1.05:
                shape_type = "Square"
            else:
                shape_type="Rectangle"
        elif len(approx) > 4:
            perimeter = cv2.arcLength(contour,True)
            area = cv2.contourArea(contour)
            circularity = 4 * np.pi * (area / ( perimeter * perimeter ))
            if circularity > 0.8: 
             shape_type = "circle"

        if shape_type:
            cv2.drawContours(image,[approx],0,(0,255,0),2)
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(image,shape_type,(x,y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)

    output_path = tempfile.NamedTemporaryFile(delete=False,suffix='.jpg').name
    cv2.imwrite(output_path,image)

    return output_path

@app.route('/detect-shapes',methods=['POST'])
def detect():
    if 'image' not in request.files:
        return{'error':'Image file not provided'},400
    
    image_file = request.files['image']
    with tempfile.NamedTemporaryFile(delete=False,suffix=".jpg") as tmp:
        image_file.save(tmp.name)
        output_path = detector(tmp.name)

    return send_file(output_path, mimetype='image/jpeg')

if __name__ == '__main__':
    print("🚀 Starting Flask Server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
