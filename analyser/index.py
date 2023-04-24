import cv2
import numpy as np

# Load the image in color mode
image = cv2.imread('./K2_00015.png', cv2.IMREAD_COLOR)

# Convert image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 12))
# eroded = cv2.erode(gray, kernel)

blur = cv2.medianBlur(gray, 3)


# Use canny edge detection
edges = cv2.Canny(blur, 50, 200, apertureSize=3)

# dilated = cv2.dilate(edges, kernel)

# Apply HoughLinesP method to
# to directly obtain line end points
lines_list = []
lines = cv2.HoughLinesP(
    edges,  # Input edge image
    1,  # Distance resolution in pixels
    np.pi/180,  # Angle resolution in radians
    threshold=100,  # Min number of votes for valid line
    minLineLength=5,  # Min allowed length of line
    maxLineGap=10  # Max allowed gap between line for joining them
)

# Iterate over points
for points in lines:
    # Extracted points nested in the list
    x1, y1, x2, y2 = points[0]
    # Draw the lines joing the points
    # On the original image
    if (y2 - y1 + x2 - x1 > 50):
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        lines_list.append([(x1, y1), (x2, y2)])

# All the changes made in the input image are finally
# written on a new image houghlines.jpg
# cv2.imwrite('linesDetected.jpg', img)
cv2.imshow('Detected Surfaces', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
