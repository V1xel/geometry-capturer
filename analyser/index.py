import cv2
import numpy as np

# Load the three frames
frame1 = cv2.imread('./K2_00015.png')
frame2 = cv2.imread('./K2_00019.png')
frame3 = cv2.imread('./K2_00023.png')

# Convert frames to grayscale
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
gray3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2GRAY)

# Find the absolute difference between frames
diff1 = cv2.absdiff(gray1, gray2)
diff2 = cv2.absdiff(gray2, gray3)

# Threshold the difference images to remove noise
thresh1 = cv2.threshold(diff1, 25, 255, cv2.THRESH_BINARY)[1]
thresh2 = cv2.threshold(diff2, 25, 255, cv2.THRESH_BINARY)[1]

# Combine the thresholded images
thresh = cv2.bitwise_and(thresh1, thresh2)

# Define a kernel for morphological operations
kernel = np.ones((5, 5), np.uint8)

# Perform morphological operations to fill in gaps and remove noise
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)

# Detect edges in the resulting image
edges = cv2.Canny(opened, 50, 100, apertureSize=3)

# Perform Hough Line Transform to detect lines in the image
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=100, minLineLength=10, maxLineGap=5)

# Create a list to store the filtered lines
filtered_lines = []

# Iterate over the detected lines
for line in lines:
    x1, y1, x2, y2 = line[0]
    # Compute the angle of the line
    angle = np.arctan2(y2-y1, x2-x1) * 180.0 / np.pi
    # Only keep lines that are within a certain angle range
    if abs(angle) > 10 and abs(angle) < 170:
        # Compute the length of the line
        length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        # Only keep lines that are long enough
        if length > 50:
            # Check if the line is already in the filtered lines list
            if not any(np.allclose(line, l, atol=5) for l in filtered_lines):
                # Add the line to the filtered lines list
                filtered_lines.append(line)

# Draw the filtered lines on the original image
for line in filtered_lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(frame2, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Show the resulting image
cv2.imshow('Filtered Lines', frame2)
cv2.waitKey(0)
cv2.destroyAllWindows()
