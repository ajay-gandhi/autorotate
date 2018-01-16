import math
import cv2
import numpy as np
import sys

if len(sys.argv) < 3:
    print "Needs 2 arguments, image and line threshold"
    exit()

# Returns tuples of indexes of parallel lines
def find_parallel_lines(lines):
    parallel_pairs = []

    for i in range(len(lines)):
        for j in range(i, len(lines)):
            if (i == j): continue
            if (abs(lines[i][1] - lines[j][1]) == 0):
                parallel_pairs.append((i,j))

    return parallel_pairs

# Finds set of parallel lines that is largest (the "baseline" of the image)
def find_baseline(lines):
    angle_counts = {}
    current_max = -1
    most_common_angle = 0

    for i in range(len(lines)):
        for j in range(i, len(lines)):
            if (i == j): continue
            if (abs(lines[i][1] - lines[j][1]) == 0):
                key = str(lines[i][1])
                if key in angle_counts:
                    angle_counts[key] += 1
                else:
                    angle_counts[key] = 1

                if angle_counts[key] > current_max:
                    current_max = angle_counts[key]
                    most_common_angle= lines[i][1]

    return angle_counts, most_common_angle

# Finds the angle of rotation required to straighten the image to the closest
# axis (horizontal or vertical)
def convert_to_rotation_angle(line_angle):
    angle = 360 - line_angle
    if line_angle < 45:
        pass
    elif line_angle < 135:
        angle = 90 - line_angle
    elif line_angle < 225:
        angle = 180 - line_angle
    elif line_angle < 315:
        angle = 270 - line_angle

    # Always return positive angle
    return angle if angle > 0 else angle + 360

# Draws a line on img given r and theta in polar
# Computes two points in (x, y) and passes them to cv2.line
def draw_line(r, theta, img):
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*r
    y0 = b*r

    x1 = int(x0 + 1000 * -b)
    y1 = int(y0 + 1000 * a)
    x2 = int(x0 - 1000 * -b)
    y2 = int(y0 - 1000 * a)

    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

img = cv2.imread(sys.argv[1])

# Blur and grayscale image
blur = cv2.blur(img, (5, 5))
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

# Lines are found by lining up edge features
edges = cv2.Canny(gray, 50, 150, apertureSize = 3)
hough_lines = cv2.HoughLines(edges, 1, np.pi / 90, int(sys.argv[2]))

# hough_lines is an array of r and theta values
if hough_lines is None:
    print "No lines found"
    exit()

lines = list(map(lambda x: x[0], hough_lines))

# Draw parallel lines on the image
parallels = find_parallel_lines(lines)
for idx_pair in parallels:
    idx1, idx2 = idx_pair
    draw_line(lines[idx1][0], lines[idx1][1], img)
    draw_line(lines[idx2][0], lines[idx2][1], img)

cv2.imwrite("withlines.jpg", img)

angles, likely_angle = find_baseline(lines)

# Print this just for info
print angles
print convert_to_rotation_angle(math.degrees(likely_angle))
