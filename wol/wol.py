#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from wakeonlan import send_magic_packet

# Replace 'your_secret_string' with your desired secret string
SECRET_STRING = b'your secret goes here'

class WOLRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'''
            <html>
            <head><title>Wake-on-LAN</title></head>
            <body>
            <h1>Enter the secret string:</h1>
            <form method="post">
                <input type="text" name="secret" placeholder="Secret String">
                <button type="submit">Submit</button>
            </form>
            </body>
            </html>
        ''')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        params = parse_qs(post_data.decode('utf-8'))
        if 'secret' in params:
            if params['secret'][0].encode('utf-8') == SECRET_STRING:
                send_magic_packet('54:e1:ad:ad:c4:d1')  # Replace with the MAC address of the target machine
                response_message = 'WakeOnLAN message sent to wake up computer successully!'
            else:
                response_message = 'Incorrect secret string. Please try again.'
        else:
            response_message = 'No secret string provided.'

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response_message.encode())

def run(server_class=HTTPServer, handler_class=WOLRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting server...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Server stopped.')

if __name__ == '__main__':
    run()
