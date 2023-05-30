import socket
import ssl

class SocketClient:
    def __init__(self, ca_cert, client_cert, client_key, server_host, server_port):
        self.ca_cert = ca_cert
        self.client_cert = client_cert
        self.client_key = client_key
        self.server_host = server_host
        self.server_port = server_port
        self.ssl_socket = None

    def connect(self):
        # Cria o contexto SSL
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=self.ca_cert)
        ssl_context.load_cert_chain(certfile=self.client_cert, keyfile=self.client_key)

        # Estabelece a conexão TCP
        tcp_socket = socket.create_connection((self.server_host, self.server_port))

        try:
            # Encapsula o soquete TCP com SSL/TLS
            self.ssl_socket = ssl_context.wrap_socket(tcp_socket, server_hostname=self.server_host)
        
        except ConnectionResetError:
            # Lidar com o erro de conexão resetada pelo servidor
            print("Server connection reset")

    def send_data(self, data):
        self.ssl_socket.sendall(data)

    def receive_data(self, bufsize=1024):
        return self.ssl_socket.recv(bufsize)

    def close(self):
        if self.ssl_socket:
            self.ssl_socket.close()
            self.ssl_socket = None
