# image rotator

## Example

**Original:**

<img src="https://raw.githubusercontent.com/ajay-gandhi/image-rotator/master/test.jpg" width="350" />

**Fixed:**

<img src="https://raw.githubusercontent.com/ajay-gandhi/image-rotator/master/output.jpg" width="350" />

## Usage

If you just want to try it, run `rotate.sh` on a file. The repo comes with a
test file (`test.jpg`) which you can try it on.

```bash
# Only runs on Mac OS (uses sips)
./rotate.sh test.jpg
```

If you're not on Mac or if you want to see everything for yourself, first run
`parallel.py` on a test image. The script takes two inputs, the path to the file
and the threhold to detect lines (still working on finding a good constant for
this). The last line of output is what you'll need, it's the clockwise angle
from the positive y axis (vertical) that the image must be rotated by.

## Todo

* Add requirements file
* Improve interface
* Implement auto-cropping based on original aspect ratio
* OS independent

## References

* [Hough Line Transform docs](https://docs.opencv.org/2.4/doc/tutorials/imgproc/imgtrans/hough_lines/hough_lines.html)
* [Line detection with OpenCV](https://www.geeksforgeeks.org/line-detection-python-opencv-houghline-method/)
