import SocketServer
import logging
import socket
from paramiko.py3compat import u

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
        except Exception as e:
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
            client = SSHClientConnection(self.request)
            cl_channel = client.get_channel(10)

            rhost, rport, alias = client.get_remote_address()

            rport = int(rport)
            alias = 'user'
            LOG.info("connecting to remote endpoint on %s %d" % (rhost, rport))

            endpoint = SSHRemoteClient(alias, (rhost, rport))
            if endpoint.is_active():
                ep_channel = endpoint.get_channel()
                ep_channel.get_pty()
                ep_channel.invoke_shell()
                
                LOG.info("connected to endpoint channel.")

            # import 
                
            while True:
                r, w, e = select([cl_channel, ep_channel], [], [])
                if cl_channel in r:
                    data = u(cl_channel.recv(1024))
                    if len(data) == 0:
                        LOG.info("lost connection to client.")
                        break
                    ep_channel.send(data)
                elif ep_channel in r:
                    data = u(ep_channel.recv(1024))
                    if len(data) == 0:
                        LOG.info("lost connection to endpoint.")
                        break
                    cl_channel.send(data)


            # self.server.inputs.extend([cl_channel, ep_channel])
            # self.server.outputs.extend([cl_channel, ep_channel])
            
        except Exception as e:
            LOG.exception(e)
            cl_channel.close()
            ep_channel.close()
            raise RuntimeWarning("Failed to connect client")
        

if __name__ == "__main__":
    import sys
    HOST, PORT = "localhost", int(sys.argv[1])

    # Create the server, binding to localhost on port 9999
    LOG.info("Creating %d port on %s" % (PORT, HOST))
    server = SocketServer.TCPServer((HOST, PORT), SSHHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C

    server.serve_forever()
    server.server_close()

