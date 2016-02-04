import sys
import socket
import threading
import paramiko
import traceback
import select
from binascii import hexlify

from paramiko.py3compat import b, u, decodebytes

import termios
import tty


def load_host_key(filename='/home/jack/.ssh/id_rsa'):
    return paramiko.RSAKey(filename=filename)


class SplatchServer(paramiko.ServerInterface):

    data = (b'AAAAB3NzaC1yc2EAAAABIwAAAIEAyO4it3fHlmGZWJaGrfeHOVY7RWO3P9M7hp'
            b'fAu7jJ2d7eothvfeuoRFtJwhUmZDluRdFyhFY/hFAh76PJKGAusIqIQKlkJxMC'
            b'KDqIexkgHAfID/6mqvmnSJf0b5W8v5h2pI/stOSwTQ+pxVhwJ9ctYDhRSlF0iT'
            b'UWT10hcuO4Ks8=')

    good_pub_key = paramiko.RSAKey(data=decodebytes(data))
    
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
        
    def check_auth_password(self, username, password):

        # db here
        if (username == 'jack') and (password == 'foo'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_interactive(self, username, submethods):
        
        print username
        return paramiko.AUTH_FAILED
    
    def check_auth_publickey(self, username, key):
        print('Auth attempt with key: ' + u(hexlify(key.get_fingerprint())))
        if (username == 'robey') and (key == self.good_pub_key):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
        
    def get_allowed_auths(self, username):
        return 'password, keyboard-interactive'
        
    def check_channel_shell_request(self, channel):
        self.event.set()
        return True
    
    def check_channel_pty_request(self, channel,
                                  term, width, height, pixelwidth,
                                  pixelheight, modes):
        return True


class ClientServer:

    def __init__(self, socket, address):

        self._socket = socket
        self._hostname = address[0]
        self._port = address[1]
        try:
            self._transport = paramiko.Transport(self._socket)

            self._transport.add_server_key(load_host_key())
            self._server = SplatchServer()

            self._transport.start_server(server=self._server)
        except paramiko.SSHException:
            raise Exception("ssh negotiation failed.")
        except:
            raise Exception("failed to init client")
        
    def get_channel(self, timeout=3):
        channel = self._transport.accept(timeout)
        if channel is None:
            raise Exception("no channel opened. timeout...")
        return channel

if __name__ == "__main__":

    try:
        srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv_sock.bind(('', 2200))
    except:
        print "Failed to bind server socket."
        sys.exit(0)

    try:
        srv_sock.listen(50)
    except:
        print "Failed to listen."
        sys.exit(0)

    rlist = [srv_sock]

    while True:
        r, w, x = select.select(rlist, [], [])

        if srv_sock in r:
            client_sock, client_addr = srv_sock.accept()
            print "connection from %s on %d" % (client_addr[0], client_addr[1])
            try:
                client = ClientServer(client_sock, client_addr)
                channel = client.get_channel(3)
                # do stuff
                channel.close()
            except Exception as e:
                print "Failed to connect client"
                # Client()
        # else do other socket stuff
        
