from http.server import BaseHTTPRequestHandler, HTTPServer
import simplejson
import sys
import os

import base64
import cv2
import numpy as np

from rotateUtils import autorotate

PORT = 8000

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, contentType="text/html"):
        self.send_response(200)
        self.send_header("Content-type", contentType)
        self.end_headers()

    def do_GET(self):
        if self.path == "/main.js":
            self._set_headers("application/javascript")
            f = open("public/main.js", "r")
        else:
            self._set_headers()
            f = open("public/index.html", "r")

        self.wfile.write(f.read().encode())

    def do_POST(self):
        self.send_response(200)
        self.end_headers()

        data_string = self.rfile.read(int(self.headers["Content-Length"]))
        data = simplejson.loads(data_string)
        decoded = np.frombuffer(base64.b64decode(data["image_data"]), dtype=np.uint8)
        #  decoded = np.fromstring(data["image_data"].decode("base64"), np.uint8)
        img = cv2.imdecode(decoded, cv2.IMREAD_COLOR)

        success, result = autorotate(img)
        if success:
            retval, buf = cv2.imencode(".png", result)
            as_text = base64.b64encode(buf)
            result = { "success": True, "imageData": as_text }
            self.wfile.write(simplejson.dumps(result).encode())
        else:
            self.wfile.write(simplejson.dumps({ "success": False, "error": result }).encode())


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server_address = ("", port)
    httpd = HTTPServer(server_address, RequestHandler)
    print ("Starting server on port {}".format(port))
    httpd.serve_forever()
