import socket
import sys
from time import sleep, time_ns

host = sys.argv[1]
port = int(sys.argv[2])
destination = (host, port)
msg = b"some-message"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cycle_ms = 4
i = 0
while True:
    start = time_ns()
    for _ in range(64):
        sock.sendto(msg, destination)
        i += 1
        if i % 1000 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()
            i = 0
    elapsed_ms = (time_ns() - start) / 1_000_000
    if elapsed_ms > cycle_ms:
        continue
    sleep((cycle_ms - elapsed_ms) / 1000)
    
