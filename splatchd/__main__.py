import SocketServer
import logging
import socket
from paramiko.py3compat import u
import threading
import paramiko
from select import select

from remote import SSHRemoteClient
from server_handler import ServerHandler


logging.basicConfig(
    format='[%(levelname)-7s]::[%(name)-5s] %(message)s',
    level=logging.DEBUG)

LOG = logging.getLogger('spatch')

BUFSIZE = 1024
DO_GSS_API_KEY_EXCHANGE = True
DOMAIN_NAME = ""
RSAKEY = paramiko.RSAKey(filename='keys/splatch')
TRANSPORT_ACCEPT_TIMEOUT = 20  # None == no timeout
SHELL_REQUEST_TIMEOUT = 10  # After authentication


class SSHClientConnection(object):

    def __init__(self, sock):
        self._socket = sock
        # self._client_address
        try:
            self._transport = paramiko.Transport(self._socket)
            
            self._transport.add_server_key(RSAKEY)
            self._server = ServerHandler()
            self._transport.start_server(server=self._server)
        except paramiko.SSHException:
            raise RuntimeError("ssh negotiation failed.")
        except Exception:
            raise RuntimeError("failed to init client")

    def get_channel(self, timeout=3):
        channel = self._transport.accept(timeout)

        if channel is None:
            raise Exception("no channel opened. timeout...")
        if self._server.wait_for_event() is False:
            raise Exception("client did not ask for shell.")
        return channel

    def get_remote_address(self):
        return self._server.remote_address


class SSHHandler(SocketServer.BaseRequestHandler):

    def handle(self):

        try:
            print "TEST"
            client = SSHClientConnection(self.request)
            client_channel = client.get_channel(10)    
            rhost, rport, alias = client.get_remote_address()

            rport = int(rport)
            LOG.info("connecting to remote endpoint on %s %d" % (rhost, rport))

            endpoint = SSHRemoteClient(alias, (rhost, rport))
            endpoint_channel = endpoint.get_channel()
            if not endpoint.is_active():
                raise RuntimeError("Could not get endpoint channel")
                
            LOG.info("connected to endpoint channel.")
            endpoint_channel.get_pty()
            endpoint_channel.invoke_shell()

            while True:
                r, w, e = select([client_channel, endpoint_channel], [], [])
                if client_channel in r:
                    data = u(client_channel.recv(1024))
                    if len(data) == 0:
                        LOG.info("lost connection to client.")
                        break
                    endpoint_channel.send(data)
                elif endpoint_channel in r:
                    data = u(endpoint_channel.recv(1024))
                    if len(data) == 0:
                        LOG.info("lost connection to endpoint.")
                        break
                    client_channel.send(data)
            client_channel.close()
            endpoint_channel.close()

        except Exception as e:
            LOG.exception(e)
            raise RuntimeWarning("Failed to connect client")


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    import sys
    HOST, PORT = "localhost", int(sys.argv[1])

    # Create the server, binding to localhost on port 9999
    LOG.info("Creating %d port on %s" % (PORT, HOST))
    server = ThreadedTCPServer((HOST, PORT), SSHHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C

    server.serve_forever()
    server.shutdown()
    server.server_close()

