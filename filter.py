import atexit
import ctypes as ct
import time
import threading
import socket
import sys
import os

from bcc import BPF

DEVICE = sys.argv[1]
CONFIG_SOCKET_FILE = sys.argv[2]


class Config(ct.Structure):
    _fields_ = [
        ("should_drop", ct.c_int),
        ("source_port", ct.c_int)
    ]


def toggle_drop():
    if os.path.exists(CONFIG_SOCKET_FILE):
        os.unlink(CONFIG_SOCKET_FILE)
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(CONFIG_SOCKET_FILE)
    zero = ct.c_int(0)
    while True:
        server.listen(1)
        conn, addr = server.accept()
        datagram = conn.recv(1024)
        print(datagram)
        should_drop, source_port = datagram.split()
        source_port = int(source_port)
        should_drop = int(should_drop)
        cfg = Config(should_drop=should_drop, source_port=source_port)
        print(f"Received new packet drop config: {should_drop} / {source_port}")
        config[zero] = cfg


b = BPF(src_file="filter.c")
config = b["config"]

threading.Thread(target=toggle_drop, daemon=True).start()

fn = b.load_func("udpfilter", BPF.XDP)


b.attach_xdp(DEVICE, fn, 0)

try:
    b.trace_print()
except KeyboardInterrupt:
    pass

atexit.register(lambda: b.remove_xdp(DEVICE, 0))
