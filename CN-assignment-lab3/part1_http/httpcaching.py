import http.server
import socketserver
import os
import hashlib
import time
from email.utils import formatdate, parsedate_to_datetime

PORT = 8082
FILE_PATH = "index.html"

class CachingHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/" and self.path != f"/{FILE_PATH}":
            self.send_error(404, "File Not Found")
            return

        # Read file content
        with open(FILE_PATH, "rb") as f:
            content = f.read()

        # Generate ETag
        etag = hashlib.md5(content).hexdigest()

        # Last-Modified
        last_modified = os.path.getmtime(FILE_PATH)
        last_modified_http = formatdate(last_modified, usegmt=True)

        # Check client cache headers
        if_none_match = self.headers.get("If-None-Match")
        if_modified_since = self.headers.get("If-Modified-Since")

        if if_none_match == etag or (
            if_modified_since and 
            parsedate_to_datetime(if_modified_since).timestamp() >= last_modified
        ):
            # File not modified
            self.send_response(304)
            self.end_headers()
            return

        # File changed → send full response
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("ETag", etag)
        self.send_header("Last-Modified", last_modified_http)
        self.end_headers()
        self.wfile.write(content)

# Run server
with socketserver.TCPServer(("", PORT), CachingHandler) as httpd:
    print(f"Serving on port {PORT}...")
    httpd.serve_forever()
