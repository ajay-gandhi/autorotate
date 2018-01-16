# image rotator

## Example

**Original:**

<img src="https://raw.githubusercontent.com/ajay-gandhi/image-rotator/master/test.jpg" width="350" />

**Fixed:**

<img src="https://raw.githubusercontent.com/ajay-gandhi/image-rotator/master/output.jpg" width="350" />

## Usage

Run `parallel.py` on the image you want to rotate. The script takes two
[required] arguments, the path to the image and the threshold for recognizing
lines.

```bash
python parallel.py test.jpg 100
```

## Todo

* Add requirements file
* Improve interface
* Implement auto-cropping based on original aspect ratio
* OS independent

## References

* [Hough Line Transform docs](https://docs.opencv.org/2.4/doc/tutorials/imgproc/imgtrans/hough_lines/hough_lines.html)
* [Line detection with OpenCV](https://www.geeksforgeeks.org/line-detection-python-opencv-houghline-method/)
