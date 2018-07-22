#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import socket
import time

obj = socket.socket()

obj.connect(("127.0.0.1",8080))

ret_bytes = obj.recv(1024)
ret_str = str(ret_bytes,encoding="utf-8")
print(ret_str)

while True:
    inp = input("command >>>")
    if inp == "exit":
        obj.sendall(bytes(inp, encoding="utf-8"))
        time.sleep(1)
        break
    else:
        obj.sendall(bytes(inp, encoding="utf-8"))
        ret_bytes = obj.recv(1024)
        ret_str = str(ret_bytes,encoding="utf-8")
        print(ret_str)

# obj.close()