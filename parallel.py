import math
import cv2
import numpy as np
import sys

if len(sys.argv) < 3:
    print "Needs 2 arguments, image and line threshold"
    exit()

def rotate_img(img, angle):
    image_center = tuple(np.array(img.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

# Returns tuples of indexes of parallel lines
def find_parallel_lines(lines):
    parallel_pairs = []

    for i in range(len(lines)):
        for j in range(i, len(lines)):
            if (i == j): continue
            if (abs(lines[i][1] - lines[j][1]) == 0):
                parallel_pairs.append((i, j))

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
    if line_angle < 0.25 * np.pi:
        return line_angle

    elif line_angle < 0.75 * np.pi:
        return line_angle - 0.5 * np.pi

    elif line_angle < 1.25 * np.pi:
        return line_angle - np.pi

    elif line_angle < 1.75 * np.pi:
        return line_angle - 1.5 * np.pi

    else:
        return line_angle
    #  angle = 2 * np.pi - line_angle
    #  if line_angle < 0.25 * np.pi:
        #  pass
    #  elif line_angle < 0.75 * np.pi:
        #  angle = 0.5 * np.pi - line_angle
    #  elif line_angle < 1.25 * np.pi:
        #  angle = np.pi - line_angle
    #  elif line_angle < 1.75 * np.pi:
        #  angle = 1.5 * np.pi - line_angle

    #  #  Always return positive angle
    #  return angle if angle > 0 else angle + 2 * np.pi

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

    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 2)

input_img = cv2.imread(sys.argv[1])

# Blur and grayscale image
blur = cv2.blur(input_img, (5, 5))
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
    draw_line(lines[idx1][0], lines[idx1][1], gray)
    draw_line(lines[idx2][0], lines[idx2][1], gray)

cv2.imwrite("withlines.jpg", gray)

angle_count, likely_angle = find_baseline(lines)
rot_angle = math.degrees(convert_to_rotation_angle(likely_angle))

# Print this just for info
print "Angle count:\t" + str(angle_count)
print "In degrees:\t" + str(math.degrees(rot_angle))

# Write rotated image
rotated_img = rotate_img(input_img, rot_angle)
cv2.imwrite("output.jpg", rotated_img)

# Crop rotated image using original
#  print str(np.array(input_img.shape))
#  print str(np.array(input_img.shape)[0:2])
[diff_y, diff_x] = np.array(input_img.shape[0:2]) / 2
[c_y, c_x] = np.array(rotated_img.shape[0:2]) / 2
print str(c_x) + "," + str(diff_x) + "," + str(c_y) + "," + str(diff_y)
cropped_img = rotated_img[c_y - diff_y:c_y + diff_y, c_x - diff_x:c_x + diff_x]
cv2.imwrite("cropped.jpg", cropped_img)
