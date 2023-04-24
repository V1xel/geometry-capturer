import cv2
import numpy as np

# Load frames
frame1 = cv2.imread("./K2_00015.png")
frame2 = cv2.imread("./K2_00023.png")

# Convert frames to grayscale
prev_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

# Calculate optical flow using Lucas-Kanade method
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
prev_pts = cv2.goodFeaturesToTrack(prev_gray, maxCorners=200, qualityLevel=0.01, minDistance=30)
next_pts, status, err = cv2.calcOpticalFlowPyrLK(prev_gray, gray, prev_pts, None, **lk_params)

# Filter out points with large motion
motion_threshold = 5
good_new = next_pts[status == 1]
good_old = prev_pts[status == 1]
motion = np.sqrt(np.sum((good_new - good_old)**2, axis=1))
motion_mask = motion > motion_threshold
good_new = good_new[motion_mask]
good_old = good_old[motion_mask]

# Draw motion vectors on frame2
for i, (new, old) in enumerate(zip(good_new, good_old)):
    a, b = new.ravel()
    c, d = old.ravel()
    frame2 = cv2.arrowedLine(frame2, (int(a), int(b)),(int(c), int(d)), (0, 255, 0), 2)

# Show the result
cv2.imshow("Optical Flow", frame2)
cv2.waitKey(0)
cv2.destroyAllWindows()
