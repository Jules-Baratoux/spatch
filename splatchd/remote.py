import sys
import select
import socket
import paramiko

import tty, termios

DEFAULT_KEY_PATH = "./keys/splatch"


class RemoteSSHClient(object):
    
    def __init__(self, username, raddress):

        self._active = False
        self._remote_host = raddress[0]
        self._remote_port = raddress[1]
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self._sock.settimeout(3)
            self._sock.connect((self._remote_host, self._remote_port))
            self._sock.settimeout(None)
            # self._session = paramiko.SSHClient()

            self._transport = paramiko.Transport(self._sock)
            self._transport.start_client()

            self._key = self._transport.get_remote_server_key()
            if not self.is_known(self._key):
                raise Exception("unkown host")

            self.authenticate(username)
            self._active = True
        except socket.timeout:
            print "socket timed out."
            self._active = False
        except Exception as e:
            print e
        
    @classmethod
    def is_known(cls, key):
        return True

    def is_active(self):
        return self._active
    
    def authenticate(self, username, key_path=DEFAULT_KEY_PATH):
        # authenticates using splatch
        # private key which is configured on the rmeote servers
        try:
            private = paramiko.RSAKey.from_private_key_file(key_path)
            self._transport.auth_publickey(username, private)
        except paramiko.PasswordRequiredException:
            pass
        except Exception as e:
            print e
        finally:
            if not self._transport.is_authenticated():
                raise Exception("faield to authenticate")

    def start_session(self):
        channel = self._transport.open_session()
        return channel


REMOTE_HOST_ADDRESS = list([
    {
        'username': 'splatch',
        'hostname': 'splatch',
        'port': 8000
    },
    {
        'username': 'example',
        'hostname': 'example.com',
        'port': 22
    }

])
        
        
if __name__ == "__main__":

    remote_hosts = []
    try:
        for rhost in REMOTE_HOST_ADDRESS:
            print "Connecting to %s on port %d" % (rhost['hostname'],
                                                   rhost['port'])
            hsock = RemoteSSHClient(rhost['username'], rhost['hostname'],
                                    rhost['port'])
            if hsock.is_active():
                print "connected"
                remote_hosts.append(hsock)
            else:
                print "failed to connect %s on port %d" % (rhost['hostname'],
                                                           rhost['port'])
    except KeyError as e:
        raise Exception("config error")
    except Exception as e:
        print e
    finally:
        pass
        for rhost in remote_hosts:
            # get the socket
            if rhost.is_active():
                channel = rhost.start_session()
                print "Opened channel %s" % channel
                channel = rhost.start_session()
                print "Opened channel %s" % channel
                # do something with socket
                channel.close()  # close it
    # c.start()
    # c.stop()
