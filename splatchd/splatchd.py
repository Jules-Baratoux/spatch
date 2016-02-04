import sys
import socket
import select
import logging
import paramiko
from server_handler import ServerHandler


logging.basicConfig(format='[%(levelname)-7s]::[%(name)-20s] %(message)s',
                    level=logging.DEBUG)

LOG = logging.getLogger('spatch')
# from binascii import hexlify
# from paramiko.py3compat import b, u, decodebytes


def load_host_key(filename='/home/jack/.ssh/id_rsa'):
    return paramiko.RSAKey(filename=filename)


class ClientServer:

    def __init__(self, socket, address):

        self._socket = socket
        self._hostname = address[0]
        self._port = address[1]
        try:
            self._transport = paramiko.Transport(self._socket)

            self._transport.add_server_key(load_host_key())
            self._server = ServerHandler()

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
        LOG.info("creating socket...")
        srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        LOG.info("binding to port %d" % 2200)
        srv_sock.bind(('', 2200))
    except:
        LOG.error("Failed to create server socket.")
        sys.exit(0)

    try:
        srv_sock.listen(50)
        LOG.info("listening...")
    except:
        LOG.error("Failed to listen.")
        sys.exit(0)

    rlist = [srv_sock]
    
    while True:
        LOG.info("waiting for something...")
        r, w, x = select.select(rlist, [], [])
        if srv_sock in r:
            client_sock, client_addr = srv_sock.accept()
            LOG.info("Client connected from %s on port %d" % (client_addr[0],
                                                              client_addr[1]))
            try:
                client = ClientServer(client_sock, client_addr)
                channel = client.get_channel(3)
                # do stuff
                # channel.close()
            except Exception as e:
                LOG.error("client failed to connect %s" % e)
                # Client()
        # else do other socket stuff
        
