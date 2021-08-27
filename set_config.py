import socket
import sys

filename = sys.argv[1]
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect(filename)
sock.sendall(sys.argv[2].encode('utf8'))
