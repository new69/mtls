from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import ssl

class MTLSHandler(SimpleHTTPRequestHandler):
    def setup(self):
        self.connection = self.request
        self.rfile = self.connection.makefile('rb', self.rbufsize)
        self.wfile = self.connection.makefile('wb', self.wbufsize)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Received your POST request')

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.abspath(__file__))
    certfile = f'{dir_path}/server.pem'
    keyfile = f'{dir_path}/server.key'
    cafile = f'{dir_path}/ca.crt'

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    context.load_verify_locations(cafile=cafile)
    context.verify_mode = ssl.CERT_NONE

    server_address = ('server.127.0.0.1.nip.io', 4433)
    httpd = HTTPServer(server_address, MTLSHandler)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    httpd.serve_forever()
