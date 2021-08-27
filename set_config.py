import socket
import sys

filename = "/tmp/lg-drop-udp.sock"
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect(filename)
sock.sendall(sys.argv[1].encode('utf8'))
