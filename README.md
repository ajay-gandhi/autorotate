# image rotator

## Example

**Original:**

<img src="https://raw.githubusercontent.com/ajay-gandhi/image-rotator/master/test.jpg" width="350" />

**Fixed:**

<img src="https://raw.githubusercontent.com/ajay-gandhi/image-rotator/master/output.jpg" width="350" />

## Web rotator

Visit [Autorotate](http://autorotate.herokuapp.com) for a live demo!

## CLI

Make sure you have OpenCV installed. Run `cli.py` on the image you want to
rotate. Use the `help`/`h` flag for all the command line options. There's a
sample image in the repo called `test.jpg`.

```bash
python cli.py test.jpg
```

## References

* [Hough Line Transform docs](https://docs.opencv.org/2.4/doc/tutorials/imgproc/imgtrans/hough_lines/hough_lines.html)
* [Line detection with OpenCV](https://www.geeksforgeeks.org/line-detection-python-opencv-houghline-method/)
