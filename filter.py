from bcc import BPF
import ctypes as ct
import time
import threading
import socket
import os

CONFIG_SOCKET_FILE = "/tmp/lg-drop-udp.sock"

class Config(ct.Structure):
  _fields_ = [("should_drop", ct.c_int)]


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
    new_value = int(datagram)
    try:
      current = config[zero].should_drop
    except KeyError:
      current = zero
    cfg = Config(should_drop=new_value)
    print(f"Received new packet drop config: {new_value} (used to be {current})")
    config[zero] = cfg
    time.sleep(0.5)


b = BPF(src_file="filter.c")
config = b["config"]

t = threading.Thread(target=toggle_drop)
t.start()

device = "lo"
fn = b.load_func("udpfilter", BPF.XDP)


b.attach_xdp(device, fn, 0)

try:
  b.trace_print()
except KeyboardInterrupt:
  pass

b.remove_xdp(device, 0)
