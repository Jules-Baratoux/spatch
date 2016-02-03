import sys
import socket
import threading
import paramiko
import traceback
import select
from binascii import hexlify

from paramiko.py3compat import b, u, decodebytes


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
    
    def check_auth_publickey(self, username, key):
        print('Auth attempt with key: ' + u(hexlify(key.get_fingerprint())))
        if (username == 'robey') and (key == self.good_pub_key):
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
        
    def check_channel_pty_request(self, channel,
                                  term, width, height, pixelwidth,
                                  pixelheight, modes):
        return True
    
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

    # remote = paramiko.SSHClient()
    
    while True:

        r, w, x = select.select(rlist, [], [])
        
        client_sock, client_addr = srv_sock.accept()

        print "connection %s : %d" % (client_addr[0], client_addr[1])
        try:
            if srv_sock in r:

                print "Request"
                # client(transport, channel)
                transport = paramiko.Transport(client_sock, gss_kex=False)
                transport.load_server_moduli()
                transport.add_server_key(load_host_key())
                transport.start_server(server=SplatchServer())
                print transport.is_active()
                channel = transport.accept(20)
                if channel is None:
                    print "No channel"

                rlist.append(channel)
                print "Authenticated!"
                channel.send("Please select a server:")
            else:
                print "TEST"
                # for channel in r:
                
                # if remote_chan is None:
                #     print "Rejected"
                # print channel
            
                
            
            # transport.request_port_forward('192.168.1.72', 8000)
            # # transport.open_forwarded_tcpip_channel(
            # #     ('localhost', 6000), ('192.168.1.72', 8000)) 
            # # transport.open_channel("forwarded-tcpip",
            # #                        dest_addr=('192.168.1.72', 8000),
            # #                        src_addr=('localhost', 2200))
            
        except Exception as e:
            print e
            traceback.print_exc()
            sys.exit(1)
