import os
import socket
import ssl

# Configurações do servidor
dir_path = os.path.dirname(os.path.abspath(__file__))
HOST = 'server.127.0.0.1.nip.io'
PORT = 4433
CERTFILE = f'{dir_path}/server.pem'
KEYFILE = f'{dir_path}/server.key'
CA_CERTFILE = f'{dir_path}/ca.crt'

# Cria o socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Vincula o socket ao endereço e porta
server_socket.bind((HOST, PORT))

# Inicia a escuta por conexões
server_socket.listen()

# Função para tratar a conexão
def handle_connection(conn):
    # Realiza o handshake SSL/TLS
    conn_ssl = ssl.wrap_socket(conn,
                                server_side=True,
                                certfile=CERTFILE,
                                keyfile=KEYFILE,
                                ca_certs=CA_CERTFILE,
                                cert_reqs=ssl.CERT_NONE,
                                ssl_version=ssl.PROTOCOL_TLS)

    try:
        # Lê os dados enviados pelo cliente
        data = conn_ssl.recv(1024).decode('utf-8')

        breakpoint()
        # Processa os dados recebidos
        if data.strip().lower() == 'hello':
            response = 'ok'
        else:
            response = 'opsss!!!'

        # Envia a resposta para o cliente
        conn_ssl.send(response.encode('utf-8'))
    except ConnectionResetError:
        # Lidar com o erro de conexão resetada pelo cliente
        print("Client connection reset")

    finally:
        # Fecha a conexão SSL
        conn_ssl.close()

# Loop principal para aceitar conexões
while True:
    conn, addr = server_socket.accept()
    handle_connection(conn)
