import pytest

from mtls_poc.SocketClient import SocketClient
from test.test_setup import CA_CERT_PATH, CLIENT_CERT_PATH, CLIENT_KEY_PATH, SERVER_HOST, SERVER_PORT


@pytest.fixture
def mtls_client():
    client = SocketClient(CA_CERT_PATH, CLIENT_CERT_PATH, CLIENT_KEY_PATH, SERVER_HOST, SERVER_PORT)
    yield client
    client.close()

def test_mtls_client_connect_success(mtls_client):
    mtls_client.connect()

    assert mtls_client.ssl_socket is not None 

def test_mtls_client_send_and_receive_data(mtls_client):

    mtls_client.connect()

    mtls_client.send_data(b"hello")

    data = mtls_client.receive_data()

    assert data.decode() == "ok"

def test_mtls_client_connect_failure(mtls_client):
    mtls_client.server_host = "host_invalido.com"

    with pytest.raises(Exception):
        mtls_client.connect()

    assert mtls_client.ssl_socket is None
