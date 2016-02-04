
import paramiko


class Client(object):
    
    def __init__(self, username, public_key_file):
        self.username = username
        self.public_key = paramiko.RSAKey(filename=public_key_file)


class RemoteHost(object):

    def __init__(self, hostname, username, port):
        self.hostname = hostname
        self.username = username
        self.port = port

