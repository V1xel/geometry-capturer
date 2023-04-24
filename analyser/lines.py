import cv2
import numpy as np

image = cv2.imread('./K2_00015.png', cv2.IMREAD_COLOR)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 12))
# eroded = cv2.erode(gray, kernel)

blur = cv2.medianBlur(gray, 3)

edges = cv2.Canny(blur, 50, 100, apertureSize=3)

# dilated = cv2.dilate(edges, kernel)

lines_list = []
lines = cv2.HoughLinesP(
    edges,  # Input edge image
    3,  # Distance resolution in pixels
    np.pi/180,  # Angle resolution in radians
    threshold=100,  # Min number of votes for valid line
    minLineLength=5,  # Min allowed length of line
    maxLineGap=15  # Max allowed gap between line for joining them
)

for points in lines:
    x1, y1, x2, y2 = points[0]
    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    lines_list.append([(x1, y1), (x2, y2)])


cv2.imshow('Detected Surfaces', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
