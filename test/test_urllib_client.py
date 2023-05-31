import pytest

from mtls_poc.UrllibClient import UrllibClient
from test.test_setup import CA_CERT_PATH, CLIENT_CERT_PATH, CLIENT_KEY_PATH, SERVER_HOST, SERVER_PORT, replay

@pytest.fixture
def mtls_client():
    client = UrllibClient(f'https://{SERVER_HOST}:{SERVER_PORT}/', CLIENT_CERT_PATH, CLIENT_KEY_PATH, CA_CERT_PATH)
    yield client

@replay.use_cassette
def test_urllib_client_connect_success(mtls_client):
    conn = mtls_client.send_data(b'hello')

    assert conn.status is 200

@replay.use_cassette
def test_urllib_client_send_and_receive_data(mtls_client):

    conn = mtls_client.send_data(b"hello")

    assert conn.read().decode('utf-8') == "Received your POST request"
