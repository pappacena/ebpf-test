import socket
import sys
from time import sleep, time_ns

host = sys.argv[1]
port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))
print('ok')
i = 0
while True:
    sock.recvmsg(128)
    i += 1
    if i % 1000 == 0:
        sys.stdout.write('.')
        sys.stdout.flush()
        i = 0
