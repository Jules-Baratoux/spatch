import logging
import threading

import paramiko
import database

LOG = logging.getLogger('spatch')


def query_server_selection(granted_servers):

    info = """Enter an endpoint you wish to connect to:\n\n{}\n"""

    server_list_fmt = "- {hostname:>5}:{port} as {alias}"
    L = []
    for server in granted_servers:
        L.append(server_list_fmt.format(hostname=server[0],
                                        port=server[1], alias=server[2]))
    info = info.format('\n'.join(L))
    q = paramiko.InteractiveQuery("", info)

    q.add_prompt("Enter the server's hostname: ", echo=True)
    return q


class ServerHandler(paramiko.ServerInterface):

    def __init__(self):
        self._allowed = set(['keyboard-interactive', 'publickey', 'password'])

        self._shell_request_event = threading.Event()
        
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
        
    def check_auth_password(self, username, password):

        # db here
        if (username == 'jack') and (password == 'foo'):
            return paramiko.AUTH_SUCCESSFUL
            # return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_interactive(self, username, submethods):
        self._granted = database.granted_servers(username)
        if len(self._granted) == 0:
            return paramiko.AUTH_FAILED
        return query_server_selection(self._granted)

    def check_auth_interactive_response(self, responses):
        for host, _, alias in self._granted:
            if host == responses[0]:
                self._allowed.pop()
                return paramiko.AUTH_PARTIALLY_SUCCESSFUL
        return paramiko.AUTH_FAILED
    
    def check_auth_publickey(self, username, key):
        # print('Auth attempt with key: ' + u(hexlify(key.get_fingerprint())))
        # load db
        if (username == 'robey') and (key == self.good_pub_key):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
        
    def get_allowed_auths(self, username):
        return ','.join(self._allowed)

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
