import inspect
import os
import vcr


def path_generator(function):
    func_dir = os.path.dirname(inspect.getfile(function))
    file_name = '{}.yml'.format(function.__name__)
    return os.path.join(func_dir, 'mocks', file_name)


replay = vcr.VCR(func_path_generator=path_generator)

dir_path = os.path.dirname(os.path.abspath(__file__))
CA_CERT_PATH = f"{dir_path}/certs/serverCA.crt"
CLIENT_CERT_PATH = f"{dir_path}/certs/client.crt"
CLIENT_KEY_PATH = f"{dir_path}/certs/client.key"
SERVER_HOST = "server.127.0.0.1.nip.io"
SERVER_PORT = 4433