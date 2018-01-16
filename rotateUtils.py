import math
import cv2
import numpy as np

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

    return wr, hr

# Crops an image about the center point to the new width and height
def crop_about_center(img, new_w, new_h):
    diff_x = int(new_w) // 2
    diff_y = int(new_h) // 2
    c_y, c_x = np.array(img.shape[:2]) // 2
    return img[c_y - diff_y:c_y + diff_y, c_x - diff_x:c_x + diff_x]

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

# Performs autorotation using above helpers
def autorotate(img, crop, threshold):
    # Blur and grayscale image
    blur = cv2.blur(img, (5, 5))
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

    # Lines are found by lining up edge features
    edges = cv2.Canny(gray, 50, 150, apertureSize = 3)
    hough_lines = cv2.HoughLines(edges, 1, np.pi / 90, threshold)

    # hough_lines is an array of r and theta values
    if hough_lines is None: return False, "No lines found"

    lines = list(map(lambda x: x[0], hough_lines))

    angle_count, likely_angle = find_baseline(lines)
    rot_angle = convert_to_rotation_angle(likely_angle)

    rotated_img = rotate_img(img, math.degrees(rot_angle))

    if crop:
        # Crop rotated image using original
        height, width = img.shape[:2]
        new_width, new_height = calc_cropped_bounds(width, height, rot_angle)
        return True, crop_about_center(rotated_img, new_width, new_height)
    else:
        # Return uncropped rotated image
        return True, rotated_img
