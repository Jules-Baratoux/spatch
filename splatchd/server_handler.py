
import os
import logging
import threading
import base64
import paramiko
import database
from binascii import hexlify
from paramiko.py3compat import b, u, decodebytes

LOG = logging.getLogger('spatch')


def query_server_selection(granted_servers):

    info = """Enter an endpoint you wish to connect to:\n\n{}\n"""

    server_list_fmt = "- {hostname:>5}:{port} as {alias}"
    L = []
    for server in granted_servers:
        L.append(server_list_fmt.format(hostname=server[0],
                                        port=server[1], alias=server[2]))
    info = info.format('\n'.join(L))
    query = paramiko.InteractiveQuery("", info)

    query.add_prompt("Enter the server's hostname: ", echo=True)
    return query


class ServerHandler(paramiko.ServerInterface):

    def __init__(self):
        self._allowed_auths = ['keyboard-interactive']
        self._shell_request_event = threading.Event()
        
    def get_allowed_auths(self, username):
        return ','.join(self._allowed_auths)

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_interactive(self, username, submethods):
        self._granted = database.granted_servers(username)
        if len(self._granted) == 0:
            return paramiko.AUTH_FAILED
        return query_server_selection(self._granted)

    def check_auth_interactive_response(self, responses):
        for host, port, alias in self._granted:
            if host == responses[0]:
                self.remote_address= (host, port, alias)
                self._allowed_auths = ['publickey']
                return paramiko.AUTH_PARTIALLY_SUCCESSFUL
        # self._allowed_auths = []
        return paramiko.AUTH_FAILED
    
    def check_auth_publickey(self, username, key):
        pub_key_filename = database.user(username).public_key_filename
        try:
            LOG.info("checking %s" % pub_key_filename)
            assert os.path.exists(pub_key_filename)
            with open(pub_key_filename, 'rb') as pubkey:
                pubkey_data = pubkey.read().split(' ')[1]
        except paramiko.SSHException as e:
            LOG.error(e)
            return paramiko.AUTH_FAILED
        else:
            if key.get_base64() == pubkey_data:
                LOG.info("user successfully authed publickey")
                return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_shell_request(self, channel):
        self._shell_request_event.set()
        return True

    def check_channel_pty_request(self, channel, term,
                                  width, height,
                                  pixelwidth, pixelheight, modes):
        return True

    def wait_for_event(self, timeout=10):
        self._shell_request_event.wait(timeout)
        if not self._shell_request_event.is_set():
            return False
        return True
