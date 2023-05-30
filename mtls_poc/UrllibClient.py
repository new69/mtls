from http.client import HTTPResponse
import ssl
from urllib import request

class UrllibClient:
    def __init__(self, url, certfile, keyfile, cafile):
        self.url = url
        self.cert_file = certfile
        self.key_file = keyfile
        self.ca_cert = cafile
        
    def send_data(self, data=None):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile=self.ca_cert)
        context.load_cert_chain(certfile=self.cert_file, keyfile=self.key_file)

        response: HTTPResponse = request.urlopen(self.url, data=data, context=context)
        return response

    # def send_data(self, data):
    #     # Envia dados para o servidor
    #     req = request.Request(self.url, data=data.encode('utf-8'), method='POST')
    #     response = self.opener.open(req)
    #     return response

    # def receive_data(self):
    #     # Recebe dados do servidor
    #     response = self.opener.open(self.url)
    #     return response.read().decode('utf-8')
