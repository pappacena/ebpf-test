# ebpf-test
Linux UDP packet filtering tests using eBPF


Runnning packet generator:

```
python3 send_pkts.py localhost 5555
```


Running packet receiver:

```
python3 recv.py localhost 5555
```


Running filter BPF:

```
sudo python3 filter.py
```


Enable packet filtering:

```
sudo python3 set_config.py 1
```


Disabling packet filtering:

```
sudo python3 set_config.py 0
```
