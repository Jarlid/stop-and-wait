import socket

from config import *
from engine import send, recv, say_hi

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client.settimeout(TIMEOUT)
address = ('127.0.0.1', PORT)

if SENDER == Sender.CLIENT:
    with open(IN_FILE, 'r') as file:
        send(client, file.read(), address)
else:
    say_hi(client, address)
    client.settimeout(None)
    received = recv(client)
    with open(OUT_FILE, 'w') as file:
        file.write(received)
