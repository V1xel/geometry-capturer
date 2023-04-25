import cv2
import numpy as np
import mss
import pygetwindow as gw

# Set the maximum number of lines to store
max_lines = 50

# Initialize an empty list to store the lines
lines = []

# Initialize the screen capture object
sct = mss.mss()

# Find the game window and activate it
game_window = gw.getWindowsWithTitle(
    "Star Wars: Knights of the Old Republic II: The Sith Lords"
)[0]
game_window.activate()

while True:
    # Capture a screenshot of the game window
    frame = np.array(
        sct.grab(
            {
                "top": game_window.top + 35,
                "left": game_window.left + 10,
                "width": game_window.width - 20,
                "height": game_window.height - 45,
            }
        )
    )

    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform edge detection using Canny algorithm
    edges = cv2.Canny(gray, 50, 150)

    # Perform line detection using Hough transform
    lines_new = cv2.HoughLinesP(
        edges, 1, np.pi / 180, 100, minLineLength=50, maxLineGap=10
    )

    # Match the new lines with the old lines
    if len(lines) > 0 and lines_new is not None:
        for i in range(len(lines)):
            line_matched = False
            for j in range(len(lines_new)):
                dist = np.linalg.norm(lines[i][0] - lines_new[j][0])
                if dist < 20:
                    lines[i] = lines_new[j]
                    line_matched = True
                    break
            if not line_matched:
                lines.pop(i)
                break

    # Add new lines to the list
    if lines_new is not None:
        for line in lines_new:
            line_added = False
            if len(lines) == 0:
                lines.append(line)
                line_added = True
            else:
                for i in range(len(lines)):
                    dist = np.linalg.norm(lines[i][0] - line[0])
                    if dist < 20:
                        lines[i] = line
                        line_added = True
                        break
            if not line_added and len(lines) < max_lines:
                lines.append(line)

    # Draw the lines on the original image
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Display the final image
    cv2.imshow("Game Window", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the resources
cv2.destroyAllWindows()
sct.close()
