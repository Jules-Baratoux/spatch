class User(object):
    
    def __init__(self, username, public_key_filename):
        self.username = username
        self.public_key_filename = public_key_filename


class Server(object):

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.alias_by_username = {}
