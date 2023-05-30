import os
import socket
import ssl


dir_path = os.path.dirname(os.path.abspath(__file__))

def handle_client(client_socket):
    request_data = client_socket.recv(1024).decode('utf-8')
    if not request_data:
        return

    # Extrai a URL da solicitação
    url = parse_request(request_data)

    # Processa a solicitação
    response = process_request(url)

    # Envia a resposta ao cliente
    client_socket.sendall(response.encode('utf-8'))

    # Fecha a conexão com o cliente
    client_socket.close()

def parse_request(request_data):
    # Extrai a URL da solicitação HTTP
    lines = request_data.split('\n')
    first_line = lines[0].strip()
    _, url, _ = first_line.split()
    return url

def process_request(url):
    # Processa a solicitação
    # Aqui você pode realizar qualquer lógica necessária com base na URL recebida
    # e retornar uma resposta adequada para o cliente
    # Neste exemplo, estamos apenas retornando uma mensagem de confirmação
    return 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nReceived your request'

def start_server(host, port, certfile, keyfile):
    # Cria o socket do servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configura o contexto SSL para suportar TLS
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)

    # Associa o socket do servidor ao host e porta fornecidos
    server_socket.bind((host, port))

    # Aguarda conexões de clientes
    server_socket.listen(1)
    print(f'Server listening on {host}:{port}')

    while True:
        # Aceita a conexão de um cliente
        client_socket, client_address = server_socket.accept()
        print(f'Accepted connection from {client_address}')

        # Inicia uma conexão segura usando o contexto SSL
        ssl_socket = context.wrap_socket(client_socket, server_side=True)

        # Lida com o cliente em uma thread separada
        handle_client(ssl_socket)

if __name__ == '__main__':
    host = 'server.127.0.0.1.nip.io'
    port = 4433
    certfile = f'{dir_path}/server.pem'
    keyfile = f'{dir_path}/server.key'
    # ca_certfile = f'{dir_path}/ca.crt'

    start_server(host, port, certfile, keyfile)
