import math
import cv2
import numpy as np
import sys

if len(sys.argv) < 3:
    print "Needs 2 arguments, image and line threshold"
    exit()

# Rotates an image without cropping the corners
def rotate_img(img, angle):
    height, width = img.shape[:2]
    image_center = (width / 2, height / 2)
    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1)

    radians = math.radians(angle)
    sin = math.sin(radians)
    cos = math.cos(radians)
    bound_w = int((height * abs(sin)) + (width * abs(cos)))
    bound_h = int((height * abs(cos)) + (width * abs(sin)))

    rotation_mat[0, 2] += ((bound_w / 2) - image_center[0])
    rotation_mat[1, 2] += ((bound_h / 2) - image_center[1])

    return cv2.warpAffine(img, rotation_mat, (bound_w, bound_h))

# Taken from https://stackoverflow.com/a/16778797
def calc_cropped_bounds(w, h, angle):
    width_is_longer = w >= h
    side_long, side_short = (w, h) if width_is_longer else (h, w)

    sin_a, cos_a = abs(math.sin(angle)), abs(math.cos(angle))
    if side_short <= 2. * sin_a * cos_a * side_long or abs(sin_a - cos_a) < 1e-10:
        x = 0.5 * side_short
        wr,hr = (x / sin_a, x / cos_a) if width_is_longer else (x / cos_a, x / sin_a)
    else:
        cos_2a = cos_a * cos_a - sin_a * sin_a
        wr, hr = (w * cos_a - h * sin_a) / cos_2a, (h * cos_a - w * sin_a) / cos_2a

    return np.array([int(wr), int(hr)])

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
rot_angle = convert_to_rotation_angle(likely_angle)

# Print this just for info
print "Angle count:\t" + str(angle_count)
print "In degrees:\t" + str(math.degrees(rot_angle))

# Write rotated image
rotated_img = rotate_img(input_img, math.degrees(rot_angle))
cv2.imwrite("output.jpg", rotated_img)

# Crop rotated image using original
#  print str(np.array(input_img.shape))
#  print str(np.array(input_img.shape)[0:2])
height, width = input_img.shape[:2]
diff_y, diff_x = calc_cropped_bounds(width, height, rot_angle) / 2
c_y, c_x = np.array(rotated_img.shape[:2]) / 2
print str(c_x) + "," + str(diff_x) + "," + str(c_y) + "," + str(diff_y)
cropped_img = rotated_img[c_y - diff_y:c_y + diff_y, c_x - diff_x:c_x + diff_x]
