#!/usr/bin/env python3

"""
Place this script at root folder of your media collection.
The folder either contains sub folders, or contains number of images
It scans and displays all images in folder
"""

import os
import http.server
import socketserver
import ssl
import base64

PORT = 60001  # choose any available port number
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webm")
USERNAME = 'pi'
PASSWORD = 'pipiii'

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

class SecureHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if not self.authenticate():
            self.send_authenticate_header()
            return
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def authenticate(self):
        auth_header = self.headers.get('Authorization')
        if auth_header is None:
            return False
        auth_parts = auth_header.split()
        if len(auth_parts) != 2 or auth_parts[0].lower() != 'basic':
            return False
        auth_str = bytes(f"{USERNAME}:{PASSWORD}", 'utf-8')
        auth_str_from_client =  base64.b64decode(auth_parts[1]).decode("utf-8")
        correct_auth_str = bytes(f"{auth_str_from_client}", 'utf-8')
        return auth_str == correct_auth_str

    def send_authenticate_header(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Restricted Area"')
        self.end_headers()
        self.wfile.write(bytes('Authentication failed', 'utf-8'))
        
     def list_directory(self, path):
        # check if any image files are present in directory
        has_images = any(f.lower().endswith(IMAGE_EXTENSIONS) for f in os.listdir(path))

        # use default directory listing if no images present
        if not has_images:
            return super().list_directory(path)

        # generate custom directory listing that includes images
        try:
            # generate list of images in folder
            images = os.listdir(path)
            # create HTML page with images
            page = '<html><body>'
            for image in images:
                page += f'<img src="{image}" alt="{image}" style="width: 100%;">'
            page += '</body></html>'

            html_head = '''
            <html>
                <head>
                    <title>Image Server</title>
                    <style>
                        html, body {
                            width: 100%;
                            height: 100%;
                        }
                    </style>
                </head>
                <body>
            '''
            html_foot = '''
                </body>
            </html>
            '''
            # send response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-Length', len(page))
            self.end_headers()
            self.wfile.write(html_head.encode())
            self.wfile.write(page.encode())
            self.wfile.write(html_foot.encode())
        except OSError:
            self.send_error(404, "File not found")
Handler = SecureHandler

with ThreadedHTTPServer(('0.0.0.0', PORT), SecureHandler) as httpd:
    print(f"Serving at https://localhost:{PORT}")
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   keyfile="key.pem",
                                   certfile="cert.pem",
                                   server_side=True)
    httpd.serve_forever()
