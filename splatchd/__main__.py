import SocketServer
import logging
import socket
import threading
from binascii import hexlify

import paramiko
from select import select
from paramiko import SSHException
from paramiko.py3compat import u, decodebytes

logging.basicConfig(format='[%(levelname)-7s]::[%(name)-20s] %(message)s', level=logging.DEBUG)

log = logging.getLogger('spatch')

BUFSIZE = 1024
DO_GSS_API_KEY_EXCHANGE = True
DOMAIN_NAME = ""
RSAKEY = paramiko.RSAKey(filename='test_rsa.key')
TRANSPORT_ACCEPT_TIMEOUT = 20  # None == no timeout
SHELL_REQUEST_TIMEOUT = 10  # After authentication


class SSHServer(paramiko.ServerInterface):
    # 'data' is the output of base64.encodestring(str(key))
    # (using the "user_rsa_key" files)
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
        if (username == 'robey') and (password == 'foo'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        print('Auth attempt with key: ' + u(hexlify(key.get_fingerprint())))
        if (username == 'robey') and (key == self.good_pub_key):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_gssapi_with_mic(self, username,
                                   gss_authenticated=paramiko.AUTH_FAILED,
                                   cc_file=None):
        """
        .. note::
            We are just checking in `AuthHandler` that the given user is a
            valid krb5 principal! We don't check if the krb5 principal is
            allowed to log in on the server, because there is no way to do that
            in python. So if you develop your own SSH server with paramiko for
            a certain platform like Linux, you should call ``krb5_kuserok()`` in
            your local kerberos library to make sure that the krb5_principal
            has an account on the server and is allowed to log in as a user.

        .. seealso::
            `krb5_kuserok() man page
            <http://www.unix.com/man-page/all/3/krb5_kuserok/>`_
        """
        if gss_authenticated == paramiko.AUTH_SUCCESSFUL:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_gssapi_keyex(self, username,
                                gss_authenticated=paramiko.AUTH_FAILED,
                                cc_file=None):
        if gss_authenticated == paramiko.AUTH_SUCCESSFUL:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def enable_auth_gssapi(self):
        UseGSSAPI = True
        GSSAPICleanupCredentials = False
        return UseGSSAPI

    def get_allowed_auths(self, username):
        return 'gssapi-keyex,gssapi-with-mic,password,publickey'

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth,
                                  pixelheight, modes):
        return True


class SSHClientConnection(object):

    def __init__(self, transport, channel, socket, address):
        try:
            # socket is the TCP socket connected to the client
            # channel.send('\r\n\r\nWelcome to my dorky little BBS!\r\n\r\n')
            # channel.send('We are on fire all the time!  Hooray!  Candy corn for everyone!\r\n')
            # channel.send('Happy birthday to Robot Dave!\r\n\r\n')
            # channel.send('Username: ')
            # f = channel.makefile('rU')
            # username = f.readline().strip('\r\n')
            # channel.send('\r\nI don\'t like you, ' + username + '.\r\n')

            self.client_channel = channel
            self.server_channel = ← connect to the end-point server channel and store it

        except:
            raise
        finally:
            channel.close() ← do not forget to close when the connection is not needed anymore

    def readable(self, channel):

        if channel is self.client_channel:
            self.client_server.buffer += self.client_channel.recv(BUFSIZE)
        else:
            message = self.client_channel.recv(BUFSIZE)

        message = i.recv(BUFSIZE)
        return o.send(message)

    def writable(self, channel):

        if channel is self.client_channel:
            i = channel
            o = self.server_channel
        else:
            i = self.server_channel
            o = channel

        message = i.recv(BUFSIZE)
        return o.send(message)



ssh_server = SSHServer()


class SSHHandler(SocketServer.BaseRequestHandler):

    def handle(self):

        transport = paramiko.Transport(self.request, gss_kex=DO_GSS_API_KEY_EXCHANGE)
        transport.set_gss_host(socket.getfqdn(DOMAIN_NAME))
        try:
            transport.load_server_moduli()
        except:
            raise RuntimeError('moduli loading failed: gex will be unsupported')

        transport.add_server_key(RSAKEY)

        try:
            transport.start_server(server=ssh_server)
        except SSHException:
            raise RuntimeError("ssh negotiation failed")

        channel = transport.accept(TRANSPORT_ACCEPT_TIMEOUT)
        if channel:
            log.info('Authenticated!')
        else:
            raise RuntimeError('no channel opened: timeout after %is' % TRANSPORT_ACCEPT_TIMEOUT)

        ssh_server.event.wait(SHELL_REQUEST_TIMEOUT)
        if not ssh_server.event.is_set():
            raise RuntimeError('no shell request: timeout after %is' % SHELL_REQUEST_TIMEOUT)

        channel.connection = SSHClientConnection(transport, channel, self.request, self.client_address)
        self.server.inputs.append(channel)
        self.server.outputs.append(channel)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9998

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), SSHHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C

    server.inputs  = [server.socket]
    server.outputs = []
    message_queues = {}
    while server.inputs:
        readable, writable, exceptional = select(server.inputs, server.outputs, server.inputs)
        for s in readable:
            if s is server.socket:
                channel = server.handle_request()
                pass
           else:
               channel.connection.readable(channel)

    server.server_close()

