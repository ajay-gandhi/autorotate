import math
import cv2
import numpy as np
import argparse

import util

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatically rotate images")

    parser.add_argument("--output", "-o", metavar="path", type=str, help="output path", default="output.jpg")
    parser.add_argument("--no-crop", action="store_true", help="enable cropping to remove black borders", default=False)
    parser.add_argument("--threshold", "-t", metavar="count", type=int, help="threshold to detect lines for hough transform", default=100)
    parser.add_argument("--verbose", "-v", action="store_true", help="enable logging", default=False)
    parser.add_argument("--save-intermediate", action="store_true", help="Saves intermediate steps as images", default=False)
    parser.add_argument("input", type=str, help="image to rotate")
    args = parser.parse_args()

    input_img = cv2.imread(args.input)

    # Blur and grayscale image
    blur = cv2.blur(input_img, (5, 5))
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

    # Lines are found by lining up edge features
    edges = cv2.Canny(gray, 50, 150, apertureSize = 3)
    hough_lines = cv2.HoughLines(edges, 1, np.pi / 90, args.threshold)

    # hough_lines is an array of r and theta values
    if hough_lines is None:
        print "No lines found"
        exit()
    lines = list(map(lambda x: x[0], hough_lines))

    if args.save_intermediate:
        # Draw parallel lines on the image
        parallels = util.find_parallel_lines(lines)
        for idx_pair in parallels:
            idx1, idx2 = idx_pair
            util.draw_line(lines[idx1][0], lines[idx1][1], gray)
            util.draw_line(lines[idx2][0], lines[idx2][1], gray)

        cv2.imwrite("withlines.jpg", gray)

    angle_count, likely_angle = util.find_baseline(lines)
    rot_angle = util.convert_to_rotation_angle(likely_angle)

    if args.verbose:
        # Print this just for info
        print "Angle count:\t" + str(angle_count)
        print "Rotation angle:\t" + str(math.degrees(rot_angle))

    rotated_img = util.rotate_img(input_img, math.degrees(rot_angle))

    if args.no_crop:
        # Write uncropped rotated image
        rotated_img = util.rotate_img(input_img, math.degrees(rot_angle))
        cv2.imwrite(args.output, rotated_img)
    else:
        # Crop rotated image using original
        height, width = input_img.shape[:2]
        new_width, new_height = util.calc_cropped_bounds(width, height, rot_angle)
        cropped_img = util.crop_about_center(rotated_img, new_width, new_height)

        if args.verbose:
            print "Old size:\t" + str(width) + "x" + str(height)
            print "New size:\t" + str(int(new_width)) + "x" + str(int(new_height))
        cv2.imwrite(args.output, cropped_img)

