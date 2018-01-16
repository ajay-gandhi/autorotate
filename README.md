# image rotator

## Example

**Original:**

<img src="https://raw.githubusercontent.com/ajay-gandhi/image-rotator/master/test.jpg" width="350" />

**Fixed:**

<img src="https://raw.githubusercontent.com/ajay-gandhi/image-rotator/master/output.jpg" width="350" />

## Usage

Make sure you have OpenCV installed. Run `cli.py` on the image you want to
rotate. Use the `help`/`h` flag for all the command line options. There's a
sample image in the repo called `test.jpg`.

```bash
python cli.py test.jpg
```

## Tasks

* Convert `cli.py` to use util function
* Improve web interface
  * Crop option
  * Try again button for "wrong rotation" and "no rotation"
  * Add styling
* Output image is _slightly_ blurry, not sure why

## References

* [Hough Line Transform docs](https://docs.opencv.org/2.4/doc/tutorials/imgproc/imgtrans/hough_lines/hough_lines.html)
* [Line detection with OpenCV](https://www.geeksforgeeks.org/line-detection-python-opencv-houghline-method/)
