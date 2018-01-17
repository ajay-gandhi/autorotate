from http.server import BaseHTTPRequestHandler, HTTPServer
import simplejson
import sys
import os

import base64
import cv2
import numpy as np

from rotateUtils import autorotate

def contentTypeFromFilename(filename):
    mapping = { ".js": "application/javascript", ".css": "text/css" }
    _, ext = os.path.splitext(filename)
    return mapping[ext] if ext in mapping else "text/html"

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, contentType="text/html"):
        self.send_response(200)
        self.send_header("Content-type", contentType)
        self.end_headers()

    def do_GET(self):
        # Use basename so there are no absolute paths, etc
        file_path = "public/{}".format(os.path.basename(self.path))
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            f = open("public/index.html", "r")
            self.wfile.write(f.read().encode())

        elif os.path.isfile(file_path):
            self.send_response(200)
            self.send_header("Content-type", contentTypeFromFilename(file_path))
            self.end_headers()
            f = open(file_path, "r")
            self.wfile.write(f.read().encode())

        else:
            self.send_response(404)
            self.send_header("Content-type", "text")
            self.end_headers()
            self.wfile.write("404 not found".encode())

    def do_POST(self):
        self.send_response(200)
        self.end_headers()

        data_string = self.rfile.read(int(self.headers["Content-Length"]))
        data = simplejson.loads(data_string)
        decoded = np.frombuffer(base64.b64decode(data["image_data"]), dtype=np.uint8)
        img = cv2.imdecode(decoded, cv2.IMREAD_COLOR)

        threshold = data["threshold"] if "threshold" in data else 100
        success, result = autorotate(img, data["auto_crop"], threshold)
        if success:
            retval, buf = cv2.imencode(".png", result)
            as_text = base64.b64encode(buf)
            res = { "success": True, "imageData": as_text }
            self.wfile.write(simplejson.dumps(res).encode())
        else:
            self.wfile.write(simplejson.dumps({ "success": False, "error": result }).encode())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    server_address = ("", port)
    httpd = HTTPServer(server_address, RequestHandler)
    print ("Starting server on port {}".format(port))
    httpd.serve_forever()
