# Shape Detection API using OpenCV and Flask

## Overview

This project is a simple Flask-based web API that detects basic geometric shapes — triangles, squares, rectangles, and circles — in images. It uses OpenCV for image processing and contour analysis to identify and annotate these shapes on the input images.

You can send an image via a POST request, and the API will return the image annotated with detected shapes highlighted with bounding boxes and labels.

---

## Features

- Detects triangles, squares, rectangles, and circles.
- Uses adaptive thresholding to handle varying lighting conditions.
- Draws contours, bounding boxes, and shape names on detected shapes.
- Lightweight Flask server that can be integrated with frontend applications such as mobile or web apps.

---

## How It Works

1. Converts the input image to grayscale and applies Gaussian blur to reduce noise.
2. Applies adaptive thresholding to create a binary image that works well under different lighting conditions.
3. Uses morphological closing to clean up the binary image.
4. Detects contours and approximates their polygonal curves.
5. Classifies the shape based on the number of vertices and circularity.
6. Annotates the original image with detected shapes.
7. Returns the processed image as a response.

---

## Installation and Setup

### Prerequisites

- Python 3.7 or higher
- [Flask](https://flask.palletsprojects.com/)
- [OpenCV](https://opencv.org/)
- [NumPy](https://numpy.org/)

Install the required Python packages using pip:

```bash
pip install flask opencv-python numpy
```

## Running the Server
Run the Flask application:

## Usage
Send a POST request to the /detect-shapes endpoint with a form-data key named image containing your image file.

## Future Improvements
Improve detection accuracy for imperfect or hand-drawn shapes.

Extend detection to more shape types.

Create a user-friendly frontend app (e.g., Flutter, React) to upload images and display results.

Add asynchronous processing and batch image support.

Add unit tests and CI/CD pipeline.

## Author
Ayaan Shaikh
Ayaan-7091 

Thank you for checking out this project! Feel free to contribute or raise issues.

